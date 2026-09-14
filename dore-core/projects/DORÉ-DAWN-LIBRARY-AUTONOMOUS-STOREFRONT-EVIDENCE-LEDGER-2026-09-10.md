# DORÉ DAWN LIBRARY AUTONOMOUS STOREFRONT — EVIDENCE LEDGER

Date: 2026-09-10
Updated: 2026-09-13
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Classification: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`

## Bounded evidence reviewed

- commit `a1eee5c45a436bbb475d7baec08c0e75b49a5c32` — `feat(multiwrite): launch real Dawn Library storefront`;
- commit `d3b3566bb54544e2c1aa026c4ed5e08ebc58f3e9` — persisted autonomous bookstore-growth reports;
- commits `b317fb245cb89f2ac9e028f78e80a1762ad939ab`, `918fb28210708ecfa5741bdbce674a47291cb6e5`, `6cad3eefe44673e50fc3dc2d928da89f86badc46` — verified-Chinese-catalog storefront/export correction and later persisted growth state;
- commit `aed3b1c0d0ffb5cd9e7475559cc63c9fcbec07f5` — 2026-09-11 persisted autonomous bookstore growth;
- `static/dawn-library/biblical-world/chinese-relevance-results.json` generated `2026-09-11T13:38:58.362463+00:00`;
- current Master Work Register Library/ingestion rows;
- commits `a2aa747565fa33685134ec0417ea337b87f5ecce`, `90212ab8edd371c93df9f191e4577ea3415b745b`, `f1a2d580761272c1b02eac051eb39176be2d01a7`, `b7c7543b65772055d4b55206e702a772a978ff65` — 2026-09-14 product-surface restoration sequence.

## What is actually implemented

1. The writing surface now has a distinct `黎明書局` / Dawn Library real-storefront section, separated from the narrower curated `聖經世界` layer. The storefront is described in code as mapping mature public catalogs, allowing browse/read/connect-to-writing behavior while not pre-downloading full text.
2. The autonomous catalog loop is no longer only a plan. Persisted reports show Project Gutenberg discovery, relevance gating, edition/rights resolution, promotion, catalog growth, storefront mapping and provenance-bearing source records.
3. At the earlier reviewed persistence point, the English-side catalog report recorded 29 published books, 28 verified and 1 pending; 19 titles were attributed to autonomous growth that day. The same run discovered 50 additional English candidates and promoted one newly verified title (`Outline Studies in the Old Testament for Bible Teachers`).
4. The storefront report recorded 127 mapped books and 15 source covers while preserving `contentDownloaded: false`; the catalog item inspected retained provider URL, explicit public-domain status, rights jurisdiction/declarer/evidence URL, and discovery/verification/catalog timestamps.
5. The Chinese branch materially advanced beyond the earlier zero-verification snapshot. The 2026-09-11 persisted run records 34 published / 33 verified / 1 pending books overall, 220 mapped storefront books, 129 source covers, 21 direct publications and six Chinese Wikisource storefront books. The Chinese resolver records 19 relevance-qualified inputs with `verified: 8`, `needs-review: 1`, `blocked: 10`.
6. The first bounded verified Chinese resolver/promotion milestone therefore exists and the earlier Master Register statement that the Chinese resolver reports zero verified promotions is stale.
7. However, the same run exposes a semantic curation defect that prevents treating the Chinese path as mature. At least two promoted/verified `聖經世界` entries are contemporary Israel/Palestine political texts (`巴勒斯坦、阿拉伯人民反击以色列侵略` and `巴勒斯坦游击队不断袭击以色列侵略军`). Their relevance qualification is driven only by lexical hits `strong:以色列` + `strong:巴勒斯坦`, not by evidence that they are biblical-world books or useful Scripture/history resources. The broader relevance results show the same mechanism qualifying or deferring modern diplomatic/political material on the term `以色列`.
8. Rights verification and curation relevance are therefore correctly distinct in theory but insufficiently separated in the current Chinese promotion behavior: a public-domain/verified edition can still be the wrong item for the curated `聖經世界` collection.
9. Commit `b317fb2...` corrects the storefront architecture so Chinese books are sourced from the already rights-verified local Chinese catalog, then given WS Export publication URLs on demand. Commit `918fb28...` correspondingly reclassifies WS Export from a presumed Chinese OPDS catalog to an on-demand EPUB/PDF publication service. This remains a substantive provenance/rights correction, not merely presentation work.
10. The 2026-09-14 restoration sequence establishes a materially clearer product/runtime boundary. `static/dawn-library/product/index.html` reintroduces a reader-facing bookstore surface with searchable shelves and visible 5:8 cover projection; `product.js` joins `storefront.json`, `surfaces/dawn-storefront.json` and `canonical-index.json`, using canonical Work identity/title/author while retaining legacy/storefront cover and source metadata as presentation/provenance inputs.
11. The main `/dawn-library/` route was then switched from `formal-edition/phase4/`—an engineering/formal-acceptance surface—to `dawn-library/product/`. This is a real product-history correction: engineering acceptance UI is no longer the intended reader-facing storefront.
12. The restored product surface deliberately falls back to a generated Dawn card when no safe HTTPS cover exists, adds a canonical `DAWN` badge when the Work is found in the canonical index, and keeps source opening behind an explicit source URL. This is evidence of canonical-identity/presentation separation rather than a second identity system.
13. The restoration is implementation evidence, not yet production readback. No inspected artifact in this bounded batch proves that every restored cover loads in production, every shelf-to-canonical positional join is semantically stable under reorder, or that the main route has been independently verified across desktop/mobile/accessibility after the switch.

## Evidence boundary

These commits and persisted reports prove a real implemented catalog-growth/storefront foundation, a first bounded verified Chinese resolver/promotion state, and a restored reader-facing product surface that projects canonical Work identity with cover/source metadata. They do **not** by themselves prove:

- successful production deployment/readback of every storefront interaction and restored cover;
- stable semantic joining if storefront item order and canonical surface item order diverge;
- stable quality of autonomous relevance across a representative long-run corpus;
- representative Chinese coverage or reliable curation beyond the current bounded set;
- that lexical Israel/Palestine matches are semantically appropriate for `聖經世界`;
- dedupe/identity behavior across all providers under repeated runs;
- reader usefulness, accessibility, mobile quality or cross-product Library ingestion;
- full-text preservation/availability beyond remote provider routes;
- that WS Export itself is a rights authority; rights must continue to derive from the verified source edition/provenance.

A commit is implementation evidence, not production verification. Rights verification is not curation approval. A reader-facing mount is not equivalent to production-readback acceptance.

## Current judgment

- Dawn Library real storefront: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- Restored `/dawn-library/` product surface: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`, with the older engineering/formal-acceptance UI explicitly `SUPERSEDED` as the reader-facing mount (retained only as engineering evidence/surface where still useful).
- Canonical Work identity → storefront cover/source projection bridge: `VERIFIED_COMPLETE / COMPONENT` at implementation-contract level, but runtime/order-drift acceptance remains open.
- English autonomous discovery→relevance→rights-resolution→promotion loop: `ACTIVE_PARALLEL / BOUNDED_PASS_EVIDENCE`.
- Chinese autonomous catalog path: `ACTIVE_PARALLEL / BOUNDED_PASS_EVIDENCE` for first verified resolver/promotion output, with a **triggered relevance/curation repair requirement** before broader Chinese or bilingual maturity can be claimed.
- Chinese lexical relevance gate for `聖經世界`: `COMPLETED_REVISIT_CANDIDATE / TRIGGERED` at the first bounded implementation milestone because modern political Israel/Palestine texts can cross the promotion boundary from lexical matches alone.
- WS Export integration: `MAINTENANCE / CORRECTED_BOUNDARY` — use only as an on-demand publication/export service downstream of already verified Chinese Wikisource editions.
- Existing `LIBRARY-INGEST` remains separate: a public-catalog storefront does not prove the D1-backed authenticated Liming ingestion/readback cycle required by that row.

## Durable lessons

- Discovery is not relevance; relevance is not rights verification; rights verification is not curation. All four stages need separate evidence and separate gates.
- Biblical geography/entity terms such as `以色列` and `巴勒斯坦` are highly ambiguous across ancient/biblical and modern political corpora. They cannot function as unconditional strong-positive terms for a `聖經世界` collection.
- Public-domain status is orthogonal to mission/editorial fit. A rights-clean item can still be a semantic false positive and must not auto-promote into a curated biblical collection.
- Public-domain remote catalogs can expand reader choice without copying all full text into Westside storage, provided rights/provenance, source identity and collection relevance remain explicit.
- `黎明書局` should be treated as a broader bookstore/catalog surface, while `聖經世界` is a curated subset rather than a synonym for the entire store. Some material may be lawful for the general bookstore while inappropriate for `聖經世界`.
- Autonomous growth claims should be split by language/provider and verified stage; English success must not mask Chinese relevance/curation debt.
- Publication/export tooling is not a rights authority. A generated EPUB/PDF route must inherit authority from a separately verified source edition and its provenance record.
- Canonical identity and presentation metadata are different responsibilities. Product surfaces may project cover/source metadata around a canonical Work, but they must not create a parallel Work identity.
- Engineering acceptance surfaces must not silently become the public product merely because they are more recently implemented. Public mount truth is a product decision that needs its own evidence and rollback-safe history.

## Revisit / next proof

1. Add a Chinese collection-relevance regression set with explicit negatives for modern state/diplomatic/war/news/political texts containing `以色列` / `巴勒斯坦`, while retaining true positives for biblical geography, Bible editions and genuinely relevant ancient/history resources.
2. Re-run the bounded Chinese discovery→relevance→resolver→promotion loop and prove that rights-clean semantic false positives are blocked from `聖經世界` without harming true-positive recall.
3. Audit the already promoted Chinese set and remove/reclassify false positives from `聖經世界`; preserve them only in a broader lawful bookstore collection if there is a justified editorial reason.
4. Persist one production storefront readback covering main `/dawn-library/` mount → shelves/cover projection → search → source/read route, including desktop/mobile and cover-fallback behavior.
5. Add a regression fixture proving the canonical surface/storefront join remains correct when shelf item order changes; prefer explicit `workId` identity over positional correspondence where possible.
6. Run a bounded repeated-loop regression proving stable source identity/dedupe and no re-promotion of the same work across providers.
7. Keep the existing authenticated `LIBRARY-INGEST` proof requirement separate unless the two pipelines are intentionally converged and verified.

P01 subtitle state/action was not modified by this reconciliation.
