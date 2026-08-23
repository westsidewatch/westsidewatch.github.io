# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–05 PASS
Opened: 2026-08-23
Trigger: repeated reusable-skill failures in `SUBTITLE-PROOFREADER-PREREQUISITE-DIAGNOSTIC-01.md`.

## Goal
Train Doré to recover Scripture and biblical entities from noisy/partial transcript evidence while preserving the difference between what was heard, what is suggested, and what Scripture actually says.

## Unit 01 — Noise Taxonomy and Error Model
Status: PASS
Ten noise classes and the four-layer `observed / candidate / source / confidence` evidence model. Gate: 8/8 PASS.

## Unit 02 — Candidate Generation and Phonetic Evidence
Status: PASS
Bounded lexical + phonetic + entity/transliteration + verse-window + N-best candidate generation; provenance preserved; generation never equals correction. Gate: 10/10 PASS.

## Unit 03 — Ranking, Calibration, and Abstention
Status: PASS
Evidence-fusion ranking, observed-evidence veto, weak domain priors, top-two margin/conflict reasoning, calibrated abstention. Gate: 12/12 PASS.

## Unit 04 — Phonetic Index Implementation Design and Test Fixtures
Status: PASS — DESIGN/REFERENCE IMPLEMENTATION GATE; PRODUCTION CALIBRATION NOT YET PASSED
Reusable language-aware phonetic-index contract, explicit encoder/alias/span provenance, bounded neighborhoods, variable-length spans, separated fixture schema and measurement contract. Gate: 12/12 adversarial design PASS.

## Unit 05 — Executable Fixture Harness and Structural Baseline
Status: PASS — NON-PRODUCTION HARNESS; PHONETIC MEASUREMENT PENDING UNIT 06
Evidence: `RESEARCHER-06-UNIT-05-HARNESS-SPEC.md`, `scripts/dore/noise-retrieval-baseline.mjs`, separated `fixtures/noise-retrieval-dev.json` and sealed `fixtures/noise-retrieval-test.json`.

The executable reference harness now:
- reads existing Scripture/entity indexes;
- preserves observed surface and candidate provenance;
- enforces explicit candidate budgets and exposes truncation;
- measures recall-at-budget, candidate-set size, gold misses, negative abstention and alias/entity outcomes;
- refuses `--tune` when the sealed test split is selected;
- explicitly reports the phonetic channel unavailable until reproducible versioned encoders are committed rather than fabricating phonetic scores;
- has no production wiring and promotes no capability to brain.

Gate: 8/8 PASS.

## Current capability boundary
Units 01–05 prove the error model, bounded candidate architecture, evidence-fusion/calibration rules, phonetic-index design, fixture discipline, and an executable non-production measurement harness. They still do **not** prove Chinese pinyin or English phonetic recall, calibrated production candidate budgets, numeric thresholds, or end-to-end subtitle correction. No Researcher-06 product capability is promoted to brain yet.

## Next authorized action
`RESEARCHER_06_UNIT_06_IMPLEMENT_VERSIONED_PHONETIC_ENCODERS_AND_RUN_DEV_CALIBRATION`.
Implement reproducible Mandarin pinyin and English phonetic-key channels with explicit encoder versions. Use only the development fixtures to choose bounded candidate parameters. Freeze parameters before opening the sealed final test split; do not wire production until held-out evidence passes.
