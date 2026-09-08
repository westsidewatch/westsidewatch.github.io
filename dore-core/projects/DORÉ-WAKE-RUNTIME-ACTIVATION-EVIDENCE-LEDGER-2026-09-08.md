# DORÉ WAKE RUNTIME ACTIVATION — EVIDENCE LEDGER

Date: 2026-09-08
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Classification: `VERIFIED_COMPLETE` for the bounded local wake-runtime installation/activation milestone; runtime continuity itself remains `ACTIVE / CORE SUPPORT`.
P01 impact: NONE

## Original objective

Establish a durable local wake mechanism capable of resuming bounded Doré work without depending on an already-running ad hoc process: load a macOS `launchd` service, preserve durable SQLite wake state, and prove a wake-triggered smoke task reaches terminal PASS.

## Governing acceptance contract

`dore-core/evidence/wake-runtime-local-activation-control-20260905.md` explicitly says the control/request record is **not acceptance evidence**. PASS requires behavioral proof that:

1. `org.westsidewatch.dore.wake` is loaded by launchd;
2. durable SQLite wake state exists;
3. the wake-triggered smoke probe reaches `passed`.

The original request packet `wake-runtime-local-activation-request-20260905.json` asked for the same three gates under capability `wake.runtime.install`.

## Completion evidence

`dore-core/evidence/wake-runtime-local-activation-pass-20260905.json` records a later bound acceptance result:

- `status: PASS`;
- request `wake-runtime-local-activation-20260905-03`;
- capability `wake.runtime.install`;
- verified repository head `3b8ebe605cf8c16420432a7a7b84e08537b24f29`;
- launchd label `gui/501/org.westsidewatch.dore.wake` with `loaded=true` and `plist_present=true`;
- 900-second run interval, QueueDirectories enabled, low-priority I/O enabled;
- durable SQLite state present at `~/Library/Application Support/Dore/wake-state.sqlite3`;
- current smoke task `bfaa918c-da37-4202-bf65-226c5a123ef4` reached `state=passed` on attempt 1/1 via `/usr/bin/true`, return code 0;
- kickstart return code 0;
- wake log processed 1 task, passed 1, failed/retry 0, stderr empty.

The acceptance note explicitly binds PASS to the **current smoke task ID** and states that this result supersedes both the failed v1 activation and the v2 false-positive acceptance defect. Earlier smoke tasks therefore cannot be reused to satisfy the gate.

## Current quality judgment

The milestone is defensibly complete for installation/activation because the evidence is behavioral and stateful rather than a mere configuration or request file. It verifies launchd loading, durable state existence and one current wake-triggered task execution.

The milestone must not be inflated into proof of universal autonomous scheduling, arbitrary task recovery, multi-project wake correctness, long-horizon reliability or P01 completion. Those remain governed by their own runtime/project evidence.

## What Doré retained

- acceptance evidence must be bound to the current task/run, not recycled from earlier attempts;
- service installation is not complete until the supervisor reports loaded state and a real triggered task reaches terminal behavior;
- durable wake state belongs outside ephemeral process memory;
- false-positive acceptance is itself a defect that must be explicitly superseded by a stronger gate;
- wake/runtime continuity and project completion are separate claims.

## Weaknesses / debt

- the recorded smoke is intentionally minimal (`/usr/bin/true`), so it proves activation mechanics rather than meaningful task execution;
- one successful wake does not prove long-horizon reliability, crash recovery or heterogeneous workload behavior;
- the evidence packet does not by itself establish authority/safety policy for every future wake-triggered capability;
- later changes to plist/runtime/database schema require regression proof.

## Revisit trigger

Reopen this bounded milestone only if launchd loading, wake-state persistence or current-task wake execution regresses, or if the wake architecture changes materially. Broader autonomous work execution should be verified as separate capability milestones rather than reopening this installation proof.

## Disposition

Keep the local wake-runtime activation milestone closed as `VERIFIED_COMPLETE`; retain runtime continuity as active stewardship. Treat the failed v1 activation and v2 false-positive acceptance as superseded historical evidence, not current blockers.

No P01 subtitle ordering, audio/transcription dependency, deployment state or blocker condition is changed by this ledger.
