# DORÉ WAKE RUNTIME EVIDENCE LEDGER

Date: 2026-09-07
Status: ACTIVE / SWEEP-01 EVIDENCE
Related workstreams: `RUNTIME`, `CORE`, `MEM-SWEEP-01`
P01 impact: NONE

## Bounded evidence reviewed

- `dore-core/runtime/wake_runtime.py`;
- `dore-core/tests/test_wake_runtime.py`;
- current `DORÉ-MASTER-WORK-REGISTER.md` runtime interpretation;
- bounded repository search for explicit workflow invocation of `test_wake_runtime.py`.

## What is implemented

The wake runtime is a real stdlib-only durable worker, not a narrative design note. It implements:

- SQLite durable task state with WAL;
- idempotency keys for enqueue;
- bounded task claiming with leases;
- expired-lease recovery;
- retry/backoff and terminal failure;
- verifier execution without `shell=True`;
- verify-before-promote file replacement;
- backup creation and promotion logging;
- bounded `run-once` execution so no resident daemon is required.

## Acceptance specification present

`test_wake_runtime.py` contains executable unit tests for:

1. idempotent enqueue + passing probe;
2. failing probe reaching terminal failure under bounded attempts;
3. verified file promotion with backup retention;
4. failed verifier refusing promotion;
5. recovery of an expired lease back to pending.

These tests directly exercise the runtime behaviors that matter for durable wake/resume and safe bounded promotion.

## Evidence boundary

This bounded pass did not find an explicit workflow reference proving that `test_wake_runtime.py` is currently executed in CI. The presence of runnable tests is stronger than a prose-only contract, but test-source presence alone is not a persisted passing run.

Separately, the canonical runtime/P01 evidence already shows real persisted continuity and a production `ENVIRONMENT_BLOCKED` stop at attempt 39. That production evidence supports the broader `RUNTIME = ACTIVE` interpretation but does not retroactively prove every wake-runtime unit test ran.

## Current classification

- wake runtime implementation: `ACTIVE / FOUNDATION` as part of `RUNTIME`;
- wake-runtime unit acceptance source: real and runnable;
- persisted passing wake-runtime suite: `UNKNOWN_NEEDS_EVIDENCE` in this bounded review;
- no standalone `VERIFIED_COMPLETE` promotion is justified.

## Smallest useful future proof

Persist one successful execution of the existing `test_wake_runtime.py` suite, ideally as a required regression step in the canonical runtime/foundation workflow. Preserve failure output if any test fails rather than converting source presence into a completion claim.

## Durable judgment

Do not reopen or demote the broader runtime merely because this exact CI invocation is not found: live P01 continuity evidence is stronger for runtime existence. Treat this as a narrow observability/regression-evidence gap, not an environment blocker and not a reason to interrupt P01.
