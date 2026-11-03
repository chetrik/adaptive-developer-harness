# Decision register

Legend: **Aligned** = user-stated direction in discussion; **Proposal** = proposed implementation subject to review; **Open** = decision not made.

| ID | Status | Decision / issue | Reason / next evidence |
|---|---|---|---|
| D-001 | Aligned | Target novices and non-developers without excluding professionals | Product problem and intended audience |
| D-002 | Aligned | Adapt Harness to project, not copy all framework files | Avoid unnecessary ceremony and conflict |
| D-003 | Aligned | Borrow/adapt existing OSS Skills/subagents where license permits | Avoid duplication; retain legal notices |
| D-004 | Aligned | Publish inspirations and derivative-work notices separately | Attribution vs legal compliance |
| D-005 | Aligned | Explain decisions, prioritize safety, research ready OSS alternatives | Beginner trust and developer efficiency |
| D-006 | Proposal | Canonical policy/catalog separate from per-host adapters | Portability and consistency |
| D-007 | Accepted | Deterministic selection core with LLM-assisted assessment/explanation | Repeatability and auditable decisions |
| D-008 | Proposal | Two modes: Beginner (default) and Developer | Adjustable verbosity without relaxing safety |
| D-009 | Accepted | Use Codex for first implementation; support Claude Code and Cursor by adapter | Practical staged delivery |
| D-010 | Accepted | Start repository-driven; only build custom CLI after validation | Minimize premature infrastructure |
| D-011 | Proposal | Explicit Plan approval before generation/apply | Prevent unintended writes |
| D-012 | Proposal | MIT for original project-owned code, subject to owner selection and license review | Permissive OSS; check borrowed asset restrictions |
| D-013 | Accepted | Use JSON Schema for exchange contract; YAML for catalog | Interoperability and readable policy |
| D-014 | Open | Legal copyright holder(s), organization, repository visibility and exact name | Needed before publishing LICENSE and branding |
| D-015 | Open | Which external skills/agents will be actually copied, adapted or only studied | Must precede legally accurate THIRD_PARTY_NOTICES |
| D-016 | Open | Official initial host capabilities, supported integration versions and fallback restrictions | Verify on real hosts before implementation claims |
| D-017 | Open | Whether browser UI/website or hosted automation is justified later | Out of MVP until validated |
| D-018 | Open | Whether to install/use external SDD frameworks directly or implement compatible minimal procedures | Compare duplication, runtime and licensing |

Do not mark proposals as user-approved architectural commitments. Record future ADRs for material decisions and the evidence that justified them.

## Accepted implementation decisions — 2026-11-03

These supersede the proposal status of D-007, D-009, D-010 and D-013 for MVP.

- D-019 Accepted: Python 3.11+, JSON Schema 2020-12, YAML catalog, a repository-driven agent flow with a small internal CLI; no server or LLM API dependency.
- D-020 Accepted: M0–M2 include reuse research gates BEFORE final planning, beginner explanations, actual selected Skills/rules/templates/executable checks, and PRD + URL bootstrap. These are not deferred enhancements.
- D-021 Accepted: immutable plan content and target-state fingerprints bind explicit approval; a receipt is integrity evidence, not cryptographic proof of human identity. Host permissions remain the authority boundary.
- D-022 Accepted: Codex-first; native Skills/subagents require observed capabilities. Unsupported capabilities have explicit blockers/fallbacks.
- D-023 Accepted: original minimal target components first; external imports require per-file provenance and propagated notices.
- D-024 Observed: LICENSE is MIT, copyright 2026 chetrik; D-012 no longer describes absence of a chosen repository license. Legal identity remains outside code verification.

## D-025 — Approved shared architecture and Cursor priority

One selector/plan, separate executor, target and model provider. Implement Cursor before Claude and Antigravity. Keep legacy host assessments; explicit executor/target must appear together and take precedence. Cursor 0.1 adapter is experimental shared-Skills only: user-reported format support, no invented native rules/agent contracts under HTTP 403. Native macOS validation remains a separate gate. Network permissions unchanged.

## D-026 — Original-document provenance

Agent readers handle PDF/DOCX/Markdown; bootstrap preserves original hash and records unread status. Complete reading metadata with source locators is required for PDF/DOCX final planning. No bundled PDF/DOCX parser, automatic OCR service upload or claim of comprehension. Engine 0.2.0 invalidates prior approvals and adds adapter identity to plans.
