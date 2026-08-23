# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNIT 01 PASS
Opened: 2026-08-23
Trigger: repeated reusable-skill failures in `SUBTITLE-PROOFREADER-PREREQUISITE-DIAGNOSTIC-01.md`.

## Goal
Train Doré to recover Scripture and biblical entities from noisy/partial transcript evidence while preserving the difference between what was heard, what is suggested, and what Scripture actually says.

## Unit 01 — Noise Taxonomy and Error Model
Status: PASS

### Taxonomy
Doré must classify noise before proposing a correction:

1. **Orthographic noise** — simplified/traditional variants, punctuation, whitespace, obvious character typo.
2. **Phonetic substitution** — ASR chooses characters/words with similar sound but different spelling/meaning.
3. **Biblical entity confusion** — person/place/book names are replaced by common-language tokens or another biblical name.
4. **Transliteration variation** — legitimate Chinese/English rendering traditions differ; variation is not automatically an error.
5. **Deletion/insertion** — words or clauses are dropped or hallucinated by ASR.
6. **Segmentation/boundary noise** — phrase boundaries or verse boundaries are misplaced.
7. **Morphological/inflectional noise** — English or original-language forms differ while lexical identity may remain.
8. **Paraphrase/non-quotation** — speaker conveys a biblical idea without attempting exact quotation; proofreader must not force it into a verse quote.
9. **Acoustic ambiguity** — evidence supports multiple candidates; abstention is required when ranking margin is insufficient.
10. **Theological-attractor error** — a familiar doctrinal phrase looks tempting but evidence does not justify replacing the observed speech with it.

### Evidence model
A correction candidate must keep four layers separate:
- `observed`: transcript/ASR output actually supplied;
- `candidate`: proposed correction, never silently substituted;
- `source`: Scripture/entity evidence supporting the candidate;
- `confidence`: calibrated judgment plus competing candidates/reasons to abstain.

No single evidence channel is sufficient for high-confidence correction. Candidate ranking should be able to combine lexical overlap, phonetic similarity, entity/transliteration evidence, local transcript context, Scripture-window continuity, and corpus prior, while preventing corpus familiarity from overwhelming contradictory acoustic/textual evidence.

## Unit 01 examination gate

1. Missing punctuation only → orthographic noise; correction may be high confidence if lexical content is unchanged. PASS.
2. Similar-sounding Chinese token produces a different word → phonetic substitution, not mere typo. PASS.
3. Two accepted transliterations name the same biblical person → variation first; do not label one wrong without house-style evidence. PASS.
4. Surviving words occur across adjacent verses → segmentation/boundary candidate; search a verse window rather than scoring isolated verses only. PASS.
5. Famous verse is semantically close but transcript wording is a paraphrase → classify paraphrase; do not manufacture quotation marks/exact wording. PASS.
6. Two verses have similar phonetic and lexical evidence → acoustic ambiguity; abstain or present alternatives rather than auto-correct. PASS.
7. Theologically expected term conflicts with stronger observed/context evidence → theological-attractor safeguard wins. PASS.
8. ASR output and suggested correction differ → preserve both fields and source provenance. PASS.

Gate: 8/8 PASS.

## Current capability boundary
Unit 01 establishes the reasoning/error model only. It does not yet prove candidate generation, phonetic indexing, ranking calibration, or cross-verse retrieval implementation. No product-readable brain node is promoted from this unit alone.

## Next authorized action
`RESEARCHER_06_UNIT_02_CANDIDATE_GENERATION_AND_PHONETIC_EVIDENCE`.
Develop and test generic candidate-generation principles for Chinese/English noisy Scripture retrieval, including entity/transliteration candidates, without changing production correction behavior until an adversarial gate passes.
