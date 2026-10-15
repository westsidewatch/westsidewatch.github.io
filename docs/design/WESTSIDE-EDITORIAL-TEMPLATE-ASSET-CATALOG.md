# Westside Editorial Template Asset Catalog

> Design OS internal index. Source: [English Display Typography Handbook](./WESTSIDE-ENGLISH-DISPLAY-TYPOGRAPHY-HANDBOOK.md). Extracted code is preserved verbatim below, not promoted to production. No font, color, engraving, Chinese scripture or page changes.

## Use contract

- Template-first: select an existing composition, then replace content within its constraints.
- Fixed typography and color remain owned by existing Design OS. Never stretch glyphs.
- Status **candidate** = sample code not visually validated; **component** = supporting fragment; **experimental** = conceptual layout only. None is a production-approved template.
- Preserve original page assets and positions unless explicitly approved.
- Folio / Guizang are external candidates, **not copied or installed here**; review code licenses before importing.

## Extracted composition assets

| ID | Composition | Status | Handbook lines |
|---|---|---|---|
| `phrase-grid` | Phrase-as-shape / semantic phrase grid | candidate | 359–411 |
| `half-page` | Half-page asymmetric editorial split | candidate | 412–440 |
| `responsive-headline` | Responsive display headline | candidate | 544–567 |
| `image-story` | Editorial copy and image split | candidate | 650–690 |
| `portrait-crop` | Portrait focal crop | component | 691–710 |
| `foreground-portrait` | Foreground subject / background headline | candidate | 711–750 |
| `shape-outside` | Editorial image text wrap | component | 751–764 |
| `soft-edge` | Soft image mask | component | 765–779 |
| `initial-architecture` | Monumental L/W initials | experimental | 1278–1318 |

## Source-preserving code extracts

### phrase-grid — Phrase-as-shape / semantic phrase grid

Status: **candidate**. Original handbook lines 359–411.

### 13.4 技術模式 A：語義片語 + CSS grid，避免單字孤行

以下是**可複用的實作範例**，不是已經部署的本站元件。用 span 控制有意識的斷行；完整文字在 DOM 中保持正確順序。若語義片語在極窄容器仍放不下，應切換更小字級或重新批准斷點。

```html
<h1 class="ws-editorial-display" lang="en">
  <span class="ws-editorial-display__line">He that believeth</span>
  <span class="ws-editorial-display__line">on me,</span>
  <span class="ws-editorial-display__support">as the scripture hath said,</span>
  <span class="ws-editorial-display__support">out of his belly shall&nbsp;flow</span>
  <span class="ws-editorial-display__hero">rivers of</span>
  <span class="ws-editorial-display__hero"><em>living&nbsp;water.</em></span>
</h1>
```

```css
/* Example only: page scope owns composition, Design OS owns typography. */
.ws-editorial-region {
  container: ws-editorial / inline-size;
  min-width: 0;
}
.ws-editorial-display {
  font-family: var(--ws-type-display-en);
  font-weight: 400;
  font-synthesis: none;
  display: grid;
  justify-items: start;
  gap: .12em;
  min-width: 0;
}
.ws-editorial-display__line {
  display: block;
  font-size: clamp(2rem, 5cqi, 5.5rem);
  line-height: 1.04;
}
.ws-editorial-display__support {
  display: block;
  font-size: clamp(.95rem, 2cqi, 1.75rem);
  line-height: 1.24;
}
.ws-editorial-display__hero {
  display: block;
  font-size: clamp(2.8rem, 7cqi, 7rem);
  line-height: .98;
}
@container ws-editorial (max-width: 38rem) {
  .ws-editorial-display__line { font-size: clamp(1.6rem, 6cqi, 3rem); }
  .ws-editorial-display__hero { font-size: clamp(2.2rem, 8cqi, 4rem); }
}
```

**注意：** 這是示意 CSS。`cqi` 依容器寬度計算，且容器查詢須在支持的瀏覽器上驗證。`&nbsp;` 避免特定片語拆開，但不能解決所有超長英文單字；對極窄屏要另訂版式。若實際來源是經文，不能把 span 換行變成有意義的標點或改寫內容。


### half-page — Half-page asymmetric editorial split

Status: **candidate**. Original handbook lines 412–440.

### 13.5 技術模式 B：半版字母 + 另一半留白／中文

```html
<section class="ws-editorial-region">
  <div class="ws-editorial-half">
    <div class="ws-editorial-half__headline"><!-- semantic English headline --></div>
    <div class="ws-editorial-half__counter"><!-- Chinese / portrait / negative space --></div>
  </div>
</section>
```

```css
.ws-editorial-half {
  display: grid;
  grid-template-columns: minmax(0, 1.4fr) minmax(0, .6fr);
  gap: clamp(1rem, 3cqi, 3rem);
  align-items: center;
}
.ws-editorial-half > * { min-width: 0; }
@container ws-editorial (max-width: 42rem) {
  .ws-editorial-half {
    grid-template-columns: minmax(0, 1fr);
    align-items: start;
  }
}
```

[OS] 半版不是 `50% + 50%` 的固定比例；要根據實際字形和對側內容調整。**不要**把這些範例原樣套進既有 PR 頁面，必須先移除相互衝突的局部 CSS。


### responsive-headline — Responsive display headline

Status: **candidate**. Original handbook lines 544–567.

### 14.7 CSS 範例 C：依容器重組大標

```css
.ws-optical-region { container: ws-optical / inline-size; }
.ws-optical-region .ws-optical-title {
  font-family: var(--ws-type-display-en);
  font-weight: 400;
  font-synthesis: none;
  font-kerning: normal;
  font-optical-sizing: auto;
  font-size: clamp(2rem, 6cqi, 6rem);
  line-height: 1.04;
  min-width: 0;
}
@container ws-optical (max-width: 38rem) {
  .ws-optical-region .ws-optical-title {
    font-size: clamp(1.6rem, 7cqi, 3.4rem);
    line-height: 1.08;
  }
}
```

[OS] 這些數值只是實驗起點，不可直接升格為全站硬性字級。容器變窄時先重組版位與語義分行，不使用 scaleX/scaleY 拉伸或壓扁字形。


### image-story — Editorial copy and image split

Status: **candidate**. Original handbook lines 650–690.

### 15.4 實作 A：安全半版 Grid

```html
<section class="ws-image-story">
  <div class="ws-image-story__copy">
    <h1 class="ws-image-story__title">Living Water</h1>
  </div>
  <figure class="ws-image-story__media">
    <img src="/images/example-portrait.webp" alt="Portrait description">
  </figure>
</section>
```

```css
.ws-image-story {
  display: grid;
  grid-template-columns: minmax(0, 1.1fr) minmax(0, .9fr);
  align-items: center;
  gap: clamp(1rem, 3vw, 4rem);
}
.ws-image-story > * { min-width: 0; }
.ws-image-story__title {
  font-family: var(--ws-type-display-en);
  font-weight: 400;
  font-synthesis: none;
  font-size: clamp(2rem, 5vw, 6rem);
  line-height: 1;
}
.ws-image-story__media { margin: 0; }
.ws-image-story__media img {
  display: block;
  width: 100%;
  height: auto;
}
@media (max-width: 700px) {
  .ws-image-story { grid-template-columns: minmax(0, 1fr); }
}
```

[EXPERIMENT] 欄位比例及字級僅是候選。若需要按組件容器響應，將 `container-type:inline-size` 設在**外層 wrapper**，由內部 Grid 接受 `@container` 規則；不能讓元素查詢自身寬度來改變自己的欄數。


### portrait-crop — Portrait focal crop

Status: **component**. Original handbook lines 691–710.

### 15.5 實作 B：圖片焦點與裁切

```css
.ws-portrait-window {
  aspect-ratio: 4 / 5;
  overflow: hidden;
}
.ws-portrait-window img {
  width: 100%;
  height: 100%;
  object-fit: cover;
  object-position: 62% 30%; /* per-image candidate, not global */
}
@media (max-width: 700px) {
  .ws-portrait-window img { object-position: 55% 24%; }
}
```

[OS] `object-fit:cover` 只裁切，不得拉伸人物；每張圖片的焦點須經人工核准。不能把同一 `object-position` 套到所有講員。


### foreground-portrait — Foreground subject / background headline

Status: **candidate**. Original handbook lines 711–750.

### 15.6 實作 C：人物在字母前景（特批）

```html
<div class="ws-portrait-cover">
  <h1 class="ws-portrait-cover__headline">LIVING WATER</h1>
  <img class="ws-portrait-cover__foreground"
       src="/images/example-cutout.webp" alt="">
</div>
```

```css
.ws-portrait-cover {
  position: relative;
  isolation: isolate;
  overflow: hidden;
  min-height: 32rem;
}
.ws-portrait-cover__headline {
  position: relative;
  z-index: 1;
  font-family: var(--ws-type-display-en);
  font-weight: 400;
  font-synthesis: none;
}
.ws-portrait-cover__foreground {
  position: absolute;
  z-index: 2;
  right: 0;
  bottom: 0;
  max-width: 70%;
  max-height: 100%;
  width: auto;
  height: auto;
  object-fit: contain;
  pointer-events: none;
}
```

[OS] 前景素材需真正透明並具使用權；`alt=""` 只用於已由其他內容描述的裝飾性重複圖層。重要字母被人物遮到無法辨識時，改回半版，而不是犧牲文字。


### shape-outside — Editorial image text wrap

Status: **component**. Original handbook lines 751–764.

### 15.7 實作 D：shape-outside 只用於適當的長文

```css
.ws-feature-portrait {
  float: right;
  width: min(40%, 22rem);
  shape-outside: ellipse(48% 49% at 50% 50%);
  shape-margin: 1.25rem;
  margin: 0 0 1rem 1.5rem;
}
```

[OS] `shape-outside` 控制浮動元素旁的文字流，**不是**所有大型標題的排版工具。對短巨字應優先使用 Grid 和明確語義分行，避免文字被人物輪廓切成孤字。


### soft-edge — Soft image mask

Status: **component**. Original handbook lines 765–779.

### 15.8 實作 E：圖片遮罩與漸層

```css
.ws-editorial-image--soft-edge {
  -webkit-mask-image: linear-gradient(
    to right, transparent, #000 20%, #000 100%
  );
  mask-image: linear-gradient(
    to right, transparent, #000 20%, #000 100%
  );
}
```

[EXPERIMENT] 此處黑色只是遮罩的不透明度定義，**不是新增黑金配色**。遮罩只可套在經批准的圖片層，不能裁掉人物的重要部位，亦不可套整個 section 誤傷文字與 CTA。


### initial-architecture — Monumental L/W initials

Status: **experimental**. Original handbook lines 1278–1318.

### 21.3 可用 CSS 起點（概念代碼，尚未合入頁面）

```html
<div class="lw-art" aria-hidden="true">
  <span class="lw-art__l">L</span>
  <span class="lw-art__w">W</span>
</div>
<!-- 完整經文仍留在原有 .scripture-en；中文仍留在 .scripture-zh -->
```

```css
/* Scoped art direction; use only after deleting replaced old rules. */
.edition[data-variant="0"] { container-type: inline-size; }
.edition[data-variant="0"] .lw-art {
  position: absolute; inset: 0; pointer-events: none; z-index: 1;
  font-family: var(--ws-type-display-en); font-weight: 400;
  font-style: normal; font-synthesis: none;
}
.edition[data-variant="0"] .lw-art__l,
.edition[data-variant="0"] .lw-art__w {
  position: absolute; display: block; line-height: .72;
  letter-spacing: -.055em; white-space: nowrap;
}
.edition[data-variant="0"] .lw-art__l {
  left: 5%; top: 12%; font-size: clamp(110px, 34cqi, 470px);
  color: var(--ws-ink);
}
.edition[data-variant="0"] .lw-art__w {
  left: 32%; bottom: 10%; font-size: clamp(110px, 31cqi, 420px);
  color: var(--ws-water);
}
/* The content/engraving must be positioned after measuring actual glyphs.
   Do not paste these coordinates as production constants. */
@container (max-width: 680px) {
  .edition[data-variant="0"] .lw-art__l { font-size: 27cqi; }
  .edition[data-variant="0"] .lw-art__w { font-size: 27cqi; left: 42%; }
}
```

這段是**構圖試驗起點**，不是可直接宣告 PASS 的最終 CSS。既有 edition 已有 grid/overflow/positioning 規則，實作必須先移除衝突的舊規則，不能在檔尾疊加 `!important`。如果原元素無法成為 query container，改在其內設置專用容器，避免破壞既有定位上下文。


## External template candidates

- [Folio](https://github.com/Jorgut/folio): evaluate actual template assets, license, input contract and output before adoption.
- [Guizang PPT Skill](https://github.com/op7418/guizang-ppt-skill): review AGPL-3.0 obligations before any code reuse; no import performed.
- [Open Design Kilo](https://github.com/mojila/open-design-kilo): evaluate compatible layouts, avoid duplicating Design OS.

## Acceptance gate

A candidate becomes `approved` only after same-page visual comparison at relevant breakpoints, confirmed typography tokens, correct engraved background, protected Chinese scripture placement, collision checks, and an explicit PASS record.


## Registered research project — Folio × Doré engraved editorial surfaces (2026-10-15)

**Project ID:** `WS-OS-EDITORIAL-ENGRAVING-01`  
**Owner / authority:** existing Westside Design OS. This is a research-and-asset registry, **not** a new CSS authority, component framework, CI gate, or parallel design system.  
**Target:** PR #1325, second-screen John 7:38 first; other First Look pages only after visual approval.  
**Live preview:** https://pr-1325.westsidewatch-github-io.pages.dev/experiments/sevenfold-first-to-second.html  
**Status:** layout and typography selected from local experiments; engraving treatment **in progress / not visually approved**.

### Source registry (retain original URLs and provenance)

| Source / asset | Purpose | Adoption state / restrictions |
| --- | --- | --- |
| [Folio — Jorgut/folio](https://github.com/Jorgut/folio) | Layout structures, facing-page / landscape editorial compositions; original L01–L47 family inventory | Candidate reference; **no upstream Folio source template imported yet**; verify MIT license and per-image rights. [Detailed mapping](./WESTSIDE-FOLIO-LAYOUT-ADOPTION.md). |
| [Westside English Display Typography Handbook](./WESTSIDE-ENGLISH-DISPLAY-TYPOGRAPHY-HANDBOOK.md) | Position, monumental type, optical proportions, subject-safe zones and candidate scoring | Existing Design OS handbook; typography authority remains the Design OS runtime/tokens. |
| [Westside Editorial Template Asset Catalog](./WESTSIDE-EDITORIAL-TEMPLATE-ASSET-CATALOG.md) | Reusable structural candidate index and source-preserving snippets | This file; never claim an experimental template is a direct Folio import. |
| [Gustave Doré — Wikimedia Commons category](https://commons.wikimedia.org/wiki/Category:Gustave_Dor%C3%A9) | Engraving study: directional hatching, tonal density, light/shadow and print grain | Visual reference only until each work's provenance and reproduction rights are verified; **no bulk download required**. |
| [The Metropolitan Museum of Art — Open Access](https://www.metmuseum.org/hubs/open-access) | Public-domain print and engraving reference discovery with item-level rights metadata | Candidate external IIIF / online reference; no unverified work claimed as approved. |
| [Art Institute of Chicago API](https://api.artic.edu/docs/) | Open collection metadata and IIIF image reference exploration | Candidate online research interface; verify each artwork's public-domain status before reuse. |
| [IIIF Presentation API](https://iiif.io/api/presentation/3.0/) | Remote manifests / attribution / image metadata for research without mirroring archives | Technical standard reference, not itself an engraving collection. |

### Approved local composition / locked constraints

- Selected structure: **08 facing-page diptych**, locally reconstructed; **07 display pairing**: Bodoni Moda `Living` roman + `Water.` italic. Do not describe this as an imported Folio original.
- Chinese scripture: restore template-wide bottom position; do not move it individually into the right column.
- Keep original sevenfold motion, upper blue curtain, scripture semantics, page index, CTA and other six panels. No new preview URL.
- Current engraving is **existing procedural curved / hatch-like CSS**, not verified as a historical Doré engraving; replace or refine **only the background layer**, not type/geometry.
- Typography, palette, material, stroke weight, responsive rules and layering must read existing Design OS tokens; no new black-gold palette, no stretched glyphs, no duplicate global CSS.

### Engraving experiment — implementation and acceptance

1. **Material audit:** locate current second-screen line generation and determine whether it is CSS gradients, SVG paths or image texture; isolate the owning rule, remove only superseded line styles.
2. **Reference extraction:** compare at least one documented Doré engraving and one historical engraving reference for line density, cross-hatching, directional light and negative-space distribution; record exact URLs and rights metadata before any image adoption.
3. **Single-layer prototype:** implement a scoped noninteractive engraving material for the existing second-screen preview; keep lettering, English/Chinese scripture and footer above the texture with readable contrast.
4. **Visual gate:** wide / medium / narrow, zoom and half-screen/full-screen; inspect line aliasing, moiré, readability, and motion/reduced-motion. No CI-as-visual-PASS.
5. **Promotion gate:** only after screenshot comparison and explicit approval mark the material `approved`; until then `experimental`.

**Do not lose the assets:** future work must start from this project ID, the source table and the existing [Folio adoption contract](./WESTSIDE-FOLIO-LAYOUT-ADOPTION.md), not restart research or invent another catalog.


## Temple Objects Engraving — church fixed material and biblical visual theology (2026-10-15)

**Part of project:** `WS-OS-EDITORIAL-ENGRAVING-01`. **Authority:** existing Westside Design OS. **Status:** editorial / theological design plan; not yet visually approved or implemented as a fixed site material.

### Core distinction
- **Church fixed engraving material:** derived from identifiable **biblical sanctuary/temple objects**, not generic landscapes, arbitrary abstract ornament or secular scenery. Select one scripturally grounded object per section; extract micro-details for subtle banknote/intaglio-style hatching. Reuse as that section's stable identity.
- **Second-screen narrative SVG:** the user's Moses crossing the Red Sea poster is the **specific reference for that second-screen feature**: sparse flowing contour lines, parted negative space and minimal silhouettes. Do not replace the church's fixed object-based material with the narrative SVG.
- Both are expressions of one existing OS engraving grammar, not two design systems. Source text, historical interpretation and artistic license must remain distinguishable.

### Initial biblical object registry

| Section candidate | Object / engraving detail | Scriptural anchor | Theological reading (editorial interpretation, not automatic literal symbolism) |
| --- | --- | --- | --- |
| Church home | Solomon's temple pillar pomegranates / networked capitals | 1 Kings 7:18–20, 42 | Fruitfulness / temple beauty |
| Bible study / ONE | Golden lampstand: branches, almond-blossom cups | Exodus 25:31–40; Revelation 1:20 | Light / witness |
| Prayer / worship | Sanctuary veil: woven folds and cherubim motifs | Exodus 26:31–33; Hebrews 10:19–20 | Holiness / access |
| Testimony / mercy | Mercy seat and cherubim: wing-feather details | Exodus 25:17–22 | Presence / mercy |
| Baptism / church life | Bronze Sea: vessel rim, lily form and water | 1 Kings 7:23–26; 2 Chronicles 4:2–5 | Cleansing / preparation |

### Source and design constraints
1. Read and cite the biblical object passage **before** drawing; distinguish tabernacle objects from Solomon's temple objects and later temple periods. Never present a speculative reconstruction as exact biblical appearance.
2. Each section gets **one dominant object**, with only a close-up fragment rendered as engraving material: seed lattice, bronze curves, textile weave, feather contour, carved rim, etc. The motif should be recognizable when explained, but remain low-contrast beneath text.
3. Engraving geometry should be object-derived, with directional hatch, tonal hierarchy and local negative space. Avoid wallpaper repetition, guilloché-for-its-own-sake, unrelated scenery, black-gold palettes or busy religious clip art.
4. Keep the existing OS typography, color tokens, contrast, responsive behavior and single CSS authority; no new parallel manager or compulsory CI.
5. First prototype: **pillar pomegranate** for the church fixed material, **Moses crossing** as the independent second-screen narrative SVG. Validate both separately against the existing live PR preview and user-provided visual reference.
6. Record artwork provenance, object/scripture mapping, reuse rights, actual preview URL, and screenshot approval here before promoting any motif from `candidate` to `approved`.

**Spiritual design intent:** an atmosphere rooted in biblical objects and the language of worship rather than worldly landscape decoration. This is an art-direction principle, not a claim that an ornamental image itself possesses spiritual power.


### Micro-crop correction — banknote-scale biblical details (2026-10-15)

**Supersedes the framing of the initial object registry, not its scripture mapping.** The approved art-direction *scale* is far tighter than a complete temple object or full motif:

`biblical object → one decorative detail → partial micro-fragment → monumental crop → low-contrast engraved hatching`.

- Pillar pomegranate (1 Kings 7:18): a **portion of the crown or skin curve**, not a full fruit, cluster or column.
- Lampstand almond blossom (Exodus 25:33): **part of one petal**, not the seven-branched lampstand.
- Temple lily (1 Kings 7:19): **one curling petal edge**, not the whole lily or capital.
- Veil (Exodus 26:31): **a few interwoven threads**, not a complete hanging curtain.
- Cherubim (Exodus 25:20): **a small wing-edge fragment**; feather anatomy is artistic interpretation, not textually specified.

**Composition:** crop the fragment beyond the page edge; retain generous negative space, soft tonal hierarchy and delicate engraved strokes. **Never** tile complete icons or fill a page with repeated flowers, fruit or obvious religious clip art. The result may be abstract at first glance, but its precise biblical provenance must remain documented. This is a fixed section material; the second-screen Moses SVG remains a separate narrative illustration. **Status:** specification only, pending visual prototype.
