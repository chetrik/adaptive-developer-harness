---
name: select-harness
description: Recommend an explainable minimum sufficient Developer Harness from project assessment, risk policy and component catalog.
---

# Select Harness — original draft procedure

**Status:** draft. A future deterministic policy engine must replace unsupported LLM-only selection claims. Inputs: assessed project, host capabilities, catalog, policy, reuse evaluation.

## Procedure

1. Start with mandatory safety/quality baseline and existing project conventions. Do not confuse feature size with risk.
2. Evaluate every relevant catalog module as selected, skipped, host-blocked or conflicting. Explain decisions and trace to assessment evidence; use `not-applicable` rather than generic 'optional' when it will not be used.
3. Resolve dependencies and functional duplication. Do not stack complete SDD toolchains as a default.
4. Evaluate project-wide Harness separately from per-feature workflow route. Limit documents to those the project needs.
5. Make proposed file operations explicit; preserve existing user files and permissions.
6. Show beginner-readable plan using `templates/HARNESS_PLAN.md`; separately export planned JSON matching `schemas/harness-plan.schema.json` if supported.
7. **Stop before target file changes.** Request specific user approval and address blockers; never assert approved if no explicit permission exists.

## Quality checks

Every selected/skipped module has a reason; every dependency exists; no unresolved conflicts; all required risk gates retained; unsupported host features labeled. Output is a proposed plan, **not** completed setup.
