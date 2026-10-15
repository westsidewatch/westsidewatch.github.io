# Living Water — Motion Engraving v1 Checkpoint

Status: **user visually confirmed initial motion works** (2026-10-15). Preserve this checkpoint before further updates.

## Approved baseline
- Static engraving: `static/experiments/assets/living-water-contour-engraving-v10.svg`. Do not edit or replace v10.
- Official second screen: `static/experiments/sevenfold-first-to-second.html`; still uses static v10, not the animation.
- Motion experiment: `static/experiments/living-water-motion-study.html`.
- Preview: https://pr-1325.westsidewatch-github-io.pages.dev/experiments/living-water-motion-study.html
- PR: https://github.com/westsidewatch/westsidewatch.github.io/pull/1325
- Motion implementation commit: `bb724cc6e943d2912a356bac316ba3e5dc03fd71`.
- Preview workflow repair commit: `540e532c338fdb00cf3553555d68fec9a6c069b5`.
- CI: Church Editorial Branch Preview and Production Build passed on workflow repair commit; Core Contract failed independently.

## v1 implementation
- Preserve static v10 SVG as the underlying image; add a transparent SVG overlay.
- 24 new short paths derived from existing contours: 12 upper, 12 lower.
- Staggered individual phases and lifetimes; upper nominal 32 s, lower nominal 19 s, with individual variation.
- Growth and disappearance implemented with SVG stroke dash controls; modes subtle / balanced / visible, growth toggle, pause, intersection visibility and reduced-motion preference.
- Earlier motion layer also animates selected original contour clones with subtle opacity/translation.
- User confirmed: **「有動，初步成功」**. This confirms initial visible motion, not final visual quality.

## Design constraints
- Guiding idea: **活水不停歇** — continuous overlapping birth and disappearance, no whole-field synchronized restart.
- Distance: water flow; middle: tonal relief; close: engraved hatching.
- Keep full-bleed upper and lower flow, central scripture-safe negative space, no boxed image or masking, no figures, no AI-generated imagery.
- Upper slower and calmer; lower somewhat faster. Avoid obvious path-drawing or artificial ridges.

## Future update, NOT YET IMPLEMENTED
1. Improve curve-tangent growth rather than horizontal translation.
2. Generate new hatches based on real contour geometry, local direction and density constraints; protect central negative space.
3. Add natural overlap and smooth decay with bounded stroke count and performance tests.
4. Test visuals and reduced-motion behavior in isolated preview before any official-page integration.
5. Keep this v1 checkpoint intact for comparison/rollback; do not replace baseline assets.

## Deployment guard
The preview workflow must check the approved **v10** filename and the motion-study page. The earlier stale v6 assertion caused preview failure and stale First Look routing. Never claim live deployment until the workflow succeeds.
