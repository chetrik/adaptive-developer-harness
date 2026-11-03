# Roadmap — approved executable MVP

0.5.1 bounded improvement: align lightweight instructions, improve task context and UI/acceptance checks, and preserve installed 0.5.0 configurations through the existing update path. Native user-scenario testing is being performed by the owner; no native success is inferred from automated generator tests. Use concrete findings from those trials to prioritize further work.

Current 0.5.0 delivery and verified platform boundaries: [PLATFORM_DELIVERY.md](PLATFORM_DELIVERY.md). Earlier version checkpoints below are historical where superseded.

Approved 2026-11-03. Requirements, code and bounded evidence are mapped in TRACEABILITY.md.

| Milestone | Current status | Evidence / remaining limits |
|---|---|---|
| M0: integrate v2 and public bootstrap | Implemented | 55 requirements and 49 scenario IDs preserved/linked; structural validator passes |
| M1: contracts, deterministic selection, early reuse and beginner plan | Implemented | Selector/contract suite; first checkpoint passed 16 tests before M2 |
| M2: approval, real selected components, Apply/recovery, Codex flow | Implemented for bounded POSIX/Codex workflow | Integration/negative tests, generated checker and native baseline Skill discovery; model comprehension and reviewer invocation remain separately unverified |
| M3: expand candidate research and UX evaluation | Planned | MVP already includes live Git evidence collection, required pre-plan research and readable explanations |
| M4: external Skill adaptation and expanded library | Planned | MVP already installs original selected Skills/rules/templates; external assets need per-file notices and tests |
| M5: additional hosts and advanced migration | Sequenced below | Native evidence is required per adapter |
| M6: release review | Pending | Independent security review, novice evaluation, license review and publication |

All four user-mandated MVP outcomes remain in M0–M2. A passing unit suite does not complete every broad acceptance scenario. No production release or deployment has been performed. See VERIFICATION.md.

## Approved priority order after Codex MVP

1. Preserve Codex regression suite and extract shared adapter interface — implemented in 0.2.0.
2. Cursor shared-Skills adapter — automated Linux integration tests; native rules/subagents pending accessible official contracts.
3. Real Cursor/macOS Apply and Skill application — NOT RUN; follow [test protocol](CURSOR_MACOS_TEST.md). User diagnostics are preliminary evidence only.
4. Claude Code adapter, then Antigravity adapter — planned; verified native contracts and tests required.
5. Lovable Integration + Project Handoff — planned; Project Instructions, AGENTS.md, selected Workspace Skills and confirmed GitHub/ZIP import, actual instruction application, code export. External generator unless Python execution is demonstrated.
6. Google AI Studio Export & Continue — planned; ZIP and supported GitHub export, missing files/services/secrets configuration inventory, preserve existing code. No assumed custom Skill execution.
7. Ollama Model Provider — planned; normalized PRD assessment via API, unchanged deterministic selection.

Each stage runs automated tests, then native integration where available. Native failures/unavailable hosts are reported, never promoted to PASS. Handoff keeps code export, database/data movement and development context/history separate. See [network domains and evidence](PLATFORM_ACCESS.md).

## Shared-core increment: sessions and updates

Scope and acceptance gates are in [SESSION_UPDATE_PLAN.md](history/SESSION_UPDATE_PLAN.md). Approved stages delivered; implementation checkpoints below supersede this original ordering:

1. Derive structured phase/session recommendations from the existing deterministic route.
2. Add validated handoff checkpoints and safe resume with stale-state detection.
3. Add version inventory and incremental update reconciliation; protect managed AGENTS edits and retain ownership of obsolete files until resolved.
4. Add tested deletion/recovery and the first explicit legacy migration before enabling full update Apply.

Run regression checks after each stage and record actual evidence. Existing Cursor/macOS native gate and subsequent adapter ordering remain in force. No new host integration or automatic session API is implied.

Approved revised order: integrity fixes → Harness Update Management → Session Workflow → Session Handoff. Stage 1 checkpoint: implemented and 59 tests passed; managed-block conflicts and pending-removal inventory covered. Subsequent stage evidence is recorded in VERIFICATION.md.

Stages 2 and 3 implemented: incremental versioned updates/migration/deletion/recovery (74-test checkpoint), then structured session workflow (77-test checkpoint). Native Cursor/macOS evidence is still pending; unit counts do not change that gate.

Stage 4 implemented: structured immutable handoff through the same Plan/Apply, resume freshness checks, CLI and interruption tests. Shared-core stage delivery is complete within the documented limits; native Cursor/macOS and model behavior remain separate gates. Usage: [UPDATES_AND_SESSIONS.md](UPDATES_AND_SESSIONS.md). Future work: additional explicitly tested release migrations and native session integration only where supported.

## Engineering Gates — approved 0.4.0 increment

Implemented in sequence: exact 0.3.0 compatibility registry/recovery regression; strict spec/context/readiness contracts; observed unittest RED/GREEN; shared Plan/handoff/managed Skill integration. Automated evidence is recorded in VERIFICATION.md. Remaining: native host gate hooks, verified PDF/DOCX reader receipts, other test runners/CI attestations, authenticated host approval events, independent security review. No second SDD pipeline or universal agent interception. [Operational guide](ENGINEERING_GATES.md).

## Product delivery checkpoint — 0.5.0

Product-delivery priority supersedes the earlier serial platform list: finish existing adapters and real first-task flows; no new framework layers. Delivered code: Claude rendering, 0.4 compatibility, lightweight daily workflow, local Ollama contract, project handoff/export and diagnostics. Remaining release blockers: actual native Claude/Cursor test, confirmed Antigravity/Lovable contracts and native integrations, AI Studio export/account verification, real Ollama model run. PLATFORM_DELIVERY.md is the current capability table.

Native-contract delivery update: official documentation now accessible. Cursor and Antigravity native renderers and Lovable Project Instructions/selected-Skill ZIP packaging are implemented through the same adapter/Plan/Apply. AI Studio ZIP/GitHub Export & Continue is documented and backed by shared inspection/handoff tools. Automated contracts are tested; real host invocation/import/account-dependent steps remain explicitly unverified. Current details: [PLATFORM_DELIVERY.md](PLATFORM_DELIVERY.md).
