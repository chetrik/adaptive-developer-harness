# Generator and target libraries

The generator has **orchestration Skills** that run inside its source project and a **library of potential target-project Skills/subagents**. Do not conflate them. Selection chooses what the target receives; no blanket copy.

Runtime target components now exist in `library/target/` and are selected by the catalog. The tables below describe the broader library design; they are not claims that every listed role is implemented. Native discovery evidence and remaining limits are in VERIFICATION.md.

## Generator orchestration Skills

| Skill ID | Trigger | Input | Output | Gate |
|---|---|---|---|---|
| `assess-project` | New project or significant change | PRD/idea, repo metadata, host capabilities | Normalized assessment, missing facts | Read-only; no install |
| `discover-reuse` | Commodity/OSS-plausible need | Requirements, tech constraints, web/GitHub access | Evidence-backed build/adapt/buy review | No unverified claims; no execution |
| `select-harness` | Assessment exists | Assessment, catalog/policy/host | Reproducible Harness Plan | No target writes |
| `explain-plan` | Proposed plan ready | Plan, user mode | Plain-language rationale and approvals | Cannot rewrite policy decisions as facts |
| `generate-harness` | Approved valid plan | Plan, target repository, adapter | Bounded file operations + apply report | Explicit approval; protect existing data |
| `validate-harness` | Proposed or generated setup | Plan, real files, test evidence | Structural/semantic/host/provenance report | No unsupported PASS claims |
| `update-harness` | Existing setup changed | Current plan, current repo, new needs | Diff, migration proposal, new plan | No breaking overrides without consent |

## Target-project library examples

| Skill or agent | When useful | Key responsibilities |
|---|---|---|
| Skill: feature-specify | Medium/large changes, requirements ambiguity | Scope, AC, behavior vs implementation separation |
| Skill: architecture-design | Architecture-level decisions | Alternatives, risks, current vs target, ADR where justified |
| Skill: implementation | Approved task | Bounded change, tests, documentation impact |
| Skill: documentation-sync | Canonical docs affected | Stale/updated/N/A matrix with evidence |
| Skill: security-review | Elevated risk | Threat-oriented checklist, permissions, unresolved security gaps |
| Skill: release-check | Public or production deployment | Preflight checks, approvals, rollback, evidence |
| Subagent: explorer | Nontrivial existing codebase | Read-only source mapping and relevant facts |
| Subagent: researcher | OSS/library uncertainty | External research with sources; no execution |
| Subagent: architect | Significant architectural trade-offs | Options, compatibility, constraints, impact |
| Subagent: implementer | Subtask implementation supported by host | Bounded edits, tests and precise status |
| Subagent: verifier | Material change and supported host | Independent read-only review from diff/spec/test evidence |
| Subagent: security-auditor | Elevated risk and expertise available | Independent risk review and findings |

## Canonical Skill contract (recommended)

Each reusable Skill should declare `id`, purpose, triggers/anti-triggers, inputs, required tools/permissions, untrusted-data handling, algorithm, allowed side effects, outputs, evidence requirements, stop conditions, failure fallback, provenance and compatible hosts. SKILL.md is a rendering target, not necessarily the canonical data structure.

## Canonical subagent contract (recommended)

Each subagent should declare role, tools and writable paths (if any), relevant scope, input evidence, output schema, independence expectation, failure mode, parent coordination rules, provenance and host capability limitations. A read-only verifier must not modify code, approve a deployment or mark a task shipped.

## Reuse of external Skills/agents

The team **wants to inspect and may adapt specific third-party Skills/subagents**, especially from `genkovich/sdd` and `gotalab/cc-sdd`. Do not assume they were copied into this archive. Before any import, decide whether it is a direct licensed adaptation, a rewritten independently authored implementation informed by ideas, or a runtime dependency. Maintain original obligations, including in generated target projects.
