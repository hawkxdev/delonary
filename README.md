# Delonary

Delonary is a planned self-hosted workspace for freelance projects: find project resources, manage the next action, and understand delivery costs and profit.

ERPNext is the selected foundation. The project is at the design stage; there is no installable Delonary application yet.

The [accepted delivery model](docs/adr/0001-replaceable-erpnext-foundation.md) keeps Delonary's extensions, shared configuration and reproducible deployment in this repository. ERPNext and Frappe are external dependencies whose selected sources may be upstream releases or separately maintained forks. A complete installable delivery is not implemented yet.

The first [shared settings utility](docs/operations/shared-settings.md) checks and applies a reviewed configuration profile in an existing Bench environment. Its initial setting disables native product suggestions; application packaging and full deployment remain separate work.

The immediate priority is hands-on use of stock ERPNext before choosing substantial adaptations. Project-resource navigation, work management, project economics and useful agent access guide later changes. DOCX/PDF generation and automatic cost collection are deferred to future stages. Client communication stays in existing channels.

Read the [roadmap](docs/ROADMAP.md) for the proposed development stages and the [project model](.agents/skills/project-guide/references/project-model.md) for the intended concepts and technical questions. See [CONTRIBUTING.md](CONTRIBUTING.md) for proposing changes and [AGENTS.md](AGENTS.md) for working instructions.

Delonary is licensed under the [GNU General Public License v3.0 only](LICENSE) (`GPL-3.0-only`). Third-party components, including ERPNext and Frappe Framework, retain their own licenses.
