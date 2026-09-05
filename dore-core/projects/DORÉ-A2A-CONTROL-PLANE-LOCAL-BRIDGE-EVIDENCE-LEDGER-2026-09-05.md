# DORÉ A2A CONTROL-PLANE LOCAL BRIDGE EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- recent A2A/control-plane commits through `45f1373b342d12ddeb2e78f87ff7a278b13b9432`;
- `local/dore-local/a2a_adapter.py` v0.3 bridge introduced by `9f3cdedcd387d09167e84f4f1abc1eb4250babea`;
- capability-runtime CI path gating added by `45f1373b342d12ddeb2e78f87ff7a278b13b9432`;
- immediately preceding resident `localhost:4312`, Companion transport, typed control-envelope and Design-consumer implementation commits in the same bounded sequence;
- existing sparse-capability-runtime canonical addendum and prior A2A/Storybook autonomy evidence.

## Current classification

### A2A local control-plane bridge
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

A concrete convergence milestone is now implemented: the established local A2A adapter is no longer only a legacy task-compatibility seam. It lazily constructs the shared sparse capability runtime/executor and routes typed `dore.a2a/1` envelopes through the Design control plane. This deliberately avoids inventing a second localhost daemon for the same intelligence.

### End-to-end operational acceptance
`ACTIVE / UNKNOWN_NEEDS_EVIDENCE`

The implementation commits and CI wiring are real, but the latest bounded commit currently has no persisted combined-status receipt in the available GitHub status surface. Therefore repository implementation + workflow configuration must not be promoted into a latest-head CI PASS or a sustained resident-runtime PASS.

## Evidence boundary

1. The adapter explicitly preserves legacy A2A behavior while adding lazy typed-control routing; this is architectural convergence, not a replacement of every older transport path.
2. The bridge constructs `CapabilityExecutor` + `LazyCapabilityRuntime`, registers synthetic visual handlers, and calls the Design control-plane builder. This is strong evidence that sparse capabilities and A2A are now joined in code rather than merely described in doctrine.
3. Capability-runtime workflow path filters and test commands now include the local adapter and dedicated bridge test. This improves regression coverage but is configuration evidence until an actual run receipt is persisted.
4. The bounded sequence also adds a canonical resident localhost `4312` server/Companion transport path and Design as the first control-plane consumer. These are implementation milestones, not proof that every product or capability already uses the shared plane.
5. No evidence in this batch proves broad multi-product A2A adoption, authenticated cross-boundary authority, long-running resident reliability, offline restart/recovery, or materially different-domain transfer.
6. Earlier authority debt remains relevant: a typed control envelope improves structure but does not by itself prove cryptographically trustworthy mutation authority.

## Current quality judgment

The direction is materially stronger than parallel ad-hoc agent/server paths. Reusing the mature local adapter and routing typed envelopes into one capability runtime reduces duplicate orchestration and aligns with the governing principle that Doré Image/Design are capabilities of one persistent intelligence rather than separate agents.

The main remaining weakness is evidence closure. Several implementation commits landed rapidly, but implementation density is ahead of persisted runtime/CI proof. The next useful work is acceptance evidence, not another transport abstraction.

## Durable learned principles

- A2A should converge on one typed control plane and one persistent intelligence rather than multiplying localhost daemons.
- Legacy compatibility can remain while typed capability routing is introduced behind a narrow adapter seam.
- Lazy runtime construction preserves sparse activation and prevents control-plane integration from forcing all capability bodies resident.
- CI path inclusion is regression intent, not a passing-test receipt.
- Typed envelopes improve protocol discipline but do not automatically satisfy authority/authentication requirements.

## Revisit / supersession judgment

- The architectural idea of adding a second independent local control server for the same mature A2A path is `SUPERSEDED` by adapter convergence for current Design/control-plane work.
- The bridge itself is not a completed project; retain it as a completed submilestone under an active runtime workstream.
- Revisit if a concrete product requires isolation that cannot safely share the adapter/runtime, or if profiling shows the lazy bridge introduces unacceptable startup or resident cost.

## Smallest next proof

Persist one latest-head acceptance packet containing:

1. capability-runtime CI PASS including `tests.test_dore_local_a2a_control_bridge`;
2. live resident `localhost:4312` health + typed-envelope dispatch through the mature adapter;
3. one Design request with request ID/idempotency identity preserved through dispatch and result;
4. one negative/unauthorized mutation test at the authority boundary;
5. one non-visual request proving visual capability bodies/provider schemas remain dormant.

Do not infer whole-system A2A completion from this packet; use it to close only the local bridge/runtime acceptance boundary.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified by this reconciliation.
