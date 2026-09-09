# DORÉ Local Control-Plane Registry Drift Evidence Ledger — 2026-09-09

Status: ACTIVE / GOVERNANCE-DRIFT-IDENTIFIED
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Bounded evidence reviewed

- `dore-core/runtime/product-registry.v1.json`
- `dore-core/architecture/DORÉ-SYSTEM-RELATIONSHIP-MAP-v1.md`
- commit `1deb1bebcc5c665d06ab2ea2677862a1687e40c3` — `DORÉ: Local Intelligence Fabric Phase 1`
- recent native-control commits surfaced by commit search, including `83776b45fea89a40de0c73492677deab38ee5acf` and `e8cd4f17789d6f30e1ffcef84488be8ecdf18bd1`

## Reconciliation finding

The high-level product/core relationship doctrine remains valid, but the machine-readable runtime-plane declaration is no longer complete enough to be treated as an exact current transport map.

`product-registry.v1.json` currently declares:

- `dore-local` at `127.0.0.1:8788`;
- `dore-a2a` as `github-event -> self-hosted-runner -> unix-domain-socket -> dore`;
- Design at `127.0.0.1:4310`;
- Image at `127.0.0.1:8790`.

The later Local Intelligence Fabric engineering evidence explicitly adds **Native Messaging production control** and records `local/dore-local/native_host.py` as an A2A/Core entry seam through capability resolution, while preserving the launchd Unix-domain-socket path as a browser-independent activation path. Subsequent September 7–8 commits further harden Native Host production worktree binding and align stale native-host tests with Unix routing architecture.

Therefore this is not evidence that `8788` or the Unix-domain-socket path should be retired. It is evidence that the current registry/runtime-plane model is **incomplete/ambiguous**: Native Messaging is now a real bounded production control path but is not represented as a first-class runtime/control-plane seam in the machine-readable registry.

## Classification

- Core/product relationship doctrine: `CORE/CONTINUOUS`, retain.
- Existing local transports (`8788`, UDS, Native Messaging): `ACTIVE`; no retirement judgment from this batch.
- `product-registry.v1.json` runtime-plane completeness: `COMPLETED_REVISIT_CANDIDATE / GOVERNANCE_DRIFT`.
- Exact transport precedence/fallback semantics across Native Messaging, UDS and localhost service paths: `UNKNOWN_NEEDS_EVIDENCE` until a current machine-readable declaration + tests make the relationship explicit.

## Risk

If the registry is consumed as literal current truth, future engineering can accidentally rebuild an already-promoted transport, route around the Capability Bus, or mistake one compatibility path for the sole canonical production path. This is architecture/governance debt, not evidence of a runtime outage.

## Smallest useful repair

Update the machine-readable registry so it explicitly distinguishes:

1. **capability runtime endpoints** (for example localhost services),
2. **control-plane transports** (Native Messaging / GitHub receiver / UDS activation),
3. **fallback/compatibility paths**, and
4. the invariant that all of them enter Doré through Core capability resolution rather than becoming separate brains.

Then run one bounded acceptance proving the declared routing/fallback model matches the current native-host + UDS implementation.

## P01 isolation

No P01 subtitle code, ordering, runtime, deployment, audio/transcription dependency, credential, or blocker state was changed by this sweep batch.
