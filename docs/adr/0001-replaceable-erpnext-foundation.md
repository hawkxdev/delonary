# 0001. Keep the ERPNext foundation replaceable

Status: accepted. Implementation and deployment remain pending.

## Context

Delonary uses ERPNext and Frappe as its foundation. The repository must become the source of a reproducible Delonary installation, including shared settings and extensions. Native use can reveal both configuration needs and changes that require application or core code. Choosing an extension mechanism now must preserve the option to change the foundation later.

## Decision

Delonary remains an independent repository for its own Frappe application, selected shared configuration, and build, installation and deployment definitions. ERPNext and Frappe remain explicit external dependencies. Their complete source trees do not need to be copied into this repository.

Delivery inputs must identify each dependency's source and immutable version, using repository URLs with source revisions or immutable image references as appropriate to the selected build. The delivery design must allow an upstream source to be replaced with an explicitly selected fork. No fork is required before a concrete change needs one.

Choose the mechanism for each adaptation from the actual requirement: native configuration, exported customization, application code or a core change. A separate application is the initial extension boundary, not a prohibition on modifying ERPNext or Frappe. A required core change belongs in a separately maintained fork of the affected dependency. Delonary records the selected fork and version as delivery inputs.

Version useful shared settings from the first configuration work, rather than waiting for custom business logic. A setting stored in the database needs a reviewed representation and a repeatable application mechanism. For example, disabling product suggestions can be represented by the intended System Settings field and value. Exporting an entire database or all settings is not the configuration contract; secrets and operational records remain separate inputs.

## Consequences

The repository can acquire configuration and deployment files before it contains custom application logic. Users should eventually obtain the selected foundation, apply Delonary's configuration and install its extensions from the documented repository version.

A fork creates ongoing work to reconcile upstream changes and verify the combined system. Changing a dependency URL alone does not establish compatibility. Record the selected source, upstream base, required changes and relevant checks when a fork is actually introduced. Separate applications also need compatibility verification after dependency changes.

The current native evaluation installation is not yet that reproducible Delonary delivery. Application packaging, concrete build inputs, settings application, installation and upgrade procedures still need implementation and evidence. This decision does not create a fork or migrate an existing installation.

## Verification boundary

A future delivery must demonstrate installation on a clean compatible environment, application of the selected public settings and the expected behavior. Repeated configuration must have defined effects. A switch to a fork needs its own build and functional verification; neither a configuration file nor this decision proves a working installation or safe upgrade.

## Sources

- [Frappe applications](https://docs.frappe.io/framework/user/en/basics/apps)
- [Frappe configuration hooks and fixtures](https://docs.frappe.io/framework/user/en/python-api/hooks)
- [Single DocType settings storage](https://docs.frappe.io/framework/user/en/basics/doctypes/single-doctype)
- [Official Frappe Docker image and application boundaries](https://github.com/frappe/frappe_docker/blob/main/docs/02-setup/01-overview.md)
