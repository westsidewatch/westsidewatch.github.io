# Scripture Studio V29.4 — Genuine font asset integration and acceptance

**Engineering branch:** `draft/p2-0104-olive-entry-20261105`. Experimental only, no main site changes.

## What is actually committed

1. `static/fonts/scripture-studio/BodoniModaSC-VF.ttf`: official **Bodoni Moda SC** variable font from `google/fonts/ofl/bodonimodasc/BodoniModaSC[opsz,wght].ttf`. Git blob SHA **438e5a00be9b907f798b9d54b40dc33d37b2f36c**. Byte size **161,760**.
2. `static/fonts/scripture-studio/OFL-BodoniModaSC.txt`: original SIL OFL 1.1 license from the Google Fonts upstream directory.
3. `static/experiments/scripture-studio-motherform-v29-4-selfhosted-font.html`: self-hosted English face in CSS; same face in English poem, artwork and specimen; remote Google/Fontsource English imports removed. Chinese continues using the official `chiron-hei-hk-webfont` CSS (subset WOFF2, font family `Chiron Hei HK WS`, weight 900/200).
4. `static/experiments/scripture-studio-v29-4-font-smoke-test.html`: focused font validation page with specimen, scripture text, large impression sample, Chinese Heavy/ExtraLight, and explicit FontFaceSet status.

## Actual binary verification (not CSS inference)

Read the committed TTF's SFNT tables and name records. Confirmed:

- Family name `Bodoni Moda SC`, full name `Bodoni Moda SC Regular`, PostScript name `BodoniModaSC-Regular`.
- Variable axes: `wght` = **400–900** and `opsz` = **6–96**.
- GSUB table contains both **`smcp`** and **`c2sc`**.
- The source font TTF Git blob SHA matches the committed binary exactly.

The smoke test checks that `document.fonts` has loaded the self-hosted face, checks official Chiron 900 and 200, and compares font family, features, caps and weights between the English samples. `document.fonts.check()` alone is insufficient to reject silent fallback.

## Outstanding real-world validation

A successful commit and valid font binaries do **not** demonstrate that the current Cloudflare/GitHub Draft preview actually serves both faces. Local Chromium has no access to the web font files and is not suitable for optical or live-font acceptance. A normal networked browser must load the smoke test from the same deployed branch and confirm all status fields true, especially `selfHostedBodoniSC`, `ChironHeavy900`, `ChironExtraLight200` and `identicalEnglishCSS`. Only then audit glyph ink and 07 type composition.

The English TTF is self-hosted; Chiron is still from the official Unicode-range CDN. Full offline Chinese self-hosting has **not** been delivered. Because standalone HTML would lose its relative TTF asset, exporting misleading standalone HTML is deliberately blocked.

## Source and rights

- https://github.com/google/fonts/tree/main/ofl/bodonimodasc
- https://github.com/indestructible-type/Bodoni
- https://fontsource.org/fonts/bodoni-moda-sc/about
- https://github.com/chiron-fonts/chiron-hei-hk/blob/release/README.en.md

