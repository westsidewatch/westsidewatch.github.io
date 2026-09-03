# Doré Language Witness Baseline Reconciliation — 2026-09-02

Status: SWEEP-01 EVIDENCE LEDGER / BOUNDED RECONCILIATION
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`
Scope: Foundation Language/Text baseline witness chronology; no P01 mutation.

## Sources reviewed

- `dore-core/knowledge/foundation/language-text/BASELINE-ACCESS-SURVEY-01.md`
- `dore-core/knowledge/foundation/language-text/CHINESE-ENGLISH-WITNESS-REGISTRY.yaml`
- `dore-core/knowledge/foundation/language-text/LANGUAGE-WITNESS-EXPANSION-MATRIX.yaml`
- `dore-core/knowledge/foundation/language-text/WITNESS-ACCESS-ARCHITECTURE.md`
- `scripts/run_english_baseline_routes.py`
- Language Core commit chronology on 2026-08-22
- GitHub Actions `Doré Language Core` run `32589955459` (run 29) and artifact `9480058598`
- GitHub Actions `Doré Language Core` run `32590171607` (run 31) and artifact `9480118432`

## Chronology and contradiction

The initial active witness registry was created before the later Language Core ingestion and route work. It therefore still records KJV and ASV as `local_corpus_candidate / source_and_license_survey_required` and the major licensed English witnesses as `human_only / licensed_access_survey_required`. Those states are no longer current.

The first workflow labeled `run complete English baseline witness gate` is also not sufficient completion evidence by itself. Run 29 (`32589955459`) completed successfully, but its persisted `DORÉ-ENGLISH-BASELINE.json` was schema v1 with only 3/11 witnesses passing and 8 licensed witnesses at `CREDENTIAL_REQUIRED`; overall status was `PARTIAL`. At that commit, the runner did not yet fail the process when `all_pass` was false. Commit `732e4a1b50c3ca94d189b7d85156a2a88a047669` immediately corrected this by adding fail-closed `SystemExit(1)` behavior.

The later v2 implementation then added lawful external-reader fallback for licensed witnesses without retaining protected text. Commit `323b8a660a4f6032a11b5381f945597b64d85d7d` triggered Language Core run 31 (`32590171607`), which completed successfully under the fail-closed gate. Its persisted artifact is decisive bounded evidence:

- `DORÉ-ENGLISH-BASELINE.json`: schema `dore.english-baseline.v2`, status `PASS`, milestone `ENGLISH_BIBLICAL_WITNESS_BASELINE_COMPLETE`, 11/11 witnesses PASS;
- WEBU, ASV and KJV are local-corpus routes;
- ASV: 66 books / 31,157 verses / validation errors `[]` / PASS;
- KJV: 66 books / 31,102 verses / validation errors `[]` / PASS;
- RSV, NRSVue, NASB 2020, ESV, NIV, NLT, NET and CSB pass canonical-reference external-reader routes, with `text_retained: false` and no protected full-text persistence.

## Classification

### ENGLISH_BIBLICAL_WITNESS_BASELINE_COMPLETE

Classification: `VERIFIED_COMPLETE` as a bounded English witness-access milestone.

Original objective: give Doré a lawful, provenance-aware baseline across important English Bible witnesses without conflating research access with permission to mirror copyrighted text.

Completion evidence: enforced Language Core run 31 plus persisted artifact `9480118432`, not the earlier run title or commit message alone.

Current quality: strong for the defined access-routing contract. It separates local corpora from licensed/external-reader access and deliberately avoids retaining protected text. It does not prove corpus-wide textual comparison quality for every licensed witness, long-term external-reader stability, or broader Foundation graduation.

What was learned: workflow success is not completion evidence unless the task gate itself fails closed; access to a witness and possession of a witness are different states; rights/provenance attach to exact witness/provider/snapshot, not merely a version label.

Weakness / debt: the active witness registry and expansion matrix still contain planning-era states that predate later ingestion and route verification. Those documents can mislead future resume logic unless read chronologically.

Revisit trigger: a provider route changes, a rights policy changes, a baseline witness edition changes, or comparison requirements require a stronger licensed API rather than navigation-only external-reader access.

Disposition: retain the English baseline milestone closed; maintain route/rights regression; reconcile stale planning-state metadata rather than rerun completed ingestion by default.

## Superseded state interpretation

The following old states are `SUPERSEDED` as current execution truth while retained as historical provenance:

- KJV and ASV `local_corpus_candidate / source_and_license_survey_required` in the initial registry;
- licensed English witnesses `human_only / licensed_access_survey_required` where run 31 proves a lawful Tier-3 external-reader route;
- `source_selection` for the open-English onboarding milestone in the early expansion matrix;
- any inference that Language Core run 29 proved the English baseline complete merely because the workflow conclusion was success.

The governing access architecture itself is not superseded. Its four-tier rights model remains sound and is the reason the later v2 baseline can be considered complete without copying copyrighted full text.

## Boundary: overall Foundation corpus milestone remains open

`ENGLISH_BIBLICAL_WITNESS_BASELINE_COMPLETE` is not the same claim as `BIBLICAL_CORPUS_READING_COMPLETE`.

The broader baseline completion gate also requires the Chinese baseline witness family and comparison/coverage requirements. The current Chinese registry still contains several human-only/access-survey-pending states. Therefore no global `BIBLICAL_CORPUS_READING_COMPLETE` token is justified from this batch.

This also does not complete Scripture Canon Course 01, Seminary Core, global Researcher formation, or the dedicated original-language reader acceptance boundary.

## P01 impact

None. No subtitle runtime, deployment, credential, audio/transcription path, ordering or blocker state was changed by this reconciliation.
