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