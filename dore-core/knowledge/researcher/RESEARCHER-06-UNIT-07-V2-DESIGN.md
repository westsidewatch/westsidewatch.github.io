# Researcher 06 — Unit 07 V2 Pronunciation Architecture and Fresh Evaluation Protocol

Status: DESIGN COMPLETE / IMPLEMENTATION STARTED
Date: 2026-08-24

## Problem established by Unit 06–07 evidence
The frozen `mandarin-pinyin-lite-v1` passed development calibration but failed the one-time held-out gate because its Mandarin table covered only 39 / 774 unique Han characters in the entity corpus. Corpus-wide audit showed only 30.78% Han-occurrence coverage and 2.33% fully covered Chinese entity surfaces. A pinned research comparison using `pinyin-pro@3.29.3` converted the audited corpus completely.

The failure is therefore architectural coverage debt, not a reason to patch the exposed failing entity or to tune on the opened Unit 06 final.

## V2 architecture
Research implementation: `scripts/dore/phonetic-encoders-v2.mjs`.

Mandarin channel:
- encoder id: `mandarin-pinyin-pro-v2-research`;
- pinned source: `pinyin-pro@3.29.3`;
- tone-free syllable sequence;
- `ü` normalized to `v` for stable ASCII keys;
- Han characters that cannot be converted remain explicit `u<codepoint>` unknown tokens;
- provenance is returned with every encoding;
- no product wiring and no mutation of v1.

English channel remains the existing metaphone-lite implementation as a control. Unit 07 is specifically repairing the demonstrated Mandarin coverage failure; changing both channels simultaneously would confound attribution.

## Leakage-safe evaluation protocol
The exposed Unit 06 test is permanently retired as unseen evidence. It may be used only for diagnosis/regression after a new final has been frozen and scored.

Fresh evaluation must follow this order:
1. **Architecture freeze** — pin encoder version, dependency version, normalization rules, retrieval budget, ranking rules and abstention policy before final-case identities are inspected.
2. **Corpus-derived development set** — deterministic hash partition of entity IDs/surfaces; development partition may be inspected and used for implementation debugging.
3. **Fresh final partition** — different deterministic hash bucket, generated mechanically from the whole entity corpus after freeze; no hand selection based on whether v2 succeeds.
4. **Algorithmic perturbations** — use declared, reproducible perturbation families rather than manually repairing the old failing name. Each case stores the perturbation generator and seed/provenance.
5. **Negative controls** — include ordinary non-Bible utterances and near-phonetic distractors so increased recall cannot be purchased by removing abstention.
6. **Single scoring pass** — after final generation, score once. Any parameter/code change after opening the final invalidates that final for unseen claims and requires a new partition/seed.

## Required final metrics
Minimum reporting:
- recall-at-budget;
- gold misses;
- mean candidate-set size;
- negative abstention correctness;
- Mandarin unknown-Han rate;
- result counts by perturbation family;
- encoder/dependency versions and freeze commit.

No production/brain promotion is allowed merely because corpus conversion reaches 100%. Retrieval usefulness and abstention must pass the fresh final gate.

## Examination gate for this unit
PASS criteria for Unit 07 design:
- does not patch the exposed Unit 06 failure by name;
- explains the corpus-wide root cause with persisted measurements;
- v2 implementation preserves explicit provenance and unknown handling;
- v1 remains frozen and available as a control;
- final protocol prevents reuse of the exposed Unit 06 test as unseen evidence;
- architecture is frozen before opening a new final;
- final requires both positive retrieval and negative abstention metrics;
- no product or brain promotion before a fresh gate.

Result: **8/8 PASS**.

## Next authorized action
`RESEARCHER_06_UNIT_08_BUILD_FRESH_FIXTURE_GENERATOR_AND_FREEZE_V2`.

Build the deterministic partition/perturbation harness, run only development/self-tests first, persist a v2 freeze record, then open one fresh final exactly once. If it fails, diagnose broadly and do not tune on the opened final.
