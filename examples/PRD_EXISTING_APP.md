# Test fixture — existing application with tiny bug

**User story:** The current web application already has project instructions, tests, CI and a documented SDD workflow. Fix a copy typo and adjust a non-sensitive UI label. Do not modify APIs or data schema. There are uncommitted local changes from the user.

**Expected harness characteristics:** inspect current README/AGENTS/instructions and relevant tests; do not introduce a second full SDD framework, rewrite unrelated docs, install packages, or overwrite dirty files. Present the scope and a bounded diff; run relevant tests where possible. Keep documentation in sync only if the change makes it stale.
