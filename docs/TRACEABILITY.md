# Requirements traceability matrix

**Purpose:** make omissions visible. Canonical requirement definitions are in [PRD.md](PRD.md), and test definitions in [ACCEPTANCE.md](ACCEPTANCE.md). Rows below are a **design mapping, not an assertion of implementation**.

Status for all rows: `specified / not implemented` until Codex changes status based on actual test evidence. `Implementer evidence` field will be added per milestone when code exists.

| Requirement | Condensed statement | Design source | Acceptance tests | Origin / note |
|---|---|---|---|---|
| `UX-01` | Progressive intake. A short free-form or voice-derived idea is enough to start | BEGINNER_EXPERIENCE.md | AT-09 | Урок: PRD як source of truth; спершу короткий опис |
| `UX-02` | Progressive disclosure. Show what/why/impact/decision first; provide technical detail on r… | BEGINNER_EXPERIENCE.md | AT-29, AT-36 | Обговорені вимоги + інженерне уточнення |
| `UX-03` | Experience modes. Beginner (default for target product) and Developer | BEGINNER_EXPERIENCE.md | AT-30 | Обговорені вимоги + інженерне уточнення |
| `UX-04` | Fewer questions. Infer from supplied context when safe, explicitly mark uncertainty; ask f… | BEGINNER_EXPERIENCE.md | AT-09 | Обговорені вимоги + інженерне уточнення |
| `UX-05` | User-language and handoff. Explain unfamiliar terms the first time they affect a decision … | BEGINNER_EXPERIENCE.md | AT-28, AT-29 | Обговорені вимоги + інженерне уточнення |
| `UX-06` | Purpose-sensitive discovery. Do not force marketing/target-audience research for a tool bu… | BEGINNER_EXPERIENCE.md | AT-10, AT-11 | Урок: JTBD/аналіз ЦА лише для зовнішнього ринку |
| `UX-07` | Learning without a gate. Offer optional teaching notes and ready-to-use examples; users ne… | BEGINNER_EXPERIENCE.md | AT-36 | Урок: не блокувати початок перфекціонізмом |
| `UX-08` | Small safe experiments. When feasibility is uncertain, propose a bounded proof of concept … | BEGINNER_EXPERIENCE.md | AT-01, AT-09 | Урок: маленькі експерименти та перевірка ідеї |
| `UX-09` | Costs and portability. Disclose recurring API/hosting fees and vendor lock-in risks; keep … | BEGINNER_EXPERIENCE.md | AT-28, AT-32 | Обговорені вимоги + інженерне уточнення |
| `AS-01` | Assess new and existing projects. Detect greenfield/brownfield status; read only relevant … | ARCHITECTURE.md, SELECTION_POLICY.md | AT-04, AT-34 | Обговорені вимоги + інженерне уточнення |
| `AS-02` | Classify complexity across two dimensions. Project-level scale/risk and feature-level size… | ARCHITECTURE.md, SELECTION_POLICY.md | AT-01, AT-03 | Обговорені вимоги + інженерне уточнення |
| `AS-03` | Identify risk signals. Customer/personal data, payments, authentication, children, financi… | ARCHITECTURE.md, SELECTION_POLICY.md | AT-02, AT-03 | Обговорені вимоги + інженерне уточнення |
| `AS-04` | Inspect execution capabilities. Determine coding agent, supported Skills/subagents, file p… | ARCHITECTURE.md, SELECTION_POLICY.md | AT-18, AT-19, AT-31 | Обговорені вимоги + інженерне уточнення |
| `AS-05` | Maintain bounded context. Discover file metadata first; read only relevant sources; keep o… | ARCHITECTURE.md, SELECTION_POLICY.md | AT-04, AT-28 | Обговорені вимоги + інженерне уточнення |
| `RU-01` | Evaluate build/adapt/buy. Before committing to building a substantial commodity subsystem,… | REUSE_FIRST.md | AT-02, AT-10 | Урок: знайти open-source CRM/обробник перш ніж будувати |
| `RU-02` | Validate every concrete candidate. Confirm repository URL, license, copyright/NOTICE, main… | REUSE_FIRST.md | AT-02, AT-22 | Дискусія: юридично та технічно перевіряти репозиторії |
| `RU-03` | No invented evidence. Without live/reliable access, state research is unavailable or unver… | REUSE_FIRST.md | AT-21 | Обговорені вимоги + інженерне уточнення |
| `RU-04` | Compare trade-offs. Produce an explicit option analysis with reasoned recommendation and w… | REUSE_FIRST.md | AT-02 | Обговорені вимоги + інженерне уточнення |
| `SE-01` | Explainable selection engine. Select a minimum sufficient set of instructions, docs, specs… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-01, AT-02, AT-03 | Обговорені вимоги + інженерне уточнення |
| `SE-02` | Conditional routes. Offer quick/standard/full or equivalent, with explicit skip rules for … | SELECTION_POLICY.md, ARCHITECTURE.md | AT-05, AT-06, AT-07, AT-08 | Обговорені вимоги + інженерне уточнення |
| `SE-03` | Avoid incompatible duplication. Do not install multiple complete competing SDD workflows i… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-04 | Обговорені вимоги + інженерне уточнення |
| `SE-04` | Resolve dependencies and conflicts. Machine-readable module metadata; stable IDs, compatib… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-12, AT-31 | Обговорені вимоги + інженерне уточнення |
| `SE-05` | Human review of a Harness Plan. Before file writes or installation, show selected and skip… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-15 | Обговорені вимоги + інженерне уточнення |
| `SE-06` | Intentional overrides. Allow users to change route/module decisions, log rationale, warn w… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-13, AT-14 | Обговорені вимоги + інженерне уточнення |
| `SE-07` | Deterministic planning core. With the same normalized inputs, policy version, catalog vers… | SELECTION_POLICY.md, ARCHITECTURE.md | AT-12 | Обговорені вимоги + інженерне уточнення |
| `GN-01` | Generate approved components only. Compare intended changes, preserve existing files, idem… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-15, AT-16, AT-17, AT-34 | Обговорені вимоги + інженерне уточнення |
| `GN-02` | Separate generator from output. Generator's own Skills/subagents, reusable library, select… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-01, AT-31 | Обговорені вимоги + інженерне уточнення |
| `GN-03` | Portable canonical model. Generate host-specific instructions for Codex, Claude Code, Curs… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-18, AT-19, AT-31 | Дискусія: Codex/Claude/Cursor/Antigravity portable |
| `GN-04` | Canonical project context. Where justified, create a concise AGENTS.md/host equivalent poi… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-04, AT-28 | Обговорені вимоги + інженерне уточнення |
| `GN-05` | Scaled engineering artifacts. For simple projects omit nonessential architecture ceremonie… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-01, AT-05, AT-06, AT-07 | Обговорені вимоги + інженерне уточнення |
| `GN-06` | Separate independent review from implementation. For material code changes or risk, use an… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-18, AT-19, AT-27 | Дискусія: genkovich/cc-sdd, independent verifier |
| `GN-07` | Documentation impact. For each behavioral change, assess which canonical documents require… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-26 | AgentSG-референс: documentation impact gate |
| `GN-08` | Resume and evolution. Record decisions, progress, unfinished tasks, evidence, and explicit… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-28, AT-33 | Урок: легко змінювати агента при обмеженнях |
| `GN-09` | No speculative capabilities. Generated artifacts must match platform-native supported form… | ARCHITECTURE.md, SKILLS_AGENTS.md, STATE_HANDOFF.md | AT-19, AT-31 | Обговорені вимоги + інженерне уточнення |
| `SC-01` | Security-by-default baseline. Assess secrets, access, authentication/authorization, untrus… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-02, AT-03, AT-25 | Обговорені вимоги + інженерне уточнення |
| `SC-02` | Explicit approvals. High-impact operations (deployments, destructive edits, DB migrations,… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-14, AT-15, AT-32 | Обговорені вимоги + інженерне уточнення |
| `SC-03` | Defense against prompt injection. Treat third-party repo content, search output, docs, web… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-20 | Доданий технічний захист від чужих інструкцій |
| `SC-04` | Enforce, do not merely promise. Prefer host-native permissions, hooks, sandbox, CI and tes… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-19, AT-20 | Обговорені вимоги + інженерне уточнення |
| `SC-05` | Evidence-based completion. Link requirements to executed tests/manual checks/code diffs, s… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-26, AT-27 | Обговорені вимоги + інженерне уточнення |
| `SC-06` | IP provenance. Keep inspiration credits separate from actual copied/adapted files; maintai… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-22, AT-23, AT-24 | Дискусія: переробка Skills, збереження MIT notices |
| `SC-07` | Privacy and data minimization. Do not upload user files, credentials, customer records or … | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-25 | Обговорені вимоги + інженерне уточнення |
| `SC-08` | User-visible limitations. Distinguish security review from guarantee, test pass from compl… | SECURITY.md, ../THIRD_PARTY_NOTICES.md | AT-27, AT-35 | Обговорені вимоги + інженерне уточнення |

## Definition of traceability completeness

1. Every unique `[PREFIX-NN]` in `PRD.md` has exactly one matrix row.
2. Every row points to at least one actual test ID in `ACCEPTANCE.md`.
3. Before marking implementation complete, add executable test evidence, changed file paths and any intentionally rejected/unmet part.
4. `tools/validate_package.py` checks structural requirements in this starter; it does **not** measure implementation coverage.

## Change management

New user idea or clarified constraint → amend PRD first → extend row and corresponding acceptance test → revise architecture/selection policy if needed → implement bounded work → verify and update Current State. Never infer that a requirement is implemented merely because the PRD describes it.
