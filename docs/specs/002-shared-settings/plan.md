# Shared settings implementation

Requirements and acceptance owner: [issue #3](https://github.com/hawkxdev/delonary/issues/3). The accepted [delivery decision](../../adr/0001-replaceable-erpnext-foundation.md) permits configuration files before custom application packaging. This plan tracks local implementation; it does not duplicate the issue's requirements or authorise a release.

## Route and scope

Use one JSON profile and a standalone repository utility in an existing Bench environment. Keep the first supported data contract to editable checkbox fields on Single DocTypes. This needs no custom app, third-party runtime dependency or operational database migration.

## Tasks

- [x] Add the selected public profile and explicit check/apply utility.
- [x] Verify validation, permission and repeat-operation contracts with unit tests.
- [x] Verify the final source bytes on an isolated native site, including persistence and boot defaults.
- [x] Write operator instructions and repository quality configuration.
- [x] Present the complete local result for owner acceptance and commit approval.

## Verification and delivery boundaries

Use synthetic data on a disposable Frappe 16.54.0 site. Preserve operational records and existing runtime services. Keep raw execution evidence and access details private; report safe outcomes in the issue.

The owner accepts the prepared component and authorises its commit and protected PR delivery. Source delivery and a complete reproducible installation remain distinct steps; this utility does not supply application packaging or deployment.
