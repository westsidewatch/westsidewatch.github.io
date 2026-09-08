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
3. Checkpoint 47 identified a stale acceptance contradiction: both the canonical runtime registry and the Knowledge Lab registry marked `library.books` as `existing`, while the then-current acceptance script still required the older `planned` behavior.
4. That specific acceptance-contract defect has now been repaired in repository code. Current `local/dore-local/capability_registry_acceptance.py` requires `library.books` to be `existing` and `free-only`, and adds a Core↔Knowledge-Lab parity assertion for overlapping capability statuses.
5. `.github/workflows/dore-capability-registry.yml` now watches the canonical Core registry path in addition to the projection and acceptance files, so future pull requests touching the canonical registry can trigger the registry acceptance job.
6. The repository history contains the corrective commits `074842e302f2fad91e922598b27a21a3d84def68` (`Reconcile capability registry acceptance with promoted library capability`) and `fd2babb18d3c484cb6056b404dd829ad79379c19` (`Watch canonical capability registry in acceptance workflow`).
7. No persisted GitHub Actions workflow run was associated with either corrective commit in the bounded check. Because the workflow is pull-request-triggered and these commits do not themselves provide a durable PASS receipt, the code defect is repaired but fresh current-registry acceptance remains unproven.
8. Therefore the earlier classification must be refined rather than simply closed: acceptance-contract drift = `RESOLVED_IN_CODE`; current acceptance verification = `UNKNOWN_NEEDS_EVIDENCE`; duplicate projection drift risk = still `COMPLETED_REVISIT_CANDIDATE` governance debt.
9. This is maintenance/evidence debt, not a P01 blocker and not a reason to roll back `library.books` or redesign the Capability Registry.

## Classification

- Canonical machine-readable Capability Registry implementation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- Stale `library.books` acceptance assertion: `SUPERSEDED / RESOLVED_IN_CODE` by the current acceptance contract.
- Current registry acceptance: `UNKNOWN_NEEDS_EVIDENCE / VERIFICATION_ONLY` until a fresh successful acceptance run is persisted against the current canonical registry.
- Duplicate Knowledge Lab registry projection: `COMPLETED_REVISIT_CANDIDATE` technical debt; retain parity assertion now, then prefer generated/synchronized projection when dependency-safe.

## Smallest useful next proof

1. Execute `python local/dore-local/capability_registry_acceptance.py` or the `Doré Capability Registry` workflow against the current repository state.
2. Persist the exact `DORE_CAPABILITY_REGISTRY_ACCEPTANCE=PASS` result plus commit/run identity.
3. Keep the new Core↔Knowledge-Lab parity assertion as a regression gate.

Only after that fresh PASS should the Master Register's EVOLUTION next milestone advance from “correct stale acceptance contract” to broader cross-product blind-transfer proof.

No P01 state or action is modified by this finding.
