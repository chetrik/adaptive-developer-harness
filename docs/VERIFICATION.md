# Verification evidence — 2026-11-03

## Durable bootstrap artifacts after Claude trial

BOOTSTRAP and the user/assessment guidance now specify persistent original PRD storage, separate retained plan runs, a durable shared recovery state-dir and the original reviewed generator checkout. Source copies require applicable write authorization and byte comparison; changed sources require regenerated plans. Installation permission is distinct from application work; native Skill invocation is distinct from manually following a file. Historical comparisons without retained artifacts remain unverified.

`python3 -m unittest discover -s tests -v`: **136 passed**, exit 0 (31.925 s). Structural validation and `git diff --check` passed. Runtime, managed components and engine/library hashes are unchanged. These are agent instructions, not a new persistence mechanism; actual retention and adherence in native environments remain to be verified.

## Bootstrap clarification after user-provided Claude trial

The supplied transcript showed a prose proposal, not an executed generator plan or installation. BOOTSTRAP, the copyable Ukrainian prompt and generator-side assessment guidance now explicitly avoid redundant preparation approval, arbitrary Skill limits, handwritten entrypoint selection and omission of UI requirements. This changes guidance only: runtime, managed assets, engine/library hashes and migration contracts are unchanged.

Validation: `python3 -m unittest discover -s tests -v` passed **136 tests** (29.257 s, exit 0); `python3 tools/validate_package.py` and `git diff --check` passed. No new native run was performed; a repeat Claude trial must verify actual adherence. No tests asserting prose wording were added.

## 0.5.1 lightweight workflow and guidance patch

- `python3 -m unittest discover -s tests -v`: **136 tests passed**, exit 0 (30.560 s). Includes Codex/Cursor regressions and 4 new migration tests with Codex/Cursor/Claude subcases.
- `python3 tools/validate_package.py`: passed, exit 0; 35 required files, 67 requirements, 64 acceptance scenario IDs, local links and plan schema. Scenario IDs are not a count of executed native trials.
- `git diff --check`: passed. No native host scenario was run for this patch; the owner is conducting those trials separately.
- Verified 0.5.0 → 0.5.1: preserve user files and text outside the managed AGENTS block; block customized components and stale approvals; recover an interrupted write, retry, and produce no operations on unchanged repeat. The original 0.5.0 checkout can still recover its own interrupted operations before a new upgrade.
- Existing 0.3.0/0.4.0 migration/recovery tests pass. Manifest remains 2.0; target paths/platform formats are unchanged. Generator engine/library fingerprints change, so old plans require a fresh preview and approval. Apply and formal gate enforcement code are unchanged.
- Generated guidance now aligns small-task handoff with the quick route and strengthens bounded context, beginner choices, UI journeys and criterion-based verification. This tests delivery/integrity, not LLM adherence.

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

## Repository cleanup verification

Cleanup retains all runtime sources, schemas (including fingerprinted historical schemas), catalog, target assets, LICENSE and legacy migration fixture byte-for-byte against commit 0ede22c. Only contributor guidance, documentation navigation, historical placement and development checks changed. No main merge was performed.

- Full regression suite: **92 unittest methods passed** (90 existing + 2 explicit repository/output boundary tests). This includes legacy manifest migration, interrupted migration/deletion recovery, user-edit preservation, session handoff and Codex/Cursor coverage.
- Structural validation passed: 35 required paths, 63 requirements, 58 acceptance scenario IDs; local Markdown links and all schemas validated. Historical v0 example remains validated at its new archive path.
- Eight fixture/host combinations produced the exact same per-file output hashes as before cleanup. Each was applied, reapplied with already-applied status, and replanned with zero operations. No internal or historical documentation entered the target.
- README → BOOTSTRAP → PRD + generator URL remains the active entry; BOOTSTRAP and executable bootstrap are unchanged. Contributor instructions reside in AGENTS.md, distinct from generated AGENTS.
- engine_hash unchanged: `5df62584f6f87710af13d1cd7d76aa00db1c6dd9f99f61e271edc0c2f93ecf4f`.
- library_hash unchanged: `13293c5106154d4ba357d64f3cd47c6084d9316b0b1dc2e12a600b687c0207dd`.
- catalog fingerprint unchanged: `28c34539578ebf6d5311aecdc2a3fdbf94c620f6371afc7f9a57f76ec0b91b59`.

Tracked structure after cleanup: **101 files total: 92 active/development/compatibility files and 9 historical files under docs/history/** (including its index). Eight files moved into history; two duplicate documents were merged and their old paths removed. This is a navigation cleanup, not a smaller runtime or new release of component formats. Existing valid 0.3.0 plans retain their fingerprint compatibility; target/PRD freshness conditions still apply. Unknown engine versions remain unsupported. Native Cursor/macOS behavior was not evaluated by this cleanup.

## Engineering Gates stage 1 checkpoint

Existing 92 regression tests passed; four additional 0.3.0 migration tests passed. Preserved exact original output and component hashes. Explicit 0.3.0 → 0.4.0 transition retains manifest 2.0. Tests cover customization conflicts, stale plans, migration interruption/recovery/retry, and actual recovery with pinned original 63dc1bd code from local Git. New Apply refuses to overtake unfinished journals in the supplied state directory; callers must reuse the original state directory and retain the reviewed old checkout.

## Engineering Gates stage 2 checkpoint

108 tests passed, including 12 initial gate/evidence cases; structural validation passed. Shared evaluator enforces spec completeness, approval identity, context delivery/freshness and stage readiness. Host-owned HMAC receipts distinguish actual bounded reader/test observations from arbitrary JSON. A real synthetic unittest assertion failed before the fix and passed after it; changed expectations, fabricated receipts, old code results, skips/import errors/timeouts/empty suites were rejected or not-verified. Local receipts are not protection against a malicious owner of the host/key; observed delivery is not comprehension.

## Engineering Gates 0.4.0 final verification

Stage 3/4 integrated gate, CLI and handoff checks passed: 18 engineering tests. Full regression: **115 unittest methods passed** (92 baseline + 18 gates/evidence + 5 version migration tests). Five migration methods also passed after extending pinned 0.3.0 execution to interruption AFTER a real file write, in addition to the pre-write journal interruption. Structural validation: **35 required paths, 67 requirements, 64 acceptance IDs**, all local Markdown links and schemas valid. These are automated Linux results; no new native Cursor/macOS or Codex model/hook enforcement run is claimed.

Confirmed: inline XS/S, incomplete complex specification rejection, stale/forged/missing evidence, bounded/protected context, initial RED and current GREEN, changed expectations and undeclared fixture rejection, no execution from spec consent alone, crash/skip/empty suite/timeout/output limits, shared Plan/handoff integration for both adapters. All existing Codex/Cursor, updates, deletion, recovery and boundary tests pass. Migration recognizes frozen 0.3.0 assets, rejects user edits/unknown versions/stale plans, recovers/retries interrupted updates, rejects unfinished old journals and recovers with the actual original engine. Unchanged replan produces zero operations.

Changed managed output: generated AGENTS block and existing feature/implement/verify/handoff assets, plus manifest metadata. No new third-party dependencies or imported implementation; only original project output is retained as migration fixture. Changed/new-file credential-pattern scan found no matches; no files exceed 1 MiB. This bounded scan is not independent security or legal certification.

Engine fingerprint is intentionally changed to `6bff53fe34225ab0ddc2287fed15bc8017ccdc35d283ed2ef294c163b5fb13cf`; library fingerprint is `06b5c8675173cf239f8d7135c7d0a062f6af41c38a3d539ee8039de2be5f8500`. Old plans require their original reviewed engine for recovery; new updates require a fresh approved plan. Manifest remains 2.0. The full trust boundary and remaining runner/native-reader limits are documented in [ENGINEERING_GATES.md](ENGINEERING_GATES.md).

## Product/platform delivery 0.5.0

**132 regression tests passed** on Linux/Python 3.12.14, including all previous safety/update/workflow/Engineering Gates cases, 14 delivery tests and three Ollama-provider tests. The delivery suite was additionally rerun after replacing the synthetic old-Cursor metadata setup with frozen output produced by the actual pinned 0.4.0 engine: 13 passed. Structural validation passed (35 required paths, 67 requirements, 64 acceptance IDs), all local links/schemas valid, git diff whitespace checks clean.

Verified executable behavior:

- Shared selector/Plan/Apply for Codex, Claude Code, Cursor, Antigravity, and Lovable external import-package target. Repository-boundary tests cover four project fixtures per adapter; internal/historical docs never enter installed output.
- Claude native-format Skills, entry and readonly-tool reviewer; Cursor .mdc alwaysApply rule and readonly reviewer; Antigravity always_on rule and exact view_file/grep_search reviewer contract. Original target assets; no new project dependency or copied third-party implementation.
- Lovable external generation accepts unknown native discovery only for preparing import packages, never claims activation. One-Skill ZIP layout, size/name limits, no overwrite, edited-Skill refusal, and supplied instruction differences requiring semantic review tested. Actual UI/account import remains not run.
- Existing-code export preserves selected bytes; inspection lists dependency/env/service/context gaps, excludes secret-like files, refuses traversal/symlink inputs and unsafe ZIP paths. Database, accounts and chat history explicitly separate. Archive inspection does not extract or execute untrusted code.
- Real loopback HTTP server exercises the Ollama /api/chat request/structured-response contract. Inference cannot grant observed capabilities or mark reading complete; remote endpoints rejected. No real Ollama model was installed/run.
- Generated Claude Harness coexists with a working JavaScript application: actual `node --test` and generated integrity checker pass; unchanged replan produces zero operations. This is application/runtime evidence, not an LLM-turn test.
- Exact 0.4.0 Codex and Cursor output fixtures; 0.3/0.4 → 0.5 update, customized-file blocking, pending removal across adapter switch, approved deletion, interruption/recovery/retry/no-op. Original 0.3 and 0.4 Git checkouts recover their own interrupted operations (before and after file write) before current-engine upgrade. Unknown versions remain blocked.

Native checks: Claude Code 2.1.317 was installed temporarily outside the repository and `claude doctor` returned 0 inside a generated project. It reported no usable sign-in credentials; model invocation, Skill application and reviewer execution were NOT RUN. Codex 0.163.0 app-server startup currently fails with read-only filesystem; older discovery evidence is historical. Cursor/macOS and Antigravity native sessions and Lovable/AI Studio account actions were NOT RUN. Do not convert documented format support into a native behavior claim.

Documentation access: after user-approved network configuration was saved, official Cursor, Antigravity, Lovable and AI Studio pages returned HTTP 200 and their contracts were read. Claude official pinned GitHub examples and Ollama official pinned API docs supplied remaining contracts; source links in [PLATFORM_DELIVERY.md](PLATFORM_DELIVERY.md).

Current engine hash: `d52d23f60159817dcf46cae05bde50c987f643eecdc29738a649cbb8dd7669db`. Library hash: `7075c70d183996c53b97670fd82fa2ee0d1478536ee25c643026943f33a0b364`. Both intentionally change with 0.5.0; old recovery keeps its original reviewed engine. Manifest format remains 2.0. Small-task instructions now permit inline scope and the application's real test runner without mandatory task JSON or machine receipts; formal gates remain available without fabricated verified results.

Final additional RED → GREEN regression caught AGENTS.md pointing at the Codex Skill path for Claude/Lovable. The generated entry now derives its Skill path from the selected adapter; all five variants pass. Full suite after this fix: 132 passed. Secret-pattern review of all 48 changed/new files found no matches and no files over 1 MiB; this is bounded scanning, not independent certification.
