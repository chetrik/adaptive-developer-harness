# Architecture — executable MVP and remaining boundaries

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
- Existing legacy `harness-plan.schema.json` and calculator JSON are marked historical v0 examples; runtime uses `plan-v1.schema.json` and `examples/assessments/`.

## Verification history

M0: 55 requirements / 49 acceptance scenarios structurally checked. M1: 16 selector tests passed before M2 validation. M2: integration and negative checks are recorded in [VERIFICATION.md](VERIFICATION.md); they do not imply every acceptance scenario has passed.
