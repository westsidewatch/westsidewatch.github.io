# DORÉ MEMORY SWEEP — CHECKPOINT 15

Status: PARTIAL / CONTINUE
Date: 2026-08-26
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Primary index: `DORÉ-MASTER-WORK-REGISTER.md`
Previous checkpoint: `DORÉ-MEMORY-SWEEP-CHECKPOINT-14.md`

## Bounded batch — Bible Search first work-node / live relevance evidence reconciliation

Reviewed:
- `dore-core/knowledge/BIBLE-SEARCH-WORK-NODE.md`
- `dore-core/knowledge/search-cognition-protocol.md`
- `dore-core/tests/search-cognition-understanding-gate.md`
- `dore-core/tests/search-browser-negative-relevance.mjs`
- commit `9b8a7a649e21c39f622ba8e29df0932056c31125` and its persisted negative-relevance evidence lineage
- `dore-core/projects/TEMP-BIBLE-SEARCH-FAILURE-SIGNALS-2026-08-25.md`
- current `DORÉ-MASTER-WORK-REGISTER.md`
- current `DORÉ-MISSING-EVIDENCE-REGISTER.md`
- current `DORÉ-COMPLETED-WORK-REVISIT-QUEUE.md`

## Findings and classifications

1. **The original Bible Search work-node milestone was legitimately earned, but it is not a current product-quality completion claim.** `BIBLE-SEARCH-WORK-NODE.md` establishes the first external Doré Scripture-search service boundary and a v0.1 contract covering reference/text/lemma/morphology/fuzzy retrieval with canonical witness/provenance fields. Its own contract already says fuzzy retrieval returns candidates only and must not be represented as certainty. The service-boundary decision remains current and useful.

2. **The live Search workstream remains correctly classified `MAINTENANCE + DISCOVERY`, not `VERIFIED_COMPLETE`.** The Master Register already records negative-relevance regression protection and a cognition gate still at `TAUGHT`. Nothing in this batch justifies promoting Search to concept/product complete.

3. **Existing negative-relevance evidence is real but bounded.** `search-browser-negative-relevance.mjs` protects two unrelated English multiword fixtures (`Mortal Shell II`, `Grand Theft Auto`) from fabricated Scripture hits while preserving explicit Chinese/English references and one single-term fuzzy case. The CI workflow persists a PASS artifact for that bounded contract. This is meaningful regression evidence, not proof that arbitrary unrelated production queries abstain correctly.

4. **The current external real-use memo exposes a fired revisit trigger in both directions.** F1 records a relevant cross-version lexical/concept query (`Tablets of the Testimony`) failing to adequately retrieve KJV `tables of the testimony`; F2 records an unrelated English combination still producing Scripture. These are respectively false-negative and false-positive signals. They are not safely reducible to a single synonym patch or to the already-passing two-fixture negative-relevance test.

5. **The cognition protocol is sound doctrine but remains ungraduated.** It requires Doré to distinguish SEARCH / QUESTION / HYBRID / uncertain intent and to explain the choice in terms of user intent. The understanding gate explicitly remains `TAUGHT`; unseen transfer and live product routing are still required for `CONCEPT_PASS` / `PRODUCT_PASS`.

6. **The original Search node is therefore a `COMPLETED_REVISIT_CANDIDATE`, while current Search remains active maintenance/discovery.** This is a historical-completion/current-quality distinction: the first work node can remain legitimately earned even though current association, relevance calibration, abstention and self-repair behavior require another pass.

7. **The revisit trigger is high-value but must not interrupt P01.** A live user-facing Scripture-search failure deserves high learning priority, especially where underlying Bible/version knowledge appears to exist but retrieval cannot connect it. However, the active P01 subtitle path remains the canonical critical path. Search diagnosis/evaluation should proceed when dependency-safe or in bounded parallel work that does not displace P01.

8. **A stronger Search repair claim requires Doré-owned diagnosis and unseen transfer, not merely repaired examples.** The temporary memo intentionally supplies external evidence without prescribing the final root cause. Completion requires Doré to persist its own diagnosis, isolated-vs-systemic scope judgment, repair rationale, broader unseen regression results and durable learning; later similar failures should be detected without another human prompt.

9. **Checkpoint 14's Reflex result strengthens, rather than replaces, this direction.** Reflex Consolidation 1.0 is a bounded historical PASS whose doctrine explicitly favors capability-class repair, unseen transfer and regression over memorized aliases. The present Search failures should become new reflex/evaluation inputs, not be used to retroactively invalidate the older six-track Reflex milestone.

10. **No HUMAN_DECISION_BLOCKED or ENVIRONMENT_BLOCKED condition was encountered.** Sweep 01 remains `PARTIAL / CONTINUE`; P01 was not modified or displaced.

## Durable outputs

- `DORÉ-COMPLETED-WORK-REVISIT-QUEUE.md`: added `RQ-003 — Bible Search first work-node relevance / association upgrade`, classified `COMPLETED_REVISIT_CANDIDATE`, priority `HIGH / TRIGGERED` but subordinate to P01.
- No Master Work Register status change is warranted in this batch: `SEARCH = MAINTENANCE + DISCOVERY` already matches the evidence boundary.
- The temporary Bible Search failure memo remains active; its deletion tests are not satisfied.

## Durable learning retained

- Historical product/work-node completion and current product quality are separate judgments.
- A narrow PASS regression must not be inflated into universal production behavior.
- False negatives and false positives should be retained as evaluation evidence and may indicate a systemic relevance boundary problem.
- Search candidate retrieval, cognition/intent understanding, cross-version association, ranking/calibration and abstention are distinct layers that should not be conflated.
- Real-use failures in knowledge-rich domains are especially valuable learning signals because they can expose connection/retrieval limits rather than missing data.
- A repair is not autonomous learning unless diagnosis/generalization/verification is Doré-owned and transfers beyond the reported examples.

## Next bounded batch

Continue another unreconciled required Sweep-01 family. Prefer `dore-core/cloudflare/` or concrete ONE/Main/Join/WSS product history, checking completion claims against runtime/tests/production evidence. Also carry forward Checkpoint 13's pending P01 visual-brief sequencing supersession candidate and Checkpoint 14's `CW-010 — Reflex Consolidation 1.0` completed-work-ledger candidate on the next safe ledger writes.

Do not interrupt or replace P01.