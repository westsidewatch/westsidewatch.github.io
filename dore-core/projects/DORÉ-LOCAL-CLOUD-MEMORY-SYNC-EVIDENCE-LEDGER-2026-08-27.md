# DORÉ LOCAL ↔ CLOUD MEMORY SYNC — EVIDENCE LEDGER

Date: 2026-08-27
Status: ACTIVE / UNKNOWN_NEEDS_EVIDENCE
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`

## Bounded evidence reviewed

- commit `3e12f96302da35c04fe386ee9416eef2e829d818` — authenticated local-to-cloud memory sync endpoint;
- commit `372a4423ff0949264c25ace58273e5a3fb95475d` — local push + bidirectional sync client;
- follow-up commits `1d974115822d1d75a15166337679a419625a805c`, `dc4cc6ddbb95d631f6597427275ebb2a99b2c855`, `bcd783bbc0793508ed1a45d3622088f1645fc64e`, `108abc5e692675e9edc5d3db2530d846cc96d448` — readiness exposure, compatibility alias, probe logic and deployment trigger.

## Current classification

`ACTIVE / UNKNOWN_NEEDS_EVIDENCE` as a memory-continuity extension nested under the existing Doré CORE/RUNTIME/Conversation-Memory architecture. The reviewed evidence does not yet justify a separate top-level product classification.

## What is implemented

1. Cloud endpoint accepts authenticated batches through `DORE_CLOUD_SYNC_TOKEN`.
2. Server-side writes require both `DORE_SENSORY` and `DORE_MEMORY_ARCHIVE`.
3. Records are archived to R2 before D1 insertion.
4. Message identity is hash-checked; exact duplicates are deduplicated and non-identical ID collisions use an explicit `cloud-wins` conflict policy.
5. Local client can pull cloud memory, select local unsynced rows, push them to cloud, persist a local sync log, and run both directions in one invocation.
6. The implementation explicitly records `workers_ai_used:false`; this is transport/storage continuity, not semantic-memory evaluation.

## Evidence boundary

Repository implementation and deployment-trigger commits are real, but this batch found no persisted production proof of a successful end-to-end bidirectional cycle showing:

`local row → authenticated cloud endpoint → R2 archive + D1 insert → later cloud pull → same canonical record locally`

Nor is there persisted evidence yet for:

- conflict-policy behavior on a deliberate same-ID/different-content fixture;
- project/conversation isolation across two scopes;
- replay after local state loss or reinstall;
- rollback/recovery after a partial failure between R2 and D1;
- token rotation/revocation behavior;
- convergence under repeated push/pull cycles without duplicate amplification.

## Current quality judgment

The architecture is materially stronger than one-way import because it adds authenticated writes, idempotence, explicit conflict handling and dual persistence. However, it is too early to call the sync milestone complete. The critical missing evidence is operational convergence, not more code.

## Smallest next proof

Run one bounded production-safe fixture with two projects and two conversations that proves:

1. one local-only message is pushed and independently visible in R2 + D1;
2. one cloud-only message is pulled locally;
3. repeating the cycle creates no duplicate;
4. one deliberate same-ID/different-content case returns `conflict` and preserves cloud-wins semantics;
5. no record crosses project/conversation boundaries.

Persist the result as machine-readable evidence before any `VERIFIED_COMPLETE` promotion.

## Disposition

Keep active and evidence-gated. Do not treat deployment/readiness commits as completion. Do not modify or interrupt P01 subtitle execution.