# Delonary knowledge sources

Paths below are relative to the repository root. This guide owns navigation and project-model explanations.

| Need | Owner | Reading condition |
|---|---|---|
| Purpose and entry | `README.md` | Start here for the product's intended value and observed stage |
| Project concepts and integration questions | `.agents/skills/project-guide/references/project-model.md` | Read before designing entities, imports, financial calculations, document generation or MCP operations |
| Delivery ownership and replaceable foundation | `docs/adr/0001-replaceable-erpnext-foundation.md` | Read before configuration versioning, packaging, deployment or selecting an upstream source versus a fork |
| Versioned shared checkbox settings | `docs/operations/shared-settings.md`, `scripts/apply_settings.py`, `scripts/settings/shared.json` | Read before checking or applying configuration in an existing Bench environment; native integration needs an authorised disposable site |
| Independent Lead work titles and separate contacts | `docs/operations/lead-title.md`, `scripts/apply_list_view.py`, `scripts/settings/lead-list.json`, issue #2 | Read before changing Lead display titles; preserve person names and the explicit schema/presentation preparation boundary |
| Native Opportunity names and separate contacts | `docs/operations/opportunity-list.md`, `scripts/settings/opportunity-list.json` | Read for the separate Opportunity list; it does not replace the independent Lead title requirement |
| Work and verification rules | `AGENTS.md` | Read before changing project files |
| Proposing and submitting a change | `CONTRIBUTING.md` | Read before preparing a contribution or requesting review |

Assigned feature packages belong under `docs/specs/`; accepted architecture decisions belong under `docs/adr/`. The delivery decision above does not supply an implementation assignment or a feature contract. Use the actual assigned task rather than inferring implementation from these directory roles.
