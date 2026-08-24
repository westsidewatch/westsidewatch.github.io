# Researcher 06 — Retention Transfer Practicum 01

Status: PHASE A COMPLETE — IMPLEMENTATION GAP CONFIRMED; PHASE B REQUIRED
Date: 2026-08-24

## Purpose
Test what remains after Researcher 06 graduation without prematurely opening Researcher 07.

## Phase A — current Search implementation inspection
Current `static/dore/dore-search.js` was re-inspected after graduation.

Relevant findings:
- `textSearch()` iterates each verse independently and scores each verse independently;
- reference-range parsing can display an explicitly requested range, but free-text fuzzy retrieval does not construct or score contiguous multi-verse windows;
- fuzzy retrieval is character/surface based (`scoreFuzzy`) rather than a semantic paraphrase candidate generator;
- current plain search therefore cannot distinguish "speaker paraphrased Scripture" from "ASR corrupted a quotation" through a dedicated semantic-vs-correction contract.

## Classification
### Cross-verse quotation
Current status: **IMPLEMENTATION / RETRIEVAL-MODEL GAP CONFIRMED**.

This does not by itself justify a new researcher course. The graduated noise-aware reasoning can still govern evidence, abstention and provenance; the missing mechanism is contiguous-window candidate construction/scoring.

### Paraphrase-vs-correction
Current status: **CAPABILITY QUESTION STILL OPEN**.

The implementation has no semantic paraphrase generator, but absence of an implementation is not yet evidence that Doré needs a new course. A held-out set of genuine paraphrase/corruption contrasts is required before deciding whether the missing piece is ordinary implementation, retention failure, or a reusable semantic-retrieval capability deficit.

## Anti-fabrication boundary
Do not mark this practicum PASS yet. Phase A is architecture inspection, not a transfer exam. Do not infer semantic competence from a fixture whose candidate/anchor is supplied by the fixture itself.

## Phase B required families
A future frozen offline partition should include:
1. quotation spanning adjacent verses;
2. one-verse exact/near-exact controls;
3. genuine paraphrase that should retrieve a passage but must not be labeled a textual correction;
4. ASR corruption that should permit a correction proposal;
5. ambiguous biblical phrase requiring review/abstention;
6. ordinary non-biblical negative.

Outputs must preserve distinct labels for `quotation_recovery`, `paraphrase_retrieval`, `correction_proposal`, `review`, and `abstain` rather than collapsing all successful retrieval into one "corrected" answer.

## Next authorized action
`RESEARCHER_06_RETENTION_TRANSFER_PRACTICUM_01_PHASE_B_DESIGN_FREEZE`.

Design a product-neutral contiguous-window + paraphrase/correction evidence contract and a development-only fixture set. Do not open a fresh final until the development contract is executable and passes. Do not open Researcher 07 unless repeated held-out failures demonstrate a reusable semantic-retrieval deficit.
