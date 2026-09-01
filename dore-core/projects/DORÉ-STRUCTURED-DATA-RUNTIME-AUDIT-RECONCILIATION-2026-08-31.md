# Doré Structured Data Runtime Audit Reconciliation — 2026-08-31

Status: SWEEP_01_BOUNDED_EVIDENCE
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

## Bounded evidence reviewed

- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`
- `dore-core/projects/DORÉ-CLOUDFLARE-JOURNAL-LIMING-PLACEMENT-EVIDENCE-LEDGER-2026-08-30.md`
- `dore-core/projects/DORÉ-CLOUDFLARE-MILESTONE-CHAIN-EVIDENCE-LEDGER-2026-08-30.md`
- current `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md` Checkpoint 25 interpretation
- current `DORÉ-MASTER-WORK-REGISTER.md` MEM-SWEEP-01 interpretation

## Contradiction resolved

Checkpoint 25 and the current Master Register say the named structured data-runtime follow-on audit was not found and therefore classify that follow-on as `UNKNOWN_NEEDS_EVIDENCE / POSSIBLY_SUPERSEDED_IN_PART`.

That statement is now superseded by stronger direct evidence. `dore-core/cloudflare/STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md` exists and explicitly records `Status: COMPLETE / PASS`. It audits the active Search/Brain structured datasets and records placement decisions rather than a destructive migration.

The later `DORÉ-CLOUDFLARE-MILESTONE-CHAIN-EVIDENCE-LEDGER-2026-08-30.md` independently reconstructs the same chronology and correctly classifies the structured data-runtime audit as `VERIFIED_COMPLETE` for placement/governance.

## Verified bounded milestone

Classification: `VERIFIED_COMPLETE` for the declared structured-data placement/governance audit.

The audit explicitly keeps:

- `static/dore/search-index.json` on Pages for the working browser Search runtime;
- `static/dore/original-index.json` on Pages;
- `static/dore/entity-index.json` on Pages;
- Doré Brain/status snapshots on GitHub/Pages;
- Liming Library and Journal versioned YAML/JSON in GitHub;
- D1 for mutable/queryable registry and operational state;
- R2 for independently addressable media/content objects.

It rejects moving 10 MB-class browser indexes to R2 or D1 merely because they are large. The decision is based on access pattern, mutability, build atomicity, runtime dependency and operational risk.

## Retrospective evaluation

**Original objective:** decide whether Search/corpus/Brain structured datasets should move after the GitHub + Cloudflare reorganization without breaking the already-working Search product.

**Completion evidence:** the named audit itself records `COMPLETE / PASS`, enumerates the production datasets and consumers, makes explicit placement decisions, defines D1/R2/GitHub/Pages boundaries, and carries regression requirements forward to Search Runtime Consolidation.

**Current quality:** strong placement-governance milestone. The decision remains coherent with later architecture: deterministic/versioned browser snapshots remain with the build/runtime that directly consumes them; mutable/queryable state belongs in D1; media belongs in R2. Later Search service-boundary duplication is a separate revisit issue and does not invalidate the storage audit.

**Durable learning:** storage placement follows workload semantics, not file size or provider availability. A zero-migration or keep-in-place decision can be the correct verified outcome.

**Weakness/debt:** the Sweep checkpoint and Master Register retained an outdated “audit not found” statement after the later evidence-ledger pass had already found the audit. This is memory-reconciliation debt, not infrastructure debt.

**Revisit trigger:** reopen only if Search delivery architecture materially changes, browser indexes become operationally burdensome, repository/build constraints change, or a canonical service boundary replaces direct browser snapshot loading.

**Disposition:** keep the 2026-08-24 audit historically closed as `VERIFIED_COMPLETE`; maintain later Search/service-boundary revisit separately; do not create a new structured-data migration task from the stale checkpoint wording.

## P01 boundary

No P01 subtitle runtime, deployment, credential, binding, job state, ordering or blocker condition was changed by this reconciliation.
