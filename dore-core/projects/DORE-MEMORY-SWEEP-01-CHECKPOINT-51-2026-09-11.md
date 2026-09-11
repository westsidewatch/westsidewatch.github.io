# DORÉ MEMORY SWEEP 01 — CHECKPOINT 51

Date: 2026-09-11
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-DAWN-VISUAL-GRAPH-PHASE1-EVIDENCE-LEDGER-2026-09-11.md`

## Bounded evidence reviewed

- PR #618 — Dawn Library 2.0 Visual Graph Phase 1;
- PR #634 — verified-only historical map surface;
- workflow run `34559244117` (`Dawn Visual Graph Check`) with conclusion `success`;
- issue #636 — Visual Graph Phase 2 engineering/deferred-work memo.

## Reconciliation findings

1. Dawn Library Visual Graph Phase 1 is a real bounded implementation milestone, not merely an architectural proposal. The implementation was merged and its dedicated acceptance workflow completed successfully.
2. The verified Phase 1 boundary includes first-class VisualWork / VisualRepresentation / VisualRegion / SurfacePreset structures, rights/provenance constraints, shared VisualSurface consumption, native IIIF validation, authority-defined manuscript-region evidence, and four heterogeneous acceptance fixtures.
3. Historical-map support is correctly classified as a safe foundation rather than a finished mapping capability. The implementation explicitly keeps historical survey/place evidence separate from raster georeference control points and prevents Allmaps activation while georeference remains unverified.
4. The Doré biblical engraving fixture is content/authority evidence inside the visual graph. It must not be confused with the separate VIS-GRAMMAR objective of generating purpose-built Doré-style website assets.
5. Issue #636 is the durable deferred-work boundary: cartographic intelligence, visual fuzzy search/multimodal retrieval, richer VisualRegions, Doré corpus expansion, Visual RAG → Image Local, broader surface rollout and provider adapters belong to Phase 2 and should not reopen Phase 1.
6. The anti-pollution rule is explicit and strategically important: authority corpus → Visual RAG/reference → Image Local → generated asset is one-way; generated outputs remain derivative/generated and do not silently re-enter authority/training canon.
7. This checkpoint supersedes any interpretation of Dawn Library visual work as only page-level image presentation. The durable direction is a shared visual-resource graph plus surface layer reusable across products.
8. No P01 subtitle ordering, runtime, deployment, audio/transcription dependency, credential or blocker state was changed.

## Classification updates

- Visual Graph Phase 1: `VERIFIED_BOUNDED_MILESTONE / IMPLEMENTED_FOUNDATION`.
- Historical map overlay: `DEFERRED / UNKNOWN_NEEDS_EVIDENCE` beyond fail-closed foundation.
- Visual fuzzy search / multimodal visual intelligence: `DEFERRED / DISCOVERY`.
- Doré Visual Corpus expansion + Visual RAG → Image Local: `DEFERRED / ACTIVE_PARALLEL`.
- Shared VisualSurface rollout beyond Dawn Library + homepage: `DEFERRED / ACTIVE_PARALLEL`.

## Revisit / missing-evidence candidates

- one standards-compliant verified Georeference Annotation or reviewed raster GCP set;
- one real Allmaps interaction proof after georeference verification;
- visual fuzzy-search / image-to-image / composition-light retrieval proof;
- expanded authenticated Doré visual corpus;
- verified VisualSurface consumption by ONE, Journal, Doré Folio or Doré Design.

## Canonical-register delta to reconcile

- `MEM-SWEEP-01`: add Checkpoint 51 and the Visual Graph Phase 1 evidence ledger to reconciled evidence.
- `DAWN-LIBRARY`: record Visual Graph Phase 1 as a verified bounded foundation while keeping Phase 2 open.
- `VIS-GRAMMAR`: retain separation between curated/original-work authority resources and purpose-built Doré-derived/generated brand elements.

## Smallest next proof

Keep Phase 1 closed and regression-protected. For Phase 2, prefer one narrow proof: either verified georeference → Allmaps without weakening fail-closed policy, or one new real product consuming stable VisualWork identity + shared VisualSurface.

Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and introduces no new human/environment blocker.