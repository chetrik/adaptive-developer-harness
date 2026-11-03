---
name: generate-harness
description: Apply only an approved Harness Plan to a target repository using a verified host adapter and bounded file operations.
---

# Generate Harness — generator orchestration procedure

**Status:** generator-side guidance connected to the executable MVP; native installation of this orchestration Skill is not claimed. Follow BOOTSTRAP.md and the runtime schemas. Target-project assets are separately stored in library/target/.

## Hard preflight

- Plan exists, schema valid, modules resolved, **approval explicitly recorded**, target path and host capabilities verified.
- Review git status/existing instructions, inspect conflicts and show affected paths/diffs; no secret logging.
- Third-party assets may be copied only with reviewed provenance, license and notices, including generated distribution obligations.
- Any unapproved file overwrite, install, network call, deployment, permission change, production write or destructive operation → STOP and ask for the missing narrow permission.

## Procedure after preflight

1. Use the existing deterministic plan and its exact operations; do not create a second staging/apply workflow.
2. Confirm the plan adapter and capability evidence. Never invent native support.
3. Use runtime explain/preview and validate the plan before recording the actual approval; resolve conflicts through a new plan, not blind overwrites.
4. Apply selected file operations idempotently, recording exact changes and a recovery route.
5. Run `validate-harness` on actual files. Do not claim verified success merely because generation returned normally.
6. Write short user-facing outcome and portable handoff with limitations.

If an unsupported host prevents a critical gate, return BLOCKED/NEEDS-REVIEW and safe fallback; do not silently omit it.

## Runtime binding

Use the agent-operated commands in BOOTSTRAP.md. Selection uses `adaptive_harness.core.make_plan`; approval/apply/recovery use `adaptive_harness.apply`; validation reports actual file checks separately from application tests and native discovery. Do not implement formal policy by improvising this prose.
