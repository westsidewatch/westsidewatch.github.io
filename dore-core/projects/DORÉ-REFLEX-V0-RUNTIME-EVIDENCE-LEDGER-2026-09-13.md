# DORÉ REFLEX V0 RUNTIME EVIDENCE LEDGER — 2026-09-13

Status: BOUNDED VERIFIED COMPONENT / CORE CONTINUOUS
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Scope

This ledger reconciles the newly merged `local/dore-local/reflex_*` runtime introduced by PR #687 with the older `dore-core/reflex/REFLEX-CONSOLIDATION-1.0.md` lineage.

The two systems share the word **Reflex** but are not the same capability layer:

- **Reflex Consolidation 1.0** is a cognitive/evidence-routing layer for Scripture, retrieval, original-language, witness, entity and geography transfer.
- **Reflex v0 runtime** is an ephemeral canonical-source projection layer for turning admitted document payloads into transient structural events and purpose-specific projections.

Neither supersedes the other.

## Current implementation evidence

PR #687 (`Doré Reflex v0: ephemeral canonical-source projection runtime`) merged to `main` from verified head `26c0402a83ddeb9dd717eeb53f6b0057eb38b026`.

Current runtime contracts establish:

- canonical source identity remains external to Reflex;
- `canonicalId` and `sourcePointer` pass through the runtime unchanged;
- sessions are request-scoped and destructively closed after projection;
- public runtime results do not expose internal Reflex session/event state;
- the runtime exposes one capability, `reflex.project`, rather than one capability per file type;
- supported purpose projections are `text.search`, `publishing.structure`, and `design.structure`;
- lightweight text/Markdown/HTML parsing is native;
- DOCX and XLSX use a narrow optional in-memory MarkItDown adapter;
- unsupported formats fail into a bounded degraded structural result rather than becoming a second persistent substrate;
- the acceptance workflow explicitly rejects `.reflex` / Reflex JSON persistence artifacts.

## CI evidence

At verified head `26c0402a83ddeb9dd717eeb53f6b0057eb38b026`, GitHub Actions recorded:

- `DORE Reflex v0` run `34720842447`: SUCCESS;
- `Doré Capability Runtime` run `34720842353`: SUCCESS;
- `Doré Capability Registry` run `34720842301`: SUCCESS;
- `DORE A2A True Control Plane` run `34720842286`: SUCCESS;
- `Doré Autonomous Loop Contract` run `34720842355`: SUCCESS.

This is sufficient to accept the **Reflex v0 runtime component** as a bounded historical completion milestone.

## Current classification

- Reflex v0 request-scoped projection runtime: `VERIFIED_COMPLETE` as a bounded component milestone.
- Reflex as a system/faculty: `CORE/CONTINUOUS`.
- Cognitive Reflex Consolidation 1.0: remains separately `VERIFIED_COMPLETE` for its own bounded graduation contract.

## Architecture / naming finding

The repository now contains two legitimate but materially different meanings of `Reflex`. That is not a functional defect, but it is a documentation and future-maintenance ambiguity.

Current governing interpretation:

1. **Cognitive Reflex** = learned evidence-routing / transfer behavior.
2. **Projection Reflex** = ephemeral source-to-structure runtime.

Future documents, registry descriptions and project plans should name the layer explicitly when ambiguity is possible. Do not merge their completion claims, tests or provenance.

## Quality judgment

The v0 implementation is strong at its declared boundary: canonical identity discipline, transient lifecycle, fail-closed/no-substrate behavior, lazy dependency loading and capability-bus integration are all explicitly tested.

The evidence does **not** prove:

- broad document-format coverage beyond the currently admitted lightweight + DOCX/XLSX set;
- semantic correctness for every downstream Search/publishing/design use;
- durable visual-design competence;
- large-document performance/cost behavior;
- that cognitive Reflex and projection Reflex should ever be physically unified.

## Capability retention

Retain:

- canonical-source identity passthrough;
- request-scoped destructive sessions;
- provider-neutral structural-event vocabulary;
- purpose projection from one admitted source;
- lazy optional adapter loading;
- degraded-but-bounded unsupported-format behavior;
- hard prohibition on Reflex becoming a second persistence substrate;
- canonical Capability Registry / Capability Bus routing.

## Revisit triggers

Revisit when:

- additional file families are admitted;
- a downstream product demonstrates projection-quality failure;
- large-file latency/memory becomes material;
- Reflex state begins leaking across runtime boundaries;
- naming ambiguity causes architecture or evidence claims to conflate the cognitive and projection layers.

## Smallest next proof

Keep the component closed at v0. Add only evidence-driven extensions: one materially different new format or downstream consumer should demonstrate that the same canonical identity + transient projection contract generalizes without creating persistent Reflex state.

No P01 subtitle runtime, ordering, deployment, credential, binding or blocker condition was changed by this reconciliation.
