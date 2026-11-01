"""Apply selected checkbox settings."""

import argparse
import contextlib
import importlib
import json
import sys
from pathlib import Path
from typing import Any


def load_profile(profile_path: Path) -> dict[str, Any]:
    """Validate a settings profile."""
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    if not isinstance(profile, dict) or set(profile) != {'doctype', 'values'}:
        raise ValueError('Profile requires exactly doctype and values')
    if not isinstance(profile['doctype'], str) or not profile['doctype']:
        raise ValueError('doctype must be a nonempty string')
    values = profile['values']
    if not isinstance(values, dict) or not values:
        raise ValueError('values must be a nonempty object')
    for field, value in values.items():
        if not field or type(value) not in (bool, int) or value not in (0, 1):
            raise ValueError('Settings must be named checkbox values 0 or 1')
    return {'doctype': profile['doctype'], 'values': values}


def apply_profile(
    frappe: Any, profile: dict[str, Any], apply: bool = False
) -> dict[str, Any]:
    """Validate and reconcile checkbox settings."""
    doctype = profile['doctype']
    meta = frappe.get_meta(doctype)
    if not meta.issingle:
        raise ValueError('Only Single DocTypes are supported')
    for field in profile['values']:
        definition = meta.get_field(field)
        if definition is None:
            raise ValueError(f'Unknown field: {doctype}.{field}')
        if definition.fieldtype != 'Check' or definition.read_only:
            raise ValueError(f'Not an editable checkbox: {doctype}.{field}')
    document = frappe.get_doc(doctype)
    document.check_permission('read')
    changes = {
        field: {
            'current': frappe.utils.cint(document.get(field)),
            'desired': int(value),
        }
        for field, value in profile['values'].items()
        if frappe.utils.cint(document.get(field)) != int(value)
    }
    if apply:
        document.check_permission('write')
        if changes:
            for field, change in changes.items():
                document.set(field, change['desired'])
            document.save()
            persisted = frappe.get_doc(doctype)
            for field, value in profile['values'].items():
                if frappe.utils.cint(persisted.get(field)) != int(value):
                    raise RuntimeError(f'Readback failed: {doctype}.{field}')
            frappe.db.commit()
    return {'doctype': doctype, 'applied': apply, 'changes': changes}


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse explicit target arguments."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True)
    parser.add_argument('--sites-path', required=True, type=Path)
    parser.add_argument('--user', required=True)
    parser.add_argument(
        '--profile',
        type=Path,
        default=Path(__file__).parent / 'settings' / 'shared.json',
    )
    parser.add_argument('--apply', action='store_true')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run in the native Bench context."""
    args = parse_args(argv)
    profile = load_profile(args.profile.resolve())
    sites_path = args.sites_path.resolve(strict=True)
    if Path(args.site).name != args.site or args.site in ('.', '..'):
        raise ValueError('site must be a site directory name')
    if not (sites_path / args.site / 'site_config.json').is_file():
        raise ValueError('Target site configuration does not exist')
    with contextlib.chdir(sites_path):
        frappe: Any = importlib.import_module('frappe')
        frappe.init(site=args.site, sites_path='.')
        try:
            frappe.connect()
            frappe.set_user(args.user)
            result = apply_profile(frappe, profile, apply=args.apply)
        except Exception:
            if getattr(frappe.local, 'db', None):
                frappe.db.rollback()
            raise
        finally:
            frappe.destroy()
    print(json.dumps(result, sort_keys=True))
    return 0 if args.apply or not result['changes'] else 1


if __name__ == '__main__':
    sys.exit(main())
