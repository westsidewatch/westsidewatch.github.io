# Sevenfold Dawn — Stage 1 verified integration audit

Read against current default branch on 2026-10-14. This is an audit, not a claim of rendered visual acceptance.

## Design OS — actual seven section color authorities

| Section | CSS source token | Value at current main |
|---|---|---|
| Church | `--ws-water` | `#5b8fa8` |
| Journal | `--ws-first-light` | `#a2872a` |
| Bible | `--ws-pale-gold` | `#cebd74` |
| Sermon | `--ws-olive` | `#738a5a` |
| Books | `--ws-harvest` | `#b8944a` |
| Cinema | `--ws-crimson` | `#a14d57` |
| Life | `--ws-daylight-mauve` | `oklch(67% .075 330)` |

Verified in `static/css/westside-design-os.css` around lines 122–148 and 283–289. These are references to authoritative CSS variables, not a copied standalone palette. No new palette.

## Current DOM and conflict inventory

Source: `layouts/partials/watch-home-editorial.html`.

1. Floating nav `.sites-home-nav--floating` includes a homepage-only top-left duplicate wordmark `.sites-home-nav__brand`, native `details > summary` with visible `CONTENTS` and `+` symbol, seven anchors, search, preview iframe, and three auxiliary entry links.
2. Hero also contains a separate `.sites-home-nav` with eight destination links. Consolidate visible controls while retaining route functionality.
3. `.sites-home-film > iframe` has a fixed source and must never be recreated or have its src changed on menu transitions.
4. Existing logo image is `/images/westside-watch-masthead-landscape.svg`; there is also a distinct morning star asset `/images/westside-watch-morning-star.svg`. Verify actual SVG appearance and size before assigning the small/large logo instances.
5. Slogan is `h1#sites-home-title` within `.sites-home-intro`.
6. Scripture is `.sites-home-scripture-pair` containing Chinese `.sites-home-slogan-zh` and English `.sites-home-scripture` with citation. It must become an independent fixed anchor, not move with the slogan.
7. `.sites-home-entry` contains three links outside the floating menu. Preserve their destinations even if visual entry buttons are removed from the homepage composition.

Source: `static/js/first-look-host.js`.

8. Floating-nav controller binds to `details`, intercepts summary click, and toggles `ws-scale-reveal-active/open`. Must replace, not run alongside, the new controller.
9. Preview logic mutates `iframe.src` only for the *hover-preview iframe*, not the Film. Preserve this separation.
10. Anchor navigation, escape handling, scroll tone/hiding, and menu link handlers currently live in the same IIFE. Preserve behavior when replacing controller.
11. Hero, navigation and brand styles may be spread across stylesheets. Do not assume `static/css/sites-home.css` exists: it returned 404. Find authoritative selectors before implementing, not via guessed file names.

## Engineering decisions locked

- One brand-plane `translateY` only; small logo and large logo are two stationary assets inside the same moving parent, not separately animated.
- Seven top-down fold elements; final layer chosen from Design OS tokens. No invented colors.
- Scripture position in viewport is unchanged across states, including typography; contrast-only transition allowed.
- Native Film iframe untouched; no iframe cloning, remounting, or scaling.
- No changes to PR #1303, no changes to production main until complete implementation and real visual acceptance.
- Joby studied for visual timing/geometry, not imported.

## Next integrated implementation batch

Trace active CSS authority for hero/nav/brand, then modify homepage partial, controller and one scoped CSS file together. Keep draft PR until working visual frames have been reviewed. A Playwright PASS without actual rendered screenshot inspection is insufficient.
