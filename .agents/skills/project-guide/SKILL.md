---
name: project-guide
description: >
  Explain Delonary project concepts and technical boundaries. WHEN: Delonary architecture,
  project resources, cost inputs, document generation, Делонари, устройство проекта,
  изучи проект, изучай проект. WHEN NOT: private coordination or generic ERPNext administration.
allowed-tools: [Read, Grep, Glob, Bash]
---

# Delonary Project Guide

## Role

Explain Delonary's project model and the distinction between intended capabilities and demonstrated implementation. README.md owns the introduction; AGENTS.md owns work instructions.

## Degrees of Freedom: MEDIUM

## Entry

Read [references/kb-index.md](references/kb-index.md), then the project model before discussing implementation. Use current task sources for an assigned change. With an explicit task, recover its relevant context and continue within its authority; without one, explain the relevant project concepts or ask for the intended project operation. Do not restart another entry procedure already in progress.

## Technical reasoning

Keep project resource navigation separate from operational tasks, resource coverage separate from a numeric cost, and delivery acceptance separate from payment. The project model owns these distinctions and the unresolved integration questions.

ERPNext is the selected foundation. Read the [accepted delivery boundary](../../../docs/adr/0001-replaceable-erpnext-foundation.md) before choosing packaging or an extension mechanism. Delonary owns its extensions, shared configuration and deployment definitions; the selected foundation can use upstream sources or separate forks. This boundary is accepted but not implemented. Evaluate each adaptation against the actual requirement, compatible release and reproducible scenario. Do not infer DOCX output or unrestricted custom actions from PDF printing or the presence of an MCP endpoint.

## Knowledge upkeep

Maintain useful project-specific explanations at their existing owner within task authority. Report missing or contradictory evidence. This guide is usable with repository files alone and does not require personal notes or private skills.

## Harness enhancements

Use available project tools and file reads. State missing capabilities and separate an author's walkthrough from actual runtime verification.
