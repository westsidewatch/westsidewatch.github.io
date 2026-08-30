# Doré Design — Provider Bake-off

This is an engineering selection process, not a feature-list comparison.

## Shared production brief

Every provider receives the same Westside Watch homepage design objective and brand constraints. No candidate passes merely because it installs, connects, or creates a rectangle.

## Gates

| Gate | Requirement |
|---|---|
| G0 | Open-source source and license identified |
| G1 | Runs in current local/macOS environment without incremental paid service |
| G2 | Doré can control it without user terminal mediation |
| G3 | Doré can create/read/update/delete structured design nodes |
| G4 | Doré can render/export evidence |
| G5 | User can see the real design |
| G6 | Result remains editable |
| G7 | Doré can perform a second revision on the same document |
| G8 | Repeated-operation stability test passes |
| G9 | Failure/recovery behavior is observable and bounded |

## Candidates

| Candidate | Base-engine potential | Components to inspect | Status |
|---|---|---|---|
| Penpot | yes | canvas, document model, plugin/MCP, export | compatibility investigation |
| OpenPencil | high | canvas, MCP, CLI, node tools, import/export | priority experiment |
| Framesmith | possible supporting engine | scene graph, renderer, headless visual review | experiment |
| Doop | possible | agent-native canvas, MCP, collaboration, memory | experiment |
| Tela | possible component/base | SVG canvas, local-first state, RPC/dispatch | experiment |

## Decision rule

The first stable provider is allowed to become the provisional base; testing continues far enough to identify superior reusable components in other candidates. Doré Design should combine compatible strengths through clean boundaries rather than becoming permanently coupled to the first winner.

## Evidence required per candidate

- exact source/revision/version
- license
- environment and install result
- control interface
- CRUD mutation evidence
- real Westside Watch artifact/render
- editability evidence
- second-revision evidence
- repeated-operation results
- failures/workarounds
- components recommended for reuse
- final disposition: reject / observe / component / provisional base / base
