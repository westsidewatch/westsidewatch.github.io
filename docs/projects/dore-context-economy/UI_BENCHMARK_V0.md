# Doré UI Context Economy Benchmark v0

Status: baseline protocol locked

## Purpose

Measure real savings before Context Economy becomes the default Codex route. No theoretical percentage is accepted as evidence.

## Paired-run rule

Each benchmark case is run twice against the same starting commit and same task specification:

- A: current Codex workflow (baseline)
- B: Context Economy gated workflow

The implementation target and acceptance criteria must be identical. A gated run is invalid if it saves context by skipping required engineering or visual verification.

## Required metrics

- files_read
- bytes_read
- search_calls
- tool_calls
- context_bytes
- repeated_reads
- verification_passed
- visual_acceptance

Provider-reported token counts may be recorded when available, but context_bytes is the stable local proxy so measurement does not depend on a paid API or provider-specific telemetry.

## Initial real UI case set

1. Doré Explore motion refinement
2. Paradise Cinema chronology / discovery transition
3. Journal editorial card/layout refinement
4. Living Water responsive homepage refinement
5. Dawn Library collection UI refinement

Cases must use real repository surfaces, not synthetic toy pages.

## PASS

The pipeline may become default only when paired runs are reproducible, correctness verification does not regress, human visual acceptance does not regress, and aggregate context consumption is materially lower.

No target percentage is pre-declared as a PASS shortcut. Report measured reduction.
