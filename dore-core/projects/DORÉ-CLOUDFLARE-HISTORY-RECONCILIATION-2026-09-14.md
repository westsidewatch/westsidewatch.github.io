# DORÉ CLOUDFLARE HISTORY RECONCILIATION — 2026-09-14

Status: SWEEP-01 EVIDENCE LEDGER
Scope: bounded historical reconciliation of early Cloudflare service/asset work. This document does not alter or interrupt P01.

## Evidence reviewed

- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/ASSET-MIGRATION-MILESTONE-PLAN-2026-08-24.md`
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/` inventory listing as of 2026-09-14
- current canonical architecture/status interpretation in `DORÉ-MASTER-WORK-REGISTER.md`

## CH-001 — Doré product-neutral service-layer milestone

**Historical classification:** `VERIFIED_COMPLETE` for the bounded 2026-08-24 architectural milestone.

**Original objective**
Create a stable product-neutral entry contract at `/api/dore/query` with a common response envelope and server-side intent routing across Scripture, Brain, Asset Registry and Status, while preserving the already-proven browser Scripture engine instead of prematurely rewriting it.

**Completion evidence**
The milestone document explicitly records `COMPLETE / PASS`, a concrete `dore.query.v1` contract, GET/POST request forms, lane classification, response-envelope fields, explicit delegation behavior and compatibility boundaries.

**Current quality judgment**
The historical milestone is valid and architecturally disciplined for its time: it preferred non-destructive delegation over a risky server rewrite and established a cross-product service boundary. However, the current Doré architecture has since accumulated Capability Registry/Runtime, A2A/control-plane work, Reflex projection and shared Source Capability layers. Therefore the older claim that `/api/dore/query` is the single stable entry contract should no longer be treated as self-evidently governing without fresh production evidence.

**Current disposition**
`COMPLETED_REVISIT_CANDIDATE` for service-boundary reconciliation, not because the historical work failed, but because later architecture may have superseded part of its role. Do not remove the endpoint merely from architectural age. Future reconciliation should determine whether it remains a compatibility facade, is actively consumed by products, should delegate into Capability Runtime, or has already become dead/legacy surface.

**Revisit trigger**
Any service-boundary consolidation, removal of duplicated routing, or new cross-product client should prove current `/api/dore/query` production consumption before changing it.

## CH-002 — Priority-A R2/D1 asset migration milestone

**Historical classification:** `VERIFIED_COMPLETE` for the declared migration milestone.

**Original objective**
Move selected canonical/priority binary media into governed R2 storage with D1 registry verification without deleting GitHub sources before a verified replacement/runtime path existed.

**Completion evidence**
The closure document records Batch 001 Matthew 3 canonical motion PASS, Batch 002 Priority ONE media PASS, `7/7` migrated or deduplicated in R2 and `7/7` D1/search verified, removal/exclusion of obsolete revisions, and zero unresolved Priority-A items. It also names receipt files under `dore-core/cloudflare/receipts/`.

**Current quality judgment**
Strong bounded migration evidence. The important retained lesson is the authority rule: migration is not complete merely because objects exist in R2; runtime delivery and canonical identity must be verified before deleting rollback/source copies. The 2026-08-24 closure explicitly left seven GitHub source copies for rollback/runtime compatibility until R2-backed public delivery switched on.

**Current disposition**
Keep the migration milestone closed as `VERIFIED_COMPLETE`. Separately mark **post-migration source-copy retirement as `UNKNOWN_NEEDS_EVIDENCE`** until current runtime/reference evidence proves whether those seven retained copies were later switched away from and safely removed, intentionally retained, or superseded by later Source Capability architecture.

**Revisit trigger**
Storage/runtime consolidation, duplicate-binary cleanup, or a product delivery regression should re-open only the post-migration delivery/retirement question, not the original migration milestone.

## CH-003 — Journal + Liming zero-migration audit

**Historical classification:** `VERIFIED_COMPLETE` for the bounded placement audit and zero-migration decision.

**Original objective**
Audit current Journal and Liming Library material and migrate only eligible binary media, while preserving structured versioned editorial/resource data in GitHub.

**Completion evidence**
The milestone records that Journal had no local binary collection to migrate, `data/volumes/vol-00.yaml` remained GitHub editorial/build data, Liming `data/resources.json` remained structured versioned source data, eligible binaries were `0`, and therefore R2 writes, D1 rows and GitHub removals were all `0`.

**Current quality judgment**
This is a legitimate completion, not a skipped task. It demonstrates an important storage-governance principle: existence of R2 is not itself a reason to move reviewable JSON/YAML or create competing masters. The result should not be misread as proof that later Journal/Library media never required ingestion; it only verifies the audited 2026-08-24 state.

**Current disposition**
Keep closed as `VERIFIED_COMPLETE`. Treat later Journal/Library ingestion and Source Capability work as separate workstreams rather than reopening this audit.

## Durable capability retention

This historical Cloudflare batch contributed reusable principles that remain valid across later Doré architecture:

1. **Non-destructive migration:** establish replacement + verification before deleting an existing source/runtime path.
2. **One canonical truth:** avoid GitHub/R2 competing masters.
3. **Placement by access/authority semantics, not fashion:** versioned JSON/YAML can correctly remain in GitHub even when object storage exists.
4. **Compatibility facade discipline:** a service boundary may delegate to proven subsystems instead of rewriting them.
5. **Historical completion is distinct from present architecture:** later Capability/Source/Reflex layers can create a revisit need without invalidating the original milestone.

## Missing-evidence item introduced by this reconciliation

**CF-ME-001 — post-migration runtime delivery/source-copy retirement**

The 2026-08-24 migration closure explicitly says seven GitHub source copies remained for rollback/runtime compatibility until R2-backed public delivery was switched on. This bounded sweep batch did not find decisive current evidence proving the later disposition of those copies. Required future proof is small: enumerate the seven retained paths from the migration inventory/receipts, resolve current product references for each, and classify each as active canonical source, rollback-only retained copy, safely retired copy, or superseded by later Source Capability/projection behavior.

No human decision is required by this finding, and no P01 action is changed.