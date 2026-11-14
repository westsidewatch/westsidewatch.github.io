# Scripture Studio V30 — 07 mother-form layout QA (2026-11-11)

**Source:** `static/experiments/scripture-studio-motherform-v30-07-ink.html` on `draft/p2-0104-olive-entry-20261105`.

## Verified in isolated Chromium structural test

- Native editable HTML / CSS / JS; no generated image used as design source.
- Seven mixed-language strips; four strips contain three or more alternating passages. Unlike V29, strips may begin in English or Chinese, and signatures are deliberately nonrepetitive.
- Six strips have deliberately asymmetrical Chinese/English passage lengths in the selected offline fallback-only test.
- 31,095 legal candidate combinations were ranked after filtering out violations of the majority-asymmetry rule. The number may change with real font metrics.
- Exact Traditional Chinese and English KJV strings reconstruct from the displayed mother-form tokens with no deletion, reordering within each language, or case conversion in source data.
- Two compositions use identical token runs and positions; second print rotates the mother forme 90 degrees. Chinese weight changes from 900 to 200 on reverse reading, English remains actual Bodoni Moda SC 400, `smcp=1`, `c2sc=0`.
- No uncaught browser JavaScript exceptions in the isolated test.
- In offline fallback-only diagnostic, one ranked arrangement had a bounding box aspect ratio of ~0.746; **this is not real-font or ink-pixel acceptance**.

## Acceptance limits

- Browser will not show artwork if the actual Bodoni Moda SC and Chiron webfont faces (900/200) have not loaded. The source is `static/fonts/scripture-studio/BodoniModaSC-VF.ttf` committed in prior V29.4.
- This offline environment did not load either font. The simulated layout was used only for automated structural verification, not presented as a final design preview.
- CSS bounding box ≠ actual ink contour. Real ink-density and print-polish not yet passed. Soft secondary poetic breaks remain provisional editorial candidates until reviewed.
- Cloudflare URL has not been independently verified as deployed after this commit; the GitHub source is committed and verified.
- The V30 browser must be opened from the same deployment that serves `static/fonts/scripture-studio/BodoniModaSC-VF.ttf`; downloading HTML alone loses its relative font dependency.

## Next acceptance gate

Run the V30 link in a networked browser and verify that all three font checks pass. Inspect the two reading orientations at 390, 768 and desktop widths. Then use real glyph-ink pixels/contours, not text-box percentages, to refine the square seal density. Do not merge to production P2 until art-direction approval.