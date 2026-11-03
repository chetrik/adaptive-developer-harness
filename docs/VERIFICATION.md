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
- Claude Code/Cursor integration (AT-47), production deployments and legal/security certification.
- Import and propagation of an actual third-party Skill (AT-23/24/44). Original component provenance/license propagation is tested; external adaptation remains deferred.
- A fresh published environment or remote release. All implementation evidence is from this checkout.

## Final bounded walkthrough

The current agent used the calculator PRD and generator URL, retained explicit assessment sources, used observed Codex capabilities, previewed and applied a synthetic test plan under the user's authorization to validate the MVP. Exactly 8 selected files were installed: two Skills, managed AGENTS.md, handoff/UI templates, LICENSE, manifest and executable validator. No application was generated.

The agent read the generated `adh-verify` Skill and ran its integrity command: exit 0, `Harness integrity: PASS`. Application tests were not run because this synthetic target has no application implementation. `python3 tools/probe_codex_skills.py --target <temporary-target>` returned pass with both expected Skills on the final generated files. No native model turn/subagent was invoked.

Final structural validator: 31 required files, 55 requirement IDs and 49 acceptance scenario IDs; schema/catalog/fixture/local-link validation passed. These are separate from the 48 executed runtime tests.
