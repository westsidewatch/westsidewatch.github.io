# Jerusalem 3000 — Phase 2

Status: ACTIVE

Phase 1 is accepted: canonical DEM, Three.js runtime, temporal lifecycle, evidence gates, destruction/rebuild transitions, and terrain-aware city placement are operational.

Phase 2 replaces schematic proof geometry with historically legible Jerusalem.

## Workstream A — Urban morphology

- Era-specific city footprint and expansion envelope
- Street and lane hierarchy
- Block / courtyard fabric instead of uniform boxes
- Density and building-height grammar by era
- Terrain-following placement remains mandatory

## Workstream B — Fortification

- Era-specific wall circuits
- Gates, towers, citadel and defensive transitions
- Destruction / abandonment / rebuilding states

## Workstream C — Monumental anchors

- Temple / sanctuary complexes
- Palaces, civic and religious monumental structures
- Major churches, mosques, citadel and later landmarks where historically applicable
- Evidence class remains visible in the reconstruction contract

## Workstream D — Infrastructure

- Water systems
- Roads and processional axes
- Valleys / topographic constraints as city-form drivers

## Workstream E — Temporal differentiation

Every anchor phase must be visually distinguishable without reading the caption. A phase change must alter several of: footprint, wall circuit, street structure, density, monumental anchors, ruin state, or expansion direction.

## Phase 2 first executable slice

Replace the generic `addEraFabric()` box grid with a terrain-aware urban morphology generator composed of streets, courtyard blocks, perimeter walls and landmark anchors. Start with three calibration eras: David–Solomon, Herodian–Jesus, and Crusader. Once the grammar is stable, propagate it across the complete timeline.

## Hard rule

Phase 2 must not regress Phase 1. Canonical terrain, runtime readiness, evidence audits, reversibility and timeline controls remain production gates.
