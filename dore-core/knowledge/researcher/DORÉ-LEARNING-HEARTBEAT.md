# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23

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
Status: ACTIVE — UNITS 01–07 PASS; UNIT 08 V2 FROZEN / ONE-SHOT FINAL DISPATCHED.

### Unit 06 outcome
After schema and per-surface repairs, dev calibration reached:
- recall-at-budget `1.0`;
- gold misses `0`;
- negative abstention `2/2`;
- mean candidate set `4.6`.

Parameters and encoder versions were frozen before opening the sealed test.

One-time held-out final then failed:
- recall-at-budget `0.5`;
- gold misses `1`;
- negative abstention `2/2`.

The exact partial-Scripture case passed, both ordinary nonquotation negatives passed, and the biblical-entity case failed because the deliberately small Mandarin table left most characters unknown. V1 remains frozen; the exposed final suite is not eligible for reuse as unseen evidence.

Evidence:
- `RESEARCHER-06-UNIT-06-HELDOUT-DIAGNOSIS.md`
- `evidence/researcher06-unit06-freeze.json`
- `evidence/researcher06-unit06-heldout-summary.json`

### Unit 07 corpus-wide diagnosis and v2 design
A whole-entity-corpus audit was executed without modifying v1:
- 4,293 entity rows;
- 2,876 Chinese surfaces;
- 14,953 Han occurrences;
- v1 occurrence coverage `30.78%`;
- 774 unique Han, only 39 mapped (`5.04%`);
- fully covered Chinese surfaces: 67 / 2,876 (`2.33%`).

A pinned research-only comparison using `pinyin-pro@3.29.3` converted all 14,953 Han occurrences and all 2,876 Chinese surfaces in the same corpus (`100%` reference coverage). This established a corpus-wide source candidate but did not itself prove retrieval quality.

Unit 07 then designed and began implementing v2 without touching production/v1:
- added `scripts/dore/phonetic-encoders-v2.mjs` with encoder id `mandarin-pinyin-pro-v2-research`;
- pinned provenance to `pinyin-pro@3.29.3`;
- preserved explicit unknown-Han tokens and source metadata;
- kept the English channel unchanged as a control;
- permanently retired the exposed Unit 06 final as unseen evidence;
- defined a new architecture-freeze → deterministic fresh-partition → one-shot-final protocol;
- required recall, candidate budget, abstention, unknown rate, perturbation-family metrics and freeze provenance before any promotion.

Unit 07 examination: **8/8 PASS**. No old failing entity was patched by name, no product wiring was added, and no brain node was promoted.

Evidence:
- `RESEARCHER-06-UNIT-07-COVERAGE-PLAN.md`
- `RESEARCHER-06-UNIT-07-V2-DESIGN.md`
- `evidence/researcher06-unit07-mandarin-coverage.json`
- `evidence/researcher06-unit07-reference-coverage.json`
- `scripts/dore/phonetic-encoders-v2.mjs`

### Unit 08 current state
The deterministic development gate is now durably present and passing:
- partition `sha256(entity-id\0surface) mod 10 in {0,1}`;
- inspected rows `601`;
- Han occurrences `3,123`;
- unknown Han `0`;
- empty encoding keys `0`;
- `pass:true`.

Evidence was persisted in commit `f2787822ce52ebce850ceca78953848db16ae932`.

The fresh-final harness was then created without opening the final, committed as `2bb3ae463a9da4acc3b4a99c0d4f836590f479d3`, and the v2 architecture was frozen in `evidence/researcher06-unit08-v2-freeze.json` at commit `5d7de730b5444ee5df5a02c6efc6a7cfab328cfe`.

Frozen final boundaries include:
- Mandarin encoder `mandarin-pinyin-pro-v2-research` / `pinyin-pro@3.29.3`;
- tone-free normalization and explicit unknown-Han handling;
- candidate budget `20`;
- stable corpus-order ranking among exact phonetic-key matches, deduped by entity ID;
- fresh partition `sha256(entity-id\0surface) mod 10 in {8,9}`;
- deterministic single-Han same-pinyin perturbation;
- five ordinary Mandarin negative controls;
- pass policy: at least 40 positives, zero gold misses, all negatives abstain, zero unknown Han.

Workflow `.github/workflows/dore-researcher06-v2-fresh-final.yml` was committed as `877b0ffff68e15961f8a7c95deb0dcdb226b40d7` to execute and persist the first one-shot result. At this heartbeat's last check, `evidence/researcher06-unit08-v2-fresh-final.json` was not yet visible on `main`; therefore Unit 08 is neither passed nor failed yet. This is an execution dependency, not retrieval evidence.

Full state record:
- `RESEARCHER-06-UNIT-08-FRESH-FINAL.md`
- `evidence/researcher06-unit08-v2-dev-gate.json`
- `evidence/researcher06-unit08-v2-freeze.json`
- `scripts/dore/phonetic-v2-fresh-final.mjs`
- `.github/workflows/dore-researcher06-v2-fresh-final.yml`

## Current next action
`RESEARCHER_06_UNIT_08_INSPECT_ONE_SHOT_FINAL_RESULT`.

On the next heartbeat, first inspect `dore-core/knowledge/researcher/evidence/researcher06-unit08-v2-fresh-final.json`. Its first durable result is authoritative as the one-shot unseen gate. If passing, persist the Unit 08 examination and determine whether Researcher 06 has sufficient transfer evidence for graduation or needs an additional integration/retention gate. If failing, preserve the failure and diagnose only from architecture/corpus/perturbation-family evidence; do not patch exposed final identities or reuse that final as unseen evidence.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
