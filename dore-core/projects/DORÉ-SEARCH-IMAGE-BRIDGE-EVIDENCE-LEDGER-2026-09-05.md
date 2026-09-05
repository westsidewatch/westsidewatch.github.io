# DORÉ SEARCH → RESIDENT IMAGE BRIDGE EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SEARCH-IMAGE-BRIDGE-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `3d2a288f1875c45c5d6df2df7690c7b1b627236f` — `Connect Doré Search AI directly to resident Image`;
- follow-on hardening commit `851ad1fbd9dfddb96656da2a2bc1db13259312f4` — `Harden Doré Image local bridge before live render`;
- existing sparse capability/runtime and A2A control-plane canonical addendum.

## Current classification

### Search AI → resident Image command surface
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

A real browser-facing image-command path now exists. Search AI mode can recognize bounded natural-language image requests, call a local Image bridge, queue a resident Image job, invoke the resident autorun seam, and return a generated artifact reference to the Search conversation surface. The follow-on hardening removes workstation-path leakage, constrains request size/shape, narrows served image types, and preserves loopback-only execution.

This is repository implementation evidence. It is not a live real-render acceptance result and does not prove full Doré Image readiness.

## Architecture judgment

The new `127.0.0.1:8790` bridge is useful as a bounded local compatibility/product surface, but it introduces an architectural tension with the already-canonical direction that normal capabilities should converge through one typed control plane / one persistent intelligence rather than multiplying product-specific localhost control services.

Therefore:

- the Search-facing image experience is a legitimate product integration submilestone;
- the direct `Search browser → localhost:8790 → resident Image` route is **not** promoted as the long-term canonical control-plane architecture;
- retain `8790` as `MAINTENANCE / COMPATIBILITY` while the shared typed-control path is proven;
- future consolidation should route the same Search image intent through the shared capability/control-plane seam without changing the reader-facing behavior.

This is not a failure and not a blocker. It is technical-debt / convergence evidence.

## Quality / safety judgment

The hardening follow-up materially improves the local bridge before real-media use:

- loopback host only;
- constrained allowed origins;
- explicit private-network CORS handling;
- request-size and request-field validation;
- file-name/path traversal protection;
- narrow image MIME/extension allowlist;
- browser-safe artifact metadata that excludes workstation paths;
- generic exception names instead of private exception strings.

These are meaningful defensive improvements. They do not substitute for authority/authentication proof: the `X-Dore-Origin: dore-search` header and browser origin checks are routing guards, not cryptographic authorization.

## Evidence boundary

No bounded evidence in this pass proves:

- a configured real resident renderer successfully generated media through this Search path;
- visual critique/correction completed on a real asset;
- Search → Image → Design shared-state transfer;
- shared-control-plane parity with the direct 8790 path;
- cryptographically trustworthy mutation authority;
- latest-head CI PASS for the introducing/hardening commits.

## Revisit / supersession judgment

`COMPLETED_REVISIT_CANDIDATE` for the direct local service boundary, while the reader-facing Search image command remains active.

Revisit trigger: once the shared Companion/A2A/capability control plane has live acceptance, migrate Search image intent onto that seam and compare behavior, latency, privacy and failure handling. Retire the product-specific `8790` control endpoint if no isolation requirement remains.

## Smallest next proof

1. one real purpose-built Westside asset generated from Search through a configured resident renderer;
2. persisted artifact checksum/provenance and real visual review;
3. equivalent request routed through the shared typed capability plane;
4. negative unauthorized-request test;
5. latest-head CI/runtime receipt.

## P01 isolation

No P01 subtitle/runtime/deployment/audio-transcription state, ordering or blocker was modified.