# DORÉ DAWN LIBRARY AUTONOMOUS STOREFRONT — EVIDENCE LEDGER

Date: 2026-09-10
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Classification: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`

## Bounded evidence reviewed

- commit `a1eee5c45a436bbb475d7baec08c0e75b49a5c32` — `feat(multiwrite): launch real Dawn Library storefront`;
- commit `d3b3566bb54544e2c1aa026c4ed5e08ebc58f3e9` — persisted autonomous bookstore-growth reports;
- commits `b317fb245cb89f2ac9e028f78e80a1762ad939ab`, `918fb28210708ecfa5741bdbce674a47291cb6e5`, `6cad3eefe44673e50fc3dc2d928da89f86badc46` — verified-Chinese-catalog storefront/export correction and later persisted growth state;
- current Master Work Register Library/ingestion rows.

## What is actually implemented

1. The writing surface now has a distinct `黎明書局` / Dawn Library real-storefront section, separated from the narrower curated `聖經世界` layer. The storefront is described in code as mapping mature public catalogs, allowing browse/read/connect-to-writing behavior while not pre-downloading full text.
2. The autonomous catalog loop is no longer only a plan. Persisted reports show Project Gutenberg discovery, relevance gating, edition/rights resolution, promotion, catalog growth, storefront mapping and provenance-bearing source records.
3. At the earlier reviewed persistence point, the English-side catalog report recorded 29 published books, 28 verified and 1 pending; 19 titles were attributed to autonomous growth that day. The same run discovered 50 additional English candidates and promoted one newly verified title (`Outline Studies in the Old Testament for Bible Teachers`).
4. The storefront report recorded 127 mapped books and 15 source covers while preserving `contentDownloaded: false`; the catalog item inspected retained provider URL, explicit public-domain status, rights jurisdiction/declarer/evidence URL, and discovery/verification/catalog timestamps.
5. The Chinese branch has now materially advanced beyond the Checkpoint-50 snapshot. Commit `6cad3eef...` persists 202 Chinese candidates, 19 relevance-qualified, and resolver results of `verified: 5`, `needs-review: 4`, `blocked: 10`. This disproves the earlier `verified: 0` snapshot as current truth, but still does not justify broad Chinese or bilingual maturity.
6. Commit `b317fb2...` corrects the storefront architecture so Chinese books are sourced from the already rights-verified local Chinese catalog, then given WS Export publication URLs on demand. Commit `918fb28...` correspondingly reclassifies WS Export from a presumed Chinese OPDS catalog to an on-demand EPUB/PDF publication service. This is a substantive provenance/rights correction, not merely presentation work.

## Evidence boundary

These commits and persisted reports prove a real implemented catalog-growth/storefront foundation and a first bounded verified Chinese resolver state. They do **not** by themselves prove:

- successful production deployment/readback of every storefront interaction;
- stable quality of autonomous relevance across a representative long-run corpus;
- representative Chinese coverage or reliable verification beyond the current bounded set;
- dedupe/identity behavior across all providers under repeated runs;
- reader usefulness, accessibility, mobile quality or cross-product Library ingestion;
- full-text preservation/availability beyond remote provider routes;
- that WS Export itself is a rights authority; rights must continue to derive from the verified source edition/provenance.

A commit is implementation evidence, not production verification.

## Current judgment

- Dawn Library real storefront: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- English autonomous discovery→relevance→rights-resolution→promotion loop: `ACTIVE_PARALLEL / BOUNDED_PASS_EVIDENCE`.
- Chinese autonomous catalog path: `ACTIVE_PARALLEL / BOUNDED_PASS_EVIDENCE` for first verified resolver output (`5` verified); broader Chinese catalog quality remains evidence-gated.
- WS Export integration: `MAINTENANCE / CORRECTED_BOUNDARY` — use only as an on-demand publication/export service downstream of already verified Chinese Wikisource editions.
- Existing `LIBRARY-INGEST` remains separate: a public-catalog storefront does not prove the D1-backed authenticated Liming ingestion/readback cycle required by that row.

## Durable lessons

- Discovery is not relevance; relevance is not verification; verification is not curation. The implementation correctly persists these as separate stages.
- Public-domain remote catalogs can expand reader choice without copying all full text into Westside storage, provided rights/provenance and source identity remain explicit.
- `黎明書局` should be treated as a broader bookstore/catalog surface, while `聖經世界` is a curated subset rather than a synonym for the entire store.
- Autonomous growth claims should be split by language/provider and verified stage; English success must not mask Chinese verification debt.
- Publication/export tooling is not a rights authority. A generated EPUB/PDF route must inherit authority from a separately verified source edition and its provenance record.

## Revisit / next proof

1. Persist one production storefront readback covering browse → source/read route → connect-to-writing behavior.
2. Run a bounded repeated-loop regression proving stable source identity/dedupe and no re-promotion of the same work across providers.
3. Expand the Chinese resolver proof from the first five verified titles to a representative bounded sample with explicit rights/source evidence and false-positive review.
4. Keep the existing authenticated `LIBRARY-INGEST` proof requirement separate unless the two pipelines are intentionally converged and verified.

P01 subtitle state/action was not modified by this reconciliation.
