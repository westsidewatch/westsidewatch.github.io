# DORÉ MEMORY CONSOLIDATION SWEEP — 01
## Checkpoint 28 — English baseline witness / fail-closed evidence reconciliation (2026-09-02)

Status: `ACTIVE_PARALLEL` checkpoint
Primary sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Primary index: `DORÉ-MASTER-WORK-REGISTER.md`
Detailed evidence: `DORÉ-LANGUAGE-WITNESS-BASELINE-RECONCILIATION-2026-09-02.md`

### Bounded evidence reviewed

- Foundation Language/Text baseline access survey, witness registry, expansion matrix and four-tier access architecture;
- current `scripts/run_english_baseline_routes.py`;
- 2026-08-22 Language Core commit chronology;
- Language Core run 29 (`32589955459`) + artifact `9480058598`;
- fail-closed correction commit `732e4a1b50c3ca94d189b7d85156a2a88a047669`;
- external-reader baseline implementation commit `323b8a660a4f6032a11b5381f945597b64d85d7d`;
- Language Core run 31 (`32590171607`) + artifact `9480118432`.

### Reconciliation findings

1. The initial active witness registry contained planning-era states that became stale within the same day: ASV/KJV were still marked corpus candidates and major licensed English witnesses were still marked access-survey/human-only.
2. Workflow success must not be confused with milestone completion. Run 29 was green, but its persisted English-baseline report was `PARTIAL` (3 PASS / 8 `CREDENTIAL_REQUIRED`) because the runner had not yet been made fail-closed.
3. The next correction made the gate fail closed when `all_pass` is false. The later v2 route implementation added lawful external-reader fallback without retaining protected text.
4. Run 31 is decisive bounded completion evidence: the enforced workflow completed successfully and its persisted v2 report records 11/11 PASS plus `ENGLISH_BIBLICAL_WITNESS_BASELINE_COMPLETE`.
5. ASV and KJV are individually verified local-corpus milestones (66 books each; 31,157 and 31,102 verses respectively; zero validation errors in the persisted artifact). WEBU is also a passing local-corpus route in the baseline report. RSV, NRSVue, NASB2020, ESV, NIV, NLT, NET and CSB pass external-reader canonical-reference routes with no protected text retained.
6. The English witness baseline is therefore `VERIFIED_COMPLETE` as a bounded Language/Text access milestone. The four-tier access architecture remains current; the obsolete registry/expansion states are `SUPERSEDED` as current truth but retained as chronology.
7. This does **not** issue `BIBLICAL_CORPUS_READING_COMPLETE`: the broader Chinese baseline and cross-witness/comparison gates remain open. It also does not complete Scripture Canon Course 01, Seminary Core, Researcher global formation or reader acceptance.
8. The canonical Master Work Register workstream classifications remain materially correct (`SCRIPTURE-CANON` active foundation; Sweep active-parallel), so this checkpoint does not require a workstream status promotion/demotion. The active witness registry has been corrected in place and the detailed evidence ledger is durable.
9. No P01 subtitle runtime, deployment, audio/transcription dependency, credential, ordering or blocker state was changed.

### Durable updates

- created `DORÉ-LANGUAGE-WITNESS-BASELINE-RECONCILIATION-2026-09-02.md`;
- reconciled `CHINESE-ENGLISH-WITNESS-REGISTRY.yaml` to run-31 verified English states while preserving the still-open overall completion gate;
- retained the current Master Register classifications; no P01 action taken.

Sweep 01 remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and exposes no new human/environment blocker.
