# Subtitle Proofreader Prerequisite Diagnostic 01

Date: 2026-08-23
Status: COMPLETE — COURSE WARRANTED

## Purpose
Test whether Doré's existing graduated research capabilities plus current Bible Search implementation are sufficient for a future subtitle-proofreader role, before opening another course.

## Existing implementation inspected
`static/dore/dore-search.js` currently provides:
- Traditional/Simplified Chinese folding for a bounded character map;
- book/reference parsing and aliases;
- exact normalized Chinese/English verse-text retrieval;
- character-bigram / longest-fragment fuzzy retrieval;
- Hebrew/Greek original-language lookup and evidence display.

This is a useful Bible Search substrate, but it is not yet an ASR/noisy-quotation correction system.

## Bounded transfer benchmark
The benchmark uses failure classes rather than hand-coding answers.

| Case | Noisy/partial input class | Needed behavior | Current substrate judgment | Failure class |
|---|---|---|---|---|
| 01 | exact/near-exact Scripture quotation with punctuation loss | recover verse | normalization + substring search can handle many cases | COVERED |
| 02 | partial quotation with one omitted span | rank verse by surviving fragments | fuzzy character overlap can sometimes recover | PARTIAL / IMPLEMENTATION |
| 03 | Chinese homophone ASR substitution (same pronunciation, unrelated characters) | infer likely biblical token/verse from phonology + context | current normalizer has no phonetic representation | FAIL — MISSING REUSABLE SKILL |
| 04 | biblical personal/place name misrecognized as common words | identify candidate entity and preserve uncertainty | entity/search aliases do not model ASR confusion lattices | FAIL — MISSING REUSABLE SKILL |
| 05 | transliteration variant across Chinese traditions | map variants to same entity without silently rewriting | bounded aliases can cover known forms but no systematic transliteration model | FAIL — CORPUS + REUSABLE SKILL |
| 06 | English ASR near-homophone in Bible quotation | retrieve by phonetic/lexical similarity | character-bigram text similarity is inadequate | FAIL — MISSING REUSABLE SKILL |
| 07 | multiple plausible corrections | rank candidates and expose confidence/margin instead of asserting one correction | current Search scores fuzzy hits but has no correction decision/calibration contract | FAIL — MISSING REUSABLE SKILL |
| 08 | quotation crosses verse boundary | retrieve/rank contiguous verse window | current search scores verses independently | FAIL — IMPLEMENTATION / RETRIEVAL MODEL |
| 09 | speaker paraphrases rather than quotes | distinguish paraphrase retrieval from correction | existing research judgment can preserve uncertainty, but retrieval layer lacks semantic candidate generation | FAIL — IMPLEMENTATION/CAPABILITY GAP |
| 10 | doctrinally loaded word differs by one ASR token | never auto-correct solely because a theological reading is familiar | graduated research methods supply anti-retrojection/uncertainty discipline | COVERED AT JUDGMENT LAYER |

## Diagnosis
Repeated independent failures (03, 04, 05, 06, 07) share one reusable capability deficit rather than a single product bug: Doré lacks a trained method for **noise-aware Scripture retrieval and uncertainty-calibrated correction**. This includes phonetic similarity, biblical entity/transliteration normalization, candidate generation/ranking, and abstention when evidence is insufficient.

Cases 08–09 also require product implementation work, but implementation alone should not invent the linguistic/retrieval method.

Therefore a new course is justified under Autonomous Learning I's rule: the missing skill repeats across independent task types and is not supplied by Biblical Languages I or Biblical Concept Development I.

## Course decision
OPEN `RESEARCHER-06 — NOISE-AWARE SCRIPTURE RETRIEVAL I`.

Course boundary:
- not generic speech recognition training;
- not a subtitle UI course;
- not theology-by-autocorrect;
- focuses on reusable retrieval/correction reasoning that can serve Bible Search, Westside Stories subtitle proofreading, and later products.

Required competence gates:
1. distinguish orthographic, phonetic, transliteration, omission/insertion, segmentation and paraphrase noise;
2. generate candidates from Scripture/entity corpora without hard-coded per-question rules;
3. rank with multiple independent evidence channels;
4. calibrate confidence and abstain on ambiguous corrections;
5. recover cross-verse quotation windows;
6. pass adversarial tests where the familiar biblical phrase is *not* the spoken phrase;
7. preserve provenance: observed ASR text vs suggested correction vs source verse must remain separable.

## Next authorized action
`RESEARCHER_06_UNIT_01_NOISE_TAXONOMY_AND_ERROR_MODEL`.
Build the error taxonomy and examination set before changing product correction behavior.
