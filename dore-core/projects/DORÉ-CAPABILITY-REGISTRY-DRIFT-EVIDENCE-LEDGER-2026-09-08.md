# DORÉ CAPABILITY REGISTRY DRIFT — EVIDENCE LEDGER

Status: ACTIVE / SWEEP-01 EVIDENCE
Date: 2026-09-08
Related work: `EVOLUTION`, `SEARCH`, `LIBRARY-INGEST`, `NERVOUS-SYSTEM`
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

## Bounded evidence reviewed

- `dore-core/runtime/capability-registry.v1.json`
- `local/dore-local/capability_registry.py`
- `local/dore-local/capability_registry_acceptance.py`
- `dore-design/knowledge-lab/capabilities/registry.json`
- `.github/workflows/dore-capability-registry.yml`

## Findings

1. A machine-readable Capability Registry is no longer merely future architecture. A canonical runtime registry exists at `dore-core/runtime/capability-registry.v1.json`, is explicitly owned by `dore-core`, and is consumed by `local/dore-local/capability_registry.py` for filtered discovery and lookup.
2. The runtime registry currently declares existing capabilities for Scripture Search, original-language Search, Library books, heritage maps/images and Westside context, while academic scholarship remains planned. This is real bounded implementation progress toward the Evolution doctrine's Capability Registry, but not proof that every product discovers capabilities through it or that self-equipping autonomy is operational.
3. A stale acceptance contradiction exists. Both the canonical runtime registry and the Knowledge Lab registry now mark `library.books` as `existing`, but `local/dore-local/capability_registry_acceptance.py` still asserts that `get('library.books') is None` unless `include_planned=True`, and then requires the status to be `planned`.
4. Therefore the current `Doré Capability Registry` GitHub Actions acceptance contract is internally inconsistent with the repositories it is supposed to validate. A passing historical run, if any, must not be treated as current-registry acceptance after the `library.books` status promotion.
5. This is a maintenance/evidence-drift defect, not a P01 blocker and not a reason to roll back the Library capability. The correct repair is to update the acceptance contract to the canonical `existing` state, then execute and persist a fresh passing acceptance run.
6. The duplicate Knowledge Lab registry is currently aligned for the overlapping entries reviewed, but canonical ownership belongs to `dore-core/runtime/capability-registry.v1.json`; long-term drift risk remains if two registry copies are edited independently.

## Classification

- Canonical machine-readable Capability Registry implementation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- Current registry acceptance: `UNKNOWN_NEEDS_EVIDENCE / MAINTENANCE` because the checked acceptance script contains a stale assertion.
- Duplicate registry-copy governance: `COMPLETED_REVISIT_CANDIDATE` technical debt; converge generation/synchronization on the canonical Core registry rather than allowing silent divergence.

## Smallest useful next proof

1. Update `capability_registry_acceptance.py` so `library.books` is expected as `existing` and discoverable by default.
2. Run the workflow against the current canonical registry and persist a fresh PASS.
3. Add one parity assertion that the Knowledge Lab projection cannot contradict canonical Core status for shared capability IDs, or generate the projection from Core.

No P01 state or action is modified by this finding.
