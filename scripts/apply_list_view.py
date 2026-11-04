"""Apply reviewed list presentation."""

import argparse
import contextlib
import importlib
import json
import re
import sys
from pathlib import Path
from types import SimpleNamespace
from typing import Any


def load_profile(profile_path: Path) -> dict[str, Any]:
    """Validate ordered list configuration."""
    profile = json.loads(profile_path.read_text(encoding='utf-8'))
    if (
        not isinstance(profile, dict)
        or not {'doctype', 'columns'} <= set(profile)
        or set(profile) - {'doctype', 'columns', 'subject'}
    ):
        raise ValueError(
            'Profile requires doctype, columns and optional subject'
        )
    if (
        not isinstance(profile['doctype'], str)
        or not profile['doctype'].strip()
    ):
        raise ValueError('doctype must be a nonempty string')
    columns = profile['columns']
    if not isinstance(columns, list) or not columns:
        raise ValueError('columns must be a nonempty list')
    names = set()
    for column in columns:
        if (
            not isinstance(column, dict)
            or not {'fieldname', 'label'} <= set(column)
            or set(column) - {'fieldname', 'label', 'width'}
        ):
            raise ValueError(
                'Columns require fieldname, label and optional width'
            )
        if any(
            not isinstance(column[key], str) or not column[key].strip()
            for key in ('fieldname', 'label')
        ):
            raise ValueError(
                'Column names and labels must be nonempty strings'
            )
        if column['fieldname'] in names:
            raise ValueError('Duplicate column fieldname')
        if 'width' in column and (
            type(column['width']) is not int or column['width'] <= 0
        ):
            raise ValueError('Column width must be a positive integer')
        names.add(column['fieldname'])
    if 'subject' in profile:
        subject = profile['subject']
        if not isinstance(subject, dict) or set(subject) != {
            'fieldname',
            'insert_after',
        }:
            raise ValueError('Subject requires fieldname and insert_after')
        if (
            not isinstance(subject['fieldname'], str)
            or not re.fullmatch(
                r'custom_[a-z][a-z0-9_]*', subject['fieldname']
            )
            or not isinstance(subject['insert_after'], str)
            or not subject['insert_after']
        ):
            raise ValueError('Subject requires a custom field and an anchor')
        if subject['fieldname'] != columns[0]['fieldname']:
            raise ValueError('Subject must be the first configured column')
    return profile


def list_settings(frappe: Any, doctype: str) -> Any:
    """Read permission checked list settings."""
    if frappe.db.exists('List View Settings', doctype):
        document = frappe.get_doc('List View Settings', doctype)
    else:
        document = frappe.new_doc('List View Settings')
        document.name = doctype
    document.check_permission('read')
    return document


def subject_field(frappe: Any, profile: dict[str, Any], meta: Any) -> Any:
    """Validate an explicit custom subject."""
    subject = profile.get('subject')
    if subject is None:
        return None
    name = subject['fieldname']
    field = meta.get_field(name)
    exists = frappe.db.exists('Custom Field', f'{profile["doctype"]}-{name}')
    if field is not None:
        if (
            not exists
            or field.fieldtype != 'Data'
            or field.hidden
            or field.read_only
            or field.is_virtual
        ):
            raise ValueError(f'Conflicting custom subject field: {name}')
        return field
    if exists or meta.get_field(subject['insert_after']) is None:
        raise ValueError(
            'Custom subject metadata or insertion anchor conflicts'
        )
    return SimpleNamespace(
        fieldname=name,
        fieldtype='Data',
        hidden=0,
        is_virtual=0,
        label=profile['columns'][0]['label'],
        in_list_view=1,
    )


def inspect_profile(frappe: Any, profile: dict[str, Any]) -> dict[str, Any]:
    """Compare effective list presentation."""
    doctype = profile['doctype']
    meta = frappe.get_meta(doctype, cached=False)
    if meta.issingle:
        raise ValueError('Single DocTypes have no record list')
    subject = subject_field(frappe, profile, meta)
    title_field = (
        subject.fieldname if subject is not None else meta.title_field
    )
    if profile['columns'][0]['fieldname'] != title_field:
        raise ValueError('The first column must be the native title field')
    changes = {}
    if subject is not None:
        if meta.get_field(subject.fieldname) is None:
            changes['subject_field'] = {
                'current': None,
                'desired': profile['subject'],
            }
        if meta.title_field != title_field:
            changes['title_field'] = {
                'current': meta.title_field,
                'desired': title_field,
            }
    for column in profile['columns']:
        name = column['fieldname']
        field = meta.get_field(name)
        if field is None and subject is not None and name == subject.fieldname:
            field = subject
        if field is None or field.fieldtype not in {'Data', 'Link'}:
            raise ValueError(f'Not a supported text or link field: {name}')
        if field.is_virtual or (field.hidden and name != title_field):
            raise ValueError(f'Not a visible stored field: {name}')
        for property_name, current, desired in [
            ('label', field.label, column['label']),
            ('in_list_view', frappe.utils.cint(field.in_list_view), 1),
        ]:
            if current != desired:
                changes[f'{name}.{property_name}'] = {
                    'current': current,
                    'desired': desired,
                }
    document = list_settings(frappe, doctype)
    rows = json.loads(document.get('fields') or '[]')
    if not isinstance(rows, list) or any(
        not isinstance(row, dict) or not isinstance(row.get('fieldname'), str)
        for row in rows
    ):
        raise ValueError('Existing list fields are malformed')
    current_order = [row['fieldname'] for row in rows]
    desired_order = [column['fieldname'] for column in profile['columns']]
    if current_order != desired_order:
        changes['columns'] = {
            'current': current_order,
            'desired': desired_order,
        }
    existing = {row['fieldname']: row for row in rows}
    widths = {
        column['fieldname']: {
            'current': existing.get(column['fieldname'], {}).get('width'),
            'desired': column['width'],
        }
        for column in profile['columns']
        if 'width' in column
        and existing.get(column['fieldname'], {}).get('width')
        != column['width']
    }
    if widths:
        changes['widths'] = widths
    return changes


def property_setter(
    frappe: Any,
    doctype: str,
    field: str | None,
    property_name: str,
    value: Any,
) -> Any:
    """Prepare a normal customization document."""
    mode = 'DocField' if field is not None else 'DocType'
    name = f'{doctype}-{field or "main"}-{property_name}'
    if frappe.db.exists('Property Setter', name):
        document = frappe.get_doc('Property Setter', name)
        if (
            document.doc_type != doctype
            or document.field_name != field
            or document.property != property_name
            or document.doctype_or_field != mode
        ):
            raise ValueError(f'Conflicting customization: {name}')
    else:
        document = frappe.new_doc('Property Setter')
        document.update(
            {
                'doctype_or_field': mode,
                'doc_type': doctype,
                'field_name': field,
                'property': property_name,
            }
        )
    document.check_permission('create' if document.is_new() else 'write')
    document.value = str(value)
    document.property_type = (
        'Check' if property_name == 'in_list_view' else 'Data'
    )
    document.flags.validate_fields_for_doctype = True
    return document


def custom_subject_document(frappe: Any, profile: dict[str, Any]) -> Any:
    """Prepare one stored subject field."""
    document = frappe.new_doc('Custom Field')
    document.update(
        {
            'dt': profile['doctype'],
            'fieldname': profile['subject']['fieldname'],
            'label': profile['columns'][0]['label'],
            'fieldtype': 'Data',
            'insert_after': profile['subject']['insert_after'],
            'in_list_view': 1,
        }
    )
    document.check_permission('create')
    return document


def apply_profile(
    frappe: Any, profile: dict[str, Any], apply: bool = False
) -> dict[str, Any]:
    """Reconcile labels and list order."""
    doctype = profile['doctype']
    changes = inspect_profile(frappe, profile)
    prepared_subject = False
    if apply:
        settings = list_settings(frappe, doctype)
        settings.check_permission('create' if settings.is_new() else 'write')
        subject_document = (
            custom_subject_document(frappe, profile)
            if 'subject_field' in changes
            else None
        )
        operations = []
        for key, change in changes.items():
            if key in {'columns', 'widths', 'subject_field'}:
                continue
            if key == 'title_field':
                field, property_name = None, 'title_field'
            else:
                field, property_name = key.rsplit('.', 1)
            operations.append(
                property_setter(
                    frappe, doctype, field, property_name, change['desired']
                )
            )
        if subject_document is not None:
            subject_document.save()
            frappe.db.commit()
            prepared_subject = True
        for document in operations:
            document.save()
        if {'columns', 'widths'} & changes.keys():
            existing = {
                row['fieldname']: row
                for row in json.loads(settings.get('fields') or '[]')
            }
            rows = []
            for column in profile['columns']:
                row = dict(existing.get(column['fieldname'], {}))
                row['fieldname'] = column['fieldname']
                if 'width' in column:
                    row['width'] = column['width']
                rows.append(row)
            settings.fields = json.dumps(rows, ensure_ascii=False)
            settings.save()
        if changes:
            frappe.clear_cache(doctype=doctype)
            if inspect_profile(frappe, profile):
                raise RuntimeError('List presentation readback failed')
            frappe.db.commit()
    return {
        'doctype': doctype,
        'applied': apply,
        'changes': changes,
        'prepared_subject': prepared_subject,
    }


def parse_args(argv: list[str] | None = None) -> argparse.Namespace:
    """Parse explicit operator targets."""
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--site', required=True)
    parser.add_argument('--sites-path', required=True, type=Path)
    parser.add_argument('--user', required=True)
    parser.add_argument('--profile', type=Path, required=True)
    parser.add_argument('--apply', action='store_true')
    return parser.parse_args(argv)


def main(argv: list[str] | None = None) -> int:
    """Run with the existing Bench runtime."""
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
                frappe.clear_cache(doctype=profile['doctype'])
            raise
        finally:
            frappe.destroy()
    print(json.dumps(result, ensure_ascii=False, sort_keys=True))
    return 0 if args.apply or not result['changes'] else 1


if __name__ == '__main__':
    sys.exit(main())
