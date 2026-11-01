# Delonary

Delonary is an early-stage project for a self-hosted freelance workspace on [ERPNext](https://github.com/frappe/erpnext) and [Frappe](https://github.com/frappe/frappe). Its goal is to connect project materials, next actions, agreements and delivery economics in one working system.

[Available now](#available-now) · [Requirements](#requirements) · [Usage](#usage) · [Development](#development) · [Documentation](#documentation) · [Contributions](#maintainer-and-contributions)

## Available now

The repository provides a small utility for versioned checkbox settings in Frappe. Keep a reviewed preference in Git, check a site's configuration for differences, and explicitly apply the profile through normal Frappe permissions and validation. The included [profile](scripts/settings/shared.json) disables native product suggestions.

The complete Delonary workspace is not packaged for installation yet. Development starts with real use of stock ERPNext and adds adaptations for observed needs.

## Requirements

- Git to obtain the source.
- Python 3.11 or newer for repository development and unit tests.
- An existing configured Bench site to use the settings utility. Native checks cover Frappe 16.54.0; the Bench interpreter must satisfy the installed Frappe release's own requirements.
- Trusted operator access and a Frappe user with read permission for checks and write permission for applying System Settings.

The utility uses Python's standard library and the site's installed Frappe API. Site credentials, database provisioning and schema belong to the existing Bench installation. The development environment below is separate from that runtime.

## Setup

Get the source:

```bash
git clone https://github.com/hawkxdev/delonary.git &&
cd delonary
```

## Usage

Use your existing Bench Python environment. Replace the Bench path, repository path and site name below with your actual installation and checkout:

```bash
cd /path/to/frappe-bench &&
./env/bin/python /path/to/delonary/scripts/apply_settings.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator
```

This checks for differences without saving. Exit 0 means the profile matches. Exit 1 with a JSON changes object means settings differ; an execution error instead has a traceback and a nonzero exit.

After reviewing the differences, apply from the same Bench directory:

```bash
./env/bin/python /path/to/delonary/scripts/apply_settings.py \
  --sites-path ./sites \
  --site example.local \
  --user Administrator \
  --apply
```

Run the check again to verify the result. Reapplying a matching profile skips another save. Initially, profiles support editable checkbox fields on Single DocTypes.

See the [operator guide](docs/operations/shared-settings.md) for prerequisites, exit codes, container file access, repeat application and recovery.

## Development

The POSIX development commands below are checked on macOS with Python 3.14. From the repository root, create an environment with the checked [Ruff 0.16.4](https://pypi.org/project/ruff/0.16.4/) and [mypy 1.19.1](https://pypi.org/project/mypy/1.19.1/) versions:

```bash
cd /path/to/delonary &&
python3 -m venv .venv &&
.venv/bin/python -m pip install ruff==0.16.4 mypy==1.19.1
```

Run all local checks; each command stops the sequence on failure:

```bash
.venv/bin/python -m unittest discover -s tests -v &&
.venv/bin/ruff check scripts tests &&
.venv/bin/ruff format --check scripts tests &&
.venv/bin/mypy
```

Unit tests need no running Frappe site. Native integration additionally needs a disposable configured site; see the operator guide.

## Project structure

| Path | Purpose |
|---|---|
| [scripts/apply_settings.py](scripts/apply_settings.py) | Explicit check/apply command |
| [scripts/settings/shared.json](scripts/settings/shared.json) | Reviewed public settings profile |
| [tests/test_settings_profile.py](tests/test_settings_profile.py) | Validation, permission and repeat-operation unit cases |
| [pyproject.toml](pyproject.toml) | Ruff and mypy configuration |

## Documentation

| Document | Purpose |
|---|---|
| [Roadmap](docs/ROADMAP.md) | Product direction and proposed stages |
| [Project model](.agents/skills/project-guide/references/project-model.md) | Concepts, intended workflows and evidence limits |
| [Delivery decision](docs/adr/0001-replaceable-erpnext-foundation.md) | Accepted extension and replaceable-foundation boundary |
| [Shared settings guide](docs/operations/shared-settings.md) | Runtime prerequisites, operation and recovery |
| [Shared settings plan](docs/specs/002-shared-settings/plan.md) | Component implementation and acceptance source |

## Planned workspace

Intended workflows include project-resource navigation, tasks and next actions, fixed-price stages, separate acceptance and payment states, project economics, and read/write agent access. Client communication stays in existing channels. DOCX/PDF generation and automatic cost collection are deferred.

The delivery design keeps Delonary's extensions, shared configuration and deployment definitions here, with upstream ERPNext/Frappe releases or selected forks as versioned dependencies.

## Maintainer and contributions

Project owner: [hawkxdev](https://github.com/hawkxdev). Use [GitHub issues](https://github.com/hawkxdev/delonary/issues) for questions and proposals, with synthetic examples. Read [CONTRIBUTING.md](CONTRIBUTING.md) before implementation and [AGENTS.md](AGENTS.md) for work instructions.

## License

Delonary is licensed under the [GNU General Public License v3.0 only](LICENSE) (`GPL-3.0-only`). Third-party components, including ERPNext and Frappe Framework, retain their own licenses.
