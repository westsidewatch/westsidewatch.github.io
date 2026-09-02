# DORÉ SENSORY DIAGNOSTIC PERSISTENCE EVIDENCE LEDGER — 2026-08-31

Status: SWEEP-01 BOUNDED EVIDENCE / MAINTENANCE FINDING
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Related: `CW-001`, `RQ-001`, `ME-001`, `CORE`, `MEM-SWEEP-01`

## Scope reviewed

This bounded pass reviewed the current rolling sensory-memory evidence path without touching the active P01 subtitle critical path:

- `.github/workflows/dore-sensory-heartbeat.yml`;
- `.github/workflows/dore-actions-probe.yml`;
- current `dore-core/memory/sensory-*-diagnostic.json` evidence;
- current `dore-core/memory/actions-probe-diagnostic.json`;
- recent repository commits produced by those workflows on 2026-08-31, including `15dc6f2168ce63d0bfcce9e6362bda1c091852d9` and `91504d10d2761fa4df70f88a0e07d5f275b88d65`.

## Evidence

### 1. Historical repair remains verified

The current heartbeat path continues to obtain successful deployed responses. The 2026-08-31 diagnostic commit records a seed HTTP success, `state=CONSOLIDATED`, `deduplicated=true`, `schema_reconciled=true`, and a successful claim step. The heard counter has continued to rise (607 in the reviewed commit). The Actions probe also continues to persist successful scheduled-run evidence.

This strengthens retention evidence for the already-completed sensory-loop repair/consolidation milestone. It does **not** create a new named completion milestone and does not prove heterogeneous-signal research quality.

### 2. The current evidence-persistence implementation guarantees repository churn

`dore-sensory-heartbeat.yml` is scheduled every five minutes. Each run writes fresh timestamps into seed/claim/heartbeat diagnostics and commits whenever the staged diagnostic files differ. Because the timestamp changes on every run, a successful scheduled heartbeat normally produces a repository commit even when the underlying sensory state has not materially changed.

`dore-actions-probe.yml` is also scheduled every five minutes. It writes a new run id, SHA and timestamp, then commits and pushes unconditionally. Therefore a normal successful probe also produces a repository commit every scheduled run.

Recent history shows the two evidence writers interleaving repeatedly. This is consistent with the workflow definitions rather than evidence of a fault loop.

At the configured cadence the design can generate up to roughly 24 diagnostic-only commits per hour (12 heartbeat + 12 Actions-probe runs) when schedules execute normally, before any other Doré/product work.

### 3. Classification

- sensory runtime / learning system: `CORE/CONTINUOUS`;
- historical sensory repair/consolidation milestone: retain `VERIFIED_COMPLETE`;
- rolling diagnostic persistence mechanism: `MAINTENANCE`;
- current high-frequency Git-history persistence strategy: `COMPLETED_REVISIT_CANDIDATE` as an implementation detail of the verified observability milestone, **not** a reason to reopen the underlying repair milestone;
- broad robustness / heterogeneous-signal quality remains `UNKNOWN_NEEDS_EVIDENCE` under `ME-001` and `RQ-001`.

## Current quality judgment

The original design was useful because it made otherwise ephemeral live evidence durable and auditable during the sensory repair period. With the repair milestone now stable, committing timestamp-only evidence to `main` every few minutes is disproportionately noisy. It increases history volume, makes material product/architecture commits harder to scan, and couples observability retention to source-control churn.

This is technical-maintenance debt, not an environment blocker and not a present production failure.

## Revisit trigger and preferred future direction

Do not change this path merely for cosmetic history cleanup while higher-value work is active. Revisit when one of the following is true:

- repository-history noise materially impairs operations/auditability;
- sensory observability is being formalized under the Nervous System;
- heterogeneous-signal/volume benchmarking is introduced;
- a low-risk maintenance window exists.

Preferred future direction: preserve state-transition/error evidence durably while reducing timestamp-only source commits. Candidate patterns include commit-on-material-transition/failure, periodic summarized checkpoints, workflow artifacts for short-lived diagnostics, or a D1/R2 observability store with selected Git summaries. Any change must preserve the ability to prove deployed heartbeat/probe operation and must not weaken incident forensics.

## P01 boundary

No P01 subtitle runtime, deployment, binding, credential, job ordering, blocker state or resume state was changed in this pass. The existing P01 production audio/transcription environment dependency remains untouched.

## Sweep disposition

This batch adds a maintenance/revisit finding and stronger retention evidence, but it does not justify `MEM-SWEEP-01 = VERIFIED_COMPLETE`.

## 2026-09-01 revalidation

A fresh bounded history check confirms the same persistence pattern is still active and has not changed classification. Recent commits continue to alternate between `chore(dore): persist sensory heartbeat evidence [skip ci]` and `chore(dore): persist Actions probe evidence [skip ci]`, including heartbeat commits `7251222c137f87353f69e1d804f7b04f52a05dca`, `eaa6335f9f89f3bc86164f0cfbd954db75f764ba`, `014d66a6548dcc9ff018f14adc5dfbdf18c3dff3`, `b469af3af362bea4bc732cf06ba3038643d5d039`, `6b6b8f50bebad5432035593c8d435a16a0b1d9f4`, and probe commits `3f43565ea0cf735039fff0f6a5d2ac9483ddb748`, `83cc7a0a6c1303f767045ac26a7da6a4f7c7e2ce`, `40d06ae36e6ccd07e4e258fbfc15f47a74e40b9e`, `3e1a2a5cd6c5047f1cc0e2735a995a3cd5f90f9c`.

The observed timestamps remain consistent with the previously documented roughly five-minute cadence and interleaving writers. This is retention evidence that the observability path remains live; it is also further confirmation that the source-control-churn debt is persistent rather than a one-day anomaly.

No new blocker, completion milestone, P01 impact, or canonical status change is justified. The Master Register's existing `MEM-SWEEP-01` interpretation already captures this as `MAINTENANCE` / completed-observability revisit debt, so no canonical row rewrite is required from this bounded revalidation.

## 2026-09-02 revalidation

A fresh bounded history + commit-diff check confirms the same behavior is still active on 2026-09-02. Recent history continues to alternate heartbeat/probe persistence commits; the heartbeat commit `6705d0865a151546afaad89b64e06123f94b53ca` changed the seed/heartbeat/claim timestamps and advanced `heard_count` from `1015` to `1016` while preserving `http_status=200`, `state=CONSOLIDATED`, `deduplicated=true`, `schema_reconciled=true` and successful claim behavior.

This is useful retention evidence that the repaired sensory path remains live two days after the original maintenance finding. It also confirms that the high-frequency Git-history churn is ongoing rather than transient: timestamp/counter-only evidence is still being persisted to source history at the configured rolling cadence.

Current classification remains unchanged: historical repair `VERIFIED_COMPLETE`; persistence mechanism `MAINTENANCE`; high-frequency Git persistence `COMPLETED_REVISIT_CANDIDATE`; broader heterogeneous-signal robustness still `UNKNOWN_NEEDS_EVIDENCE`. The canonical Master Register already expresses this operational truth, so no row/status rewrite is warranted.

P01 impact remains none: no subtitle runtime, deployment, binding, credential, source order, blocker, or resume state was changed.