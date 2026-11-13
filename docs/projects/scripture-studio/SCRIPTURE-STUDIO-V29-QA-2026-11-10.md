# Scripture Studio V29 — 07 composition engine / QA

Date: 2026-11-10. Status: **engineering progress; NOT an approved print seal**.

## Engineering changes

- Registered Bodoni Moda SC (Owen Earl / indestructible type*) in the authoritative OS editorial manual. License OFL-1.1. Formal font variable package: `@fontsource-variable/bodoni-moda-sc`, CSS family `Bodoni Moda SC Variable`; actual caps requested through `font-variant-caps: all-small-caps` and `smcp` / `c2sc`.
- Chinese Chiron Hei HK WS 900 primary / 200 countertype (font-specific artwork overrides, not global OS 600 heading token).
- Retained the *full existing* Isaiah 62:6 CUV/KJV strings and editorially tentative line locks; V28 shortened the passage and was not used as content authority.
- Replaced English Canvas measuring with DOM font-run measurement (post-load when fonts available), and broadened candidate optical positions (six rhythm patterns, five gap choices, and 26 layout indices in each family).
- The compositor chooses a motherforme with visibly varied text-run heights and left/right mass; 90° rotated presentation derives from the same composition. Not enough to satisfy user design review yet.
- Added optional in-browser official font file load (no upload); rejects obvious wrong file names and does not infer authenticity solely from them.
- Maintained strict fail-closed display and formal export when font faces are not registered as loaded. A CSS declaration is not a verified font face.

## One-run actual Chromium test

- Source: `/mnt/data/scripture-studio-motherform-v29-07.html`.
- Headless Chromium executable: `/usr/bin/chromium`.
- All external requests intentionally blocked to reproduce offline/font-missing conditions.
- JavaScript syntax check: PASS.
- One default configuration: **780 actual DOM candidate arrangements evaluated**; 7 bands; 4 bands with >=2 mixed-language switches; 5/7 distinctly non-50/50; Chinese exact source PASS; English exact source PASS; font-size does not decrement.
- Browser layout/structure acceptance PASS; official OS fonts **FAIL** (no access to font resources); ink silhouette **NOT TESTED/FAIL**; full artwork **NOT APPROVED**.
- Typography: CSS 900/200 and all-small-caps are present; this does *not* prove genuine glyphs. Never claim final typography from a fallback test.
- Full 9-combination size/variant test did not finish within this local browser run's timeout; do not claim a multi-configuration pass.

## Remaining hard gates

1. Load official Bodoni Moda SC WOFF2 (verify actual family and SC glyph forms) and Chiron variable WOFF2 (200 and 900) in accessible browser/Cloudflare context, ideally self-hosted under approved font assets. Internet fetch is blocked in this local container.
2. Rerun search after font load (real font metrics change geometry); compare small-caps vs upper-case at identical size and verify real `smcp` / `c2sc` face behavior.
3. Validate full bilingual poetry lines and each secondary break with Bible editorial review.
4. Independent pixel-level ink occupancy in both axes, more than DOM rectangle occupancy, and collision/orphan tests at 1648/768/390/320.
5. If the 07 work remains skinny, change legal phrase grouping and artboard composition, not text size or scripture content.

Main site and P2 untouched. GitHub Draft only.