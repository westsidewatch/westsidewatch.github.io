# Doré Cloudflare Service + Asset Migration Evidence Ledger — 2026-09-14

Status: BOUNDED_RECONCILIATION
Sweep: DORÉ MEMORY CONSOLIDATION SWEEP 01

## Evidence reviewed

- `dore-core/cloudflare/ASSET-MIGRATION-INVENTORY-2026-08-24.md`
- `dore-core/cloudflare/receipts/ASSET-MIGRATION-PRIORITY-ONE-RESULT.json`
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- current implementation `functions/api/dore/query.js`
- current canonical Master Work Register rows for `ONE`, `JOIN`, `WSS`, `SEARCH`, `RUNTIME`

## 1. Priority-A media migration

Classification: `VERIFIED_COMPLETE` for the original seven-asset migration milestone; later runtime cutover is governed separately by current ONE/asset-delivery evidence.

Original objective:
Move selected canonical ONE media into governed R2+D1 storage without creating competing masters or deleting rollback copies before a delivery path existed.

Completion evidence:
The persisted receipt records `PASS`, `asset_count: 7`, `verified_count: 7`, no error, content hashes, R2 locators and active registry identities for all seven governed assets. The inventory also records zero unresolved Priority-A items and removal of three obsolete Matthew 3 motion revisions.

Current quality judgment:
The migration policy was strong for its time: canonical identity, content hash, provenance, preservation class, rollback safety and a prohibition on silent GitHub/R2 dual-master divergence were all explicit. Its deliberate refusal to delete repository rollback binaries before a first-class R2 delivery path was the correct safety boundary rather than unfinished cleanup.

What was learned / retained:
- storage migration and runtime delivery are distinct milestones;
- successful object copy does not justify source deletion;
- canonical asset identity belongs in a registry, not in incidental repository paths;
- immutable hashes and lifecycle state are durable verification primitives;
- reproducible derivatives are safer cleanup targets than canonical sources.

Historical debt / supersession:
The original inventory's “next milestone” was an R2-backed runtime layer. That next step is no longer merely prospective: the canonical Master Register now records a bounded verified Priority-A ONE private-R2 runtime cutover and a Priority-B five-asset site-media cutover for JOIN. Therefore the 2026-08-24 inventory must be read as historical migration provenance, not as the current live-state description.

Current disposition:
Keep as `VERIFIED_COMPLETE` historical milestone. Do not reopen migration itself unless registry/hash/delivery regression appears. Runtime-delivery maintenance belongs to current ONE/JOIN stewardship.

## 2. Doré product-neutral service layer (`dore.query.v1`)

Classification: `VERIFIED_COMPLETE` as a bounded architecture/implementation milestone; not evidence that every product has completed live end-to-end adoption.

Original objective:
Expose one product-neutral Doré query contract at `/api/dore/query` while preserving the proven browser Scripture engine and delegating Brain, Asset Registry and Status through explicit boundaries.

Completion evidence:
`functions/api/dore/query.js` exists and currently implements the claimed `dore.query.v1` envelope, GET/POST query handling, auto classification into `scripture`, `brain`, `asset`, and `status`, provenance/boundary fields, Brain matching, Asset/Status delegation and Scripture delegation with protected capability metadata.

Current quality judgment:
The milestone remains architecturally sound as a compatibility boundary. It avoided a risky server-side Scripture rewrite and gave products a stable Doré entry contract. However the implementation still delegates Scripture to the browser dataset and uses compact rule-based intent classification/Brain matching. It should therefore be treated as a routing/service contract, not as proof of unified Search cognition or universal semantic quality.

What was learned / retained:
- shared service contracts can unify products without prematurely centralizing every engine;
- compatibility-preserving delegation is preferable to rewrites that risk regression;
- provenance and epistemic boundary fields belong in the service envelope;
- service-layer completion and consumer-product end-to-end proof are separate claims.

Weakness / revisit trigger:
Revisit only when a real consumer need demands stronger server-side cognition, when Search/Core convergence establishes a new canonical execution boundary, or when a regression proves the current delegation model insufficient. Do not reopen merely because newer architecture exists.

Current disposition:
Retain as bounded `VERIFIED_COMPLETE` infrastructure history. Keep consumer-specific live proof under their own workstreams (for example WSS packaged-app proof and Search cognition/service-boundary convergence).

## Register reconciliation

No canonical status promotion is warranted in this batch. The current Master Register already reflects the later state correctly:

- `ONE` records the bounded verified Priority-A R2 runtime cutover rather than stopping at migration-only evidence;
- `JOIN` records the later Priority-B private-R2 site-media cutover;
- `WSS` remains `ACTIVE_PARALLEL` because repository wiring is not equivalent to packaged live end-to-end proof;
- `SEARCH` remains `MAINTENANCE + DISCOVERY`, so the presence of `dore.query.v1` must not be inflated into Search cognition completion.

This ledger closes the historical interpretation gap: the August 24 migration and service-layer memos are legitimate completed components, but their successor work belongs to current runtime/product rows rather than reappearing as active standalone projects.

## P01 safety

No P01 state, runtime, deployment, subtitle, audio or transcription action was taken in this reconciliation.
