# ADR-002 — DORÉ DESIGN 2.0

Status: Accepted / implementation gate opened
Date: 2026-09-05
Issue: #294

## Decision
DORÉ DESIGN is the production workbench. A versioned DORÉ document is the single source of truth for editor, preview and publication. DOM is a renderer, never the source of truth.

## Layers
1. Document — stable IDs, content, geometry/style, semantic intent, assets, publication metadata.
2. Commands — every user mutation is an explicit validated command. Undo/redo records commands/revisions, not DOM snapshots.
3. Renderer — deterministic DOM from document coordinates. Viewport zoom never changes document geometry.
4. Interaction adapters — Moveable/Selecto first; replaceable and editor-only.
5. Inspector — contextual precision controls for Page/Text/Image/Selection.
6. DORÉ — contextual recommendation + accept/reject observation; never blocks direct editing.
7. Publication — immutable candidate revision -> validation -> preview -> explicit publish -> rollback metadata.

## Dependency boundary
No framework migration. No React/Vue requirement. Daybrush interaction packages are pinned, locally bundled/vendored for production, and isolated behind adapters. Published pages contain no editor runtime. OpenPencil/Penpot/Puck/GrapesJS remain reference/harvest sources unless a later ADR proves a runtime dependency necessary.

## Security boundary
Resident remains localhost-scoped. Editor requests express domain operations, never shell commands. Publish accepts only allowlisted page ID + exact revision. It cannot accept arbitrary filesystem paths or executable code. Imported/user content is data; arbitrary JS is never executed. Build happens in staging and only a validated candidate can be promoted. Last-known-good publication metadata is retained.

## Command contract v1
Commands are JSON objects with `op`, `page_id`, target IDs where relevant, and typed values. Initial operations:
- `node.patch`: validated geometry/text/style patch for one node.
- `node.patch_many`: atomic validated patches for a selection.
- `node.nudge`: document-coordinate delta.
- `node.align`: left/center/right/top/middle/bottom against selection bounds.
- `node.distribute`: horizontal/vertical distribution.
- existing add/delete/duplicate operations remain compatibility commands until migrated.

Geometry fields are finite document-coordinate numbers. Width/height must be positive when present. Text alignment is one of left/center/right. Font size has bounded positive values. Unknown style/geometry keys are rejected at the 2.0 command boundary.

## Compatibility strategy
DORÉ DESIGN 1.9.1 remains the fallback on `main`. 2.0 develops on `dore-design-2`. Multiwrite Homepage is the first production specimen. No replacement until parity acceptance passes.

## First acceptance slice
Open Multiwrite Homepage -> select a text node -> center text -> change font size -> drag/move -> resize -> undo/redo, with the document remaining canonical and deterministic. Publication is deliberately not coupled to this first slice.
