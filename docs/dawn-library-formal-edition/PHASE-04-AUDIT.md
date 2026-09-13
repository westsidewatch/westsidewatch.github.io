# Dawn Library Formal Edition — Phase 4 Audit

Status: **PASS**

Phase 4 closes only after both the full-canonical runtime audit and real browser acceptance pass on the formal-edition branch.

## Identity correction discovered during audit

The first 10k+ gate exposed a real adapter defect: the Phase 4 discovery layer treated `dawn:*` as the canonical-ID format and therefore surfaced only 1,040 Works. That assumption was wrong.

`dawn.library.canonical-index.v1` is the identity authority. Authority-backed Works may keep their authority Work ID; `dawn:*` is the deterministic fallback for Works without that authority identity. Phase 4 was corrected to test canonical membership against `canonical.works`, not a string prefix.

This is not a relaxed gate. The corrected audit now requires:

- canonical schema `dawn.library.canonical-index.v1`
- `identityAuthority: Dawn`
- catalog size exactly equal to `canonical.workCount`
- every UI Work ID to exist in `canonical.works`
- both authority-backed IDs and `dawn:*` fallback IDs to remain intact without rewriting

## Final accepted metrics

- Canonical Works: **11,692**
- Authority-backed Works: **10,652**
- `dawn:*` fallback IDs: **1,040**
- Render window: **72 Works**
- Second window offset: **72**
- Full-catalog fuzzy result window: **72**
- `第二聖殿` relation facet results: **7**
- Compare retained canonical refs:
  - `dawn:4ef73b08ef18424f1900`
  - `dawn:157e63ed1adf50df2385`
- CollectionContext schema: `dawn.collection-context.v1`

## Browser acceptance

GitHub Actions run `34722916865` completed successfully.

Passed steps:

1. Full canonical runtime audit
2. Local formal-edition HTTP server boot
3. Headless Chrome acceptance against the real 10k+ canonical catalog
4. Real Phase 4 UI boot smoke test
5. Diagnostics preservation

Browser acceptance result:

`PHASE4_BROWSER_PASS catalog=11692 window=72 offset=72`

Real UI DOM check rendered exactly **72** `.work-token` nodes, proving the 11,692-Work catalog is not expanded into unbounded DOM.

## UI system accepted in Phase 4

- Search / Fuzzy / Facet / Compare mutate or consume the same CollectionContext.
- FLOW / SHELF / SPECTRUM share the same canonical catalog and context.
- Library Card preserves focused Work identity.
- Compare stores canonical Work refs, not copied book identity payloads.
- Cursor state is serializable and restores the large-catalog window.
- Surface relation cues enrich canonical Works but do not own identity.
- Work-token interaction no longer nests a button inside a button; keyboard focus and independent Compare controls are valid interaction primitives.
- `prefers-reduced-motion` and responsive behavior remain in the Phase 4 UI shell.
- No new production runtime dependency was added.

## Phase boundary

Phase 4 is closed as **PASS**.

Formal-edition progress: **4 / 8**.

The next stage may proceed to Phase 5 without changing the Phase 4 identity, bounded-DOM, CollectionContext, or motion/state contracts.
