# DORÉ CLOUDFLARE R2 ASSET + SERVICE HISTORY — EVIDENCE LEDGER

Date: 2026-09-12
Status: SWEEP-01 / BOUNDED RECONCILIATION
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Scope

This ledger reconciles the early `dore-core/cloudflare/` migration/service milestone family against later durable receipts and current repository implementation. It is historical classification work only. It does not change, resume, replace, or interrupt P01.

Evidence reviewed:

- `dore-core/cloudflare/ASSET-MIGRATION-INVENTORY-2026-08-24.md`
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/receipts/ASSET-MIGRATION-PRIORITY-ONE-RESULT.json`
- `dore-core/cloudflare/receipts/R2-DELIVERY-MILESTONE-PASS.json`
- `dore-core/cloudflare/receipts/R2-POST-DELIVERY-CLEANUP-RESULT.json`
- `dore-core/cloudflare/receipts/R2-PRIORITY-B-SITE-MEDIA-PASS.json`
- current `functions/api/dore/query.js`
- current Master Register ONE/JOIN interpretations.

## Finding 1 — Priority-A asset migration is a completed historical milestone

**Classification:** `VERIFIED_COMPLETE / COMPONENT`.

The early inventory correctly records the first governed migration milestone as 7 Priority-A canonical ONE assets migrated/registered into R2 + D1, with 0 unresolved Priority-A items. That was not the end state, but the milestone itself is legitimate historical completion.

Later receipts strengthen rather than contradict that completion: `R2-DELIVERY-MILESTONE-PASS.json` records `status=PASS`, `asset_count=7`, a content hash for each governed asset, `one_page_http_pass=true`, and no requirement for public R2 exposure because delivery is private/registry mediated.

## Finding 2 — the inventory's “runtime delivery not yet switched” statement is superseded

**Classification of the old statement:** `SUPERSEDED` as current-state guidance; retain only as historical provenance.

`ASSET-MIGRATION-INVENTORY-2026-08-24.md` says the seven GitHub copies were retained because runtime delivery had not yet switched to an R2-backed layer and names R2-backed delivery as the next milestone.

That statement was true at the inventory checkpoint but is no longer current. `R2-DELIVERY-MILESTONE-PASS.json` proves the seven assets were delivered through the governed private R2 path, and `R2-POST-DELIVERY-CLEANUP-RESULT.json` records:

- `status=PASS`;
- `active_github_reference_count=0`;
- `github_binaries_removed=7`;
- `r2_delivery_post_cleanup_verified=7`;
- canonical Doré 241 originals untouched.

Therefore the rollback-copy phase is closed for this Priority-A set.

## Finding 3 — Priority B is no longer deferred

**Classification:** `VERIFIED_COMPLETE / COMPONENT` for the five-asset site-media cutover.

The early inventory's `PRIORITY B — DEFERRED BY DESIGN` section is also a superseded current-state snapshot. `R2-PRIORITY-B-SITE-MEDIA-PASS.json` records:

- `milestone=priority-b-site-media`;
- `status=PASS`;
- `asset_count=5`;
- `runtime_cutover=registry-private-r2`;
- `github_binaries_removed=5`;
- `r2_delivery_verified=5`;
- brand SVG policy remains `KEEP_IN_GITHUB`;
- canonical Doré 241 originals untouched.

The current Master Register already reflects this later truth in the JOIN row, which states that its background and WeChat QR are actively delivered through the verified Priority-B five-asset private-R2 cutover. No separate active migration queue should be recreated from the older inventory text.

## Finding 4 — current placement policy is differentiated, not “move everything to R2”

The completed migration taught a durable placement rule:

- governed large/runtime media can use registry-mediated private R2 delivery;
- code/UI identity SVGs may remain in GitHub when atomic versioning with code is the stronger invariant;
- canonical Doré 241 originals were explicitly protected from this cleanup;
- removal from GitHub followed verified delivery and active-reference audit rather than preceding it.

This is a reusable infrastructure capability, not merely a one-time storage cleanup.

## Finding 5 — Doré service-layer milestone remains a valid bounded completion

**Classification:** `VERIFIED_COMPLETE / COMPONENT`, with later architecture evolution expected.

`DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md` declared the product-neutral `/api/dore/query` contract complete under schema `dore.query.v1`, with routing among scripture, brain, asset and status lanes while intentionally preserving the proven browser Scripture engine.

The current `functions/api/dore/query.js` still exposes `schema:'dore.query.v1'`, retains GET/POST query handling, performs the same lane classification/delegation model, sends asset queries to `/api/dore/assets/search`, status to the status snapshot, brain matches to the Doré knowledge index, and Scripture to the browser search dataset. The historical milestone therefore has current implementation continuity rather than being a memo-only claim.

This does not imply that `dore.query.v1` is the final Doré execution architecture. A2A, Living Retrieval, capability registry and later execution-plane work extend the system. The correct interpretation is “bounded service-contract milestone completed and still present,” not “all Doré services complete.”

## Completed-work evaluation

### Original objective
Create a governed binary-storage/delivery foundation and one stable product-neutral Doré service boundary without regressing existing product behavior.

### Completion evidence
Priority-A migration receipt + seven-asset delivery PASS + post-delivery cleanup PASS + five-asset Priority-B PASS + surviving `dore.query.v1` endpoint implementation.

### Current quality
Strong for the declared bounded milestones. Evidence includes machine-readable receipts, hash-bearing delivery verification, post-cutover cleanup checks and current executable service code. It is not global proof of every R2 asset family or every modern Doré execution path.

### Durable learning retained
- storage migration is incomplete until delivery is verified;
- cleanup follows cutover/readback, never precedes it;
- registry identity/provenance/hash should govern binaries independently of physical storage;
- code-coupled identity assets can legitimately stay in GitHub;
- one stable service envelope may preserve proven specialized engines rather than forcing premature rewrites.

### Weaknesses / debt
- early inventory prose is now stale if read as current state;
- later R2/media families may require their own regression and rights/provenance checks;
- `dore.query.v1` is intentionally simple and should not be mistaken for the later full A2A/capability execution plane;
- this batch does not independently live-probe production endpoints or R2 objects in 2026-09-12 runtime.

### Revisit trigger
Reopen only if registry/private-R2 delivery regresses, storage policy changes, current products reintroduce duplicate GitHub masters, hash/provenance drift appears, or `dore.query.v1` is intentionally deprecated/replaced by a new canonical public service boundary.

### Disposition
Keep Priority-A migration, Priority-A delivery/cutover cleanup, Priority-B five-asset cutover, and the bounded `dore.query.v1` service-layer milestone closed as historical component completions. Treat the early “delivery pending” and “Priority B deferred” prose as superseded snapshots, not active work.

## Canonical reconciliation

The Master Register's current ONE and JOIN rows already encode the later R2 truth, so their product statuses do not require promotion. The useful Sweep correction is historical: do not regenerate obsolete migration work from the 2026-08-24 inventory, and preserve the receipts as the governing completion evidence for those bounded migrations.

Sweep 01 remains `ACTIVE_PARALLEL`. This batch does not justify Sweep-wide `VERIFIED_COMPLETE`.