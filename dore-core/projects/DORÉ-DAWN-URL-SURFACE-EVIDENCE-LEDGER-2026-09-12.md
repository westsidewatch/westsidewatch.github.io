# DORÉ DAWN URL SURFACE EVIDENCE LEDGER — 2026-09-12

Status: ACTIVE EVIDENCE LEDGER
Related workstreams: `DAWN-LIBRARY`, `EVOLUTION`, `NERVOUS-SYSTEM`, `MEM-SWEEP-01`

## Evidence

### Commit `40e38e21fb621721b01ae1388d19dec97d71ef8a`
Introduced a provider-neutral URL-surface contract over Dawn's external discovery pointers, including:
- deterministic pointer routing;
- a real-corpus benchmark over the existing 900+ discovery set;
- a pointer-only external surface index;
- live-probe tooling;
- public Dawn Web Surface integration for approved Project Gutenberg catalog pointers;
- unit/contract tests and a dedicated workflow.

The governing boundary is explicit: presentation is not admission. Successful preview must not promote, delete or take ownership of an external resource.

### Commit `8112d1c2dffb1e87d4b3fe3c098085edae5f37dd`
Introduced `SurfaceMountRegistry` and `SurfacePlan`, separating route selection from equipment that is actually mounted. Current bounded inventory recorded by the implementation:
- `bibliographic-page`: `mounted`, scoped to Project Gutenberg;
- `iiif-visual-surface`: `dormant`;
- `pdfjs`: `dormant`;
- `book-reader`: `dormant`;
- `zotero-translate`: `dormant`;
- `oembed-opengraph`: `dormant`;
- `readability`: `dormant` fallback.

The test contract requires route truth and mount truth to remain distinct and asserts that the current discovery corpus is executable through the mounted Gutenberg surface without mutating candidate data.

## Classification

| Item | Classification | Evidence boundary |
|---|---|---|
| URL-surface resolver | `VERIFIED_COMPLETE / COMPONENT` | Real implementation + bounded acceptance contract |
| Mount-truth registry | `VERIFIED_COMPLETE / COMPONENT` | Real implementation + bounded acceptance contract |
| Gutenberg Web Surface | `VERIFIED_COMPLETE / BOUNDED PRODUCT COMPONENT` | Repository integration and contract evidence; production readback still open |
| IIIF/PDF/EPUB-MOBI/Zotero/general-web adapters | `READY / NOT MOUNTED` | Routed contracts exist; executable equipment is not mounted |
| Heterogeneous external-reading system | `ACTIVE_PARALLEL / UNKNOWN_NEEDS_EVIDENCE` | Requires additional mounted adapters and persisted real execution evidence |
| “route implies executable capability” assumption | `SUPERSEDED` | Replaced by explicit mount truth |

## Retained capability

Durable principle:

`discoverable/routable capability ≠ mounted/executable capability`

Any future Doré capability registry, executive router, self-equipping loop or product orchestration should expose both planning truth and execution truth. A named adapter, route, provider or skill is not evidence that the equipment is installed, authorized, healthy or runnable.

## Non-conflation rules

- Preview/render success does not prove editorial relevance.
- Preview/render success does not admit a candidate into Dawn.
- External pointers remain externally owned.
- A routed dormant adapter is not a completed integration.
- Repository tests are not production readback.

## Open proof

Smallest useful next proof:
1. persist a fresh acceptance/CI PASS for the mount-truth gate;
2. production-readback one approved Gutenberg item through the mounted Web Surface;
3. mount one materially different adapter such as direct PDF or IIIF;
4. verify fallback/refusal and no mutation of discovery/admission state.

## Sweep linkage

Reconciled by `DORE-MEMORY-SWEEP-01-CHECKPOINT-83-2026-09-12.md`.