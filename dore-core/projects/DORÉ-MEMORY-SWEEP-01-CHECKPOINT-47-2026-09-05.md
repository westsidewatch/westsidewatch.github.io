# DORÉ MEMORY SWEEP 01 — CHECKPOINT 47 — A2A / SPARSE RUNTIME BRIDGE RECONCILIATION

Status: BOUNDED_RECONCILIATION_COMPLETE
Date: 2026-09-05
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md` + `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
Evidence ledger: `DORÉ-A2A-CONTROL-PLANE-LOCAL-BRIDGE-EVIDENCE-LEDGER-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- recent A2A/control-plane implementation sequence through commit `45f1373b342d12ddeb2e78f87ff7a278b13b9432`;
- mature adapter bridge commit `9f3cdedcd387d09167e84f4f1abc1eb4250babea`;
- capability-runtime CI gating commit `45f1373b342d12ddeb2e78f87ff7a278b13b9432`;
- immediately preceding typed-envelope, Design-consumer, Companion/4312 resident-path commits;
- existing sparse-capability-runtime canonical addendum and A2A/Storybook autonomy interpretation.

## Reconciliation findings

1. The A2A and sparse-capability-runtime lines have materially converged in code. `local/dore-local/a2a_adapter.py` v0.3 now lazily builds the shared capability runtime/executor and dispatches typed `dore.a2a/1` envelopes through the Design control plane while preserving legacy task compatibility.
2. This is a legitimate `VERIFIED_COMPLETE_SUBMILESTONE` of architecture implementation: the mature adapter is the preferred seam instead of another independent localhost control daemon for the same intelligence.
3. The bounded sequence also establishes Design as the first control-plane consumer and a resident localhost `4312` / Companion transport path. Capability-runtime CI configuration now includes the adapter bridge test and watches the relevant bridge files.
4. Implementation and workflow configuration are not latest-head acceptance proof. The available combined-status query for the latest bounded commit returned no persisted statuses, so CI PASS, resident-runtime reliability and end-to-end production acceptance remain `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`.
5. Existing authority debt remains open. Typed envelopes and idempotency/request identity improve structure but do not alone prove authenticated authorization for mutating execution.
6. The smallest next useful proof is an acceptance packet, not another transport abstraction: latest-head CI PASS; resident 4312 health + typed dispatch; request/idempotency preservation; unauthorized mutation rejection; and one non-visual task proving visual bodies remain dormant.
7. No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified.

## Current disposition

- sparse capability runtime: `ACTIVE_PARALLEL / FOUNDATION`;
- A2A local control-plane bridge: `VERIFIED_COMPLETE_SUBMILESTONE` under the active runtime;
- broad A2A/control-plane operational acceptance: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE`;
- second independent local control daemon for this mature path: `SUPERSEDED` as the current architectural direction;
- authority hardening: remains active evidence debt under Nervous System / coordination governance.

Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and does not create a new human/environment blocker.
