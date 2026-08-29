# DORÉ CLOUDFLARE ASSET + SEARCH RUNTIME EVIDENCE LEDGER — 2026-08-28

Status: ACTIVE / SWEEP-01 EVIDENCE
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Related canonical rows: `ONE`, `JOIN`, `SEARCH`, `STEWARDSHIP`, `MEM-SWEEP-01`

## Bounded evidence reviewed

- `dore-core/cloudflare/ASSET-MIGRATION-MILESTONE-PLAN-2026-08-24.md`
- `dore-core/cloudflare/R2-DELIVERY-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/R2-PRIORITY-B-SITE-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`
- canonical `DORÉ-MASTER-WORK-REGISTER.md`
- existing `DORÉ-COMPLETED-WORK-LEDGER.md` interpretation for `CW-011`
- existing Search revisit interpretation (`RQ-003`) from Sweep checkpoint 19

## Reconciliation findings

### 1. Priority-A ONE R2 migration/delivery is a defensible historical completion

The 2026-08-24 asset-migration milestone and private R2 delivery milestone form one bounded completed sequence rather than two independent products.

Evidence is materially stronger than a commit-only claim:

- Priority-A unresolved count reached zero;
- selected ONE binaries were migrated/deduplicated into private R2 and registered in D1;
- 7/7 assets were delivered through the governed Pages Function;
- 7/7 delivered bytes matched D1-registered SHA-256 values;
- active ONE references were cut over to stable `asset_code` delivery URLs;
- post-switch audit found zero active references to the seven GitHub rollback binaries;
- rollback binaries were removed only after delivery verification;
- post-removal delivery still passed 7/7;
- the canonical Doré Original Library 001–241 was explicitly excluded.

Canonical disposition remains exactly as already recorded in `CW-011` and the Master Register: `VERIFIED_COMPLETE` for this bounded migration/runtime cutover; ONE itself remains `MAINTENANCE`.

### 2. Priority-B shared site-media R2 cutover is also a separate bounded `VERIFIED_COMPLETE` milestone

The Priority-B milestone is not merely a plan. It records five concrete large site assets migrated to private R2 + D1 with runtime cutover through the governed site-delivery route:

- `SITE-BACKGROUND`
- `SITE-DAMASCUS-GATE`
- `SITE-JERUSALEM-WALL`
- `SITE-TEMPLE-STONE-LIGHT`
- `SITE-WECHAT-QR`

The milestone explicitly preserves the placement boundary: code/UI/version-coupled brand vectors and small atomic fixtures stay in GitHub; content/media binaries move only when governed delivery and safe removal are proven. The canonical Doré 241 source library was not touched.

Current classification: `VERIFIED_COMPLETE` for this bounded five-asset site-media cutover. It should not be inflated into “all Journal/Library media migrated” or “all assets belong in R2.” The Master Register's current JOIN row already reflects the relevant production consequence, so no row-status change is required.

### 3. Durable capability retained from the two R2 milestones

The reusable architectural lesson is now clear and should govern future migrations:

`stable asset_code identity -> D1 locator/hash/metadata -> private R2 binary -> controlled product-facing Pages delivery -> runtime verification -> only then remove redundant GitHub binary`

Additional retained boundary:

- media placement is semantic, not ideological;
- large content/runtime media may belong in R2;
- code/UI-coupled identity assets may correctly remain GitHub-owned;
- source-locked libraries must not be swept into unrelated migration work;
- production delivery and byte-integrity evidence are stronger than storage-presence claims.

This capability is reusable for Journal and Liming Library media, but those later migrations remain separate work and require their own evidence.

### 4. Search Runtime Consolidation is a legitimate historical completion, but now a revisit-context milestone rather than current architecture completion

`SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md` records a bounded PASS: it introduced one shared browser submit lifecycle (`dore:search-query`) while deliberately preserving the existing Scripture Search/router implementation and moving entity context onto the shared event surface.

For its original objective, this is a valid historical completion:

- one supplemental browser lifecycle was established;
- entity search stopped owning an independent submit hook;
- existing Scripture/reference/original-language/chapter/Brain paths were intentionally preserved;
- the document explicitly deferred service-layer replacement to a later milestone.

However, Sweep checkpoint 19 later found architectural duplication between the browser Search intelligence and `dore_core.search.BibleSearchIndex`. Therefore this 2026-08-24 PASS must not be read as current Search-architecture completion.

Current classification for the historical runtime-consolidation milestone: `COMPLETED_REVISIT_CANDIDATE` in the context of `RQ-003`, while the live `SEARCH` workstream correctly remains `MAINTENANCE + DISCOVERY`.

The revisit trigger has already fired conceptually: future Search-quality/service work should converge on one canonical execution/specification boundary and prove parity/regressions rather than add more independent browser retrieval logic.

### 5. No supersession/retirement action is justified for the delivery routes

The reviewed evidence does not show that either `/api/dore/assets/file?code=...` or `/api/dore/assets/site-file?code=...` has been superseded or should be retired. They remain historical/current governed delivery surfaces unless later runtime evidence says otherwise.

Likewise, the shared browser event lifecycle is not itself proven harmful; the debt is duplication of search intelligence, not the existence of a coordination event.

## Canonical register reconciliation

No status correction is required in the current Master Register from this batch:

- `ONE = MAINTENANCE` remains correct and already names the verified Priority-A private-R2 cutover;
- `JOIN = MAINTENANCE` remains correct and already names the Priority-B site-media cutover consequence;
- `SEARCH = MAINTENANCE + DISCOVERY` remains correct and already carries the later cognition/service-boundary debt;
- `MEM-SWEEP-01 = ACTIVE_PARALLEL` remains correct.

The useful new consolidation is therefore historical classification and capability retention, not a live workstream promotion/demotion.

## Completed-work / revisit interpretation

- Priority-A ONE migration/runtime cutover: keep `VERIFIED_COMPLETE` (`CW-011`).
- Priority-B five-asset site-media cutover: `VERIFIED_COMPLETE` bounded milestone; candidate for a future dedicated completed-work entry if the main ledger is normalized by migration family.
- Search Runtime Consolidation 2026-08-24: `COMPLETED_REVISIT_CANDIDATE` because its original coordination goal was achieved, while later architecture evidence exposed service-boundary duplication.

## Missing evidence / future proof

No new blocker is created by this batch. Future related proof should be attached to the later workstreams rather than reopening the old migration milestones:

- Journal/Liming media: governed inventory -> placement decision -> R2+D1 migration -> runtime/byte verification -> safe cleanup;
- Search: canonical service-boundary convergence + parity/regression evidence across the existing reference/fuzzy/original-language/entity routes.

## P01 isolation

This Sweep batch did not resume, pause, reorder, deploy, bind, or otherwise modify P01. The existing subtitle critical-path environment dependency is unchanged.
