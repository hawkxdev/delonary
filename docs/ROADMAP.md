# Delonary roadmap

Status: proposed. The immediate direction is to use stock ERPNext before deciding which adaptations are necessary. Detailed custom requirements follow observed use rather than blocking the first working system.

## Direction

Delonary should help a solo freelancer find project materials, manage work and agreements, distinguish acceptance from payment, and understand project economics. ERPNext is the selected foundation. The initial users are the owner and authorized agents; client communication remains in existing channels.

The [project model](../.agents/skills/project-guide/references/project-model.md) retains the intended concepts and distinguishes future adaptations from demonstrated native behavior.

The [accepted delivery boundary](adr/0001-replaceable-erpnext-foundation.md) makes this repository the future source of Delonary's extensions, shared configuration and reproducible deployment. ERPNext/Frappe dependencies can use upstream sources or separately maintained forks; no fork is required in advance.

## Development sequence

| Phase | Intended outcome | Basis for proceeding | Completion evidence |
|---|---|---|---|
| 1. Use stock ERPNext | The owner can try the native system without substantial customization | An isolated working installation with a demonstration company | The owner can open and use ordinary project/task workflows and identify concrete friction |
| 2. Choose initial adaptations | A small set of changes addresses needs demonstrated during use | Observed cases, retained product goals and the owner's priorities | Each selected change has a scenario, acceptance criterion and verified result |
| 3. Extend confirmed workflows | Additional capabilities address a justified next need | Experience with the working system and an explicit decision to revisit deferred scope | The selected workflow works end to end without breaking existing use |
| 4. Make the solution reusable | A supported installation can be reproduced and maintained independently | A useful working version, a chosen delivery model and reviewed third-party obligations | Installation, representative use, upgrade and restoration work from delivered documentation |

Dates and forecasts follow the actual selected work, dependencies and available capacity. Publishing this roadmap does not establish implemented behavior or a delivery date.

## Phase 1: use stock ERPNext

Start with a normal ERPNext installation and fictional demonstration data. The first objective is hands-on use, not a custom application or an exhaustive specification.

- Open the standard interface and try customers, projects, tasks and other native records relevant to the owner's workflow.
- Walk through a small example and observe what is already useful, what can be configured, and what causes a concrete problem.
- Retain links to existing project materials through the native facilities available in the trial; record missing navigation behavior instead of building a replacement in advance.
- Preserve selected reusable settings in reviewed versioned files with a repeatable application path. Configuration and deployment files can enter the repository during this phase, before custom application logic; export and replay still need their own evidence.
- Keep the installation isolated and its evaluation data persistent. A successful trial is not production-readiness or an approved migration of real client data.

Do not make custom document generation, automated cost intake, a complete bespoke profit model or a custom integration a prerequisite for seeing the native system. Read/write agent access remains a product goal; its detailed coverage can be evaluated against actual tasks after the first manual walkthrough.

The owner decides what needs improvement after using the system. Keep a concrete example, expected result and observed limitation for each proposed adaptation.

## Phase 2: choose initial adaptations

Compare observed needs with native behavior before writing custom code. Distinguish an existing function, a configuration choice, a justified extension and a remaining unknown. Preserve earlier needs as inputs rather than assuming that every one requires a change.

Relevant areas include project-resource navigation, tasks and next actions, fixed-price stages, separate acceptance and payment states, project economics and useful agent operations. Explore native cost entry and reports before deciding what additional inputs or calculations are needed; this roadmap does not select a new custom manual cost-entry subsystem.

Record the agreed adaptation scope in `docs/specs/001-first-version/requirements.md` when there is enough experience to define it. Verify the selected mechanism and acceptance scenario before claiming that a change meets the requirement. Exact releases and extension packaging follow their actual technical decisions.

For each adaptation, compare native configuration, application extensions and a core change. When a core change is justified, maintain it in a separate dependency fork and select its source/version through the delivery inputs. Verify the resulting combination rather than assuming a source URL change is sufficient.

## Phase 3: extend confirmed workflows

The following capabilities are explicitly deferred beyond the initial work:

- Template-based DOCX/PDF generation, returning an edited DOCX and producing its matching PDF.
- Automatic collection of owner time, agent time, token usage and attributable expenses.

These capabilities remain future goals. Their technical trials and implementation do not block Phase 1 or the initial adaptation scope. Revisit them when the owner prioritizes a concrete need; no date or exact later release is committed.

Other improvements should also follow observed use: repeated corrections, difficult reconciliation, navigation friction or missing operational visibility. Check the original case and relevant regressions before deciding to keep, change or stop an approach. Preserve source evidence, unknown costs and the distinction between acceptance and payment.

## Phase 4: make the solution reusable

Prepare a documented installation and maintenance path, supported-version boundaries, synthetic examples and a clear extension boundary. Verify upgrades and recovery with the selected adaptations in place. Preserve [Delonary's GPL-3.0-only licensing](../LICENSE) and verify third-party obligations for the actual distributed package.

This phase hardens and validates reproducibility for independent use; it does not postpone all versioned configuration and deployment work until the end of development.

Broader use is conditional on a concrete audience and an acceptable support burden. Personal usefulness and a public repository do not establish external demand. A client portal, team product or commercial offering requires its own product decision.

## Scope and review rules

The initial priority is a usable native system. DOCX/PDF generation and automatic cost collection are deferred; they are not silently replaced by promises of equivalent custom work. Existing documents may still be linked as project resources.

Fixed prices and project-level economics remain planning inputs. Hourly client billing, per-stage profit, proactive business reminders and a unified client-message inbox are not selected first-version targets. Client accounts are outside the selected initial scope.

Review this roadmap after hands-on use identifies a meaningful need, a technical observation changes feasibility, or the owner revisits deferred scope. Keep detailed requirements with their specification and accepted architecture decisions under `docs/adr/`.
