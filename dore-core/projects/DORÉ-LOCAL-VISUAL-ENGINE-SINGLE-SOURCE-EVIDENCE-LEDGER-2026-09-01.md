# DORÉ LOCAL VISUAL ENGINE SINGLE-SOURCE EVIDENCE LEDGER — 2026-09-01

Status: SWEEP-01 / BOUNDED RECONCILIATION
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

## Evidence reviewed

- `.github/workflows/dore-engine-single-source-cleanup.yml`
- `local/dore-local/penpot_agent.py`
- `local/dore-local/setup-penpot-mcp.sh`
- `local/dore-local/local_updater.py`
- `local/dore-local/learning_worker.py`

## Classification

### Current local-model / visual-engine relationship

`CORE/CONTINUOUS / MAINTENANCE`

The current executable local stack uses one active model source: `DORE_LOCAL_MODEL` (default `gemma4:e4b`). `penpot_agent.py` binds `VISION_MODEL=MODEL`; `setup-penpot-mcp.sh` binds `VISION_MODEL="$MODEL"`; `learning_worker.py` reads the same `DORE_LOCAL_MODEL`; and `local_updater.py` propagates the active model into spawned workers while persisting `visual_engine_follows_active_model: true`.

This is implementation evidence for single-source model selection inside the current local Doré/Penpot path. It is not evidence that the visual system is aesthetically complete, that D4 visual verification has passed, or that every Doré execution surface globally shares one model/runtime.

### `dore-engine-single-source-cleanup.yml`

`SUPERSEDED / RETIRED-AS-ACTION`

The workflow encodes a one-shot migration from an independent `DORE_LOCAL_VISION_MODEL` override to a single active `DORE_LOCAL_MODEL`. The current executable files already exhibit the workflow's intended post-migration state, while the workflow file itself still remains in the repository. Its migration instruction is therefore historical provenance, not a current work item or a reason to re-run cleanup.

A bounded commit search found no commit carrying the workflow's intended self-removal message (`fix(dore): remove independent visual engine override`), so the exact execution history of that one-shot workflow remains unproven. Current-state source evidence is sufficient to classify the migration goal as satisfied, but not to claim the workflow itself successfully executed.

## Durable lessons

1. Configuration convergence and visual competence are separate evidence layers. One active model source reduces drift but does not prove design quality.
2. One-shot migration workflows must not remain interpretable as live work after their target state is already present. Preserve them as provenance or explicitly retire them in the canonical index.
3. Current truth should be inferred from executable source plus runtime evidence, not from an old migration script's imperative wording.
4. This reconciliation does not modify P01 subtitle state or its existing production audio/transcription environment dependency.

## Current disposition

- single-source local model selection: retain as current implementation / maintenance baseline;
- independent local visual-model override: `SUPERSEDED`;
- one-shot cleanup workflow: `RETIRED-AS-ACTION`, retained only as historical provenance unless later repository hygiene safely removes it;
- D4 Penpot visual readback / Westside visual-quality proof: remains separately evidence-gated under `VIS-GRAMMAR` / `ME-015`.

## Canonical reconciliation note

A one-shot Actions-based attempt to append this finding into the Master Register, Sweep 01 checkpoint ledger, and Superseded/Retired Index entered an immediate no-job workflow failure. That failure is treated as a maintenance-path/tooling issue, not as evidence against the classification above and not as a new P01 blocker. The evidence is durably preserved here so a later Sweep pass can reconcile the canonical indices through a working write path without redoing discovery.
