# DORÉ CLOUDFLARE CONNECTION + ASSET REGISTRY HISTORY — EVIDENCE LEDGER — 2026-09-13

Status: COMPLETE / BOUNDED HISTORICAL RECONCILIATION
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Evidence reviewed

- `dore-core/cloudflare/CLOUDFLARE-CONNECTION-CHECKPOINT-2026-08-24.md`
- `dore-core/cloudflare/asset-registry-schema-v1.sql`
- current `functions/api/dore/assets/` implementation family
- current canonical Master Register interpretations for ONE, JOIN, Dawn and Cloudflare-backed asset delivery
- Checkpoints 92–98 Cloudflare/runtime/storage reconciliations

## Historical completion

The 2026-08-24 Cloudflare Connection Checkpoint is a legitimate bounded `VERIFIED_COMPLETE` infrastructure milestone. It recorded a production D1 + R2 round trip through the first-party Pages Function with successful write, D1 registration, R2 read, SHA-256 verification, registry verification, cleanup in both stores and zero residue. That proves the foundational operational chain rather than merely documenting desired bindings.

The accompanying Asset Registry schema is also substantive architecture, not placeholder text. It defines canonical asset identity and metadata across GitHub/R2, including content hashes, provenance, rights/license fields, preservation classes, lifecycle state, product usage relationships, review state, usage records and a maintenance queue.

## Current reconciliation

Current `functions/api/dore/assets/` still contains the health, roundtrip, migration, file-delivery and search endpoint family, while later persisted milestones independently prove real ONE and shared-site private-R2 cutovers. Therefore the original connection milestone remains valid historical infrastructure provenance.

However, the 2026-08-24 checkpoint's "next phase" list must not be treated as unfinished merely because it is written as future tense. Several listed capabilities were subsequently implemented or exercised in bounded product cutovers. Conversely, the existence of schema tables and endpoint files does not by itself prove that every present asset family, Dawn cover, Journal media object or future generated visual asset is fully registered with current rights/provenance/usage relationships.

## Classification

- D1 + R2 production connection / disposable round-trip milestone: `VERIFIED_COMPLETE / COMPONENT`.
- Asset Registry schema v1: `VERIFIED_COMPLETE / ARCHITECTURE FOUNDATION`, with current coverage remaining a maintenance/evidence question rather than a schema-completion question.
- historical "next phase" checklist as one unresolved project: `SUPERSEDED` by later granular product/runtime milestones; do not reopen it wholesale.
- current whole-ecosystem Asset Registry coverage/parity: `UNKNOWN_NEEDS_EVIDENCE` unless supported by bounded inventory/runtime checks.

## Retrospective evaluation

**Original objective** — prove that GitHub code could safely drive production Pages → R2 → D1 asset registration and verification without residue, then establish a governed asset metadata model.

**Completion evidence** — production round-trip PASS recorded with hash and registry verification plus zero-residue cleanup; production schema persisted; later private-R2 cutovers prove the foundation was reusable.

**Current quality** — strong separation of binary storage from governed metadata and unusually good preservation/rights/use-state fields for an early milestone. The weakness is not the schema design but the absence, in this bounded batch, of one current ecosystem-wide coverage acceptance proving all relevant live asset families conform.

**Durable learning** — storage connectivity and storage governance are separate claims. A successful R2/D1 round trip proves infrastructure; asset-registry coverage must be proven per live asset family. Temporary proof endpoints may remain as maintenance diagnostics without becoming the canonical product surface.

**Revisit trigger** — only when a live asset lacks traceable canonical identity/hash/provenance/rights, competing masters appear, registry schema no longer represents product needs, or a product bypasses the governed delivery path.

**Disposition** — retain the connection milestone and schema as historical/core infrastructure; do not redesign Cloudflare merely because the original memo is old; evaluate coverage through current product-specific evidence.

## P01 isolation

No P01 state, deployment, credential, binding, source ordering, subtitle job or resume condition was changed by this reconciliation.
