# P1 — Living Current Native

Status: implementation prototype, not production architecture.

## Goal

Prove that the first New Westside 8:5 Living Current can be built with zero new motion runtime dependencies.

## Implementation

Prototype route:

`/dore-design/prototypes/p1-living-current-native/`

Files:

- `static/dore-design/prototypes/p1-living-current-native/index.html`
- `static/dore-design/prototypes/p1-living-current-native/styles.css`

Runtime dependency count: **0**.

Uses only:

- semantic HTML;
- CSS Grid;
- horizontal overflow;
- CSS scroll snap;
- `aspect-ratio: 8 / 5`;
- focus-visible styling;
- responsive media queries;
- `prefers-reduced-motion` fallback.

## What P1 is testing

1. One shared 8:5 spatial grammar can host visibly different editorial identities.
2. Horizontal Living Current interaction does not require Lenis, GSAP, Motion or a carousel library.
3. Mobile can show one dominant cover plus a visible next-cover edge without trapping vertical page scroll.
4. Native browser scrolling remains keyboard/focus reachable.
5. Reduced motion can preserve content/IA without a parallel implementation.

## P1 acceptance gates

- [x] zero new animation runtime dependencies;
- [x] canonical HTML content exists without JavaScript;
- [x] 8:5 geometry is structural, not image-specific;
- [x] desktop horizontal browsing works through native overflow;
- [x] mobile horizontal browsing uses the same content model;
- [x] viewport is focusable;
- [x] visible focus state;
- [x] reduced-motion path removes snap/transform enhancement;
- [x] no SPA conversion;
- [x] no scroll hijacking;
- [x] prototype isolated from production homepage.

## Deliberately not solved in P1

- viewport conductor / lead-current state;
- semantic current speeds;
- cover-to-opening object continuity;
- View Transitions;
- Motion/GSAP/Lenis bakeoff;
- Scripture Cinema cinematic transitions;
- final art direction/assets.

Those belong to P2+.

## Decision after P1

Native browser primitives are sufficient for the base Living Current structure. Do **not** admit a motion dependency for this problem unless later visual/hardware acceptance demonstrates a concrete failure.
