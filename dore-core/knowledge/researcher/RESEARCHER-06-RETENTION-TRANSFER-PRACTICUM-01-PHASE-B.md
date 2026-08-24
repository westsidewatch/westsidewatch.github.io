# Researcher 06 — Retention Transfer Practicum 01 / Phase B

Status: DESIGN FROZEN — DEV FIXTURES REQUIRED
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

## Anti-leakage boundary
This is a development-only contract. No future fresh-final partition may be opened or tuned against until an executable dev harness passes this frozen contract. Passing the dev contract will authorize a sealed held-out transfer exam; it will not establish production subtitle or Search accuracy.

## Next authorized action
`RESEARCHER_06_RETENTION_TRANSFER_PRACTICUM_01_PHASE_B_DEV_FIXTURES_AND_HARNESS`.

Build a development-only fixture set covering all six families and an executable product-neutral harness against this frozen contract. Record failures honestly. Do not open Researcher 07 and do not create product-readable brain knowledge from this practicum unless a genuine learned knowledge node emerges.
