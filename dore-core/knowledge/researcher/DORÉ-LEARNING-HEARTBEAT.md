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
Status: ACTIVE — UNITS 01–05 PASS; UNIT 06 HELD-OUT FAIL; UNIT 07 IN PROGRESS.

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

### Unit 07 corpus-wide diagnosis
A whole-entity-corpus audit was executed without modifying v1:
- 4,293 entity rows;
- 2,876 Chinese surfaces;
- 14,953 Han occurrences;
- v1 occurrence coverage `30.78%`;
- 774 unique Han, only 39 mapped (`5.04%`);
- fully covered Chinese surfaces: 67 / 2,876 (`2.33%`).

This proves the held-out miss is one symptom of a broad coverage deficit, not a single-name bug.

A pinned research-only comparison using `pinyin-pro@3.29.3` then converted all 14,953 Han occurrences and all 2,876 Chinese surfaces in the same corpus (`100%` reference coverage). This is only a source/architecture experiment; no production dependency, v1 mutation, product wiring, or brain promotion has occurred.

Evidence:
- `RESEARCHER-06-UNIT-07-COVERAGE-PLAN.md`
- `evidence/researcher06-unit07-mandarin-coverage.json`
- `evidence/researcher06-unit07-reference-coverage.json`

## Current next action
`RESEARCHER_06_UNIT_07_DESIGN_V2_AND_FRESH_EVALUATION_PROTOCOL`.

Design the v2 pronunciation architecture from corpus-wide evidence, preserving version/provenance and unknown handling. Before claiming generalization, establish a fresh leakage-safe evaluation protocol that is not the exposed Unit 06 test. Do not promote to product/brain until a new held-out gate passes.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
