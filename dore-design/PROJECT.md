# Doré Design

Status: WORKING PRODUCT FOUNDATION COMPLETE — ACTIVE EVOLUTION
Established: 2026-08-30
Accepted working foundation: 2026-08-31

## Mission

Doré Design is the local structured design environment built for the existing Doré stack and real Westside Watch / ONE production work. It is not intended to reproduce Figma, Penpot, or another general-purpose design suite.

The fixed goal is reliable design production in one shared artifact that both the human and Doré can inspect and edit. Tools and upstream components remain replaceable.

## Working product

Doré Design 0.9 is the accepted resident product foundation. It runs locally at `127.0.0.1:4310` through a macOS LaunchAgent and stores a durable multi-page `dore.design.workspace.v1` document.

The same workspace is exposed through the browser, HTTP API and Doré CLI. Human and machine edits therefore modify one document rather than separate visual copies.

Current working surface includes:

- multi-page/artboard workspace;
- page create, rename, duplicate and delete;
- structured layers with create, edit, duplicate and delete;
- direct pointer dragging on the canvas;
- Inspector editing of coordinates, width, type size and text;
- shared design tokens;
- canvas dimensions;
- keyboard Delete/Backspace;
- history and Undo / Cmd-or-Ctrl-Z;
- deterministic per-page SVG render/export;
- machine verification of every page and render hash;
- resident HTTP control surface;
- Doré CLI read/write/verify/export surface;
- migration guard for superseded legacy structural data;
- local same-artifact acceptance testing.

## Acceptance contract — PASSED for the working foundation

The working foundation was required to satisfy all of the following:

1. Doré can execute the local workflow without the user acting as a terminal operator.
2. The human can open and see the rendered design.
3. The result remains structurally editable rather than being a flattened AI image.
4. Doré can inspect and modify the same document in later iterations.
5. The same artifact can be rendered/exported and machine-verified after mutation.
6. Core operation is local and does not depend on metered paid AI/API quotas.
7. Failures and acceptance results are machine-readable and can be returned through the resident execution path.

GitHub Actions product acceptance run `33379900466` completed SUCCESS.

Physical Mac task `dd-product-020` completed SUCCESS on the resident 0.9 service. Health reported `version=0.9`, `workspace=multi-page`, `direct_manipulation=true`. The live acceptance probe returned `DORE_DESIGN_LOCAL_ACCEPTANCE_PASS` after mutating the same workspace, confirming rerender and machine verification, and cleaning up its probe. Workspace verification also confirmed the obsolete legacy structure was absent.

## Architecture

`Human browser ↘`

`                 shared structured workspace -> canvas/render -> SVG/verifier/history`

`Doré CLI/API  ↗`

The document is the durable object. The browser canvas is a human editing view; the CLI/API is Doré's machine editing view; both address the same state.

GitHub is versioning, synchronization, backup and remote engineering coordination. It is not the intended central bus for every local edit. Doré's mature local path is direct controlled local tooling -> Doré Design workspace -> render/verify -> evidence/versioning.

## Engineering rules

- Goal fixed; components replaceable.
- Current product state outranks superseded design memory.
- Do not restart visual discovery when the editing engine changes.
- Preserve structured identity across edits.
- Structural evidence is required to prove a mutation occurred.
- Render verification follows mutation; it does not substitute for mutation evidence.
- Human intervention is reserved for genuine authorization, unavoidable GUI-only actions, or high-risk/irreversible decisions.
- Build new editing capabilities from concrete production needs rather than speculative feature parity with incumbent design suites.
- Every real production cycle should leave both work evidence and reusable Doré learning evidence.

## Product phase transition

The original construction/bake-off phase is closed. Penpot, OpenPencil, Framesmith, Doop, Tela and other projects remain sources of reusable ideas/components, but no provider is a prerequisite for Doré Design operation.

The next phase is production and evolution: use Doré Design for actual Westside Watch / ONE work, discover missing capabilities through that work, add them to the self-owned product, verify them, and teach Doré through the same real production loop.

The project now succeeds or fails on the quality and reliability of real design work produced in Doré Design, not on whether an upstream provider passes an experiment.
