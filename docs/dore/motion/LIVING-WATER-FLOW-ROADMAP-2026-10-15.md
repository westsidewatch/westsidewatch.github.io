# Living Water Flow — Phase 1

Status: RESEARCH / NOT DEPLOYED
Date: 2026-10-15

## Goal
Turn the approved second-page v2 vertical breathing water into visibly directional, continuous flow without sacrificing its approved composition. This is the sole current deliverable; acceptance precedes deployment.

## Protected baseline
- Approved second-page file: `static/experiments/sevenfold-first-to-second.html`
- Approved baseline commit: `c489901abec92e62f9c4ab33963d8bb5ce01a566`; restored and confirmed at `d88712db9728b1b54ba66a143f920431beb24c96`.
- Original v10 SVG: `static/experiments/assets/living-water-contour-engraving-v10.svg` (read-only).
- Never modify the approved v2 or original asset during exploratory iterations.

## Experiments (not approved replacements)
- `static/experiments/living-water-continuous-field-lab.html` — original twisting/flow experiment, surprising pseudo-3D appearance.
- `static/experiments/engraving-surface-seamless-sea-lab.html` — interpolation bridges; visually reported as 2D twitching; not accepted.
- `static/experiments/living-water-overlap-surface-3d-lab.html` — dual overlapping surface attempt; not accepted.

## Phase 1 execution
1. Copy approved v2 into an isolated flow lab; preserve vertical breathing.
2. Add coherent directional wave propagation with small deformation; do not replace original geometry or introduce hard splits, seams, clipping, white borders, or cloth-like twisting.
3. Visually compare at multiple animation times and screen sizes, check reduced-motion behavior and performance.
4. Only after acceptance, integrate in one controlled change and deploy.

## Lessons
Splitting at y=450 created a visible seam; dashed strokes broke engraving continuity; over-strong local deformation produced cloth-like motion; careless restoration caused white borders or frozen animation. Do not confuse code commit, deployed preview, and visual acceptance.

## Next stages
Phase 2: Engraving Ocean 3D. Phase 3: general engraved 3D surfaces. Phase 4: cinematic engine, future only. Do not expand Phase 1 scope.
