# Delonary working instructions

Read [.agents/skills/project-guide/SKILL.md](.agents/skills/project-guide/SKILL.md) and its relevant references before project work. Use native skill loading when available; otherwise read the files directly.

## Scope and structure

Delonary is in design, with ERPNext selected as its foundation. Runtime versions, installation and the extension architecture still need a concrete task and verification. Do not infer Django conventions from the use of Python.

Use `src/` for product sources, `tests/` for product tests, `scripts/` for repository utilities, `docs/specs/<NNN-feature>/` for assigned feature packages and `docs/adr/` for accepted architecture decisions. Populate these roles only with useful assigned content. Frappe application packaging must be designed before adding source files.

README.md introduces the project, the project guide explains its concepts, and these instructions govern work. Keep new instructions and technical references in English. Preserve exact identifiers and language-dependent examples.

## Changes and verification

Resolve the accepted task, affected owners and concrete acceptance criteria before implementation. Keep requirement changes with their task owner and preserve concurrent work. For a new feature, record its requirements, plan and tasks under `docs/specs/` when that work is assigned.

Review new files as well as diffs. Run `git diff --check` for tracked changes and inspect new files for whitespace and broken links. These checks establish repository hygiene only. Derive product checks from actual application metadata once product code exists; do not invent setup, build or test commands.

Use local execution for checks and builds. Do not add or trigger GitHub Actions. Installing ERPNext, starting services, changing production or publishing requires task authority for that action.

Every commit requires the owner's explicit approval of the prepared changes. The first commit message is exactly `chore: initialize project`. Publication requires separate authority. For an owned public repository, changes use pull requests and the human owner performs the final merge; do not force push or delete branches. Server protection must be verified when a destination exists.
