# Third-party notices and modified works

**Status of the MVP:** No third-party source files, SKILL.md bodies, scripts, or agent definitions have intentionally been copied into the generator or target library. This does not imply the sources listed in `INSPIRATIONS.md` are owned by this project.

Before importing or modifying an external file:

1. Record original repository URL, exact path, commit SHA / release, author or copyright holder, license and all associated notices.
2. Confirm the file belongs to that license and that dependencies/assets do not carry different terms.
3. Preserve the original copyright and applicable MIT license text for copies/substantial portions. Observe other license obligations where applicable (e.g. Apache-2.0 NOTICE and modification notices).
4. Identify our modifications and new paths; separate source-derived files from independently authored files.
5. Recheck obligations when distributing the bundle or generated target files. Notices may need to accompany **generated output**, not merely the generator source.
6. Record source and license in machine-readable module metadata and in the generated Harness Plan.

## Imported components registry

| Generated path / module | Origin URL + revision | Original author / license | Modifications | Required notices included? |
|---|---|---|---|---|
| _No external files incorporated in this starter_ | — | — | — | — |

A `SOURCES.md`/`INSPIRATIONS.md` credit is **not a substitute** for carrying legally required notices when source files are copied or adapted. Seek legal review for uncertain cases or license incompatibilities.

## Original generated assets

`library/target/` contains original MIT components, copyright 2026 chetrik. Each installed file is listed in `.adaptive-harness/manifest.json` with source path/content fingerprint, copyright, license and scope; `.adaptive-harness/LICENSE` carries the full license. For an existing AGENTS.md, attribution applies only to the generated block; prior user text retains its ownership. This is not evidence of third-party import support.

0.5.0 platform delivery: official Anthropic GitHub examples, Cursor/Antigravity/Lovable/AI Studio documentation and Ollama API documentation were used to confirm file/API contracts. No source implementation or prompt bodies were copied. New target files are original project MIT assets. A temporary Claude CLI 2.1.317 installation was used for diagnostics only, outside this repository; it is not bundled or redistributed. Exact references are in docs/PLATFORM_DELIVERY.md.
