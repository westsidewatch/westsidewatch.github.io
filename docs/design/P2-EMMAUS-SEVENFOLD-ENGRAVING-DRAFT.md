# P2 / 03 以馬忤斯 — 展卷七重（Draft Art Direction）

Status: **PR #1381 only; not approved; no production release**.
Parent authority: [Westside Design OS](WESTSIDE-DESIGN-OS.md) and [Editorial Manual](WESTSIDE-EDITORIAL-MANUAL.md); visual research: `dore-design/AWARD-CALIBRE-DIGITAL-ART-DIRECTION-CORPUS-2026-09-09.md`.
The latest user's specific desktop composition correction supersedes the earlier master plan's 1/3 + 2/3 line: **Emmaus left 2/3 = ONE + study; right 1/3 = actual Doré original gallery**.

## 1. Sevenfold identity — ONE shared entrance, seven distinct realm compositions

- Do **not** restart seven top-anchored homepage curtains in chapter 03.
- Existing P2 magazine seven-color book spines remain the source of the seven realm colors (Water, First Light, Pale Gold, Olive, Harvest, Crimson, Daylight Mauve), assigned by existing Design OS tokens.
- **2026-10-30 review: freeze the existing Magazine book spines.** No duplicate folio tabs, no new chapter-03 spine animation, no recoloring or relocating the accepted Magazine sevenfold. Its original iframe is untouched and continues to own the design. Reverse-scrolling the 02→03 handoff must still restore the original scene.

## 2. Engraving subject and provenance

The visual motif is a **micro close-up of the rolled edge of a manuscript opening onto a flat leaf**: dark-to-light copperplate-like cross-contours, with asymmetrical curved hatching and small tonal fields.
The candidate `static/images/p2-emmaus-scroll-micro-engraving.svg` is a newly created *vector art-direction study*. It must **never** be captioned as a Gustave Doré original or as documentation of a specific historical manuscript.
The right 1/3 separately uses the canonical Doré inventory, 241 engravings. It starts at actual entry **#212: Jesus and the Disciples Going to Emmaus**, then continues circularly through the complete 241-item list, so the initial plate is topical without reducing the archive. Museum evidence: [Pitts Digital Image Archive, Emory University](https://dia.pitts.emory.edu/image_details.cfm?ID=17248); verified public-domain edition, artist Gustave Doré, engraver Adolphe Gusmand. The bridge must reuse the previously displayed image, not generate another substitute layer.

## 3. ONE content is real, not a fake screenshot

The mid-field in `static/experiments/p2-emmaus-olive-handoff-lab.html` reads
`ONE_DATA.luke.chapterStudies["24"]` from the exact ONE files `luke-core.js` and `luke-21-24.js`.
It exposes three chapter route segments, genuine history/background, genuine cross-reference and genuine discussion question. All live text is semantic HTML and populated using `textContent`, not baked into the engraving SVG.
The tab labels are feature views. The 66-book controller reads the one canonical `ONE_DATA.books` record. Each selected book replaces the identity, study area, ONE chapter link, and right Doré sequence together. Luke 24 and Matthew 1 have real loaded study excerpts; other books reveal an honest book overview with live chapter choices rather than carrying Luke's exposition across volumes.

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


## 6. 66-book and engraved-archive contract (2026-10-29 revision)

The bottom canonical rail is **the controller** of the spread, not just a shortcut.
On any selection, `selectBook(number)` changes:
1. The selected 66-book state, English/Chinese names, testament, chapter count and ONE deep-link;
2. The central ONE work-window. Luke 24 and Matthew 1 use real loaded ONE data; all other volumes show the selected book's canonical identity and actionable chapter coordinates (1 / midpoint / final), with the selected chapter passed to the real ONE URL and no fictitious study content;
3. The right-hand 241-plate Doré carousel. `bookPlates` is a conservatively curated mapping of catalogue IDs to their canonical books, using the existing exact title inventory; all matching plates are played **first**, followed by the remaining 241-plate archive. Books without a match start at a randomized in-range canonical ID. The library is never replaced by theme-only pictures. A late or failed Wikimedia load must never leave the previously selected book's artwork visible; retries advance inside the canonical 241-item order and otherwise show a truthful unavailable caption. 03→04 continues transferring the same right-hand image field.

## 7. Frozen Magazine spine and corrected ONE palette (2026-10-30)

- The Magazine seven-color book spine remains **unchanged in its owning page**. The second Emmaus-specific seven-tab navigation, associated jump handlers, new-color fills and staggered animation have been removed. P2's existing scene jump buttons in its proof header remain available for QA.
- ONE's actual opening uses stronger ochre manuscript paper (its standalone product declares `--one-paper:#ded096`), not the pale white/cream texture of Magazine. In chapter 03, the OS source of truth now includes `--ws-one-paper:rgb(222 208 150)` alongside `--ws-papyrus` and `--ws-pale-gold`. The P2 leaf uses the exact ONE color and original temple-stone paper texture; the previous approximate 52% gold/48% papyrus mix never reliably painted the left pane because an inner custom-property declaration overrode it. Do not reintroduce that approximation or a second independent palette. Ink is `--ws-night`, not a night/Olive blend.
- The 03 Doré gallery uses a night-blue neutral frame and OS pale-gold ruling rather than the green shadow previously borrowed from 04 Olive Mountain. The scroll engraving remains on the left, fading before actual ONE reading content.
- Future work on sevenfold continuity is **paused** until the user approves a design. No new spines should be generated as a quick substitute.

## 8. Acceptance must cover behavior, not merely source checks

Desktop and phone: changing Luke → Mark → Genesis → James → Luke must update the study heading, the right art-series start (Mark = canonical #183; Genesis = #1; Luke = #193; James = valid random fallback), the ONE link, and the selected rail state.
The accepted Magazine sevenfold spine must remain untouched in its owning iframe; use existing P2 scene controls for navigation without fabricating another sevenfold in Emmaus. Text must be legible at 390 px without the engraving overprinting it. Core Contract failures in unrelated protected assets must be recorded but must not be misrepresented as P2 visual success.

## 9. Implementation record — OS review and correction (2026-10-29)

- Authority audited before modifying this Draft: `WESTSIDE-DESIGN-OS.md` and `WESTSIDE-EDITORIAL-MANUAL.md`. No new runtime entry point, extra global type scale or standalone color manager was introduced.
- Previously missing papyrus, pale gold, morning gold, night and seventh-realm mauve variables are registered in the canonical Design OS JSON and its generated CSS runtime, rather than invented locally in P2. Mauve is the sRGB-rounded equivalent of the existing `oklch(67% .075 330)` authority.
- Emmaus's left 2/3 uses exact ONE `#DED096` ochre from the OS `one-paper` token, true night-blue OS ink and visible engraved space; the right retains real Doré originals. The second seven-leaf treatment and green-washed ink were rejected and disabled; Magazine spines remain untouched.
- All 66 book labels, chapter counts and links come from `ONE_DATA.books`; local `renderBookStudy(number,chapter)` renders a genuine loaded excerpt when present or a real chapter selector if not. The right 1/3 retains the shared 241-image Doré registry and book-first order.
- The original 03→04 physical image transfer and Church/Vol.00 iframe handoff are not changed.
- Source checks and syntax validation completed in the draft branch; visual acceptance at desktop/mobile/200% zoom, third-party image availability and reverse-scroll inspection remain separate release requirements. **Do not merge** solely because source checks pass.

## 10. Magazine-owned proportions → seven authored realm backdrops (2026-10-30)

**User decision supersedes the earlier full-screen surround and common-film
ideas.** LivingWaterWest / Church retains its unique water/door split and
proportions. Magazine retains its approved 5:8 cover, square Contents,
7-color spine and full-stage six-clip homepage film in the background,
without resizing or re-creating the film. Chapters 03 onward inherit the
**same original measured Magazine spread outer rectangle**; the film's
remaining field is instead painted with each realm's own engraved surface.
No second full-screen reveal, repeated movie player or separate 8.5% frame.

- The in-progress **?film=1** prototype was rejected: a narrow slit covered
  almost the entire video and the later invented 8.5% cinema surround did
  not respect the Magazine's approved actual ratio. Neither survives.
- Current opt-in compare: `?d=9.10&ground=1` for the Bible and
  `?d=11.10&ground=1` for Sermon; the proof header toggles this feature
  without restarting the scene or changing the active book/portrait.
- Read the real `dual-cover` + `dual-contents` bounds through the
  pre-existing protected Magazine iframe and use their bounding union
  for both the ONE 2:1 paper+gallery spread and the Olive portrait/editorial
  spread. The OS engraved field is clipped to the **outside** of that exact
  live Magazine union, so it cannot obscure the accepted Contents/cover
  during the handoff. Mobile reads the actual stacked Magazine geometry,
  not a new hand-coded global breakpoint or fixed percent.
- A single **non-interactive P2 background field** (`p2-realm-background`)
  reads `static/css/westside-engraving-authority.css`; Chapter 03
  selects the `bible` line grammar + the existing approved manuscript-edge
  study SVG, Chapter 04 selects `sermon` olive terrace contours.
  The same authority owns Book/Cinema/Life grammar for future chapters.
- The film remains the ORIGINAL Magazine player. When the Magazine ends,
  it stops instead of playing invisibly beneath other chapter paper.
  Existing painting is clipped to this same scroll timeline, and reverse
  scroll fully restores both source pages, book spines and video.
- These two engraved fields are **implementation candidates**, not finished
  authored engraving artwork. The Editorial Manual now documents the
  canonical motif sources and the required subject-specific linework QA.
  Do not fabricate future 05–07 pages or declare visual acceptance.
