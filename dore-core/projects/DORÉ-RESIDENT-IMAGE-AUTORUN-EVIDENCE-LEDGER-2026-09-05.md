# DORÉ RESIDENT IMAGE AUTORUN — EVIDENCE LEDGER

Date: 2026-09-05
Status: SWEEP_RECONCILED / VERIFIED_COMPLETE_SUBMILESTONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Evidence reviewed

- commit `69c4a40a2e082749a7d03c54a68948305a24f3fa` (`Continue Doré Image: resident autorun bridge (#313)`);
- `dore_core/capabilities/image_runtime_config.py`;
- `scripts/dore_image_autorun.py`;
- `tests/test_dore_image_autorun.py`;
- commit-associated workflow-run surface for the introducing commit.

## Findings

1. Doré Image now has a bounded zero-terminal resident autorun seam rather than requiring an operator to manually invoke the lower-level resident generation entrypoint each time. The runner discovers a local resident configuration, distinguishes `NOT_READY`, `IDLE` and `PASS`, validates a loopback-only renderer endpoint, loads a typed workflow template, verifies renderer health, consumes a queued image job, persists `last-completed.json`, and removes the consumed job only after generation returns.
2. The configuration contract deliberately rejects non-loopback endpoints and requires model/template identity. This is consistent with the free/local resident direction and prevents the autorun path from silently selecting a remote paid image endpoint.
3. This is a `VERIFIED_COMPLETE_SUBMILESTONE` for runtime orchestration architecture, not a real visual-production acceptance result. The introducing commit has no persisted commit-associated workflow-run receipt, and the tests prove configuration/refusal boundaries rather than a real ComfyUI/model render.
4. `NOT_READY` on missing config or unreachable renderer is an environment-readiness state, not by itself a new Sweep blocker. No evidence in this bounded batch shows that a configured real resident renderer was attempted and failed.
5. The next acceptance proof is unchanged but now has a more direct execution seam: configure the approved local resident renderer, place one real purpose-built Westside job (prefer Doré-derived light texture or Bethlehem-star grammar), execute autorun through durable resident bytes, then continue real vision observation → critic/correction → accepted artifact → typed Design application.
6. No P01 subtitle state, ordering, deployment or audio/transcription dependency was changed.

## Current classification

- resident image autorun orchestration: `VERIFIED_COMPLETE_SUBMILESTONE`;
- real local renderer/model execution: `UNKNOWN_NEEDS_EVIDENCE`;
- real Westside visual acceptance loop: `UNKNOWN_NEEDS_EVIDENCE`;
- human/environment blocker discovered by Sweep: NONE.
