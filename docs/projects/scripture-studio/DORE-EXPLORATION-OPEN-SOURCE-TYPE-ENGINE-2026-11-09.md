# 多雷探索 — Scripture Studio 真正的中西鉛字交叉排字引擎
## Open-source technical research · 2026-11-09

**Status:** Research/selection, not installed, not implementation proof or finished artwork.
**Purpose:** Replace the defective V1–V3 ad-hoc independent Chinese and English coordinate systems with one shared measured typographic register. Avoid visual style suggestions that do not change geometry.
**Reference:** Onion Design Associates, *Dream Pool of Gutenberg* (2017): mixed Chinese/English movable-metal-type letterpress print, original design and Ri Xing Type Foundry production context. https://www.behance.net/gallery/59203037/Dream-Pool-of-Gutenberg

## 1. Root problem

V1 splits page into separate Chinese/Latin boxes. V2 and V3 place Chinese columns and English lines using two independent heuristic coordinates; neither computes real glyph outlines, shared grid cells, collision constraints, typography fit or common yin/yang geometry. V3 preview/source divergence also undermined verification. More CSS alignment, gradient and ornamental material cannot solve this.

**Technical target:** `verified excerpt + semantic type groups + font glyph metrics → glyph runs → shared modular grid → collision-aware candidate compositions → editorial optical selection → immutable layout geometry → both yin/yang impression states → SVG/HTML preview + identical export`.

Real artists can deliberately choose overlaps, rotations, asymmetry and negative space. The solver must permit explicit exceptions, not simply maximize packing. The design is a **guided composition generator**, not a random collage or fully automatic award-winning design machine.

## 2. Open-source shortlist (primary sources, licenses verified from repos where available)

| Layer | Library | Technical use | Verified facts and caveats | Decision |
| --- | --- | --- | --- | --- |
| Glyph reader + metrics + outline | [opentype.js](https://github.com/opentypejs/opentype.js) | Parse OTF/TTF/WOFF; measure glyph advances/kerning, build SVG outlines | MIT, browser/Node. Specialized shaping has limits; use registered exact OS fonts where license allows access. | **P0 preferred** |
| 2D spatial candidate test | [RBush](https://github.com/mourner/rbush) | R-tree index for bounding-box intersection queries while searching candidate positions | MIT; ESM v4.0.1 seen in repo. Bounding rectangles are *conservative* proximity checks; not true glyph outline overlap. | **P0 optional small module** |
| Vector contour and boolean operations | [Paper.js](https://github.com/paperjs/paper.js) | Real outline intersection/unite/subtract and geometry for approved overlap logic; vector path manipulation | MIT; browser canvas/scriptographer heritage. Use on shortlist of candidates, not every glyph continuously. | **P0/P1 selective** |
| SVG scene control | [SVG.js](https://github.com/svgdotjs/svg.js) | Editable SVG native display; manipulation/animation; same geometry reused for export | MIT, lightweight and no dependencies. Optional if native DOM SVG sufficient; don't install just to replicate DOM APIs. | **P1 optional** |
| Accurate shaping | [harfbuzzjs](https://github.com/harfbuzz/harfbuzzjs) | Shaping and glyph positioning; v1 breaking API compared with 0.x; WASM | MIT; use if opentype.js cannot accurately shape actual fonts or vertical substitutions; not a 2D compositor. | **P1 conditional** |
| Alternate complete font engine | [fontkit](https://github.com/foliojs/fontkit) | Shaping, metrics, SVG contours, subsetting | More advanced scope / potential alternative to opentype.js. Avoid bringing both engines into first prototype. Check current license for exact pinned version before adoption. | **Alternative** |
| Print folio/page output | [Paged.js](https://github.com/pagedjs/pagedjs) | HTML paginated PDF publication | Open-source, but not relevant to constructing a single interwoven typographic seal; revisit when making print calendar/book. | **Defer** |
| Print-side path ops | [fontTools](https://github.com/fonttools/fonttools) + [skia-pathops](https://github.com/fonttools/skia-pathops) | Font subsetting and exact contour boolean output in backend or build step | fontTools MIT; skia-pathops BSD-3-Clause. Python toolchain not warranted for interactive first cut. | **Defer / output pipeline** |
| Canvas editor | [Konva](https://github.com/konvajs/konva) | Interactive canvas editor and export | MIT; mature, but requires separate Canvas/export path and is broader than the native-SVG proof. | **Do not adopt for first slice** |

**Source evidence:** https://github.com/opentypejs/opentype.js ; https://github.com/mourner/rbush ; https://github.com/mourner/rbush/blob/main/package.json ; https://paperjs.org/reference/path/ ; https://paperjs.org/license/ ; https://github.com/svgdotjs/svg.js ; https://github.com/harfbuzz/harfbuzzjs ; https://github.com/harfbuzz/harfbuzzjs/blob/main/LICENSE ; https://github.com/foliojs/fontkit ; https://github.com/fonttools/fonttools ; https://github.com/fonttools/skia-pathops ; https://github.com/pagedjs/pagedjs ; https://github.com/konvajs/konva .

## 3. Adopt minimal viable stack

**Core minimum:** existing Scripture Studio plain JS + SVG DOM + `opentype.js` + our own **typographic register + constraint-search engine**. Introduce RBush only once number of candidate collisions warrants it; simple direct checks may be cheaper for 20–100 blocks. Introduce Paper.js for contour clearance/overlap tests only after a measurable need is shown. Do not add HarfBuzz and fontkit in first pass without evidence of shaping errors.

No server/SaaS or subscription. Prefer pinned versions, locally bundled compatible runtime modules if production license permits. Do not invent new OS fonts or colors; use existing design tokens. Ensure correct glyph coverage for Chinese and all selected punctuation; fonts are licensed separately from libraries.

**Caution:** path-based SVG export can turn editable text into geometric outlines, useful for archival/print but not text selection. Retain separately the source passage in DOM/JSON and a normal accessible text layer. For live visual editing, use authoritative layout object and fonts rather than relying on manually altered raw SVG paths.

## 4. Genuine interwoven typographic register

1. **Content decomposition:** exact original text + reference is immutable. Editor selects a *visual excerpt* (one key verse, phrase or a few precise characters), splits it into meaningful Chinese groups and Latin phrases intentionally, not by arbitrary char counts. All groups map back to verified source span.
2. **Font metrics:** independently shape each run; obtain glyph outlines, advance and visual bounds in normalized units. Chinese vertical and Latin horizontal (and inverse experiment) share ONE register. Real font size ratio and baseline arise from measured contours and optical targets, not unrelated hardcoded x values.
3. **Occupancy grid:** 16×16 or 24×24 virtual cells is a starting hypothesis, not a mandated aesthetic; candidate glyph group placements occupy measured contours and maintain a configurable safe inset.
4. **Composition candidate search:** a finite set of artist-designed compositional grammars with constraints (root/anchor phrase, secondary phrase, cross-axis, negative space, edge alignment and reading direction). Generate scored candidates: recognizability, contour interference, semantic integrity, density balance, central vs edge gravitational strength, aspect ratio fit, mobile/large feasibility. Avoid random coordinates and simply fitting everything.
5. **Optical selection:** show editor meaningful alternatives, permit art-director choice/adjustment, store adjustments as optical corrections in the recipe. No guarantee that auto-scoring substitutes for artistic judgment.
6. **Yin/Yang:** generate color/ink polarity variants from the **same immutable geometry register**. User request of alternative direction pairs can be modeled as related transformations of the same register with documented correspondence; do not create two unrelated independent layouts.
7. **Identical output:** one canonical layout JSON consumed by the on-screen SVG renderer AND file exporter, never parallel layout algorithms.

## 5. First engineering proof — deliberately narrow

**Use 2 samples first:** short (Romans 10:17 / `信道是從聽道來的` and verified KJV phrase) and long (Luke 24:27 chosen excerpt) to test extremes. Do not manually author 8 separate posters. Once engine passes both, rerun home + seven realm presets in a batch.

**Proof gate:**
- Parse the exact approved OS fonts and extract measurable bounds for Chinese/Latin runs; warn if font cannot be loaded or lacks glyphs.
- Render 2–3 layout candidates each using one shared register; no arbitrary second CSS coordinate map.
- Zero involuntary cropped letters or missing words; mandatory exact-citation check.
- Debug mode exposes measured bounding boxes/occupied cells; production mode hides guides without changing geometry.
- Yin/Yang rendered from same layout object, export SVG pixel-compatible with actual browser preview.
- Responsive snapshots 1648, 768, 390, 320 px; actual font loaded, not fallback luck.
- Clean monochrome static still remains an artwork; no borders, fake distressed textures, clipart, glyph strokes drawn as decoration.
- Native selectable/full Scripture remains available to reader separately; special art mode may interweave to make image, full Bible reader must not be transformed.
- Compare actual screenshots and edit recorded design judgment, not just unit test passing.

## 6. Fit with existing Doré Core and existing product

- Design intelligence and sample selection belong in existing Doré Design visual research / Storybook context, **not** a new foundational LLM agent.
- The Scripture Studio editor adopts `dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md` direct-on-output surface and source/provenance separation.
- Only one authoritative type-geometry model serves artwork, Folio DNA export, all seven realm entrance signatures, and Bethlehem / A Day recurring art.
- Existing P2 scenes, original posters, home scrolling and Church/ONE motion remain untouched until separately approved. A finished art proof is a dependency before additional live animation.

## 7. Immediate decisions

1. **Stop adding V4/V5 demos that only change heuristic coordinates.**
2. Begin P0 with `opentype.js` glyph metrics and a shared geometry data structure, plus hand-designed semantic group templates.
3. Use RBush and Paper.js only where real collision tests demonstrably require them.
4. Verify actual OS Chinese/Latin font loading and licenses before bundling assets; no arbitrary system fallback.
5. Require an actual screenshot/identical-export QA gate before another user-facing "preview".
6. After art approval, derive Folio and high-frequency Bethlehem daily typography from the same retained design DNA.

**No software has been installed or deployed as a result of this research record.**
