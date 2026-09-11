# DORÉ DAWN VISUAL GRAPH PHASE 1 — EVIDENCE LEDGER

Date: 2026-09-11
Status: VERIFIED_BOUNDED_MILESTONE
Parent workstream: Dawn Library / Visual Graph
Sweep source: Memory Consolidation Sweep 01
P01 impact: NONE

## Evidence reviewed

- PR #618 — `Dawn Library 2.0: Visual Graph Phase 1`, merged to `main` as `b623fa9dbcd355f661911c9f18178c9345fb0691`.
- PR #634 — `Dawn Library 2.0: add verified-only historical map surface`, merged into the Phase 1 branch as `a10b1336691cb8ae2de1d36966c596167ef7ec69`.
- Workflow run `34559244117` — `Dawn Visual Graph Check`, completed with conclusion `success` against Phase 1 head `a10b1336691cb8ae2de1d36966c596167ef7ec69`.
- Issue #636 — `Dawn Library 2.0 — Visual Graph Phase 2 Engineering Memo`, retained open as the explicit deferred-work boundary.

## Verified Phase 1 milestone

The reviewed evidence supports a bounded Phase 1 completion claim for the shared Visual Graph architecture, not a completion claim for Visual Graph as a whole.

Implemented and acceptance-gated:

1. `VisualWork`, `VisualRepresentation`, `VisualRegion`, and `SurfacePreset` are represented as first-class visual-resource structures.
2. Rights resolution is fail-closed; generated work is prevented from entering A/B/C authority canon.
3. Shared `VisualSurface` consumption is proven across Dawn Library and the homepage rather than duplicated presentation logic.
4. The acceptance set contains four deliberately different fixtures: Doré biblical engraving; religious art/manuscript; historical Palestine map; Chinese-Christian historical photograph.
5. Native IIIF support and at least one authority-defined manuscript crop are asserted by CI.
6. Historical-map handling explicitly separates historical place/survey evidence from raster georeference evidence. An unverified map cannot expose an Allmaps annotation or activate overlay.
7. The Phase 1 workflow validates graph identity, rights-policy references, provenance constraints, IIIF requirements, map fail-closed behavior, JavaScript syntax, and a Hugo production build.
8. The final Phase 1 workflow run completed successfully before merge.

## Classification

- Dawn Visual Graph Phase 1: `VERIFIED_BOUNDED_MILESTONE / IMPLEMENTED_FOUNDATION`.
- Map georeference/Allmaps activation: `DEFERRED / UNKNOWN_NEEDS_EVIDENCE` beyond the verified fail-closed boundary.
- Visual Intelligence / visual fuzzy search / multimodal retrieval: `DEFERRED / DISCOVERY`.
- Doré Visual Corpus expansion and Visual RAG → Image Local generation bridge: `DEFERRED / ACTIVE_PARALLEL` under Phase 2, not Phase 1 completion evidence.
- Cross-product rollout beyond Dawn Library + homepage: `DEFERRED / ACTIVE_PARALLEL`.

## Superseded / retired interpretation

The earlier interpretation that Dawn Library visual handling was mainly a presentation/storefront concern is now superseded for this bounded family. The durable architecture is a shared resource graph + surface layer with explicit rights/provenance boundaries. Individual source URLs, crops, providers, or page-specific image hardcodes must not be treated as the canonical architecture.

The Phase 1 branches/PRs are closed by design. Additional provider growth, manual GCP refinement, visual-intelligence experiments, corpus expansion, and new surface types are explicitly Phase 2 work and should not reopen Phase 1.

## Revisit candidates / missing evidence

1. A reviewed raster pixel↔geographic control-point set or standards-compliant Georeference Annotation for the PEF map is still missing; map overlay correctly remains fail-closed until that exists.
2. No Phase 1 evidence proves real Allmaps interaction against a verified annotation.
3. No Phase 1 evidence proves visual fuzzy search, multimodal embeddings, composition/light similarity retrieval, or image-to-image retrieval.
4. Doré corpus growth beyond the initial authenticated fixtures remains open.
5. Visual RAG → Image Local generation must preserve the one-way anti-pollution boundary: authority corpus → retrieval/reference → generation; generated assets must not silently re-enter authority/training canon.
6. ONE, Journal, Doré Folio, and Doré Design have not yet been verified as consumers of the shared `VisualSurface` architecture.

## Smallest next proof

Preserve Phase 1 as closed and regression-protected. Begin Phase 2 with one bounded task only: either (a) verify one standards-compliant historical-map georeference/Allmaps path without weakening fail-closed rules, or (b) prove one real cross-product consumer using stable VisualWork identity and shared VisualSurface. Do not expand provider count merely for coverage.

## P01 safety

No P01 subtitle runtime, deployment, credential, audio/transcription dependency, ordering, or blocker state was modified.