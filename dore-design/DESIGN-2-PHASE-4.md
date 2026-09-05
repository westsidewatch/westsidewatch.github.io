# DORÉ DESIGN 2.0 — Phase 4

Status: ACTIVE
Issue: #294

## Gate
Canonical renderer + Preview/Publish immutable snapshot pipeline + rollback.

## Invariants
- One canonical DORÉ document feeds editor preview and published rendering.
- Save never publishes.
- Preview renders an exact immutable candidate revision.
- Publish requires page ID + exact revision and rejects stale candidates.
- Build goes staging -> validate -> promote.
- Last-known-good publication metadata is preserved and rollback remains available.
- Publication targets are allowlisted; no arbitrary filesystem path or executable input.
- Published output contains no editor runtime or Moveable/Selecto dependency.

## First implementation slice
1. Canonical revision snapshot object with content hash.
2. Candidate registry separated from mutable workspace state.
3. Deterministic renderer entry point over a supplied snapshot.
4. Validation contract and staging manifest.
5. Promotion metadata with previous/last-known-good revision.
6. Rollback operation that selects a prior validated immutable release.
