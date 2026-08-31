# Doré Cloudflare Service-Layer Evidence Ledger — 2026-08-31

Status: SWEEP-01 BOUNDED RECONCILIATION
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Source sweep: `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`

## Evidence reviewed

- `dore-core/cloudflare/CLOUDFLARE-CONNECTION-CHECKPOINT-2026-08-24.md`
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`
- current canonical Master Work Register interpretation of RUNTIME, P01, ONE, WSS and Cloudflare/service-placement history.

## Finding 1 — D1 + R2 production asset round trip

**Classification:** `VERIFIED_COMPLETE` for the bounded infrastructure/asset-round-trip milestone.

The checkpoint records production bindings `DORE_SENSORY → dore-sensory` and `DORE_ASSETS → westside-assets`, plus a disposable production round trip that completed Pages Function → R2 write → D1 registry write → R2 read → SHA-256 verification → registry verification → R2 cleanup → D1 cleanup with `residue:false` and `clean:true`.

### Current quality judgment

Strong historical completion evidence for connectivity and transactional round-trip behavior because it records a live production path, hash verification and zero-residue cleanup rather than only configuration or deployment. It does **not** prove the whole Asset Registry product, ongoing durability under load, or every later migration.

### Durable capability retained

- production D1/R2 binding verification;
- content-address/hash verification across storage and registry;
- reversible/disposable acceptance testing with cleanup verification;
- separation of infrastructure proof from later product migration claims.

### Revisit trigger

Re-run when bindings, registry schema, storage policy, or delivery architecture changes materially, or if a live asset workflow exposes integrity/residue drift.

### Disposition

Keep the round-trip milestone closed. Treat later registry/migration work as separate workstreams rather than reopening this infrastructure proof.

## Finding 2 — `dore.query.v1` product-neutral service contract

**Classification:** `VERIFIED_COMPLETE` for the bounded architectural service-layer milestone; service quality and downstream consumer integrations remain continuous/active work.

The milestone records `/api/dore/query` with a stable response envelope and intent routing across scripture, brain, asset and status lanes. It explicitly preserved the existing browser Scripture engine instead of rewriting it, delegated Asset and Status to their existing services, and made the service endpoint a product-neutral entry contract for downstream clients.

### Current quality judgment

Legitimate historical completion for the declared non-destructive architecture gate. The contract existed and intentionally avoided a risky Scripture rewrite. However, later Sweep evidence shows Search still has browser/Core duplication and parity/service-boundary debt; therefore this 2026-08-24 service-layer PASS must **not** be inflated into proof that all search intelligence is centralized or that all clients now use one canonical cognition path.

### Durable capability retained

- stable product-neutral Doré service boundary;
- explicit provenance/confidence/boundary response fields;
- compatibility-first migration strategy;
- lane delegation rather than forced premature rewrites;
- reusable external-worker boundary later consumed by WSS/subtitle work.

### Weaknesses / debt visible now

- Scripture remained deliberately browser-backed at this milestone, which was correct then but left later browser/Core search-intelligence duplication to be reconciled;
- architectural endpoint existence is not evidence of universal product adoption or end-to-end cognition quality;
- service-contract stability still needs regression protection when lane implementations evolve.

### Revisit trigger

Revisit when Search service-boundary convergence work begins, when the response schema changes, or when a downstream client needs a capability that would otherwise reintroduce duplicated routing/intelligence.

### Disposition

Keep the 2026-08-24 service-layer milestone closed as historically complete. Carry the browser/Core convergence issue under the existing Search revisit/maintenance work rather than misclassifying the original milestone as failed.

## Sweep reconciliation

These two milestones reinforce, rather than change, the current canonical map:

- Cloudflare connectivity/service-layer work contains real bounded `VERIFIED_COMPLETE` milestones;
- RUNTIME and product services remain active because continuity, consumers and later architecture continue evolving;
- P01 remains untouched and its existing production audio/transcription `ENVIRONMENT_BLOCKED` condition is unchanged;
- no new human action is created by this bounded batch.

This ledger should be linked from future completed-work/capability-retention consolidation when the canonical files are next compacted; it does not justify promoting Sweep 01 to `VERIFIED_COMPLETE`.