# Sevenfold Dawn Navigation — engineering contract

Status: implementation branch, not production. Source of truth: current main, not PR #1303.
Scope: homepage only. Do not alter chapter screens, realm homepages, global navigation on other pages, or the existing Design OS authority.

## Approved design

Closed: full-screen continuous Film; four homepage visual regions only: menu toggle, existing logo, slogan, bilingual Romans 13:12. Scripture sits independently in the middle region, not adjacent to slogan. Remove homepage-only top-left duplicate WESTSIDE WATCH wordmark.

Open: upper navigation occupies half of desktop viewport; lower half remains the same Film iframe and is visually dedicated to a large existing logo. Upper half contains seven editorial links, slogan top-left, stationary bilingual scripture near bottom-right, toggle top-right.

Motion: one BRAND PLANE containing small logo, slogan, large logo, with fixed internal geometry. Translate this single plane upward: small logo leaves through top, slogan arrives upper-left, large logo rises from below viewport into lower-half center. No cross-layout Flip, no logo shape stretching, no independent logo motion. Seven color folds descend from the top, counter-moving against the brand plane; they settle into a quiet half-screen. Scripture is an independent viewport-anchored unit: same exact position and type metrics in both states, only contrast may change. Menu icon morphs from three ultra-thin strokes to a proportionate Christian cross (not X or generic plus).

Color: map exactly seven current Design OS section colors (church, journal, bible, sermon, books, cinema, life). On each *new complete opening*, rotate/shuffle order so the final stable color varies; avoid immediate repeat where practical. No hard-coded rainbow colors or black-and-gold fallback.

Film: keep the same iframe DOM node mounted and its src unchanged throughout the interaction. No video duplication, hero scale-down, or full-screen dark scrim.

Navigation: preserve all seven existing destinations, search and functional entry points, hover previews and keyboard behavior. Avoid extra visible homepage brand labels and on-page explanation of theological symbolism.

## Verified current-main touchpoints (2026-10-14)

- layouts/partials/watch-home-editorial.html: floating details/summary menu, seven anchor links, hover-preview iframe, extra intro and entries; hero contains another nav, Film iframe, masthead image /images/westside-watch-masthead-landscape.svg, star /images/westside-watch-morning-star.svg, slogan h1, scripture pair .sites-home-scripture-pair, and entry links.
- static/js/first-look-host.js: openCurtain / closeCurtain and ws-scale-reveal-* class toggles currently own the menu; hover previews and anchor scrolling are handled here.
- static/css/westside-design-os.css: typography and color system; read actual tokens before selecting palette.
- Preserve all unrelated site routes and pages.

## Implementation order (single integrated PR)

1. Audit authoritative CSS selectors, active stylesheets, actual brand SVG and seven Design OS section color values. Record screenshot geometry targets before writing styles.
2. Replace only homepage Scale Down Reveal controller with one reversible GSAP master timeline; never layer competing controllers.
3. Build brand plane and calculate a single translateY endpoint at viewport resize. Validate initial and open visibility bounds of small/large logo and slogan; preserve intrinsic logo aspect ratio.
4. Build seven descending folds clipped to upper-half navigation; resolve randomized final layer order before timeline play. Coordinate folds with brand ascent.
5. Keep scripture fixed in viewport coordinates across states, with responsive typography and contrast rules. Layout seven links and hover preview without collisions.
6. Implement accessible SVG toggle, keyboard/escape, focus return, reduced-motion fallback, interrupted/repeated clicks, scroll behavior, and responsive short-viewport mode.
7. Run functional DOM tests and real-browser frame captures at closed, 25%, 50%, 75%, open and reverse states. Inspect visual output; CI green alone is NOT visual acceptance.

## Acceptance gates

- Closed: only the four designated homepage visual regions, with no duplicated top-left wordmark.
- Open desktop: folds fill upper ~50dvh; Film remains visibly continuous below; large logo centered in lower half and dominant.
- One brand-plane transform only, with fixed relative element positions; small logo invisible open, large logo invisible closed.
- Scripture bounding box remains stable across opening/closing; bilingual text remains one block, readable over each of seven final colors.
- Seven distinct OS colors appear per opening; final color can vary between openings; close reverses the active sequence cleanly.
- Same Film iframe element and source throughout; no unintended pause or reload attributable to DOM changes.
- Links, previews, accessibility and mobile layout work.
- Real rendered screenshots reviewed, not merely generated. If screenshots cannot be obtained, explicitly mark visual QA blocked and do not merge.
- No changes to PR #1303. No production merge without verified acceptance.

## External research

Joby Aviation Menu Animation is a visual study reference for layered reveal rhythm, not a codebase to transplant or a dependency. GSAP Core is an optional timeline implementation tool; avoid GSAP Flip, scroll libraries, duplicate animation frameworks and unnecessary third-party packages.
