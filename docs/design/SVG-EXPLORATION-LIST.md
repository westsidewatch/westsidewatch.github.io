# SVG Exploration — Doré Research List

Status: research evidence and implementation candidates under the **single Westside Design OS**. Not a separate visual authority or CI. Updated: 2026-10-17.

## Scope and preservation

The P2 Living Water V75 engraved ocean, rising water and Red Sea door are protected visual assets. Preserve their approved geometry, animation appearance, seven programme rows, page typography, and existing Design OS authority. No automatic library migration, canvas rewrite, global CSS changes, or merge without visual and CI acceptance.

## SVG research list

| ID | Source / mature precedent | Finding | Applicability to P2 | Decision |
| --- | --- | --- | --- | --- |
| SVG-01 | [Chromium: hardware-accelerated animations](https://developer.chrome.com/blog/hardware-accelerated-animations) | SVG transforms and opacity can be composited where eligible; changing SVG path geometry is not automatically compositor-only. | Separate door translation/opacity from the live engraving geometry. | **Study and measure** |
| SVG-02 | [svg-dom: performance patterns](https://github.com/ChrisWhealy/svg-dom/blob/main/docs/design_notes/performance.md) | Reuse scratch buffers, avoid redundant attribute writes, coalesce high-frequency events. | Optimize the per-frame path-string construction and DOM writes in `p2-water-surface.js`. | **Preferred dependency-free pattern** |
| SVG-03 | [Chromium Issue 393260698](https://issues.chromium.org/issues/393260698) | Excess compositor eligibility checks for clip-path animations have been reported. Not evidence that this particular site hits that bug. | Isolate the dynamic `clipPath` update in A/B profiling. | **Investigate, not assumed root cause** |
| SVG-04 | [Chromium SVG animation implementation study](https://nothing.graphics/docs/wg/research/chromium/svg/animation-and-smil) | SVG compositor eligibility depends on target and animation type; direct attribute mutations remain different from compositor transform animation. | Avoid blanket claim that all SVG animation is GPU-accelerated. | **Architecture reference** |
| SVG-05 | [SVG.js](https://github.com/svgdotjs/svg.js) | Established SVG animation/timeline library. | Only consider if existing single RAF cannot be maintained; a library does not eliminate path rasterization. | **Defer dependency** |
| SVG-06 | [Motion](https://motion.dev/docs/animate) | Modern animation interface with small-footprint options and native animation support. | Optional for door transform/opacity; not a fix for live `d` updates. | **Defer dependency** |
| SVG-07 | [Flubber](https://github.com/veltman/flubber) | Path morph interpolation. | Different problem from continuous flowing engraved contours. | **Not selected** |
| SVG-08 | [SVGO](https://github.com/svg/svgo) | Mature MIT-licensed SVG optimizer. | Offline analysis of static source only; protect geometry and compare visuals before any optimization. | **Candidate for static asset audit only** |
| SVG-09 | [Awesome SVG](https://github.com/willianjusten/awesome-svg) | Curated open-source SVG reference list, including animation, masks and optimization. | Discovery index, not a production dependency. | **Reference index** |
| SVG-10 | [Chrome DevTools Performance](https://developer.chrome.com/docs/devtools/performance/) | Frame timeline, paint/composite analysis, scripting and rendering attribution. | Compare P2 opening at `vh=1.72`, same viewport and scroll route. | **Required evidence** |

## Current P2 code evidence (2026-10-17)

- `static/js/p2-water-surface.js`: on each water frame, constructs fresh SVG `d` strings and calls `setAttribute('d', ...)` across the animated contour collection; also updates accents and hatch marks.
- `static/js/p2-living-water.js`: computes a 65-point wave and updates `clipPath`, door `transform`, layer visibility and the editorial scene; door visibility switches at `vh >= 1.72`.
- Existing `bc07301` stops the live-water paint call after `vh >= 2.37`, but does **not** demonstrate that the `vh=1.72` handoff is smooth.
- This is a source-code diagnosis, **not a measured performance trace**. Do not label SVG repaint or CSS pollution as the proven root cause.

## Reproducible diagnosis list

- [ ] Capture a baseline Performance trace around `vh=1.72`, including main-thread scripting, style, paint, raster and compositing; log long frames and memory/GC.
- [ ] A/B 1: pause `wsP2Water.paint` during the opening interval, leaving door and masks active.
- [ ] A/B 2: keep the live engraving, freeze only the wave `clipPath` updates.
- [ ] A/B 3: keep engraving and mask, defer the right editorial visibility switch by one frame (test only, never ship without visual approval).
- [ ] Compare SVG path update counts, total `waterPaintMs`, slowest frame, scroll continuity and appearance.
- [ ] Apply the smallest measured fix, prefer allocation/write avoidance before dependencies or rendering-engine replacement.
- [ ] Verify desktop/mobile, viewport height and zoom, Chrome/Firefox where possible, reduced motion, door appearance, and existing Design OS/CI acceptance.

## Release boundary

Research notes may be committed independently. No production animation change is authorized by this list. Do not create a separate Design OS, a new CI check, or an unrelated design system.

## P2 isolation implementation (2026-10-17)

Commit `6de1ac1` adds **opt-in** `?p2perf=` modes to `static/js/p2-living-water.js`:
- `water-off`: omit `wsP2Water.paint()`; isolate animated SVG path updates.
- `clip-off`: omit scene cover/tint/sea clip-path writes; deliberately changes the test rendering only.
- `editorial-off`: hide editorial pane while keeping door choreography.
- `trace`: expose `window.wsP2Perf` (frame count, frame intervals over 32 ms, maximum frame interval, accumulated water and scene JS execution time); log periodically.

Use the same browser, viewport, zoom and scroll path for all four. `wsP2Perf.longFrames` counts inter-frame intervals, **not** a Chrome Performance trace or an attribution of dropped frames; use DevTools Performance for scripting/paint/composite evidence. `water-off` and `clip-off` are diagnostic only and are not approved visual alternatives. Default mode remains unchanged. Results not yet captured; no root cause or fix claimed.

## Four-mode browser audit page (2026-10-17)

Commit `e759d2e` adds `static/p2/performance-audit.html`. Open `/p2/performance-audit.html` on the **same-origin deployed preview**, click **Run four modes**, then export JSON. It loads the existing P2 page as an embedded frame and drives the existing `westside-p2-scroll` message protocol through the opening interval (scene progress 1.30–2.45, crossing the critical 1.72 threshold). It compares `trace`, `water-off`, `clip-off` and `editorial-off` under one viewport.

**Limitations:** RAF intervals and JavaScript execution times are only first-pass screening; browser painting/compositing and garbage collection require DevTools Performance trace. Results can be affected by iframe, machine load and browser throttling. The diagnostic page has not yet been run against the deployed site in this environment because the preview host was not reachable. No performance improvement is claimed. Normal page behavior remains unchanged.
