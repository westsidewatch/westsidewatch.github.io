# DORÉ SENSORY MEMORY RUNTIME EVIDENCE LEDGER — 2026-09-14

Status: ACTIVE / SWEEP-01 EVIDENCE
Related: `CORE`, `RUNTIME`, `SEARCH`, `NERVOUS-SYSTEM`, `ME-001`, `ME-008`
Source family: `dore-core/memory/`

## Bounded evidence reviewed

- `dore-core/memory/sensory-active.json`
- `dore-core/memory/sensory-seed-diagnostic.json`
- `dore-core/memory/sensory-heartbeat-diagnostic.json`
- `dore-core/memory/sensory-claim-step-diagnostic.json`
- `dore-core/memory/actions-probe-diagnostic.json`

## Strong evidence

1. A real sensory signal (`5cf2c608-e66f-4176-a3f8-b3284819158a`, query `馬利亞有幾位?`) is durably `CONSOLIDATED` with brain node `research.nt.mary-count`.
2. The 2026-09-14 seed diagnostic reached HTTP 200 and returned the existing signal as `CONSOLIDATED`, `deduplicated:true`, `schema_reconciled:true`, with `heard_count:1308`. This is fresh evidence that the deployed seed path still recognizes and reconciles the historical signal rather than creating a duplicate.
3. The 2026-09-14 heartbeat diagnostic returned `ok:true` and `reconciled_consolidated:1`; the claim-step diagnostic records `outcome:"success"`; the latest Actions probe also records `ok:true`.

These facts retain the earlier bounded sensory-loop repair milestone. They are freshness/maintenance evidence, not proof of broad autonomous memory completion.

## New drift / liveness finding

`sensory-active.json` contains three signals that have remained `RESEARCHING` since 2026-08-28 and still have `brain_node:null`:

- `3973e981-e7e2-4e09-b0ef-6ab22ba1544f` — Search-page dialogue question;
- `5a7c7590-004c-4903-9e28-d322c42bec90` — Scripture phrase query;
- `4a2ab8d9-0bc4-4952-8dc2-ba60a8b09ed8` — `初光金` memory test.

The fresh 2026-09-14 heartbeat still reports the first of these as `RESEARCHING`, with `changed:false`; its `last_heard_at` remains 2026-08-27. Therefore successful heartbeat/claim transport must not be interpreted as evidence that queued research is making forward progress.

## Current interpretation

- historical one-signal consolidation / schema-reconciliation repair: bounded `VERIFIED_COMPLETE` component milestone;
- sensory runtime transport / diagnostic freshness: `MAINTENANCE` evidence;
- broad queue liveness, fairness, retry/timeout policy, and heterogeneous-signal completion: `UNKNOWN_NEEDS_EVIDENCE` under existing `ME-001`;
- live product expression of `QUEUED / RESEARCHING` plus eventual learned improvement: still `UNKNOWN_NEEDS_EVIDENCE` under existing `ME-008`.

No new standalone missing-evidence ID is warranted because the new evidence sharpens, rather than replaces, `ME-001` and `ME-008`.

## Smallest useful follow-up

Run a bounded representative sensory batch with explicit maximum-age / retry expectations and persist per-signal transitions (`heard → claimed → researching → consolidated | failed | timed-out`) plus brain-node creation and dedupe counts. A signal that stays `RESEARCHING` beyond the declared bound must become an explicit retry/failure state rather than silently remaining active indefinitely.

Priority: LOW/MEDIUM, subordinate to P01. This is not a HUMAN_DECISION_BLOCKED or ENVIRONMENT_BLOCKED condition.
