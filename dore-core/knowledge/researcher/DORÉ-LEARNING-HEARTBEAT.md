# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23
Updated: 2026-08-24

## Rule
Doré learning does not wait for a human to say `continue`, `execute`, `next`, or approve each course. On wake, read current state, execute `AUTONOMOUS_ALLOWED` work, self-check, persist evidence/failures/state/next action, and continue while evidence and authority remain clear. Course completion requires exam gates. Retention/transfer failures reopen learning.

Human approval is reserved for irreversible/destructive external actions, paid obligations, official outward doctrinal/editorial publication, brand/governance changes, new private credentials/access, material legal/security/privacy consequences, or genuine unresolved value conflicts.

## Major completed milestones
- Biblical Languages I: `PASS / GRADUATED`.
- Researcher 04 — Autonomous Learning I: `COMPLETE → RETENTION_WATCH`, final 12/12 PASS.
- Researcher 05 — Biblical Concept Development I: `PASS / GRADUATED → RETENTION_WATCH`, independent resurrection transfer 6/6 PASS.
- First durable sensory → research → brain consolidation: `馬利亞有幾位?` consolidated to `research.nt.mary-count` after independent research and 7/7 examination.
- Generic Brain → Product repository regression established without per-question answer logic.

## Sensory state checked this heartbeat
`dore-core/memory/sensory-active.json` contains no `RESEARCHING` signal without a `brain_node`. Existing Mary signal remains `CONSOLIDATED`; therefore no live sensory research preempted the course loop.

## Researcher 06 — Noise-Aware Scripture Retrieval I
Status: ACTIVE — UNITS 01–08 PASS; UNIT 09 ACTIVE / INTEGRATION CONTRACT FROZEN.

### Unit 06 honest failure
After dev calibration reached recall-at-budget 1.0 with zero gold misses, the frozen one-time held-out final failed at recall 0.5 because the deliberately small Mandarin mapping covered only a small fraction of the biblical entity corpus. V1 remains frozen and that exposed final is permanently retired as unseen evidence.

### Unit 07 corpus-wide repair
Corpus audit showed 2,876 Chinese entity surfaces / 14,953 Han occurrences but only 30.78% occurrence coverage under v1. A pinned research-only `pinyin-pro@3.29.3` reference covered the corpus, leading to `mandarin-pinyin-pro-v2-research` without identity-specific patches. Unit 07 examination: 8/8 PASS.

### Unit 08 authoritative fresh final
The first durable result at `evidence/researcher06-unit08-v2-fresh-final.json` is authoritative for the frozen v2 architecture:
- positives: 80;
- recall-at-budget: 1.0;
- gold misses: 0;
- negative abstention: 5/5;
- unknown Han rate: 0;
- mean candidate set: 2.4941;
- perturbation family: single-Han same-pinyin;
- pass: true.

`RESEARCHER-06-UNIT-08-EXAM.md` records the 8/8 PASS. This proves the corpus-wide v2 Mandarin encoder repaired the v1 coverage failure for the tested unseen biblical-entity perturbation while preserving conservative negative abstention. It does not alone prove mixed transcript-noise correction, subtitle editing safety, calibrated ambiguity handling, or production readiness.

### Unit 09 — Offline Integration Transfer Gate
Unit 09 remains active. This heartbeat completed the authorized design/freeze stage:
- added `fixtures/noise-retrieval-unit09-dev.json`, an exposed development-only mixed-noise fixture set spanning exact/partial Scripture, homophone/entity corruption, deletion/insertion, alias/transliteration, ambiguity and ordinary negatives;
- added `RESEARCHER-06-UNIT-09-FREEZE.md` freezing the product-neutral result schema, adapters, decision surface, ambiguity/abstention policy, encoder identity and fresh-final protocol;
- explicitly prohibited the development fixtures and exposed Unit 06 final from being reused as unseen evidence.

No fresh final has been opened. No PASS is claimed from fixture authorship alone.

## Current next action
`RESEARCHER_06_UNIT_09_IMPLEMENT_GENERIC_OFFLINE_TRANSFER_HARNESS_AND_RUN_DEV_GATE`.

Implement one generic retrieval object consumed unchanged by Search-like and subtitle-proofreader adapters. Run only the exposed development partition first and persist the result. If the development gate satisfies provenance, abstention and shared-adapter invariants, author/seal a separate fresh final partition and run it once. A fresh failure must be preserved and diagnosed generically.

## Brain/Product status
This heartbeat changed no product-readable knowledge node, so no Brain → Product regression was required. Researcher 06 remains research-only and is not production-promoted.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
