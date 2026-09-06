# DORÉ Explore — Autonomous Evolution Last Layer

Date: 2026-09-05
Status: RESEARCH COMPLETE / READY FOR BOUNDED IMPLEMENTATION
Trigger: 多雷探索

## Need

Complete the last layer required for unattended small evolution cycles:

1. autonomous trigger;
2. automatic accept / rollback gate;
3. durable wake state.

All choices are filtered by DORÉ Constitution 0.3: free-first, open/mature, small, low-energy, simple, safe, stable, maintainable, replaceable, local-first, low-lock-in.

## Wave 1 — Landscape

The mature pattern is not an always-running autonomous agent. It is durable deterministic orchestration around an agent:

EVENT / TIMER -> durable queue/state -> bounded work -> verifier gate -> commit or reject -> next wake condition.

Strong references found:

- Apple launchd: native macOS on-demand/timed/path-triggered process launcher. Apple recommends on-demand launch rather than keeping a daemon continuously alive. Supports WatchPaths, QueueDirectories, StartInterval and StartCalendarInterval.
- APScheduler: mature Python scheduler with persistent stores, but current v4 is prerelease and adds dependencies; useful as a reference, not preferred for DORÉ's Mac-native minimum layer.
- sqlite-durable-workflow: zero-runtime-dependency Python + SQLite jobs/outbox, idempotency, leases, fencing token, bounded retry, heartbeat, recovery.
- DurableFlow / durable-agents / chowki / Alkaline: useful implementations of checkpointing, replay suppression, approval/gating, budgets and restart-safe agent work; mostly pattern sources rather than dependencies.
- 2026 research on self-evolution contamination shows post-hoc rollback is insufficient when bad skills have already contaminated descendants; admission needs a pre-commit verifier gate.

## Wave 2 — Mechanism

### Autonomous trigger

Preferred: **ABSORB / USE macOS launchd**.

Why:
- already part of macOS;
- no new package/runtime service;
- on-demand rather than resident;
- path, queue and time triggers;
- wake-after-sleep behavior for relevant scheduled jobs;
- system-managed lifecycle.

DORÉ should not recreate a resident Python scheduler for this purpose.

APScheduler 3.x remains mature but would add a Python scheduling dependency. APScheduler 4.x has useful persistent scheduling architecture but is still prerelease and has current issue traffic around leases/SQLite/DST. Outcome: WATCH/ABSORB, not adopt for this layer.

### Durable wake state

Preferred: **ABSORB sqlite-durable-workflow pattern; implement DORÉ-owned thin SQLite schema using Python stdlib sqlite3 unless its library proves materially better in bounded testing.**

Minimum durable state:
- loop/capability id;
- trigger reason;
- status;
- not_before / next_wake_at;
- attempt count / bounded retry state;
- idempotency key;
- evidence/version baseline;
- candidate revision;
- verifier result;
- accepted revision;
- rollback pointer;
- last_run / last_success / last_failure;
- lease/fencing token if concurrent execution becomes possible.

No permanent process is required. launchd wakes a short-lived worker; SQLite tells it what is due; worker exits when no bounded work remains.

### Automatic accept / rollback gate

Preferred: **pre-commit deterministic gate + isolated candidate revision + explicit promotion.**

Pattern:

BASELINE -> candidate change in isolated branch/worktree/temp checkout -> cheap deterministic checks -> targeted behavioral acceptance -> regression checks -> cost/resource/safety limits -> PASS: promote/commit -> FAIL: discard candidate and retain failure evidence.

Important research lesson: do not rely mainly on post-hoc rollback. A harmful learned capability can influence later learning, so unverified candidate material must remain outside canonical Memory/Capability Registry until it passes admission checks.

For code changes, Git itself provides cheap versioning/rollback primitives already present in DORÉ's workflow. The gate should prefer discard-before-promotion over revert-after-contamination.

## Wave 3 — DORÉ Fit

### USE
- macOS launchd for wake/on-demand activation.
- SQLite (stdlib sqlite3) for durable wake state.
- Git branch/worktree/commit primitives for candidate isolation and promotion where code is involved.
- existing DORÉ acceptance tests/Vital Signs as verifier inputs.

### ABSORB
- sqlite-durable-workflow: idempotency key, lease/fencing, bounded retry, unknown-side-effect isolation.
- DurableFlow/durable-agents/chowki: checkpoint, replay suppression, approval/gate and crash-resume patterns.
- Alkaline: cycle prevention and explicit budget guardrails.
- APScheduler: trigger/data-store separation and schedule identity/conflict concepts.
- Verifier-as-Gatekeeper research: pre-commit admission before learned skills enter canonical context.

### WATCH
- APScheduler 4.x until stable production release/migration story.
- newer embedded agent workflow engines until maturity/reliability exceeds the benefit of DORÉ's thin native layer.

### REJECT FOR CORE NOW
- Temporal/LangGraph/Prefect-class orchestration for this single-Mac layer: capable but too much machinery for the present need.
- permanent polling daemon solely to keep evolution alive.
- unrestricted self-modification followed by rollback only after failure.

## Recommended DORÉ architecture

```text
Event / timer / path change / loop gap
            |
         launchd
            |
    short-lived DORÉ wake worker
            |
      SQLite durable state
            |
     due? -- no --> exit/sleep
      |
     yes
      |
Memory freshness + duplicate check
      |
Open Research Micro-Loop if needed
      |
Candidate isolated from canonical state
      |
Verifier Gate
  |              |
 FAIL           PASS
  |              |
record          promote
failure         candidate
+ discard       atomically
  |              |
  +------> SQLite next wake <-----+
                 |
                exit
```

## Acceptance contract for implementation

A production PASS must prove all of these with behavioral evidence:

1. no ChatGPT/user conversation is required to trigger a due bounded evolution task;
2. no resident DORÉ research daemon is required;
3. reboot/process-kill does not lose pending wake state;
4. duplicate trigger does not duplicate the same evolution job;
5. failed candidate cannot enter canonical Memory/Registry/code path;
6. accepted candidate is linked to verifier evidence and baseline;
7. failed/aborted candidate has a rollback/discard path;
8. retries and research waves are bounded;
9. idle resource cost is effectively only launchd + SQLite file state;
10. human Terminal repetition is not required after bootstrap.

## Decision

Proceed with a thin DORÉ-owned implementation rather than adopting a workflow framework:

**launchd + Python stdlib sqlite3 + DORÉ verifier/Vital Signs + Git isolation/promotion.**

External projects are retained as architecture nutrition and test-pattern references, not hard dependencies unless a later bounded bake-off proves otherwise.
