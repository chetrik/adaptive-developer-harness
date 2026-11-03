---
name: validate-harness
description: Verify planned versus generated harness modules, host compatibility, consistency, provenance and evidence without inventing passed checks.
---

# Validate Harness — original draft procedure

**Status:** draft. Prefer deterministic tooling and host-native tests where they exist. This skill is not an independent security certification.

## Procedure

1. Read the approved plan and inspect actual target files (not the implementer's summary).
2. Verify expected file paths, metadata, compatible adapter frontmatter and no unapproved files or conflicts.
3. Check required risk controls, prompts versus actual technical enforcement, module dependencies and contradictory instructions.
4. Check policy consistency across canonical docs and generated files; documentation-impact status `stale` is a failure until fixed.
5. For imported source or templates verify file-level provenance, copyright/license notices and generated output obligations.
6. Execute safe relevant tests only with host permissions; report exact commands, results, unknowns and skipped checks.
7. If a genuinely independent read-only verifier ran, record its output. Otherwise label review 'inline' or 'not run'.
8. Output `PASS / NEEDS_REVIEW / FAIL / NOT_VERIFIED` with evidence. Never mark deployment or compliance complete based solely on prompt rules.
