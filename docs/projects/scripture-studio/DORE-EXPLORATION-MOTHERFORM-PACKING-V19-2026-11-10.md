# 多雷探索與可執行母本 V19 — Scripture Studio Isaiah 62:6

**State:** isolated art-direction / algorithm proof, not public or editorial-approved verse layout. Source: `static/experiments/scripture-studio-motherform-v19.html`.

## Compared actual available mechanisms

1. **USFM 3 poetry** (`q1/q2/q3`): structural *source data* for poetic lines, not an algorithm for inventing correct lineation. [Official specification](https://ubsicap.github.io/usfm/poetry/). The motherform carries manual editorial candidate lines and explicitly does not misrepresent them as a licensed edition's official USFM structure.
2. **Bridgeconn USFM Grammar**: open source parsing/validation of USFM / USJ / USX, browser and Node compatible. Useful later when actual legally usable marked-up CUV/KJV data is supplied. It is not bundled into V19. [Repository](https://github.com/Bridgeconn/usfm-grammar).
3. **Mapbox potpack**: small open source near-square rectangle packer; takes arbitrary rectangles, reorders them and returns x/y/fill. Excellent reference for spatial occupancy but **cannot be used unmodified**, because generic packing destroys each translation's reading order and poetic continuity. [Repository](https://github.com/mapbox/potpack).
4. **W3C Writing Modes / CSS `vertical-rl` + `text-orientation:mixed`**: uses actual browser text shaping for Han vertical and embedded Latin sideways, with natural right-to-left Chinese column order. Selected for V19. [W3C](https://www.w3.org/TR/css-writing-modes-3/).
5. **Knuth–Plass / tex-linebreak** is for choosing breaks in a known sequence; it cannot by itself discover two-language interleaved compositional sequences. A corpus-aware semantic lock layer must come first. [Implementation](https://github.com/robertknight/tex-linebreak).
6. **Exact glyph contours / opentype.js + Paper.js** are candidates for a future print-ready true vector path output; V19 measured browser typographic bounding boxes, NOT actual black ink outline. Do not conflate these.

## Real solver executed

**Input:** Isaiah 62:6 traditional Chinese CUV and English KJV, immutable canonical passage strings. Use 11 Chinese and 9 English manually curated phrase units; the protected `呼籲耶和華的，` remains whole. **Important:** optional splitting within `他們晝夜必不靜默。` in this engineering study is **awaiting human editorial approval** and may not be published.

**Search:** seven-column finite permutation search, with requested mixture of `ZEZE ×2`, `ZEZ ×2`, `ZE ×3`; deduplicated 206 complete candidate compositions. Preserves the original intra-language reading order and complete source punctuation. Filters by strict-majority asymmetry (> half columns outside 40–60%) and scores near-square geometry plus varied lengths.

**Render:** one shared HTML/CSS motherforme with native Chinese vertical RTL, sideways English embedded, rotated 90 degrees for the English-reading presentation. Chinese 900 / Chinese 200 styles and English Bodoni roles are explicitly bound, but **the local test Chromium did not load the network font faces**. Capture as fallback only; 200/900 optical appearance remains UNVERIFIED.

**Optical fit:** fixed 44px nominal letterpress font size, configurable alternatives 40/48. Layout adjusts number/width and gap of bars, not font size to fit more text. Browser computes native scroll bounding box of type, compares to intrinsic square print side. In the default tested specimen the measured type box is 894×910 px in a 1046px square, giving **85.5% width / 87.0% height**. This is *typographic box occupancy*, not actual glyph-ink area; contours and white space internal to letters are not measured by the prototype.

## Automated QA actually performed

Chromium generated **36 combinations**: viewport 1648, 768, 390, 320 × nominal type size 40/44/48 × three candidate arrangements. All 36 passed exact bilingual reconstruction, both scripts in all bars, 4/7 bars with >=2 cross-language switches, 6+/7 asymmetrical for the default, >=72% both-axis measured typographic bounds, fixed font size, and **zero intersecting fragment rectangles in each bar**, in both rotated/unrotated views. JSON export/download was exercised and checked; screenshots saved.

**Not yet verified:**
- real Chiron Hei HK WS 900/200 and Bodoni Moda/SC/Italic in a browser with network fonts loaded;
- precise glyph-ink shape, beyond typographic rectangles, and true text-outline print SVG;
- artistic suitability/approval of each proposed soft poetic break; especially the optional breakdown of `他們晝夜必不靜默。`;
- every artifact's English-leading / Chinese-leading perception. A single physically rotated forme may have orientation-order tension even while individual reading language order remains correct; flag for editorial review, do not invent a claim of automatic resolution.
- generalization to the other seven sections' scripture corpus: V19 intentionally validates one motherforme.

## Production gate

Until font loading, poetic editorial review, glyph collision / ink silhouette and export fidelity all pass, V19 is a **technical and compositional prototype**, not a completed award-level design. Keep main site and P2 untouched. Next changes should be evaluated against the exactly preserved lines and one shared source layout, not fixed row quotas or arbitrary text boxes.
