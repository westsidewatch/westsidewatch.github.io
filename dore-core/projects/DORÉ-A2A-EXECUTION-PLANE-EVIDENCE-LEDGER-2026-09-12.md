# DORÉ A2A EXECUTION PLANE — EVIDENCE LEDGER

Date: 2026-09-12
Status: BOUNDED COMPONENT VERIFIED
Parent workstreams: `NERVOUS-SYSTEM`, `EVOLUTION`, `MEM-SWEEP-01`

## Objective

Separate transport acceptance from durable execution completion so Doré cannot treat message delivery, worker claim, artifact creation, verification and completed work as the same state.

## Evidence

- `82fe3ab033deeb52c19a438be44d0047a785a938` adds `local/dore-local/a2a_execution_plane.py`.
- `3f7cde2c6c46efd73b978a11f6a93985d077538f` adds `local/dore-local/a2a_execution_plane_acceptance.py`.

Implemented durable states include `ACCEPTED`, `CLAIMED`, `RUNNING`, `ARTIFACT_PRODUCED`, `VERIFIED`, `PASS`, plus terminal failure/rejection behavior. State is persisted per task; event transitions are append-recorded; source commit/ref and content digest are retained; worker leases have expiry/heartbeat semantics.

The acceptance contract explicitly verifies:

- replay-safe registration;
- exclusive live worker lease;
- lease-required running transition;
- no PASS without artifact;
- no PASS without verification;
- verified-artifact PASS;
- verification failure terminates as FAIL;
- expired lease can be reclaimed.

## Completion judgment

Classification: `VERIFIED_COMPLETE / COMPONENT` for the execution-lifecycle contract.

This is stronger than architecture prose because executable implementation and a deterministic acceptance specification exist. It does not prove that a real production task has yet traversed this exact plane end to end.

## Current quality

The layer is appropriately narrow: transport and execution are separated, completion is fail-closed, provenance-bearing delivery metadata can be retained, and leases prevent two live workers from silently treating the same task as exclusively theirs.

The main evidence boundary is external to this component. Sender/origin authority is not authenticated by the execution plane itself; it trusts the registered delivery/message. Therefore the authority hardening already recorded under `ME-016` remains open.

## Reusable capability retained

`delivery → durable task lifecycle → exclusive claim → execution → artifact → verification → completion evidence`

This primitive is reusable for local Doré work, A2A orchestration, autonomous recovery and future work-state evaluation.

## Missing evidence / next proof

Need one persisted real authorized episode crossing delivery and execution boundaries:

`authenticated/equivalent origin → accepted delivery → execution registration → live lease → real work → provenance-bearing artifact → independent verification → PASS`

and one negative episode proving forged/unauthorized mutating origin is rejected before execution.

## Disposition

Retain and integrate. Do not promote `NERVOUS-SYSTEM`, `EVOLUTION`, broad A2A conformance or production autonomy to complete from this component milestone alone.

Sweep linkage: `DORE-MEMORY-SWEEP-01-CHECKPOINT-82-2026-09-12.md`.