# DORÉ DESIGN 2.0 — Phase 4

Status: IMPLEMENTING / SOFTWARE GATES BUILT
Issue: #294

## Implemented
- immutable page snapshot with SHA-256 integrity
- deterministic canonical snapshot renderer
- candidate registry isolated from mutable workspace state
- revision-bound preview
- explicit publish promotion
- current-release + last-known-good metadata
- rollback
- structural / URL / executable-content validation before promotion
- allowlisted staging targets and staging manifest
- accessibility / link / published-runtime smoke checks
- published-render hash parity check
- resident 2.0 entrypoint layered on the current product
- tests for snapshot immutability, publish/rollback, validation rejection and render parity

## HTTP contract
- `POST /api/design2/candidate`
- `GET /api/design2/preview?candidate=<id>`
- `POST /api/design2/publish`
- `GET /design2/published`
- `POST /api/design2/rollback`
- `GET /api/design2/publication`

## Invariants
- Save never publishes.
- Published output reads the promoted immutable candidate, never live mutable workspace state.
- Publish is candidate/revision-bound.
- Invalid snapshot integrity, duplicate IDs, executable attributes and unsafe URL schemes block promotion.
- Promotion requires an allowlisted target and staging manifest.
- Image accessibility, link shape, editor-runtime absence and snapshot marker are checked before promotion.
- Public rendering must hash-match the staged candidate rendering.
- Published output contains no editor runtime dependency.

## Remaining closure gate
Run CI + resident/local acceptance. Only after that passes may the installed service switch from the 1.9.1 fallback entrypoint to `app_design2.py`. The fallback remains available until parity acceptance.
