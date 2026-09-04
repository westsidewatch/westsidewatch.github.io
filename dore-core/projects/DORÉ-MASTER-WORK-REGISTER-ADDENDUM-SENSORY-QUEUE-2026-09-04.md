# DORÉ MASTER WORK REGISTER — SENSORY QUEUE ADDENDUM

Date: 2026-09-04
Status: CANONICAL_EXTENSION
Parent: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence: `DORÉ-SENSORY-STALE-RESEARCH-QUEUE-EVIDENCE-LEDGER-2026-09-04.md`

This addendum deepens the existing `MEM-SWEEP-01` / sensory-memory interpretation until the parent register can be safely rewritten in full.

## Canonical extension

| ID | Workstream | Status | Current position | Next milestone |
|---|---|---|---|---|
| SENSORY-QUEUE-LIFECYCLE | Sensory research-item lifecycle / terminalization | MAINTENANCE / UNKNOWN_NEEDS_EVIDENCE | Sensory heartbeat and Actions probe remain live/`ok`, preserving the earlier observability repair milestone. Separately, three durable signals remain `RESEARCHING` since 2026-08-28 with `brain_node: null`; the current heartbeat observes the oldest with `changed: false`. There is no persisted proof yet of timeout/retry budget/escalation or explicit non-success terminalization for stale items. This is lifecycle debt, not a P01 blocker and not a sensory transport regression. | Implement and persist a bounded stale-item lifecycle proof covering retry/timeout/escalation plus explicit `CONSOLIDATED`, `PARKED`, `FAILED/NEEDS_REVIEW`, and genuinely active states while preserving provenance and preventing heartbeat/probe health from being mistaken for semantic completion. |

## Governing boundary

- Do not silently promote stale sensory research into learned/canonical knowledge.
- Do not reopen the historical sensory transport/heartbeat repair milestone without contrary runtime evidence.
- Treat this as maintenance/evidence debt and keep P01 untouched.
