# DORÉ A2A DELIVERY PLANE — EVIDENCE LEDGER

Date: 2026-09-09
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / ACCEPTANCE_EVIDENCE_INCOMPLETE
Related canonical rows: `RUNTIME`, `NERVOUS-SYSTEM`, `MEM-SWEEP-01`
P01 impact: NONE

## Bounded evidence reviewed

- `local/dore-local/a2a_delivery_plane.py`
- `local/dore-local/a2a_delivery_plane_acceptance.py`
- `local/dore-local/a2a_response_stall_acceptance.py`
- `local/dore-local/a2a_supervisor.py`
- current `DORÉ-MASTER-WORK-REGISTER.md` A2A/runtime/authority interpretation

## What is implemented

The local A2A delivery plane is real code, not only architecture. It fetches ChatGPT→Doré coordination messages from a remote ref without requiring a checkout mutation, validates sender/recipient/schema/message identity, binds accepted content to SHA-256, persists a durable inbox plus delivery/consumer receipts, rejects identity conflicts, deduplicates replays, and explicitly separates `DURABLE_ACCEPTED` from task execution.

`canonical_delivery_reply()` preserves an important evidence rule: transport/delivery/consumer status is not task-completion evidence. This is compatible with Sweep doctrine that a delivery acknowledgement must not be promoted into project completion.

The supervisor also embodies the intended non-blocking collaboration rule: ChatGPT absence is normal; peer-pending state is durable but non-blocking; human gates remain explicit; unchanged autonomous work can escalate to attention/recovery state.

## Evidence boundary

Repository acceptance scripts exist, but the bounded evidence reviewed here does **not** include an independently persisted run artifact proving the current scripts pass against the current tree.

The response-stall acceptance has an additional contract weakness: it reports `first_missing_transition: RECEIVED -> TASK_REGISTERED`, but its `received_to_running` check only verifies a consumer receipt at `RECEIVED`; it then calls `coordination_worker.dispatch(msg)` directly. That does not independently prove that the durable delivery inbox drives a real `RECEIVED → TASK_REGISTERED/RUNNING → PASS/FAIL` lifecycle through the production consumer path.

Therefore the durable delivery implementation is stronger than the current persisted acceptance evidence.

## Current classification

- A2A durable delivery/identity/replay foundation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- Delivery-vs-execution semantic separation: retain as governing behavior.
- Current end-to-end consumer lifecycle acceptance: `UNKNOWN_NEEDS_EVIDENCE`.
- A2A supervisor non-blocking doctrine/implementation: `ACTIVE_PARALLEL`; no global autonomy-completion claim.
- Existing coordination authority debt remains unchanged: sender strings plus executable/cwd allowlists are not a cryptographically authenticated authority envelope.

## Smallest next proof

Run the current delivery-plane acceptance against the current tree and persist the result. Then strengthen the stall acceptance so a durable inbox message is consumed by the actual worker lifecycle and produces persisted transition evidence for `DURABLE_ACCEPTED → RECEIVED → TASK_REGISTERED/RUNNING → PASS/FAIL`, including replay/no-reexecution and one identity-conflict negative case.

This work must remain subordinate to P01 and must not alter the current P01 environment blocker or resume ordering.
