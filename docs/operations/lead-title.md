# Independent Lead titles

[Issue #2](https://github.com/hawkxdev/delonary/issues/2) requires a work name first and a separate contact second. This requirement also applies to the Lead list. The [Lead profile](../../scripts/settings/lead-list.json) gives each Lead an editable work title without replacing the person's name.

## Field and presentation

The profile creates a stored Data custom_project_name field labelled 'Project Name', inserted after lead_name. It selects that field as the Lead DocType title and configures the default list:

| Field | Display label | Width in CSS pixels |
|---|---|---|
| custom_project_name | Project Name | 420 |
| lead_name | Contact | 180 |

For example, a Lead can show 'Marketplace integration' beside 'Alex Example'. Enter the work name in the form and use the normal Save action. The page heading and first list column use that work name; first_name, last_name and lead_name keep person identity. ERPNext still maintains its internal generated Lead.title, which is no longer the selected display title. No upstream controller is changed.

Profile labels and public examples use English source text. Frappe translates labels for the selected interface language through its existing translation catalog.

The new subject is optional and has no name-derived default. Existing records are not renamed or populated automatically. Enter a meaningful title when working with a record; an empty display title can fall back to the native record ID. The profile creates no company and converts no Lead into an Opportunity. The separate [Opportunity profile](opportunity-list.md) remains available for that native workflow.

## Check and apply

Use an existing configured ERPNext site and its compatible Bench Python. Native verification covers ERPNext 16.53.0/Frappe 16.54.0. Read permission for settings is required for checks; application needs normal Custom Field, Property Setter and List View Settings create/write permissions. Operator access to the site environment is privileged, and --user selects the permission principal.

Before first application to an operational site, use its native backup/recovery procedure. The verified backup command includes files:

```bash
bench --site example.local backup --with-files
```

Keep backups and site configuration outside product Git. From the existing Bench directory, substitute actual paths/site/user:

```bash
./env/bin/python /path/to/delonary/scripts/apply_list_view.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator \
  --profile /path/to/delonary/scripts/settings/lead-list.json
```

Default mode reports differences without schema or presentation writes. Exit 0 means a match; exit 1 with a JSON changes object means drift. Errors return nonzero with a traceback. After reviewing the explicit target and differences, repeat with --apply, then run a fresh check and reload the default Lead list.

## Schema and recovery boundary

The optional subject object explicitly names one custom_ Data field and an existing insertion anchor. Its field must be the first configured column. The command validates all selected fields and planned permissions before writing, and rejects incompatible existing subject fields.

Initial Custom Field creation uses the normal controller and changes the database schema. Native DDL can commit independently, so it is a separate preparation phase. After successful field preparation, title selection, labels and list order/widths are saved and verified as presentation configuration. A matching replay creates no duplicate field and performs no further saves or commits.

If presentation verification fails after initial field creation, that field remains prepared while the failed presentation transaction rolls back. Inspect the fresh check and rerun the same reviewed profile to finish configuration. Do not assume schema creation was undone. Recovery of an unwanted schema change uses the established site backup/restore procedure and an assessment of any data already stored in the field.

The disposable-site check verifies a nonmutating preview, Guest denial before schema creation, invalid later-field rejection, the explicit schema/presentation failure boundary, replay and two normal Lead saves plus a fresh read. The browser verifies editing the field through the native form, saving, the work-name heading and reopening the list with the same contact. Real records and existing names are not migrated by these tests.
