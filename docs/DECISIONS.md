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
| D-007 | Proposal | Deterministic selection core with LLM-assisted assessment/explanation | Repeatability and auditable decisions |
| D-008 | Proposal | Two modes: Beginner (default) and Developer | Adjustable verbosity without relaxing safety |
| D-009 | Proposal | Use Codex for first implementation; support Claude Code and Cursor by adapter | Practical staged delivery |
| D-010 | Proposal | Start repository-driven; only build custom CLI after validation | Minimize premature infrastructure |
| D-011 | Proposal | Explicit Plan approval before generation/apply | Prevent unintended writes |
| D-012 | Proposal | MIT for original project-owned code, subject to owner selection and license review | Permissive OSS; check borrowed asset restrictions |
| D-013 | Proposal | Use JSON Schema for exchange contract; YAML for catalog | Interoperability and readable policy |
| D-014 | Open | Legal copyright holder(s), organization, repository visibility and exact name | Needed before publishing LICENSE and branding |
| D-015 | Open | Which external skills/agents will be actually copied, adapted or only studied | Must precede legally accurate THIRD_PARTY_NOTICES |
| D-016 | Open | Official initial host capabilities, supported integration versions and fallback restrictions | Verify on real hosts before implementation claims |
| D-017 | Open | Whether browser UI/website or hosted automation is justified later | Out of MVP until validated |
| D-018 | Open | Whether to install/use external SDD frameworks directly or implement compatible minimal procedures | Compare duplication, runtime and licensing |

Do not mark proposals as user-approved architectural commitments. Record future ADRs for material decisions and the evidence that justified them.
