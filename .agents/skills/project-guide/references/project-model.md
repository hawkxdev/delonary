# Delonary project model

This reference belongs to [project-guide](../SKILL.md). It describes the intended model at the design stage; it does not establish runtime behavior or replace an assigned feature's acceptance criteria.

## Project resources and work

A project resource is a location of relevant material: source repository, project directory, notes, documents or correspondence. External links can provide navigation without importing the material itself. A task represents work with a next action or deadline and is intended to be managed inside Delonary. A resource link alone does not complete an operational task.

Client communication remains in its existing channels. Relating correspondence and recording agreements do not imply an automatic inbox, message import or permission to send a message. Client login and a customer portal are outside the selected initial scope.

## Resource measurements and project economics

Project economics remains a product goal, but automatic collection of owner time, agent time, weighted token usage and additional attributable expenses is deferred. The immediate work uses stock ERPNext and observes its native inputs and reports before choosing adaptations. A future collector must retain source identity, project attribution, units, covered period and coverage limits. Missing measurements remain unknown; a partial cost total cannot establish complete project profit.

Contract value, invoiced amount, received payment, accepted-work revenue, resource cost and profit represent different facts. ERPNext's native project margin must be compared with the required cost model before reuse. A matching field name does not establish matching accounting semantics.

## Template documents

DOCX/PDF template generation and the editable-document round trip are deferred to future stages. Their design and technical trials do not block initial use of stock ERPNext. Existing documents can remain project resources linked through available native facilities. When generation is revisited, the intended action produces both formats from project data; attaching an externally produced file does not fulfill that future generation requirement. The template engine, conversion route and later priority remain undecided.

## Agent operations

Read/write agent access through MCP remains a product goal. It is not a prerequisite for the owner's first manual walkthrough of stock ERPNext. Coverage must be established for each selected entity and action using the actual installation's permissions and persisted results. Tool discovery, an endpoint response or a successful read does not establish write coverage. No installed Delonary MCP server is claimed.

## Foundation and delivery boundary

ERPNext supplies the selected application foundation; Frappe supplies its application framework. The [accepted delivery decision](../../../../docs/adr/0001-replaceable-erpnext-foundation.md) keeps Delonary's application, shared configuration and deployment definitions in this repository while preserving upstream and forked dependency sources. Exact releases, application packaging, build inputs, input connectors and upgrade behavior still require implementation decisions and verification.

Native use supplies representative cases and the owner's observations. Reusable configuration should be versioned as it is selected; custom business logic is not a prerequisite for repository delivery files. Later checks follow selected adaptations: navigation reaches the intended resource, measurements have explicit coverage, generated documents match their selected source, agent writes persist, and upgrades preserve the selected extensions and foundation. Deferred capabilities do not become initial launch criteria. These examples are not completed tests or an assigned implementation plan.
