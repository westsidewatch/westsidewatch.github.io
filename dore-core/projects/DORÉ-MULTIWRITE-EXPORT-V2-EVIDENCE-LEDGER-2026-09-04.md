# DORÉ MULTIWRITE EXPORT V2 EVIDENCE LEDGER — 2026-09-04

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md` + `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-DORE-DESIGN-MAC-2026-09-04.md`
Related workstreams: `DORE-DESIGN-PUBLISHING`, `DORE-MAC`, `BOOK-02`
P01 impact: NONE

## Bounded evidence reviewed

- commits `60e416f6caa2218ceaf00c76c14f1022b0c7a1d4`, `2c93e4c2cf95f40747c9ec9f7e983a5b7e830a11`, `ba2321103c8ef1205aa235c1e24197eb952fbf5f`, `e51c40ebf1b738f5dc1dcfb51e46ed62c3cd0900`, `5fefd9b74e3d8441affdcf170b4518d8573e4eca`, `a392c13d4731a195d37fe0eb21ea29cee3eab841`, `d9841915f3435c6374b0ab53703a60fe9b9e2057`, `ad669e71616c269b9a3e4ac8c7b64121d37a0b63`;
- current `static/multiwrite/export-core.mjs` / `static/multiwrite/export.js` implementation lineage;
- `tests/multiwrite-export.test.mjs`;
- `.github/workflows/multiwrite-import.yml`;
- prior `DORÉ-MULTIWRITE-IMPORT-EDITOR-IMPLEMENTATION-EVIDENCE-LEDGER-2026-09-04.md` and Checkpoint 44 interpretation.

## Classification

### Multiwrite deterministic export core

`ACTIVE_PARALLEL / IMPLEMENTED_ALPHA`

Whole-book export is now materially implemented beyond the earlier “missing deterministic export” state. The browser path collects the manifest-defined structure in source order, uses saved working drafts where present and original imported content otherwise, and exposes Markdown, TXT and JSON backup export. The regression test verifies source-order preservation without rewriting section text, JSON backup preservation of complete text + draft state, and filename sanitation.

### DOCX + print/PDF export

`ACTIVE_PARALLEL / BOUNDED_IMPLEMENTATION`

A DOCX path and a print-ready HTML/PDF path now exist in repository code. The DOCX route uses the `docx` browser bundle and produces a structured document with title/subtitle, section headings and page breaks. The PDF path produces a print-oriented A4 HTML document and invokes browser print/save-as-PDF. This is real implementation evidence, but not yet a print-quality acceptance milestone.

## Evidence boundary

1. Export is no longer merely a future requirement. Repository implementation and a dedicated export regression test exist.
2. The export regression currently proves deterministic merge/order/backup logic, not byte-identical DOCX/PDF output, typography fidelity, page-break quality, bilingual font availability, images/footnotes/tables, print color handling, or round-trip re-import.
3. The workflow now explicitly runs both import and export regression tests and triggers on `static/multiwrite/**` plus both test files. This is a stronger machine-test contract than Checkpoint 44.
4. No successful workflow-run/status receipt was found for the latest export head in this bounded pass. `fetch_commit_workflow_runs` returned no run for latest commit `ad669e71616c269b9a3e4ac8c7b64121d37a0b63`, and combined commit status exposed no checks. Therefore workflow configuration and test files must not be inflated into CI PASS.
5. DOCX currently loads its library from jsDelivr at export time. This is acceptable alpha evidence but is not yet an offline/local-first or packaged-Mac dependency proof.
6. PDF export currently depends on browser popup + print behavior. That is not deterministic cross-browser PDF rendering proof and should not be called print-ready final output without acceptance evidence.
7. The implementation preserves the important source/draft boundary during export: current working drafts are exported where they exist, while the original imported source remains separately stored. This advances the publishing architecture but still does not equal the full Author Lock/revision/recovery contract.

## Retrospective / quality judgment

### Original objective

Make Multiwrite capable of taking the same manuscript state used for reading/editing and producing whole-book outputs without manual copy/paste or silent rewriting.

### Current quality

Strong alpha progress: export is integrated into the actual editor surface and shares the same manifest + draft state rather than creating a disconnected export-only content model. The JSON backup format is particularly useful as a provenance/recovery bridge.

The primary weakness is acceptance depth. The core textual merge is tested, while the high-risk formats—DOCX and PDF—are still implementation-first. Production publishing quality requires real artifact inspection, especially Chinese typography, pagination, section hierarchy, print equivalence and deterministic repeatability.

## Durable capability retained

`manifest/source tree + preserved original + working draft state → one canonical whole-book collection → multiple export adapters`

This is reusable across Book 01, Book 02, Journal specials and future Mac packaging, provided adapters never become separate manuscript authorities.

## Supersession / revisit judgment

The prior statement “deterministic export is not yet implemented” is now `SUPERSEDED` as an implementation claim. The remaining acceptance claim is narrower and current: export exists, but deterministic artifact-quality verification remains `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` for DOCX/PDF and real-browser output.

No completed-work revisit or retirement classification applies because the workstream is active.

## Smallest useful next proof

Persist one export acceptance packet from the Kingdom Language golden manuscript:

1. latest-head workflow PASS receipt for import + export regressions;
2. export MD/TXT/JSON twice from the same unchanged state and verify identical semantic content/order;
3. export one DOCX and inspect title/section hierarchy, Chinese text fidelity and page-break behavior;
4. export one PDF through the supported browser path and inspect A4 pagination, CJK font fallback, widows/orphans and section starts;
5. edit one chapter, re-export and prove only the expected manuscript delta changes;
6. preserve the original imported source separately and prove export does not mutate it;
7. record any dependency/offline limitation before using this as Mac-readiness evidence.

Only after that should export be promoted from implemented alpha to a stronger product-acceptance milestone.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified.