# Adaptive Developer Harness Generator

> Project status: **design starter / specification**, not a production-ready generator.

An adaptive, beginner-friendly toolkit that helps a coding agent examine a PRD and an existing project, propose a **minimum sufficient Developer Harness**, and generate it **only after user approval**.

## Why we built this

Coding agents make software development accessible, but setting up reliable project instructions, specifications, tests, security controls, documentation, and independent checks remains difficult for people without an engineering background. Existing frameworks provide strong building blocks; selecting and configuring them can itself require expertise.

This project is intended to make that work easier for beginners and non-technical builders, while remaining useful to experienced teams. A simple calculator should not inherit the same process as a multi-tenant SaaS with customer data.

**Principle: begin with what the project needs; add complexity only when justified by evidence and risk.**

## What it is

A **meta-generator of development workflows**, not a generic app template, a new foundation model, a replacement for coding agents, or a production security scanner.

1. **Assess:** understand product intent, current code, technical environment, user experience level, risks, and existing controls.
2. **Discover reuse:** evaluate credible off-the-shelf services, OSS products, libraries, and reusable architectures before reinventing them.
3. **Select:** propose Skills, subagents, agent instructions, specifications, tests, docs, and enforceable controls with reasons and exclusions.
4. **Approve:** show a plain-language Harness Plan, intended file changes, risks, and approximate effort. Get explicit approval.
5. **Generate:** write only selected components, using an adapter for the target coding environment and preserving existing work.
6. **Validate and maintain:** check consistency, safety policy coverage, evidence, provenance, and documentation impact. Support changes to the harness over time.

## Foundational principles

- **Minimum sufficient configuration:** no universal large template; conditional modules and explicit skips.
- **Beginner-first communication:** explain implications, not every code line; offer both beginner and developer modes.
- **Security by default:** meaningful risk analysis and enforced gates where supported; prompt text alone is not a security boundary.
- **Reuse before custom build:** verify licenses, maintenance, integration cost, security, and fit before recommending OSS.
- **Human approval:** no unapproved high-impact writes, dependency installs, production deployments, or destructive actions.
- **Traceability and honest status:** distinguish current from target; claims of success require evidence.
- **Portable by design:** canonical modules, agent-specific adapters, capability checks, and clear fallbacks.
- **IP compliance:** recognize inspirations separately from copied/adapted assets; retain licenses and attribution.

## Start here

- Ukrainian beginner guide: [START_HERE_UA.md](START_HERE_UA.md)
- Full requirements: [docs/PRD.md](docs/PRD.md)
- Architecture and status: [docs/ARCHITECTURE.md](docs/ARCHITECTURE.md)
- What must not be forgotten: [docs/TRACEABILITY.md](docs/TRACEABILITY.md)
- Ready-to-paste first task for Codex: [CODEX_BOOTSTRAP_PROMPT.md](CODEX_BOOTSTRAP_PROMPT.md)
- Project sources: [INSPIRATIONS.md](INSPIRATIONS.md)
- Third-party notices: [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md)

## Current state

This archive includes a **draft specification, policies, a machine-readable schema, a draft module catalog, an example Harness Plan, draft canonical Skill/subagent role files, and a validation script**. It does **not** yet include an implemented Selection Engine, working CLI, generated adapters, platform-installed or tested Skills, or production-grade policy enforcement. They are planned in the roadmap.

## Attribution

Inspired by open-source agentic development work. See [INSPIRATIONS.md](INSPIRATIONS.md). This starter package does not intentionally contain source code or `SKILL.md` text copied from those repositories. If such material is later incorporated, record licenses and notices in [THIRD_PARTY_NOTICES.md](THIRD_PARTY_NOTICES.md).
