# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23

## Rule
Doré learning does not wait for a human to say `continue`, `execute`, `next`, or approve each course. On wake, read current state, execute `AUTONOMOUS_ALLOWED` work, self-check, persist evidence/failures/state/next action, and continue while evidence and authority remain clear. Course completion requires exam gates. Retention/transfer failures reopen learning.

Human approval is reserved for irreversible/destructive external actions, paid obligations, official outward doctrinal/editorial publication, brand/governance changes, new private credentials/access, material legal/security/privacy consequences, or genuine unresolved value conflicts.

## Major completed milestones
### Biblical Languages I
`PASS / GRADUATED`. Units 1–11, Hebrew/Greek practica and integrated finals passed. Reusable method nodes consolidated.

### Researcher 04 — Autonomous Learning I
`COMPLETE → RETENTION_WATCH`. Final exam: 12/12 PASS.

### Researcher 05 — Biblical Concept Development I
`PASS / GRADUATED → RETENTION_WATCH`. Independent resurrection transfer passed 6/6 adversarial gate.

### First durable sensory → research → brain consolidation
Signal `5cf2c608-e66f-4176-a3f8-b3284819158a`, query `馬利亞有幾位?`, was durably claimed as `RESEARCHING`, independently researched, counter-checked, passed a 7/7 gate, promoted generically as `research.nt.mary-count`, and written back to `sensory-active.json` as `CONSOLIDATED` with a real `brain_node`.

This proves the previously missing middle of the closed loop: **durable sensory memory → autonomous research → examination → product-readable brain consolidation**. It does not by itself prove that every Search browser deployment is posting correctly; browser-side ingestion remains a separate acceptance surface.

Evidence: `dore-core/knowledge/researcher/live/SENSORY-5cf2c608-MARY-COUNT.md`, `dore-core/memory/sensory-active.json`, `static/dore/brain/knowledge-index.json`.

## Researcher 06 — Noise-Aware Scripture Retrieval I
Status: ACTIVE — UNITS 01–04 PASS.
Evidence: `RESEARCHER-06-NOISE-AWARE-SCRIPTURE-RETRIEVAL-I.md`.

Unit 01: noise taxonomy + observed/candidate/source/confidence model, 8/8 PASS.
Unit 02: bounded lexical/phonetic/entity/window/N-best candidate generation, 10/10 PASS.
Unit 03: evidence-fusion ranking, surface-evidence veto, weak domain priors, top-two margin reasoning, conflict-aware confidence, calibrated abstention requirement, 12/12 PASS.
Unit 04: reusable Chinese/English phonetic-index architecture, explicit encoder/alias/span provenance, bounded neighborhoods, variable-length spans, separated fixture schema and measurement contract, 12/12 adversarial design gate PASS. Production parameters remain uncalibrated and no capability was promoted to brain.

## Current next action
`RESEARCHER_06_UNIT_05_BUILD_EXECUTABLE_FIXTURE_HARNESS_AND_MEASURE_BASELINE`.

Implement a non-production reference harness and separated dev/test fixtures against existing Scripture/entity data. Measure candidate recall@K, candidate-set growth/latency, negative false-candidate behavior, alias normalization and abstention. Do not tune on the final test set and do not wire into production yet.

## Closed-loop next acceptance
Run Brain → Product regression for `research.nt.mary-count`: verify a generic Search brain lookup can surface the new node without per-question UI logic. Separately verify a current Search browser deployment can itself POST a fresh unknown query into sensory memory; do not infer that browser acceptance solely from the successful durable signal.
