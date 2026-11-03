# State, documentation and cross-session handoff

## Canonical documents in a generated project (when selected)

- Product intent: PRD, lean brief or equivalent; no demand for a lengthy PRD for a tiny utility.
- Current vs Target: what runs/tests today vs what is planned; a planned feature cannot be labeled built.
- Decisions: ADR or brief decision log for material trade-offs and rejected options.
- Feature acceptance: small spec with observable behavior and test plan; minimal tests may be inline.
- Roadmap/task state: one explicit next bounded task with dependency information.
- Agent entrypoint: short navigation to relevant canonical files and commands; no duplicated whole PRD.
- Licensing/provenance: source references and notices where adapted assets are used.

## Documentation-impact check

For changed behavior, examine the PRD/brief, current-target architecture, feature spec, decision log, test contracts, security rules, relevant documentation, and license notices. Mark each `stale`, `updated` or `N/A` with evidence. `stale` prevents a verified-complete claim until resolved.

## Minimal portable handoff

```text
PROJECT: ...
USER GOAL: ...
CURRENT: ... (observed and tested)
TARGET/NEXT: ... (planned)
DECISIONS MADE: ... (with references)
FILES CHANGED: ...
TESTS ACTUALLY RUN: ... (result and date)
RISK / PERMISSION BLOCKERS: ...
LICENSE / EXTERNAL CODE: ...
NEXT ACTION: ...
HOST LIMITATIONS: ...
```

Agent portability is a design target, not a claim that every host can interpret every tool-specific instruction. Keep the project truth in text/structured data and generate host-specific wrappers as needed.
