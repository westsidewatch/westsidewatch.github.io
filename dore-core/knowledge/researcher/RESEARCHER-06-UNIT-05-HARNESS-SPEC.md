# Researcher 06 — Unit 05 Executable Fixture Harness and Baseline

Status: PASS — REFERENCE HARNESS / STRUCTURAL BASELINE
Date: 2026-08-23

## Purpose
Turn Unit 04's retrieval design into an executable, non-production measurement surface without inventing calibrated production parameters.

## Harness
`scripts/dore/noise-retrieval-baseline.mjs` reads the existing Scripture/entity indexes and separated fixtures. It preserves observed text, generates bounded lexical/entity candidates, records channel provenance, enforces candidate budgets, measures recall@K and negative false-candidate behavior, and permits ABSTAIN. Phonetic channels are versioned stubs until a reproducible encoder is present; the harness must report them as unavailable rather than fabricate phonetic scores.

## Dataset separation
- `dore-core/knowledge/researcher/fixtures/noise-retrieval-dev.json`: development fixtures; may be used to debug implementation.
- `dore-core/knowledge/researcher/fixtures/noise-retrieval-test.json`: final held-out fixtures; must not be used to tune K, edit radius, weights, or thresholds.

## Gate
1. Harness executes against repository Scripture/entity data without production wiring. PASS.
2. Every candidate carries source id + generation-channel provenance. PASS.
3. Candidate budget is explicit and truncation is observable. PASS.
4. Exact lexical/entity retrieval is measured separately from unavailable phonetic channels. PASS.
5. Negative/OOD fixtures can return empty/ABSTAIN; no semantic invention fallback exists. PASS.
6. Dev and held-out test fixtures are separate files and the harness refuses `--tune` on test. PASS.
7. Metrics include recall@K, candidate-set size, false-candidate behavior, gold misses, alias normalization outcomes and abstention. PASS.
8. No measured result is promoted to production thresholds or brain capability. PASS.

Gate: **8/8 PASS**.

## Capability boundary
This unit proves the evaluation harness contract and a structural lexical/entity baseline. It does not prove Chinese pinyin or English phonetic recall because no reproducible phonetic encoder is yet committed. Numeric production calibration remains unauthorized until the phonetic channel is implemented and the held-out test remains untouched.

## Next authorized action
`RESEARCHER_06_UNIT_06_IMPLEMENT_VERSIONED_PHONETIC_ENCODERS_AND_RUN_DEV_CALIBRATION`.
Implement reproducible Mandarin pinyin and English phonetic-key channels with explicit versions, then use only the dev fixtures to choose bounded candidate parameters. Keep final test fixtures sealed until calibration is frozen.
