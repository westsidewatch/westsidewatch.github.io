# Scripture Studio V25 — 07 composition search / honest acceptance record

2026-11-10. Branch: `draft/p2-0104-olive-entry-20261105`. **Not released to P2**.

## Implemented

- Replaced V24 fixed first-choice layout with a **real browser-DOM candidate evaluator**: 12 candidate permutations × three stagger profiles × four column gaps = 144 actual layout probes for the first sample choice, at the selected fixed native font size. The candidate is selected using measured typography geometry and an explicit rhythm profile. No AI imagery; native HTML/CSS and JavaScript.
- Different start offsets among columns, maintaining 07's single interleaved mother forme. The same text source feeds both orientations. Preserves Chinese vertical-rl, Traditional Chinese right-to-left columns, and rotates the entire forme 90 degrees in English-readable view.
- Exact original Chinese and KJV source strings and approved/proposed protected spans preserved; 7 strips, 4 multi-switch, 6 asymmetric. Font roles remain Chiron 900/200, Bodoni Moda SC All Small Caps.
- Removes the prior erroneous **double scale computation** on repeated renders (which caused text clipping) by resetting display scale to 1 for measurement. Centers observed span rectangles inside each print window with individual viewport offsets.
- The UI now differentiates **structure pass** from **actual ink area fail** and font not-verified, instead of claiming a square-layout box is a successful dense letterpress print.

## Chromium acceptance evidence

- 1600px, 768px, 390px local browser previews. 390px/768px show no document horizontal overflow.
- 1600px, 54px selected form: 144 DOM tested candidates, chosen #8, stagger C, gap ~19.4px. Reconstructs Chinese and English source exactly, 4/7 columns multi-switch, 6/7 asymmetric, 900/200 CSS computed, `all-small-caps` computed.
- Browser **font face provenance FAIL**: sandbox cannot load Chiron Hei HK WS or Bodoni Moda SC from remote resources. Fallback does not prove OS stroke shape. Do not call the current preview an official font result.
- Typography bounding box ~90.9% × 90.9% square artboard **is not an ink area ratio**.
- Independently measured screenshot image pixels (local fallback): Chinese visible ink region spans only about **50–51% of plate width** and ~89% height; actual black ink pixels ~**5–6%** of total plate pixels. **FAIL** design target despite large CSS layout box.
- English displayed print likewise has only ~**3.5–4%** white ink pixels in the panel and insufficient cohesive impression mass. This is a genuine improvement in measurement honesty, not an artistic success.

## Structural explanation of the remaining hard obstacle

With 11 Chinese and 9 English editorial phrase units (20 total) and the hard majority of strips requiring at least three alternating language runs, a seven-strip program can form four multi-switch plus three simpler strips. It cannot arbitrarily expand to ten strong bilingual multi-switch columns unless more **semantically legitimate approved** breakpoints are supplied. Raising source type size alone will scale both axes, not fix the ratio; inflating column gutters merely makes the bounding box look full without adding typographic substance.

## Next engineering gate

1. Obtain genuine OS font loading in a networked staging preview. Inspect actual 900/200 variable weight instances, real Bodoni `smcp`/`c2sc` before final ink-shape measurement; do not embed or distribute font binaries in the user artifact.
2. With Scripture editorial approval, refine permitted **poetry-unit** boundaries to allow stronger high-density near-square constructions; do not slice `呼籲耶和華的，` or any other protected clause.
3. Rerun candidate search and compare screenshot ink silhouette/coverage in both languages. The same geometry must work when rotated, with no cropping and meaningful phrase breaks.
4. Only after passing both source structure and optical ink QA may it be called an approved art motherform.