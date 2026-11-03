# Roadmap — approved executable MVP

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
