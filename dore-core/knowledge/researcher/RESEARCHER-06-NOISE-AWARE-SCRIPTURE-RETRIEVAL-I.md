# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–02 PASS
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

## Unit 02 — Candidate Generation and Phonetic Evidence
Status: PASS

### Source evidence
- Chen et al., ROCLING 2021, *Integrated Semantic and Phonetic Post-correction for Chinese Speech Recognition*: Chinese ASR homophonic errors are common; semantic-only correction can degrade performance, while combining contextual and phonetic evidence lowers CER. https://aclanthology.org/2021.rocling-1.13/
- Fang et al., NAACL 2022, *Non-Autoregressive Chinese ASR Error Correction with Phonological Training*: phonological tokens support phonetically similar and variable-length corrections rather than only one-token substitutions. https://aclanthology.org/2022.naacl-main.432/
- Leng et al., Findings EMNLP 2021, *FastCorrect 2*: multiple ASR hypotheses can be aligned using token and pronunciation similarity and can outperform single-candidate correction. https://aclanthology.org/2021.findings-emnlp.367/
- Im et al., Findings ACL 2025, *DeRAGEC*: named-entity candidate retrieval benefits from phonetic similarity but noisy retrieved candidates must be filtered before correction. https://aclanthology.org/2025.findings-acl.786/
- Singh et al., ACL Industry 2026, *Graph-Based Phonetic Error Correction of Noisy ASR*: explicitly restrict correction to acoustically plausible phonetic candidate neighborhoods, then contextually rerank; this reduces unconstrained rewriting/hallucination. https://aclanthology.org/2026.acl-industry.151/

### Generic candidate-generation method learned
Candidate generation is recall-oriented but bounded. It precedes ranking and must not itself assert a correction.

1. **Preserve the observed surface.** Never normalize away the original ASR token/string before evidence is recorded.
2. **Generate lexical candidates.** Exact/fuzzy character or token neighbors remain one channel, not the sole channel.
3. **Generate phonetic candidates.** For Chinese, compare pronunciation representations at syllable level and permit bounded tone/initial/final confusions; for English, use pronunciation/phoneme evidence rather than spelling edit distance alone. Do not treat phonetic similarity as semantic correctness.
4. **Permit variable-length neighborhoods.** Candidate spans may be 1→N or N→1 because ASR deletion/insertion and segmentation errors are not fixed-length.
5. **Add domain entity candidates separately.** Biblical person/place/book forms and known transliteration variants may expand recall, but entity prior cannot override contradictory surface evidence.
6. **Use verse-window candidates.** When surviving evidence can cross a verse boundary, generate adjacent-verse windows before ranking.
7. **Retain multiple hypotheses.** If N-best ASR hypotheses exist, preserve and align them; agreement can strengthen evidence but disagreement must remain visible.
8. **Prune before semantic reranking.** Keep only acoustically/textually plausible candidates; do not let an unconstrained language model invent a famous verse or entity outside the bounded candidate set.
9. **Carry provenance per candidate.** Each candidate records which generator produced it (lexical, phonetic, entity/transliteration, boundary/window, N-best) and its evidence features.
10. **Candidate generation does not authorize correction.** Ambiguous candidate sets flow to later ranking/calibration and may end in abstention.

### Unit 02 adversarial examination gate
1. Chinese ASR produces a homophonic common word where a biblical term is plausible: generate both phonetic and lexical/entity candidates; do not auto-select the biblical term. PASS.
2. Correct form differs by two characters but is nearly identical in pronunciation: spelling distance may not suppress a strong phonetic candidate. PASS.
3. Famous verse is semantically perfect but acoustically implausible: it must not enter merely through semantic/theological attraction. PASS.
4. Error is one observed token but intended phrase could be two tokens: variable-length candidate generation is required. PASS.
5. Biblical name has two legitimate transliterations: retain both as candidates/aliases; do not mark one erroneous solely because corpus prior favors the other. PASS.
6. Surviving words straddle adjacent verses: generate verse-window candidate rather than force a single verse. PASS.
7. Two ASR N-best hypotheses disagree on a named entity: preserve both and use agreement/disagreement as later ranking evidence. PASS.
8. English spelling is distant but phoneme sequence is close: pronunciation channel keeps the candidate alive. PASS.
9. Entity dictionary returns many phonetic neighbors: prune by acoustic/textual plausibility before contextual reranking; domain membership alone is insufficient. PASS.
10. Top two bounded candidates remain nearly tied: Unit 02 must pass both forward; correction/abstention is a later calibration decision. PASS.

Gate: 10/10 PASS.

## Current capability boundary
Units 01–02 prove the error model and bounded multi-channel candidate-generation method. They do **not** yet prove ranking weights, confidence calibration, abstention thresholds, implementation-level phonetic indexes, or production subtitle correction. No product-readable brain node is promoted yet.

## Next authorized action
`RESEARCHER_06_UNIT_03_RANKING_CALIBRATION_AND_ABSTENTION`.
Develop and adversarially test ranking principles that combine lexical, phonetic, entity, context, verse-window, and corpus evidence without allowing semantic/domain priors to swamp contradictory observed evidence. Define explicit uncertainty/abstention behavior before any product promotion.
