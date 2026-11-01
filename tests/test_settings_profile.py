"""Check shared settings contracts."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from scripts import apply_settings as settings


class SettingsProfileTests(unittest.TestCase):
    """Check profile and permission boundaries."""

    def load(self, content):
        """Load a temporary profile."""
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / 'profile.json'
            filename.write_text(json.dumps(content), encoding='utf-8')
            return settings.load_profile(filename)

    def runtime(self, current=0):
        """Create an observable settings boundary."""
        document = Mock()
        document.get.return_value = current
        definition = SimpleNamespace(fieldtype='Check', read_only=False)
        meta = Mock(issingle=True)
        meta.get_field.return_value = definition
        runtime = Mock()
        runtime.get_meta.return_value = meta
        runtime.get_doc.return_value = document
        runtime.utils.cint.side_effect = lambda value: int(value or 0)
        return runtime, document

    def test_rejects_non_checkbox_values(self):
        for invalid in ['1', 2, None, {}, []]:
            with self.subTest(value=invalid), self.assertRaises(ValueError):
                self.load({'doctype': 'Settings', 'values': {'flag': invalid}})

    def test_rejects_unknown_profile_keys(self):
        with self.assertRaises(ValueError):
            self.load(
                {'doctype': 'Settings', 'values': {'flag': 1}, 'run': 'x'}
            )

    def test_check_reports_drift_without_writing(self):
        runtime, document = self.runtime()
        result = settings.apply_profile(
            runtime,
            {'doctype': 'Settings', 'values': {'flag': 1}},
        )
        self.assertEqual(
            result['changes']['flag'], {'current': 0, 'desired': 1}
        )
        document.set.assert_not_called()
        document.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_validates_every_field_before_mutation(self):
        runtime, document = self.runtime()
        runtime.get_meta.return_value.get_field.side_effect = [
            SimpleNamespace(fieldtype='Check', read_only=False),
            None,
        ]
        with self.assertRaises(ValueError):
            settings.apply_profile(
                runtime,
                {'doctype': 'Settings', 'values': {'valid': 1, 'missing': 1}},
                apply=True,
            )
        document.save.assert_not_called()
        runtime.get_doc.assert_not_called()

    def test_rejects_protected_and_non_checkbox_fields(self):
        for fieldtype, read_only in [('Password', False), ('Check', True)]:
            runtime, document = self.runtime()
            runtime.get_meta.return_value.get_field.return_value = (
                SimpleNamespace(fieldtype=fieldtype, read_only=read_only)
            )
            with self.assertRaises(ValueError):
                settings.apply_profile(
                    runtime,
                    {'doctype': 'Settings', 'values': {'flag': 1}},
                    apply=True,
                )
            document.save.assert_not_called()

    def test_denied_write_does_not_save(self):
        runtime, document = self.runtime()
        document.check_permission.side_effect = [None, PermissionError()]
        with self.assertRaises(PermissionError):
            settings.apply_profile(
                runtime,
                {'doctype': 'Settings', 'values': {'flag': 1}},
                apply=True,
            )
        document.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_matching_profile_does_not_save_again(self):
        runtime, document = self.runtime(current=1)
        result = settings.apply_profile(
            runtime,
            {'doctype': 'Settings', 'values': {'flag': 1}},
            apply=True,
        )
        self.assertEqual(result['changes'], {})
        document.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_readback_failure_prevents_commit(self):
        runtime, document = self.runtime(current=0)
        with self.assertRaises(RuntimeError):
            settings.apply_profile(
                runtime,
                {'doctype': 'Settings', 'values': {'flag': 1}},
                apply=True,
            )
        document.save.assert_called_once()
        runtime.db.commit.assert_not_called()

    def test_rejects_non_single_document_before_reading_it(self):
        runtime, document = self.runtime()
        runtime.get_meta.return_value.issingle = False
        with self.assertRaises(ValueError):
            settings.apply_profile(
                runtime,
                {'doctype': 'Settings', 'values': {'flag': 1}},
                apply=True,
            )
        runtime.get_doc.assert_not_called()
        document.save.assert_not_called()


if __name__ == '__main__':
    unittest.main()
