# DORÉ DAWN VISUAL EDITORIAL DIRECTOR — EVIDENCE LEDGER

Date: 2026-09-11
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / ACCEPTANCE_PENDING
Owner workstream: `DAWN-LIBRARY`
Sweep parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Scope

This ledger reconciles the bounded Dawn Library Phase 2 visual-editorial sequence introduced on 2026-09-11. It does not replace the broader Dawn Library catalog/rights/relevance evidence ledger and does not promote the whole Library workstream to completion.

## Evidence reviewed

- commit `ada854e3c31d3503ac91df9315d2ec3326c8dff8` — Phase 2 Cut 01, Visual Fuzzy Retrieval Foundation;
- commit `58e90894c272a9b1454ac9c1d0104e2e45ea4d03` — Phase 2 Cut 02, graph-bound Editorial Director runtime;
- commit `ed8d9bb578ccc11633b0a14017ece2f0f212ab8e` — Phase 2 Cut 03, live Editorial Director surface consumption;
- `data/dawn_visual_editorial_queries.json`;
- `data/dawn_visual_editorial.json`;
- `scripts/dore/build-dawn-visual-editorial-feed.mjs`;
- `layouts/partials/visual-resource-card.html`;
- `.github/workflows/dawn-visual-graph-check.yml`.

## Current evidence-based interpretation

1. Phase 2 now has a real implementation chain rather than an isolated retrieval experiment: request manifest → graph-bound selection runtime → deterministic generated editorial feed → Hugo card consumption.
2. The initial persisted request is concrete: `Sea of Galilee storm`, `WATCH`, `Mark 4:35–41`, `8:5`, `card-8x5`, `display`, minimum authority `C`, limit `1`.
3. The persisted generated feed identifies `visual-princeton-galilee-storm-1591` with score `0.506667`, authority class `A`, and `card-8x5` surface support. The feed explicitly records `graphBound: true` and names `dore.visual-editorial-director.v1` as source.
4. The Dawn visual card now consumes that feed and exposes a distinct `EDITORIAL DIRECTOR` state plus director score when the current VisualWork is selected. This is meaningful surface integration, not merely a backend ranking artifact.
5. The workflow contract has also been tightened: it rebuilds `data/dawn_visual_editorial.json` and fails if the committed feed differs, protecting deterministic regeneration from the request/runtime/graph inputs.
6. No workflow run associated with commit `ed8d9bb578ccc11633b0a14017ece2f0f212ab8e` was returned by the available commit-workflow probe in this reconciliation. Therefore the repository implementation is real, but a successful CI execution and production storefront readback for Cut 03 are not yet proven here.
7. This work must not be conflated with the separate Chinese `聖經世界` relevance defect (`RQ-006`). A correct visual-selection path does not repair book/catalog editorial relevance, and rights cleanliness still does not equal editorial fit.

## Classification

- Visual fuzzy retrieval foundation: bounded implementation milestone, `COMPLETED / RETAIN` inside the active workstream.
- Graph-bound Editorial Director runtime: bounded implementation milestone, `COMPLETED / RETAIN` inside the active workstream.
- Dawn surface consumption of generated director feed: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`, with acceptance evidence still pending.
- Whole Dawn Library visual-editorial system: **not** `VERIFIED_COMPLETE`.

## Missing evidence / acceptance boundary

Before promoting this slice to a verified surface milestone, retain at least:

1. one successful `dawn-visual-graph-check` run containing the feed-build/diff gate;
2. one production Dawn Library readback proving the director-selected VisualWork actually renders with the intended card state and metadata;
3. one negative/contrast case proving an unselected visual does not receive the director-selected state;
4. one changed-request regeneration case proving the output follows the request/graph rather than a hard-coded visual identity;
5. no regression in rights/authority/surface-preset constraints.

## Revisit trigger

Reopen this architecture if the feed becomes hand-edited, graph identity drifts from surface identity, selection scores are exposed as authority rather than ranking evidence, request changes fail to regenerate deterministically, or visual curation begins bypassing rights/authority/surface constraints.

## Durable judgment

Retain the request → graph-bound runtime → generated feed → surface-consumption pattern as a reusable Dawn editorial-selection primitive. Treat current Cut 03 as real implementation progress with acceptance pending, not as a new global Doré editorial-intelligence completion token.
