# DORÉ MEMORY SWEEP — CHECKPOINT 20

Status: ACTIVE_PARALLEL / BOUNDED BATCH COMPLETE
Date: 2026-08-26
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Primary index: `DORÉ-MASTER-WORK-REGISTER.md`
Previous checkpoint: `DORÉ-MEMORY-SWEEP-CHECKPOINT-19.md`

## Bounded batch — Westside Stories / Doré external-worker product history

Reviewed:
- canonical `DORÉ-MASTER-WORK-REGISTER.md`
- `westsidewatch/Westside-Stories` repository history and current product files
- `README.md`
- `ROADMAP.md`
- `docs/DORE-FIRST-EXTERNAL-WORKER-MILESTONE.md`
- `app/dore_proofreader.py`
- `app/main_dore.py`
- `build_app.command`
- commits `5362c912672577880970bb78f83af999f4696bcd`, `b19b9b9e324df2ccfeb0a3b016e6255a1a874e22`, `f85401a0f0a66fd497183f71831367481430e872`, `eb651bcd864819233efeb84da53fc5ba8513949f`, `44e44aa2f10d53d2c04b0c1b80d892b7c862643d`
- `DORÉ-COMPLETED-WORK-LEDGER.md`

## Findings and classifications

1. **Westside Stories 1.0 is a real historical product release.** Its repository identifies a macOS Apple-Silicon subtitle application with local MLX Whisper transcription, SRT generation, optional subtitle burn-in, Traditional Chinese + English UI and local processing. This is product-history evidence, but the Sweep does not infer current distribution/adoption quality from the release label alone.

2. **The later Doré proofreading integration is materially stronger than the Master Register's old wording `integration line exists`.** The product contains a concrete service client for `dore.subtitle-proofread.v1`, a Doré-aware production worker, and a build script that packages `app/main_dore.py` as the application entry point.

3. **The external-worker milestone is accepted as a bounded historical `VERIFIED_COMPLETE` implementation/service-boundary milestone.** `docs/DORE-FIRST-EXTERNAL-WORKER-MILESTONE.md` explicitly records `COMPLETE / PASS`; current code independently corroborates its declared architecture rather than leaving it as a memo-only claim.

4. **The completion boundary is narrow.** It proves a concrete executable consumer outside the main Westside Watch site, conservative contract semantics, explicit failure, SRT index/timestamp preservation and a Doré-aware production/package entry point. It does **not** prove that a packaged `.app` has been independently run end-to-end against the current live Doré endpoint.

5. **WSS overall therefore remains `ACTIVE_PARALLEL`, not `VERIFIED_COMPLETE`.** The next evidence target is a packaged macOS App run covering either Whisper output or an existing SRT → live Doré endpoint → corrected SRT → optional burn-in/result, with persisted runtime/release evidence.

6. **The WSS roadmap contains a superseded future claim.** `ROADMAP.md` still lists `Optional AI proofreading` under Future even though Doré proofreading is already wired into the production entry path. This is documentation/history debt; it must not be interpreted as current product state. The Sweep did not modify the WSS product repository in this batch.

7. **The reviewed WSS root evidence does not expose a visible CI/test suite for live-contract regression.** This is not proof that no tests exist anywhere, but it is insufficient evidence for live packaged-product reliability. The Master Register therefore now names the missing end-to-end verification explicitly.

## Completed-work ledger update

Added:

`CW-012 — Westside Stories first Doré external-worker integration`

Disposition:
- bounded service-boundary/executable-consumer milestone: `VERIFIED_COMPLETE`;
- packaged-App live Doré execution: still open;
- WSS product: remains `ACTIVE_PARALLEL`.

The ledger records the conservative service contract, structure-preserving SRT adapter, Doré-aware production entry point, packaging path, current debt and reopen trigger.

## Canonical register reconciliation

Updated the WSS row to replace the vague prior state with evidence-bounded current truth:

- WSS 1.0 exists as the local subtitle-app baseline;
- Doré proofreading is part of the production entry/build path through `dore.subtitle-proofread.v1`;
- repository evidence proves the executable consumer boundary;
- end-to-end packaged-App execution against the live endpoint remains the next milestone.

Updated the Sweep row to record Main + WSS product-history reconciliation and move the next bounded batch to remaining product-history/evidence families.

## P01 protection

No P01 code, runtime state, deployment path, blocker state, Cloudflare configuration or subtitle critical-path ordering was modified.

The current P01 `ENVIRONMENT_BLOCKED` state remains governed by the existing runtime/checkpoint evidence. WSS verification is not allowed to substitute for or interrupt P01.

## Next bounded batch

Continue one remaining material product-history/evidence family, prioritizing Journal/Main sub-surfaces not already covered, Liming Library presentation/runtime history, or remaining Cloudflare structured-runtime history. Reconcile only evidence that changes current truth, completion judgment, supersession history or missing-evidence boundaries.

Do not interrupt or replace P01.