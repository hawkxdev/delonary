"""Check list profile boundaries."""

import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import Mock

from scripts import apply_list_view as lists


class ListProfileTests(unittest.TestCase):
    """Verify presentation preflight behavior."""

    def profile(self):
        """Return a synthetic list contract."""
        return {
            'doctype': 'Example',
            'columns': [
                {'fieldname': 'title', 'label': 'Work'},
                {'fieldname': 'person', 'label': 'Contact'},
            ],
        }

    def load(self, profile):
        """Read a temporary profile."""
        with tempfile.TemporaryDirectory() as directory:
            filename = Path(directory) / 'profile.json'
            filename.write_text(json.dumps(profile), encoding='utf-8')
            return lists.load_profile(filename)

    def subject_profile(self):
        """Return an independent subject contract."""
        profile = self.profile()
        profile['subject'] = {
            'fieldname': 'custom_work_name',
            'insert_after': 'person',
        }
        profile['columns'][0]['fieldname'] = 'custom_work_name'
        return profile

    def runtime(self):
        """Create an observable native boundary."""
        fields = {
            name: SimpleNamespace(
                label=label,
                fieldtype=fieldtype,
                hidden=False,
                is_virtual=False,
                in_list_view=1,
                read_only=False,
            )
            for name, label, fieldtype in [
                ('title', 'Work', 'Data'),
                ('person', 'Contact', 'Link'),
            ]
        }
        meta = SimpleNamespace(
            issingle=False,
            title_field='title',
            get_field=fields.get,
            fields=fields,
        )
        settings = Mock()
        settings.get.return_value = json.dumps(
            [{'fieldname': 'title'}, {'fieldname': 'person', 'width': 180}]
        )
        settings.is_new.return_value = False
        runtime = Mock()
        runtime.get_meta.return_value = meta
        runtime.get_doc.return_value = settings
        runtime.utils.cint.side_effect = int
        return runtime, settings, meta

    def test_rejects_duplicate_columns(self):
        profile = self.profile()
        profile['columns'].append(profile['columns'][0])
        with self.assertRaises(ValueError):
            self.load(profile)

    def test_rejects_subject_defaults_and_noncustom_names(self):
        for changes in [{'default': 'Person'}, {'fieldname': 'title'}]:
            profile = self.subject_profile()
            profile['subject'].update(changes)
            with self.subTest(changes=changes), self.assertRaises(ValueError):
                self.load(profile)

    def test_subject_must_match_the_first_column(self):
        profile = self.subject_profile()
        profile['columns'].reverse()
        with self.assertRaises(ValueError):
            self.load(profile)

    def test_missing_subject_is_planned_without_schema_writes(self):
        runtime, settings, meta = self.runtime()
        runtime.db.exists.side_effect = lambda dt, name: (
            dt == 'List View Settings'
        )
        result = lists.apply_profile(runtime, self.subject_profile())
        self.assertEqual(
            result['changes']['title_field'],
            {'current': 'title', 'desired': 'custom_work_name'},
        )
        self.assertIn('subject_field', result['changes'])
        runtime.new_doc.assert_not_called()
        settings.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_invalid_later_field_prevents_subject_creation(self):
        runtime, settings, meta = self.runtime()
        runtime.db.exists.return_value = False
        profile = self.subject_profile()
        profile['columns'][1]['fieldname'] = 'missing'
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, profile, apply=True)
        runtime.new_doc.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_subject_requires_an_existing_anchor(self):
        runtime, settings, meta = self.runtime()
        runtime.db.exists.return_value = False
        profile = self.subject_profile()
        profile['subject']['insert_after'] = 'missing'
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, profile, apply=True)
        runtime.new_doc.assert_not_called()

    def test_rejects_a_readonly_existing_subject(self):
        runtime, settings, meta = self.runtime()
        meta.fields['custom_work_name'] = SimpleNamespace(
            fieldtype='Data',
            hidden=0,
            is_virtual=0,
            read_only=1,
        )
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, self.subject_profile(), apply=True)
        settings.save.assert_not_called()

    def test_rejects_empty_labels_and_unknown_keys(self):
        for column in [
            {'fieldname': 'title', 'label': ' '},
            {'fieldname': 'title', 'label': 'Work', 'execute': 'x'},
        ]:
            profile = self.profile()
            profile['columns'][0] = column
            with self.subTest(column=column), self.assertRaises(ValueError):
                self.load(profile)

    def test_checks_later_fields_before_any_write(self):
        runtime, settings, meta = self.runtime()
        profile = self.profile()
        profile['columns'][0]['label'] = 'Changed'
        profile['columns'][1]['fieldname'] = 'missing'
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, profile, apply=True)
        settings.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_rejects_invalid_widths(self):
        for width in [True, 0, -1, '420', None]:
            profile = self.profile()
            profile['columns'][0]['width'] = width
            with self.subTest(width=width), self.assertRaises(ValueError):
                self.load(profile)

    def test_reports_only_requested_width_changes(self):
        runtime, settings, meta = self.runtime()
        profile = self.profile()
        profile['columns'][0]['width'] = 420
        changes = lists.inspect_profile(runtime, profile)
        self.assertEqual(
            changes,
            {'widths': {'title': {'current': None, 'desired': 420}}},
        )

    def test_rejects_replacing_the_native_first_field(self):
        runtime, settings, meta = self.runtime()
        profile = self.profile()
        profile['columns'].reverse()
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, profile, apply=True)
        settings.save.assert_not_called()

    def test_rejects_hidden_or_virtual_columns(self):
        for attribute in ['hidden', 'is_virtual']:
            runtime, settings, meta = self.runtime()
            setattr(meta.get_field('person'), attribute, True)
            with (
                self.subTest(attribute=attribute),
                self.assertRaises(ValueError),
            ):
                lists.apply_profile(runtime, self.profile(), apply=True)
            settings.save.assert_not_called()

    def test_matching_profile_preserves_width_and_does_not_save(self):
        runtime, settings, meta = self.runtime()
        result = lists.apply_profile(runtime, self.profile(), apply=True)
        self.assertEqual(result['changes'], {})
        settings.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_native_title_can_be_hidden_in_the_form(self):
        runtime, settings, meta = self.runtime()
        meta.get_field('title').hidden = True
        result = lists.apply_profile(runtime, self.profile())
        self.assertEqual(result['changes'], {})

    def test_native_title_cannot_be_virtual(self):
        runtime, settings, meta = self.runtime()
        meta.get_field('title').is_virtual = True
        with self.assertRaises(ValueError):
            lists.apply_profile(runtime, self.profile())

    def test_check_reports_order_drift_without_saving(self):
        runtime, settings, meta = self.runtime()
        settings.get.return_value = json.dumps([{'fieldname': 'title'}])
        result = lists.apply_profile(runtime, self.profile())
        self.assertEqual(
            result['changes']['columns'],
            {'current': ['title'], 'desired': ['title', 'person']},
        )
        settings.save.assert_not_called()
        runtime.db.commit.assert_not_called()

    def test_denied_apply_does_not_write(self):
        runtime, settings, meta = self.runtime()
        settings.check_permission.side_effect = [None, None, PermissionError()]
        with self.assertRaises(PermissionError):
            lists.apply_profile(runtime, self.profile(), apply=True)
        settings.save.assert_not_called()
        runtime.db.commit.assert_not_called()


if __name__ == '__main__':
    unittest.main()
