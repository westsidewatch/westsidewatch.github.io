# DORÉ Theology Stage64 Evidence Ledger — 2026-09-08

Status: EVIDENCE_LEDGER / SWEEP_01
P01 impact: NONE

## Bounded evidence reviewed

- `DORÉ-THEOLOGY-STAGE32-EVIDENCE-LEDGER-2026-09-08.md` and Sweep checkpoint 59;
- PR #480 / merge `e4c1ef6f3a7966ee2230a74eedf50d01132f632a` — fixed offline held-out `theology.training.eval32` gate;
- PR #482 / merge `9ca338274b92f5d39385ab3586a2c60147038c3f` — micro32 adapter-load correction into an MLX-VLM bundle;
- PR #486 / merge `d0ce37c5dd5a816485e39631a57120cb4c353c70` — bounded stage64/micro64/eval64 escalation path;
- PR #490 / merge `d672923f390ddf1cba4583c9ddecad2d8c92df97` — lower-LR micro64 recovery and stronger multilingual degeneration guard;
- repository commit chronology through `80ab229e7e623376b4747051fb06d3e9148dbf23`.

## Reconciliation

1. Checkpoint 59's exact next-step wording is now historically stale in one narrow sense: the engineering line did open a 64-example path after micro32 held-out behavioral failure. PR #486 explicitly states that stage64/micro64/eval64 were added **after micro32 held-out behavioral failure**. The governing principle remains minimum-sufficient learning, but `keep 64 closed unless 32 materially improves` no longer describes actual chronology.

2. The 32-example line gained a real fixed held-out evaluator before escalation. PR #480 defines eight bilingual held-out ministry prompts, compares base versus adapter, requires at least 80% adapted concept coverage with no regression, and keeps evaluation offline, fixed-input, no-paid-API, no-canonical-ingest and no-fusion. This is a meaningful evaluation-contract milestone, not evidence that micro32 passed it.

3. PR #490 records an important observed failure narrative: **micro32 and the first micro64 both loaded correctly but collapsed on held-out generation**. This is stronger than checkpoint 59's earlier `UNKNOWN_NEEDS_EVIDENCE` about whether an adapter ever loaded, but the PR description is not a persisted machine-readable terminal evaluation artifact. Current classification is therefore `FAILED_HELDOUT / NARRATIVE_EVIDENCE`, not a verified numeric benchmark.

4. The first 64-example path is a bounded experimental escalation, not a graduation. PR #486 keeps the same cached Gemma 4 base, exactly 64 positive bilingual authority examples, fixed A2A actions, offline execution, no caller-controlled model/path/prompt/shell, no paid API, no canonical ingest and no adapter fusion. `eval64` reuses the same eight held-out prompts and adds an obvious-repetition degeneration guard.

5. The first micro64 training pressure was judged too high after held-out collapse. PR #490 lowers the fixed LoRA learning rate from `2e-5` to `2e-6`, reduces updates from 40 to 24, records the effective learning rate, and strengthens multilingual degeneration detection to catch Chinese substring loops and repeated spans. This supersedes the original micro64 hyperparameter choice; it does not prove that the recovery run passes.

6. The latest repository chronology contains no later persisted terminal low-LR micro64/eval64 result after merge `d672923...`; only routine sensory heartbeat persistence follows in the bounded commit window. Therefore the recovered 64-example adapter remains `ACTIVE_PARALLEL / EVALUATION_PENDING`, and no move to 128/256 is evidence-justified.

7. A safety-quality lesson is now durable: simple concept-hit scoring is insufficient when generation can collapse into repetition while still containing target terms. Theology adapter evaluation must include multilingual degeneration/repetition detection alongside concept coverage and no-regression comparison. This is reusable evaluation doctrine for any future small-adapter training path.

8. No evidence in this batch authorizes canonical ingestion of the quarantine data or adapter, replacement/fusion of the base model, broad theological-authority claims, Seminary completion, or `DORÉ_ALIVE` promotion.

9. No P01 subtitle state, ordering, deployment, credential, audio/transcription dependency or blocker was modified.

## Current classification

- fixed micro32 held-out evaluator: `ACTIVE / IMPLEMENTED_EVALUATION_GATE`;
- micro32 held-out behavior: `FAILED_HELDOUT / NARRATIVE_EVIDENCE`;
- first micro64 hyperparameter setting (`2e-5`, 40 iterations): `SUPERSEDED`;
- stage64 dataset/control-plane path: `ACTIVE_PARALLEL / IMPLEMENTED_PREPARATION`;
- low-LR micro64 recovery (`2e-6`, 24 iterations): `ACTIVE_PARALLEL / EVALUATION_PENDING`;
- eval64 multilingual degeneration guard: `ACTIVE / IMPLEMENTED_EVALUATION_GATE`;
- 128/256 escalation: `PARKED / NOT_EVIDENCE_JUSTIFIED`;
- canonical ingest / adapter fusion: `RETIRED_AS_CURRENT_ACTION / PROHIBITED_UNTIL_SEPARATE_ADMISSION`.

## Smallest next proof

Persist one terminal low-LR `micro64` + `eval64` artifact from the real Mac with: exact model and adapter identity, effective LR/iterations, wall-clock and peak unified memory, adapter size/load fingerprint, all eight base/adapted outputs, concept scores, zero-degeneration result, and explicit offline/no-paid/no-canonical-ingest/no-fusion fields. If it fails, stop and diagnose before any 128-example expansion; if it passes, treat that as a bounded adapter-evaluation milestone only, not theological or Seminary graduation.
