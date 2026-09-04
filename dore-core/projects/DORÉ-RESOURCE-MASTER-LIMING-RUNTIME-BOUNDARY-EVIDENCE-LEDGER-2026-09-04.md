# DORÉ RESOURCE MASTER ↔ LIMING RUNTIME BOUNDARY — EVIDENCE LEDGER

Date: 2026-09-04
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Classification: bounded knowledge/product-runtime reconciliation

## Bounded evidence reviewed

- `data/resources.json`
- `data/liming-dore-ingest-seed.json`
- `functions/api/dore/library/resources.js`
- `.github/workflows/dore-liming-ingest.yml`
- canonical `LIBRARY-INGEST` and `MEM-SWEEP-01` interpretation in `DORÉ-MASTER-WORK-REGISTER.md`

## Finding

`data/resources.json` and the newer D1-backed Liming Library resource registry are related but are **not the same layer and should not be treated as a simple migration/replacement pair**.

`data/resources.json` is a static Resource Master / knowledge-and-curation inventory. It records durable editorial doctrine and taxonomy: Scripture-centered resource principles, annual/monthly/weekly/daily curation rhythm, candidate→selection→Three Morning Stars→Spectrum→curated collection→resource card→Dawn Library workflow, categories, source domains, shelves, inventory departments, activation surfaces and recovered historical inventory. Its own text also acknowledges partially restored/editorial states such as books whose detailed editing, URL verification and curation still need recovery.

The D1-backed `liming_resources` / `liming_resource_edges` runtime is a narrower operational registry. It stores individually addressable resources with stable IDs, source URLs, creator/series/type/language, source class, rights status, Morning Stars score, Chinese-access state, lifecycle status, Scripture/topic/product edges, provenance and timestamps. The two current seed records demonstrate this operational shape with link-only David Pawson resources and explicit product relationships.

The ingest workflow targets only `data/liming-dore-ingest-seed.json` and `functions/api/dore/library/resources.js`; it does not ingest `data/resources.json`. Therefore no evidence supports claiming that the static Resource Master has been migrated into D1, that D1 fully represents its inventory/taxonomy, or that `resources.json` can now be retired.

## Current classification

- `data/resources.json`: `CORE/CONTINUOUS` as a static Library knowledge/curation source with historical inventory; **not** the canonical mutable runtime registry.
- D1 `liming_resources` / `liming_resource_edges`: `ACTIVE_PARALLEL` operational runtime under `LIBRARY-INGEST`.
- `data/liming-dore-ingest-seed.json`: `ACTIVE` bounded seed/input artifact for the runtime registry.
- claim "Resource Master migrated to D1": `UNKNOWN_NEEDS_EVIDENCE` / currently unsupported.
- retiring `data/resources.json`: not justified.

## Retrospective evaluation

### Original objective

The Resource Master was designed to organize valuable resources into a reusable truth/learning structure shared by Journal, ONE, church, media and publication. The later D1 work adds machine-addressable ingestion, provenance/rights, relationship edges and lifecycle/query behavior.

### Completion evidence

The static Resource Master exists and is materially populated. The D1 API/schema and authenticated ingest workflow also exist in repository source, and two explicit seed resources are defined.

### Current quality

The two layers are complementary but currently under-integrated. The static file has much richer curation ontology and historical inventory, while the D1 runtime has stronger operational identity/provenance/query semantics. Treating either as the whole Library would lose information from the other.

### Durable learning

A knowledge model and a runtime registry should be separated intentionally: doctrine/taxonomy/editorial rhythm need not be forced wholesale into mutable resource rows, while individually published resources need stable machine-readable runtime identity, rights and provenance. Convergence should happen through explicit mappings/interfaces, not accidental duplication or destructive migration.

### Weakness / debt

There is no persisted parity/mapping artifact showing which Resource Master inventory concepts/items have runtime representations, which remain editorial-only, and which are obsolete. There is also still no persisted successful live `Doré Liming Library Ingest` Actions/readback receipt in the bounded evidence already recorded by the Master Register.

### Revisit trigger

Revisit when the first live ingest/readback proof is persisted, when bulk Library population begins, or before any cleanup/migration that proposes deleting or replacing `data/resources.json`.

### Current disposition

Retain both layers. Keep `LIBRARY-INGEST` active. Do not perform a blanket `resources.json`→D1 migration and do not retire the Resource Master. Before broad population, define a small canonical mapping between Resource Master concepts and D1 runtime fields/edges, then prove it on a bounded sample.

## Master-register effect

The current `LIBRARY-INGEST` status remains correct: repository implementation exists but live ingest/readback completion evidence is still missing. This bounded reconciliation **does not require a status change**. It adds an important interpretation guardrail: the D1 registry is the canonical mutable resource runtime, while `data/resources.json` remains a durable knowledge/curation source unless a later evidence-backed consolidation explicitly supersedes it.

The current `MEM-SWEEP-01` status also remains `ACTIVE_PARALLEL`; this source family is now explicitly accounted for by this ledger.

## P01 boundary

No P01 subtitle runtime, deployment, source order, credential, binding, audio/transcription dependency or blocker state was modified.