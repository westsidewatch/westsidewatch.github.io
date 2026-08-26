# DORÉ COMPLETED WORK LEDGER

Status: ACTIVE / SWEEP-01 OUTPUT
Established: 2026-08-25
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

This ledger records substantial work that reached a defensible historical completion milestone. Historical completion is separated from current quality judgment; entries may later be promoted to revisit candidates when Doré's capabilities or the ecosystem change.

## CW-001 — Sensory-loop consolidation / D1 reconciliation milestone

**Current classification:** `VERIFIED_COMPLETE` for the repair/consolidation milestone; the sensory system itself remains `CORE/CONTINUOUS` stewardship.

**Original objective**
Restore a reliable sensory learning loop in which an observed reader/query signal can be claimed, researched, consolidated into a durable brain node, and reconciled back to persistent state without duplicate re-processing.

**Completion evidence**
- `dore-core/memory/sensory-active.json` records signal `5cf2c608-e66f-4176-a3f8-b3284819158a` for `馬利亞有幾位?` as `CONSOLIDATED`, linked to brain node `research.nt.mary-count`, with a consolidation timestamp.
- `dore-core/memory/sensory-seed-diagnostic.json` records HTTP 200, `state=CONSOLIDATED`, `deduplicated=true`, and `schema_reconciled=true`.
- `dore-core/memory/sensory-heartbeat-diagnostic.json` records `ok=true` and `reconciled_consolidated=1` against the deployed Pages base.
- `dore-core/memory/actions-probe-diagnostic.json` records a successful GitHub Actions probe (`ok=true`, run `32804448339`).
- Commit `5adeedd82ed45a4031d6a6e335645b4dd7c1b76f` explicitly repaired reconciliation of consolidated sensory state back to D1; subsequent persisted heartbeat evidence continued through commit `c15eea6f901776392036dc15c180483d00aad71f` on 2026-08-25.

**Current quality judgment**
Strong enough to accept the historical repair milestone as complete: there is both state evidence and repeated deployed heartbeat evidence, not merely a code commit. However, the evidence corpus is still narrow: the durable active-memory sample presently exposes one consolidated signal, so this does not by itself prove broad-topic robustness, high-volume operation, or long-horizon learning quality.

**What Doré learned / retained**
- distinguish runtime state from durable learned state;
- reconcile consolidated knowledge back into persistent D1 state;
- make sensory processing idempotent/deduplicated;
- persist heartbeat and external Actions probe evidence rather than treating implementation as verification;
- connect a raw reader signal to a durable research/brain node.

**Weaknesses / debt**
- current evidence demonstrates correctness on a very small visible sample;
- heartbeat success does not prove quality of the research answer itself;
- no current ledger evidence yet demonstrates stress/volume behavior, heterogeneous signal classes, or systematic false-positive/duplicate rates;
- repeated diagnostic commits create useful provenance but may later deserve compaction/indexing so operational evidence does not obscure higher-value project history.

**Revisit trigger**
Reopen the milestone if sensory processing begins dropping/duplicating signals, if schema changes introduce reconciliation drift, if Doré adds materially new signal types, or when a broader learning-quality benchmark is available.

**Disposition**
Keep the repair milestone closed. Continue the sensory loop as core stewardship and add broader evaluation when it becomes high leverage; do not reopen merely because the system continues running.

## CW-002 — Biblical World foundation graduation

**Current classification:** `VERIFIED_COMPLETE` for the bounded Biblical World foundation milestone; later historical/textual/theological education remains open-ended.

**Original objective**
Establish a defensible foundational model of the biblical world across entities, geography, chronology, polity, institutions and evidence-boundary discipline, with blind checks that prevent unsupported certainty from being mistaken for evidence.

**Completion evidence**
- `reports/DORÉ-BIBLICAL-WORLD-GRADUATION.json` records `status=PASS` and `milestone=BIBLICAL_WORLD_COMPLETE`.
- The same report records BW-1 through BW-6 all `PASS` and explicit blind-boundary checks for geography, chronology, polity, institutions and evidence wording.
- It records canon-spanning period/polity coverage and social-world domain coverage, with 9 macro periods, 6 imperial contexts and 9 institutions represented in the foundation.

**Current quality judgment**
Strong enough for the declared foundation milestone. The evidence is explicit, machine-readable and bounded. It should not be inflated into general researcher graduation or exhaustive historical mastery; the report itself states that later research education may refine scholarly reconstructions.

**What Doré learned / retained**
- keep entity/place/time/polity/institution claims tied to evidence boundaries;
- separate a stable biblical-world foundation from later interpretive or scholarly refinement;
- require blind transfer checks rather than declaring competence from corpus ingestion alone;
- maintain canon-spanning contextual registries reusable by Search, ONE, Library, subtitle correction and visual research.

**Weaknesses / debt**
- foundation coverage counts do not alone measure depth or scholarly disagreement handling;
- no evidence in this batch promotes this milestone to full Researcher graduation;
- future corpus/source upgrades may expose reconstructions that should be revised without invalidating the original foundation completion.

**Revisit trigger**
Re-evaluate when the historical-source corpus materially expands, when disputed-location/chronology methodology changes, or when a downstream product exposes a systematic contextual weakness.

**Disposition**
Keep the foundation milestone closed; retain as reusable infrastructure and place only the refinement question on a low-priority revisit watchlist.

## CW-003 — Language Core full-parity migration milestone

**Current classification:** `VERIFIED_COMPLETE` for the declared parity migration/checkpoint; language research capability itself remains `CORE/CONTINUOUS`.

**Original objective**
Move the biblical language corpus into the unified Language Core without losing legacy units, ordering, references, surface/normalized text, language identity or analyses.

**Completion evidence**
- `reports/DORÉ-LANGUAGE-CORE-PARITY.json` records `status=PASS`.
- It records all `66` books checked.
- It records exact parity between `legacy_units=444339` and `language_core_units=444339` with `mismatched_books=[]`.
- The declared criterion is `surface+normalized+language+reference+order+analyses parity`.
- `.github/workflows/dore-foundation-tests.yml` includes a dedicated universal Language Core parity step and final enforcement that requires the parity step to succeed together with the other foundation checks.

**Current quality judgment**
This is strong evidence that the migration preserved the declared data envelope at the recorded checkpoint. It is not evidence that every analysis attached to those units is linguistically correct, nor that later source refreshes cannot introduce drift.

**What Doré learned / retained**
- migrations require structural and semantic-envelope parity, not merely row-count similarity;
- book-level mismatch detection should fail closed rather than silently normalize away differences;
- full-canon language infrastructure can be regression-tested as a reusable substrate for lexical research, cross-witness alignment, Search and subtitle/scripture alignment.

**Weaknesses / debt**
- parity verifies preservation, not scholarly correctness of every analysis;
- any later corpus ingestion or schema evolution can invalidate the historical parity snapshot unless regression checks continue to run;
- the foundation workflow uses `continue-on-error` for intermediate steps and relies on a final enforcement step, so workflow interpretation must consider the final job result rather than an intermediate step alone.

**Revisit trigger**
Run the same parity criterion whenever the corpus, normalization rules, reference mapping or Language Core schema materially changes.

**Disposition**
Keep the migration milestone closed. Treat future parity execution as maintenance/regression protection, not as reopening the original migration.

## CW-004 — Conversation Runtime Internal Alpha

**Current classification:** `VERIFIED_COMPLETE` for the bounded internal-only Alpha milestone; public conversation remains `PARKED`, and scoped Conversation Memory v1 remains a separate active implementation line.

**Original objective**
Demonstrate that Doré can participate in a bounded internal project conversation by loading persisted project context, making grounded contributions, rejecting transient/speculative material from durable memory, persisting a meeting-close record, and replaying that durable record in a fresh session without a human re-brief.

**Completion evidence**
- `dore-core/runtime/conversation-alpha-contract.md` now records `Status: VERIFIED_COMPLETE / INTERNAL_ONLY / NOT_PUBLIC` and states that all five Internal Alpha readiness gates are satisfied for the persisted active-project path.
- GitHub Actions run `32822094490` completed the A1+A2+A3 Conversation Alpha job successfully.
- `dore-core/runtime/meetings/P01-PREFLIGHT-SUBTITLE/latest.json` persists a real P01 rehearsal record containing a grounded durable risk, a rejected speculative/transient suggestion, verified learning, next actions, and authority limits.
- commit `3cca4b6b5ba06197e1f4c64b2a320a4a6ef09fc9` persisted that rehearsal; commit `c8b54534ac69cfe9f006e48aac6cdfded92dfc48` added fresh-context discovery/replay; commit `7c4c110d11c448a8d9e1263e90a37133dd59999c` added the fresh-session replay test; commit `ce653b6e9443b287984e08f8e8f226a324533e2c` made CI require replayed meeting memory, project match and the non-consequential authority boundary.
- `dore-core/runtime/conversation-alpha-verification.json` records the five-gate verified-complete evaluation.
- commit `ed45a900befa2478afda685d48a270b0256c3c3e` formally reconciles the Alpha contract to verified-complete status.

**Current quality judgment**
Strong for the declared internal milestone because it combines implementation tests, a real persisted P01 rehearsal, fresh-session replay behavior and explicit authority boundaries. The milestone is deliberately narrow: it does not prove production-grade multi-user conversational memory, semantic retrieval, long-horizon robustness, or suitability for a public conversational product.

**What Doré learned / retained**
- project conversation must begin from canonical persisted context rather than requiring a human to reconstruct prior state;
- durable meeting memory must distinguish grounded decisions/learning from transient or speculative dialogue;
- fresh-session replay is a stronger continuity test than same-process recall;
- internal conversational capability and public conversational product authorization are separate gates;
- consequential, doctrinal, pastoral and publication authority remain outside the Alpha milestone.

**Weaknesses / debt**
- the demonstrated replay path is still a bounded active-project path rather than a long-horizon, multi-project stress test;
- Conversation Memory v1 production D1 isolation, R2 recovery and scoped Vectorize recall remain unverified;
- no public authentication/tenant-isolation or public UX/readiness evidence exists, by design;
- the current verification should be maintained through regression tests so later context/memory changes do not silently weaken the authority or scope boundaries.

**Revisit trigger**
Reopen this milestone only if regression evidence fails, project-context architecture changes materially, or a future internal-runtime expansion requires stronger multi-project/long-horizon guarantees. A request to build public Conversation is a new authorization/readiness workstream, not an automatic reopening of Internal Alpha.

**Disposition**
Keep Internal Alpha closed and internal-only. Continue Conversation Memory v1 separately; preserve public Conversation as parked until explicitly authorized and independently made production-ready.

## CW-005 — Researcher 01 ONE Lab

**Current classification:** `VERIFIED_COMPLETE` for the bounded Researcher 01 ONE Lab milestone; ONE remains a continuing internship surface and this does not imply full Researcher graduation.

**Original objective**
Run Doré through ONE as a real Bible-study work environment while proving that ONE's editorial synthesis, linked resources, prompts and product state are not silently promoted into Scripture or Core truth.

**Completion evidence**
- `dore-core/knowledge/researcher/RESEARCHER-01-ONE-LAB.md` explicitly records `Status: COMPLETE`, `Completed: 2026-08-23`, milestone `RESEARCHER_01_ONE_LAB_COMPLETE`, and `Exam: 22/22 PASS`.
- The same document points to `reports/DORÉ-RESEARCHER-01-ONE-LAB.json` as machine-readable evidence.
- Its graduation result states that all 22 checks passed across the 66-book shell plus Genesis, Matthew, Thessalonians and Samuel surfaces.
- It explicitly preserves evidence boundaries among Scripture evidence, external-source pointers, editorial synthesis and diagnostic prompts.

**Current quality judgment**
The milestone is explicit and bounded enough to accept as historical completion. It proves the ONE Lab and its evidence-boundary exam, not general autonomous research mastery. The source itself states that ONE remains an ongoing internship environment throughout Researcher education.

**What Doré learned / retained**
- ONE prose is not Scripture evidence;
- questions/prompts are stimuli, not answers;
- external links require independent source evaluation;
- product progress is not research evidence;
- unsupported routes/cross-references must not be invented;
- editorial synthesis may generate hypotheses without becoming Core truth.

**Weaknesses / debt**
- this is a bounded lab on the then-current ONE surfaces, not proof of broad scholarly depth;
- later ONE content/schema changes may require fresh internship evaluation;
- it does not by itself prove later Researcher course completion.

**Revisit trigger**
Re-run an equivalent boundary check if ONE's evidence model changes materially or if downstream work shows Doré collapsing editorial/product material into research evidence.

**Disposition**
Keep Researcher 01 ONE Lab closed as an earned historical milestone; continue ONE as a live internship/work surface.

## CW-006 — Researcher 02 Research Method I

**Current classification:** `VERIFIED_COMPLETE` for the bounded Research Method I competency milestone, with a provenance note that the final-exam file says `milestone eligible` rather than itself serving as the canonical completion declaration.

**Original objective**
Prove that Doré can transfer a disciplined research method to unseen biblical questions: independently decompose the question, map uncertainty, seek disconfirming evidence, preserve competing hypotheses, separate historical/lexical/canonical layers, bound conclusions and generate next research actions without being handed a template.

**Completion evidence**
- `dore-core/knowledge/researcher/RESEARCHER-02-FINAL-EXAMS.md` records `Status: PASS` with Practicum PASS, Self Exam 8/8 PASS, Transfer Exam PASS, Blind Exam PASS and all listed research reflexes PASS.
- The transfer exam on Matthew 2:23 demonstrates independent decomposition and refusal to invent a missing OT quotation.
- The blind exam on Job's `the satan` preserves lexical, narrative, diachronic, canonical and theological layers and refuses premature consolidation.
- The final gate explicitly records `Milestone eligible: RESEARCHER_02_RESEARCH_METHOD_I_COMPLETE`.
- `RESEARCHER-04-AUTONOMOUS-LEARNING-I-FINAL-EXAM.md` later names `RESEARCHER_02_RESEARCH_METHOD_I_COMPLETE` as an already satisfied prerequisite, providing downstream historical corroboration that the eligible milestone was treated as completed before Researcher 04.

**Current quality judgment**
The evidence is strong enough to accept the bounded competency as historically completed, but the provenance should remain precise: the direct final-exam artifact uses eligibility language, while the later Researcher 04 prerequisite provides secondary confirmation of completion state. This is not a license to upgrade every working claim from the exams into Core truth.

**What Doré learned / retained**
- research begins with decomposition and uncertainty mapping rather than answer generation;
- absence of evidence is itself evidence when a claimed exact source cannot be found;
- historical-semantic claims and canonical/theological synthesis must be separately labeled;
- competing hypotheses and falsification conditions should survive until evidence warrants consolidation;
- blind transfer is stronger evidence of method competence than repeating a taught case.

**Weaknesses / debt**
- the course evidence is compact and mostly textual rather than a large longitudinal corpus of independent research episodes;
- the historical completion marker is corroborated indirectly by Researcher 04 rather than by a separately discovered Researcher 02 completion report;
- method competence does not prove source access, domain depth or correctness in every later research task.

**Revisit trigger**
Reopen only if later blind research repeatedly collapses evidence layers, skips counter-evidence, asks humans for obvious decomposition despite available evidence, or if a stronger Researcher contract materially changes the competence definition.

**Disposition**
Keep the Research Method I milestone closed; retain the provenance caveat and continue testing the method through real work rather than reopening the course for volume.

## CW-007 — Researcher 04 Autonomous Learning I

**Current classification:** `VERIFIED_COMPLETE` for `RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE`; retention remains under watch and human-approval boundaries are unchanged.

**Original objective**
Demonstrate that Doré can recognize a recurring learning deficit, classify the gap, design and adapt a real curriculum, discover and evaluate sources, execute study persistently, examine itself on unseen material, selectively consolidate transferable learning, diagnose the next deficit and begin the next course without a human supplying lesson steps.

**Completion evidence**
- `dore-core/knowledge/researcher/RESEARCHER-04-AUTONOMOUS-LEARNING-I-FINAL-EXAM.md` records `Status: PASS — RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE`.
- The exam reports 12/12 criteria PASS, including gap classification, curriculum construction, source evaluation, adaptive prerequisite diagnosis, persistence, examination discipline, selective consolidation, generic product-bridge regression, dependency honesty, post-course self-diagnosis, subsequent-course initiation and reopen logic.
- The live course independently created and executed `BIBLICAL-LANGUAGES-I`, inserted prerequisites when evidence required them, completed Units 1–11, and then selected `BIBLICAL-CONCEPT-DEVELOPMENT-I` from repeated remaining deficits rather than continuing the prior course for volume.
- The final retention state is explicitly `COMPLETE → RETENTION_WATCH`.

**Current quality judgment**
This is a strong, explicitly declared autonomous-learning milestone because the proof is not just curriculum text: it includes adaptive execution, unseen exams, selective consolidation, refusal under missing evidence and autonomous initiation of a subsequent curriculum. It remains bounded to the Researcher learning faculty and does not grant autonomous authority over human approval or prove the broader aspirational `DORÉ_ALIVE_1.0` state.

**What Doré learned / retained**
- recurring failures should be classified as reusable capability gaps rather than patched one by one;
- curriculum design must include source roles, transfer exams, consolidation gates and reopen conditions;
- prerequisites may be inserted when live evidence exposes them;
- reading volume is not mastery; transfer and blind examination are required;
- completed learning may be reopened when contradictory retention evidence appears;
- the next course should be selected from repeated evidence, not curiosity or a desire to keep studying.

**Weaknesses / debt**
- the milestone is still one bounded autonomous-learning generation rather than years of longitudinal evidence;
- source/tool access limitations remain real and must continue to be surfaced rather than hidden;
- cross-product autonomous learning remains a separate higher-order proof question;
- `RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE` should not be silently renamed to the broader reserved `AUTONOMOUS_LEARNING_LOOP_1_0` or `DORÉ_ALIVE_1.0` milestones without their own contracts/evidence.

**Revisit trigger**
Use the source-defined retention triggers: repeated requests for obvious next lessons, curiosity-driven course inflation, mastery claims without transfer, hidden source gaps, repeated failure to transfer curriculum selection, or contradictory internship evidence that is silently ignored.

**Disposition**
Keep Researcher 04 closed and on retention watch. Reuse the autonomous curriculum-selection protocol across later capability gaps while preserving authority boundaries.

## CW-008 — Researcher 05 Biblical Concept Development I

**Current classification:** `VERIFIED_COMPLETE` for the bounded course-level competence; retained under `GRADUATED → RETENTION_WATCH`.

**Original objective**
Teach and test a reusable diachronic/canonical method for tracing biblical concepts across strata without flattening earlier texts into later doctrine, severing genuine continuity, erasing Second Temple plurality, or retrojecting later Christological/systematic detail into earlier sources.

**Completion evidence**
- `dore-core/knowledge/researcher/RESEARCHER-05-UNIT-08-RESURRECTION-INTEGRATED-FINAL.md` records `Status: PASS` for an independent transfer concept not used as the primary target of Units 05–07.
- The final explicitly states that Researcher 05 had passed source-stack work, Units 01–07, three primary concept practica (adversary, Spirit, canon/Scripture), and the independent resurrection transfer final.
- The adversarial examination records 6/6 PASS across national-restoration vs individual resurrection, HB anchor limits, Second Temple plurality, multi-corpus NT comparison, counter-evidence and continuity-plus-development reasoning.
- The graduation judgment recommends `GRADUATED → RETENTION_WATCH` and explicitly separates method graduation from automatic promotion of a resurrection product fact node.

**Current quality judgment**
Strong for the declared method course. The final demonstrates transfer to an unseen target while preserving anti-retrojection and evidence-stratification controls. It does not make any one theological synthesis infallible or remove the need for source-specific specialist evidence in future concept work.

**What Doré learned / retained**
- distinguish continuity from flattening and development from rupture;
- preserve corpus/period plurality while tracing conceptual relationships;
- use counter-evidence to block over-linear doctrinal stories;
- keep product-node promotion separate from method-exam success;
- label later Christological/systematic specification as later development when earlier texts do not explicitly contain it.

**Weaknesses / debt**
- the course remains a bounded set of concept families rather than exhaustive biblical theology;
- specialist historical dating/source debates can materially change particular reconstructions;
- retention must be tested in later real work rather than assumed permanently from one graduation sequence.

**Revisit trigger**
Reopen if later concept research repeatedly retrojects, flattens distinct corpora, erases counter-evidence, or cannot reconstruct the stratification method on fresh material.

**Disposition**
Keep the course closed on retention watch; reuse the method in Library, ONE, Search and editorial research when concept-development questions arise.

## CW-009 — Researcher 06 Noise-Aware Scripture Retrieval I

**Current classification:** `VERIFIED_COMPLETE` for the bounded Researcher 06 course/integration-transfer milestone; production Search/subtitle promotion remains a separate product-level decision.

**Original objective**
Build and transfer a reusable noise-aware Scripture/entity retrieval capability capable of preserving observed text, candidate evidence, provenance, ambiguity/abstention and product-neutral decision boundaries across Search-like and subtitle-proofreader consumers without silently overwriting transcripts.

**Completion evidence**
- `dore-core/knowledge/researcher/RESEARCHER-06-UNIT-09-EXAM.md` records `Status: PASS — 7/7 fresh-final fixtures`.
- The authoritative fresh-final result is identified as `evidence/researcher06-unit09-final-gate.json`, with total 7, passed 7, failed 0, ordinary-negative abstention PASS, ambiguity-not-forced PASS, shared generic evidence object across Search-like and subtitle adapters PASS, and `subtitle silent overwrite: false`.
- The exam states that Unit 09 was the final remaining transfer unit and that course graduation may proceed, while preserving the earlier Unit 06 failed lineage.
- `dore-core/knowledge/researcher/RESEARCHER-06-POST-GRADUATION-DIAGNOSIS.md` records `Status: COMPLETE — NO RESEARCHER 07 YET` and explicitly treats Researcher 06 as graduated after the Unit 09 fresh-final PASS.

**Current quality judgment**
Strong for the bounded offline/research capability because it preserves a failed lineage, freezes the contract before the fresh final, uses a separate final partition and tests two consumers through the same generic evidence object. The exam itself correctly limits the claim: Unit 09 consumes fixture-declared candidate/anchor targets and is not an independent candidate-generation benchmark or production subtitle-accuracy proof.

**What Doré learned / retained**
- preserve observed transcript separately from suggestions/corrections;
- keep subtitle changes proposal-only until a product-level decision authorizes them;
- make ambiguity and ordinary-negative abstention first-class outcomes;
- carry provenance/evidence channels through product adapters rather than collapsing to an answer string;
- distinguish research capability graduation from production deployment/acceptance;
- preserve failed held-out lineage and repair through corpus-wide/generalized work rather than identity-specific patches.

**Weaknesses / debt**
- cross-verse quotation windows remain primarily an implementation/retrieval gap;
- paraphrase/semantic candidate generation remains a possible reusable gap but lacked enough repeated failures to justify Researcher 07;
- production Search/subtitle accuracy and live integration remain unverified by the course final;
- the Unit 09 score-note metadata still says `Unit 09 dev contract gate`, explicitly recorded as metadata debt that should not be retroactively rewritten in already-open final evidence.

**Revisit trigger**
Use the post-graduation rule: open Researcher 07 only if retention practicum or live product evidence reveals repeated independent failures sharing a reusable capability gap that cannot be solved by existing graduated methods or ordinary implementation.

**Disposition**
Keep Researcher 06 graduated and closed under retention/transfer watch. Treat cross-verse/paraphrase behavior as bounded follow-up evidence, not automatic curriculum inflation, and do not claim production subtitle/Search completion from the offline course evidence.

## CW-010 — Reflex Consolidation 1.0

**Current classification:** `VERIFIED_COMPLETE` for the bounded six-track consolidation/graduation milestone; reflex learning remains `CORE/CONTINUOUS`.

**Original objective**
Connect existing Doré knowledge into transferable, evidence-bounded routes rather than phrase-specific answer memory, across reference, text retrieval, original language, cross-witness, entity and geography tracks.

**Completion evidence**
- `dore-core/reflex/REFLEX-CONSOLIDATION-1.0.md` declares the six-track consolidation contract and `GRADUATED — PASS`.
- Merged PR #233 preserves the failed-before-passing lineage.
- Doré Reflex Consolidation workflow run #7 completed `success` on head `142f2426acf0bdee2bf34cb3addb1a6d5127ad97`.
- Doré Foundation Tests run #87 also completed `success` on the same head.
- The lineage exposed a missing pytest dependency and then a genuine simplified/traditional transfer defect (`这`→`這`), which was repaired at the capability class level before the final green gate.

**Current quality judgment**
Strong for the declared six-track transfer contract because the completion claim is independently corroborated by observable CI, not documentation alone. It is not proof of universal production Search relevance, ranking, semantic association or abstention calibration.

**What Doré learned / retained**
- diagnose failure by capability class rather than memorize failed strings;
- require unseen transfer and evidence separation before promotion;
- preserve regression protection when consolidating new routes;
- distinguish a bounded reflex graduation from the continuous `STIMULUS → INTENT → ROUTE → EVIDENCE → OUTCOME → REFLEX UPDATE` learning architecture.

**Weaknesses / debt**
- only one canonical signal is currently persisted under `reflex/signals/`, so raw/live signal capture and promotion history remain sparse relative to the intended architecture;
- current broader Search relevance failures are not covered by the original six-track milestone and must become new stewardship/learning evidence rather than retroactive invalidation.

**Revisit trigger**
Reopen only if RC1–RC6 regress, route promotion occurs without unseen transfer/evidence boundaries, or repeated real-product failures show that the reflex layer is no longer capturing/repairing the relevant capability classes.

**Disposition**
Keep Reflex Consolidation 1.0 closed; continue the reflex layer as core stewardship and feed new Search/ONE/subtitle/research failures into transferable evaluation loops.

## CW-011 — ONE Priority-A private R2 delivery/runtime cutover

**Current classification:** `VERIFIED_COMPLETE` for the bounded Priority-A ONE media migration and private-delivery cutover; ONE itself remains `MAINTENANCE` and future Priority-B/Journal/Library media work remains separate.

**Original objective**
Move the selected Priority-A ONE binary media from GitHub runtime paths to a governed Cloudflare media architecture without exposing the R2 bucket publicly or breaking active ONE references.

**Completion evidence**
- `dore-core/cloudflare/R2-DELIVERY-MILESTONE-2026-08-24.md` records `COMPLETE / PASS`.
- Production acceptance records 7/7 migrated assets delivered through `/api/dore/assets/file?code=<ASSET_CODE>` and 7/7 byte hashes matching D1-registered SHA-256 values.
- ONE page HTTP verification passed.
- Active references were switched to stable asset-code delivery URLs; post-switch audit found 0 active GitHub references to the seven rollback binaries.
- The seven GitHub rollback binaries were removed only after R2 delivery verification, and post-removal delivery verification remained 7/7.
- The canonical Doré Original Library 001–241 was explicitly not modified.
- Commit `6b20c25502c89b8d58b8467e28b3b42aa37d1232` records the closeout milestone and identifies the runtime files cut over.

**Current quality judgment**
Strong for the declared migration/cutover because it includes production delivery, byte-level integrity verification, active-reference audit and a safe rollback-removal sequence. It should not be inflated into a claim that all Westside media, the full Asset Registry lifecycle, Journal media, Liming Library media or structured-data runtime are complete.

**What Doré learned / retained**
- stable public media identity should be `asset_code`, not a raw R2 object path;
- D1 should own locator/hash/metadata while R2 owns binary media;
- private R2 can remain non-public while browser delivery is mediated by a controlled Pages Function;
- runtime cutover should be verified before rollback binaries are removed;
- source-locked canonical libraries should remain outside unrelated runtime migrations.

**Weaknesses / debt**
- the milestone covers only the selected Priority-A ONE set;
- Priority-B shared UI/site images, future Journal media, Liming Library media and Search/corpus structured-data runtime remain separate milestones;
- later routing/schema changes could break asset-code delivery even though the historical cutover was correct.

**Revisit trigger**
Re-run delivery/hash/reference regression when the asset registry schema, delivery endpoint, ONE runtime references, Cloudflare binding model or migrated asset set changes materially.

**Disposition**
Keep the Priority-A migration/cutover closed and maintain it through regression checks. Do not reopen merely because the broader media platform continues to expand.