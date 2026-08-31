# DORÉ CLOUDFLARE ASSET MIGRATION BATCH LIFECYCLE — EVIDENCE LEDGER

Date: 2026-08-31
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Classification: historical migration evidence reconciliation

## Bounded evidence reviewed

- `dore-core/cloudflare/ASSET-MIGRATION-BATCH-001.json`
- `dore-core/cloudflare/receipts/ASSET-MIGRATION-BATCH-001-PASS.json`
- `dore-core/cloudflare/ASSET-MIGRATION-BATCH-002.json`
- `dore-core/cloudflare/receipts/ASSET-MIGRATION-BATCH-002-RESULT.json`
- `dore-core/cloudflare/receipts/ASSET-MIGRATION-PRIORITY-ONE-RESULT.json`
- `dore-core/cloudflare/receipts/` inventory

## Reconciled chronology

### Batch 001 — Matthew 3 baptism cover motion

The batch specification was initially recorded as `READY_FOR_GOVERNED_MIGRATION` for `ONE-MAT-03-BAPTISM-COVER-MOTION`, with a final-only retention policy and explicit refusal to migrate obsolete r2–r4 revisions.

The later receipt records `PASS` at `2026-08-24T08:48:52.542413+00:00`. The migration action was `dedupe_no_copy`: the SHA-256 was computed, an already-existing active R2/D1 asset record was found, registry search returned exactly one result, and no duplicate binary copy was needed.

Current classification:

- Batch 001 migration milestone: `VERIFIED_COMPLETE` as a bounded asset-migration event.
- `r2`, `r3-mobile`, `r4-mobile`: `RETIRED` obsolete revisions; retain their deletion/history only as provenance.
- `r5-mobile`: retained canonical final revision for the historical milestone.

Durable lesson: governed migration may legitimately complete through content-hash deduplication rather than a fresh copy. `dedupe_no_copy` is success when identity, locator, lifecycle state and registry readback are verified.

### Batch 002 — initial failed attempt versus later priority-one completion

`ASSET-MIGRATION-BATCH-002.json` currently records `PASS` and points to `ASSET-MIGRATION-PRIORITY-ONE-RESULT.json` as its verifying receipt.

However, the earlier receipt `ASSET-MIGRATION-BATCH-002-RESULT.json` records a real failed attempt at `2026-08-24T08:56:43.578782+00:00`: the first asset (`ONE-JUDE-01-MICHAEL-MOSES-STUDIO`) returned HTTP 403 / Cloudflare error 1010 and the batch stopped after one asset.

A later, stronger receipt `ASSET-MIGRATION-PRIORITY-ONE-RESULT.json` records `PASS` at `2026-08-24T09:07:53.854601+00:00`, with seven assets verified, `verified_count: 7`, `asset_count: 7`, and `error: null`. Each listed asset resolves to an active R2/D1 record and the migration action is `dedupe_no_copy`.

Current classification:

- the 08:56 Batch-002 failure receipt: `SUPERSEDED` as current milestone state, but retained as valid incident/history evidence;
- the 09:07 Priority-One receipt: governing completion evidence for the batch/milestone;
- Priority-One migration milestone: `VERIFIED_COMPLETE` as a bounded migration milestone, consistent with the current Master Work Register's ONE/R2 history;
- the historical HTTP 403 / error 1010 is **not** a current environment blocker and must not be revived as one without newer evidence.

## Contradiction resolved

The repository intentionally contains both a failed receipt and a later pass receipt. Reading the earlier receipt in isolation would incorrectly reactivate a resolved Cloudflare blocker. Chronology and verification strength resolve the conflict: the later seven-of-seven Priority-One PASS supersedes the earlier one-asset failure as the governing state while preserving the failure as provenance.

## Master-register effect

No status change is required in the canonical Master Work Register: its current ONE/Cloudflare interpretation already treats the Priority-A private-R2 delivery/runtime migration as a bounded verified milestone. This ledger strengthens the provenance for that interpretation and records the failed-attempt supersession explicitly.

## Sweep disposition

- meaningful historical work classified;
- completed milestone evidence strengthened;
- superseded transient failure identified;
- obsolete revisions classified retired;
- no missing human decision discovered;
- no new environment blocker discovered;
- no P01 subtitle critical-path state or action changed.

Sweep 01 remains `ACTIVE_PARALLEL`.