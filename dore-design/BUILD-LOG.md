# Doré Design — Construction / Teaching Log

Status: BUILDING

Doré observes this log while ChatGPT owns the mainline engineering.

## Build 001 — Own the minimum working spine

Decision: stop making provider success a prerequisite for Doré Design. Build a tiny self-owned spine first, then reuse upstream components behind it.

Implemented: `structured document JSON -> mutation API -> browser canvas`.

Teaching point: a design tool is not an image generator. The durable object is the structured document. Canvas is a view; mutation changes the object; render makes it visible.

## Build 002 — Make the document durable and operable

The spine now owns a real document lifecycle instead of a demo-only mutation.

Added:

- revision history snapshots before every mutation;
- stable node CRUD: set, add, delete;
- design-token mutation for palette work;
- explicit canvas dimensions;
- deterministic SVG export from the same structured document;
- browser workbench exposes export and same-document refinement.

Control contract:

- `GET /api/document/<id>` — inspect current structured state.
- `POST /api/document/<id>/mutate` with `op=set` — edit an existing node by stable ID.
- `op=add` / `op=delete` — structural editing.
- `op=token` — alter a named design token.
- `GET /api/document/<id>/export.svg` — export a visible vector representation generated from current state.

Teaching point for Doré: editing must preserve identity. If `hero` changes size, it is still the same `hero` node in the same document and revision advances. Before mutation, the previous revision is snapshotted. This is the basis for later undo, comparison, visual verification and autonomous repair.

Next acceptance: exercise Build 002 locally as a real resident service, verify GET -> mutate -> GET revision/state change -> SVG export. Then add machine-readable health/verification and a resident launch path so Doré Design is a tool, not a script someone has to manually start.
