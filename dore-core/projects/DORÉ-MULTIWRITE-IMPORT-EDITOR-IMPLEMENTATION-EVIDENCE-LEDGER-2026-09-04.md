# DORÉ MULTIWRITE IMPORT / READER / EDITOR IMPLEMENTATION EVIDENCE LEDGER — 2026-09-04

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md` + `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-DORE-DESIGN-MAC-2026-09-04.md`
Related workstreams: `DORE-DESIGN-PUBLISHING`, `DORE-MAC`, `BOOK-02`
P01 impact: NONE

## Bounded evidence reviewed

- current `static/multiwrite/` implementation family;
- current `tests/multiwrite-import.test.mjs`;
- `.github/workflows/multiwrite-import.yml`;
- commits `eec4a6d0478b87752db5f3e2d77930e64f20933c`, `e47da40ef9ddcf70f7a665a11ffa95c5534c3ee7`, and `748088c9180515b9b090c54be6bec486fcea6429`;
- recent 2026-09-04 commit lineage adding the Kingdom Language manuscript/appendices, reader shell, editable workspace, save/continue-writing behavior and DB compatibility fixes;
- `DORÉ-DESIGN-PUBLISHING-MAC-PRODUCT-DIRECTION-EVIDENCE-LEDGER-2026-09-04.md`;
- `DORÉ-BOOK-02-EDITOR-INTAKE-DIAGNOSTIC-EVIDENCE-LEDGER-2026-09-04.md`.

## What is now materially implemented

1. `static/multiwrite/` is no longer only a product-direction document. A browser product surface exists with import UI, parsing core, library, book reader, editable manuscript workspace and persistent browser-local draft storage.
2. Import v1 has a machine-readable parser/test boundary. `tests/multiwrite-import.test.mjs` verifies chapter/section/appendix detection without rewriting content, preserves multi-file source order, and allows manual role correction while retaining `aiTransformed:false`.
3. A dedicated workflow exists for Import v1 regression and validates the golden Kingdom Language manifest contract. Workflow-file existence is implementation evidence; this bounded pass found no current commit status/workflow-run receipt proving the latest head passed that workflow, so CI success must not be inferred from configuration alone.
4. The Kingdom Language book is materialized as a golden-case content tree under `static/multiwrite/books/`, with chapters and academic appendix content represented in a manifest-driven reader path.
5. Reader editing deliberately separates original imported text from a browser-local working draft: the UI states that the original import is not overwritten, drafts are stored separately in IndexedDB, and save/continue-writing behavior is implemented.
6. The later DB-version fix reconciles homepage/import and editor storage schemas by adding a common v2 database version and `drafts` object store, preventing the reader/editor capability from being stranded behind a mismatched client schema.
7. PDF extraction explicitly fails closed when no selectable text is available; v1 does not silently OCR or fabricate import content.

## Current classification

### Multiwrite browser implementation

`ACTIVE_PARALLEL / IMPLEMENTED_ALPHA`

The product has moved beyond architecture into a real repository implementation and real Book 02/Kingdom Language content integration. It is not `VERIFIED_COMPLETE`: this bounded evidence does not prove latest-head CI PASS, deployed-browser acceptance, cross-browser persistence/recovery, Author Lock semantics beyond source-vs-draft separation, deterministic same-source export, or sustained editorial use.

### Import v1 parser contract

`ACTIVE / BOUNDED_IMPLEMENTATION`

Parser regression tests and a golden manifest exist. The strongest missing proof is an actual passing workflow/run receipt for the latest implementation plus browser acceptance against real MD/DOCX/PDF/text inputs and failure cases.

### Reader/editor working-draft behavior

`ACTIVE / BOUNDED_IMPLEMENTATION`

The source-preservation design is directionally aligned with protected authorship, but browser-local draft separation is not yet equivalent to the full canonical Author Lock/revision/recovery contract.

## Retrospective / quality judgment

### Original objective

Make old manuscripts usable without requiring AI dialogue first: import existing files/text, recover structure, preserve source order and author text, open the manuscript as a book, and allow continued writing/editing without silently overwriting the imported source.

### Current quality

Strong as an early product slice because it joins import, real content, reading and editing in one visible surface rather than leaving them as separate specs. The implementation also makes two sound safety choices: parser tests explicitly preserve source content and PDF import fails closed instead of inventing OCR output.

The main weakness is evidence maturity. Repository commits prove implementation, not durable product acceptance. Browser-local IndexedDB drafts are useful for alpha work but do not yet prove revision history, recovery across storage loss, collaborative identity, deterministic export, production-grade migration/version handling or Mac productization.

### Durable capability retained

`old manuscript → deterministic structural import → preserved source provenance/order → visible reader → separate working draft → save/continue writing`

This is reusable for Book 01, Book 02, Journal special issues and the future Mac product, provided later work keeps source/provenance/presentation/output identities separate.

## Supersession / contradiction findings

1. The earlier Book 02 editor-intake diagnostic ledger correctly said that request commits alone did not prove execution. The later `static/multiwrite/` implementation materially supersedes the implication that Book 02 intake is only a requested diagnostic state: a real manuscript/golden-case reader/editor path now exists in repository code and content.
2. It does **not** supersede the missing proof for the separate local Doré Design Publishing Studio runtime (`127.0.0.1:4310`) or its exact `/api/health`/workspace diagnostic. The browser Multiwrite alpha and the local canonical studio are related surfaces, not evidence-identical runtimes.
3. `Dore / 多寫` commercial readiness remains unproven. A browser alpha is product-truth evidence, not sandbox/signing/privacy/business/App-Store evidence.

## Smallest useful next proof

Persist one bounded acceptance packet containing:

1. latest-head Import v1 workflow PASS receipt;
2. browser import of one real MD/DOCX/selectable-text PDF set plus one text paste;
3. verified structure/source-order/provenance preservation against expected output;
4. open/read the golden manuscript through the real book route;
5. edit one chapter, save a working draft, reload and recover it without changing the imported source;
6. explicit failure evidence for image-only PDF/no-text import;
7. deterministic export/revision proof once that capability is implemented.

Only after that should the alpha be considered for a stronger acceptance milestone.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified.