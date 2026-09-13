# DORÉ CLOUDFLARE SERVICE + MEDIA-MIGRATION HISTORY EVIDENCE LEDGER — 2026-09-13

Status: COMPLETE / BOUNDED EVIDENCE RECONCILIATION
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Evidence reviewed

- `dore-core/cloudflare/ASSET-MIGRATION-INVENTORY-2026-08-24.md`;
- `dore-core/cloudflare/DORE-SERVICE-LAYER-MILESTONE-2026-08-24.md`;
- current `functions/api/dore/query.js`;
- current canonical Master Register interpretations for `ONE`, `WSS`, `EVOLUTION`, `REFLEX`, and P01.

## Reconciled findings

### 1. Priority-A media migration was a real historical milestone, but its runtime-state instructions are superseded

The 2026-08-24 media inventory documents a legitimate first governed migration milestone: seven Priority-A ONE assets were written to R2, registered in D1, registry-search verified, three obsolete Matthew 3 motion revisions were removed, and the rollback-copy policy correctly prevented premature deletion before runtime delivery existed.

That historical completion remains valid. However, the memo's then-current runtime state—GitHub rollback binaries retained because no R2-backed public delivery path existed—is no longer governing truth. The canonical Master Register now records the later bounded ONE cutover as verified: the seven assets are delivered through asset-code/D1/R2 with hash verification, active references were cut over, and rollback binaries were removed only after post-cutover verification.

**Current classification:**

- 2026-08-24 Priority-A migration milestone: `VERIFIED_COMPLETE` historical precursor;
- its old "R2 written but runtime still on repository paths / keep rollback copies" operational state: `SUPERSEDED`;
- current ONE delivery/runtime state: governed by the later verified private-R2 cutover in the Master Register.

This prevents an old migration memo from reopening already-completed delivery work or reintroducing GitHub/R2 dual-master behavior.

### 2. `dore.query.v1` still exists, but the 2026-08-24 architectural claim must be bounded

`functions/api/dore/query.js` still implements the `dore.query.v1` compatibility contract with status, asset, brain, and scripture routing. The endpoint therefore must not be marked retired or imaginary.

At the same time, the historical service-layer milestone described `/api/dore/query` as the stable cross-product Doré entry contract and named the WSS subtitle proofreader as the next external-worker milestone. The current system has since gained materially newer execution/control abstractions—Capability Registry, A2A execution, projection Reflex—and WSS now has a dedicated `dore.subtitle-proofread.v1` production consumer boundary. Therefore the 2026-08-24 service-layer document is no longer sufficient as a description of Doré's canonical control plane.

The current `query.js` also remains intentionally shallow in one important respect: scripture requests delegate to the browser search dataset rather than executing a unified server-side Scripture/Search capability, while simple regex/heuristic routing remains local to this facade. That is compatible with its original non-destructive milestone, but it should not be promoted into evidence that the later capability architecture has converged behind one execution boundary.

**Current classification:**

- `dore.query.v1` endpoint: `MAINTENANCE / COMPATIBILITY`;
- 2026-08-24 service-layer milestone: `VERIFIED_COMPLETE` for its bounded historical architectural objective;
- its broader "one stable Doré entry contract" interpretation as the system-wide control-plane description: `SUPERSEDED` by later capability/A2A/runtime architecture;
- architectural cleanup/convergence: `COMPLETED_REVISIT_CANDIDATE`, only if future product/runtime work exposes routing duplication, parity drift, or an avoidable maintenance burden.

No endpoint removal is justified from this evidence alone.

## Durable lessons

1. Migration completion and runtime cutover are distinct milestones; do not keep old rollback-state instructions active after cutover is independently verified.
2. A compatibility facade can remain useful after its original architecture narrative is superseded.
3. Historical `COMPLETE / PASS` documents must be interpreted at the exact milestone boundary they proved; they do not freeze later architecture.
4. When newer shared execution systems emerge, older product-neutral routing layers should be evaluated for compatibility value versus duplicated intelligence rather than automatically deleted.

## Revisit trigger

Reopen the `dore.query.v1` compatibility boundary only when one of these becomes true:

- a live consumer depends on behavior that diverges from Capability Registry/A2A semantics;
- duplicated intent/search routing produces a demonstrated parity defect;
- a product needs the facade to expose a capability already standardized elsewhere;
- maintaining the facade creates measurable operational or correctness debt.

Until then, keep it stable and bounded rather than rewriting it for architectural neatness.

## P01 boundary

No P01 file, state, deployment, credential, binding, subtitle job, audio/transcription dependency, blocker classification, or critical-path ordering was modified by this reconciliation.
