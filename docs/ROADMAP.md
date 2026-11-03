# Roadmap — bounded implementation milestones

All milestones are **planned**. No implementation of the Selection Engine or agent adapters has been completed in this starter archive.

## M0 — Specification baseline (starter delivered)

- [x] Consolidate product requirements and beginner UX principles from conversation and supplied teaching notes.
- [x] Record security/IP/reuse policies and inspirations.
- [x] Define acceptance scenarios, traceability and draft plan/schema.
- [x] Create a starter docs/schema validation script.
- [ ] **User review** of decisions and intended product scope.

### M1 — Research & architecture decision

- [ ] Audit competitor/framework repositories at pinned commits; classify compatible techniques and licensing constraints.
- [ ] Compare repository-driven vs custom CLI/SDK plan and select implementation boundaries.
- [ ] Agree core modules, approval mechanism, exact host fallback contracts and generated file structure.
- [ ] Resolve relevant items in `DECISIONS.md` and capture ADRs as appropriate.
- [ ] Ensure requirement traceability with no unexplained omissions.

**Exit:** written architecture review, approved MVP and research/provenance ledger.

### M2 — Assessment + Selection Engine

- [ ] Implement normalized project assessment and host capability detection.
- [ ] Define validated module catalog, trigger/dependency/conflict rules, risk overrides.
- [ ] Produce deterministic Harness Plan JSON and human-readable version.
- [ ] Test plans for calculator/CRM/sensitive SaaS/existing app.

**Exit:** AT-01 through AT-14 and policy consistency checks as applicable.

### M3 — Approved generation, validation and first adapter

- [ ] Generate only approved files with diff preview, no silent overwrite, idempotency.
- [ ] First official target adapter (Codex, subject to verified host capabilities).
- [ ] Structural validator, doc impact, risk, provenance and evidence reports.
- [ ] Canonical Skills + agents are selected from library rather than blanket installed.

**Exit:** AT-15 through AT-17, AT-25, AT-27, AT-34, AT-35, plus host tests.

### M4 — Reuse-first + beginner experience

- [ ] OSS/service research workflow with true citations, license/security/maintenance evidence and offline fallback.
- [ ] Beginner/Developer explanation modes and minimal clarification discipline.
- [ ] Safe proof-of-concept guidance, scope-sliced PRD support, cost disclosures.

**Exit:** AT-02, AT-09 through AT-11, AT-20 through AT-22, AT-29, AT-30.

### M5 — Cross-host + updates + provenance

- [ ] Second adapter, then Cursor/other beta/optional adapter after compatibility tests.
- [ ] Independent reviewer where supported, honest inline fallback otherwise.
- [ ] Harness update, migrations, recovery/handoff, docs drift checks.
- [ ] Third-party import pipeline and generated-license propagation.

**Exit:** AT-18, AT-19, AT-23, AT-24, AT-26, AT-28, AT-31, AT-33.

### M6 — Public release gates

- [ ] Complete all required acceptance checks, security audit and licensing review.
- [ ] Finalize ownership and public license; verify external assets and notices.
- [ ] Publish README, quickstart, examples and limitations; demonstrate 3–4 real host/project scenarios.
- [ ] No false claims of production readiness, compatibility or certification.

## Change discipline

Each feature is scoped with acceptance criteria, implemented, tested, reviewed according to risk, followed by a documentation-impact check. Update Current State and traceability only when evidence justifies it. Carry a concise handoff with next work; choose a single next milestone rather than attempting the entire roadmap in one agent run.
