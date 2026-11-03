---
name: select-harness
description: Recommend an explainable minimum sufficient Developer Harness from project assessment, risk policy and component catalog.
---

# Select Harness — generator orchestration procedure

**Status:** generator-side guidance connected to the executable MVP; native installation of this orchestration Skill is not claimed. Follow BOOTSTRAP.md and the runtime schemas. Target-project assets are separately stored in library/target/.

## Procedure

1. Start with mandatory safety/quality baseline and existing project conventions. Do not confuse feature size with risk.
2. Evaluate every relevant catalog module as selected, skipped, host-blocked or conflicting. Explain decisions and trace to assessment evidence; use `not-applicable` rather than generic 'optional' when it will not be used.
3. Resolve dependencies and functional duplication. Do not stack complete SDD toolchains as a default.
4. Evaluate project-wide Harness separately from per-feature workflow route. Limit documents to those the project needs.
5. Make proposed file operations explicit; preserve existing user files and permissions.
6. Obtain the machine-valid plan from the runtime `plan` command and use `explain` and `preview` for the beginner-readable review. Do not manually reconstruct a plan from the historical Markdown template.
7. **Stop before target file changes.** Request specific user approval and address blockers; never assert approved if no explicit permission exists.

## Quality checks

Every selected/skipped module has a reason; every dependency exists; no unresolved conflicts; all required risk gates retained; unsupported host features labeled. Output is a proposed plan, **not** completed setup.

## Runtime binding

Use the agent-operated commands in BOOTSTRAP.md. Selection uses `adaptive_harness.core.make_plan`; approval/apply/recovery use `adaptive_harness.apply`; validation reports actual file checks separately from application tests and native discovery. Do not implement formal policy by improvising this prose.
