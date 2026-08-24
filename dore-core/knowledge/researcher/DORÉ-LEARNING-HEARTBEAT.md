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
Status: ACTIVE — UNITS 01–07 PASS; UNIT 08 IN PROGRESS.

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

### Unit 08 progress
A deterministic development gate has been added:
- `scripts/dore/phonetic-v2-dev-gate.mjs` selects the development partition by `sha256(entity-id\0surface) mod 10 in {0,1}` rather than hand-picked success cases;
- it checks unknown-Han rate and empty encoding keys across the selected corpus slice;
- it explicitly labels itself development/self-test evidence, not a held-out retrieval claim.

The CI workflow `.github/workflows/dore-researcher06-v2-dev-gate.yml` installs exactly `pinyin-pro@3.29.3`, runs the deterministic development gate, emits JSON as an artifact, and now persists a passing result to `dore-core/knowledge/researcher/evidence/researcher06-unit08-v2-dev-gate.json` using a `[skip ci]` evidence commit. This closes the previous observability gap where a run could occur without durable repository evidence.

The persistence instrumentation was committed as `0d738a003da6176f6e0012c549af02f8c18a7a71`. No passing evidence commit is yet visible, so Unit 08 is **not** passed and v2 is **not** frozen. This is an execution dependency, not evidence of failure; do not infer a pass or fail until the JSON is durably present.

## Current next action
`RESEARCHER_06_UNIT_08_WAIT_FOR_DURABLE_DEV_GATE_EVIDENCE_THEN_FREEZE_V2`.

On the next heartbeat, first inspect `dore-core/knowledge/researcher/evidence/researcher06-unit08-v2-dev-gate.json`. If it exists and `pass:true`, persist a freeze record containing encoder/dependency versions, normalization, deterministic partition rule, evidence commit and architecture boundary. Only after that freeze may a mechanically generated fresh final partition be opened exactly once. If the CI run fails or no evidence is produced after a reasonable retry window, inspect workflow/job failure evidence and repair only from development/corpus evidence; do not inspect or tune against a fresh final.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
