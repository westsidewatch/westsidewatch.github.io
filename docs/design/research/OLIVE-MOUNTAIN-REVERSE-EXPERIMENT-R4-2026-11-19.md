# Olive Mountain R4 — concrete source reverse experiment (2026-11-19)

Scope: source-specific investigation for P2 Olive Mountain; no production asset replacement.

## A. Walter Crane botanical source
- Source: https://freesvg.org/johnny-automatic-olive-branch-1
- Source page labels the asset as 'Line and Form by Walter Crane, 1914', SVG, ~0.07 MB, Public Domain.
- Source metadata discoverable via public web search.
- Direct download from current Python container **failed at DNS resolution**. Original SVG bytes, viewBox, paths, actual editability and rendering **not inspected**.
- Decision: candidate, not approved or installed. Next test must retrieve original SVG via permitted network runner and parse/render the file before any reuse.

## B. Codrops GSAP Flip
- Article: https://tympanus.net/codrops/2026/01/20/animating-responsive-grid-layout-transitions-with-gsap-flip/
- Published 2026-01-20 by Iqbal Muthahhary; discusses vanilla JS, CSS Grid, GSAP Flip for resizing/reordering grid items.
- The article text and demo references are discoverable via public web search, reversing the earlier R3 blanket 'Codrops 403' conclusion: access varies by route and retrieval channel.
- Demo source code/license not downloaded or inspected; no code incorporated. Grid rearrangement is **not equivalent** to 3D card-face flipping or scroll-reversible motion.
- Decision: candidate for grid transition only; not approved for replacing 12 card flip.

## Tool acceptance status
- Research discovery: PASS for both named sources.
- Source metadata and provenance: PARTIAL (source-reported license for A, article authorship for B).
- Direct Firecrawl extraction: NOT RUN.
- Direct Scrapling extraction: NOT RUN.
- Original SVG downloaded/validated: BLOCKED (DNS).
- GSAP demo downloaded and isolated browser execution: NOT RUN.
- P2 live integration: NOT RUN.

## Follow-on acceptance
Retrieve the actual SVG and code in an authorized network-enabled environment. Verify vector path integrity, SVG dimensions, origin/rights, and GSAP demo license. Compare actual card behavior to approved Olive Mountain P2 with desktop/mobile screenshots and reverse-scroll; only then choose reuse vs rejection.

Sources:
- https://freesvg.org/johnny-automatic-olive-branch-1
- https://tympanus.net/codrops/2026/01/20/animating-responsive-grid-layout-transitions-with-gsap-flip/
