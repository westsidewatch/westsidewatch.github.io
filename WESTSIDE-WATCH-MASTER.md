# WESTSIDE WATCH — Master Engineering Memory

> Status: consolidated engineering decision index; 2026-10-15. This is an index and decision log, **not** a replacement for Design OS or existing specialist Markdown documents. Preserve existing specialist MDs unchanged. Never claim an asset has been located without verifying its actual path.

## Site-wide engineering workflow — binding rule for every project

**Scope:** All Westside Watch projects and subprojects, including homepage, P2/First Look, church, Olive Mountain, ONE, Doré Folio, Cinema, Dawn Library, Design OS, tools and experiments. Apply this workflow by default without asking the user to repeat it.

1. Work in an existing project PR/branch and its **Cloudflare Pages PR preview**. When starting a genuinely new project, create one PR and provide its actual Cloudflare preview URL immediately after deployment is confirmed. The PR's GitHub page is not the visual preview.
2. For subsequent revisions, commit to **the same PR** and keep **the same Cloudflare preview URL**. Cloudflare automatically redeploys that PR; inspect the updated preview rather than creating duplicate branches, previews or competing implementations.
3. Make a coherent batch of changes, clean up CSS/JS authority and remove conflicting obsolete rules instead of piling on overrides or submitting one-line micro-commits. Run relevant checks and inspect the actual preview, including motion, responsive layouts and regressions. CI passing alone does not constitute visual acceptance.
4. Continue fixing identified failures within the same engineering phase, without repeatedly stopping for an unnecessary “continue” message. Report concise, verified results, the **clickable Cloudflare preview URL**, and genuine blockers only.
5. **Do not merge into `main` unless the user explicitly requests a merge.** Preview deployment and PR commits are not merges; do not make merge approval a prerequisite for preview work, and do not repeatedly raise merging when the user is reviewing a preview.
6. Preserve the last approved visual and functional baseline, its original assets and the user's design decisions. When a new preview is unavoidable, explain why and give the new working preview URL; never silently move the user to a different preview.
7. Distinguish confirmed working preview URLs from URLs inferred from naming conventions. Verify deployment before claiming a URL is live; if verification is pending, state that plainly.

**Default reporting format:** completed changes + verified checks + current Cloudflare preview link; omit repetitive PR/merge discussion unless requested or materially relevant.

## Source of truth and change rules

- Canonical seven-realm order comes from the **live homepage source**, `layouts/partials/watch-home-editorial.html`, including its numbered floating Contents menu and First Look anchors. Do not reorder from conversation memory.
- Approved preview means the entire approved implementation, including motion, composition and content, not a sample to strip down.
- Preserve existing specialist MDs. Merge their key decisions and verified pointers into this index only after inspecting the originals. No deletion, renaming or rewriting of specialist files as part of consolidation.
- Keep **verified implementation**, **approved design**, **candidate**, and **unverified recollection** distinct.
- One integrated Design OS controls global type, colors, geometry and style; do not create competing management systems. Per-page overrides must not unexpectedly change the entire site.
- Do not stretch type, do not use prohibited black/gold palettes, and do not replace existing approved assets with approximate reconstructions.
- Work in coherent engineering phases rather than numerous micro-PRs. CI pass is not proof of browser visual acceptance.

## Homepage canonical seven-realm order

| No. | Realm | Homepage anchor | Existing First Look |
|---|---|---|---|
| 01 | LivingWaterWest · 教會 | `#first-look-church` | `/first-look-editorial/church.html` |
| 02 | Magazine · 西望雜誌 | `#first-look-magazine` | `/first-look-editorial/magazine.html` |
| 03 | Emmaus · 查經 | `#first-look-bible` | `/first-look-editorial/bible.html` |
| 04 | Olive Mountain · 橄欖山 | `#first-look-sermon` | `/first-look-editorial/sermon.html` |
| 05 | Dawn Library · 黎明書局 | `#first-look-book` | `/first-look-editorial/book.html` |
| 06 | Paradise Cinema · 天堂電影院 | `#first-look-cinema` | `/first-look-editorial/cinema.html` |
| 07 | Daylight Café · 日光咖啡館 | `#first-look-life` | `/first-look-editorial/life.html` |

This order applies to P2, navigation, documentation and later First Look alignment.

## P2 — Sevenfold Editorial Showcase

**Intent:** One scroll-controlled editorial stage. The original seven overlapping/folding layers are a shared spatial grammar: fold → divide → reshape/recompose → reveal each realm. Seven realms have distinct editorial compositions, not seven independent websites or seven unrelated effects.

**Sequence:** 00 identity prologue: Sevenfold folding reveals that Westside Watch belongs to Living Water West church. Then 01–07 realm-specific showcases, starting with a distinct church showcase and its **left/right opening doors**. Do not confuse the identity prologue with church realm 01.

**MERSI reference:** study the continuity of composition, split/crop, reflow, Flip-style spatial transformations, reversible scroll and horizontal movement. **The church door-opening is our own design, not an effect attributed to MERSI.** Integrate ideas; do not copy the reference site wholesale.

| No. | Realm | Assigned distinct spatial composition |
|---|---|---|
| 01 | Church | Left/right opening doors following the identity prologue |
| 02 | Magazine | Three-column editorial composition; asymmetric reflow/cross-column layout |
| 03 | Emmaus | Unequal 1/3 + 2/3 split and layered Bible/visual material |
| 04 | Olive Mountain | Main portrait plus multiple small windows, reorganizing toward a speaker gallery |
| 05 | Dawn Library | 1/4 rectangle/section expands into a book/editorial scene |
| 06 | Paradise Cinema | Upper/lower split unfolds toward widescreen cinema |
| 07 | Daylight Café | Asymmetric collage/recomposition of different-sized panels |

**Status of realm choreography:** the above are recovered planning decisions, not a claim that all seven have been implemented or visually accepted.

**P2 implementation verified on main:**
- `layouts/partials/watch-home-editorial.html`: second screen iframe `/p2/living-water.html`, sticky scroll host and progress bridge.
- `static/p2/living-water.html`: seven `.plane` layers and seven `.edition` layers; scroll-driven rendering; Fixed Ocean 2.5 overlay.
- `static/experiments/sevenfold-first-to-second.html`: earlier experimental preview (check branch/ref before treating as the approved canonical version).
- `static/experiments/assets/living-water-contour-engraving-v10.svg`: contour engraving asset.
- PR #1332 integrated full preview and scroll bridge; PR #1333 addressed suspected ocean white strips, merged as `68d2748c6635cc1d38cb9c417fc001db799bc422`. CI green was reported, but **browser visual acceptance remains unverified**.
- Ocean reference preset: propagation 1.5, gradient 2.0, local amplitude 6px, density 2.5, 620 paths. Avoid retuning approved parameters without explicit design authorization.
- **P2 is unfinished.** Do not advance to screen 3 as though P2 were complete.

## Related assets and documentation — verified vs pending

### Verified code paths
- `static/js/church-mersi-journey.js`: scroll scene progression, reversible scene changes, horizontal gallery; this is a church-specific prior implementation, not proof of the Sites prototype.
- `static/css/church-mersi-motion.css`: church MERSI-inspired compositions and transitions.
- `static/js/first-look-host.js`: homepage First Look frames and floating nav/Sevenfold menu.
- `static/css/sevenfold-dawn.css`: first-screen Sevenfold/navigation styling and cross-screen visibility constraints.

### Recovery register: DO NOT LOSE
- **十字架的影子 / Cross Shadow** — important existing visual decision/asset. **Original specialist MD, source asset, exact implementation and approved appearance have not yet been located or verified.** Search source, PRs, historic branches and specialist documents; record verified paths and screenshots here when found. Do not improvise or recreate it from memory.
- **Sites MERSI prototype** — previously referenced Sites URL: `https://westside-watch.chenjingyu1948302.chatgpt.site/`. Current accessibility and exact source mapping unverified. Preserve existing original work.
- **Design OS / typography / colors / engraving / Jerusalem / Olive Mountain / cinema / ONE / Doré Folio / First Look** — specialist MD inventory pending full repository tree audit. Do not claim these documents were merged or deleted.
- **七層折疊歷史方案** — staircase-fold and bookmark-fold were considered; do not silently treat unaccepted candidates as final P2 assignments.

## Consolidation protocol

1. Inventory every existing `.md` by verified repository path and its purpose.
2. Identify authoritative decisions, source assets, PR history and pending questions for each.
3. Put short, durable decisions and direct file pointers here; **retain all specialist MDs unchanged**.
4. Link related entries (e.g. Cross Shadow) even if the source is not yet located; label missing paths explicitly.
5. Update this master index when a design is approved or a PR merges, separating merge/CI status from browser acceptance.

## Next engineering stage

P2 seven-realm storyboard and shared motion architecture, in homepage 01–07 order. Preserve the approved church identity reveal, seven-layer folding, Fixed Ocean 2.5, and build the distinct church opening before extending the other six. Browser-verify transitions, responsive behavior, reduced-motion and exact asset continuity before claiming completion.
