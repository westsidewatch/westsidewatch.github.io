# PR #1352 — P2 editorial award-calibre quality review

Status: **IN PROGRESS / NOT VISUALLY APPROVED**  
Date: 2026-10-21  
Authority: [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) §6A and the single [Westside Design OS](WESTSIDE-DESIGN-OS.md).  
Skills: [new-westside-editorial-web](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/SKILL.md), visual grammar rubric, `ui.visual-hierarchy`, `ui.motion-forensics`, `ui.critique`, `ui.accessibility`, `ui.visual-verification`.

## Thesis

**One river becomes two doors; one editorial volume appears as cover above contents, held between the star/西望 and Romans 13:12.** Award-calibre recognition is a quality *target*, not a quality *claim*.

## Source of evidence

- User-provided 2026-10-21 screenshots: ~61% and ~71% Church split, ~90% closed spread, 100% opened three-column state, and the newer cover+contents state.
- Actual repository proof CSS/JS and official Vol.00 editorial map.
- Browser screenshot of the **newest candidate after this pass: NOT AVAILABLE YET**. The preview can build/deploy without proving optical quality.

## First critique and coherent corrective pass

| Priority | Defect in supplied view / code | Decision | Owner / acceptance |
| --- | --- | --- | --- |
| **block** | Nearly blank scroll intervals break the causal transition | Retain current proof-only compact handoff; require replay, reverse and reduced-motion test | `static/js/p2-living-water.js`; in-browser scroll checkpoint trace |
| **block** | Full-open Contents copy is far too small relative to the page and has no clear scan hierarchy | Increase Chinese titles, English labels, section numbers and interlude reading sizes, improve rhythm without inventing copy | `static/css/p2-magazine-transition-proof-v3.css`; actual 1648×928 and phone screenshots, check clipping/scroll |
| **important** | The right verse completes in the upper part of a tall navy plane, leaving an unexplained lower half | Move the English/Chinese reading group up to meet the star's axis while extending Chinese/folio to the middle of the field | Same scoped stylesheet; compare 90% and 100% poses |
| **important** | Original 西望 SVG remains disproportionately large and heavy after opening | Reduce the final display height, preserving the original vector proportions, and keep star/glyph synchronized | Same CSS/JS; 90%/100% screenshots |
| **important** | Reduced motion only disabled will-change but did not stop scroll-bound transforms | Snap the five proof stages; star iframe already respects OS reduced-motion preference | Proof JS + original morning-star asset; actual reduced-motion user-agent test |
| **important** | Real rendered browser geometry, contrast, keyboard, 200% zoom and responsive frames not independently observed | Remain unapproved rather than assume screenshots from green CI | Design OS geometry tool and visual verification |


## Pass 3 — Negative space as a 44% editorial register

**Before:** The user's 18:10 screenshot shows left gold and right navy as unstructured remainder despite the strong central paper pairing. More decorative objects would worsen the problem.

**Single design direction: dawn threshold.** Above the exact 44% cover/contents fold, the morning star and English Roman text hold the attention; beneath it, the natural-aspect original 西望 SVG and Chinese scripture establish the second reading movement. The Romans source settles near the base, safely above the city wall. Both moving color-leaves share one almost invisible registration rule aligned to the real paper seam, not a repeated engraved texture.

**Implementation:** The right quotation now has separate semantic English/Chinese groups in one full-height 44/36/20 editorial grid. The star ends at 18svh instead of 13svh; 西望 is lifted nearer the star and becomes 5svh shorter during opening, without horizontal or vertical distortion. Subtle local dawn/night lighting references the actual subject, not decorative filler. The middle cover and complete contents are preserved.

**Acceptance pending:** Compare the 90% held two-leaf state with the 100% opened triptych at 1648×928, 768×1024, 390×844 and 200% zoom; verify no overlaps with real font metrics, reversibility, independent article scrolling, reduced motion, and keyboard focus. This is design implementation, **not** evidence of award-calibre approval until screenshots are checked.

**Rejected direction:** Adding extra line engravings or metadata to fill both color fields. This would reduce editorial restraint without fixing the compositional weight.


## Integrated re-art-direction dependency — professional longform publishing (2026-10-21)

**Decision:** PR #1352 remains a P2 **prototype**, not a finished magazine or standalone sufficient art direction. P2/First Look cannot be signed off independently of real Vol.00 article layout. The Design OS [Editorial Manual §6C](WESTSIDE-EDITORIAL-MANUAL.md) now defines one connected **P2 → issue → longform feature → optional paged export** project.

**Doré Explore findings:** Paged.js MIT/API/CLI is the smallest practical HTML-based print proof; Vivliostyle AGPL-3.0/CLI/Viewer has strong paged magazine/book facilities but requires architecture-specific licence review; DesignCraft MIT/Apache-2.0 offers headless/MCP special spread layout but still requires testing on protected CJK manuscripts; Folio is short-form presentation-oriented and not the tens-of-thousands-of-characters composer. Native Hugo semantic article HTML with Westside OS remains the screen-reading authority. The earlier open-source research was not indexed in the actual manual before this review; it is now recorded **as a candidate selection, not an installed engine**.

**Next-stage work plan:** A) locate and protect manuscript source; B) one shared editorial blueprint for P2, issue, reader; C) readable longform first, with fixture tests; D) compare isolated Paged.js/Vivliostyle proofs + agent-led DesignCraft spread; E) integrate true links and responsive state; F) evaluate actual screenshots, performance and CI. This plan is a **dependency** for the P2 re-art-direction, not an authorization to overwrite unrelated book, Doré or Dawn Library stores.

**Blocked until proven:** source inventory, real article lengths, Chinese paragraph/font metrics, 390px reader, keyboard/footnotes, 20k/50k stress rendering, print proof and before/after screenshots. **NOT VISUALLY APPROVED / DO NOT MERGE.**

## Font authority audit (2026-10-21)

**Correction:** Earlier P2 longform planning incorrectly described Noto Serif TC as the active Chinese Journal reading family. The loaded Sites OS stylesheet overrides --ws-type-reading-zh to Chiron Hei HK WS; article typography enforcement consumes that resolved variable. Canonical token JSON and some older bundles still declare Noto, so cross-surface authority is NOT RECONCILED.

Documentation corrected in the Design OS overview, editorial manual and typography detail. This commit does **not** change live font CSS or font downloads. Before promotion, reconcile OS token/runtime authority and verify actual Chinese/English computed fonts at Journal, Vol.00, book and tool, including long text, phone and 200% zoom. Status: OPEN.

## Award lenses and current score

Internal 10-axis rubric is **NOT SCORED** until the updated preview is actually observed at desktop, tablet and phone. Earlier screenshots expose blockers; they do not support an 18/20 promotion. Awwwards score, Webby score and FWA score **are not provided or inferred**.

Pre-release gate: internal review ≥18/20 with no zero, no unresolved block; additionally all browser, usability and scroll checkpoints must pass. These thresholds are **local Westside gates only**, never official award thresholds.

## Review cycles

1. **Pass 1 — source code and editorial critique:** no-op scroll audited, complete Vol.00 contents preserved, typography hierarchy and two-leaf balance adjusted, keyboard focus and reduced-motion behavior improved. JS syntax check and CI still required.
2. **Pass 2 — static keyboard/reduced-motion critique:** add `inert` to unready magazine content; keep interactive contents in the Tab order only after the leaves open; make the inner Contents region keyboard-scrollable and visibly focused. These are code-level corrections, **not** a keyboard-browser PASS. Deployed side-by-side browser screenshots still pending: measure 90% / 100% at 1648×928, 768px, 390px and 200% zoom.
3. **Pass 3 — rejection / refinement:** apply only if pass 2 supplies reproducible defects, not speculative CSS overlays; re-run the same screen and use the same rubric.

**Do not merge** merely because PR is conflict-free or Cloudflare preview/Production Build succeeds.

## Chinese longform typography normalization (engineering pass, 2026-10-21)

Canonical Chiron reading family is generated from the existing Design OS JSON, duplicate CSS declarations are removed from both Sites and non-Sites compatibility bundles, Hugo `.prose` consumes the reading token and the existing OS contract guards future divergence. **This is one source-of-truth normalization, not a new design system or a new CI.** No English long-body font has been invented; test before choosing it. Non-Sites books/tools could change appearance as Noto falls back to Chiron. Actual font loads, 20k/50k Chinese text, 390px/768px/200% zoom, mixed English and other surfaces **remain NOT VERIFIED / DO NOT MERGE**.

## Longform typography browser fixture (2026-10-21)

A read-only, non-indexed proof is available at `/experiments/editorial-longform-type-audit.html` on the PR branch preview. It loads the **real Westside Design OS and typography enforcement**; tests Chinese OS reading role with 5k/20k/50k synthetic characters and two English comparison samples (Bodoni display face versus browser Georgia reference, **not** an approved English font). It reports computed CSS family, discovered/loaded Chiron FontFaces, line-height, column geometry and horizontal overflow. It does **not** modify a real article, canonical text or production reading type.

**Offline Chromium structure test:** 51,591 synthetic characters, 1,050 paragraphs and 34 headings at 1648×928, 768×1024, 390×844 and an approximate 200% text-zoom stress viewport of 195px: no page horizontal overflow. Render process about 77–183ms in this local environment for this synthetic fixture. **Zero Chiron faces loaded offline**, and local fallback fonts were used. These data verify neither production webfont loading nor real reading comfort. Browser computed font and real downloaded font must be confirmed on deployed proof.

**Visual verification gate remains OPEN:** compare actual 390px/768px/1648px glyph appearance, long English passages, punctuation, kerning, line heights, fallback and CJK extents; test article-local TOC, anchors, return navigation and 200% browser zoom separately. Keep status NOT VISUALLY APPROVED; no automatic merge.

## Three user screenshots — browser type-audit finding (2026-10-21, 22:36 Toronto)

The user supplied **three real browser captures** from the deployed proof at 20,000 synthetic characters: English Georgia reference, English Bodoni Moda and Chinese OS role. The Chinese mode reports `computedFontFamily: "Chiron Hei HK WS, Noto Sans TC, sans-serif"`, positive loaded Chiron faces and `horizontalOverflow: false`; report width was approximately **356px** despite the 1648px desktop viewport. This is evidence that *a Chiron font face loaded* and CSS selects the intended family, not proof of exactly which glyphs were rendered or that the longform design is good.

**FAIL found:** Georgia/Bodoni modes reported different **wrapper** `font-family` but rendered similarly. Root cause: the live OS typography-enforcement selector applied the Chinese reading role to **all** article `p,li,blockquote`, including those inside `lang="en"`. A wrapper-only `getComputedStyle` masked the error. Also, the 40ch grid track produced an unnecessarily narrow desktop reading column.

**Corrections:** The existing OS enforcement now excludes `:lang(en)` descendants from the Chinese role (respecting inherited language); the proof gives English paragraphs/headings explicit language, calculates and reports the **actual paragraph's** `font-family`, and fails its own check if the active paragraph family differs from the selected mode. A 40rem desktop column replaces 40ch; under 980px the layout becomes a full-width, capped one-column reader. The existing OS contract asserts the language guard. No English production body face was selected; Bodoni-vs-Georgia is still a visual research experiment. This does not declare award-level typography or approve the P2 PR.

**Acceptance still needed:** Recheck 390px, 768px, 1648px at 100% and 200% zoom; real glyph/fallback comparison; a longer English original sample; genuine article assets and notes. The status is **PARTIALLY VERIFIED / DO NOT MERGE**.


## Deployment-confirmed browser screenshots — typography phase 1 (2026-10-22, 00:14 Toronto)

**Evidence:** User supplied three real screenshots of the rebuilt longform proof (Chinese reading token, English Bodoni Moda, English Georgia reference) using **20,000-character synthetic text**, taken after the browser test was deployed. These replace the earlier 22:36 screenshots where English modes were ineffective. The actual browser report says `viewportWidthPx: 2992`, `columnWidthPx: 640` (regardless of the dimensions of the uploaded/compressed screenshot).

| Observed in the three captures | Chinese / Chiron | English / Bodoni | English / Georgia |
| --- | --- | --- | --- |
| `paragraphFamilyMatchesSelection` | true | true | true |
| `computedParagraphFamily` | Chiron Hei HK WS, Noto Sans TC, sans-serif | Bodoni Moda, serif | Georgia, serif |
| `paragraphTextCharacters` | 20,000 | 20,000 | 20,000 |
| `loadedChironFaces` | 10 | 10 | 10 |
| `loadedBodoniFaces` | 3 | 3 | 3 |
| `columnWidthPx` | 640 | 640 | 640 |
| `horizontalOverflow` | false | false | false |
| CSS paragraph font size | approx. 18.88px | approx. 18.88px | approx. 18.88px |
| CSS paragraph line-height | approx. 34.37px | approx. 32.1px | approx. 32.1px |

**What this actually proves:** The deployed **desktop** experiment now selects the intended CSS family *on the paragraph element*, the Chiron and Bodoni webfont families have loaded faces in the document, and the synthetic long-text layout is horizontally contained at the reported viewport. English paragraph styles are no longer overridden by the Chinese reading selector. Georgia is a *local reference*, not an approved or downloaded English body font. FontFace status does not prove every displayed glyph avoided fallback.

**What it does NOT prove:** Actual Chinese glyph-by-glyph family selection, multi-page professional readability, typography on `journal` / `vol-00` / ONE / Dawn Library / book routes, 390px/768px/200% browser zoom, printed folios, real manuscript and footnote behavior, or award-level composition. The screenshot visibly remains a minimal test scaffold with repeated synthetic paragraphs, not the published magazine reader. Chinese heading weights may still be overridden by `static/css/westside-typography-enforcement.css` (`font-weight:200!important` for general heading selectors), so **display hierarchy needs a separate scoped semantic-role test** rather than a local patch.

**Disposition:** **PASS — phase-1 desktop language-aware font selection and 640px measurement.** **OPEN — cross-surface authority, mixed-script running text, headings, original manuscripts and complete editorial/visual QA.** The P2 PR remains **NOT VISUALLY APPROVED / DO NOT MERGE**. Next use genuine prose and verify reading roles and weights across existing site routes, not more decorative changes to the diagnostic page.

## Twelve-role Design OS editorial scale — implementation and review gate (2026-10-22)

The user confirmed: Chinese MAIN title 900; English companion genuinely Bodoni 400, visually much larger; all other Chinese NON-BODY editorial headings 200, compensated through type-size and layout, not boldness. This rule is now encoded as twelve semantic responsive role tokens in the same JSON/generator/OS and as opt-in CSS classes, rather than a new design system. The former realm 600 and unqualified Chinese primary 200 are inconsistent legacy assumptions; scope migration is still pending. The full role-by-role sizing table is in docs/design/WESTSIDE-EDITORIAL-TYPOGRAPHY.md. A branch-only hierarchy specimen is at /experiments/editorial-type-hierarchy-lab.html.

Acceptance is not a passing build alone: photograph the actual main-title/secondary-title distinction on P2, issue and real longform, verify true loaded Chiron 200 and 900, at mobile, tablet, desktop and 200% zoom, plus correct Bodoni 400 and untouched functional 400 body/controls. **Status: design type grammar implemented, page migration NOT VISUALLY APPROVED; do not merge.**

## Visual identity research gate — Classical source, contemporary graphic expression (2026-10-22)

**Work before further P2 CSS:** Research chapter **§6D** was appended to the existing [Westside Editorial Manual](WESTSIDE-EDITORIAL-MANUAL.md), containing 42 recorded research paths, 14 in-depth precedents with transfer/rejection logic, links to the older Doré Visual Reference System and kinetic typography memo, and 3 proposed comparative compositions for P2. The user clarified the goal is **an original Westside Magazine art direction**, not a generic typographic scale, three equally sized columns, nostalgic texturing or simply spectacular UI motion. Hypothesis name: **Engraved Editorial Modernism** (classical sources, contemporary editorial expression), to be tested rather than adopted by declaration.

**Current P2 failure map:** the earlier 87–90% held two-panel mustard/navy stage reads as adjacent posters, not a coherent issue; the 100% equal triple with miniature central Contents, disconnected sidebars, and repeated crenellation strip reads as UI instead of a publication. The users' 4 screenshots prioritize unequal editorial columns, large type/actual photo, display serif monumentalism, complete readable pages and deliberately directed negative space.

**Three visual candidate tests:** A Monumental Engraving / 42:58 held spread and ~20:56:24 open; B Living Atlas / 35–45% archival plate held and ~24:52:24 open; C Cine-Folio / legally reusable original homepage video still transformed into an issue image with accessible body layout. All percentages are hypotheses, NOT coded changes or accepted tokens. Chinese 900/200 and authentic Bodoni 400 remain the one OS, with deliberate giant-size exceptions considered only *after* selecting the visual grammar. Mobile after opening retains the center editorial reading column.

**Stop condition:** do not refactor live P2 on the strength of citations or token fixes. First produce real-image/real-copy comparative stills for 87–90%, 100% and a longform article, verify sources and rights, then select **one** authored direction. CI and work on fonts alone do not constitute art-direction approval. **Research filed / prototype NOT YET BUILT / NOT VISUALLY APPROVED / DO NOT MERGE.**


## Three rendered art-direction candidates — comparative stage (2026-10-22)

**Implemented:** one isolated proof at `/experiments/p2-magazine-art-direction-studio.html` with direct query params `?concept=a|b|c&view=hold|open|article`. It contains 9 deliberately **structurally different** states (3 visual directions × 87–90% hold / 100% open / real-manuscript article opener), with a responsive mobile reflow. This does **not** switch the current P2 animation, replace approved assets or alter the Design OS source.

**Content authority:** `docs/projects/watch-city-vol00/EDITORIAL_MAP.md` defines 4–4–2–2 / 12 columns / 3 interludes; the prototype renders all 12 and their confirmed works without fabricating missing Bethlehem / Beersheba / Bethel articles. Article stage uses genuine excerpts from `docs/projects/watch-city-vol00/manuscripts/the-gate/城門口的人.md`, `docs/projects/watch-city-vol00/manuscripts/carmel/canonical/01-人為什麼要建一座城.md`, and `docs/projects/watch-city-vol00/manuscripts/carmel/canonical/00-王進城了.md`. These excerpts are separately attributed in the lab, not represented as finished web publication.

**Asset reuse:** official `static/images/westside-watch-masthead-landscape.svg`; the already stored `static/images/home-opening-engraving.jpg` as the classical engravable illustration; existing temple-stone substrate where relevant; Cine-Folio mounts the **actual existing homepage film consumer** `/preview/watch-city-vol00/hosanna/?cover=1&v=20261012-cover-palette-r1` only while concept C is selected. It is treated as an editorial moving-image object and preserves an image poster fallback. The player is noninteractive in this comparison; the official film link remains usable. Do not claim the engraving photo is a specific ancient archaeological image or licensed for print beyond the site's existing use.

**Directional comparisons:**
- **A · Monumental Engraving:** asymmetrical 42:58 held; desktop open 20:55:25. Ink-blue giant serif "CITY / of / LIGHT" and true Chinese 900 make the monumental cover; a side plate is a crop of site engraving; all verified TOC exists on the right desktop register, with a **separate mobile-only true TOC inside the center** when side elements hide.
- **B · Living Atlas:** atlas specimen left, giant "00" issue folio and deliberately factual image-caption register; 23:53:24 open screen. Issue structure and four movement parts remain in central Contents. Architectural media not repeated as a low-res border wallpaper.
- **C · Cine-Folio:** 62:38 moving-image-held spread, open 60:40 including source-video field, giant Bodoni DAWN title and true Vol.00 Contents. On phone the *opened* moving-image side is hidden and the editorial middle reading panel is retained. Original video may be expensive or unavailable: poster still must persist without motion.

**First-pass structural review:** All three variants have real art direction, separate editorial registers and verified copy; none pretends to be a finished magazine. This phase **cannot pass visual approval on code alone**. Priority screenshots and issues: (1) A English letter crop versus adjacent image; (2) A 100% side register scrolling and its mobile transfer; (3) B number / image / text balance and four movement legibility; (4) C actual player load/poster and image-text contrast; (5) exact Chiron 900 / 200 and Bodoni genuine Roman 400 computed typography; (6) keyboard stage switches and reduced-motion; (7) 1648px/768px/390px and 200% zoom, viewport-height constraints. Avoid rating 18/20 before snapshots and factual editorial review.

**Status:** FIRST COMPARATIVE COMPOSITION IMPLEMENTED / NOT VISUALLY APPROVED / DO NOT MERGE. Promote exactly **one** direction after user sees the real screenshots, then recompose existing P2 stages via the current owner JS/CSS. No alternate system or separated production route.


## Rejection after real screenshots — no magazine triptych; homepage film protected (2026-10-22)

**Binding user decisions:** Keep the **currently approved full-bleed film homepage intact**, including its film, framing, playback and scroll behavior. Only *after* selecting the Westside Watch visual identity may homepage **font size, font weight and text placement** be separately reviewed. No homepage code, assets or CSS changed here.

**Reject for all P2 magazine art-direction options:** the visually independent three-column panel composition. A's 20:55:25 and B's 23:53:24 opened triptychs are withdrawn; do not restore them by changing ratios. These read as independent UI panels, not one editorial work. Functional micro-grids within a coherent Contents or a distinct Church schedule are not banned.

**Revised isolated lab only:** A becomes a single engraving field + one unified paper field containing title, real four-movement Contents and CTA, with one DOM copy of Contents. B becomes one archival plate + one editorial field; Romans 13:12 is embedded *after* the actual Contents, not used as a third full-height navy panel. C remains video/image + publication field; on mobile, preserve the video/poster instead of hiding it. All actual article excerpts retain a single readable column. Existing approved original homepage and actual P2 animation are untouched.

**Gate:** These are revised layout hypotheses requiring desktop/mobile screenshots, actual font, long titles, mixed-script wrapping, 200% zoom, accessibility, reduced motion, source film fallback, and design signoff. **NOT VISUALLY APPROVED / DO NOT MERGE.**


## WoI square-composition reference: a selectively chosen trait, no Folio endorsement (2026-10-22)

The user clarified that **The World of Interiors** is a source of **square-image/square-composition mechanisms** within an otherwise freely varied editorial identity, not an instruction to copy its print page, eliminate rectangular or full-bleed photography, or approve any current A/B/C/Cine-Folio/Square Folio direction. A square focal frame is **one provisional component**, not the page-template system. Previous "reject independent triptych" remains valid: **one uninterrupted image backing the left and right with a square editorial focal field** is a different experiment from three unrelated, separately colored, vertically divided UI columns.

First-party 2022 GTF/Hamish Bowles redesign rationale and print/digital examples reviewed; findings, evidence-vs-inference distinctions and test matrix are filed in the *existing* Design OS Editorial Manual §6D.5b. The proposed "continuous-image + square focal field" should be compared with wide rectangular and full-bleed editorial alternatives before visual selection. Preserve the accepted full-bleed homepage video, official assets and existing P2 movement. This stage records **research and candidate constraints only**, changes **no prototype HTML/CSS/JS**, and implies **no approval or merge**. Current PR remains **NOT VISUALLY APPROVED / DO NOT MERGE**.


## Square / wide / full-bleed — same-source award-level visual study (2026-10-22)

Implemented on the **existing isolated art-direction studio** only: `?view=geometry&shape=square|wide|full`. All three presentations share exactly the same historical engraving source, official logo, real *The Gate / 城門口的人* excerpt and complete canonical Vol.00 Contents; shared underlying source/reading grid. No new Design OS, no new runtime or image generation; original fullscreen home film, P2 ocean/church/magazine choreography and frozen logo assets remain untouched. The 1:1 square is one *selected candidate feature*, not endorsement of Folio or exclusion of landscape/full-bleed. See existing Editorial Manual §6D.5c.

**Award-calibre prerequisites:** Design OS §6A, not a second authority: Awwwards Design 40 / UX 30 / Creativity 20 / Content 10; Webby holistic structure/functionality/content; FWA original interaction. Existing 10-criterion 0–2 internal rubric, **18/20 without any zero/block**, independently checked text flow/performance/accessibility. Compare deployed 1648×928, 768×1024, 390×844, 200%-zoom screenshots before scoring. **CODED / NOT VISUALLY APPROVED / DO NOT MERGE**.


## User screenshot — wide 1.95:1 is below release quality; corrective composition pass (2026-10-22)

**Grounded screenshot audit:** At 2048×1152, the wide switch was selected. The actual preview had two treatments of one engraving (blurred/blue tinted background and sharper inset crop); THE GATE. white serif was imposed on a crowded central image without safe zone; large empty grey surroundings narrowed the page to roughly half the screenshot; small dense Contents and low-legibility provenance followed a disproportionately large cover phrase. Reject this candidate snapshot: publication character and reader hierarchy are not resolved by different hero aspect ratios alone.

**Corrective implementation in existing single comparison HTML:** one img per hero with source/provenance separated; geometry-only experiment spans viewport; true square uses image as a distinct witness opposite live Bodoni/Chiron; wide places text below a genuine 1.95:1 plate; full-bleed uses one image and explicit ink contrast overlay; two non-square variants retain a small 1:1 dossier/issue marker rather than duplicating image. All variants retain one canonical TOC and original prose; introductory display uses first actual source sentence and avoids duplicating it in the following paragraph. No original homepage film, P2 production, Design OS palette, source image, masthead or scroll-motion code changed.

**Review status:** CODED correction, awaits visual inspection at desktop/tablet/phone and 200% zoom; no award score assigned. **NOT VISUALLY APPROVED / DO NOT MERGE.**


## Explicit award-quality loop / actual browser evidence (2026-10-22)

Read and applied **the existing** Design OS Editorial Manual §6A, §4, §5 and the repo's \`new-westside-editorial-web/SKILL.md\` plus \`references/visual-grammar.md\`. This is not a second scoring system: Awwwards Design 40%, Usability 30%, Creativity 20%, Content 10%; Webby overall experience/navigation/functionality/content; FWA conceptually original, functional digital interaction. Westside's own 10 × 0–2 rubric remains a *creative* internal release screen (18/20 minimum, no 0/block), not an official award prediction.

**Prevent CI-green/visually-unknown promotion:** the **existing** First Look Branch Preview workflow now captures *Chromium-rendered* proof of square, wide and full-bleed studies at desktop 1648×928, tablet 768×1024, phone 390×844, and a desktop 824×928 effective-width zoom proxy. Its new **supporting script** \`scripts/capture_p2_magazine_geometry_review.cjs\` checks actual browser asset decodes, source, manuscript excerpt, four movements/twelve sections, image geometry, typography legibility, horizontal overflow, meaningful square folio link and picture/type collisions on bounded layouts. Results include 12 full-page PNGs and \`manifest.json\` in the run's \`p2-magazine-art-direction-evidence\` artifact; objective failures are CI-blocking. This is **not** an additional workflow or a new OS; the prior Preview workflow and design authority stay intact. 824 CSS pixels is **not actual browser 200% zoom**, which remains a separate required manual check.

The retained 1:1 dossier number on non-square states now **navigates to the real Contents by keyboard**, instead of being an inert visual badge. The square-image composition itself is not mandated for all pages. True thumbnail character, art-direction novelty, image-subject crop, body rhythm, mobile gestalt and creative scoring require human eyes on the screenshots. Without that, \`NOT VISUALLY APPROVED / DO NOT MERGE\`. Each iteration records exact defect, owner and correction, then recaptures before another candidate is considered.


## Actual first Chromium screenshot artifact critique (2026-10-22, run 39749248702)

**12 real Playwright PNGs were captured** at 1648×928, 768×1024, 390×844 and 824×928 width-equivalent. Available as \`p2-magazine-art-direction-evidence\` [Actions artifact, run 39749248702](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/39749248702/artifacts/12413251284). Structural audit: 11/12 passed, one desktop-wide \`WIDE_RATIO\` failure; at 1648px the declared 1.95:1 image actually rendered **1450×631 = 2.298:1**, because \`max-height:68svh\` distorted the figure box. The 200%-width proxy is NOT real browser zoom. Actual designer-reviewed PNGs additionally revealed a **BLOCK not caught by the script**: desktop full-bleed rendered the picture only in the left grid tracks (image box **709×761**), with a large flat empty navy right side; the absolute-positioned image retained the grid-column:1/span6 placement from the generic hero image rule. Earlier claims of "full-bleed" were visually false.

**Single corrective pass:** preserve the intended wide 1.95:1 figure by removing the competing max-height rather than weakening test tolerance; for full-bleed, restore the hero itself as the absolute image containing block by resetting the inherited grid placement. Strengthen Chromium gate with **FULL_BLEED_NOT_FULL_WIDTH_HEIGHT** actual DOM extent check at desktop/tablet layouts. A reader viewport screenshot and static build alone had not proven this. The square candidate was structurally sound (709×709 source at 1648px) but still has a comparatively generic left-image/right-title silhouette; mark **IMPORTANT original art-direction distinction** rather than pretending it meets the existing §6A 18/20 bar. Contents remained 12 entries, font approximately 17.3px desktop / 15px tablet / 16px phone, with no horizontal overflow, and both masthead and source image decoded across all 12 states.

**Mandatory next visual review:** repeat 12 screenshots after correction, verify full image really spans all hero content (not an empty color field), preserve the original source crop, then further art-direct the square signature without forcing rectangular and full media into the same composition. No global Design OS edits, no original film or production P2 asset changes. **NOT AWARD-APPROVED / DO NOT MERGE.**


## Award-quality editorial iteration: visible square focal link and clean publication view (2026-10-22)

Invoked the existing New Westside Editorial Web skill and referenced Design OS §6A, §6D. Following actual browser captures (12 states), the square image/right-side serif arrangement is still a generic editorial silhouette, not demonstrated award-level concept distinction. A studio toolbar and testing paragraphs visually precede/follow the issue, which is helpful for QA but obscures the actual publication experience. The reviewer must not confuse the 12 structural checks with artistic acceptance.

Corrective hypothesis in the **same** isolated studio: the actual 1:1 archival image houses a functional, keyboard-focusable square dossier link **03** leading to its true four-movement Contents, while the documentary marginal WATCH axis gives the square image an editorial coordinate; the same link on wide/full remains functional. The full-bleed dark scrim is placed inside the figure so it cannot cover the functional dossier link. \`?view=geometry&shape=square&presentation=1\` hides QA toolbar and debug footer to judge the actual publication; remove \`presentation=1\` to retain the comparison UI and keyboard shape controls. All original editorial copy, original masthead, image, homepage video and live P2 runtime remain unchanged.

**Still BLOCKED on quality** until clean presentation-mode screenshots, visual critique of square link placement and genuine 200% zoom, with no award score or merge claim. Awwwards/Webby/FWA aspirations do not constitute an objective score.


## Independent concept candidate: THRESHOLD / city gate as editorial aperture (2026-10-22)

Actual clean publication screenshot after the square-dossier revision showed: 14 real-browser checks passed, including the functional 03 link and no horizontal overflow, but the left-square/right-headline composition still looked interchangeable with competent ordinary editorial web design. **Reject its creative-distinction release claim**; improved functionality ≠ award-grade originality. The new hypothesis \`?view=issue&presentation=1\` therefore is an **independent semantic cover + contents DOM** in the existing isolated studio, rather than another CSS variant of \`geometry()\` — consistent with \`new-westside-editorial-web/SKILL.md\`. It uses the historical gate as an opening/threshold image, a large typographic layer on paper which the square picture may partially mask, a strong Chinese 900 article title, genuine manuscript text and the full canonical four-movement Contents. Ink/paper register, no duplicated image, no extra visual authority or global token. Square folio 03 is a link to the actual Contents; reading and source remain available. This candidate is deliberately **unapproved until real-browser screenshots** demonstrate legibility, safe occlusion and a more distinctive thumbnail.

Keep existing A/B/C and shape comparison, source homepage movie, P2 ocean/door scene, source photo and official masthead unchanged. Do not interpret independent concept as selected magazine direction. **NOT VISUALLY APPROVED / DO NOT MERGE**.


## Real-browser THRESHOLD art-direction self-critique (2026-10-22) — 17/20, NOT APPROVED

Evidence: [First Look Preview 39752360939](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/39752360939), artifact **p2-magazine-art-direction-evidence**. Sixteen real Chromium screenshot states include \`threshold-desktop.png\` 1648×928 and \`threshold-phone.png\` 390×844. All objective browser gates succeeded: authentic source image decodes; 1:1 frame, official masthead, full 12-desk/four-movement Contents, provenance, no horizontal overflow, hidden studio controls and keyboard-operable 03→Contents anchor. 8/8 engineering workflows succeeded. These are technical and UX evidence, not award judging.

The independent THRESHOLD cover is an improvement on the ordinary left-image/right-title geometry: a giant Roman Bodoni meets one historically grounded square image, a functional 03 folio, original Chinese 900 title and substantial real editorial text. Nonetheless the image and type remain largely adjacent, rather than becoming a visually inseparable original threshold; **creative distinction remains IMPORTANT**, and its static navigation alone is not a genuinely expressive interaction. The phone version is readable and ordered, but actual browser 200% zoom and full assistive-tech testing are **NOT VERIFIED**.

Provisional **Westside internal** 10×2 rubric based on the cited real screenshots, **not** official jury marks: meaning 2, subject 2, composition distinction 1, typography 2, two-ink 2, hierarchy 2, meaningful interaction 1, mobile 2, accessibility 1, editability 2 = **17/20**, **below the §6A 18/20 release objective**. No fabricated pass and **DO NOT MERGE**. The rendered Chinese publication title is also promoted to a true semantic \`h1\` (CSS preserved); the studio's hidden comparison heading was insufficient as publication semantics. Further concept work needs a more authored *image-to-letter* encounter or a narrative threshold interaction **without obscuring the authentic picture, breaking Contents or adding arbitrary effects**. Original homepage film, P2 animation and Design OS tokens remain unchanged.


### Specific visual experiment after 17/20 rejection — the square frame meets the letter (2026-10-22)

The first THRESHOLD screenshot still resembled an adjacent type block + square picture. The next *single-variable art-direction test* enlarges the actual **single 1:1** archival image from 48vw/max760 to **51vw/max820** and grows the desktop hero vertically (97svh) to avoid cutting the added photo. This deliberately moves the picture left toward the terminating E of the giant Bodoni GATE, creating a *subject-specific threshold between type and image*, with the engraved image **in front of** any crossing letter strokes (no white words on dense figures). Mobile/tablet rules and the real Contents remain unchanged. This remains a hypothesis, not an award-score improvement, until verified new desktop + phone PNGs prove the source remains visible and the English title legible. **NOT APPROVED / DO NOT MERGE.**


### Visual rejection of the enlarged square-photo crop (2026-10-22)

[Real Chromium evidence, run 39753556781](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/39753556781): 16 objective structural/keyboard checks passed and 8/8 workflows succeeded. But **threshold-desktop.png at 1648×928 visually showed the larger 51vw/820px square covering the final portion of the important Roman Bodoni word GATE**, despite all geometry and asset tests passing. This is an **art-direction BLOCK**: increased visual contact does **not** justify losing a primary heading's visible word. Reject that larger-photo iteration and restore the earlier 48vw/max760 with 88svh hero. The separate THRESHOLD semantic page, accessible folio-to-Contents jump, preserved original artwork, responsive reading, complete Contents and semantic Chinese h1 remain. No fabricated 18/20 result. Next direction must achieve distinctive image/type interplay by composition and editorial reasoning without hiding words, and needs actual screenshots again before promotion. **DO NOT MERGE.**


## Magazine design-book Doré exploration / manual-first reset (2026-10-22)

**User direction:** Stop premature pixel/detail iterations. The first task is to build a **complete, source-based, operational Westside Watch editorial specification book**. Start with genuine magazine-design book research that teaches *how a concept becomes an actual composition and technical specification*, not an endless parade of small visual changes.

This round adds **§6E** directly to the **single existing Design OS Editorial Manual**, with B01–B11 evidence sources (publisher-author contents verified, no unlicensed book replication), a precise provenance/approval vocabulary, a magazine master-page role map, bounded grid/crop/type-reading hypotheses, actual longform / captions / notes / scripture / Contents contracts, accessible editor workflow and measurable 1648/768/390/320/200%-zoom evaluation. It contains an explicit path to later complete brand art direction, Doré artwork grammar and printed/digital responsive production. [TRIAL] measurements are **not new globally approved tokens**.

**Scope:** Documentation and project skill routing ONLY; no CSS/JS/site/preview layout/CI/font-token/homepage/film/P2-motion changes. Earlier THRESHOLD and geometry prototypes remain evidence of partial work, not selected art direction. **Magazine identity NOT ESTABLISHED; 18/20 QUALITY NOT CONFIRMED; DO NOT MERGE pending actual visual and editorial approval.**


## Doré editorial-manual R2 — 17 magazines and complete specification-sheet inventory (2026-10-22)

The user requests 12+ classic-modern magazine standards-book research, emphasising how style is built from exact observable detail and how to write a full operational Westside manual. This round expands the existing unified Design OS Manual §6E with **17 documented publication case studies** (M01–M17), specific evidence links, editing frameworks, micro typographic/graphic decisions, Westside translations, rejection and source limitations; cross-case editorial grammar comparison, **32 mandatory detailed production sheets S01–S32**, Doré ink/subject/crop methodology, five concrete cross-magazine design dilemmas and the award-calibre verification gate. These are reconstructed method notes, **not 17 proprietary official brand PDFs**. No site assets, original Homepage movie, P2 animation, global tokens or styles changed. Research does not establish award-ready Westside art direction. **DO NOT MERGE.**


## User art-direction rejection — Monocle (2026-10-22)

**Decision:** MONOCLE / M09 = REJECTED as an aesthetic, grid, layout, and typographic precedent for Westside Watch Magazine: the overall editorial composition is not sufficiently contemporary for the sought classical × modern identity. The §6E source case remains a documented *negative research example*; all positive references to M09 have been removed from the recommendation synthesis and detailed micro-lessons. The separate requirement for a 32-sheet comprehensive design book is Westside's own governance decision, not an adoption of Monocle's layout. Screening count now **17 magazines researched / 16 eligible comparative references / 1 formally rejected**. No actual design/asset/runtime changes. PR still unapproved; **DO NOT MERGE**.


## Doré original-plate forensic atlas R3 — six source-authenticated artworks / rights gating (2026-10-22)

**User's next manual workstream:** depth research into the actual engraved source, not micro-decoration or more layout thumbnails. Updated existing single Design OS Editorial Manual **§6E.23–27** with six verified Doré works: (D01) Abraham Gen22 original IIIF, (D02) Babel tower, (D03) Jerusalem mourning / Lamentations, (D04) Moses found / Nile, (D05) Red Sea / Exod14, (D06) *Over London-by Rail* / 1872 urban plate. Commons, Emory, Science Museum, London Museum and University Utpictura scholarly records show artist/period/event and relevant image rights/engraver provenance. One genuine original Doré image has an existing IIIF manifest in repo; the original source identity for current site's *home-opening-engraving.jpg* is NOT attested by its GitHub file listing. No misattribution to Doré or claim to six newly imported local art files.

**Delivered handbook method:** per-plate subject/illumination/engraving density/depth observations, safe crop tradeoffs, facts-vs-inferences, original-raster/credit/rights checklist, exact square-crop loss of **19.45–20.71%** of height for four documented 1866 portrait image dimensions, six editorial translation grammar candidates (witness / threshold / city / crowd / light / source), and BLOCK-level award/reader/performance gates. London Museum hosted image may require a license; its object records are research references, not media import authorization. All normalized subject polygon coordinates remain OPEN until original image pixels are available and actually inspected.

**Scope:** edits are to existing Manual, skill routing and PR review only, no artwork replacement, visual OS token, HTML/CSS/JS, cover, church motion or homepage movie. This is **source research and manual progression**, NOT actual completed 6-image crop review, artistically approved Westside identity, or an 18/20 production pass. **DO NOT MERGE** until creative direction approved.


## R4 source-image geometry and bilingual type-safe design research (2026-10-22)

Next **handbook-first** research after R3: operationalize subject-safe cropping / typography rather than continuing the THRESHOLD polish. The single Design OS Editorial Manual §6E.28–§6E.28 R4.8 now specifies:
- Proof ladder separating art-record, 500×630 Commons preview, 512-square search thumbnail, acquired full raster, and genuine live-browser evidence; corrects the overconfident Genesis 22 “earlier journey” moment description by retaining actual visible wood/staff details and not inventing knife/ram/angel.
- Reversible formula for \`object-fit:cover\` / fractional \`object-position\`, reference JS and source-space/normalized box math. D01 real source (2303×2904) center-square discards 20.70% of original image, 1.95:1 wide discards 59.33%; **math verified, artistic subject safety NOT verified**.
- Four research masking layers (protected person/objects, compositional axes, hatch/brightness, inscriptions), mandatory subject preservation & text safe-zone tests, open normalized polygon data rather than invented precision.
- Existing Bodoni Roman/Italic/SC and Chiron 900/200/400 role-specific title behavior, real contrast, captions, a source manifest specimen with unfilled unavailable evidence, full 1648/768/390/320/200%-zoom acceptance matrix, and step-by-step design review.
- [Method reference] CSS Images 3, MDN object-fit/object-position, W3C CLREQ and WCAG 2.2. **No artwork raster acquired through this research connector**, no falsely precise image-density zones; only documentation and skill routing changed.

**Explicit scope:** 3 Markdown files, no new token authority, no production HTML/CSS/JS, film, P2 or artwork changes. Creative identity remains unselected; **DO NOT MERGE** until full verified layout and §6A gate.


## R5 design-research correction — continuous DIGITAL SPREAD, not only picture crop (2026-10-22)

**User clarification:** The magazine's proper design scale is a **whole continuous digital spread** inspired by a physical double-page layout, **freed from paper binding, mid-gutter loss, fixed trim, print advertisements or opposite-page restrictions**. A square may physically/visually straddle the two virtual editorial regions **50/50 or 30/70**, or act as a live-type/negative-space/cut-through field with no image crop at all. Another possible “30/70” means two unequal areas of the entire spread; the two meanings must not be confused. Previous R3/R4 picture-crop emphasis was necessary for faithful historical artwork but far too narrow to define publication art direction.

**Documentation action:** Added **§6E.29–31** within the one existing Westside Design OS Editorial Manual; corrected priority order in §6E.4 and explicitly demoted R4 crop math to an image-only specialization. R5 documents print vs digital constraints, one continuous canvas, mathematically defined cross-axis square examples (W1440 S560; 50/50 x=440–1000, 30/70 x=552–1112), 7 square roles beyond cropping, a five-layer compositional grammar, scoped manual-only CSS specimen, desktop/tablet/mobile recomposition, same-content comparative art-direction gates and mapping to existing **S04/S06/S07/S08/S09–S10/S19–S22/S29–S31** specification sheets. Source method grounded in original WoI redesign, Pentagram Citizen/No Man's Land and MDN Grid/translate/webby criteria; we do not claim these are official Westside proportions.

**Scope:** only existing Manual, new-westside-editorial-web project skill, and PR review. **NO production layout, CSS, JS, images, protected homepage film, motion or tokens edited**. The square is an occasional identity instrument, not a forced page template. The magazine's full art direction still **NOT APPROVED**, not 18/20; **DO NOT MERGE** just because documentation/CI passes.
