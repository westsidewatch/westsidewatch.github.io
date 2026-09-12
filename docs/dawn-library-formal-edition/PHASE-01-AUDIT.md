# Phase 1 Audit — Foundation Freeze

Status: COMPLETE

## Repository evidence

The formal-edition branch preserves the existing Dawn canonical substrate: `static/dawn-library/canonical-index.json`, `surfaces/dawn-storefront.json`, and `surfaces/multiwrite-biblical-world.json`. The canonical index is a generated multi-megabyte artifact; the formal edition must never duplicate the full catalog into rendered DOM state.

The persisted Biblical World surface already references canonical `dawn:*` Work IDs and points back to `../canonical-index.json`. Eight persisted refs are frozen as the first real vertical-slice seed. We do not invent Job metadata merely to satisfy a fixture name: Phase 2 must derive/prove the Job anchor through the relation layer before calling the slice Job-related.

## Non-regression boundaries

- Dawn remains identity authority for Work / Edition / Resource / Artifact.
- Surfaces reference canonical IDs and do not own a second catalog.
- Wikisource remains forbidden.
- External discovery/reconciliation sources do not become runtime reading or identity dependencies.
- Existing main-site architecture is not changed in Phase 1.

## Formal contracts frozen

Phase 1 commits v1 schemas for `dawn.relation-overlay.v1`, `dawn.collection-context.v1`, and `dawn.projection.v1`. Personal relations are intentionally excluded from the public Relation Overlay schema; they belong to Personal Knowledge State in Phase 6.

## Dependency decision

No explored UI/graph dependency is admitted in Phase 1. Graphology, PixiJS, VIKUS-derived patterns, TanStack Virtual, Muuri/Packery, Motion, Embla and Sigma remain candidates. Admission is deferred until an exact Phase 2–4 implementation need proves bundle/runtime/license value. This prevents exploration from becoming dependency accumulation.

## Performance baseline

The first baseline is architectural and payload-based: the canonical index is multi-megabyte while persisted surface manifests are small canonical-reference lists. Formal Edition therefore uses bounded candidate windows and projection-specific payloads. It must not ship the entire canonical index into a rendered Surface or instantiate 10k+ DOM cards. Phase 3 adds interaction/frame/runtime measurements against the real vertical slice; Phase 8 repeats them against the full production catalog.

## Phase 1 exit decision

PASS.

Identity/runtime boundaries are frozen, Relation/Context/Projection contracts are committed, dependency admission is constrained, a real canonical fixture is committed, and the first performance invariant is explicit. Phase 2 may begin. Documentation is not treated as proof where repository evidence differs.