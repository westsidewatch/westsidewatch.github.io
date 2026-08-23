# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–03 PASS
Opened: 2026-08-23
Trigger: repeated reusable-skill failures in `SUBTITLE-PROOFREADER-PREREQUISITE-DIAGNOSTIC-01.md`.

## Goal
Train Doré to recover Scripture and biblical entities from noisy/partial transcript evidence while preserving the difference between what was heard, what is suggested, and what Scripture actually says.

## Unit 01 — Noise Taxonomy and Error Model
Status: PASS

Ten noise classes: orthographic; phonetic substitution; biblical entity confusion; transliteration variation; deletion/insertion; segmentation/boundary; morphology/inflection; paraphrase/non-quotation; acoustic ambiguity; theological-attractor error.

Evidence remains four-layered: `observed` / `candidate` / `source` / `confidence`. No channel alone licenses a high-confidence correction.

Gate: 8/8 PASS. Full prior evidence preserved in repository history.

## Unit 02 — Candidate Generation and Phonetic Evidence
Status: PASS

Candidate generation is recall-oriented but bounded: preserve observed surface; lexical + phonetic + entity/transliteration + verse-window + N-best channels; permit bounded variable-length spans; prune acoustically/textually implausible candidates before semantic reranking; carry provenance; never equate generation with correction.

Source stack: ROCLING 2021 Chen et al.; NAACL 2022 Fang et al.; Findings EMNLP 2021 FastCorrect 2; Findings ACL 2025 DeRAGEC; ACL Industry 2026 G-SPIN.

Gate: 10/10 PASS. Full prior evidence preserved in repository history.

## Unit 03 — Ranking, Calibration, and Abstention
Status: PASS

### Source evidence
- Singh et al., ACL Industry 2026, G-SPIN: restrict the search space to acoustically plausible phonetic neighbors before contextual reranking; decoupling phonetic candidate structure from semantic selection reduces unconstrained rewriting. https://aclanthology.org/2026.acl-industry.151/
- Park, BEA 2026, *Intent vs. Surface*: stronger ASR language models can mask what was actually pronounced; surface-faithful reranking with phoneme-level acoustic similarity reduced false acceptance. https://aclanthology.org/2026.bea-1.23/
- Asano et al., COLING Industry 2025: ranking can combine lexical/semantic context with phonetic correspondence over N-best ASR hypotheses while monitoring false positives. https://aclanthology.org/2025.coling-industry.32/
- Xin et al., ACL 2021, *The Art of Abstention*: selective prediction explicitly allows abstention on low-confidence cases and evaluates confidence estimation, not only raw accuracy. https://aclanthology.org/2021.acl-long.84/
- Fisch et al., 2022, *Calibrated Selective Classification*: accepted predictions themselves need calibrated uncertainty; raw confidence ranking is not sufficient. https://arxiv.org/abs/2208.12084

### Learned ranking contract
Ranking is evidence fusion, not semantic completion.

1. **Eligibility before score.** A candidate must first survive bounded acoustic/textual plausibility from Unit 02. Famous or domain-salient verses outside that set cannot win by semantic prior.
2. **Observed evidence has veto power.** Strong contradiction from phonetic/surface evidence cannot be canceled merely by biblical frequency, theological familiarity, or semantic elegance.
3. **Independent channels add support.** Lexical overlap, phonetic proximity, entity/transliteration match, local transcript context, verse-window continuity, and N-best agreement are recorded separately before fusion.
4. **Context reranks; it does not invent.** Local context may discriminate among eligible candidates but may not introduce an unconstrained candidate.
5. **Corpus/domain prior is weak evidence.** Scripture frequency and entity salience break ties only after surface/phonetic plausibility; they cannot dominate contradictory evidence.
6. **Margin matters.** A high top score is insufficient when runner-up evidence is nearly equal. Confidence depends on both absolute support and separation from credible alternatives.
7. **Conflict lowers confidence.** Strong disagreement between channels is evidence of uncertainty, not an invitation to average the conflict away.
8. **Abstention is a valid output.** When support is weak, contradictory, out-of-distribution, or the top-two margin is not validated, return alternatives / `UNCERTAIN` rather than silently rewriting.
9. **Thresholds require calibration data.** No numeric production threshold is invented in this unit. Acceptance thresholds must be fitted/evaluated on held-out noisy Scripture/ASR examples and tracked by risk–coverage / false-correction behavior.
10. **Correction confidence is not verse confidence.** A verse can be identified confidently while the exact transcript correction remains uncertain; preserve both judgments.

### Adversarial examination gate
1. Famous verse has perfect semantic fit but poor phonetic fit; obscure verse has strong surface+phonetic fit → obscure eligible candidate ranks above famous semantic attractor. PASS.
2. Top candidate score looks high but runner-up is nearly tied → abstain/present alternatives until calibrated margin supports acceptance. PASS.
3. Entity prior strongly favors `耶利米` but observed syllables strongly support `尼希米` → entity prior cannot override surface contradiction. PASS.
4. Two accepted transliterations differ but denote same entity → do not treat variant spelling as evidence of transcript error; normalize identity separately. PASS.
5. Adjacent-verse window explains all surviving words while a single famous verse explains only half → continuity/window evidence outranks fame. PASS.
6. N-best hypotheses agree on phonetic skeleton but disagree lexically → agreement strengthens phonetic evidence only; lexical uncertainty remains visible. PASS.
7. Local sermon context points to Romans, but no bounded Romans candidate is acoustically plausible → do not invent Romans correction. PASS.
8. Candidate is highly likely in Bible corpus but observed evidence may be ordinary non-quotation speech → classify paraphrase/non-quotation or abstain; do not force quotation. PASS.
9. Model confidence is 0.94 but no held-out calibration exists → do not call 0.94 a 94% correctness probability or set production threshold from it. PASS.
10. Verse identity is strong but one word's acoustic realization is ambiguous → identify verse if justified while abstaining on exact word correction. PASS.
11. Channel scores conflict sharply → lower confidence; do not hide disagreement in a weighted average. PASS.
12. User-facing proofreader would change sacred-text quotation under low margin → abstention is preferred to false correction. PASS.

Gate: **12/12 PASS**.

## Current capability boundary
Units 01–03 prove the error model, bounded candidate generation, qualitative evidence-fusion ranking, and the necessity/logic of calibrated abstention. They do **not** yet prove production scoring weights, numeric thresholds, implementation-level phonetic indexes, or end-to-end subtitle correction. No retrieval-method product brain node is promoted yet.

## Next authorized action
`RESEARCHER_06_UNIT_04_PHONETIC_INDEX_IMPLEMENTATION_AND_TEST_FIXTURES`.
Build/test a reusable Scripture/entity phonetic-candidate index design with Chinese and English fixtures. It must preserve observed/candidate provenance, variable-length spans, transliteration aliases, and bounded candidate neighborhoods. Do not wire it into production until fixture-level precision/recall and abstention behavior are measured.
