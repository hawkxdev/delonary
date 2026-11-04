# Project names and contacts

[Issue #2](https://github.com/hawkxdev/delonary/issues/2) owns the requirement and acceptance criteria. This profile uses ERPNext Opportunity for individual potential engagements and keeps person identity in a separate Contact. Multiple opportunities may reference the same person. The owner also requires an independent [Lead title](lead-title.md); using Opportunity does not replace that requirement. Naming an engagement does not establish an accepted order or agreed price.

## Profile and prerequisites

[opportunity-list.json](../../scripts/settings/opportunity-list.json) configures the first two data columns of the default Opportunity list:

| Native field | Display label | Width in CSS pixels |
|---|---|---|
| title | Project Name | 420 |
| contact_person | Contact | 180 |

Profile labels use English source text. Frappe translates them for the selected interface language through its existing translation catalog.

The native ID column and row controls may also appear. Contact links display the contact name through the existing Contact title configuration. Saved personal layouts can override the default presentation; return to the default list when checking this profile. The utility preserves personal layouts and unrelated list settings.

Use an existing configured Bench site with ERPNext. Native checks cover ERPNext 16.53.0 and Frappe 16.54.0. Other releases and customizations need their own verification. The [utility](../../scripts/apply_list_view.py) uses the standard library and the installed Frappe API; repository development requires Python 3.11 or newer, while the site interpreter follows its installed applications.

The operator needs read permission for checks and normal create/write permissions for Property Setter and List View Settings when applying. Server access is already privileged; --user selects the permission principal and does not authenticate an untrusted caller.

Real opportunities require an explicitly selected operating Company. The profile does not create a company, choose accounting settings, convert leads or create contact/work records. Use fictional records on a disposable site for evaluation.

## Check and apply

From the existing Bench directory, substitute actual paths and an authorised site/user:

```bash
cd /path/to/frappe-bench &&
./env/bin/python /path/to/delonary/scripts/apply_list_view.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator \
  --profile /path/to/delonary/scripts/settings/opportunity-list.json
```

Default mode reports differences without saving. Exit 0 means the profile matches; exit 1 with a JSON changes object means it differs. Execution errors produce a traceback and a nonzero exit.

After reviewing the differences and the target's native backup/recovery procedure, repeat with --apply:

```bash
./env/bin/python /path/to/delonary/scripts/apply_list_view.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator \
  --profile /path/to/delonary/scripts/settings/opportunity-list.json \
  --apply
```

Run the default check again through a fresh process, then reload the default Opportunity list. Reapplying a matching profile skips saves and commits. Container operators must make both the script and profile available inside the existing Bench environment; this repository does not supply a complete container installation.

## Effects and recovery

The command validates the full profile and native fields before writing. It uses ordinary Property Setter documents for labels and in_list_view, and List View Settings for field order and selected widths. Existing widths without a profile override and other list options are preserved. The first column must remain the native title field; supported columns are stored Data or Link fields. The native title can be hidden in the form because Desk displays it as the subject.

This profile has no subject declaration and changes presentation only. All planned document permissions are checked before saves. Readback occurs before commit; an exception rolls back the presentation transaction and clears the affected metadata cache. Profiles that create a custom subject have the separate schema preparation boundary described in [the Lead guide](lead-title.md#schema-and-recovery-boundary). The script uses no permission bypass and changes no upstream application files.

Before applying to an operational site, retain a native backup and the exact existing selected settings. Recover through that site's established restoration procedure or explicitly restore the affected settings using native customization tools. The utility does not delete customizations or promise to reconstruct defaults from a different release.

## Use and verification

Create an Opportunity with its own title and a separate contact. To edit the title of a saved record, use the pencil in the record sidebar and change the title while retaining the document ID and leaving merge disabled. Reopen the list and confirm that the contact name stays unchanged.

The disposable-site check saves two opportunities for one synthetic contact, applies the reviewed profile, verifies fresh-process and repeated application, rejects Guest writes and an invalid later field, and verifies rollback after a forced readback failure. Browser verification covers the two labels, order, contact display, normal title editing and reopening. These checks do not establish every role, personal layout, future release or operational migration.

Run repository checks with the commands in [README.md](../../README.md#development). Unit tests need no Frappe site; native checks require a separately authorised disposable ERPNext site.
