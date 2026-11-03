# Selection policy: minimum sufficient, explainable harness

Status: executable MVP in `adaptive_harness/core.py`; the broad examples below remain product guidance. Exact supported behavior and limitations are in ARCHITECTURE.md and VERIFICATION.md.

Runtime routes derive from feature size (XS/S → quick, M → standard, L/XL → full). Project scale independently affects project-level artifacts. Security gates remain required on every route. The catalog uses a finite allowlist of trigger names, not Python expressions or LLM instructions. Missing/changed hard-baseline rules, graph cycles and missing dependencies are errors. Reuse evidence must precede ready-for-approval for commodity systems.

## Inputs

1. Product intent: purpose, first release vs full vision, internal vs public, commercial/monetization intent, users and data.
2. Current repository evidence: files, commands, framework, tests, deployment, existing agent instructions and policies.
3. Complexity: feature size (XS/S/M/L/XL as a heuristic), overall project scale, user-facing surfaces (web, mobile, desktop, API, CLI, worker, library), number of integrations, change/migration risk.
4. Security/privacy risk: sensitive data, authentication, payments, children, internet exposure, production, data retention, regulated contexts; uncertainty must be made visible.
5. Host features: read/write, network, Skills, subagents, permissions, hooks, CI, platform syntax.
6. User preference: Beginner/Developer explanations, approvals, resource/cost constraints, optional skill preferences.

## Computation principles

- **Start from an irreducible safety-and-honesty baseline**, not from an empty unchecked setup.
- Evaluate each module: `required / recommended / optional / not-applicable / blocked-by-host / conflict`. Assign a reason and evidence.
- Risk-driven elevation can add hard validation gates **without adding unrelated documents**.
- Determine workflow route after checking what already exists; do not require replacing a functioning stack or introducing competing methodologies.
- Show the effect of user overrides; require explicit escalation for overrides that affect risks, and never silently disable hard safety checks.
- De-duplicate functions: choose one authoritative owner for specification lifecycle, review protocol, and release process.
- Check dependencies and conflicts, adapters and platform capability before producing file operations.
- Preserve existing files: on conflict propose reuse, incremental patch, or user-approved migration; no blind overwrite.
- Provide file-level diffs/preview, estimated maintenance burden and user-facing rationale before apply.

## Sample selection matrix (illustrative, not fixed product rules)

| Signal | Suggested components | Omit / avoid if not applicable |
|---|---|---|
| One-page offline calculator, no personal data | Minimal PRD, single entrypoint, basic tests, concise security basics | Separate ADR collection, multiservice architecture, payment/security subagents |
| Existing app, focused bug fix | Inspect existing tests, bug repro, bounded fix, tests, doc-impact check | Entire greenfield SDD scaffolding |
| UI feature | UI flow/screens, accessibility and UI smoke checks scaled to scope | HTTP contract for UI-only change without API modification |
| Changed persistence schema | Data model and migration safety, rollback/backup plan | Data migration artifact if schema unchanged |
| Public API changed | Interface contract and backward compatibility checks | New API docs if public interface untouched |
| CRM processing customer records | Privacy/data flow, authN/authZ, tenant/role checks, real-OSS evaluation, production safety | Prototype-only shortcuts when exposed to real data |
| Payment processing / sensitive SaaS | Security escalation, test tiers, strict approvals, reviewer, deploy gates | Disabling controls because module count is small |
| Solo personal workbook utility | Example inputs, bounded automation, functional test, minimal docs | Marketing research unless future distribution planned |
| No subagent support | Inline review labeled non-independent; optionally request alternate host | Claiming independent verifier ran |
| Existing mature SDD framework | Integrate or reconfigure existing rather than stacking another full framework | Duplicate SDD lifecycle / conflicting constitutions |

## Two different decisions (do not conflate)

- **Project Harness selection:** which capabilities and durable documents to install for the *whole project* (once or on major project change).
- **Feature route:** for a specific change, which steps are N/A and which validations are needed. A one-line CSS fix in a sensitive SaaS may use a short feature route while retaining the project's permission/security policies.

## Required explanation for every module decision

- `id`: stable catalog identifier.
- `decision`: selected/skipped/blocked.
- `trigger`: requirement, risk, host or user preference.
- `evidence`: PRD section, observed file, tool capability check or user statement; label inference if uncertain.
- `reason`: brief beginner-readable rationale.
- `dependencies`: required companion modules.
- `cost`: new files, complexity, recurring tools or maintenance.
- `status`: planned, generated, verified; never conflate.

## Example of explicit skip

`ui.screen-manifest = not-applicable; reason: target is a command-line CSV converter with no UI surface. No screens.md generated.`

## Anti-patterns

- Installing all 23 or all 17 Skills because a source framework offers them.
- Adding a separate ADR and full architecture document for an XS copy edit without a specific need.
- Promising safety because Markdown says `be secure`.
- Guessing the adapter paths or claiming untested platform support.
- Asking beginner to decide PostgreSQL vs SQLite without first explaining constraints and presenting justified options.
