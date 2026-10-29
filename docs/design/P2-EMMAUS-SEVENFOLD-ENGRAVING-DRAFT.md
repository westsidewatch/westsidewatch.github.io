# P2 / 03 以馬忤斯 — 展卷七重（Draft Art Direction）

Status: **PR #1381 only; not approved; no production release**.
Parent authority: [Westside Design OS](WESTSIDE-DESIGN-OS.md) and [Editorial Manual](WESTSIDE-EDITORIAL-MANUAL.md); visual research: `dore-design/AWARD-CALIBRE-DIGITAL-ART-DIRECTION-CORPUS-2026-09-09.md`.
The latest user's specific desktop composition correction supersedes the earlier master plan's 1/3 + 2/3 line: **Emmaus left 2/3 = ONE + study; right 1/3 = actual Doré original gallery**.

## 1. Sevenfold identity — ONE shared entrance, seven distinct realm compositions

- Do **not** restart seven top-anchored homepage curtains in chapter 03.
- Existing P2 magazine seven-color book spines remain the source of the seven realm colors (Water, First Light, Pale Gold, Olive, Harvest, Crimson, Daylight Mauve), assigned by existing Design OS tokens.
- In Emmaus they become seven **fine folio edges**, not seven new banners, not seven sub-functions of ONE. Their scalar transform samples `oneDrop` from the same existing P2 scroll distance; no autoplay, catch-up timer or independent scroll clock.
- A held scroll position must produce held edges. Reverse scroll must restore the previous geometries.

## 2. Engraving subject and provenance

The visual motif is a **micro close-up of the rolled edge of a manuscript opening onto a flat leaf**: dark-to-light copperplate-like cross-contours, with asymmetrical curved hatching and small tonal fields.
The candidate `static/images/p2-emmaus-scroll-micro-engraving.svg` is a newly created *vector art-direction study*. It must **never** be captioned as a Gustave Doré original or as documentation of a specific historical manuscript.
The right 1/3 separately uses the canonical Doré inventory, 241 engravings. It starts at actual entry **#212: Jesus and the Disciples Going to Emmaus**, then continues circularly through the complete 241-item list, so the initial plate is topical without reducing the archive. Museum evidence: [Pitts Digital Image Archive, Emory University](https://dia.pitts.emory.edu/image_details.cfm?ID=17248); verified public-domain edition, artist Gustave Doré, engraver Adolphe Gusmand. The bridge must reuse the previously displayed image, not generate another substitute layer.

## 3. ONE content is real, not a fake screenshot

The mid-field in `static/experiments/p2-emmaus-olive-handoff-lab.html` reads
`ONE_DATA.luke.chapterStudies["24"]` from the exact ONE files `luke-core.js` and `luke-21-24.js`.
It exposes three chapter route segments, genuine history/background, genuine cross-reference and genuine discussion question. All live text is semantic HTML and populated using `textContent`, not baked into the engraving SVG.
The tab labels are feature views. The 66-book rail is independent, based on `ONE_DATA.books`, and opens an actual ONE deep link; the featured Luke 24 preview remains explicitly labeled even when the reader chooses another book.

## 4. OS typography

OS source: `design-system/tokens/westside.tokens.json` → `static/css/westside-design-os.css`.
- English display: Bodoni Moda Roman 400; small-cap editorial metadata: real Bodoni Moda SC 400.
- Chinese headings: Chiron Hei HK WS 600 structural or 200 airy if legible.
- Chinese interactive labels: Chiron 400, OS UI scale, accessible size.
- Scripture or study-body reading: Noto Serif TC 400, OS reading scale.
- Do not introduce a new global CSS layer. ONE uses the existing owning `static/one/one-book.css` with `body[data-ws-scope="one"]`; P2 uses its own scoped stylesheet.

## 5. Acceptance gates (not yet visually approved)

- Validate 1648×928, 390×844, 200% zoom and keyboard focus.
- Verify that 03 has a live, readable ONE study window rather than an empty gap; no line engraving over text.
- Confirm scroll forward, reverse, stationary and reduced-motion, and preserve the approved Church → Magazine composition.
- 03→04 must remain physically continuous and never preemptively hide study content with a blank white Olive field.
- Keep production main untouched. Deploy only preview until user explicitly accepts the art direction.
