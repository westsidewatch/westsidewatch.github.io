# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: PASS / GRADUATED → RETENTION_WATCH
Opened: 2026-08-23
Graduated: 2026-08-24
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

V1 passed development calibration but failed its one-shot held-out biblical-entity case because the deliberately small Mandarin character table lacked corpus-wide coverage. The failure is preserved permanently; the exposed final remains retired from unseen evidence.

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

First durable final result:
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

## Unit 09 — Offline Integration Transfer Gate
Status: PASS — 7/7 fresh-final fixtures.

The frozen product-neutral retrieval/evidence contract passed through two consumers: Search-like recovery and subtitle-proofreader suggestion. The final preserved observed transcript, candidate/source provenance, non-probabilistic score boundary, ambiguity abstention, ordinary-negative abstention, shared generic-object behavior, and subtitle no-silent-overwrite.

Evidence:
- `RESEARCHER-06-UNIT-09-FREEZE.md`
- `RESEARCHER-06-UNIT-09-INTEGRATION-TRANSFER.md`
- `RESEARCHER-06-UNIT-09-EXAM.md`
- `evidence/researcher06-unit09-dev-gate.json`
- `fixtures/unit09-final-partition.json`
- `evidence/researcher06-unit09-final-gate.json`

Boundary: Unit 09 is an integration-transfer exam and consumes fixture-declared candidate/anchor targets. Independent retrieval/generalization evidence remains Unit 08. It does not establish production subtitle accuracy or calibrated probability.

## Graduation judgment
Researcher 06 graduates because the course demonstrated: explicit noise taxonomy; candidate/phonetic evidence design; ranking/abstention discipline; executable measurement; honest held-out failure handling; systematic corpus-wide repair without test leakage; frozen fresh generalization success; and product-neutral transfer to both Search-like and subtitle-proofreader consumers.

The failed Unit 06 lineage remains part of the record and is not erased by graduation.

## Current capability boundary
Doré may now treat noise-aware Scripture/entity retrieval as a graduated research capability under retention watch. Production wiring remains a separate authorization and acceptance problem. The system must still preserve `observed → candidate → source → confidence/decision`, abstain under ambiguity, and prohibit silent subtitle overwrite.

## Next authorized action
`POST_GRADUATION_DIAGNOSIS_FOR_RESEARCHER_07`.

Do not invent Researcher 07 merely to continue a curriculum. Inspect current real work (Search, subtitle proofreading, live sensory questions, ONE, library/resource work) and open a new course only if repeated unresolved failures reveal a reusable capability gap that the graduated stack cannot solve.
