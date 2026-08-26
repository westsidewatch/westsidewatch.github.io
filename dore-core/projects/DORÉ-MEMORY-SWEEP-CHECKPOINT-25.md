# Doré Memory Sweep Checkpoint 25

Date: 2026-08-26
Sweep: `MEMORY-CONSOLIDATION-SWEEP-01`
Batch: Bible Search relevance evidence boundary and temporary-failure-memo reconciliation
Status: COMPLETE_FOR_BATCH

## Scope

This bounded batch inspected the live Search-quality evidence surrounding the paired real-use relevance failures recorded on 2026-08-25, and reconciled that evidence against the original Bible Search work-node contract and the already-created completed-work revisit trigger.

Primary evidence:
- `dore-core/projects/TEMP-BIBLE-SEARCH-FAILURE-SIGNALS-2026-08-25.md`
- `dore-core/knowledge/BIBLE-SEARCH-WORK-NODE.md`
- `dore-core/runtime/evidence/search-negative-relevance.json`
- commit `9b8a7a649e21c39f622ba8e29df0932056c31125` (`ci(dore): persist Search negative-relevance verification evidence`)
- commit `51e2b82422cae9a4f2f8c9f2d17cd0eb32eb938a` (`dore: add Bible Search relevance revisit trigger`)
- `dore-core/projects/DORÉ-COMPLETED-WORK-REVISIT-QUEUE.md` (`RQ-003`)
- `dore-core/projects/DORÉ-MISSING-EVIDENCE-REGISTER.md` (`ME-006`)
- `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md` (`SEARCH`)

The active P01 subtitle critical path was not modified, replaced, or interrupted.

## Classification

### Original Bible Search v0.1 work-node milestone

Classification: **historically complete for its original service-boundary objective; `COMPLETED_REVISIT_CANDIDATE` for present Search quality**.

The original work node established a real, durable boundary:
- canonical reference / witness / language / provenance in results;
- explicit reference, text, lemma, morphology and fuzzy query modes;
- fuzzy retrieval treated as candidate retrieval rather than certainty;
- consumer products should call Doré rather than fork Scripture intelligence locally where practical.

Those decisions remain valid. The current evidence does not justify superseding or retiring the work node itself.

### Live Search workstream

Classification remains **`MAINTENANCE + DISCOVERY`**.

Reason:
- the negative-relevance regression is real and persisted;
- real-use evidence nevertheless shows both a false-negative direction (`Tablets of the Testimony` not adequately reaching KJV `tables of the testimony`) and a false-positive direction (unrelated English text still capable of surfacing Scripture in observed use);
- the Search cognition gate remains recorded `TAUGHT`, not `CONCEPT_PASS` or `PRODUCT_PASS`;
- therefore neither the original work-node milestone nor the bounded negative fixture may be promoted into a broad Search-quality completion claim.

No Master Work Register status correction is required in this batch because the canonical `SEARCH` row already records the appropriate maintenance/discovery posture and explicitly protects negative-relevance regression while leaving cognition/product gates open.

## What the negative-relevance evidence actually proves

`dore-core/runtime/evidence/search-negative-relevance.json` is a legitimate bounded verification artifact.

It proves the persisted fixture set passed at `2026-08-25T08:40:20Z`:
- `Mortal Shell II` → zero Scripture results;
- `Grand Theft Auto` → zero Scripture results;
- `John 3:16` → explicit reference resolves;
- `約翰福音 3:16` → explicit reference resolves;
- `begining` → single-term fuzzy retrieval remains available.

This is useful regression evidence because it protects a specific abstention boundary while checking that obvious positive/reference behavior did not collapse.

It does **not** prove:
- general production abstention for arbitrary unrelated language;
- broad precision calibration;
- cross-version lexical equivalence;
- semantic/concept association;
- multilingual semantic stability;
- ranking quality across exact/equivalent/related candidates;
- unseen transfer;
- the self-reflection/self-repair loop required by the temporary failure memo.

The bounded PASS therefore remains valid without being inflated into a global Search PASS.

## Temporary failure memo decision

`TEMP-BIBLE-SEARCH-FAILURE-SIGNALS-2026-08-25.md` remains **TEMPORARY / ACTIVE** and must **not** be deleted yet.

Deletion is not justified because the memo's own completion tests still require evidence that is not present in this batch:
1. a Doré-owned diagnosis of the paired false-negative/false-positive signals;
2. explicit isolated-vs-systemic scope judgment with supporting evidence;
3. repair broader than a one-off phrase patch unless isolation is proved;
4. broader unseen recall + precision/abstention evaluation;
5. cross-version `tablets` → KJV `tables` evaluation;
6. durable Search/Core learning after diagnosis/repair;
7. later detection/routing of a similar failure without another external human prompt.

The correct disposition is therefore **retain as a temporary external evidence anchor until RQ-003's repair/evaluation contract is satisfied**.

## Missing-evidence reconciliation

No new top-level missing-evidence ID is necessary.

The newly inspected gap is already canonically represented by two linked durable records:
- `RQ-003` in the Completed Work Revisit Queue captures the triggered Search-quality revisit and the paired real-use failures;
- `ME-006` in the Missing Evidence Register captures the still-unproved Search cognition understanding/product gates.

This batch sharpens the boundary between them:
- `RQ-003` = **why the completed Search work node deserves a quality revisit now**;
- `ME-006` = **what broader cognition/product evidence is still missing before stronger Search claims can be credited**.

A future Search repair may close parts of both, but the two should not be collapsed prematurely.

## Superseded / retired / contradiction review

No inspected Search artifact is proved superseded or retired.

The temporary memo is not a competing design document; it is an external failure-evidence anchor with explicit deletion conditions.

No contradiction requiring Master Register mutation was found:
- original work-node completion remains historically true;
- the bounded negative regression remains truly passing for its named fixtures;
- real-use failures legitimately trigger a revisit without invalidating those earlier bounded milestones;
- Search remains open for maintenance/discovery and stronger cognition/product evidence.

## Revisit trigger quality judgment

`RQ-003` remains a **HIGH / TRIGGERED** revisit candidate, but subordinate to P01.

Reason for high value:
- Bible Search is a live public Scripture encounter surface;
- the paired failures expose both recall and precision/abstention weaknesses;
- the knowledge substrate appears richer than the observed retrieval behavior, making this a high-leverage association/relevance problem rather than a simple missing-data task;
- a systemic improvement would benefit Search consumers across Main, Join, ONE and future Library/Conversation pathways.

Reason not to interrupt P01:
- no evidence in this batch converts Search relevance into a safety-critical blocker for the current subtitle critical path;
- the Sweep governing rule explicitly forbids replacing P01 with parallel stewardship work.

## Sweep result

Batch 25 is complete.

Useful durable outcome:
- the original Search work node is preserved as a valid historical completion while its present quality is explicitly separated into a triggered revisit;
- the negative-relevance evidence is credited exactly at its bounded fixture scope and not overclaimed;
- the temporary external failure memo is explicitly retained because its self-diagnosis/generalization/deletion gates remain unsatisfied;
- `RQ-003` and `ME-006` are reconciled as complementary rather than duplicate records;
- no P01 state, runtime, deployment, or subtitle files were changed.
