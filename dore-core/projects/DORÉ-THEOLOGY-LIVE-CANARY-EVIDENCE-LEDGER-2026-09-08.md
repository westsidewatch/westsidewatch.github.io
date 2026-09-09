# DORÉ Theology Live Canary Evidence Ledger — 2026-09-08

Status: EVIDENCE_LEDGER / SWEEP_01
P01 impact: NONE
Parent lineage: `DORÉ-THEOLOGY-RECOVERY64-EVIDENCE-LEDGER-2026-09-08.md`

## Bounded evidence reviewed

- Sweep checkpoint 63 / recovery64 interpretation;
- merge `4aa9981e1535f3b66be8f962eaf02a3b85184b5e` — fixed localhost live-canary server, real `/chat` acceptance and owner-only self-hosted workflow;
- merge `137042122fbd85a8f99ee24af923edf35dbd53a1` — bilingual scoring correction;
- merge `9fb6acbd14dddc56e419cd7b239bbdcc30eb68a5` — tightened recovery examples/scoring behavior;
- merge `31ee52d73dac3dc672bdabaa5d1915880911b880` — per-case conversation isolation;
- Issue #516 persisted live-canary FAIL (`8/12`, ratio `0.6667`, zero degeneration) before per-case isolation;
- Issue #518 persisted live-canary PASS (`10/12`, ratio `0.8333`, zero degeneration) after per-case isolation;
- Issue #515 persisted `theology.shadow.acceptance64` PASS for the same recovery adapter (`21/24`, ratio `0.875`, zero degeneration), improving over base `17/24`, ratio `0.7083`.

## Reconciliation

1. The recovery64 line has crossed an additional bounded acceptance boundary. The fixed recovery adapter is not merely wired for evaluation: a persisted shadow64 acceptance result records `ok=true`, 8 cases, adapter ratio `0.875`, zero degenerate cases, and a positive four-hit delta over the base model. This supersedes checkpoint 63's narrower `TERMINAL_RUN_PENDING` interpretation for the shadow-acceptance part of the recovery proof.

2. A separate live-inference canary now exercises Doré's real `dore_local.H` `/chat` path while replacing only the inference function inside a localhost-only canary process. The canary pins `mlx-community/gemma-4-e4b-it-4bit`, the recovery64 adapter, offline model loading, no paid API, no canonical ingest, no adapter fusion, and no production-default change. This is materially stronger than an isolated evaluator because it includes the real handler and memory/context pipeline.

3. Issue #516 is a useful failed experiment rather than evidence against the adapter. All four requests succeeded and degeneration was zero, but one revelation-boundary answer repeated the preceding interfaith answer because the initial harness reused one conversation ID across semantically unrelated cases. That contaminated the evaluation with conversational memory and produced a failing `8/12` score.

4. Commit `31ee52d73dac3dc672bdabaa5d1915880911b880` corrected the harness by assigning a distinct conversation ID per case. Issue #518 then passed the same four-case live-canary contract at `10/12 = 0.8333`, zero degeneration, with the real `/chat` handler and the same recovery adapter. The earlier shared-conversation canary result is therefore `SUPERSEDED_AS_EVALUATION_TRUTH` for independent-case scoring, while remaining valuable provenance demonstrating why test-case isolation is necessary.

5. This is a bounded `VERIFIED_COMPLETE` milestone for **localhost live-path theological canary acceptance of the recovery64 adapter**. It does not authorize replacing Doré's production default model, fusing the adapter into the base model, canonicalizing the training examples, declaring Seminary formation complete, or claiming general theological authority. The canary itself explicitly records `production_default_changed=false`, `canonical_ingest=false`, `adapter_fused_into_base=false`, `paid_api_required=false`, and `localhost_only=true`.

6. The strongest reusable learning is evaluation-harness hygiene: independent held-out prompts must not accidentally share memory state unless cross-turn memory is itself the thing being tested. Stateful product paths require two distinct test modes—isolated-case behavioral acceptance and deliberate longitudinal-conversation acceptance—rather than silently mixing them.

7. The canonical active-map status does not require promotion. Seminary Core remains curriculum/in-progress; Scripture Canon remains foundation/in-progress; theology micro-training remains a bounded engineering/behavioral POC. The newly closed sub-milestone should be retained as capability evidence under those broader evidence gates.

8. P01 subtitle ordering, deployment, audio/transcription dependency, credentials, runtime state and existing environment blocker were not changed.

## Classification updates

- recovery64 shadow acceptance: `VERIFIED_COMPLETE` as a bounded 8-case offline shadow milestone;
- recovery64 localhost real-`/chat` canary: `VERIFIED_COMPLETE` as a bounded 4-case live-path canary milestone;
- shared-conversation independent-case harness: `SUPERSEDED` for this evaluation purpose;
- per-case conversation isolation: `CURRENT_GOVERNING_TEST_CONTRACT`;
- production-default theology model promotion/fusion: `PARKED / NOT_AUTHORIZED_BY_THIS_EVIDENCE`;
- broader Seminary/theological formation: unchanged and still evidence-gated.

## Revisit trigger

Reopen this bounded milestone only if the real `/chat` handler, memory assembly, model/adapter load path, scoring contract, or theological authority policy changes materially, or if a larger blind/adversarial live set reveals regression.

## Smallest next proof

Add a distinct longitudinal-memory canary whose cases are intentionally related across turns, while preserving the isolated-case live canary as a regression gate. Do not treat a stateful-memory test as a replacement for independent held-out scoring. No production-default promotion follows automatically from either test.
