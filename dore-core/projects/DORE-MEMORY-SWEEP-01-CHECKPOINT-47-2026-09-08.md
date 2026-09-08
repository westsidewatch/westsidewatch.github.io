# DORÉ MEMORY SWEEP 01 — CHECKPOINT 47

Date: 2026-09-08
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-CAPABILITY-REGISTRY-DRIFT-EVIDENCE-LEDGER-2026-09-08.md`

## Bounded evidence reviewed

- `dore-core/runtime/capability-registry.v1.json`
- `local/dore-local/capability_registry.py`
- `local/dore-local/capability_registry_acceptance.py`
- `dore-design/knowledge-lab/capabilities/registry.json`
- `.github/workflows/dore-capability-registry.yml`

## Reconciliation findings

1. The Evolution architecture's Capability Registry is no longer only a future idea. A canonical machine-readable registry exists under `dore-core/runtime/`, is explicitly owned by `dore-core`, and has a working filtered discovery/lookup reader.
2. This is bounded implementation progress, not evidence that every product uses discovery, not evidence of cross-product capability transfer, and not evidence of broad self-equipping autonomy.
3. Current acceptance evidence is stale: both the canonical runtime registry and Knowledge Lab registry mark `library.books` as `existing`, while `capability_registry_acceptance.py` still requires it to be absent from default discovery and to be `planned` when `include_planned=True`.
4. Therefore current Capability Registry acceptance is `UNKNOWN_NEEDS_EVIDENCE / MAINTENANCE`; any older PASS cannot govern after the Library capability promotion without a fresh run against the current contract.
5. The Knowledge Lab registry currently matches the overlapping statuses reviewed, but retaining two independently edited registry copies creates drift risk. Canonical ownership remains the Core runtime registry.
6. The useful canonical correction is interpretive: the Master Register's EVOLUTION phrase `future machine-readable Capability Registry` is now stale and is superseded by this checkpoint/ledger as `implemented foundation, acceptance drift open` pending textual row reconciliation.
7. No P01 subtitle ordering, deployment, credentials, audio, transcription, runtime or blocker condition was touched.

## Classification updates

- Machine-readable Capability Registry foundation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` under `EVOLUTION`.
- Current registry acceptance: `MAINTENANCE / UNKNOWN_NEEDS_EVIDENCE` until stale Library assertions are corrected and a fresh PASS is persisted.
- Duplicate registry projection: `COMPLETED_REVISIT_CANDIDATE` governance debt; converge on Core-owned generation/synchronization when dependency-safe.

## Smallest next proof

Update the acceptance script so `library.books` is expected as `existing`, run the current workflow, persist a fresh PASS, and add one Core↔Knowledge-Lab parity assertion or generate the projection from the canonical Core registry.

Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and does not create a new human/environment blocker.
