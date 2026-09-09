# DORÉ WAKE RUNTIME ACTIVATION — EVIDENCE LEDGER

Date: 2026-09-09
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Classification: `VERIFIED_COMPLETE` for the bounded local activation milestone; wake/runtime stewardship remains `ACTIVE / CORE-ADJACENT`.

## Evidence reviewed

- `dore-core/evidence/wake-runtime-local-activation-request-20260905.json`
- `dore-core/evidence/wake-runtime-local-activation-control-20260905.md`
- `dore-core/evidence/wake-runtime-local-activation-pass-20260905.json`

## Original objective

Install and verify the local macOS wake runtime as a durable autonomous execution substrate rather than treating a requested install or process launch as success.

## Completion evidence

The request defines three explicit acceptance conditions: launchctl loaded, SQLite durable state exists, and a launchd-triggered smoke probe passes.

The control record explicitly says it is **not acceptance evidence** and requires behavioral proof from the self-hosted macOS A2A relay.

The final PASS record satisfies that bounded contract with concrete state:

- capability `wake.runtime.install`;
- verified head `3b8ebe605cf8c16420432a7a7b84e08537b24f29`;
- launchd label `gui/501/org.westsidewatch.dore.wake` loaded with plist present;
- 900-second interval, queue-directory activation and low-priority I/O enabled;
- durable SQLite state present at `~/Library/Application Support/Dore/wake-state.sqlite3`;
- current smoke task `bfaa918c-da37-4202-bf65-226c5a123ef4` reached `passed` in one attempt with return code 0;
- kickstart returned 0;
- wake log records one processed / one passed / zero failed-or-retry and empty stderr.

The acceptance note is material provenance: this PASS is bound to the current smoke task and explicitly supersedes both the failed v1 activation and the v2 false-positive acceptance defect.

## Current quality judgment

Strong for the bounded local-activation milestone because the evidence is behavioral and fail-closed: a request is separated from acceptance, persistence is checked, the current smoke task is identity-bound, and earlier false-positive evidence is explicitly superseded.

This does **not** prove all future wake tasks succeed, does not prove autonomous project completion, does not prove remote/cloud wake parity, and does not close broader Runtime/Evolution/Nervous-System work.

## Capability retained

- define acceptance before execution;
- distinguish request/control artifacts from behavioral PASS evidence;
- bind acceptance to the current execution identity so stale successes cannot satisfy a new gate;
- combine launchd process state, durable SQLite state and real task execution in one acceptance boundary;
- preserve failed/false-positive historical attempts as superseded provenance rather than deleting them.

## Weaknesses / debt

- the proof is one bounded local activation and one `/usr/bin/true` smoke probe;
- no heterogeneous long-running task or failure/retry/recovery workload is part of this milestone;
- local activation does not by itself prove cross-host authority, scheduling correctness under sleep/reboot, or broader autonomous continuity.

## Revisit trigger

Reopen the bounded milestone only if launchd installation/regression, SQLite state loss, wake-trigger failure, or stale-task acceptance regression appears. Treat broader autonomous execution quality as separate Runtime/Evolution evidence.

## Disposition

Keep the local activation milestone closed as `VERIFIED_COMPLETE`. Preserve wake/runtime as active infrastructure and use stronger real workloads for future capability claims. Do not reopen this milestone merely because the wake runtime continues operating.

## Canonical interpretation

This ledger supports the Master Register's existing statement that the wake-runtime local activation milestone has been reconciled. No P01 subtitle state, ordering, environment dependency, credential, audio or transcription path is modified by this ledger.
