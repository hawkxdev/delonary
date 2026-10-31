# Delonary roadmap

Status: proposed. This roadmap describes product outcomes and their dependencies. Detailed first-version requirements, implementation tasks and release dates remain separate decisions.

## Direction

Delonary should give a solo freelancer one operational view of an opportunity or project: where its materials are, what happens next, what has been agreed and accepted, which payments have arrived, and how delivery costs affect project profit. The owner and authorized AI agents use the workspace; client communication stays in existing channels.

ERPNext is the selected foundation. The extension architecture, exact supported releases and integration mechanisms need verification. The [project model](../.agents/skills/project-guide/references/project-model.md) explains the intended concepts and technical boundaries.

## Development sequence

| Phase | Intended outcome | Dependency | Completion evidence |
|---|---|---|---|
| 1. Validate the first-version path | An agreed scope and a feasible route through native ERPNext behavior, configuration and justified extensions | Current product decisions and representative scenarios | Requirements identify acceptance criteria; technical trials resolve blocking integration questions |
| 2. Deliver a usable first version | The owner can manage the agreed opportunity-to-delivery workflow in Delonary | Phase 1 establishes the scope and implementation path | Representative end-to-end scenarios pass, records reconcile and the owner accepts the identified version |
| 3. Improve daily operation | Repeated work and reconciliation become easier without losing traceability | Actual use of the first version exposes specific friction or gaps | Targeted improvements resolve observed cases and preserve existing behavior |
| 4. Make the solution reusable | A supported installation can be reproduced and maintained independently | A useful working version, a chosen delivery model and reviewed third-party obligations | A clean installation, representative use, upgrade and restoration work from the delivered documentation |

Phase 1 is the current planning stage. Later phases are proposed directions rather than scheduled commitments. Dates and delivery forecasts follow validated scope, dependencies and available capacity.

## Phase 1: validate the first-version path

Define the first-version boundary and check the mechanisms most likely to change its implementation cost or feasibility:

- Map opportunities, projects, stages, tasks, acceptance and payments to native entities or explicit extensions. Preserve their different meanings.
- Establish a reproducible compatible environment and evaluate the extension approach before committing product code to a packaging structure.
- Check automatic intake of owner time, agent time, token usage and attributable expenses, including project identity, units, duplicate handling and coverage limits.
- Demonstrate requested template generation in DOCX and PDF, including selection of a manually edited DOCX and its corresponding final PDF.
- Verify read/write MCP coverage for the required records and custom operations using the actual permissions and persisted results.

Use synthetic data for technical trials. Record demonstrated behavior, unresolved gaps and the proposed treatment of each gap. If a mechanism cannot meet the required outcome, return the concrete tradeoff for a product decision instead of silently dropping the requirement.

The next specification belongs in `docs/specs/001-first-version/requirements.md`. This roadmap is not a substitute for that contract.

## Phase 2: deliver a usable first version

The first-version focus is an end-to-end operating loop, with these capabilities carried into detailed scoping:

- Start a case before a sale and retain unsuccessful presales separately from delivered projects.
- Find the project's repositories, directories, notes, correspondence and documents through its resource map.
- Manage tasks, deadlines and next actions inside Delonary.
- Represent fixed-price delivery stages, acceptance and multiple payments without collapsing them into one status.
- Collect resource measurements automatically and show project-level costs and profit with explicit coverage. Keep current totals provisional where inputs are incomplete, and reconcile the final result.
- Generate documents on request, retain the selected editable version and produce the matching PDF.
- Let authorized agents persist confirmed facts through MCP while preserving the distinction between a proposal, an agreement and an executed action.

These are planning inputs for the first-version specification, not claims of implemented functionality. Automatic resource intake, document generation and agent writes are part of this focus; later phases do not replace them with a permanently manual workaround.

Before relying on the system for real work, verify the applicable permissions, invalid and repeated operations, representative financial states, document contents and backup/restoration path. Technical checks and the owner's acceptance cover the same identified version.

## Phase 3: improve daily operation

Choose improvements from observed use: recurring navigation problems, repeated corrections, missing measurement coverage, difficult reconciliation or document-version confusion. Candidates include clearer work views, better diagnostics and broader support for verified input sources or templates.

Each improvement needs a concrete case, its expected result and regression checks. Compare the result with the original case before deciding to keep, change or stop that direction. Convenience changes must preserve source evidence, unknown costs and the separation of work acceptance from payment.

## Phase 4: make the solution reusable

Prepare a documented installation and maintenance path, supported-version boundaries, synthetic examples and a clear extension boundary. Verify upgrades and recovery with the selected adaptations in place. Preserve [Delonary's GPL-3.0-only licensing](../LICENSE) and verify third-party obligations for the actual distributed package.

Broader use is conditional on a concrete audience and an acceptable support burden. Personal usefulness and a public repository do not establish external demand. A client portal, team product or commercial offering requires its own product decision.

## Scope and review rules

The initial focus uses fixed prices, project-level economics and on-request documents. Hourly client billing, per-stage profit, proactive business reminders, document generation without an explicit request and a unified client-message inbox are not first-version targets. Client accounts are outside the selected initial scope.

Review this roadmap after the first-version scope is agreed, a technical trial changes feasibility, or actual use reveals a material new need. Preserve the accepted requirement meaning when changing sequence or implementation. Keep detailed requirements with their specification and accepted architecture decisions under `docs/adr/`.
