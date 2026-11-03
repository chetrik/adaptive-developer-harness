# Product Requirements Document — Adaptive Developer Harness Generator

**Version:** 2.0 MVP · **Date:** 2026-11-03 · **Status:** architecture and M0–M2 approved; implementation evidence is in TRACEABILITY and VERIFICATION.
**Canonical product intent:** this document.  
**Audience:** beginner/non-technical project owners first; also experienced developers.  
**Language of user conversation:** default Ukrainian; public/source identifiers may be English.

## 1. Problem

A non-developer can describe an application to a coding agent but may lack the expertise to choose and maintain the development process around it: project files, security practices, architecture decisions, specifications, testing, independent review, deployment readiness, and agent instructions. Copying a comprehensive SDD framework into every project creates unnecessary ceremony; starting without safeguards can miss critical risks. Existing agent workflows are frequently tied to specific hosts.

## 2. Product goal and scope

Build a repository-driven **meta-generator** that consumes a PRD (or short idea that it helps refine), optionally an existing repository, and the capabilities of the current coding-agent environment. It assesses the project and proposes a minimal justified Developer Harness. After user approval, it creates or updates only relevant components and validates the result.

**Not building:** a new LLM, full coding IDE, universal CRM or other user application, production runtime for customer agents, unsupported one-click installer, automatic guarantee of legal/security compliance, or mandatory training course for new developers.

## 3. Intended user experience

A user may say: “I want a CRM for my tourism business.” The agent helps structure needs, checks whether adapting a real, verifiably licensed open-source CRM or existing service would make sense, evaluates risk, offers a tailored Harness Plan in plain language, gets approval, and then generates the project-specific process. The user controls critical decisions. Agent handles authorized routine technical work.

### UX contract

- **[UX-01] Progressive intake.** A short free-form or voice-derived idea is enough to start. Help shape a PRD, distinguishing proposed future features from first-version scope. Do not require a perfect up-front document.
- **[UX-02] Progressive disclosure.** Show what/why/impact/decision first; provide technical detail on request. Do not explain every line of code or overload the user with status chatter.
- **[UX-03] Experience modes.** Beginner (default for target product) and Developer. Modes affect explanations and interaction, not essential safety requirements.
- **[UX-04] Fewer questions.** Infer from supplied context when safe, explicitly mark uncertainty; ask for facts the user must choose (e.g. data sensitivity, permissions, business constraints). Bundle only related blocking decisions.
- **[UX-05] User-language and handoff.** Explain unfamiliar terms the first time they affect a decision and provide short practical next steps; maintain an agent-portable handoff.
- **[UX-06] Purpose-sensitive discovery.** Do not force marketing/target-audience research for a tool built only for personal/internal use. If the user aims to sell or share the product, offer proportionate customer/JTBD and competitor research.
- **[UX-07] Learning without a gate.** Offer optional teaching notes and ready-to-use examples; users need not master architecture or file layouts before a harmless prototype.
- **[UX-08] Small safe experiments.** When feasibility is uncertain, propose a bounded proof of concept with test data instead of committing to a complex system.
- **[UX-09] Costs and portability.** Disclose recurring API/hosting fees and vendor lock-in risks; keep essential project state in version-controlled files where feasible.

## 4. Functional requirements

### Project intake and diagnosis

- **[AS-01] Assess new and existing projects.** Detect greenfield/brownfield status; read only relevant files, note dirty git state, existing instructions, tests, architecture and toolchains. Do not overwrite existing controls.
- **[AS-02] Classify complexity across two dimensions.** Project-level scale/risk and feature-level size (XS/S/M/L/XL or equivalent); consider system boundaries, new APIs/migrations, change size, user interfaces, dependencies, consumers and expected effort. Avoid rigid dependence on inaccurate estimates.
- **[AS-03] Identify risk signals.** Customer/personal data, payments, authentication, children, financial/health data, public exposure, irreversible changes, production deployment, regulatory obligations, secrets and third-party integrations. Record unknowns and escalation.
- **[AS-04] Inspect execution capabilities.** Determine coding agent, supported Skills/subagents, file permissions, allowed tools, hooks, sandbox, network access and CI capabilities. Use fallbacks; never claim native support without checking.
- **[AS-05] Maintain bounded context.** Discover file metadata first; read only relevant sources; keep outputs and decisions available across sessions/hosts.

### Reuse-first research

- **[RU-01] Evaluate build/adapt/buy.** Before committing to building a substantial commodity subsystem, check whether existing OSS projects, supported services, libraries, and templates meet requirements. Research may be opt-in for trivial work.
- **[RU-02] Validate every concrete candidate.** Confirm repository URL, license, copyright/NOTICE, maintenance, release age, open issues where available, security concerns, supported stack, hosting cost, integration complexity and functional coverage. Cite exact evidence and date of verification.
- **[RU-03] No invented evidence.** Without live/reliable access, state research is unavailable or unverified and request permission/data if necessary. Treat star counts as weak signals, not quality guarantees.
- **[RU-04] Compare trade-offs.** Produce an explicit option analysis with reasoned recommendation and what would have to be built/changed. Never silently ingest third-party code.

### Selection, planning and approval

- **[SE-01] Explainable selection engine.** Select a minimum sufficient set of instructions, docs, specs, checks, Skills, subagents, and adapters based on project signals, risks, and user preferences. Every module has triggers, prerequisites, exclusions, cost/context burden and a reason.
- **[SE-02] Conditional routes.** Offer quick/standard/full or equivalent, with explicit skip rules for irrelevant stages (e.g. no UI → no screens; no schema change → no migration plan). Essential risk controls must not disappear just because a project is small.
- **[SE-03] Avoid incompatible duplication.** Do not install multiple complete competing SDD workflows in one target by default. Distinguish selecting a framework from borrowing a practice.
- **[SE-04] Resolve dependencies and conflicts.** Machine-readable module metadata; stable IDs, compatibility, versions, platform support; report contradictions instead of inventing precedence.
- **[SE-05] Human review of a Harness Plan.** Before file writes or installation, show selected and skipped modules, motivations, target files, impact on existing files, unresolved risks, cost and approval requests.
- **[SE-06] Intentional overrides.** Allow users to change route/module decisions, log rationale, warn when risk is increased, and prevent unsafe bypass of mandatory controls.
- **[SE-07] Deterministic planning core.** With the same normalized inputs, policy version, catalog version and host capabilities, core selection should produce equivalent decisions; LLM helps infer inputs/explanations but is not the sole policy authority.

### Generation and maintenance

- **[GN-01] Generate approved components only.** Compare intended changes, preserve existing files, idempotent reruns, clear merge/diff behavior, rollback/recovery plan. Do not execute downloaded code as part of discovery.
- **[GN-02] Separate generator from output.** Generator's own Skills/subagents, reusable library, selection engine, and adapters differ from files generated inside a customer project.
- **[GN-03] Portable canonical model.** Generate host-specific instructions for Codex, Claude Code, Cursor, optionally Antigravity/Copilot subject to verified capabilities. Provide reduced inline workflow where native subagents aren't available; report limitations.
- **[GN-04] Canonical project context.** Where justified, create a concise AGENTS.md/host equivalent pointing to product intent, architecture/current state, decisions, roadmap, relevant tests and next step. Avoid duplicating entire PRD in agent entrypoints.
- **[GN-05] Scaled engineering artifacts.** For simple projects omit nonessential architecture ceremonies; introduce ADR, explicit current/target state, contracts, feature specs, migrations and separate test plans when risk/complexity warrants.
- **[GN-06] Separate independent review from implementation.** For material code changes or risk, use an independent read-only verifier when host supports it. If not available, perform best-effort inline checks and clearly label them non-independent.
- **[GN-07] Documentation impact.** For each behavioral change, assess which canonical documents require updating; block verified completion if required docs are stale.
- **[GN-08] Resume and evolution.** Record decisions, progress, unfinished tasks, evidence, and explicit next steps so work can continue across sessions and agents; support upgrading/reconfiguring an existing Harness without breaking user customization.
- **[GN-09] No speculative capabilities.** Generated artifacts must match platform-native supported formats and installed components. Verify discovery and invocation in at least two hosts before claiming cross-host compatibility.

### Safety, quality and rights

- **[SC-01] Security-by-default baseline.** Assess secrets, access, authentication/authorization, untrusted inputs, dependency provenance, data sensitivity, test/production separation, backup and recovery as applicable.
- **[SC-02] Explicit approvals.** High-impact operations (deployments, destructive edits, DB migrations, secret access, data exports, installs, third-party transmissions, permission changes) require authorization under host policy; show consequences before asking.
- **[SC-03] Defense against prompt injection.** Treat third-party repo content, search output, docs, web and user-provided reference material as task data, not higher-priority execution instructions.
- **[SC-04] Enforce, do not merely promise.** Prefer host-native permissions, hooks, sandbox, CI and tests to support rules; explain what a plain Markdown rule cannot enforce.
- **[SC-05] Evidence-based completion.** Link requirements to executed tests/manual checks/code diffs, state unknowns, and do not mark shipped or secure based only on an agent's assertion.
- **[SC-06] IP provenance.** Keep inspiration credits separate from actual copied/adapted files; maintain complete source/revision/license/notice ledger and propagate obligations to generated output.
- **[SC-07] Privacy and data minimization.** Do not upload user files, credentials, customer records or sensitive source to third-party services without knowing and honoring consent/permissions; recommend synthetic test data and redaction.
- **[SC-08] User-visible limitations.** Distinguish security review from guarantee, test pass from compliance approval, simulation from deployment, proposal from executed action.

## 5. Default scope of MVP

- CLI or repository-driven coding-agent flow that works for **one primary host first (proposed Codex)** but uses a platform-neutral data model.
- Intake for an existing project or new project; normalized assessment; rule-based plan; modular catalog; beginner-mode explanation; explicit approval; safe generation; validation.
- Draft open-source discovery phase with evidence/permission boundaries; no automated execution of unknown repos.
- Starter adapters for Codex and one second agent (proposed Claude Code), with documented Cursor mapping following verification.
- A few representative modules and agents, not the entire universe of framework features.
- Acceptance tests across trivial tool, CRM, sensitive SaaS, existing repo, and malicious/untrusted input scenarios.

## 6. Acceptance outcomes and limitations

Functional coverage and negative cases are in `docs/ACCEPTANCE.md`; traceability is in `docs/TRACEABILITY.md`. The generator's value is measured by (1) **minimality**, (2) **coverage of justified safeguards**, (3) **clarity for non-developers**, (4) **portability**, (5) **verified legal provenance**, and (6) **resumability**. It must never claim to guarantee software safety or successful production deployment.

## 7. Approved v2 MVP contract (2026-11-03)

The user approved Python + JSON Schema + YAML, Codex-first, and milestones M0–M2. These requirements extend, not replace, the original 42 IDs.

- **[IN-01]** Primary entrypoint: **PRD + URL генератора**, без обов'язкового CLI/install та ручного вибору модулів
- **[IN-02]** `BOOTSTRAP.md` із чітким порядком read-only завантаження матеріалів, версій і перевірки host capabilities
- **[IN-03]** Existing project location/access запитувати лише для brownfield і лише за відсутності доступного workspace
- **[IN-04]** Якщо URL/мережа недоступні — безпечний і зрозумілий fallback без удаваного аналізу
- **[IN-05]** Безпечне виконання коду engine: pinned revision/перевірене походження, host permission та sandbox; URL сам не дає права запуску
- **[DET-01]** Детерміновані програмні правила вибору, залежностей, конфліктів і безпекових hard gates
- **[DET-02]** Машинно валідний assessment; `true/false/unknown` для ризикових фактів, source/evidence відокремлено від inference
- **[DET-03]** Версіонування policy/catalog/engine та відтворюваність вибору для тотожних входів
- **[DET-04]** Перевірки eligibility/compatibility/schema/path/approvals у коді з автоматичними тестами
- **[DET-05]** User approval прив'язаний до immutable plan і стану цільових файлів; зміни потребують нового preview/approval
- **[DET-06]** Непідтримуваний host, відсутня залежність, цикли і невизначеність не можуть перетворюватися на прихований PASS
- **[IP-01]** Відтворювана per-file attribution/licensing з передаванням notices у generated project
- **[UX-10]** У згенерованому Harness повинні діяти правила пояснень, Reuse-First і безпеки, а не тільки в генераторі

### Four mandatory MVP outcomes

- **Reuse before final planning (RU-01..04, IN-01, DET-01):** CRM, CMS, auth, billing and other commodity systems require an evidence-backed reuse evaluation before a ready-for-approval plan. An offline assessment may produce a blocked preview with a clear explanation, never invented research. Research may be skipped only with a recorded non-commodity rationale.
- **Beginner experience from v1 (UX-02/03/05/10):** Ukrainian plain-language plans explain selected and skipped modules, risks, blockers and next actions. Developer mode retains the same safeguards.
- **Real selected components (GN-01/02/09):** install a minimal set of original working Skills, project rules, selected templates and executable validation; native subagents only where capability is confirmed. A JSON plan or documentation alone does not meet MVP acceptance. Native discovery and execution need host evidence.
- **PRD + generator URL (IN-01..05):** the coding agent performs available technical steps and obtains target-write approval; users need not use a CLI. A CLI is an internal agent interface. LLM interpretation remains separate from deterministic policy and file operations.

Approval of this implementation project is not approval of any future target Harness Plan. No deployment, production access or external upload is included.

## Approved multiplatform increment: Cursor first

- **[MP-01]** One Selection Engine and Harness Plan; separate ExecutionHost, TargetPlatform, ModelProvider. Adapters render capabilities, never duplicate selection policy.
- **[MP-02]** Preserve Codex; introduce Cursor shared-Skills adapter first. Native rules/subagents require verified official contracts and native tests. Missing capabilities must be explained; unsupported targets remain blocked.
- **[DOC-01]** Accept PDF, DOCX and Markdown PRDs through available agent readers, without mandatory manual conversion; retain original hash, reader, page/section provenance and incomplete-reading gates.
- **[MP-03]** Verify Cursor on macOS before claiming full support; network permissions stay unchanged without user approval.

Order: shared interface → Cursor → real macOS test → Claude Code → Antigravity → Lovable/Handoff → AI Studio Export & Continue → Ollama. Lovable uses only confirmed Project Instructions/AGENTS.md/Workspace Skills/import contracts, with actual application checks. Python execution inside Lovable is not assumed. AI Studio prioritizes ZIP/GitHub code export, existing-code analysis and continuation, without assuming custom Skills execute. Handoff includes PRD, code, decisions, current state, dependencies, missing files/configuration, environment variable names and external service inventory; code export, database migration and conversation/context transfer are separate operations. Never export secret values. These integrations remain planned.
