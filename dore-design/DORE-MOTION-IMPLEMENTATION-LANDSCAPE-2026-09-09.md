# Doré Motion Implementation Landscape — New Westside

Date: 2026-09-09
Status: IMPLEMENTATION LANDSCAPE — PRE-PROTOTYPE, NOT PRODUCTION AUTHORIZATION

## Purpose

The conceptual exploration phase for New Westside motion is sufficiently mature. This record converts the design language into a minimal implementation map for Storybook/prototype validation.

The website motion language remains intentionally simple. Scripture Cinema cinematic transitions are a separate research/implementation line.

## Verified current site boundary

The current site is a Hugo multi-page site. `layouts/_default/baseof.html` loads a single Hugo-piped `assets/css/main.css`; no existing GSAP, Lenis, Motion, SPA router, or animation runtime is part of the base shell.

Therefore the implementation strategy is:

> browser-native first -> progressive enhancement -> narrow JS only where native primitives fail the design acceptance test.

Do not convert the site into an SPA to obtain motion.

## Mature implementation map

### 1. Spatial base: HTML/CSS/Hugo

Use for:
- 8:5 geometry;
- horizontal/vertical layout;
- sticky spatial framing;
- scroll snapping where editorially appropriate;
- overflow and clipping;
- scale/crop/overlap/z-order;
- typography-led camera feeling;
- reduced-motion baseline.

Default decision: REQUIRED FOUNDATION.

### 2. Viewport leadership: IntersectionObserver + small state machine

Use for:
- identify lead current;
- ambient -> approached -> focused -> reading -> leaving;
- pause/yield neighboring currents;
- defer work for dormant currents;
- transfer foreground attention without continuous polling.

Default decision: PREFERRED.

Do not make requestAnimationFrame the primary viewport detection mechanism.

### 3. Scroll-linked enhancement: CSS Scroll-driven Animations

Use for:
- scroll-progress-linked transforms;
- restrained parallax/scale/crop changes;
- lead-current progress effects;
- horizontal current progress where support exists.

Constraint:
- progressive enhancement only;
- base reading/navigation must remain complete without support;
- use `@supports` guards.

Default decision: PREFERRED WHEN SUPPORTED, NEVER LIFE SUPPORT.

### 4. Cover -> Opening / Return: View Transitions API

Use for:
- 8:5 cover object persistence across Hugo MPA navigation;
- selected cover -> opening field;
- return transition that preserves object identity where browser/session state permits.

Why it fits:
- supports cross-document transitions for MPA sites;
- avoids introducing an SPA router;
- browser owns transition snapshots and interaction lifecycle.

Constraint:
- enhancement only; ordinary links remain canonical fallback;
- `prefers-reduced-motion` must suppress non-essential transition motion;
- test page-state restoration explicitly.

Default decision: FIRST CHOICE FOR COVER CONTINUITY.

### 5. Simple semantic choreography: Motion vanilla — candidate, not dependency yet

Only evaluate if native CSS/View Transitions cannot express a required prototype cleanly.

Potential use:
- small bounded imperative sequences;
- lightweight scroll choreography;
- object transforms whose state logic becomes awkward in CSS alone.

Decision gate:
- must beat native implementation on clarity, maintainability, motion fidelity, or browser consistency;
- otherwise reject dependency.

Default decision: BAKEOFF CANDIDATE, NOT BASELINE.

### 6. Complex choreography: GSAP / Flip — exceptional layer

Use only for:
- genuinely difficult object continuity;
- multi-object FLIP choreography;
- Scripture Cinema chapter/book transitions;
- rare award-calibre sequences that cannot be expressed cleanly with native primitives.

Do not use GSAP merely to smooth ordinary site scrolling.

Default decision: RESERVE FOR HIGH-VALUE CINEMATIC/COMPLEX CASES.

### 7. Smooth-scroll runtime: Lenis — hold out of baseline

Lenis is mature and MIT-licensed, but New Westside does not currently require a global smooth-scroll controller to express the accepted website motion language.

Only admit if real-device prototypes prove that native scrolling cannot achieve the desired tactile continuity or a specific WebGL/cinematic surface requires synchronized scrolling.

Default decision: REJECT FROM BASELINE; REOPEN ONLY ON EVIDENCE.

## Implementation principle

`native CSS/layout` should own structure.
`IntersectionObserver` should own foreground-state detection.
`View Transitions` should own ordinary cross-page cover continuity.
`CSS scroll timelines` should own simple scroll-linked enhancement where supported.
`Motion` should be tested only as a narrow middle layer.
`GSAP/Flip` should remain the exceptional cinematic tool.
`Lenis` should not become site infrastructure without a demonstrated failure case.

## Dependency budget

Prototype baseline must start with ZERO new runtime animation dependencies.

A dependency may be admitted only if:
1. a named prototype fails acceptance with native primitives;
2. the candidate fixes that failure;
3. mobile and reduced-motion behavior remain sound;
4. the dependency does not become the content or navigation model;
5. removal/fallback remains possible.

## Storybook / prototype bakeoff

### P1 — Living Current Native

Goal: one horizontal 8:5 current using only semantic HTML/CSS/native scroll.

Test:
- desktop horizontal browsing;
- mobile translation;
- no JavaScript required for access/navigation;
- visual rhythm remains publication-like, not carousel-like.

Acceptance:
- immersive but obvious;
- no trapped scroll;
- keyboard operable;
- reduced motion unchanged in information architecture.

### P2 — Viewport Conductor Native

Goal: four vertically adjacent currents with different temporal characters.

Implementation:
- IntersectionObserver;
- tiny class/state toggle only;
- no animation library.

Acceptance:
- whole page feels alive;
- only one current commands foreground attention;
- reading state stops autonomous movement;
- no frame-loop detection.

### P3 — Cover -> Opening MPA

Goal: selected 8:5 persists into a Hugo content page.

Implementation order:
1. normal canonical link;
2. cross-document View Transition enhancement;
3. reduced-motion/no-support fallback.

Acceptance:
- visitor feels they entered the cover object;
- no SPA router;
- direct URL load is fully correct;
- back/forward behavior remains understandable.

### P4 — Same motion, native vs Motion vanilla

Goal: test one bounded choreography twice.

A = browser-native implementation.
B = Motion vanilla implementation.

Compare:
- code size;
- implementation complexity;
- fidelity;
- mobile behavior;
- reduced motion;
- cleanup/lifecycle;
- runtime dependency weight.

Acceptance:
- Motion enters the stack only if B materially beats A.

### P5 — GSAP exception proof

Goal: deliberately choose one transition too difficult for the baseline, preferably a Scripture Cinema transition rather than ordinary homepage motion.

Compare:
- native/View Transition attempt;
- GSAP/Flip implementation.

Acceptance:
- GSAP is admitted only for the complex class of problem, not promoted to universal site runtime.

### P6 — Lenis falsification test

Goal: test native scroll against Lenis on the exact same immersive current on desktop and mobile.

Acceptance:
- default outcome is removal;
- keep only if tactile/coordination benefit is obvious and measurable without harming mobile, accessibility, or ordinary browser behavior.

## Mobile rules

Mobile is not a reduced desktop animation.

Each prototype must choose explicitly among:
- vertical continuation;
- swipe/drag;
- native horizontal scroll;
- snap;
- static editorial stack.

No desktop-only sideways motion may be inherited blindly.

## Accessibility / reduced motion

Every prototype must preserve:
- canonical reading order;
- keyboard access;
- visible focus;
- normal links;
- semantic headings/landmarks;
- equivalent content under `prefers-reduced-motion: reduce`.

Reduced motion changes temporal behavior, not IA or content availability.

## Performance rules

- animate transforms/opacity/clip only when possible;
- avoid global per-frame work;
- dormant currents do no continuous animation work;
- sticky/native layout before JS pinning;
- no WebGL for effects reproducible with CSS/raster assets;
- no global smooth-scroll controller by default;
- image weight and decoding strategy are part of motion performance acceptance.

## Separation from Scripture Cinema

Website motion:

> simple motion language, sophisticated editorial direction.

Scripture Cinema:

> static engraving-led horizontal narrative with rare spatial/cinematic transitions at chapter/book/major narrative boundaries.

The Spark-class research belongs to Scripture Cinema transition engineering, not the base website motion runtime.

## Decision expected after bakeoff

The bakeoff should produce a small retained stack, likely close to:

`Hugo + CSS + IntersectionObserver + View Transitions + optional CSS Scroll Timelines`

with zero or one small JS motion dependency for ordinary site behavior.

GSAP/Flip remains a separate exceptional capability for Scripture Cinema / high-value cinematic transitions.

## Engineering boundary

Do not redesign production homepage directly from this document.

Next step:

`implementation landscape -> isolated Storybook/prototype branch -> P1/P2/P3 first -> human visual critique -> dependency bakeoff P4/P5/P6 -> retain smallest passing stack -> promote design rules into Doré Design constraints`

Doré learning object:

`accepted motion language -> mature implementation primitives -> minimal dependency hypothesis -> prototypes -> human critique -> retained implementation rule`
