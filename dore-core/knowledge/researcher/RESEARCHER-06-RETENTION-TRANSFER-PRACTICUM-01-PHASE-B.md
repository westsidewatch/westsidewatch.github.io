# Researcher 06 — Retention Transfer Practicum 01 / Phase B

Status: DEV GATE PASS — SEALED HELD-OUT DESIGN AUTHORIZED
Date: 2026-08-24

## Product-neutral evidence contract

Purpose: distinguish contiguous Scripture quotation recovery, semantic paraphrase retrieval, textual correction proposal, review, and abstention without product-specific routing.

### Inputs
- `observed_text`: preserve verbatim.
- optional surrounding context.
- candidate passages/windows from retrieval.
- surface: `search_like`, `subtitle_like`, or `neutral`.

### Candidate evidence
Each candidate must preserve:
- stable passage/window ID and human-readable reference;
- canonical candidate text;
- contiguous window size;
- source/corpus provenance;
- available evidence channels: surface similarity, phonetic similarity, semantic support, contiguity.

### Outcome classes
- `quotation_recovery`
- `paraphrase_retrieval`
- `correction_proposal`
- `review`
- `abstain`

### Decision boundaries
1. `quotation_recovery` requires strong textual and/or phonetic evidence. It may span adjacent contiguous verses. It never silently rewrites `observed_text`.
2. `paraphrase_retrieval` requires semantic support for a passage while explicitly denying textual-equivalence or correction status.
3. `correction_proposal` requires evidence that the observed wording is plausibly corrupted relative to a source; the correction remains a proposal.
4. `review` is required when materially different candidates remain close or evidence channels conflict.
5. `abstain` is required for ordinary negatives or insufficient evidence.
6. Semantic/theological familiarity alone may never justify `correction_proposal`.
7. Every positive result preserves observation, source, evidence channels, uncertainty, and alternatives where material.
8. Surface adapters may format results differently but may not alter the evidence class.

### Required output shape
- `observed_text`
- `outcome`
- `candidate` or null
- `alternatives`
- `reason_codes`
- `provenance`
- `silent_overwrite: false`

## Development gate families
The dev set must contain all six families:
1. adjacent-verse quotation;
2. one-verse exact/near-exact control;
3. genuine paraphrase;
4. ASR corruption;
5. ambiguous biblical phrase;
6. ordinary non-biblical negative.

The dev gate passes only if:
- every fixture receives the expected outcome class;
- every positive result preserves provenance;
- no genuine paraphrase is mislabeled `correction_proposal`;
- no ordinary negative yields a positive candidate;
- every `subtitle_like` result preserves `silent_overwrite=false`.

## Development execution — PASS
Persisted artifacts:
- `fixtures/researcher06-retention-phase-b-dev.json`
- `tools/researcher06_retention_phase_b_dev_gate.py`
- `evidence/researcher06-retention-phase-b-dev-gate.json`

Result: 6/6 fixture families PASS under the frozen decision contract.

Boundary: candidate evidence scores in the dev set are fixture-declared. This establishes executable classification behavior and evidence-boundary preservation, not independent retrieval accuracy, calibrated probabilities, production Search quality, or production subtitle accuracy.

## Anti-leakage boundary
The development contract is now executable and has passed. A sealed held-out transfer exam is therefore authorized. The held-out partition must be frozen before first execution; its cases must not be used to tune thresholds after opening. Any first-run failure must remain preserved and reopen learning rather than be erased by fixture edits.

## Next authorized action
`DESIGN_AND_FREEZE_SEALED_HELD_OUT_TRANSFER_EXAM_WITHOUT_OPENING_IT`.

The exam must cover all five outcome classes, include at least one adjacent-verse quotation, one genuine paraphrase, one ASR-like corruption, one ambiguity/review case, and one ordinary negative, and must exercise at least two surfaces while preserving the same product-neutral evidence class. Do not open Researcher 07 unless repeated held-out failures demonstrate a reusable semantic-retrieval deficit. Do not create product-readable brain knowledge from this practicum unless a genuine learned knowledge node emerges.
