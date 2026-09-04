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
