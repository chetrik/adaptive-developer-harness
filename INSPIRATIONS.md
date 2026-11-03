# Inspirations and acknowledgements

We study the following open-source projects and credit their ideas and engineering practices. **Mention here does not mean their code or documentation has been copied into this starter.** Prior to reuse, verify the particular file, revision, license and any asset-specific notices.

| Repository | Practices studied | License reported for repository | Intended role |
|---|---|---|---|
| [GitHub Spec Kit](https://github.com/github/spec-kit) | SDD, workflows, extensions, presets, bundles, catalogs | MIT | Modular component architecture |
| [Fission-AI OpenSpec](https://github.com/Fission-AI/OpenSpec) | Change lifecycle, custom schemas, artifact dependencies, requirements deltas | MIT | Declaration of optional outputs and change management |
| [genkovich/sdd](https://github.com/genkovich/sdd) | XS–XL sizing, quick/standard/full routes, surface-based gating, review/TDD | MIT | Conditional planning, minimality, specialist agent contracts |
| [gotalab/cc-sdd](https://github.com/gotalab/cc-sdd) | Discovery routing, task boundaries, implementation/review protocol, tool adapters | MIT | Adaptive paths and host capability handling |
| [OleksandrCEO/web-app-core](https://github.com/OleksandrCEO/web-app-core) | Repository instructions, project scaffolding, safety hooks | MIT | Source layout and developer ergonomics |
| [0xenzyme/agent-harness](https://github.com/0xenzyme/agent-harness) | Tasks, goals, execution DAGs, verification, state | MIT | Optional orchestration architecture |
| [SUNRNEHUI/agent-harness](https://github.com/SUNRNEHUI/agent-harness) | Planning contracts, bounded delegation, handoff and evidence | MIT | Evidence/handoff patterns |
| [OpenAI Codex](https://github.com/openai/codex) | Coding-agent host architecture and platform capabilities | Apache-2.0 | Host reference only; not an SDD template |

Also informed by developer-harness architectural examples discussed during design, including an AgentSG reference (AGENTS.md, ADRs, constitution, current/target architecture, independent verifier, documentation-impact checks). No authoritative repository URL or reusable license for AgentSG is known here; **do not copy its files until provenance and permissions are established**.

## Distinct product contribution

The product combines an assessment of the **target project's needs and risks** with a **beginner experience layer**, a **reuse-first discovery stage**, and an **explainable selection engine** that chooses the minimum sufficient Developer Harness across multiple coding-agent environments.
