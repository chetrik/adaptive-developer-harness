---
name: update-harness
description: Reassess and safely evolve an existing generated Developer Harness when project scope, host, risk or dependencies change.
---

# Update Harness — original draft procedure

**Status:** draft; host-specific tooling needed for execution.

## Procedure

1. Inspect current files, existing plan/provenance, user customizations and source git status; identify actual current state and deviations.
2. Ask whether scope/risks/host changed, but infer from available PRD/repo evidence before asking repeated questions.
3. Re-run assessment and policy selection while preserving stable module IDs and prior approvals where still valid.
4. Produce a migration/diff plan separating kept, added, modified, deprecated and user-custom items; explain safety implications.
5. Require fresh approvals for high-impact or breaking changes; avoid removing safeguards that still address active risks.
6. Apply only approved changes, test, update relevant docs/attributions, and create cross-host handoff.

Never rebuild the target from scratch as an automatic response to scope changes.
