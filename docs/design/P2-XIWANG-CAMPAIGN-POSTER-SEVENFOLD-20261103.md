# P2 / 《西望》Campaign Posters A1 + B1 / Sevenfold Dawn

**2026-11-03 · Draft implementation and art direction; NOT an approved final artwork.**

This decision supersedes the calligraphy-based requirement in P2-XIWANG-TYPE-REDESIGN-COSMOS-20261102.md. The earlier research remains archived but is no longer a binding glyph specification. The explicit user decisions are: **both posters must be made**; **no brush-calligraphy primary lettering**; **no Doré illustration in the Magazine spread** because Emmaus owns Doré; **remove the permanent seven-color magazine-side navigation**; let the homepage's sevenfold reveal introduce the poster itself.

## Two equally real magazine campaign posters

**A1 — Geometric letterform / campaign key visual.** The user's coral-red-on-pink oversized Chinese poster is a construction reference: purposefully exaggerated main strokes, counterspace, diagonal geometric cuts and nearly full-surface two-character identity. Compose two exact Traditional Chinese characters, 西 and 望, in the left square. This is a new modern publication poster, not a restyled calligraphy label. The right side remains the already approved official 5:8 Magazine cover.

**B1 — Engraved typographic field / second campaign poster.** The user's grey-on-charcoal poster with dots, curved striations and radiating line density is the structural reference: native SVG engraving and optical density should FORM the Chinese glyphs, not lie as a random texture over an already finished word. Keep it independently publishable rather than making B a decoration of A.

Source illustrations and rights: user reference posters are examples of methods, not licensed files to copy. Do not import either image into the deployed P2 or claim the original typographic artwork is open source. Both A1 and B1 have a shared cover-pair composition, paper/ink discipline, fine folio labels and native SVG semantics.

## Sevenfold fold — source checked against the actual homepage

Canonical references:
- [Sevenfold Dawn homepage contract](../SEVENFOLD-DAWN-NAVIGATION.md)
- static/js/first-look-host.js — makeFolds(), seven complete top-down scaleY panels and one reversible GSAP timeline
- static/css/sevenfold-dawn.css — .ws-dawn-folds and .ws-dawn-fold
- static/css/westside-design-os.css — seven original palette variables

**Important distinction**: the homepage sevenfold is SEVEN full-surface color curtains descending from the TOP; it is not the seven tiny vertical color ribbons visible in the old Magazine. The homepage shuffles final colors per discrete menu opening. P2 uses deterministic order per scroll progress so reverse scroll really reverses the same animation. The seven colors must be the OS variables: water, first-light, pale-gold, olive, harvest, crimson and daylight-mauve.

**Magazine placement**: the fold covers the entire square left poster, then recedes while A or B reveals top-to-bottom and eventually remains alone. The thin old Magazine spectrum bar is gone visually and interactively. Its inert, hidden DOM element temporarily survives ONLY as a measurement anchor for 03–07's already built spread geometry, never as navigation. Existing homepage section links still provide seven fully functional routes. No separate GSAP instance: follow the P2 existing reversible scroll renderer.

## Draft implementation in the original P2

1. static/js/p2-vol00-poster.js creates both selectable SVG poster studies and seven color curtains. The A geometric strokes currently use a vector text mask with deliberate angular counterspace. B uses vector dotted, wavy and radial engraving fields clipped to a Chinese glyph silhouette.
2. static/css/p2-vol00-poster.css scopes all changes to the original Magazine LEFT square. Old left Doré image, ink-brush wordmark, star and Contents are not displayed in poster mode. The protected RIGHT magazine cover remains unchanged.
3. static/experiments/p2-double-square-video-lab.html now offers A/B poster modes and controls, preserving ?poster=legacy for old approved screenshots only. It calls the same poster painter on its current scroll progress, no second animation clock.
4. static/js/p2-magazine-live-bridge.js passes same-origin P2 query poster=a or poster=b to the original embedded magazine frame.
5. Existing A/B is a **typographic composition proof**, not the final optically corrected original path master. SVG text currently inherits Design OS Chinese sans display. The next artistic step is true custom letter-shape adjustment, not pretending these are already award-grade original glyphs.

## Required verification before approval

- Full spread 1648×928, 768×1024, 390×844, 320×720, 200% zoom and reduced motion; both A and B must pair with the original 5:8 cover with no clipping or horizontal overflow.
- The sevenfold must be a top-to-bottom seven-panel reveal and reverse cleanly; by full rest no colored ribbon is visible and the poster is completely visible.
- A and B must be different real typographic systems with legible 西 and 望. Geometry and engraving are not simply filters.
- The Magazine must show no Doré illustrations, which remain available in the genuine Emmaus gallery. No changes to Church, main Homepage sevenfold, approved cover or later ONE tools.
- Preserve keyboard, accessibility, route access from Homepage, native SVG and the single Design OS; do not merge main until live browser screenshots and regression checks are reviewed.

**Design priority**: both posters are equally real campaign assets; A may open the Vol.00 spread and B may alternate as the next campaign poster. Do not turn the poster back into a Contents/illustration page.
