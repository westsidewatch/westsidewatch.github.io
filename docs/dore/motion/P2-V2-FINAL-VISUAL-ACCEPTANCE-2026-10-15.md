# P2 v2 — Final Visual Acceptance

Date: 2026-10-15
Status: **VISUALLY ACCEPTED / PARAMETER EXPLORATION CLOSED**

## Accepted candidate

- Preview: https://pr-1328.westsidewatch-github-io.pages.dev/experiments/p2-v2-fixed-ocean-25-20261015.html
- Experiment source: `static/experiments/p2-v2-fixed-ocean-25-20261015.html` on `experiment/living-water-direction-field-preview-20261015`
- Accepted source revision: `78ebf54c594ec324dc9716dc824c069f7d761eec`
- Source engraving: `static/experiments/assets/living-water-contour-engraving-v10.svg` (620 paths)

## Frozen motion parameters

| Parameter | Value |
| --- | --- |
| Direction propagation | 1.5× |
| Speed gradient | 2.0× |
| Local amplitude | 6.0px |
| Hatching density strength | 2.5 |

## Accepted behavior

- Continuous automatic wave motion, with no manual parameter or animation-time controls.
- Preserve original 620 engraved paths and the intentional central open passage.
- Preserve breathing rhythm and ocean-like dimensionality.
- Do not replace engraving-based tone with opacity or brightness animation.
- The approved candidate is a pseudo-3D ocean field, **not** a true river-advection solver.

## Scope and change control

The user approved the Fixed Ocean 2.5 preview and closed P2 v2 tuning. Do not continue parameter experiments, change the visual language, or replace this candidate without a new explicit request.

This acceptance records the preview result. It does **not** assert that the candidate has been integrated into the production First Look/P2 page, merged from PR #1328, or independently verified in production. Any future integration must isolate the accepted P2 files rather than merge the entire experimental PR.
