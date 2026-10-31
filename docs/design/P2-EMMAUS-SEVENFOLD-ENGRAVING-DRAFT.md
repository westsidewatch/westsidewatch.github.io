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
- Read the real `dual-cover` + `dual-contents` + ORIGINAL
  `dual-continuum` seven-color book-spine bounds through the
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


## V14 / Scripture–Time Manifold — time within God's sovereignty (2026-10-30)

**Status:** isolated, opt-in experimental native SVG, not a design approval or a main-site release.
Artifact: `static/images/p2-emmaus-scripture-time-manifold-v14.svg`.
Preview: `/experiments/p2-emmaus-olive-handoff-lab.html?engraving=v14`.

**User-supplied artistic insight:** The *scroll itself can be understood as a passage*, but do not depict a physical scroll. Borrow the hourglass/collapse/throat topology from a spacetime tunnel **only as a conceptual visual analogy**: multiple accounts, periods, and scripture references become intelligible through Christ's opening of the Scriptures. Nothing meaningful lies outside the encompassing divine sovereignty. Avoid portraying God as a black hole, the mechanism of the universe as revealed doctrine, or the diagram as scientific cosmology.

- Primary Emmaus passage remains **Luke 24:27** (Christ expounds the Scriptures).
- Interpretive reference **2 Peter 3:8**: one day as a thousand years and vice versa; its immediate context is divine patience, not a numerical time-conversion ratio.
- Interpretive reference **Psalm 16:2**: "My goodness is nothing apart from You" / 「我的好處不在你以外」.
- **Visual derivation:** 66 distinct native-SVG trajectories; a double-flared chronology lattice that becomes extremely narrow at the interpretive throat, then opens; multiple fine cross-reference chords and sparse register marks; a low-opacity enclosing geometry; ONE papyrus/paper remains background authority. This should be graph/engraving, never fluid-water/V75 lines or a literal parchment object.
- SVG remains completely vector; NO embedded bitmaps. Fine line density, geometry and text safety require actual P2 desktop/mobile review. This composition is currently not endorsed for production.
- Keep the existing Magazine/Church, live ONE study panel, canonical book rail, Doré gallery, 5:8+square inherited footprint and scroll behavior untouched.


## V16 / Time field engraving — film-negative-space edition (2026-10-30)

**Status:** original native SVG + reproducible zero-dependency build script, opt-in Draft PR #1381; not art-approved and not merged to production.

**Files:**
- SVG: `static/images/p2-emmaus-chronology-engraving-v16.svg` (1,812 native SVG path elements, no bitmaps or filters)
- Source generator: `scripts/build-emmaus-engraving-v16.mjs`; regenerate with `node scripts/build-emmaus-engraving-v16.mjs > static/images/p2-emmaus-chronology-engraving-v16.svg`
- Real P2 preview: `/experiments/p2-emmaus-olive-handoff-lab.html?ground=1&engraving=v16&d=9.1`

**Corrected placement:** This engraving is the *existing video surround* `#p2-realm-background[data-realm=bible]`, **not** the embedded ONE study page. Its punch-out follows the real measured 02 Magazine spread (Contents / cover / frozen book spine). No new full-screen transition, no media players, and no fake hero image.

**Visual logic:** The reference supplied by the user is a space-time tunnel; retain a spatial passage and changing time scale, but not a black hole, sci-fi lighting or a realistic scroll. The V16 system combines an orthogonal warped chronological mesh, 66 segmented scripture cross-reference registers, an open measured passage, and localized diagonally hatched tonal lenses. It is distinguished from the V75 continuous living-water flow by its *cross-indexed axes and broken citations*. No large black central void, no empty right side, no decorative water waves. Geometry spans all four edges. All strokes are native SVG paths.

**Color authority:** The actual ONE paper `--ws-one-paper` (`#ded096`), registered through the existing Design OS, is applied to the film background in CSS. Engraved strokes use the corresponding OS `--ws-night` (`#102a43`), sparse `--ws-first-light` (`#a2872a`) and muted supplementary ink; no Magazine midnight background. Do not create new palette variables or CSS authorities.

**Theological editorial context:** Luke 24:27 is the verse of interpretation; 2 Peter 3:8 and Psalm 16:2 are supplemental conceptual references, not a literal map of God's location or a scientific model of time. This is a nonfigurative design metaphor.

**Validation status:** Source inspection checked complete native SVG path geometry and CSS opt-in attachment. Existing GitHub Actions reported Production Build success and unrelated Core Contract / DORE System Atlas failures on the latest head; those failures reference a protected homepage SVG and a film-document drift, respectively. Live browser visual acceptance is **not** established by the source checks or CI alone. Keep the original Magazine, Church and existing ONE content unchanged until accepted.


## V17 / TIME HELD OPEN — manuscript time-aperture, 2026-10-30

**Review state:** isolated Draft PR art candidate; **NOT award-calibre approved**, not promoted to main. Replaces V16 only in opt-in proof `?ground=1&engraving=v17&d=9.1`. Existing V16 remains available for A/B comparison. Original 01 Church and 02 Magazine remain immutable.

**Why this changes the design, not just the code:** V16's generic warped engineering grid had unearned grey blobs and its most legible center was obscured by the opaque ONE / Doré editorial spread. V17 makes the *void of the actual editorial folio* the conceptual passage: chronological engraved plates compress toward the opening, with nonfluid corner-local hatch pressure, 66 individually indexed Scripture connection strokes placed in the **exposed surround**, and disciplined registration cuts. It is not an illustrated scroll or a dark/science-fiction black hole. The offline concept source is original SVG code, never image generation.

- Primary scripture: **Luke 24:27**, secondary design analogies **2 Peter 3:8** and **Psalm 16:2**. The artistic treatment is a metaphor, not a physical diagram of God or time.
- **Geometry owner:** `#p2-realm-background[data-realm=bible]` and existing magazine-measured `clipPath` outside the protected actual original spread. Do NOT invent a new inner opening with CSS or change the 5:8 + square spread. SVG contains a loose visual prospect only; live P2 JS still owns exact mask geometry on desktop/mobile.
- **Native artwork:** `static/images/p2-emmaus-time-held-open-v17.svg`, 2614 authored native path marks plus one internal clip path; no bitmaps, image-generator artifacts, webfont dependency or CSS-generated repeating gradient.
- **Editable source:** `scripts/build-emmaus-engraving-v17.mjs`; exact deterministic regeneration by `node scripts/build-emmaus-engraving-v17.mjs`. Six separate meaningful SVG groups: time-sectioned-aperture, pressed-plate-highlights, engraved-distance-registers, sixty-six-canonical-cross-references, time-plate-crosshatch, editorial-chapter-indexing.
- **Color:** ONE paper `#ded096`, dark OS ink `#102a43`, carefully limited `#a2872a` gold and muted supplementary ink. No midnight-blue fill or reversed bright lines.
- **Motion:** the existing P2 02→03 scroll moves/fades the field in its real measured rect; this SVG remains static at rest and respects reduced-motion by not running an independent animation. Distinct temporal-engraving motion is still an uncompleted art-direction gate, not passed merely because the background fades in.
- **Visual QA evidence:** locally rendered 1600×900 SVG artwork and inspected full-field distribution; no fabricated live browser screenshots. **P2 desktop, mobile, 200% zoom, interactive/reverse-scroll, full performance and reduced-motion acceptance remain pending.**
- **Art director judgment / blockers:** V17 is a *more coherent alternative* to the V16 fluid-looking field, but still a candidate. Compare the actual exposed clip of the art to existing accepted V75 and Magazine at desktop 1648×928 and mobile 390×844. The concentric folio impression may still read as a generic rounded frame without enough engraving material contrast; reject if so. Do not assign a final 20-point review until the real integrated preview has been visually checked.
- **Build contract:** existing P2 tests now check pure vectors, six geometry groups, canonical ONE ink/paper background, exact SVG reproducibility and opt-in scope. Technical proof is not art approval.

Editorial manual acceptance remains **15/20 exploratory score with no zero for meaning, composition distinction, accessibility or editability**, plus separate CI, actual visual, reading, responsiveness and motion gates. Do not equate 2614 SVG paths with earned art quality.
