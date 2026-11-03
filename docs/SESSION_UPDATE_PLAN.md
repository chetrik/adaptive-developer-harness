# Adaptive Session Workflow and Harness Update Management

Status: approved and implemented in bounded form in engine 0.3.0, in revised order: integrity → updates → workflow → handoff. The audit below describes the pre-change 0.2.0 baseline; it is retained as design rationale. Current usage and limits: [UPDATES_AND_SESSIONS.md](UPDATES_AND_SESSIONS.md); stage evidence: [VERIFICATION.md](VERIFICATION.md).

## Audit of the current implementation

| Mechanism | Existing evidence | Gap |
|---|---|---|
| Deterministic route | core.make_plan: XS/S quick, M standard, L/XL full; risk checks remain independent | No structured phase/session recommendation; beginner explanation does not show route |
| Specification/implementation/verification | Selected feature template, implement/verify Skills, conditional review modules | No unified phase contract or per-phase exit evidence |
| Handoff | Always-selected core.handoff template; implement Skill asks agent to fill it | No validated session record, stable resume pointer or freshness check; abrupt termination cannot guarantee a record |
| Incremental generation | make_plan compares hashes and emits only changed create/patch operations | No removal operation, module delta, migration registry or component revisions |
| Existing file preservation | Conflicting ordinary managed files block; AGENTS.md outside markers preserved | Edits INSIDE managed AGENTS block are replaced without a conflict blocker |
| Inventory | manifest lists module IDs, file hashes, provenance; plan fingerprints generator/policy/library/adapter | Installed manifest lacks generator/adapter/component version contract and baseline block hash |
| Approval and recovery | Exact preview, plan/target fingerprints, locks, backups, interrupted-write rollback | No delete recovery or version migrations; recover rejects changed engine/PRD, so old recovery runtime must remain available |
| Verification | Expected file hashes and generated validator | Does not assert absence of removed paths; handoff completeness and runtime behavior separate |

Audit baseline: 55 existing unittest methods pass; structural validator passes. A temporary M→S synthetic plan confirmed that architecture/feature templates and a reviewer can disappear from expected_files without deletion, and an edited managed AGENTS block is replaced in a ready-for-approval plan. No customer files were changed. These findings are not new passing acceptance tests.

## Minimal design: reuse existing boundaries

### A. Session workflow inside the same Harness Plan

Keep one route function in the deterministic policy layer and derive a structured `workflow` section from it. Do not implement separate route logic in adapters or Skills.

| Size | Existing route | Recommendation |
|---|---|---|
| XS/S | quick | Specification → Implementation → Verification in one short session; concise inline spec allowed |
| M | standard | Separate Specification and Implementation sessions recommended; Verification may finish Implementation unless independent review is otherwise required |
| L/XL | full | Specification followed by sessions for bounded implementation milestones; each milestone includes Verification and handoff |

All routes retain risk gates. A new chat is a recommendation, not a mandatory workflow condition. A single-chat fallback preserves phases and checkpoints. Separate chat alone does not establish independent review. The agent proposes concrete milestones from the specification; code validates their structure rather than pretending to infer semantic task boundaries.

Workflow fields: route/reason ID, ordered phases, recommended session boundaries, required artifacts and exit criteria. Specification references requirements, acceptance criteria, relevant existing code and actual scope approval. Implementation follows approved scope. Verification records acceptance results and documentation impact. Changed scope requires reassessment. This is distinct from approval to install/update Harness files.

Use the existing implement/verify Skills and core.handoff module; extend their instructions and feature template rather than installing another complete SDD framework. No automatic session creation is promised; initially boundaries are human/agent instructions. A future native API needs explicit capability evidence and tests.

### B. Session Handoff as mutable project state

Add a strict SessionHandoff schema and bounded agent-facing write/validate operation using existing path and atomic-write safety primitives. Reuse the existing handoff template. Each explicit session close/checkpoint records: session/task ID, phase/status, specification and decision references, changed file paths, workspace revision plus relevant dirty-file fingerprints, actual test commands/results (including skipped/not-verified), documentation impact, blockers and one next bounded task.

Proposed storage: `.adaptive-harness/sessions/<validated-id>.json` with a small current pointer. These are mutable project records, separate from immutable installed component hashes. Do not include private logs, secrets or full chat history. Records are evidence supplied by the agent, not proof of semantic correctness or inherited authorization. Validate links and compare referenced state on resume; stale state triggers reconciliation. Writes require existing task authorization and must not silently change a target after a pending update plan was approved.

No host-independent guarantee of detecting chat closure: instruct the agent to checkpoint at phase boundaries and before an intentional finish; abrupt termination may leave only the last checkpoint. A transcript-free handoff enables manual continuation on hosts without a session API.

### C. Update planning as current-vs-desired reconciliation

Reuse `make_plan`, `select`, adapter rendering, preview, approval and Apply. Add an inventory reader and pure reconciliation helper; do not add a second selector or updater with its own rules.

1. Read and strictly validate installed manifest and actual managed files. Record installed generator, manifest schema, policy/catalog/adapter versions and per-component content revisions. Desired version comes from the reviewed local generator checkout; no automatic download or claim to know the newest remote release.
2. Reassess changed requirements via the existing ProjectAssessment and original PRD provenance. Run the same selection rules.
3. Extend the common Harness Plan with install/update intent, old/new inventory identities, module additions/changes/removals, migration IDs, conflicts and exact operations. Persist version/baseline metadata in the new manifest. Distinguish generator version, component revision and schema version.
4. Reconcile old ownership, current bytes and newly rendered output. Unchanged files get no write. Add/remove files only when ownership and dependencies permit; shared files stay if any selected module owns them.
5. Preserve edits. For ordinary customized components, retain bytes and block conflicting update/removal pending an explicit reconciled plan. Do not silently accept modified security components as verified. For AGENTS.md, compare a separate managed-block baseline; always preserve outside text. No automatic semantic merge in the first increment.
6. Add a typed delete operation to the existing operation contract, with expected-before hash and expected absence after Apply. Never infer a recursive directory deletion, delete application data or discard orphan ownership silently. Empty directories may remain. User-edited obsolete files block removal until explicitly resolved.
7. Reuse exact preview and approval for create/patch/delete. Extend journal, conditional rollback and validation for deletion and expected absence. Save backups before mutation; recovery must preserve intervening user edits. A successful-update revert should be a new previewed/approved inverse plan with current hashes, rather than blindly replaying backups.

### D. Verified version migration

Use a small explicit registry of supported installed-schema/version → target-version transitions. Migrations are pure inventory/plan transformations applied through the same approved writer. No downloaded scripts, arbitrary migration execution or unsupported jump/downgrade. Bind migration identities to plan fingerprints.

First fixture: the actual engine 0.2.0 / manifest schema 1.0 output. It lacks generator/component versions: report unknown instead of inventing them. Recognize known original assets through reviewed release hashes and validate all paths; a manifest's claim of ownership alone is insufficient authorization to delete. For legacy AGENTS without a separate block baseline, conservatively require reconciliation unless a known original block can be established. Unsupported histories remain blocked.

Version transition tests cover supported legacy install, local customization, shared files, unknown/corrupt manifests, failed migration and recovery. Keep the old reviewed engine and plan/state available until an interrupted operation is resolved; changing engines is not a recovery strategy.

## Original proposed order (superseded by user approval)

1. **Workflow contract and rendering:** route table for all five sizes, readable explanations, same route across adapters, risk gates unchanged. No new session lifecycle API.
2. **Session handoff:** schema/write/validate/resume; stale references, missing test evidence, interrupted session and single-chat fallback tests. Native cross-session behavior remains a separate manual check.
3. **Update inventory and reconciliation:** protect managed AGENTS edits first; version inventory, module delta, shared ownership, preview/conflict tests; no unattended updates.
4. **Delete/recovery and first migration:** exact approval, no-follow paths, delete interrupted at each boundary, restoration preserving user edits, expected absence, unknown version refusal, no-op repeat, approved revert. Enable update application only after these tests pass together.

Each stage runs Codex/Cursor regression tests and updates evidence. Preserve the current feature branch and no main merge. Cursor native/macOS gate and remaining adapter order stay unchanged. This shared-core proposal does not declare those integration gates completed.

Affected implementation after review: core.py (or a small shared workflow/reconciliation helper), apply.py, __main__.py, strict schemas, module revision metadata, existing target templates/Skills/validator and tests. No new framework or dependency is proposed. Filesystem allowlist remains bounded; mutable handoff state is excluded from component integrity, not from stale-plan target checks.

## Delivered scope and deliberate limits

The current implementation uses strict manifest 2.0, one supported legacy transition, optional approved removals, structured workflow and immutable ID-addressed handoff records through the same Plan/Apply. No latest pointer or separate session writer was needed. Recovery supports interrupted operations even when PRD changed, while retaining the same engine requirement. Successful-release inverse-plan revert and arbitrary cross-version migrations remain outside delivered scope. Native session APIs are not implemented. See the usage guide for the actual interfaces.
