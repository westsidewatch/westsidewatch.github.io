# DORÉ SENSORY STALE RESEARCH QUEUE — EVIDENCE LEDGER

Date: 2026-09-04
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Classification: `MAINTENANCE / UNKNOWN_NEEDS_EVIDENCE`

## Bounded evidence

- `dore-core/memory/sensory-active.json`
- `dore-core/memory/sensory-heartbeat-diagnostic.json`
- `dore-core/memory/actions-probe-diagnostic.json`
- `dore-core/constitution/CONSTITUTION.md`

## Current evidence

The sensory substrate itself is live: the latest persisted heartbeat diagnostic is `ok: true` at `2026-09-04T13:55:30.967Z`, and the GitHub Actions probe is `ok: true` at `2026-09-04T14:35:06Z`.

However, `sensory-active.json` contains three signals still in `RESEARCHING`, all claimed on 2026-08-28 and all with `brain_node: null`:

1. Search-page conversation query `3973e981-e7e2-4e09-b0ef-6ab22ba1544f`.
2. Scripture/search query `5a7c7590-004c-4903-9e28-d322c42bec90`.
3. Memory test query `4a2ab8d9-0bc4-4952-8dc2-ba60a8b09ed8`.

The current heartbeat continues to select the first of these and reports `changed: false`; its source-side update remains 2026-08-28. This means observability/heartbeat success must not be confused with research-item progress or terminalization.

## Interpretation

- The earlier sensory repair milestone remains valid; no regression in probe/heartbeat availability is shown by this batch.
- The long-lived `RESEARCHING` items constitute lifecycle/queue-maintenance debt: the current durable evidence does not show a timeout, retry budget, explicit `PARKED`/`FAILED`/`NEEDS_REVIEW` transition, or successful consolidation path for these items.
- This is not a P01 blocker and does not justify an environment/human-decision notification.
- Constitution principles `Observation != memory`, `Memory != truth`, `Uncertainty must remain visible`, and `Failure must degrade safely` imply that stale sensory items should remain explicitly unresolved rather than being silently treated as learned knowledge.

## Revisit trigger

Revisit the sensory queue lifecycle when one of the following is true:

- a stale `RESEARCHING` signal blocks or distorts current Search/conversation behavior;
- a general sensory queue lifecycle policy is implemented;
- diagnostic commit-cadence compaction is undertaken;
- another signal remains non-terminal beyond the intended research window.

## Desired proof

A bounded acceptance proof should demonstrate:

1. a stale research item can be classified without inventing completion;
2. retry/timeout/escalation policy is persisted;
3. terminal states distinguish `CONSOLIDATED`, `PARKED`, `FAILED/NEEDS_REVIEW`, and genuinely active research;
4. heartbeat/probe observability does not itself mutate semantic completion state;
5. one intentionally stale fixture transitions according to policy while preserving provenance.

## Current disposition

Keep the sensory runtime active. Classify stale research-item lifecycle as `MAINTENANCE / UNKNOWN_NEEDS_EVIDENCE`. Do not reopen the historical sensory repair milestone and do not interrupt P01.
