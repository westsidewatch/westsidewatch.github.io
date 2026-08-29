# DORÉ CLOUDFLARE PLACEMENT / DELIVERY EVIDENCE LEDGER — 2026-08-29

Status: SWEEP-01 RECONCILED
Source family: `dore-core/cloudflare/`
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

## Bounded evidence reviewed

- `ASSET-MIGRATION-MILESTONE-PLAN-2026-08-24.md`
- `R2-DELIVERY-MILESTONE-2026-08-24.md`
- `R2-PRIORITY-B-SITE-MEDIA-MILESTONE-2026-08-24.md`
- `JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`
- `STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`
- `SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`
- `DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- linked production receipts and current Master Register interpretations for ONE, JOIN and SEARCH.

## Reconciled historical milestone chain

### 1. Priority-A asset migration — `VERIFIED_COMPLETE`

The migration milestone records Priority A closure with zero unresolved Priority-A items. It explicitly preserved rollback/runtime copies until an R2-backed delivery path existed and excluded search/corpus JSON from media migration.

### 2. ONE private-R2 delivery/runtime cutover — `VERIFIED_COMPLETE`

The later delivery milestone materially supersedes the temporary rollback state in the migration plan. Seven canonical ONE assets were delivered through the private R2 + D1 registry endpoint, all seven delivered bytes matched registered SHA-256 values, active ONE references were cut over to stable asset-code URLs, rollback binaries were removed only after post-cutover verification, and post-removal delivery passed 7/7.

Current disposition: keep the milestone closed; maintain delivery/hash/reference regression. The canonical Doré Original 001–241 library remains explicitly outside this migration.

### 3. Priority-B shared site media — `VERIFIED_COMPLETE`

Five large site-media assets (`SITE-BACKGROUND`, `SITE-DAMASCUS-GATE`, `SITE-JERUSALEM-WALL`, `SITE-TEMPLE-STONE-LIGHT`, `SITE-WECHAT-QR`) were migrated to private R2, registered in D1, cut over through registry-driven delivery and removed from GitHub only after delivery verification.

Durable placement lesson: not all visual assets belong in R2. Code/UI/version-coupled identity assets and small fixtures that must change atomically with code remain GitHub-owned.

### 4. Journal + Liming media audit — `VERIFIED_COMPLETE` as a placement audit, not a migration

The audit found zero currently eligible local Journal/Liming binary media. `data/volumes/vol-00.yaml` and `data/resources.json` correctly remain versioned GitHub source data. The `0 writes / 0 removals` outcome is an intentional PASS because moving structured source data merely because R2 exists would create competing masters and violate the placement policy.

Revisit only when independently addressable owned Journal/Library binaries actually appear.

### 5. Structured-data runtime audit — `VERIFIED_COMPLETE`

The active search JSON snapshots remain on Pages/GitHub because they are deterministic versioned browser indexes, not media objects. D1 remains for mutable/queryable registry and operational state; R2 remains for independently addressable large media/content objects. Generated research snapshots remain GitHub evidence unless repository pressure later justifies cold archival.

This is a durable architecture decision, not a temporary failure to migrate.

### 6. Search runtime lifecycle consolidation — `VERIFIED_COMPLETE` for the declared non-destructive milestone

`dore-search-runtime.js` established one supplemental form-submit observation/event boundary (`dore:search-query`) and moved entity integration onto that shared lifecycle without rewriting Scripture Search. The milestone preserved the existing search execution path by design.

Current quality judgment: valid historical completion, but not proof that Search intelligence itself is unified.

### 7. Doré service layer v1 — `VERIFIED_COMPLETE` for the bounded service-contract milestone; current service-boundary quality is a revisit concern

`/api/dore/query` (`dore.query.v1`) created a product-neutral envelope and routing lanes for scripture, brain, asset and status queries. The milestone deliberately delegated Scripture requests to the existing browser runtime rather than claiming server-side semantic parity.

A later Sweep reconciliation (Checkpoint 19 / `RQ-003`) found that browser Search and `dore_core.search.BibleSearchIndex` still contain independently evolving Scripture intelligence. Therefore the 2026-08-24 statement that products have a stable Doré entry contract remains historically true at the routing-contract level, but must not be interpreted as proof of one canonical Scripture-search engine or zero duplicated search logic.

Current disposition: keep the service-layer milestone closed; route future semantic/service-boundary consolidation through existing `RQ-003` instead of reopening the historical milestone wholesale.

## Supersession / chronology corrections

- The Asset Migration plan's `PRIORITY B DEFERRED` state is historical and was superseded later the same day by the verified Priority-B site-media milestone.
- The migration plan's seven retained GitHub rollback binaries are historical and were superseded by the verified private-R2 delivery cutover, after which those binaries were safely removed.
- The Structured Data audit intentionally supersedes any blanket "large files should move to R2/D1" interpretation: runtime role and source-of-truth semantics govern placement, not size alone.
- Search Runtime Consolidation and Service Layer v1 are architectural compatibility milestones, not evidence that browser/Core search semantics were fully converged; later `RQ-003` governs that debt.

## Capability retention

This milestone chain established reusable operating rules:

1. classify by runtime role before migrating storage;
2. use stable logical identity (`asset_code`) rather than storage object paths as product contracts;
3. keep D1 metadata/query state distinct from R2 binary storage;
4. retain rollback copies until delivery + hash + active-reference verification passes;
5. remove redundant source binaries only after post-cutover proof;
6. accept intentional zero-migration outcomes when they preserve one canonical source of truth;
7. add compatibility/service boundaries without rewriting a proven engine until parity/regression evidence exists.

## Current sweep disposition

The current `dore-core/cloudflare/` placement/delivery milestone family is now systematically accounted for in Sweep 01. No new HUMAN_DECISION_BLOCKED or ENVIRONMENT_BLOCKED condition was discovered in this bounded family, and no P01 subtitle-path state/action was modified.
