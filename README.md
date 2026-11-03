# Adaptive Developer Harness Generator

Give your coding agent **your PRD + this repository URL**. It helps choose, explain and install the smallest useful set of development Skills, rules, templates and checks for your project.

**Start:** [BOOTSTRAP.md](BOOTSTRAP.md). Українською: [START_HERE_UA.md](START_HERE_UA.md).

## Current capability

This repository contains an executable Python MVP: strict JSON contracts, a versioned YAML catalog, deterministic selection, mandatory pre-plan reuse checks for commodity systems, Ukrainian plan explanations, exact file previews, explicit hash-bound approval, bounded Apply with recovery, and generated integrity checks.

The target receives only selected original components: Codex Skills (`adh-implement`, `adh-verify`, and conditional reuse/security/migration/release Skills), a managed AGENTS.md block, templates, provenance/license data, an executable validator, and a read-only reviewer definition only when subagent capability is confirmed.

Codex CLI 0.163.0 discovery of generated `adh-implement` and `adh-verify` has been observed through `skills/list`. Application tests, model comprehension, independent reviews and every host's subagent behavior are separate checks, not automatic consequences of installation. Claude Code/Cursor adapters and third-party Skill import are not implemented.

## How it works

1. The agent reads your PRD, inspects the workspace and records facts/unknowns.
2. For CRM, CMS and similar systems it researches ready-made alternatives before a final plan.
3. Code selects modules, resolves dependencies and enforces risk/capability gates.
4. You review understandable reasons and exact changes, then approve the specific plan.
5. Code applies only approved operations and checks the output. The agent reports actual evidence and next steps.

LLM interpretation and research are agent responsibilities; this is not an automatic PRD parser. Missing evidence produces blockers or `not-verified`, never invented success. Approval receipts check integrity; host permissions establish authority. This is an MVP, not a security certification or production release guarantee.

## Development

Use a reviewed checkout, Python 3.11+ and the dependencies in `requirements.lock`. This version runs from the repository; standalone wheel distribution is not supported.

```sh
python3 -m unittest discover -s tests -v
python3 tools/validate_package.py
python3 -m adaptive_harness --help
```

Runtime implementation: [architecture](docs/ARCHITECTURE.md). Requirements and evidence: [PRD](docs/PRD.md), [traceability](docs/TRACEABILITY.md), [acceptance](docs/ACCEPTANCE.md), [verification](docs/VERIFICATION.md). Contributor rules: [AGENTS.md](AGENTS.md).

## Attribution

[Reference audit](docs/REFERENCE_AUDIT.md), [inspirations](INSPIRATIONS.md), [third-party notices](THIRD_PARTY_NOTICES.md). Target components in this MVP are original MIT-licensed files; no external framework is installed wholesale.
