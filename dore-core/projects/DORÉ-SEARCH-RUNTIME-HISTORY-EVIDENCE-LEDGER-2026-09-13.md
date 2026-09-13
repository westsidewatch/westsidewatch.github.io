# DORÉ SEARCH RUNTIME HISTORY EVIDENCE LEDGER — 2026-09-13

Status: DURABLE / SWEEP-01 EVIDENCE
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Evidence reviewed

- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`;
- `dore-core/cloudflare/STRUCTURED-DATA-RUNTIME-AUDIT-2026-08-24.md`;
- `dore-core/cloudflare/SEARCH-RUNTIME-CONSOLIDATION-2026-08-24.md`;
- current `static/dore/dore-search-runtime.js`;
- current `static/dore/dore-entity-search.js`;
- current `static/dore/dore-search.js`;
- canonical `RQ-003` Search revisit interpretation.

## Historical milestones

### 1. Journal + Liming media placement audit

**Classification:** `VERIFIED_COMPLETE` for the bounded 2026-08-24 placement milestone.

The milestone correctly concluded that there were zero eligible local Journal/Liming binary-media objects to migrate at that point. `data/volumes/vol-00.yaml` and `data/resources.json` were retained in GitHub because they were structured, reviewable source/editorial data rather than media blobs. This was an intentional zero-migration PASS, not skipped work.

**Current judgment:** the placement principle remains sound. The historical inventory counts are not a statement about the present Dawn Library or Journal media footprint; later product evolution must be read from current ledgers/runtime evidence.

### 2. Structured data runtime placement audit

**Classification:** `VERIFIED_COMPLETE` for the bounded placement/governance decision.

The audit correctly separated three storage roles:

- GitHub/Pages for deterministic, versioned browser/runtime indexes and editorial source data;
- D1 for mutable/queryable registry and operational state;
- R2 for independently addressable large media/content objects.

It explicitly refused to move large JSON snapshots merely for storage aesthetics and preserved the then-working Browser Search contract.

**Current judgment:** retain this as durable placement doctrine, but do not treat the 2026 file sizes or exact browser topology as current architecture evidence.

### 3. Search Runtime Consolidation

**Historical classification:** `VERIFIED_COMPLETE` for the bounded 2026-08-24 browser-lifecycle milestone.

The milestone introduced `static/dore/dore-search-runtime.js` as a shared supplemental lifecycle, with a `dore:search-query` event intended to let `dore-entity-search.js` subscribe without owning a separate form-submit hook. It deliberately preserved the existing Scripture-search engine.

## Current drift finding

The historical completion is valid, but its original extension contract is no longer demonstrably current.

Current `static/dore/dore-search-runtime.js` is version `7.2.0` and is now primarily a conversation/runtime bridge: local conversation health/chat/history, mode switching, persisted conversation IDs, and conversation UI. In the reviewed current file, no `dore:search-query` dispatch exists.

Current `static/dore/dore-entity-search.js`, however, still binds only to:

`window.addEventListener('dore:search-query', handler, false)`

Current `static/dore/dore-search.js` contains no reviewed `dispatchEvent` occurrence that restores this contract.

Therefore the old Search Runtime Consolidation milestone should remain historically complete, while the **current entity-context integration path is a drift / missing-regression-evidence condition**. The reviewed evidence does not justify claiming that entity context still activates in current production Search.

## Classification and disposition

- 2026 Journal/Liming zero-migration milestone: `VERIFIED_COMPLETE` historical placement milestone.
- 2026 Structured Data Runtime Audit: `VERIFIED_COMPLETE` historical placement/governance milestone.
- 2026 Search Runtime Consolidation: `VERIFIED_COMPLETE` historical browser-lifecycle milestone.
- Original `dore:search-query` extension contract as current production truth: `SUPERSEDED / DRIFTED` unless re-established by current runtime evidence.
- Entity-context activation in current Search: `UNKNOWN_NEEDS_EVIDENCE` and part of the already-triggered `RQ-003` Search revisit.

## Smallest future proof

Without interrupting P01, Search maintenance should later execute one real current Search probe using a known entity such as `摩西`, verify whether the entity card is actually injected, and then either:

1. restore a single canonical current query-event dispatch in the runtime; or
2. move entity augmentation onto the newer canonical Search/Core execution boundary.

Whichever path is chosen must add a regression test proving that entity augmentation is active while normal Scripture Search results remain intact.

## P01 protection

No P01 state, deployment, credential, binding, subtitle source order, media acquisition, transcription path, or runtime action was modified by this reconciliation.
