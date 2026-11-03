# Verification evidence — 2026-11-03

Environment: Python 3.12.14; jsonschema 4.26.0; PyYAML 6.0.3; Linux/POSIX. Local development changes are not a published release.

## Milestone evidence

- M0: `python3 tools/validate_package.py` passed after integration: 55 requirement IDs, 49 acceptance scenario IDs. These counts are document coverage, not executed functional tests.
- M1: `python3 -m unittest discover -s tests -p test_selection.py -v` passed 16 tests before application validation.
- M2: `python3 -m unittest discover -s tests -v` passed **48 tests** (exit 0). Tests cover actual writes, selected Skill files, generated validator execution, integrity failures, preservation, repeat Apply, shared locks and interrupted-write recovery.
- Native discovery: Codex CLI 0.163.0 app-server `initialize` → `skills/list` with a synthetic temporary target returned `adh-implement` and `adh-verify` from `.agents/skills/`. No model turn or external installer ran. The initial sandbox attempt could not write Codex's service cache; the same bounded local probe succeeded with approved execution permissions. This is CLI discovery evidence, not a promise for every cloud client.
- Live reuse collector: `python3 -m adaptive_harness research --url https://github.com/frappe/crm` read commit `1615aa6e1d47871f0b4c3214d3e0e9f4faaf5412`, README and LICENSE on 2026-11-03. Automatic MIT/Apache detector returned unknown; no license clearance or completed product-fit recommendation is claimed. No source code or installer from the candidate ran.

## What tests mean

`test_selection.py`: deterministic decisions, unknown risks, pre-plan CRM/CMS gates, dependency validation, immutable policy output and beginner explanations.

`test_apply.py`: four synthetic scenarios; actual selected outputs; validator subprocess; no approval/stale plan/wrong target rejection; symlink/traversal rejection; original user content; recovery; provenance and tamper detection.

`test_entrypoint.py`: two-input bootstrap and agent-operated CLI flow. The test supplies a normalized assessment fixture explicitly; it is not an automated LLM comprehension benchmark. README injection in a research fixture is read as data, never executed.

## Not verified / not implemented

- Broad beginner comprehension study and autonomous model behavior across arbitrary PRDs.
- Native reviewer invocation or independent security review of this implementation.
- Native Cursor/macOS and Claude Code integration (AT-47), production deployments and legal/security certification.
- Import and propagation of an actual third-party Skill (AT-23/24/44). Original component provenance/license propagation is tested; external adaptation remains deferred.
- A fresh published environment or remote release. All implementation evidence is from this checkout.

## Final bounded walkthrough

The current agent used the calculator PRD and generator URL, retained explicit assessment sources, used observed Codex capabilities, previewed and applied a synthetic test plan under the user's authorization to validate the MVP. Exactly 8 selected files were installed: two Skills, managed AGENTS.md, handoff/UI templates, LICENSE, manifest and executable validator. No application was generated.

The agent read the generated `adh-verify` Skill and ran its integrity command: exit 0, `Harness integrity: PASS`. Application tests were not run because this synthetic target has no application implementation. `python3 tools/probe_codex_skills.py --target <temporary-target>` returned pass with both expected Skills on the final generated files. No native model turn/subagent was invoked.

Final structural validator: 31 required files, 55 requirement IDs and 49 acceptance scenario IDs; schema/catalog/fixture/local-link validation passed. These are separate from the 48 executed runtime tests.

## Cursor increment, engine 0.2.0

55 unittest methods passed on Linux (48 existing + 7 new); structural validation passed with 59 requirements / 53 acceptance scenarios. New tests cover four Cursor Apply scenarios, preservation/idempotency, same shared selector decisions, executor/target separation, unsupported discovery, adapter tampering and original document reading/hash gates. Codex regression tests pass.

Native Cursor/macOS is NOT RUN. Official Cursor pages returned HTTP 403; only user-reported shared-Skills format is used. No third-party implementation/assets/dependencies were added. No native rules, Hooks or subagent configurations for Cursor are claimed. PDF/DOCX contract tests use synthetic bytes; they do not prove real parser/OCR behavior. The current increment does not rerun Codex native discovery; the earlier recorded baseline evidence remains scoped to its original run.

## Session/update stage 1 checkpoint

59 tests passed (55 baseline + 4 integrity cases). Managed AGENTS block edits block approval; edits outside the block are preserved. Deselected files retain hashes/provenance and pending_removal status, including repeated planning; edited obsolete files block changes. Structural validation passed. Removal/migration was not enabled at this checkpoint.

## Session/update stage 2 checkpoint

74 unittest methods passed; structural validation passed. Manifest 2.0 stores generator/policy/catalog/adapter versions, component content revisions, owners and pending removals. The unchanged selector feeds incremental update plans; --remove-obsolete previews deletion but grants no approval. The existing Apply/journal handles approved create/patch/delete and verifies absence. Tests cover pending→removal, edited/forged/unknown inventory rejection, repeat no-op, deletion interruption/recovery, rollback after later write failure, intervening user work, and real stored 0.2.0 output migrating from manifest 1.0. Native host behavior remains separately unverified.

Legacy manifests lack version identity and a block baseline. Original assets are recognized by reviewed hashes; edited legacy AGENTS (including outside text changes) conservatively blocks until reconciled. Interrupted recovery still requires the reviewed engine and unchanged PRD used for the plan. No unattended download or arbitrary-version migration is implemented.

## Session/update stage 3 checkpoint

77 unittest methods passed; structural validation passed. workflow.py derives all five feature sizes into the same common plan/rendered guidance for Codex and Cursor. Tests cover phase order, optional chat boundaries, inline XS/S specification with no extra feature document, security checks for small risky tasks, and rejection of forged workflow output. This validates deterministic guidance, not automatic session creation or model compliance.

## Session/update stage 4 and final verification

Final suite: **90 unittest methods passed** on Linux, including all existing Codex/Cursor regression cases. Stage 4 first checkpoint passed 85 methods; final additions exercise real CLI checkpoint/resume, every deletion boundary, shared ownership, Codex→Cursor reconfiguration, and interrupted legacy migration recovery after PRD change. Structural validation: **63 requirements / 58 acceptance scenario IDs**, schema and local-link checks passed. These document counts are not claims that every broad scenario is fully satisfied.

Session records use the same approval/Apply/journal, remain outside installed component hashes, reject invalid references/inconsistent reported test results, and detect workspace drift on resume. Explicit checkpoints only: no host close-event API or autonomous native session evaluation. Test commands in records are not executed by the recorder.

Recovery improvement supersedes the stage 2 limitation about unchanged PRD: a changed/missing PRD no longer prevents rollback of the approved journal, but does prevent applying the stale plan. Recovery still uses the same reviewed engine. Successful-release downgrade/revert and unknown-version migrations are not implemented. The retained legacy fixture is original project output, not third-party material; no new dependency or external assets were introduced.
