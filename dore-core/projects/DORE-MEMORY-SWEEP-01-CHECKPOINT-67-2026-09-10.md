# DORÉ MEMORY SWEEP 01 — CHECKPOINT 67 — 2026-09-10

Status: COMPLETE_BOUNDED_BATCH / SWEEP_CONTINUES
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-MULTIWRITE-NATIVE-STRUCTURE-IMPORT-EVIDENCE-LEDGER-2026-09-10.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `aefa5fb60ff53186165db42c041acf21fdd188cb` — EPUB nav/NCX chapter-title support;
- commit `58ba07a2f2eca372f6a45b6687837645b3ecd580` — native chapter structure across imports;
- commit `783ee3efa1e05f8c3d090f60abeacdbe5acef4ee` — shipped source/UI description update;
- affected Multiwrite paths: `static/multiwrite/publication-adapter.mjs`, `static/multiwrite/import.js`, `static/multiwrite/index.html`;
- current canonical `STEWARDSHIP` rule and new-work evidence boundary in `DORÉ-MASTER-WORK-REGISTER.md`.

## Reconciliation findings

1. 多寫 now has a real native-structure-first import implementation. EPUB prefers EPUB3 nav and falls back to NCX/document headings while retaining spine order; DOCX, HTML/XHTML, FB2 and PDF now have format-aware structural readers before generic inference.
2. The older interpretation that non-EPUB imports are uniformly flattened and inferred is `SUPERSEDED_CURRENT_TRUTH` for formats where native structure is available. Generic inference remains a deliberate fallback, not the primary rule.
3. The shipped source and cache-busted UI copy establish `IMPLEMENTED / SHIPPED_SOURCE`, but not browser/runtime acceptance or cross-format correctness.
4. Classification: native import architecture is `ACTIVE / IMPLEMENTED_FOUNDATION`; representative cross-format acceptance remains `UNKNOWN_NEEDS_EVIDENCE`; difficult-structure and dependency-failure coverage is a `COMPLETED_REVISIT_CANDIDATE` rather than a blocker.
5. The canonical register's `STEWARDSHIP` row already governs this as existing-product enrichment (`observe → repair/enrich/upgrade → verify`). This bounded batch does not justify a new priority, status promotion or roadmap interruption, so no canonical-row mutation is necessary.
6. The durable evidence ledger now prevents later memory from collapsing “implementation shipped” into “all advertised import formats verified complete.”
7. No P01 subtitle state, runtime, blocker, ordering, deployment, credential, audio or transcription path was touched.

## Smallest next proof

Run and persist a deterministic representative fixture matrix for EPUB3 nav, EPUB2 NCX, DOCX headings, HTML headings, FB2 nested sections, PDF outline, Markdown fallback and TXT fallback, plus at least one malformed/dependency-failure case. Verify chapter title/order/provenance, fallback semantics, validation and saved/read-back structure before granting a bounded acceptance token.

## Sweep status

Sweep 01 remains `ACTIVE_PARALLEL`. This checkpoint does not justify `VERIFIED_COMPLETE` and introduces no new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition.
