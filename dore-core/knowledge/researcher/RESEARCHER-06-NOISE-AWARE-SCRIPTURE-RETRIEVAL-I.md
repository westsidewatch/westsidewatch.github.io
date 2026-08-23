# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–04 PASS
Opened: 2026-08-23
Trigger: repeated reusable-skill failures in `SUBTITLE-PROOFREADER-PREREQUISITE-DIAGNOSTIC-01.md`.

## Goal
Train Doré to recover Scripture and biblical entities from noisy/partial transcript evidence while preserving the difference between what was heard, what is suggested, and what Scripture actually says.

## Unit 01 — Noise Taxonomy and Error Model
Status: PASS

Ten noise classes: orthographic; phonetic substitution; biblical entity confusion; transliteration variation; deletion/insertion; segmentation/boundary; morphology/inflection; paraphrase/non-quotation; acoustic ambiguity; theological-attractor error.

Evidence remains four-layered: `observed` / `candidate` / `source` / `confidence`. No channel alone licenses a high-confidence correction.

Gate: 8/8 PASS.

## Unit 02 — Candidate Generation and Phonetic Evidence
Status: PASS

Candidate generation is recall-oriented but bounded: preserve observed surface; lexical + phonetic + entity/transliteration + verse-window + N-best channels; permit bounded variable-length spans; prune acoustically/textually implausible candidates before semantic reranking; carry provenance; never equate generation with correction.

Gate: 10/10 PASS.

## Unit 03 — Ranking, Calibration, and Abstention
Status: PASS

Ranking is evidence fusion, not semantic completion. Eligibility precedes score; observed evidence has veto power; context reranks but does not invent; domain priors stay weak; top-two margin and channel conflict affect confidence; abstention is valid; numeric thresholds require held-out calibration.

Gate: 12/12 PASS.

## Unit 04 — Phonetic Index Implementation Design and Test Fixtures
Status: PASS — DESIGN/REFERENCE IMPLEMENTATION GATE; PRODUCTION CALIBRATION NOT YET PASSED

### Fresh source checks
- Singh et al., ACL Industry 2026, G-SPIN: phonetic graph neighborhoods should restrict correction search before contextual reranking; unconstrained semantic generation is unsafe for ASR correction. https://aclanthology.org/2026.acl-industry.151/
- Tan et al., ACL 2022, Chinese pinyin input: pinyin maps ambiguously to many characters, especially under abbreviation; context is needed to distinguish homophones. https://aclanthology.org/2022.acl-long.133/
- E-commerce phonetic spelling correction, ECNLP 2022: hybrid lexical/phonetic candidate generation can index exact phonetic keys plus a bounded edit-distance neighborhood; English Double Metaphone is useful but imperfect. https://aclanthology.org/2022.ecnlp-1.9/
- Yu et al., Findings ACL 2024: confidence-aware refinement of OCR/ASR Chinese spelling-correction data reduces over-correction, reinforcing the requirement to measure false corrections rather than accuracy alone. https://aclanthology.org/2024.findings-acl.914/
- Matassoni et al., LREC 2026: phonetic-based ranking is useful for filtering poor ASR pseudo-labels with controllable resources, supporting phonetic evidence as a first-class but non-exclusive channel. https://aclanthology.org/2026.lrec-1.795/

### Reusable index contract
The index is not a correction dictionary. It is a candidate-retrieval structure.

Each indexed Scripture/entity span carries:
- canonical surface and stable source id;
- language/script;
- normalized lexical key;
- one or more phonetic keys with the encoder/version recorded;
- aliases/transliterations as separate provenance-bearing forms, never silently collapsed into the canonical surface;
- span length and token/character offsets;
- verse/entity provenance;
- optional neighboring verse/span ids for bounded continuity expansion.

Query-time generation:
1. Preserve `observed` exactly before normalization.
2. Generate variable-length observed spans within an explicit maximum window.
3. Retrieve exact lexical candidates.
4. Retrieve exact phonetic-key candidates.
5. Expand only to a bounded phonetic edit/confusion neighborhood; no corpus-wide semantic jump.
6. Add explicit entity/transliteration aliases with alias provenance.
7. Add adjacent verse/window candidates only when a surviving candidate anchors the neighborhood.
8. Deduplicate by canonical source while retaining every generation channel.
9. Pass the shortlist, not the whole corpus, to contextual ranking.
10. If no candidate survives the bounded evidence rules, return empty/UNCERTAIN rather than manufacture a biblical correction.

### Chinese implementation boundary
Use a versioned Mandarin pinyin representation at minimum, retaining tone-bearing and tone-stripped keys as distinct channels. Character→pinyin is one-to-many for polyphonic characters, so alternate readings must be explicit candidates or lexicon-backed aliases; never choose a reading solely because it produces a familiar verse. Pinyin identity is not character identity: homophones intentionally produce neighborhoods, not automatic corrections.

### English implementation boundary
A versioned Double-Metaphone-like key may be one recall channel for English names/terms, with exact lexical and edit-distance channels retained. It is not language-universal and must not be reused as the Chinese encoder. Transliteration aliases such as biblical proper-name variants remain explicit alias records with provenance.

### Fixture schema
Each held-out fixture records:
`observed`, `language`, `noise_class`, `gold_source_ids`, `acceptable_aliases`, `must_not_return`, `candidate_budget`, and whether `ABSTAIN` is acceptable/required.

Required fixture families:
- Chinese same-pinyin substitution;
- Chinese near-pinyin initial/final confusion;
- Chinese polyphonic-character trap;
- Chinese biblical entity ASR substitution;
- Chinese variable-length deletion/insertion;
- English homophone/near-phone name;
- English Double-Metaphone collision trap;
- transliteration alias equivalence;
- adjacent-verse boundary recovery;
- famous-verse theological-attractor negative;
- ordinary non-quotation negative;
- out-of-index/OOD negative.

### Measurement contract
Before production wiring, evaluate at least:
- candidate recall@K by fixture family;
- mean/95p candidate-set size and latency;
- gold-source miss rate;
- false-candidate rate on non-quotation/OOD negatives;
- alias/entity normalization errors;
- downstream top-1 precision after ranking;
- abstention coverage and false-correction risk.

No production K, edit radius, score weight, or confidence threshold is fixed by this unit; those are empirical parameters for held-out calibration.

### Adversarial design gate
1. `耶利米` and a same/near-pinyin wrong surface collide → both remain candidates; pinyin alone cannot correct. PASS.
2. Polyphonic character has two readings, only one yields a famous verse → index retains reading provenance; fame cannot choose the reading. PASS.
3. English DM key collides for unrelated terms → collision expands candidates but cannot imply equivalence. PASS.
4. Transliteration aliases denote one entity but differ in spelling → canonical entity dedup preserves alias provenance. PASS.
5. Gold phrase crosses a verse/token boundary → bounded variable-length/window indexing can retrieve it without whole-corpus semantic search. PASS.
6. Famous verse is semantically perfect but outside lexical/phonetic neighborhood → excluded before reranking. PASS.
7. Ordinary speech resembles Bible semantics but has no bounded evidence → empty/ABSTAIN allowed and preferred. PASS.
8. Candidate budget explodes under a common pinyin key → enforce per-channel/per-span budget and expose truncation; do not silently claim exhaustive recall. PASS.
9. Exact lexical candidate exists alongside many phonetic candidates → exact lexical provenance remains separately visible and may be ranked later; generation does not decide correction. PASS.
10. Evaluation set is used to tune K and then reported as held-out → invalid; calibration/dev and final test fixtures must remain separated. PASS.
11. Index encoder changes version → keys must be rebuildable/versioned; mixed-version scores cannot be treated as comparable without migration. PASS.
12. No gold candidate appears → record retrieval miss and abstain; do not let contextual LLM invent a candidate. PASS.

Gate: **12/12 PASS**.

## Current capability boundary
Units 01–04 now prove a reusable, language-aware phonetic-index architecture and adversarial fixture/measurement contract in addition to the earlier error/ranking model. They still do **not** prove measured recall/precision, production candidate budgets, numeric thresholds, or end-to-end subtitle correction because no held-out fixture corpus has yet been executed against an implementation. No Researcher-06 product capability is promoted to brain yet.

## Next authorized action
`RESEARCHER_06_UNIT_05_BUILD_EXECUTABLE_FIXTURE_HARNESS_AND_MEASURE_BASELINE`.
Implement a non-production reference harness and a separated dev/test fixture set over existing Scripture/entity data. Measure recall@K, candidate-set growth, negative false-candidate behavior, and abstention. Only after measurements may Unit 06 calibrate ranking/thresholds or consider product wiring.
