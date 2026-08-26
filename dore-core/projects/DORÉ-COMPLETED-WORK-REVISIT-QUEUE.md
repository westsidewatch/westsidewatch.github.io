# DORÉ COMPLETED WORK REVISIT QUEUE

Status: ACTIVE / SWEEP-01 OUTPUT
Established: 2026-08-25
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

This queue is only for work that was legitimately completed for its original milestone but may deserve a later pass. Revisit priority is evidence-based and must not displace the active P01 subtitle critical path without a stronger reason.

## RQ-001 — Sensory-loop broader robustness evaluation

**Source completed milestone:** `CW-001 — Sensory-loop consolidation / D1 reconciliation milestone`

**Current priority:** LOW / WATCHLIST

**Why it may deserve revisit**
The repair milestone is verified on deployed evidence, including consolidated state, deduplication, schema reconciliation, heartbeat success and Actions probing. However, current visible evidence is narrow and does not yet demonstrate heterogeneous signal classes, sustained volume, duplicate/error rates, or long-horizon learning quality.

**Do not reopen now because**
The original repair objective has been met and there is no present production failure. P01 and other active mission-critical work have higher leverage.

**Revisit trigger**
Raise priority if any of the following occurs:
- duplicate or dropped sensory signals reappear;
- a schema migration changes signal/brain-node reconciliation;
- Doré begins ingesting materially new classes of sensory signal;
- enough real traffic exists to support a meaningful volume/quality benchmark;
- a regression or learning-quality benchmark can be added at low marginal cost.

**Desired future evaluation**
Measure heterogeneous-signal success, deduplication accuracy, failed-claim/retry behavior, long-horizon persistence, false consolidation risk and sampled research-answer quality.

**Current disposition:** keep closed; watch for trigger.

## RQ-002 — Biblical World foundation scholarly refinement

**Source completed milestone:** `CW-002 — Biblical World foundation graduation`

**Current priority:** LOW / WATCHLIST

**Why it may deserve revisit**
The original BW-1 through BW-6 foundation milestone is explicitly PASS and includes blind evidence-boundary checks, but the graduation report itself correctly warns that later historical/textual/theological research education may refine scholarly reconstructions. As Doré acquires stronger source criticism, archaeological/geographic evidence and cross-witness reasoning, some contextual registries may become visibly too coarse.

**Do not reopen now because**
There is no evidence in the reviewed batch of a current systematic failure, and reopening a completed foundation without a concrete downstream weakness would distract from the P01 critical path and higher-priority active implementation work.

**Revisit trigger**
Raise priority when one of the following occurs:
- a materially richer historical/geographical source corpus is ingested;
- ONE/Search/Library repeatedly exposes the same contextual weakness;
- a disputed chronology/location case fails a newer Researcher benchmark;
- a new evidence model makes a current registry incapable of representing material scholarly disagreement.

**Desired future evaluation**
Sample high-impact/disputed biblical-world entries against stronger primary/secondary evidence, measure uncertainty/provenance quality and update only the affected registries rather than reopening the entire foundation by default.

**Current disposition:** keep the foundation milestone closed; refine selectively when evidence triggers it.

## RQ-003 — Bible Search first work-node relevance / association upgrade

**Source completed milestone:** `dore-core/knowledge/BIBLE-SEARCH-WORK-NODE.md` — the first earned external Scripture-search service boundary.

**Current classification:** `COMPLETED_REVISIT_CANDIDATE` for the original v0.1 work-node milestone; the live `SEARCH` workstream remains `MAINTENANCE + DISCOVERY`.

**Current priority:** HIGH / TRIGGERED, but subordinate to the active P01 critical path.

**Why the revisit trigger has fired**
Real-use evidence now contains both directions of retrieval failure: a relevant biblical concept/version variant (`Tablets of the Testimony`) did not adequately retrieve KJV-related `tables of the testimony`, while an unrelated English word combination could still produce Scripture results. The existing negative-relevance regression proves only a bounded fixture set (`Mortal Shell II`, `Grand Theft Auto`) and does not establish universal production precision or cross-version semantic recall. The Search cognition gate also remains `TAUGHT`, not `CONCEPT_PASS` or `PRODUCT_PASS`.

**What remains valid from the original milestone**
The service-boundary decision is still sound: canonical references/witness/provenance remain part of the result contract; fuzzy retrieval is candidate retrieval rather than certainty; consumers should call Doré rather than duplicate Scripture intelligence locally where practical. The node should be extended, not discarded.

**Desired revisit evaluation**
Doré should independently diagnose whether the paired false-negative/false-positive signals arise from one or several systemic layers, then run unseen evaluation across exact text, cross-version lexical variation, concept/entity association, multilingual retrieval, spelling/noise, ranking, truly unrelated strings and explicit abstention. Existing successful reference/fuzzy behavior must remain protected. A one-off `tablets = tables` patch is not sufficient unless evidence proves the case isolated.

**Self-repair evidence requirement**
The revisit is not complete merely when the two reported examples pass. Doré must persist its own diagnosis, scope judgment, repair rationale, regression results and durable learning, and later demonstrate that a similar real-use failure can be detected and routed into reflection without another external human prompt.

**Current disposition:** trigger a systemic Search-quality revisit when dependency-safe; preserve P01 as the active critical path and keep the temporary external failure memo until its deletion tests are independently satisfied.