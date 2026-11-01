# Shared Frappe settings

[Issue #3](https://github.com/hawkxdev/delonary/issues/3) owns the requirement and acceptance criteria. This utility is the first versioned configuration component of the [delivery model](../adr/0001-replaceable-erpnext-foundation.md); it is not a complete Delonary installation.

## Profile and prerequisites

[shared.json](../../scripts/settings/shared.json) contains only System Settings.disable_product_suggestion = 1. It disables Frappe's native CRM/Helpdesk product suggestions. The file contains no accounts, connection details or database export.

The [utility](../../scripts/apply_settings.py) runs with an existing Bench Python environment containing Frappe. Its standard-library code requires Python 3.11 or newer; the installed Frappe release has its own runtime requirements. Native verification uses Frappe 16.54.0. Other releases and custom controllers need their own checks.

The site must already exist and have valid initial settings. A newly created site may still require language and time zone configuration before System Settings can be saved. Do not bypass mandatory fields to apply this profile.

This is a server-side operator tool. Access to the Bench environment and site credentials is already privileged. The explicit user selects the Frappe permission principal; it is not an authentication mechanism for untrusted callers. Normal read/write permissions and document validation remain active.

## Check before applying

From the target Bench directory, substitute the repository path, existing site and authorised user:

```bash
./env/bin/python /path/to/delonary/scripts/apply_settings.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator
```

Without --apply, the utility reports differences as JSON without saving settings. Exit 0 means the profile matches; exit 1 with a JSON changes object means settings differ. Execution errors also produce a nonzero exit and a traceback; they are not a successful comparison.

The default profile is resolved beside the script under settings/shared.json. Use --profile to select another reviewed file. Container users must make both files available inside the existing Bench environment and pass their container paths; this repository does not yet provide a container installation recipe.

## Apply and verify

Repeat the check command with --apply only after reviewing the target and differences. The utility validates the complete profile against metadata, supports editable Check fields on Single DocTypes, saves through the normal controller and verifies the written values before committing. It prints only the selected checkbox differences.

Run the check command again through a new process. A matching profile returns exit 0 with empty changes. Repeated --apply on matching settings skips save and commit. Reload the Desk to observe changes consumed through boot/default settings.

Normal controllers may validate or normalise the rest of their document. Test a profile on an appropriate disposable site before applying it to operational data, and retain the target's normal recovery path. Do not export all System Settings as a substitute for this selected profile.

To restore a previous preference, use the reviewed previous profile with the same check/apply sequence, then verify it again. Do not reverse unrelated settings or copy an operational database into Git.

## Local checks

Run from the repository root with the development tools available:

```bash
python3 -m unittest discover -s tests -v
ruff check scripts tests
ruff format --check scripts tests
mypy
```

The unit suite covers profile validation, a nonmutating check, permission denial, complete metadata validation before writes, repeat application and failed readback. Native verification additionally needs an authorised disposable Frappe site. Passing unit tests alone does not establish database persistence, boot-default updates or a working installation.
