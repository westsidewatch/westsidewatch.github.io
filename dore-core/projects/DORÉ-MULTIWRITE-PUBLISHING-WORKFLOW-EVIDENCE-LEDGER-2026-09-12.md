# DORÉ MULTIWRITE PUBLISHING WORKFLOW — EVIDENCE LEDGER — 2026-09-12

Status: ACTIVE / SWEEP-01 DURABLE EVIDENCE
Related workstream: `MULTIWRITE / 成書`
Primary issue: `#674`

## Objective

Transform 多寫 `成書` from a legacy export-menu meaning into a canonical automated publication workflow whose state is owned by `BookModel`, culminating in Doré art direction, formal cover, Web Book/EPUB publication build, validation, and Liming Library publication/read entry.

## Verified bounded implementation

- Issue #674 defines the complete target chain and acceptance boundary.
- Merge commit `d0476fe4ec48367306ffcc2fa019868abb0c63a3` lands the first workflow slice.
- `static/multiwrite/publishing-workflow.mjs` defines `dore.publishing-workflow.v1` with eight ordered publication stages.
- `static/multiwrite/publishing-workflow-ui.mjs` makes the primary `成書` action open the publication workflow rather than the legacy export meaning.
- `static/multiwrite/book-compile-bridge.mjs` compiles current manuscript state through deterministic + Core semantic Book Intelligence, constructs canonical BookModel, applies editorial analysis/mechanical fixes and emits BookBuild/validation metadata.
- `tests/multiwrite-publishing-workflow.test.mjs` verifies workflow start state, author-decision blocking before art direction, and clean editorial advancement to art direction.

## Authority rule retained

Author decisions are a hard workflow gate. A review-required manuscript with unresolved authorial decisions cannot silently progress into automated art direction/publication. This is a product authority boundary, not an environment failure.

## What is not yet proven

- real Doré art-direction output from BookModel;
- final purpose-built cover generation and selection;
- EPUB and Web Book build from the canonical model;
- publication validation against a real manuscript;
- authenticated Liming Library publication/write/readback;
- public book detail + reading entry verification;
- one end-to-end manuscript proving canonical identity/provenance and derived-output behavior;
- final DOCX/PDF derivation after canonical publication state.

## Current classification

`ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`

Issue #674 remains open. Phase 1 is real, but the overall publication workflow is not `VERIFIED_COMPLETE`.

## Superseded interpretation

The primary product meaning `成書 = DOCX/PDF export menu` is `SUPERSEDED`. DOCX/PDF remain valid derived artifacts after publication completion; they are not canonical publication state.

## Dependency boundaries

- `VIS-GRAMMAR`: supplies/validates Doré art direction and purpose-built website/book visual assets.
- `DAWN-LIBRARY`: owns public bookstore/catalog/readback acceptance.
- `MULTIWRITE / 成書`: orchestrates manuscript-to-publication state and must not collapse the independent acceptance gates of those systems.

## Next proof

Use one real manuscript to persist the compile/editorial gate and then implement the `art-direction` stage against the same BookModel. Advance stage-by-stage with durable proof until the same manuscript reaches a public Liming Library reading entry. Only then evaluate the full #674 milestone for `VERIFIED_COMPLETE`.