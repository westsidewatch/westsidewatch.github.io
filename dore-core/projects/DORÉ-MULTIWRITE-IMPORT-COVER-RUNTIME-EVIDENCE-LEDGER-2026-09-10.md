# DORÉ MULTIWRITE IMPORT + COVER RUNTIME EVIDENCE LEDGER

Date: 2026-09-10
Status: SWEEP-01 EVIDENCE
Scope: bounded recent product-history reconciliation
P01 impact: NONE

## Evidence reviewed

- commit `b6a271bb99dca68f0c105497894cb4449f70620e` — `fix(multiwrite): make EPUB package parsing namespace-safe`;
- commit `85a22d5b72ba02d2795667942c1819f279651665` — `fix(multiwrite): restore local import controls even if module init fails`;
- commit `8951e77453588dbf4f1987c22abff219af226d2b` — `feat(dawn): resolve real covers before ONE fallback`.

## Reconciliation

1. Multiwrite local-publication intake is not merely conceptual. The current browser implementation accepts local EPUB/FB2/HTML/XHTML/PDF/DOCX/TXT/Markdown inputs, preserves a personal-library boundary, and contains a real EPUB publication adapter.
2. The EPUB adapter received a concrete namespace-safety repair: package/container/metadata/manifest/spine traversal now uses `localName`-based helpers rather than namespace-fragile CSS selectors. This is implementation evidence for broader EPUB compatibility, not proof of representative-corpus acceptance.
3. Critical import controls were deliberately given a non-module fallback so the import panel/open/close/file-picker path remains usable even if the module graph or CDN dependency fails. This is a useful resilience pattern and should be retained as a regression requirement.
4. Dawn Library cover handling now attempts a source/version cover resolver first and falls back to a ONE-style book cover; resolved cover metadata may be preserved on the personal reference. This is implementation evidence for richer catalog presentation and reference continuity, not proof that every source cover is lawful/reachable/stable.
5. These commits are repair/enrichment evidence inside an active product surface. They do not justify a `VERIFIED_COMPLETE` claim for Multiwrite ingestion, EPUB compatibility, Dawn cover resolution, or the broader Library workflow because no bounded live-browser acceptance receipt, representative-format fixture matrix, offline/CDN-failure run, or source-cover rights/reachability audit was found in this batch.

## Classification

- Multiwrite local import: `ACTIVE / MAINTENANCE` implementation progress.
- EPUB namespace-safety repair: `COMPLETED_REVISIT_CANDIDATE` as a bounded repair milestone until representative EPUB regression evidence exists.
- import-control no-module fallback: `MAINTENANCE`, retain as resilience regression behavior.
- Dawn real-cover resolver: `ACTIVE_PARALLEL / ENRICHMENT`; source/rights/reachability acceptance remains `UNKNOWN_NEEDS_EVIDENCE`.

## Smallest next proof

Run one bounded browser acceptance matrix using representative local files (at minimum namespaced EPUB + TXT/Markdown + DOCX/PDF where supported), verify import-panel controls with the module/CDN path deliberately unavailable, and persist Dawn cover results for source cover / fallback cover / unreachable cover cases with provenance and rights notes. A commit alone is not terminal product verification.

## Capability retained

A useful general lesson is now explicit: reader-critical local controls should degrade independently of optional module/CDN graphs, and publication parsers should prefer namespace-robust structural traversal over format-fragile selector assumptions.

No P01 state, subtitle execution, audio/transcription dependency, deployment, or blocker condition was modified.