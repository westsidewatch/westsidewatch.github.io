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

**2026-09-09 revalidation**
The watchlist condition persists without becoming a production blocker. `sensory-active.json` still contains the same three signals in `RESEARCHING` state since 2026-08-28 with no assigned `brain_node`, while the 2026-09-09 heartbeat remains `ok: true` and the GitHub Actions probe also remains `ok: true`. This strengthens the lifecycle/provenance concern: observability is alive, but observability health is not end-to-end evidence that research signals reach an explicit terminal disposition. Preserve the historical repair milestone as complete; treat long-lived unresolved signal state as maintenance/revisit debt rather than sensory regression.

**Do not reopen now because**
The original repair objective has been met and there is no present production failure. P01 and other active mission-critical work have higher leverage.

**Revisit trigger**
Raise priority if any of the following occurs:
- duplicate or dropped sensory signals reappear;
- a schema migration changes signal/brain-node reconciliation;
- Doré begins ingesting materially new classes of sensory signal;
- enough real traffic exists to support a meaningful volume/quality benchmark;
- a regression or learning-quality benchmark can be added at low marginal cost;
- long-lived `RESEARCHING` signals continue without an explicit terminal-state policy or disposition audit.

**Desired future evaluation**
Measure heterogeneous-signal success, deduplication accuracy, failed-claim/retry behavior, long-horizon persistence, false consolidation risk and sampled research-answer quality. For the currently aged signals, persist one evidence-backed terminal disposition per signal—resumed/completed, intentionally abandoned, superseded/deduplicated, or failed with retry/escalation state—and add an age/terminal-state invariant so a fresh heartbeat cannot mask indefinitely unresolved signal work.

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

Sweep 01 has now also identified a service-boundary architecture drift. `BIBLE-SEARCH-WORK-NODE.md` explicitly says consumers should call Doré rather than duplicate Scripture intelligence locally where practical and names `dore_core.search.BibleSearchIndex` as the core implementation. The current public browser implementation in `static/dore/dore-search.js` independently reimplements book aliases, reference parsing, text normalization, fuzzy scoring and English relevance filtering. This does not invalidate the original work-node milestone, but it creates two evolving search-intelligence paths that can diverge in normalization, ranking and regression behavior.

**What remains valid from the original milestone**
The service-boundary decision is still sound: canonical references/witness/provenance remain part of the result contract; fuzzy retrieval is candidate retrieval rather than certainty; consumers should call Doré rather than duplicate Scripture intelligence locally where practical. The node should be extended, not discarded.

**Desired revisit evaluation**
Doré should independently diagnose whether the paired false-negative/false-positive signals arise from one or several systemic layers, then run unseen evaluation across exact text, cross-version lexical variation, concept/entity association, multilingual retrieval, spelling/noise, ranking, truly unrelated strings and explicit abstention. Existing successful reference/fuzzy behavior must remain protected. A one-off `tablets = tables` patch is not sufficient unless evidence proves the case isolated.

The revisit should also decide one canonical execution boundary for public Search. Preferred direction is to make browser Search consume the Doré/Core service contract, or otherwise generate both paths from one shared canonical normalization/retrieval specification with parity tests. Do not silently maintain two independent fuzzy/reference engines as if they were equivalent.

**Self-repair evidence requirement**
The revisit is not complete merely when the two reported examples pass. Doré must persist its own diagnosis, scope judgment, repair rationale, regression results and durable learning, and later demonstrate that a similar real-use failure can be detected and routed into reflection without another external human prompt.

**Current disposition:** trigger a systemic Search-quality and service-boundary convergence revisit when dependency-safe; preserve P01 as the active critical path and keep the temporary external failure memo until its deletion tests are independently satisfied.

## RQ-004 — Main homepage / Vol.00 visual-language refit

**Source completed milestones:** the August 2026 homepage rebuild around the watchful-city concept (`339679b4`), the later 5:8 / 8:5 editorial-ratio unification (`051afa76`), and subsequent live homepage Doré Search integration (`e2b7d577`).

**Current classification:** `COMPLETED_REVISIT_CANDIDATE` for the bounded homepage visual-language milestone; the live `MAIN` workstream remains maintenance and the separate `VIS-GRAMMAR` workstream is now `ACTIVE_PARALLEL / BUILDING`.

**Current priority:** MEDIUM / TRIGGERED, subordinate to P01 and to completing the visual-grammar evidence base.

**Why the revisit trigger has fired**
The original rebuild successfully established a coherent watchful-city identity using Watch Night, First Light Gold, a Jerusalem wall / Golden Gate treatment, temple-stone texture, bilingual Scripture and later an explicit 5:8 / 8:5 publication-ratio system. Current repository state still carries those decisions and now embeds direct Doré Search in the homepage. At the same time, the canonical plan explicitly says Brand V1 must wait for a proven visual grammar and records `VIS-GRAMMAR` as `ACTIVE_PARALLEL / BUILDING`, not complete. Therefore the August homepage treatment should be preserved as a legitimate historical completion but not mistaken for the final ecosystem-wide visual system.

**What remains valid from the original milestone**
The homepage learned several durable brand primitives: watch/night/dawn sequencing; city-wall / gate symbolism; temple-stone materiality; bilingual Scripture; the 5:8 portrait and 8:5 landscape publication ratios; and the principle that product utility such as Doré Search can live inside the brand center rather than as a disconnected tool.

**Weaknesses / debt**
The ratio system and framed editorial-card treatment were introduced before the current dedicated visual-grammar research program existed. The homepage also contains product-specific inline search styling and accumulated visual decisions from repeated repair/refinement passes. Those choices may be locally successful yet too literal, too card-dependent, or too tightly coupled to Vol.00 to serve as the final shared grammar for Main, Journal, Library, Search, ONE and Join.

**Revisit trigger**
Reopen only when `VIS-GRAMMAR` has produced evidence-backed, cross-surface rules and a prototype strong enough to compare against the live Main baseline. The comparison must preserve the successful semantic primitives above and prove an actual improvement in identity, restraint, readability, responsive behavior and cross-product transfer.

**Desired future evaluation**
Use the current production homepage as the control. Apply only the newly proven grammar to the same real content and product functions, then compare against the baseline on desktop/mobile, bilingual typography, material/texture behavior, Scripture readability, search discoverability, wall/gate/dawn symbolism and ability to generalize to other products. Do not replace the live homepage with conceptual placeholders.

**Current disposition:** keep production stable; maintain the August 2026 build as the historical baseline; revisit after visual-grammar evidence is mature enough for a real A/B implementation.

## RQ-005 — Join operational-information synchronization

**Source completed milestone:** live `/join/` ministry portal implementation plus the already-closed Priority-B site-media migration/cutover milestone.

**Current classification:** `COMPLETED_REVISIT_CANDIDATE` for operational-data governance only; the live Join surface itself remains `MAINTENANCE`.

**Current priority:** LOW / WATCHLIST, subordinate to P01 and not a standalone active project.

**Why it may deserve revisit**
The Join portal is materially implemented and useful: it connects readers to Doré Bible Search, ONE, Westside Watch, WeChat, Zoom, ministry contacts and the Church surface. Its migrated background and QR assets use the canonical site-asset endpoint. However, schedule, Zoom and contact values are hard-coded in the presentation layer. Source presence proves implementation, not freshness, authorization or synchronization with the church's governing operational truth.

**What remains valid from the completed milestone**
The lightweight portal structure, cross-product doorway role and asset-code delivery pattern remain sound. No evidence in the bounded review indicates that Join is broken or that the closed Priority-B media migration should be reopened.

**Revisit trigger**
Raise priority if church schedule/contact/Zoom information changes; a canonical church operational-data source/API/file is introduced; Join is redesigned under Brand V1; or a stale-value discrepancy appears between Join and another official surface.

**Desired future evaluation**
Keep stable editorial/brand content local to the page, but source time-sensitive ministry facts from one canonical, explicitly verified operational-data source shared with Church surfaces where practical. Verify freshness and fallback behavior without disturbing the proven asset-code delivery path.

**Current disposition:** keep production stable; watch for a governance trigger; do not interrupt P01.

## RQ-006 — Dawn Library Chinese `聖經世界` relevance / curation gate

**Source completed milestone:** first bounded implemented Chinese discovery → relevance → rights/edition-resolution → promotion path, including verified Chinese resolver output and verified-catalog storefront export.

**Current classification:** `COMPLETED_REVISIT_CANDIDATE` for the first lexical relevance-gate milestone; live `DAWN-LIBRARY` remains `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.

**Current priority:** HIGH / TRIGGERED, subordinate to P01.

**Why the revisit trigger has fired**
The 2026-09-11 autonomous bookstore run proves the Chinese path can now produce verified/published items, but it also exposes a concrete semantic false-positive class. `static/dawn-library/biblical-world/chinese-relevance-results.json` qualifies modern Israel/Palestine political texts using only `strong:以色列` and `strong:巴勒斯坦`; at least two of those texts (`巴勒斯坦、阿拉伯人民反击以色列侵略` and `巴勒斯坦游击队不断袭击以色列侵略军`) crossed the resolver/promotion boundary into the Chinese Wikisource storefront shelf. This is not a rights failure: it is a collection-relevance/curation failure.

**What remains valid from the completed milestone**
The staged architecture remains sound: discovery, relevance, rights verification, curation and publication/export should be distinct. Chinese rights verification and the WS Export boundary are real improvements. The failure is specifically that the current `聖經世界` relevance signal treats ambiguous modern geopolitical terms as unconditional strong positives.

**Revisit trigger**
Already fired. Repair becomes dependency-safe work when it can proceed without displacing P01 or another higher-priority critical path.

**Desired future evaluation**
Add explicit Chinese negative fixtures for modern state/diplomatic/war/news/political documents containing `以色列` / `巴勒斯坦`; preserve positive recall for Bible editions, biblical geography and genuinely relevant ancient/history resources; re-run discovery → relevance → resolver → promotion; audit the already promoted Chinese set and remove/reclassify semantic false positives from `聖經世界`. Rights-clean items may remain in the broader Dawn Library only when an editorially justified collection exists.

**Completion condition**
A bounded regression proves true-positive retention and false-positive rejection, followed by a persisted promotion report showing no known modern-political lexical false positives crossing into `聖經世界`.

**Current disposition:** trigger systemic Chinese collection-relevance repair; do not treat first verified Chinese promotion as bilingual maturity; preserve P01 ordering.

## RQ-007 — Product Registry coverage / canonical relationship drift

**Source completed milestone:** initial `dore.product-registry.v1` architecture foundation introduced by commit `d6a9744ffed0e045315c8e69680061b79214a1f9` and subsequently extended with the shared Scripture Workspace model.

**Current classification:** `COMPLETED_REVISIT_CANDIDATE / MAINTENANCE` for registry coverage; the underlying one-Doré/many-products architecture foundation remains a bounded `VERIFIED_COMPLETE / COMPONENT`.

**Current priority:** LOW / WATCHLIST, subordinate to P01.

**Why it may deserve revisit**
The registry successfully encodes the critical architecture rule that Doré Core owns identity, memory, knowledge, research, provenance, judgment, capability routing, permissions, learning and verification while products remain consumers/training environments. However, the canonical Master Work Register has expanded beyond the registry's explicit product list. Current durable workstreams/surfaces such as Westside Stories, Join, Conversation-memory evolution and Reflex are not all represented as machine-readable product/Core relationships. No persisted acceptance rule was found that defines which canonical workstream classes must appear in the Product Registry or checks coverage/parity automatically.

**What remains valid from the completed milestone**
The one-Doré/many-products principle, shared-Core promotion rule, ONE Canon Index boundary, protected StudyNote rule, Dawn-Library-not-a-second-brain rule, provider replaceability and human authority boundary remain strong and should not be reopened merely because the ecosystem grew.

**Do not reopen now because**
This is architecture bookkeeping/coverage debt rather than a live product failure. The Product Registry should not become a JSON duplicate of every project in the Master Work Register, and P01 remains higher priority.

**Revisit trigger**
Raise priority when a new durable product is added, a shared semantic layer is introduced, a product begins duplicating Core-owned identity/memory/retrieval/judgment, or a machine consumer needs authoritative product-to-capability topology that the current registry cannot answer.

**Desired future evaluation**
Define a scoped registry-coverage contract first: identify which Master Register classifications require Product Registry representation and which are intentionally project-only, learning-only or governance-only. Then add a small acceptance check comparing required canonical entities/relationships against `product-registry.v1.json`, including explicit exclusions, without turning the registry into a second operational roadmap.

**Current disposition:** keep the architecture foundation closed; place registry coverage on low-priority maintenance/revisit watch; no P01 impact.