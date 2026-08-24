# Researcher 06 — Unit 06 Held-out Diagnosis

Date: 2026-08-24
State: HELD-OUT FINAL FAIL — FROZEN V1 MUST NOT BE TUNED

## Evidence
Frozen development state before opening held-out:
- recall-at-budget: `1.0`
- gold misses: `0`
- negative abstention correct: `2/2`
- Mandarin encoder: `mandarin-pinyin-lite-v1`
- English encoder: `english-metaphone-lite-v1`

One-time sealed held-out result:
- recall-at-budget: `0.5`
- gold misses: `1`
- negative abstention correct: `2/2`
- exact partial-Scripture fixture: PASS
- biblical-entity fixture: FAIL
- both ordinary nonquotation negatives: PASS

Machine evidence:
- `evidence/researcher06-unit06-freeze.json`
- `evidence/researcher06-unit06-heldout-summary.json`
- `evidence/researcher06-unit06-heldout.ndjson`

## Failure localization
The failed held-out item is the biblical entity `尼哥底母`. The encoder emitted unknown-Han fallbacks for three of its four Han characters (`尼`, `哥`, `底`) while only `母` had a mapped syllable. Under the frozen policy, Mandarin phonetic retrieval is deliberately disabled whenever `unknown_han > 0`, so the phonetic entity channel correctly abstained rather than guessing. Lexical retrieval also found no candidate for this observed form.

This means the failure is not evidence that abstention logic is broken. It is evidence that the deliberately small auditable Mandarin mapping table has insufficient biblical-entity character coverage for held-out generalization.

## What is preserved
- The held-out negatives remained empty, so the conservative abstention boundary survived.
- Exact partial-Scripture retrieval survived.
- No parameters, mappings, budgets, ranking weights, or thresholds were changed after seeing the test.
- `mandarin-pinyin-lite-v1` and `english-metaphone-lite-v1` remain frozen historical versions.

## Non-permitted response
Do NOT add `尼哥底母` or its characters to v1 and rerun the same held-out suite as if it were still unseen. That would convert the final test into training data and invalidate the generalization claim.

## Next authorized learning action
Open **Unit 07 — Coverage Expansion Without Test Leakage**.

Unit 07 must:
1. treat the Unit 06 held-out failure only as evidence that coverage is inadequate, not as a reusable final test;
2. build a systematic Mandarin biblical-character/entity coverage inventory from the existing entity corpus, rather than patching one failed name;
3. design a new versioned encoder (`v2` or equivalent) from corpus-wide coverage rules and dev-only calibration;
4. create a fresh sealed held-out suite that is not used during v2 development;
5. preserve unknown-character abstention and negative controls;
6. require a new held-out gate before any product/brain promotion.

Unit 06 status therefore remains FAIL / LEARNING EVIDENCE, not PASS. Researcher 06 remains active.
