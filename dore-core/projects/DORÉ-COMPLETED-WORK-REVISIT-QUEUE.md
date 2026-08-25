# DORÉ COMPLETED WORK REVISIT QUEUE

Status: ACTIVE / SWEEP-01 OUTPUT
Established: 2026-08-25
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

This queue is only for work that was legitimately completed for its original milestone but may deserve a later pass. Revisit priority is evidence-based and must not displace the active P01 subtitle critical path without a stronger reason.

## RQ-001 — Sensory-loop broader robustness evaluation

**Source completed milestone:** `CW-001 — Sensory-loop consolidation / D1 reconciliation milestone`

**Current priority:** LOW / WATCHLIST

**Why it may deserve revisit**
The repair milestone is verified on deployed evidence, including consolidated state, deduplication, schema reconciliation, heartbeat success and Actions probing. However, current visible evidence is narrow and does not yet demonstrate heterogeneous signal classes, sustained volume, duplicate/error rates, or long-horizon learning quality.

**Do not reopen now because**
The original repair objective has been met and there is no present production failure. P01 and other active mission-critical work have higher leverage.

**Revisit trigger**
Raise priority if any of the following occurs:
- duplicate or dropped sensory signals reappear;
- a schema migration changes signal/brain-node reconciliation;
- Doré begins ingesting materially new classes of sensory signal;
- enough real traffic exists to support a meaningful volume/quality benchmark;
- a regression or learning-quality benchmark can be added at low marginal cost.

**Desired future evaluation**
Measure heterogeneous-signal success, deduplication accuracy, failed-claim/retry behavior, long-horizon persistence, false consolidation risk and sampled research-answer quality.

**Current disposition:** keep closed; watch for trigger.