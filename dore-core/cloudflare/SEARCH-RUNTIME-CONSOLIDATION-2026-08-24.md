# Doré Search Runtime Consolidation — 2026-08-24

Status: **COMPLETE / PASS**

## Goal
Consolidate the browser search lifecycle without rewriting the already-working Scripture Search engine. The runtime must provide one stable extension point for supplemental capabilities while preserving existing routing/interception behavior.

## Change

### Shared runtime lifecycle
Added:

- `static/dore/dore-search-runtime.js`

It observes every `#search-form` submit at the document capture phase and publishes a stable browser event:

- `dore:search-query`

Event detail contains the original query plus references to the active search form/input/results/count/status nodes. Dispatch is deferred to the next task so the existing synchronous search/router pipeline can complete first.

The runtime does **not** replace Scripture Search and does **not** decide search semantics. It is a coordination surface for supplemental search capabilities.

### Entity integration
`static/dore/dore-entity-search.js` no longer owns an independent form-submit hook. It now subscribes to `dore:search-query` and remains lazy-loaded against `/dore/entity-index.json`.

Entity context remains additive: it can prepend identity context but does not replace Scripture Search results.

### Production activation
`static/dore/search/index.html` now loads:

1. `dore-search-runtime.js` before search routers;
2. existing Scripture Search/router modules unchanged;
3. `dore-entity-search.js` as a runtime subscriber;
4. Doré Brain bridge unchanged.

This ordering ensures the runtime can observe submits even when a specialized router later intercepts the request.

## Preserved contracts

No destructive rewrite was made to:

- `dore-search.js`
- `dore-reference-input.js`
- `dore-reference-router.js`
- `dore-search-scope-router.js`
- `dore-chapter-reading.js`
- `dore-brain-bridge.js`

Therefore the milestone preserves the existing execution paths for:

1. direct verse references;
2. chapter and verse-range references;
3. multi-reference input;
4. exact and fuzzy Chinese/English Scripture search;
5. original-language and translated-to-original search;
6. chapter reading;
7. Doré Brain / self-status / asset routing;
8. graceful failure of optional lazy indexes.

Entity identity context is now explicitly activated in the production search page through the shared runtime.

## Runtime boundary

The browser boundary is now:

`form submit -> runtime observation -> existing routers/search engine -> deferred dore:search-query extensions`

This gives later service-layer work a stable browser contract instead of adding more unrelated submit listeners.

## Regression gates for the next milestone

Before replacing any browser implementation with a service call, verify at least these probes:

- `約翰福音 3:16`
- `馬太福音 5`
- `詩篇 23:1-4`
- multiple references in one input
- remembered Chinese phrase / fuzzy phrase
- English phrase
- Greek/Hebrew lemma or surface form
- translated-to-original query
- a person/entity name such as `摩西`
- Doré self-status question
- Doré asset query

## Result

**PASS.** Doré now has one shared supplemental search lifecycle without destabilizing the current Scripture Search engine. The next infrastructure milestone is **Doré Service Layer**: move selected orchestration behind a versioned service contract while keeping this browser runtime as the compatibility boundary.
