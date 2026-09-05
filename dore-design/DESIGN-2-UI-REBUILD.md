# DORÉ DESIGN 2.0 — UI REBUILD

Status: ACTIVE

## Principle
External design tools and open-source projects are learning material, not product dependencies by default. DORÉ studies interaction models, document authority, rendering, safety, local-first operation and agent interfaces, then distills them into small owned primitives.

Target qualities: free, small, simple, low-energy, safe, stable, maintainable, local-first.

## Recovered product direction
- one canonical structured workspace shared by human and DORÉ
- Pages/Layers at left; canvas in the center; contextual properties at right
- direct manipulation first
- Multiwrite is a real workspace page, not a separate design lab
- revisions/history remain durable
- AI/DORÉ operates through the same semantic operations as human editing
- generated output remains editable structured design, not an opaque bitmap
- product UI must visibly expose the Design 2.0 capabilities instead of hiding them behind APIs

## Research absorbed
Earlier recovery: Penpot; OpenPencil; Puck; GrapesJS; Rete; React Flow; Daybrush Moveable/Selecto/Guides; Figma/UI-kit patterns; local-first and structured-artifact approaches.

2026 continuation: Tela (direct manipulation, command palette, agent RPC, shared model); Artboard (JSON-on-disk, deterministic CLI rendering); Excalidraw (mature local canvas interaction); Fastlab Design Editor; Tasfer (headless canvas/document separation); Shotluma (agent uses same editor operations); Memi Canvas (revision-bound human/agent proposals); Oasis Editor; Open Design Studio; Avnac/OpenUI.

## Rebuild contract
The existing structured workspace, revision history, deterministic rendering, publication/rollback and A2A control plane remain authoritative. UI rebuild is a new visible product shell over those capabilities, not a second state system.

### Surface 1 — Product shell
- compact top bar: product/workspace identity, current page, revision, save state, preview/publish state
- left rail: Pages / Layers / Assets
- central canvas: direct selection, drag, resize, zoom/pan, alignment feedback
- right rail: contextual Inspector based on selected node
- DORÉ command surface integrated into the product rather than a detached chatbot

### Surface 2 — Multiwrite first consumer
- `multiwrite-home` is the first acceptance page
- image/cover asset is visible as a first-class layer
- human and DORÉ can select and mutate the same nodes
- asset placement, hierarchy and semantic design are visible in Inspector

### Surface 3 — lightweight primitives
Implement/retain owned primitives before importing frameworks:
- selection state
- transform handles
- camera/zoom
- layer tree
- contextual inspector
- asset registry
- command dispatch
- keyboard command map
- revision/status strip
- DORÉ semantic action dispatch

## Acceptance
UI rebuild is not accepted because APIs exist. It passes only when opening Design visibly shows the new product shell and `multiwrite-home` can be edited through it while preserving the canonical workspace and revision model.
