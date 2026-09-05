# DORÉ DESIGN 2.0 — Phase 4

Status: IMPLEMENTING
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
- Public rendering must hash-match the staged candidate rendering.
- Published output contains no editor runtime dependency.

## Remaining closure gates
1. Add accessibility/link/smoke validator hooks.
2. Run resident acceptance and only then switch the installed service entrypoint from fallback to `app_design2.py`.
3. Keep 1.9.1 fallback until parity acceptance passes.
