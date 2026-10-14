# Design OS — precise CSS positioning and geometry verification

**Authority:** one Design OS verification tool; page-specific stylesheets remain the sole owners of static geometry. This is NOT a second positioning CSS system.

## Standard workflow (required for geometry changes)
1. Identify the exact DOM selector, owning stylesheet and breakpoint. Inspect the winning computed style and overridden declarations in browser DevTools; do not add another CSS override as a blind fix.
2. Run `node scripts/design-os-geometry-audit.mjs docs/design-os-geometry.targets.json` against the preview URL. The JSON report records actual CSS-pixel viewport bounding boxes, computed position/transform/size/font, and any violations.
3. Change geometry **only in the existing owning stylesheet**. Keep GSAP motion transforms separate from static layout coordinates. Do not stretch glyphs with scaleX/scaleY.
4. Rerun the same target matrix at desktop, tablet, phone and 4K when relevant. Verify open/closed animation states separately where applicable. Compare screenshots using Playwright `toHaveScreenshot` for stable states.
5. A build passing without measured geometry and screenshot review is not a visual acceptance.

## Configuration
Create `docs/design-os-geometry.targets.json` (sample committed in this branch) and set `pages[].url` to the actual preview deployment, not an assumed live URL. `targets[].expected` may contain `x,y,width,height,right,bottom` in viewport CSS pixels; `tolerancePx` defaults to 2. `withinViewport` checks clipping; `noOverlap` lists pairs of target selectors.

**Measurement != ownership:** `getBoundingClientRect()` includes transforms and reports what the user sees. `getComputedStyle()` identifies the winning computed values, but does not identify the exact source declaration; inspect browser Styles/Computed source links for that. Scroll offsets, fonts, loading, animation state, viewport and zoom must be controlled when comparing runs.

**Compatibility:** no runtime JS or CSS added to public pages; uses existing Playwright test infrastructure when available. Do not merge a feature PR solely on the presence of this tool. A missing browser/test runner must be reported as not tested, not PASS.

## Relevant owners
- Shared typography and colors: `static/css/westside-design-os.css`.
- Sites responsive composition: `static/css/sites-composition-authority.css`.
- Homepage hero geometry: `static/css/westside-home-hero-composition.css`.
- Sevenfold navigation animation: `static/css/sevenfold-dawn.css` and `static/js/first-look-host.js` (must not create a competing static coordinate authority).

References: https://playwright.dev/docs/api/class-locator#locator-bounding-box and https://developer.chrome.com/docs/devtools/css/issues
