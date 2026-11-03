# P2 / 《西望》Campaign Posters A1 + B1 / Sevenfold Dawn

**2026-11-03 · Draft implementation and art direction; NOT an approved final artwork.**

This decision supersedes the calligraphy-based requirement in P2-XIWANG-TYPE-REDESIGN-COSMOS-20261102.md. The earlier research remains archived but is no longer a binding glyph specification. The explicit user decisions are: **both posters must be made**; **no brush-calligraphy primary lettering**; **no Doré illustration in the Magazine spread** because Emmaus owns Doré; **remove the permanent seven-color magazine-side navigation**; let the homepage's sevenfold reveal introduce the poster itself.

## Two equally real magazine campaign posters

**A1 — Geometric letterform / campaign key visual.** The user's coral-red-on-pink oversized Chinese poster is a construction reference: purposefully exaggerated main strokes, counterspace, diagonal geometric cuts and nearly full-surface two-character identity. Compose two exact Traditional Chinese characters, 西 and 望, in the left square. This is a new modern publication poster, not a restyled calligraphy label. The right side remains the already approved official 5:8 Magazine cover.

**B1 — Seven-color engraved typography collection / second campaign poster.** User-approved 2026-11-03 revision: compose **3–7 individual 西望 word-groups (test 3 / 5 / 7), preferably 7**. Every group must independently use a DIFFERENT engraved line-building method and a DIFFERENT one of the seven existing Design OS section colors. Size, orientation and optical weight can vary. Dots, curved striations, parallel and radial lines must FORM the words, not decorate or recolor A's identical huge outline. This is a typographic family/system, not an A effect/filter.

Source illustrations and rights: user reference posters are examples of methods, not licensed files to copy. Do not import either image into the deployed P2 or claim the original typographic artwork is open source. Both A1 and B1 have a shared cover-pair composition, paper/ink discipline, fine folio labels and native SVG semantics.

## 2026-11-03 / open-source research and frozen status

[Verified code choices, 17 A/B candidates, exact licenses, preferred build-only integration, seven-color engraving matrix](P2-XIWANG-A-B-OPEN-SOURCE-CODE-EXPLORATION-20261103.md). **A: opentype.js + PathBool.js**, with Paper.js/skia-pathops for path verification. **B: d3-shape + d3-contour**, with flow-lines, hatched and svg-halftone as additional distinct engraving references. Not every public GitHub repository is open-source: **Halftone Pro has a proprietary license and is rejected**.

Existing A/B v1 in `static/js/p2-vol00-poster.js` are display/rendering proofs only and still use a common two-glyph shape; this **fails the newly approved design distinction**. Do not claim it is the final A1/B1 artwork. This research change does not modify any runtime, the right-hand cover, or the original scroll animation.

## Sevenfold fold — source checked against the actual homepage

Canonical references:
- [Sevenfold Dawn homepage contract](../SEVENFOLD-DAWN-NAVIGATION.md)
- static/js/first-look-host.js — makeFolds(), seven complete top-down scaleY panels and one reversible GSAP timeline
- static/css/sevenfold-dawn.css — .ws-dawn-folds and .ws-dawn-fold
- static/css/westside-design-os.css — seven original palette variables

**Important distinction**: the homepage sevenfold is SEVEN full-surface color curtains descending from the TOP; it is not the seven tiny vertical color ribbons visible in the old Magazine. The homepage shuffles final colors per discrete menu opening. P2 uses deterministic order per scroll progress so reverse scroll really reverses the same animation. The seven colors must be the OS variables: water, first-light, pale-gold, olive, harvest, crimson and daylight-mauve.

**Magazine placement**: the fold covers the entire square left poster, then recedes while A or B reveals top-to-bottom and eventually remains alone. The thin old Magazine spectrum bar is gone visually and interactively. Its inert, hidden DOM element temporarily survives ONLY as a measurement anchor for 03–07's already built spread geometry, never as navigation. Existing homepage section links still provide seven fully functional routes. No separate GSAP instance: follow the P2 existing reversible scroll renderer.

## Draft implementation in the original P2

1. static/js/p2-vol00-poster.js currently creates selectable **v1 SVG rendering proofs** and seven color curtains; A is two outlined glyphs with cuts, B is one two-glyph outline with engraved pattern. **This is the documented baseline problem, not an approved A/B design master.** The source must be superseded by separately authored A two-character geometry and B 3–7 distinct typed engraving groups after this research selection.
2. static/css/p2-vol00-poster.css scopes all changes to the original Magazine LEFT square. Old left Doré image, ink-brush wordmark, star and Contents are not displayed in poster mode. The protected RIGHT magazine cover remains unchanged.
3. static/experiments/p2-double-square-video-lab.html now offers A/B poster modes and controls, preserving ?poster=legacy for old approved screenshots only. It calls the same poster painter on its current scroll progress, no second animation clock.
4. static/js/p2-magazine-live-bridge.js passes same-origin P2 query poster=a or poster=b to the original embedded magazine frame.
5. Existing A/B are **rendering/concept proofs**, not optically corrected final masters. The current outline paths still borrow a conventional type skeleton and the same one for both A/B. The next artistic step is custom A word construction and separately generated B multi-word line families; these are not award-grade completed glyph designs.

## Required verification before approval

- Full spread 1648×928, 768×1024, 390×844, 320×720, 200% zoom and reduced motion; both A and B must pair with the original 5:8 cover with no clipping or horizontal overflow.
- The sevenfold must be a top-to-bottom seven-panel reveal and reverse cleanly; by full rest no colored ribbon is visible and the poster is completely visible.
- A and B must be different real typographic systems with legible 西 and 望. Geometry and engraving are not simply filters.
- The Magazine must show no Doré illustrations, which remain available in the genuine Emmaus gallery. No changes to Church, main Homepage sevenfold, approved cover or later ONE tools.
- Preserve keyboard, accessibility, route access from Homepage, native SVG and the single Design OS; do not merge main until live browser screenshots and regression checks are reviewed.

**Design priority**: both posters are equally real campaign assets; A may open the Vol.00 spread and B may alternate as the next campaign poster. Do not turn the poster back into a Contents/illustration page.

### 2026-11-03 / 《西望》A2+B2 正式工程接入與可重建向量母本（非藝術定稿）

**已經實際製作／接入 P2 Draft：** \`scripts/xiwang/generate-posters.mjs\` 生成 \`static/images/xiwang-poster-a-v2.svg\` 和 \`static/images/xiwang-poster-b-v2.svg\`。\`static/js/p2-vol00-poster.js\` 改為載入上述 **外部原生 SVG、不是運行時幾何生成**；保留原 sevenfold 全幅倒帶、A／B query 切換、舊七彩條退出及右側正式 5:8 封面。舊 runtime 已封存 \`static/js/p2-vol00-poster-v1-archived.js\` 作安全回退。

A2 為兩個手工構造的大型幾何「西」「望」向量構件，\`data-authority="original-geometry"\`，不繼承 v1 Noto 普通粗字骨作 A 圖本體。B2 是真正的七組橫排「西望」，每組 \`data-poster-word="1..7"\`，分别對應 Design OS 七種原色，使用 flow、radial、halftone、contour、hatch、crosshatch、concentric 七種實際原生 SVG 線場，而非把 A 改色。B 的文字形狀輪廓起點來自已授權的 Noto CJK（OFL 1.1），本輪沒有新增 JS runtime 依賴。

**驗收紀錄：** 原生 generator 可重複 build 並通過 GitHub Actions \`git diff --exit-code\`，Cloudflare 已成功部署到 PR #1381 的隔離頁。已實際檢視 Chromium 1648 與 390 截圖：兩張非空白，B 七組可見且具有編輯節奏；A 與 B 均需下一輪**藝術品質／字骨光學**驗收，不能聲稱得獎級。第一次 CI 於手機 239×240 縮圖對七色的精確 RGB 匹配過度嚴格，測試已改為「桌面驗證 5+ 色、手機檢查真實圖形密度並核對 source 7 色」；不因此放寬圖形顯示本身的驗證。

**主站保護：** P2／03 Emmaus、教會、homepage 七層折疊、右頁城市封面及其 scripture 原碼未修改。所有修改維持 Draft，不自動合併 main。

