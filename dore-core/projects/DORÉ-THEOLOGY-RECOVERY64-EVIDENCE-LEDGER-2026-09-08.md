# DORÉ Theology Recovery64 Evidence Ledger — 2026-09-08

Status: EVIDENCE_LEDGER / SWEEP_01
P01 impact: NONE
Parent lineage: `DORÉ-THEOLOGY-STAGE64-EVIDENCE-LEDGER-2026-09-08.md`

## Bounded evidence reviewed

- Sweep checkpoint 61 and the Stage64 evidence ledger;
- merge `c42529cc84fcb66bda6ddb1b1b608e692e04cd87` — fixed bounded recovery64 continuation + self-hosted runner workflow;
- merge `738237810b75be925cb8002cfd335d0204d7b3b0` — recovery64 adapter resume-path correction;
- merge `f9f2c467d42ed20257db96f77cc51b89a0912e6d` — MLX-compatible resume-bundle correction;
- merge `9362f42301d8f6f4a608f89efaf7f5cf991e7f1f` — fixed recovery64 candidate eval/shadow routing and tests;
- repository chronology after Sweep checkpoint 62.

## Reconciliation

1. Checkpoint 61's `low-LR micro64 recovery: EVALUATION_PENDING` remains correct as an outcome classification, but the engineering state has advanced materially. A fixed recovery continuation now exists at 12 iterations / `1e-6`, using only eight bounded additional authority examples and explicitly preserving offline-only execution, no paid API, no canonical ingest, no adapter fusion, and no production-default change.

2. The recovery path is not an unconstrained training surface. The repository exposes a fixed `theology.training.recovery64` capability and a self-hosted macOS workflow triggered only by the repository owner using the exact issue title. The script accepts no caller arguments and uses fixed model/data/hyperparameter paths.

3. Two post-implementation corrections show that initial recovery wiring was not execution-complete. The resume path first required correction, then the MLX resume contract was changed to build a dedicated bundle containing `adapter_config.json` plus `adapters.safetensors`. These commits supersede the earlier direct adapter-directory resume interpretation. Historical code before the bundle correction must not be treated as the governing recovery implementation.

4. The evaluation boundary is now stronger. `theology.training.eval64` and `theology.shadow.acceptance64` are routed through fixed candidate wrappers that prefer the recovery adapter when present and otherwise fall back to the original n64 adapter. Candidate selection is repository-controlled rather than caller-controlled, and the existing held-out/degeneration gates remain the judging mechanism.

5. No persisted terminal recovery64 execution artifact, eval64 PASS, or shadow64 PASS was found in the bounded chronology reviewed here. Therefore implementation readiness must not be promoted into adapter acceptance. The current evidence proves **bounded recovery execution + candidate-gate wiring**, not successful theological behavior.

6. The correct current classification is therefore more precise than checkpoint 61 without changing the active-map status:
   - recovery64 execution path: `ACTIVE_PARALLEL / IMPLEMENTED_EXECUTION_PATH`;
   - MLX resume-bundle contract: `ACTIVE / CURRENT_GOVERNING_IMPLEMENTATION`;
   - earlier direct-resume wiring: `SUPERSEDED`;
   - recovery candidate eval/shadow gates: `ACTIVE / IMPLEMENTED_EVALUATION_GATE`;
   - recovery64 behavioral result: `UNKNOWN_NEEDS_EVIDENCE / TERMINAL_RUN_PENDING`;
   - 128/256 expansion: remains `PARKED / NOT_EVIDENCE_JUSTIFIED`.

7. This line remains an engineering proof-of-concept subordinate to Seminary/Scripture formation. It does not authorize canonical ingestion, base-model fusion/replacement, Seminary completion, theological-authority graduation, or stronger Doré autonomy claims.

8. P01 subtitle ordering, deployment, audio/transcription dependency, credentials, runtime state and existing environment blocker were not changed.

## Smallest next proof

Persist one real self-hosted recovery64 terminal report and route the resulting candidate through both fixed `eval64` and `shadow64` gates. The durable result must include exact candidate identity, effective continuation settings, timing/resource metrics, adapter-load fingerprint, all held-out outputs/scores, degeneration checks, and explicit offline/no-paid/no-canonical-ingest/no-fusion/no-production-default-change fields. Do not open 128/256 unless the bounded candidate passes the existing gates.
