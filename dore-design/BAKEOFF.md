# Doré Design — Provider Bake-off

Status: `SUPERSEDED / PHASE_CLOSED / HISTORICAL_EVIDENCE`

Current governing product state: `dore-design/PROJECT.md`.
Durable Sweep evidence: `dore-core/projects/DORÉ-DORÉ-DESIGN-FOUNDATION-EVIDENCE-LEDGER-2026-09-01.md`.

This file preserves the original engineering selection process and its acceptance gates. It is **not** a current execution plan and must not reactivate Penpot, OpenPencil, Framesmith, Doop, Tela, or any other provider as a prerequisite for Doré Design operation.

## Shared production brief

Every provider received the same Westside Watch homepage design objective and brand constraints. No candidate passed merely because it installed, connected, or created a rectangle.

## Historical gates

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

## Historical candidates

| Candidate | Base-engine potential | Components inspected / intended | Historical status |
|---|---|---|---|
| Penpot | yes | canvas, document model, plugin/MCP, export | provider experiment; no longer prerequisite |
| OpenPencil | high | canvas, MCP, CLI, node tools, import/export | provider experiment; no longer prerequisite |
| Framesmith | possible supporting engine | scene graph, renderer, headless visual review | component/reference source only |
| Doop | possible | agent-native canvas, MCP, collaboration, memory | component/reference source only |
| Tela | possible component/base | SVG canvas, local-first state, RPC/dispatch | component/reference source only |

## Historical decision rule

The first stable provider was allowed to become a provisional base while testing continued far enough to identify reusable components in other candidates. That rule served the construction phase.

It is now superseded by the accepted self-owned Doré Design architecture:

`shared structured workspace → human + Doré mutation → deterministic render/export → machine verification → revision/history`

Upstream projects may still contribute ideas or compatible components, but provider success is no longer a product prerequisite.

## Historical evidence required per candidate

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

## Current interpretation

Do not resume this bake-off merely because Doré Design needs a new feature. New capabilities should be driven first by real production gaps in the self-owned product. Reopen a provider investigation only when a concrete missing capability is better satisfied by reusing an upstream component than by extending Doré Design directly, and treat that as bounded component research rather than a return to the original provider-selection phase.
