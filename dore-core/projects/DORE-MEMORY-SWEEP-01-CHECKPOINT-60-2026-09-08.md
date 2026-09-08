# DORÉ MEMORY SWEEP 01 — CHECKPOINT 60

Date: 2026-09-08
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-CAPABILITY-REGISTRY-DRIFT-EVIDENCE-LEDGER-2026-09-08.md`

## Bounded evidence reviewed

- Checkpoint 47 Capability Registry drift finding;
- current `dore-core/runtime/capability-registry.v1.json`;
- current `local/dore-local/capability_registry_acceptance.py`;
- current `.github/workflows/dore-capability-registry.yml`;
- corrective commits `074842e302f2fad91e922598b27a21a3d84def68` and `fd2babb18d3c484cb6056b404dd829ad79379c19`;
- bounded workflow-run lookup for those corrective commits.

## Reconciliation findings

1. The stale `library.books` acceptance assertion identified in Checkpoint 47 has been repaired in code. The current acceptance script now requires `library.books` to be `existing` and `free-only`.
2. A new parity assertion prevents overlapping capability statuses in the Knowledge Lab projection from silently contradicting the canonical Core registry.
3. The GitHub Actions workflow now watches `dore-core/runtime/capability-registry.v1.json`, closing the earlier trigger gap where canonical registry edits could evade the acceptance workflow's path filter.
4. Repository history provides exact repair provenance through commits `074842e...` and `fd2babb...`.
5. No persisted workflow run was associated with either corrective commit in the bounded lookup. Therefore the defect is `RESOLVED_IN_CODE`, but a fresh current-registry PASS remains `UNKNOWN_NEEDS_EVIDENCE`; older PASS claims must not be reused automatically.
6. The Master Register's EVOLUTION row is now partially stale only in its wording: “correct the stale Capability Registry acceptance contract” has been satisfied in code, while “persist a fresh PASS” remains the smallest unfinished proof. The underlying EVOLUTION status stays `CORE/CONTINUOUS / ACTIVE_PARALLEL` and the Capability Registry remains `IMPLEMENTED_FOUNDATION`.
7. Duplicate Core/Knowledge-Lab registry storage remains `COMPLETED_REVISIT_CANDIDATE` governance debt even though the new parity check reduces immediate risk.
8. No P01 subtitle ordering, deployment, credential, audio/transcription path, runtime state or existing environment blocker was touched.

## Classification updates

- stale `library.books` acceptance contract: `SUPERSEDED / RESOLVED_IN_CODE`;
- Capability Registry implementation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`;
- current-registry acceptance receipt: `UNKNOWN_NEEDS_EVIDENCE / VERIFICATION_ONLY`;
- duplicate registry projection: `COMPLETED_REVISIT_CANDIDATE`.

## Smallest next proof

Run the current registry acceptance against current repository state and persist `DORE_CAPABILITY_REGISTRY_ACCEPTANCE=PASS` with commit/run identity. After that, advance EVOLUTION's next milestone to materially different-domain blind transfer without method re-teaching.

Sweep 01 remains `ACTIVE_PARALLEL`; this batch creates no new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition and does not justify `VERIFIED_COMPLETE`.
