# Coverage of the design conversation and teaching notes

This is a conceptual checklist of decisions, product goals and teaching principles. It is intentionally **not** a transcript. Teaching examples and conversational descriptions are not automatically product requirements; the corresponding requirement IDs are the source of truth.

| Discussed subject | Where addressed | Status |
|---|---|---|
| Audience: novices, non-technical builders, experienced devs also welcome | PRD §1–3; UX-01 through UX-09; README | Specified |
| Explain to beginners why Harness is needed, not require prior expertise | README “Why”; START_HERE_UA; BEGINNER_EXPERIENCE | Specified |
| Project-specific adaptation instead of copying all Skills/docs | SE-01 through SE-04; selection matrix | Specified |
| Distinguish generator and target project's Harness | GN-02; ARCHITECTURE | Specified |
| GitHub URL + PRD + existing code as intake | AS-01/04; START_HERE_UA; GN-09 | Specified; host permissions unknown |
| Greenfield / brownfield handling and non-destructive edits | AS-01; GN-01; AT-04/16/34 | Specified |
| Complexity XS–XL and quick/standard/full routing | AS-02; SE-02; SELECTION_POLICY | Specified, thresholds not final |
| UI vs backend vs mobile vs CLI surfaces, optional docs | AS-02; GN-05; AT-05–08 | Specified |
| Do not duplicate Spec Kit + OpenSpec + cc-sdd in one client project | SE-03, SE-04, AT-04 | Specified |
| Inherit/transform third-party Skills and subagents where licensed | SC-06; SKILLS_AGENTS; THIRD_PARTY_NOTICES | Specified; no external file copied yet |
| Credits to inspirations | INSPIRATIONS.md, README | Written |
| Copyright licenses and notices when distributing generated files | THIRD_PARTY_NOTICES; SC-06; AT-23/24 | Policy specified, actual imports pending |
| Learn practices from Spec Kit, OpenSpec, genkovich, cc-sdd | INSPIRATIONS; CODEX_BOOTSTRAP_PROMPT | Written, further deep audit pending |
| Learn repo instructions, Hooks, ADR, verifier, docs gates from web-app-core/AgentSG | INSPIRATIONS; GN-04/06/07; ARCHITECTURE | Documented; AgentSG license unknown |
| Beginner-first plain-language decisions, not line-by-line lectures | UX-02/03/05; BEGINNER_EXPERIENCE | Specified |
| Start with rough idea, help write PRD, avoid blocking by perfectionism | UX-01/04/07/08; AT-09 | Specified |
| Vision vs MVP separation | UX-01; PRD | Specified |
| Search competitors / similar functional solutions as inspiration | RU-01; REUSE_FIRST | Specified |
| Suggest ready-made OSS CRM before building from scratch | RU-01–04; REUSE_FIRST; AT-02 | Specified |
| Compare open source / existing SaaS / modular solution / custom build | RU-04; REUSE_FIRST | Specified |
| Check license, maintenance, vulnerabilities, support and expenses | RU-02; SC-06; REUSE_FIRST | Specified |
| Without network, no fabricated GitHub findings | RU-03; AT-21 | Specified |
| Use JTBD and target-audience analysis only when product is for customers | UX-06; AT-10/11 | Specified |
| Ingest user examples (budgets/files/reports) instead of guessing schema | UX-04; AS-01; BEGINNER_EXPERIENCE | Specified |
| More safety: privacy, credentials, dependency supply chain, approval gates | AS-03; SC-01–08; SECURITY | Specified |
| Prompt instructions cannot technically guarantee safety | SC-04; SECURITY | Specified |
| No silent installs or destructive/production operations | SC-02; GN-01; AT-15/32 | Specified |
| Current vs target state, no pretending plan is implemented | GN-04/07; SC-08; ARCHITECTURE; AT-35 | Specified |
| Documentation impact verification and independent reviewer where justified | GN-06/07; AT-26/27 | Specified |
| Durable handoff, optional future agent switching and cost awareness | UX-09; AS-05; GN-08; STATE_HANDOFF | Specified |
| Approval of Harness Plan before applying anything | SE-05/06; GN-01 | Specified |
| Reusable library + host-specific adapters and fallbacks | AS-04; GN-02/03/09; SKILLS_AGENTS | Specified |
| Ship light MVP first, no speculative web UI or custom SDK | ROADMAP; DECISIONS | Proposed, not yet approved |
| Test at least calculator, CRM, payment SaaS and existing app | ACCEPTANCE; ROADMAP | Tests described, not yet run |
| Cross-host functional checks in Codex/Claude/Cursor | GN-03/09; AT-18/19/31 | Specified; actual compatibility pending |
| Avoid non-evidenced “any app in two hours” or legal guarantees | UX-08; SC-08; BEGINNER_EXPERIENCE | Specified |

**Known boundary:** the supplied long-form lesson included student discussions and general educational examples. We extract reusable design principles without importing the full private transcript, student examples or personally identifying details into this public-oriented repo starter.

## Approved MVP clarification (2026-11-03)

All four are mandatory in M0–M2: pre-plan reuse research for commodity systems; beginner explanations; real selected components; PRD + URL agent-driven entry. See PRD §7 and D-019..024. Status: bounded runtime implemented; exact tests and remaining agent/host limits are in TRACEABILITY.md and VERIFICATION.md. The historical table above records design coverage, not current runtime completion.
