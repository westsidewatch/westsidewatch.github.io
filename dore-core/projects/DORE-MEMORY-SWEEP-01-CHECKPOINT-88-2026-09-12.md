# DORÉ MEMORY SWEEP 01 — CHECKPOINT 88 — 2026-09-12

Status: COMPLETE / BOUNDED BATCH
Sweep: `MEM-SWEEP-01`
P01 constraint: subtitle critical-path state was not modified.

## Evidence reviewed

- GitHub issue `#674` — `成書工作流：BookModel → Doré 美術總監 → 封面 → EPUB/Web Book → 黎明書局`;
- merge commit `d0476fe4ec48367306ffcc2fa019868abb0c63a3` and its Phase 1 implementation slice;
- `static/multiwrite/publishing-workflow.mjs`;
- `static/multiwrite/book-compile-bridge.mjs`;
- `tests/multiwrite-publishing-workflow.test.mjs`;
- current canonical Master Register, which does not yet expose 多寫 / Doré Folio `成書` as its own operational workstream.

## Findings

1. `成書` is now a real active product/architecture workstream, not a generic export affordance. Issue #674 defines the target chain as `稿件 → Book Intelligence → Editorial Gate → BookModel → Doré 美術總監 → 自動封面 → Web Book → EPUB → 黎明書局上架`, with DOCX/PDF explicitly demoted to derived outputs after publication-state completion.
2. Phase 1 is a legitimate implemented foundation. `dore.publishing-workflow.v1` defines eight ordered stages: whole-book understanding, editorial check, author decision, art direction, formal cover, publication build, publication validation and Liming Library publication. The primary `成書` action now opens this workflow rather than meaning “open export menu”.
3. The author-authority boundary is materially encoded. `workflowFromCompile` blocks progression before art direction when editorial readiness is blocked or authorial decisions remain. This is reinforced by tests proving that authorial decisions lock later stages rather than being silently auto-resolved.
4. `book-compile-bridge.mjs` already connects deterministic + Core semantic Book Intelligence, merges the report, constructs canonical `BookModel`, runs publication editorial analysis/mechanical fixes, emits validation metadata and creates a `BookBuild`. Semantic failure degrades safely rather than invalidating the whole compile path.
5. The current milestone is **not end-to-end publication completion**. Phase 1 advances only to workflow/state ownership and the existing compile/editorial foundation. No evidence in this bounded batch proves real Doré art direction output, generated final cover, EPUB/Web Book build, publication QA, Liming Library write/readback, or a real manuscript reaching the public reading entry.
6. The correct current classification is `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`, with issue #674 still open. A `VERIFIED_COMPLETE` claim would be premature.
7. The Master Register has an operational omission: 多寫 / Doré Folio is a major active product surface but is not represented as a first-class row. The canonical register should add a `MULTIWRITE / 成書` workstream rather than hiding this work under Library or visual grammar.
8. This workstream depends on, but must remain distinct from, `VIS-GRAMMAR` (purpose-built Doré asset/art-direction language) and `DAWN-LIBRARY` (public catalog/storefront). The publication workflow should orchestrate those capabilities without collapsing their independent acceptance gates.
9. No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition was discovered. Author-decision stops are expected product authority gates, not environment blockers.
10. No P01 runtime, deployment, blocker, audio/transcription dependency, binding, credential, ordering or resume condition was changed.

## Current disposition

- 多寫 / Doré Folio product: retain as active.
- `成書` publication workflow Phase 1: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- issue #674 full target: `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` until a real manuscript reaches the public reading/storefront endpoint.
- legacy interpretation `成書 = DOCX/PDF export`: `SUPERSEDED` as the primary product meaning; export remains downstream artifact machinery.

## Smallest useful next evidence

Run one real manuscript through the existing compile/editorial gates; persist author-decision behavior if present; then implement and verify the next stage boundary (`art-direction`) using the canonical BookModel. Continue through cover/build/validation/storefront in separate bounded proofs, preserving BookModel identity and provenance. The final acceptance must include public Liming Library/read-entry readback and prove DOCX/PDF are derived outputs rather than canonical state.

## Sweep disposition

This checkpoint adds a materially missing active workstream and supersession finding. Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and creates no user-notification condition.