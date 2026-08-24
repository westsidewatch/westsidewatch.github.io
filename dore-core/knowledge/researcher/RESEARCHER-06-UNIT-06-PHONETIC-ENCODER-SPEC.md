# Researcher 06 — Unit 06 Phonetic Encoder Implementation

Status: IN PROGRESS — IMPLEMENTATION COMMITTED; DEV CALIBRATION / HELD-OUT GATE NOT YET PASSED
Date: 2026-08-23

## Authorized objective
Implement reproducible Mandarin pinyin and English phonetic-key channels with explicit versions. Use only development fixtures for calibration. Freeze parameters before opening the sealed final test. Do not wire to production before held-out evidence passes.

## Implementation evidence

- `scripts/dore/phonetic-encoders.mjs`
  - Mandarin encoder version: `mandarin-pinyin-lite-v1`.
  - English encoder version: `english-metaphone-lite-v1`.
  - Mandarin uses an explicit auditable Han→syllable table for supported characters and emits deterministic `u<codepoint>` fallbacks for unknown Han instead of silently guessing pronunciation.
  - English uses deterministic rule-based normalization for common phonetic equivalences (e.g. initial `kn`, `ph→f`, silent/weak `gh`, vowel suppression after first letter).
  - Both channels expose version ids in output.
- `scripts/dore/phonetic-encoder-selftest.mjs`
  - checks exact Mandarin stability;
  - Traditional/Simplified Mary equivalence;
  - a Chinese negative pair;
  - English `knight/night` and `philip/filip` equivalence;
  - an English negative pair;
  - explicit unknown-Han fallback behavior.
- `.github/workflows/dore-researcher06-phonetic-gate.yml`
  - executes the self-test under Node 22 on changes to the encoder/gate.
- Dev fixtures expanded only on the development split. The sealed test split remains unopened and untouched.

## Boundary / non-claims

This is a deliberately conservative first version, not a comprehensive Mandarin pronunciation engine. Unknown Han characters are surfaced explicitly as unknown fallbacks. Therefore Unit 06 cannot be marked PASS merely because code exists. Required next evidence:

1. observe the executable self-test gate result;
2. integrate the versioned channels into the non-production retrieval harness;
3. tune only on dev fixtures and record chosen bounded parameters;
4. freeze those parameters;
5. only then open the sealed final test once for held-out evaluation.

No Researcher-06 capability has been promoted to the product brain and no production Search/subtitle path is wired to these encoders.
