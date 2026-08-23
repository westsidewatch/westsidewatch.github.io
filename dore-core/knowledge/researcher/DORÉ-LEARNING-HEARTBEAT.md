# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23

## Rule
Doré learning does not wait for a human to say `continue`, `execute`, `next`, or approve each course. On wake, read current state, execute `AUTONOMOUS_ALLOWED` work, self-check, persist evidence/failures/state/next action, and continue while evidence and authority remain clear. Course completion requires exam gates. Retention/transfer failures reopen learning.

Human approval is reserved for irreversible/destructive external actions, paid obligations, official outward doctrinal/editorial publication, brand/governance changes, new private credentials/access, material legal/security/privacy consequences, or genuine unresolved value conflicts.

## Major completed milestones
### Biblical Languages I
`BIBLICAL-LANGUAGES-I — Research Reading, not conversational fluency`: `PASS / GRADUATED`. Units 1–11, Hebrew/Greek practica and integrated finals passed. Reusable method nodes consolidated. Brain bridge regressions 01–06 passed.

### Researcher 04 — Autonomous Learning I
`RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE`. State: `COMPLETE → RETENTION_WATCH`. Final exam: 12/12 PASS.

### Researcher 05 — Biblical Concept Development I
`RESEARCHER-05 — BIBLICAL-CONCEPT-DEVELOPMENT-I — Diachronic and Canonical Research Method`: `PASS / GRADUATED → RETENTION_WATCH`.
Source stack and Units 01–07 passed. Unit 08 independent integrated transfer on resurrection passed 6/6 adversarial gate. Competence demonstrated across adversary, Spirit, canon/Scripture, and independent resurrection transfer without flattening corpora or retrojecting later formulations into earlier witnesses.

## Sensory-first status
Required first read this wake: `dore-core/memory/sensory-active.json`.
Result: file absent on `main`.
No user question was fabricated into repository memory.

The infrastructure failure remains bounded: `dore-core/memory/sensory-seed-diagnostic.json` records HTTP 500 / Cloudflare error 1101 from POST `/api/dore/sensory`; the claim step itself succeeds but receives no signal. Therefore the current blocker is PRODUCT → sensory ingestion runtime, not researcher knowledge.

## Latest completed actions
`POST_GRADUATION_DIAGNOSIS_FOR_RESEARCHER_06`: COMPLETE.
`SUBTITLE_PROOFREADER_PREREQUISITE_DIAGNOSTIC_01`: COMPLETE.

### Researcher 06 — Noise-Aware Scripture Retrieval I
Status: ACTIVE — UNITS 01–02 PASS.
Evidence: `RESEARCHER-06-NOISE-AWARE-SCRIPTURE-RETRIEVAL-I.md`.

Unit 01 established a ten-class noise taxonomy, four-layer provenance model (`observed` / `candidate` / `source` / `confidence`), and passed 8/8.

Unit 02 established bounded multi-channel candidate generation for Chinese/English noisy Scripture retrieval: lexical + phonetic neighborhoods, variable-length spans, biblical entity/transliteration candidates, adjacent-verse windows, N-best preservation, provenance, and pre-reranking pruning. It is grounded against ACL/NAACL/ROCLING evidence on Chinese homophone correction, phonological variable-length correction, multiple ASR hypotheses, named-entity denoising, and bounded phonetic candidate graphs. Adversarial gate: 10/10 PASS.

No product brain node has been promoted because ranking calibration and abstention are not yet proven.

## Current next action
`RESEARCHER_06_UNIT_03_RANKING_CALIBRATION_AND_ABSTENTION`.

Develop and adversarially test ranking principles combining lexical, phonetic, entity, local context, verse-window continuity, and corpus evidence. Explicitly prevent semantic/domain priors from overwhelming contradictory observed evidence. Define uncertainty margins and abstention behavior before product promotion.

Separately, PRODUCT → BRAIN closed-loop acceptance remains false until Cloudflare sensory POST stops returning 500/1101 and a signal is durably written then claimed into `sensory-active.json`.
