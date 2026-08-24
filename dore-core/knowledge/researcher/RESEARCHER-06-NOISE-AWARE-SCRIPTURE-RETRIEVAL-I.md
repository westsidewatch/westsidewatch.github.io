# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–05 PASS; UNIT 06 HELD-OUT FAIL; UNITS 07–08 PASS; UNIT 09 ACTIVE
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
Status: FAIL AT HELD-OUT FINAL — V1 FROZEN; DO NOT TUNE.

V1 passed development calibration but failed its one-shot held-out biblical-entity case because the deliberately small Mandarin character table lacked corpus-wide coverage. The failure was preserved; the exposed final remains retired from unseen evidence.

Evidence:
- `RESEARCHER-06-UNIT-06-PHONETIC-ENCODER-SPEC.md`
- `RESEARCHER-06-UNIT-06-HELDOUT-DIAGNOSIS.md`
- `evidence/researcher06-unit06-freeze.json`
- `evidence/researcher06-unit06-heldout-summary.json`

## Unit 07 — Coverage Expansion Without Test Leakage
Status: PASS — 8/8.

A corpus-wide audit replaced case patching with systematic coverage measurement. V2 was designed around pinned `pinyin-pro@3.29.3`, explicit unknown-Han behavior, versioned provenance, and a fresh evaluation lineage. No production wiring or case-specific repair was added.

Evidence:
- `RESEARCHER-06-UNIT-07-COVERAGE-PLAN.md`
- `RESEARCHER-06-UNIT-07-V2-DESIGN.md`
- `evidence/researcher06-unit07-mandarin-coverage.json`
- `evidence/researcher06-unit07-reference-coverage.json`

## Unit 08 — Fresh Frozen V2 Generalization Final
Status: PASS — 8/8.

The architecture and final harness were frozen before opening a new deterministic unseen partition. First durable final result:
- positives 80;
- negatives 5;
- recall-at-budget 1.0;
- gold misses 0;
- mean candidate set 2.4941;
- negative abstention 5/5;
- unknown Han rate 0;
- same-pinyin single-Han perturbations 80/80 recovered;
- pass true.

Evidence:
- `RESEARCHER-06-UNIT-08-FRESH-FINAL.md`
- `RESEARCHER-06-UNIT-08-EXAM.md`
- `evidence/researcher06-unit08-v2-dev-gate.json`
- `evidence/researcher06-unit08-v2-freeze.json`
- `evidence/researcher06-unit08-v2-fresh-final.json`

Interpretation: v2 repairs the specific unseen biblical-entity coverage/generalization failure that invalidated v1 while preserving conservative abstention. This is strong evidence, but Unit 08 tests one perturbation family and does not alone prove the broader course goal across mixed transcript noise and multiple product consumers.

## Unit 09 — Offline Integration Transfer Gate
Status: ACTIVE — DESIGN / FREEZE REQUIRED.

Unit 09 must test the same generic retrieval contract through at least two offline consumer adapters: Search-like recovery and subtitle-proofreader candidate suggestion. It must include multiple previously learned noise families, preserve `observed -> candidate -> source -> confidence`, enforce abstention under ambiguity/nonquotation, and freeze the integration contract before a fresh one-shot final.

Evidence/plan:
- `RESEARCHER-06-UNIT-09-INTEGRATION-TRANSFER.md`

## Current capability boundary
Doré has demonstrated reproducible measurement discipline, honest held-out failure handling, systematic corpus-wide coverage repair, frozen unseen evaluation, strong v2 Mandarin entity retrieval under same-pinyin corruption, and negative abstention. It has not yet demonstrated an integrated mixed-noise transfer gate across both Search-like and subtitle-proofreader consumers. Production wiring remains unauthorized.

## Next authorized action
`RESEARCHER_06_UNIT_09_BUILD_AND_FREEZE_OFFLINE_TRANSFER_HARNESS`.
