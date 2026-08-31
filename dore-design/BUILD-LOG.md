# Doré Design — Construction / Teaching Log

Status: BUILDING

Doré observes this log while ChatGPT owns the mainline engineering.

## Build 001 — Own the minimum working spine

Decision: stop making provider success a prerequisite for Doré Design. Build a tiny self-owned spine first, then reuse upstream components behind it.

Why: the accumulated Penpot/OpenPencil/Framesmith experiments proved the needed abstractions but also proved that provider-specific failures can stall the product goal.

Implemented spine:

`structured document JSON -> mutation API -> browser canvas`

File: `dore-design/app.py`

Current document contract: `dore.design.v1` with tokens, stable node IDs, node roles, geometry, typography/content fields, revision and updated_at.

Current control surface:

- `GET /api/document/<id>` reads the same structured document shown to the human.
- `POST /api/document/<id>/mutate` performs a bounded mutation on a stable node ID.
- `/` renders that same document in a browser canvas.

Teaching point for Doré: a design tool is not an image generator. The durable object is the structured document. The canvas is a view of that object; mutation changes the object; render makes the change visible. Provider adapters can later translate this stable contract to/from Framesmith, Tela, Doop, Penpot, or another engine.

Next acceptance work: run locally, verify browser render, verify same-document mutation increments revision and visibly changes canvas, then add save/history/export/visual evidence and stronger node operations.
