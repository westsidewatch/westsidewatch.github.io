# Researcher 06 — Retention Transfer Practicum 01

Status: PHASE B DESIGN FROZEN — DEV FIXTURES/HARNESS NEXT
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

## Classification after Phase A
### Cross-verse quotation
Current status: **IMPLEMENTATION / RETRIEVAL-MODEL GAP CONFIRMED**.

This does not by itself justify a new researcher course. The graduated noise-aware reasoning can still govern evidence, abstention and provenance; the missing mechanism is contiguous-window candidate construction/scoring.

### Paraphrase-vs-correction
Current status: **CAPABILITY QUESTION STILL OPEN**.

The implementation has no semantic paraphrase generator, but absence of an implementation is not yet evidence that Doré needs a new course. A held-out set of genuine paraphrase/corruption contrasts is required before deciding whether the missing piece is ordinary implementation, retention failure, or a reusable semantic-retrieval capability deficit.

## Phase B — design freeze completed
Authoritative design record:
`RESEARCHER-06-RETENTION-TRANSFER-PRACTICUM-01-PHASE-B.md`

The frozen product-neutral evidence contract now separates five outcomes:
- `quotation_recovery`;
- `paraphrase_retrieval`;
- `correction_proposal`;
- `review`;
- `abstain`.

The contract also freezes these boundaries:
- observed text is preserved verbatim;
- contiguous adjacent-verse windows are first-class candidates;
- semantic/theological familiarity alone cannot justify correction;
- genuine paraphrase may retrieve a passage but must not be called textual correction;
- ambiguous/conflicting evidence must route to review;
- ordinary negatives must abstain;
- subtitle-like surfaces keep `silent_overwrite=false`;
- Search-like and subtitle-like surfaces may format the same result differently but may not change its evidence class.

## Anti-fabrication / anti-leakage boundary
The practicum is still **not PASS**. A design document is not an executable transfer exam. No fresh-final partition may be opened before a development-only fixture set and executable harness pass the frozen contract. Future final material must not be used for tuning.

## Next authorized action
`RESEARCHER_06_RETENTION_TRANSFER_PRACTICUM_01_PHASE_B_DEV_FIXTURES_AND_HARNESS`.

Build a development-only fixture set covering all six required families and an executable product-neutral harness. Record failures honestly. Do not open Researcher 07 unless repeated held-out failures demonstrate a reusable semantic-retrieval deficit.
