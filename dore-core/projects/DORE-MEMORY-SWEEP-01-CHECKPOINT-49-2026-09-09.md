# DORÉ MEMORY SWEEP 01 — CHECKPOINT 49

Date: 2026-09-09
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-LOCAL-CONTROL-PLANE-REGISTRY-DRIFT-EVIDENCE-LEDGER-2026-09-09.md`

## Bounded evidence reviewed

- `dore-core/runtime/product-registry.v1.json`
- `dore-core/architecture/DORÉ-SYSTEM-RELATIONSHIP-MAP-v1.md`
- Local Intelligence Fabric Phase 1 commit `1deb1bebcc5c665d06ab2ea2677862a1687e40c3`
- bounded recent commit history for native-host / Native Messaging control-plane hardening

## Reconciliation findings

1. The one-Doré / products-as-consumers relationship doctrine remains current and coherent.
2. The runtime-plane section of the machine-readable product registry is no longer a complete literal transport map. It names localhost `8788`, GitHub→runner→UDS A2A, Design `4310`, and Image `8790`, while later engineering has promoted Native Messaging into a real production control path entering Core through capability resolution.
3. Later evidence preserves the Unix-domain-socket path as a browser-independent activation seam, so this batch does not retire UDS or localhost runtimes. The correct classification is registry/governance drift, not transport failure.
4. `product-registry.v1.json` runtime-plane completeness is now `COMPLETED_REVISIT_CANDIDATE / GOVERNANCE_DRIFT`; exact precedence/fallback semantics among Native Messaging, UDS and localhost service paths remain `UNKNOWN_NEEDS_EVIDENCE` until declared and tested explicitly.
5. The smallest repair is to separate capability endpoints, control-plane transports and fallback/compatibility paths in the machine-readable registry, while preserving the invariant that every path enters Core capability resolution rather than becoming a second brain.
6. This finding should be folded into the canonical Master Register's `EVOLUTION` / runtime governance interpretation during the next safe whole-file reconciliation; it does not justify changing P01 or declaring a new environment/human blocker.
7. No P01 subtitle ordering, code, deployment, credential, audio, transcription, runtime or blocker condition was modified.

## Current disposition

- relationship doctrine: retain `CORE/CONTINUOUS`;
- Native Messaging / UDS / localhost execution seams: retain `ACTIVE` pending explicit routing map;
- machine-readable runtime-plane declaration: `COMPLETED_REVISIT_CANDIDATE`;
- sweep: remains `ACTIVE_PARALLEL`.

Sweep 01 is not `VERIFIED_COMPLETE` from this batch and no new `HUMAN_DECISION_BLOCKED` / `ENVIRONMENT_BLOCKED` condition was discovered.
