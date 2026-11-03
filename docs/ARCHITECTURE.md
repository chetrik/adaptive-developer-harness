# Architecture — executable MVP and remaining boundaries

Current 0.5.0 delivery and verified platform boundaries: [PLATFORM_DELIVERY.md](PLATFORM_DELIVERY.md). Earlier version checkpoints below are historical where superseded.

## Current state

The approved Python + JSON Schema + YAML MVP is implemented in the existing repository. `adaptive_harness/` is the executable package; `library/skills/` remains the generator's orchestration guidance, and `library/target/` holds original components rendered into customer projects. No second project or external framework is installed.

| Layer | Implementation | Boundary |
|---|---|---|
| Agent bootstrap | BOOTSTRAP.md, bootstrap.py | Agent reads PRD and observes capabilities; scaffold retains unknowns |
| Reuse evidence | research.py, ReuseEvaluation schema | Read-only Git/README/license collection; agent must finish candidate fit/cost/integration analysis before final planning |
| Contracts | contracts.py, schemas/*.schema.json | Local JSON Schema validation; provenance of facts remains an agent responsibility |
| Catalog/policy | catalog/modules.yaml, core.py | Typed triggers, hard baseline, graph validation, dependency closure, conflict and host checks |
| Planning | core.py | Stable selected/skipped reasons, exact contents, diff, input/tool/library fingerprints; no target writes |
| Explanation | core.explain | Ukrainian selection/skips/risks/next action; same policy in both modes |
| Approval | apply.approve | Explicit user-event reference bound to immutable plan/target; not identity authentication |
| Apply/recovery | apply.py, filesystem.py | Allowlisted paths, no-follow ancestors, no-clobber creates, journal, conditional rollback, external state and target locks |
| Target components | library/target | Real Skills, selected templates, managed rules, validator, optional read-only Codex agent definition |
| Evidence | apply.verify, generated validate.py | File hashes/provenance; application tests, native discovery and independent review reported separately |

## Flow

PRD + URL → read-only agent assessment + candidate research → validated assessment → deterministic plan → human explanation and exact preview → explicit approval → Apply → checks and handoff.

The selector itself performs no network calls, evaluates no arbitrary YAML expressions and does not call an LLM. The plan hash includes normalized assessment, target snapshot, engine/schema fingerprint, policy/catalog/library fingerprints and exact operations. Metadata such as approval time is outside deterministic planning. A changed external PRD is rechecked before approval/application.

Security facts are true/false/unknown; inferred absence remains unknown. CRM/CMS/auth/billing always require pre-plan reuse research, even if a user-supplied commodity flag says false. Unsupported hosts or unverified required capabilities block final planning. Without confirmed subagents a risk-bearing plan uses an explicitly non-independent inline review.

Existing AGENTS.md text outside the managed block is preserved byte-for-byte in UTF-8. Unmanaged conflicting output files block Apply; changed managed files require reconciliation. A repeat of an applied plan checks its receipt and target snapshot and performs no writes. New plans also verify unchanged installed files through `expected_files`.

## Scope and limitations

- Run from a reviewed repository checkout on Python 3.11+ / POSIX. No standalone wheel, SaaS or LLM API dependency.
- Target scan is bounded to 10,000 entries and 64 MiB of regular-file content, excluding .git. Credential paths use metadata only; their values are not read. Larger targets require a future scoped-snapshot design, not bypassing checks.
- All file operations require human approval. A local receipt is not a cryptographic proof of consent. The trusted coding agent/host must only record approval after a real human response.
- Advisory locks coordinate generator writers; prohibit concurrent non-cooperating writers during Apply. No claim of multi-file transactional atomicity. Journals permit recovery and preserve conflicting user edits.
- Codex CLI 0.163.0 has discovered generated baseline Skills. This does not prove subagent invocation, model compliance or cloud-wide registration. The optional reviewer definition is conditional and its execution remains separately verifiable.
- Only original target assets are rendered. External Skill import/license propagation across third-party assets and other host adapters remain future work.
- The historical v0 calculator JSON is archived under docs/history; `schemas/harness-plan.schema.json` stays at its original path because it participates in the engine fingerprint; runtime uses `plan-v1.schema.json` and `examples/assessments/`.

## Verification history

M0: 55 requirements / 49 acceptance scenarios structurally checked. M1: 16 selector tests passed before M2 validation. M2: integration and negative checks are recorded in [VERIFICATION.md](VERIFICATION.md); they do not imply every acceptance scenario has passed.

## 0.2.0 adapter boundary

`adapters.py` normalizes legacy host or paired ExecutionHost/TargetPlatform into effective capabilities for the existing selector. Executor supplies read/write/execute; target supplies native_skills/subagents. The renderer is versioned in Harness Plan and covered by fingerprints/approval. Codex uses existing outputs unchanged. Cursor currently shares `.agents/skills/`, portable AGENTS.md and templates/validator; unsupported native subagent rendering reduces effective subagents to false, selecting existing inline-review rules. No new filesystem namespace is allowed. Native Cursor rules/Hooks/agents await readable official contracts.

ModelProvider is assessment metadata only in this increment. Future Ollama interprets PRD into the same validated assessment; it cannot change selection, approvals or filesystem policy. Existing schema_version 1.0 assessment fields remain compatible; the engine advances to 0.2.0 and requires adapter identity in new plans. Old plans must be regenerated and approved again.

The agent reads PDF/DOCX/Markdown, preserving original bytes/hash and requirement locators; the engine validates reading metadata and gates incomplete binary-document intake. It does not claim to verify whether a reader understood every page. See BOOTSTRAP and CURSOR_MACOS_TEST for runtime evidence boundaries.

## Session and update design history

See [audit and minimal design](history/SESSION_UPDATE_PLAN.md). Extend the existing route into structured workflow recommendations; keep one selector and one Harness Plan. Add validated mutable session state outside component integrity hashes. Extend current-vs-desired planning with versioned inventories, module delta and typed delete operations; reuse preview, approval, journal and recovery. Migrations transform inventory/plan through an explicit tested registry, not a second filesystem executor.

Audit limitation: existing managed AGENTS block edits can currently be replaced without a conflict blocker. Deselected files are not removed and can fall out of manifest tracking. Existing recovery handles interrupted create/patch, not verified cross-version migrations or successful-update revert. These gaps must be closed before claiming update management. This describes the pre-change audit; the implementation below supersedes these gaps.

## Update implementation checkpoint (0.3.0)

The same make_plan now reads a strict installed inventory via inventory.py. New manifest schema 2.0 stores versions/owners/component revisions and a managed-block hash. Explicit manifest-1-to-2 migration recognizes original 0.2.0 assets using catalog/legacy-component-hashes.json. Unknown revisions block. Obsolete files remain tracked by default; remove_obsolete adds exact deletion operations to the same approved plan and existing journalled Apply. No directories are recursively deleted. This supersedes the audit's two integrity gaps; tested evidence is in VERIFICATION.md.

## Session implementation checkpoint (0.3.0)

workflow.py is the single route function consumed by the common plan and renderers. XS/S use inline specifications; M and L/XL get recommended boundaries without mandatory chats. Every route has Verification criteria and risk-based checks. handoff.py validates agent-reported session records and compares a workspace fingerprint on resume. handoff-plan extends make_plan and uses the existing approval/Apply/journal; it refuses mixed Harness updates. Immutable session IDs eliminate a mutable latest pointer. Session data stays outside component inventory; normal plan freshness still covers those files. No session lifecycle API or automatic test execution is asserted.

## Engineering Gates: shared extension in 0.4.0

`gates.evaluate` consumes the existing selection/workflow route plus strict task contract. It computes readiness; it does not select/install modules or create a second lifecycle. Optional engineering request/readiness extends the single Plan and existing handoff. `evidence.py` provides bounded reader and external host-owned receipts; `verification.py` observes a fixed unittest runner and binds evidence to current workspace/code/test inputs. Receipts use the existing external state write helper, never a second target Apply. The original Apply/journal owns all target component and handoff mutations.

Task spec approval and test execution authorization are separate from install approval. Receipt integrity is not user identity authentication; the host remains the authority. Historical handoff readiness cannot substitute for current evaluation. Formats, threat boundary, commands and version transition: [ENGINEERING_GATES.md](ENGINEERING_GATES.md).

## Product delivery checkpoint — 0.5.0

0.5.0 adds Claude path/asset mapping in the existing Adapter and extends the existing inventory allowlist across adapters. No second selector or Apply. provider.py handles local interpretation only; project_handoff.py inspects/exports explicitly selected application files to an external archive, never installs Harness or executes exported code. diagnostics.py reports runtime availability separately from native discovery. See PLATFORM_DELIVERY.md.

Native-contract delivery update: official documentation now accessible. Cursor and Antigravity native renderers and Lovable Project Instructions/selected-Skill ZIP packaging are implemented through the same adapter/Plan/Apply. AI Studio ZIP/GitHub Export & Continue is documented and backed by shared inspection/handoff tools. Automated contracts are tested; real host invocation/import/account-dependent steps remain explicitly unverified. Current details: [PLATFORM_DELIVERY.md](PLATFORM_DELIVERY.md).
