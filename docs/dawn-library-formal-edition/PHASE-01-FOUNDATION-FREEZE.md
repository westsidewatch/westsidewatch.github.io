# Dawn Library Formal Edition — Phase 1: Foundation Freeze

Status: ACTIVE
Issue: #690
Branch: `dore/dawn-library-formal-edition`

## Project objective

Ship the first production-ready formal edition of Dawn Library using the real 10k+ canonical collection. This is one integrated inside-out project: canonical knowledge, relation, collection context, projections, motion, surfaces, editorial curation, personal state, cross-product context, and production launch.

## Eight-stage delivery plan

1. Foundation Freeze
2. Relation + Context
3. First Vertical Slice
4. Dawn UI System
5. Editorial World
6. Personal Dawn
7. Brand Integration
8. Production Launch

Only Phase 8 production runtime acceptance counts as 100% completion.

## Phase 1 hard outputs

- Freeze Dawn identity authority and existing canonical substrate as non-regression boundaries.
- Inventory current Dawn runtime, surfaces, canonical index, search/display entry points and main-site integration points.
- Freeze the formal contracts for Relation Overlay, CollectionContext, Projection and Motion boundaries before implementation.
- Validate candidate dependencies for license, bundle weight, runtime compatibility and actual need; do not add a dependency merely because it appeared in exploration.
- Establish real-collection performance baselines and select a real Job-related canonical Work set for the first vertical slice.
- Preserve the existing Wikisource ban and external-runtime ban.
- Do not modify the canonical main-site architecture document merely to encode an unapproved navigation hypothesis.

## Architecture invariant

```text
CANONICAL OBJECTS
        ↓
RELATION OVERLAY
        ↓
COLLECTION CONTEXT
        ↓
PROJECTION
        ↓
MOTION
        ↓
SURFACE
```

- Canonical objects own identity.
- Relation Overlay owns typed/provenanced edges, not object identity.
- CollectionContext owns the current way of looking at the collection, not a second catalog.
- Projection maps one context to FLOW / SHELF / SPECTRUM / CARD.
- Motion explains projection/state changes; motion never creates business state.
- Surface owns presentation only.

## Core admission gate

No new Engine/Core subsystem is admitted unless it is all of the following:

1. not cleanly composable from existing capabilities;
2. a stable primitive;
3. reused by at least two independent products;
4. does not duplicate identity, index, embeddings, relations, inference state or canonical content.

Otherwise keep it in projection, orchestration or surface code.

## First vertical-slice acceptance target

Use real Job-related canonical Works and prove:

```text
Canonical Works
→ Relation Overlay
→ CollectionContext
→ FLOW
→ SHELF
→ alternate shelf ordering
→ CARD
→ SPECTRUM
→ return with context intact
→ save Bookmark / View / Trail
```

The same Work IDs must survive the entire route. No demo catalog, copied Work records, or surface-owned identity is acceptable.

## Phase 1 exit gate

Phase 1 may close only when the current runtime inventory, non-regression boundaries, dependency decisions, formal contracts, performance baseline, and first real canonical fixture are all committed and reviewable. Passing documentation alone is not sufficient if the repository/runtime evidence disagrees.
