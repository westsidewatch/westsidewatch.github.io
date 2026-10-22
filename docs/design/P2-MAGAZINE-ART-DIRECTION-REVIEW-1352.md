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
