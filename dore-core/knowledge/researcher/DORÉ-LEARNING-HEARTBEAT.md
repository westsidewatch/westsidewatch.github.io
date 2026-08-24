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

This proves **durable sensory memory → autonomous research → examination → product-readable brain consolidation**. Browser-side ingestion remains a separate acceptance surface.

### Brain → Product generic bridge acceptance
The generic bridge now loads the live brain endpoint rather than a frozen deployment-local snapshot. `scripts/dore/brain-bridge-regression.mjs` tests three Mary question variants against `research.nt.mary-count` plus a Scripture-routing probe, using the same generic normalization/scoring contract as `static/dore/dore-brain-bridge.js`. No Mary-specific answer branch exists in the product bridge; the only Mary strings in the regression are test inputs/expected node ids. This establishes the repository-level Brain → Product regression surface. Live browser acceptance remains separate from repository-level regression.

## Researcher 06 — Noise-Aware Scripture Retrieval I
Status: ACTIVE — UNITS 01–05 PASS; UNIT 06 IN PROGRESS.
Evidence: `RESEARCHER-06-NOISE-AWARE-SCRIPTURE-RETRIEVAL-I.md`, `RESEARCHER-06-UNIT-05-HARNESS-SPEC.md`, `RESEARCHER-06-UNIT-06-PHONETIC-ENCODER-SPEC.md`.

Unit 01: noise taxonomy + observed/candidate/source/confidence model, 8/8 PASS.
Unit 02: bounded lexical/phonetic/entity/window/N-best candidate generation, 10/10 PASS.
Unit 03: evidence-fusion ranking, surface-evidence veto, weak domain priors, top-two margin reasoning, conflict-aware confidence, calibrated abstention requirement, 12/12 PASS.
Unit 04: reusable Chinese/English phonetic-index architecture, explicit encoder/alias/span provenance, bounded neighborhoods, variable-length spans, separated fixture schema and measurement contract, 12/12 adversarial design gate PASS.
Unit 05: executable non-production measurement harness + separated dev/sealed-test fixtures + tuning guard, 8/8 PASS.
Unit 06: reproducible versioned encoder implementation committed. `mandarin-pinyin-lite-v1` and `english-metaphone-lite-v1` are integrated into the non-production harness. A dedicated dev calibration workflow persists machine-readable evidence.

First measured dev run: FAIL — recall-at-budget `0`, three gold misses, while both negative abstention fixtures were correctly empty. This exposed an instrumentation/schema failure: the harness read `original-index.json` generically instead of the product `search-index.json`, and flattened entity data incorrectly. The harness was repaired to consume the real Scripture and entity schemas.

Second measured dev run after that repair: FAIL — recall-at-budget `0.6667`, one gold miss, mean candidate set `4.2`, and both negative abstention fixtures remained correctly empty. Exact Scripture and entity retrieval now pass. The remaining miss is `dev-phonetic-zh-trad-simp` (`马利亚` → gold `馬利亞`). Diagnosis: entity aliases were concatenated into one row before phonetic encoding, so exact phonetic comparison tested the whole concatenated alias string rather than each candidate surface independently. This is a representation bug, not a justified encoder failure. The harness is now repaired to retain per-row `surfaces[]` and compare the query phonetic key against each primary/alias surface separately. No held-out fixtures have been opened.

## Current next action
`RESEARCHER_06_UNIT_06_OBSERVE_SURFACE_AWARE_DEV_CALIBRATION`.

Observe the dev rerun after commit `c1ef630407bfd24d1d5cc35953d695f0e9114645`. If development recall reaches the Unit 06 gate while negative abstention remains intact, freeze parameters/version identifiers before opening the sealed held-out final test. If dev still fails, diagnose only against dev evidence. Do not wire production or promote a Researcher-06 brain capability before held-out evidence passes.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are now evidenced. The remaining product acceptance is browser-level: verify a current Search deployment itself POSTs a fresh unknown query into sensory memory and, after consolidation, surfaces the live brain result without per-question UI logic.
