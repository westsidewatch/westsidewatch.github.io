# Researcher 06 — Noise-Aware Scripture Retrieval I

Status: ACTIVE — UNITS 01–05 PASS; UNIT 06 IN PROGRESS
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

## Unit 06 — Versioned Phonetic Encoders and Dev Calibration
Status: IN PROGRESS — IMPLEMENTATION COMMITTED; EXECUTABLE DEV CALIBRATION GATE LAUNCHED
Evidence: `RESEARCHER-06-UNIT-06-PHONETIC-ENCODER-SPEC.md`, `scripts/dore/phonetic-encoders.mjs`, `scripts/dore/phonetic-encoder-selftest.mjs`, `.github/workflows/dore-researcher06-phonetic-gate.yml`, `.github/workflows/dore-researcher06-dev-calibration.yml`.

Committed encoder versions:
- `mandarin-pinyin-lite-v1` with explicit auditable Han→syllable mappings and deterministic unknown-Han fallbacks;
- `english-metaphone-lite-v1` with deterministic rule-based phonetic normalization.

The non-production retrieval harness now imports these versioned encoders and exposes phonetic provenance in its measurement output. A dedicated development-only GitHub gate has been added to run the encoder self-test first, then execute the retrieval harness against `noise-retrieval-dev.json`, and persist both NDJSON case evidence and a machine-readable summary under `dore-core/knowledge/researcher/evidence/`.

The sealed test split remains unopened and tuning on it is still programmatically refused. No production wiring or brain promotion is authorized yet.

## Current capability boundary
Units 01–05 prove the error model, bounded candidate architecture, evidence-fusion/calibration rules, phonetic-index design, fixture discipline, and an executable non-production measurement harness. Unit 06 now has reproducible encoder code plus an executable dev-only calibration gate, but no passed dev summary has yet been observed in repository evidence. It still does not prove calibrated production candidate budgets, comprehensive Mandarin pronunciation coverage, held-out generalization, or end-to-end subtitle correction. No Researcher-06 product capability is promoted to brain yet.

## Next authorized action
`RESEARCHER_06_UNIT_06_OBSERVE_DEV_CALIBRATION_EVIDENCE`.
Observe the persisted development summary produced by `.github/workflows/dore-researcher06-dev-calibration.yml`. If and only if the encoder self-test and dev evidence pass the Unit 06 thresholds, freeze the calibrated parameters in a versioned config before opening the sealed final test split for evaluation. If dev evidence fails, diagnose and revise only against development fixtures. Do not wire production or open held-out evidence prematurely.
