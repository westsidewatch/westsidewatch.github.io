# Researcher 06 — Retention Transfer Practicum 01 / Phase B

Status: SEALED HELD-OUT FIRST RUN PASS — INDEPENDENT RETRIEVAL PROBE NEXT
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
- `fixtures/researcher06-retention-phase-b-dev.json`;
- `tools/researcher06_retention_phase_b_dev_gate.py`;
- `evidence/researcher06-retention-phase-b-dev-gate.json`.

Result: 6/6 fixture families PASS under the frozen decision contract.

Boundary: candidate evidence scores in the dev set are fixture-declared. This establishes executable classification behavior and evidence-boundary preservation, not independent retrieval accuracy, calibrated probabilities, production Search quality, or production subtitle accuracy.

## Sealed held-out transfer exam — FIRST RUN PASS
The held-out partition was frozen before opening at commit `136a3eec9e4a35df2fe46bb7a2e9a8a8873d1248`:
- `fixtures/researcher06-retention-phase-b-heldout.json`.

The first run reused the already frozen development classifier thresholds; no threshold was tuned from held-out outcomes. First-run evidence is preserved in:
- `evidence/researcher06-retention-phase-b-heldout-first-run.json`.

Result: **6/6 PASS**.

Coverage:
- adjacent-verse quotation → `quotation_recovery`;
- genuine paraphrase → `paraphrase_retrieval`;
- ASR-like corruption → `correction_proposal`;
- materially close biblical candidates → `review`;
- ordinary negative → `abstain`;
- one-verse control → `quotation_recovery`.

At least two surfaces were exercised (`search_like`, `subtitle_like`, plus `neutral`) while preserving one product-neutral outcome class. `silent_overwrite=false` remained invariant.

## What this PASS does and does not establish
Established:
- the frozen evidence-classification contract transferred to fresh held-out cases;
- genuine paraphrase was not mislabeled as correction;
- ambiguity was not forced;
- ordinary negative abstained;
- surface choice did not change evidence class.

Not established:
- independent candidate retrieval quality;
- semantic embedding/retrieval generalization;
- calibrated probability values;
- production Search accuracy;
- production subtitle accuracy.

Candidate evidence channels in both dev and held-out fixtures remain declared test inputs. Therefore this PASS does **not** justify opening Researcher 07 and does **not** justify production promotion by itself.

## Next authorized action
`RESEARCHER_06_RETENTION_TRANSFER_PRACTICUM_02_INDEPENDENT_CANDIDATE_RETRIEVAL_PROBE`.

Build a non-production retrieval probe that constructs contiguous one- and multi-verse candidates from the actual Scripture corpus rather than fixture-declared candidates. Test quotation-window recall first. Separately probe whether an existing generic semantic mechanism can supply paraphrase candidates without converting semantic familiarity into correction evidence. Preserve first failures. Only repeated fresh evidence of a reusable semantic-retrieval deficit may justify Researcher 07.

Do not create product-readable brain knowledge from this practicum unless a genuine learned knowledge node emerges.
