---
name: generate-harness
description: Apply only an approved Harness Plan to a target repository using a verified host adapter and bounded file operations.
---

# Generate Harness — original draft procedure

**Status:** draft, not executable without a host adapter and authorization. Refer to `docs/SECURITY.md`, `docs/ARCHITECTURE.md` and the approved `Harness Plan`.

## Hard preflight

- Plan exists, schema valid, modules resolved, **approval explicitly recorded**, target path and host capabilities verified.
- Review git status/existing instructions, inspect conflicts and show affected paths/diffs; no secret logging.
- Third-party assets may be copied only with reviewed provenance, license and notices, including generated distribution obligations.
- Any unapproved file overwrite, install, network call, deployment, permission change, production write or destructive operation → STOP and ask for the missing narrow permission.

## Procedure after preflight

1. Generate selected canonical components to a safe staging area.
2. Render through verified host adapter. Never invent native subagent/Skill support.
3. Validate staging and produce preview; reconcile with existing files using user-approved, bounded changes only.
4. Apply selected file operations idempotently, recording exact changes and a recovery route.
5. Run `validate-harness` on actual files. Do not claim verified success merely because generation returned normally.
6. Write short user-facing outcome and portable handoff with limitations.

If an unsupported host prevents a critical gate, return BLOCKED/NEEDS-REVIEW and safe fallback; do not silently omit it.
