# DORÉ WAKE RUNTIME — EVIDENCE LEDGER

Date: 2026-09-13
Status: `VERIFIED_COMPLETE / COMPONENT` for the bounded wake-queue + verified-promotion primitive
Parent workstream: `RUNTIME`
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Scope

This ledger evaluates the current durable short-lived wake runtime represented by:

- `dore-core/runtime/wake_runtime.py`;
- `dore-core/tests/test_wake_runtime.py`.

It does **not** evaluate or alter the active P01 subtitle path, production audio/transcription dependency, resident coordination daemon, A2A execution plane, or broader autonomous-project continuity claim.

## Original objective

Provide a small stdlib-only runtime for event/condition-triggered work that can persist a queue, wake for a bounded amount of work, verify a candidate before mutation, promote atomically, preserve rollback evidence, recover stale leases, and exit without requiring a resident daemon.

## Implementation evidence

`wake_runtime.py` implements:

- SQLite/WAL durable task state with explicit `pending/running/passed/failed/retired` states;
- idempotent enqueue through a unique `idempotency_key`;
- transactional single-task claim via `BEGIN IMMEDIATE`;
- bounded leases and expired-lease recovery;
- retry/backoff with a bounded `max_attempts` terminal failure path;
- shell-free verifier execution with timeout;
- a hard rule that `promote_file` requires a verifier;
- backup creation before replacement of an existing target;
- copy-to-temporary + `os.replace` atomic promotion;
- durable `promotion_log` evidence;
- restoration from backup on promotion exception;
- bounded `run_once` execution rather than an always-resident worker.

## Acceptance evidence

`test_wake_runtime.py` contains executable unit coverage for five critical behaviors:

1. idempotent enqueue and successful probe completion;
2. failed probe reaches terminal failure at its attempt bound;
3. verified file promotion succeeds and preserves the previous target as backup;
4. failed verification prevents mutation of the target;
5. an expired lease is recovered from `running` back to `pending` when attempts remain.

The tests import the actual runtime module rather than duplicating a specification-only fixture.

## Evaluation

### Current classification

`VERIFIED_COMPLETE / COMPONENT` for the **bounded wake-runtime primitive**.

The surrounding `RUNTIME` workstream remains `ACTIVE`. This component does not prove generic autonomous scheduling, production deployment health, authorized arbitrary command execution, distributed exactly-once semantics, or global self-healing.

### Current quality

Strong for the narrow primitive. The implementation is intentionally small, stdlib-only and fail-closed around file promotion. Its most valuable property is not merely persistence; it is the mutation gate: a candidate cannot be promoted without an explicit verifier, an existing target is backed up, and failed verification leaves the target unchanged.

### Durable capability retained

The reusable pattern is:

`durable queued intent -> scoped claim/lease -> bounded execution -> explicit verifier -> atomic mutation -> backup/evidence -> terminal durable outcome`

This is compatible with the broader Doré principle that implementation is not acceptance and mutation should occur only after a bounded verifier has passed.

### Weaknesses / evidence boundaries

- repository inspection in this Sweep pass does not itself provide a fresh CI-run artifact for these tests;
- only local SQLite semantics are demonstrated, not distributed/multi-host queue correctness;
- `run_argv` can execute arbitrary argv supplied by the task payload, so production use still requires an authority/allowlist boundary outside this primitive;
- promotion is currently a local-file primitive rather than a generic transactional artifact publisher;
- recovery tests cover expired leases, not process-kill/fault-injection across every promotion stage;
- no claim is made that this runtime is the current governing mechanism for P01.

## Revisit trigger

Reopen this component if:

- production use requires multi-host claims;
- authority boundaries are moved inside the runtime;
- promotion expands beyond local files;
- failure injection exposes a mutation/rollback gap;
- the primitive becomes a dependency of a consequential production path and needs persisted CI/runtime acceptance evidence.

## Disposition

Keep the bounded primitive closed as a reusable component and regression target. Do not reopen it merely because Doré continues to use scheduling/wake behavior elsewhere. Broader autonomous continuity remains owned by the canonical `RUNTIME` workstream.

## Canonical-register interpretation

No workstream status change is warranted. `RUNTIME` remains `ACTIVE`; this ledger adds a bounded verified component beneath that row. `MEM-SWEEP-01` remains `ACTIVE_PARALLEL`.

No P01 state, dependency, ordering, blocker, credential, binding, or resume condition is changed by this evidence reconciliation.
