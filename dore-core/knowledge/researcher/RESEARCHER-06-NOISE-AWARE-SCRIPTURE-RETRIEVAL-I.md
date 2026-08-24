# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–05 PASS; UNIT 06 HELD-OUT FAIL; UNIT 07 AUTHORIZED
Opened: 2026-08-23
Trigger: repeated reusable-skill failures in `SUBTITLE-PROOFREADER-PREREQUISITE-DIAGNOSTIC-01.md`.

## Goal
Train Doré to recover Scripture and biblical entities from noisy/partial transcript evidence while preserving the difference between what was heard, what is suggested, and what Scripture actually says.

## Unit 01 — Noise Taxonomy and Error Model
Status: PASS — 8/8.

## Unit 02 — Candidate Generation and Phonetic Evidence
Status: PASS — 10/10.

## Unit 03 — Ranking, Calibration, and Abstention
Status: PASS — 12/12.

## Unit 04 — Phonetic Index Implementation Design and Test Fixtures
Status: PASS — 12/12 adversarial design gate.

## Unit 05 — Executable Fixture Harness and Structural Baseline
Status: PASS — 8/8. Non-production harness, separated dev/test fixtures, tuning guard.

## Unit 06 — Versioned Phonetic Encoders and Generalization Gate
Status: FAIL AT HELD-OUT FINAL — V1 FROZEN; DO NOT TUNE

Encoder versions:
- `mandarin-pinyin-lite-v1`
- `english-metaphone-lite-v1`

Development progression:
1. initial dev run: recall `0`, structural schema defects found;
2. schema repair: recall `0.6667`, one Traditional/Simplified entity miss;
3. per-surface representation repair: recall `1.0`, gold misses `0`, negative abstention `2/2`, mean candidate set `4.6`.

Parameters/versions were then frozen in `evidence/researcher06-unit06-freeze.json` before the sealed split was opened.

One-time held-out result:
- recall-at-budget `0.5`;
- gold misses `1`;
- negative abstention `2/2`;
- exact partial-Scripture fixture PASS;
- biblical-entity fixture FAIL;
- both ordinary nonquotation negatives PASS.

Failure localization: the failed entity contained three Han characters absent from the deliberately small auditable Mandarin mapping table. Because `unknown_han > 0` disables the phonetic channel under the frozen safety policy, Doré abstained rather than guessing. The evidence therefore shows inadequate Mandarin biblical-entity character coverage, not a broken abstention boundary.

Evidence:
- `RESEARCHER-06-UNIT-06-PHONETIC-ENCODER-SPEC.md`
- `RESEARCHER-06-UNIT-06-HELDOUT-DIAGNOSIS.md`
- `evidence/researcher06-unit06-dev-summary.json`
- `evidence/researcher06-unit06-freeze.json`
- `evidence/researcher06-unit06-heldout-summary.json`
- `evidence/researcher06-unit06-heldout.ndjson`

No Researcher-06 capability is promoted to product brain. The failed held-out suite is now exposed evidence and may never again be represented as unseen evaluation for a revised encoder.

## Unit 07 — Coverage Expansion Without Test Leakage
Status: AUTHORIZED — NOT YET PASSED

Objectives:
1. inventory Mandarin character/entity coverage systematically from the existing biblical entity corpus rather than patching a single failed name;
2. define a new versioned encoder from corpus-wide coverage rules;
3. preserve explicit unknown-character behavior and conservative negative abstention;
4. calibrate only on development data;
5. create a fresh sealed held-out suite not used during v2 development;
6. require a new final generalization gate before any production or brain promotion.

## Current capability boundary
Doré has demonstrated a reproducible measurement discipline, versioned encoders, successful dev calibration, parameter freezing, and honest held-out failure handling. It has **not** demonstrated sufficient Mandarin biblical-entity coverage or held-out generalization. Production Search/subtitle wiring remains unauthorized.

## Next authorized action
`RESEARCHER_06_UNIT_07_BUILD_CORPUS_WIDE_MANDARIN_COVERAGE_INVENTORY`.

Measure the existing entity corpus character/surface coverage against `mandarin-pinyin-lite-v1`, record uncovered-character families and coverage rates without modifying v1, then design v2 from corpus-wide evidence. Do not reuse the exposed Unit 06 held-out suite as a final test.
