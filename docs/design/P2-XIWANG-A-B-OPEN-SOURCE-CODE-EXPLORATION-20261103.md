# 多雷探索｜《西望》A 幾何字骨、B 七組刻線海報的開源代碼

**日期：2026-11-03**　**狀態：已完成來源研究、適配方案；未安裝新依賴、未替換 P2 artwork、未聲稱渲染驗收。**
**唯一 Design OS 編輯入口**：`WESTSIDE-EDITORIAL-MANUAL.md`；配合 `P2-XIWANG-CAMPAIGN-POSTER-SEVENFOLD-20261103.md` 使用。

## 0. 研究範圍及決策

這是編輯手冊定義的「多雷探索」，意思是 **針對既定設計目標，研究成熟作品／真實開源代碼／授權／維護／免費使用／可工程重用性，再提出能與原 P2 無縫對接的實作路線**，不是搜尋古斯塔夫・多雷的插圖，也不是使用出圖工具。

設計目標按使用者最新決策修改：

- **A = 只有一組、兩個巨型繁體字「西」「望」。** 純粹現代幾何字形／內白／重組；不再是常規粗黑體加一條斜線，也不靠毛筆、刻線填充、圖畫當主體。
- **B = 三至七組「西望」，首輪以七組研究最完整。** 各組使用**不同的生成刻線機制、不同的 Design OS 版塊色、不同的版式尺度／位置**；不是 A 的兩個字外輪廓塞七個紋理。
- 左頁是獨立 1:1 雜誌 Campaign Poster，右頁為已核定 5:8 Magazine Cover；Magazine 不用 Doré 圖，Doré 留在 Emmaus；左邊舊七條彩帶導航退役，七個全幅折幕可導入海報。
- 外部庫**優先只在構建時使用**。P2 runtime 保留乾淨的原生 SVG/CSS/現有 scroll 函式，不把大型編輯器、Python GUI、Qt、Rust WASM 或新動畫 runtime 帶進瀏覽器。
- **用戶提供的粉紅紅字、灰底刻線海報是設計參照，不是已授權的素材或可照搬的原作。**

### 選型評估

狀態：
**採用**＝最先做可重現的 offline proof；**候補**＝有用途、但可能難以移植／需要額外依賴；**排除**＝與設計目標、授權或成本不符。開源程式碼授權與生成作品權利是不同概念。活躍度以 2026-11-03 GitHub repo `pushed_at` 為輔助指標，並不代表經過 API 實作驗收。

## 1. A｜字型／字骨重構：9 個候選

| 優先 | 真實來源 | 授權／近期更新 | 能實際做什麼 | 判斷 |
| --- | --- | --- | --- | --- |
| **A-01** | [PathBool.js](https://github.com/r-flash/PathBool.js) · [Shape Builder Demo](https://r-flash.github.io/PathBool.js/) | **MIT**；2026-09 有提交；作者標明**早期開發** | 對 SVG `path` 做 union、difference、intersection、fracture；把構件組成幾何字、挖掉有意義的字內白 | **採用・主字形引擎**，但必須以複合輪廓 holes 等 stress tests 避免產生錯誤拓撲 |
| **A-02** | [Paper.js](https://github.com/paperjs/paper.js) · [官方網站](http://paperjs.org/) | **MIT**；2026-11 有提交 | 成熟 path/compound path 和 `unite`／`subtract`，重新修整 Bézier 曲線、控制光學重量和局部圓角 | **採用・布林核對／曲線精修**；一律 offline 輸出 native SVG |
| **A-03** | [opentype.js](https://github.com/opentypejs/opentype.js) · [示範](https://opentype.js.org/) | **MIT**；2026-08 更新 | 讀 OTF/TTF/WOFF 裡的「西」「望」字形 Bézier outlines，輸出 path 作字骨基底 | **採用・來源輪廓解析**，不是現成藝術字產生器 |
| **A-04** | [fontTools](https://github.com/fonttools/fonttools) · [文件](https://fonttools.readthedocs.io/) | **MIT**；2026-11 有提交 | Python 離線抽出／驗證輪廓、TTF/OTF/UFO 資料、subset、檢查 contour | **採用・建構工具**；不進瀏覽器 |
| **A-05** | [skia-pathops](https://github.com/fonttools/skia-pathops) | **BSD-3-Clause**；2026-02 有提交 | Skia path union/difference/intersection/xor，作 PathBool 對 CJK 複合輪廓的**獨立布林驗證** | **採用・備援品質工具**，Python offline |
| **A-06** | [Glyphr Studio 2](https://github.com/glyphr-studio/Glyphr-Studio-2) · [實際編輯器](https://www.glyphrstudio.com/app/) | **GPL-3.0**；2026-10 更新 | 直接人工編輯兩字的節點、字腹、部件比例；可離線／網頁單獨使用 | **候補・獨立編輯工具**。不嵌入／複製 GPL 编辑器程式到站點；匯出的自創作品權利由創作者決定 |
| **A-07** | [Maker.js](https://github.com/microsoft/maker.js) · [官方文檔](https://maker.js.org/) | **Apache-2.0**；2026-10 更新 | 程序化直線、弧、幾何模型、分層 SVG、參數化楔角 | **候補**：適合輔助幾何基準，不宜以 CAD 自動化替代字形光學設計 |
| **A-08** | [SVG.js](https://github.com/svgdotjs/svg.js) | **MIT**；2026-08 更新 | SVG DOM path／group／transform／animation 操作 | **候補**：現有原生 SVG DOM 已夠用，只有互動字形設計台需要時才用 |
| **A-09** | [bouffont](https://github.com/meodai/bouffont) | **MIT**；2026-10 更新 | 從字型抽 skeleton 並重建膨脹 lettering；可生 SVG | **研究但不採為主案**：泡泡字／骨架膨脹傾向與要求的幾何強結構不一致，亦需核實大型 CJK 字支援 |

**字型來源授權：**若使用 Noto Sans CJK TC／Source Han Sans 作初始可改編字骨，必須核對實際 `Sans/LICENSE`（[Noto 官方庫](https://github.com/notofonts/noto-cjk/blob/main/Sans/LICENSE)，**SIL OFL 1.1**）；標註母本來源，按 OFL 及作品形態保留必要授權文字，不帶第三方受限 font bytes 進輸出，不把外部字型本身轉成 Westside 官方自有獨立授權字型。最終海報是兩字自訂 SVG path；不要把「可免費瀏覽的字體」誤當可隨意移植。注意 OFL 對再發布字體衍生品與使用字體製作的圖形作品區分，發行前按具體輸出核對。

**A 推薦施工管線：**

```text
有授權的「西」「望」初始輪廓
   → opentype.js / fontTools 提取各自 glyph path
   → PathBool.js: 拆解、加楔、union、difference，重新組織字骨與字內白
   → Paper.js / skia-pathops：修曲線、核對複合 path holes
   → 人工 optical pass：內白、筆畫重量、兩字頂／中／底的承重與對頁節奏
   → A1: 僅 xi.svg + wang.svg 兩組獨立 SVG paths
   → Chromium 實際像素及 320px 等縮放驗證
```

PathBool 官方真實可用 API（**程式使用示例，非已安裝/跑通**）：

```js
import * as PathBool from 'path-bool';
const xi = PathBool.pathFromPathData(originalXiPath);
const cut = PathBool.pathFromPathData(designedNegativeSpacePath);
const engine = new PathBool.PathBoolean([
  { path: xi, fillRule: PathBool.FillRule.NonZero },
  { path: cut, fillRule: PathBool.FillRule.NonZero }
]);
const result = engine.get(PathBool.PathBooleanOperation.Difference);
const paths = result.map(PathBool.pathToPathData); // offline SVG export
```

**一票否決：**僅用 `textLength` 拉伸粗黑字、在原版加 4 塊不相干斜切、只換配色／濾鏡、把 A 再改成筆刷，都不算重新製作幾何字型。要至少有可解釋的「西」「望」各自的構件、承重、負形設計證據。

## 2. B｜刻線生成：8 個具體開源候選

| 優先 | 真實來源 | 授權／近期更新 | 可用的紋理／生成能力 | 判斷 |
| --- | --- | --- | --- | --- |
| **B-01** | [d3-shape](https://github.com/d3/d3-shape) | **ISC**；2026-11 更新 | SVG path / Bézier / radial line / curveCatmullRom，適合同心弧、波浪、放射、非等距線 | **採用・最簡潔幾何核心**（只離線生成 path） |
| **B-02** | [d3-contour](https://github.com/d3/d3-contour) | **ISC**；2026-11 更新 | Marching Squares 等值線，從 scalar field 形成「順形刻線」而非均勻 `pattern` | **採用・順形線場** |
| **B-03** | [flow-lines](https://github.com/msurguy/flow-lines) · [DEMO](https://msurguy.github.io/flow-lines/) | **MIT**；2026-08 更新 | 從向量流場產生獨立 SVG 路徑、方向線、曲線流線 | **採用・波浪／水流／向量走向參照**；既有 app 用 Vue，**只借/改寫生成器邏輯，不引入整站 UI** |
| **B-04** | [hatched](https://github.com/plottertools/hatched) | **MIT**；最近 repo push 2025-03 | 平行線、**同心圓形刻線**、層次陰影、輸出 SVG；Python build tool | **採用・交叉／同心刻線參照**；偏 raster → SVG，字形需要手動引導 |
| **B-05** | [svg-halftone](https://github.com/evestera/svg-halftone) | **MIT**；最後 repo push 2023-08 | Rust CLI：Poisson／矩形／hex 網點、圓／六角／鑽石點，SVG 輸出 | **採用・網點參照、只用 offline**；舊專案，適合借算法不擴大 runtime |
| **B-06** | [Plottter](https://github.com/pywkt/plottter) | **MIT**；2026-10 更新 | 約 39 類生成器（多層線、密度線、contour、flow、hatch、stipple、radial），多層 SVG 匯出 | **採用・資料庫與樣本產生**；Python／Qt 桌面程式過重，不植入 P2 |
| **B-07** | [hatchsvg](https://github.com/Veedubin/hatchsvg) | **MIT**；2026-06 更新、規模小 | 彩色圖片→分色刻線 SVG，獨立 layer、hatch angles、plotter 優化 | **候補**：可研究分色與軸向線條；不推薦先把字 rasterize 再向量化 |
| **B-08** | [Krbn](https://github.com/vpalos/krbn) | **MIT**；2026-07 更新 | 曲率方向場、單／交叉刻線、可重現 SVG 畫法 | **參照但暫不集成**：主體是 3D/mesh rendering，超出純兩字海報需求 |

**另作輔助／不是獨立刻線引擎：**[SVG.js](https://github.com/svgdotjs/svg.js)（MIT）可做生成器面板，[SVGO](https://github.com/svg/svgo)（MIT，2026-10 更新）可對**凍結後 SVG** 做優化；壓縮時須保留 `clipPath`、`pattern` 的 ID、`viewBox`、個別組別 metadata 與 transform/animation owner，不因優化讓文字消失。

### 必須排除的「看似開源」候選

**[Halftone Pro](https://github.com/petra-dot/halftone-pro)**：公開 repository 和 README 中有非常貼近 B 的 Spots / Lines / Stipple / Image、交叉線和 SVG path，但其實際 [LICENSE](https://github.com/petra-dot/halftone-pro/blob/main/LICENSE) 標明 **Proprietary License**，**禁止公開再分發修改版、禁止把程式碼作商用套件整合**；而且依賴 Adobe Illustrator CEP。**不是開源碼，不能複製或植入 Westside P2。**研究其效果類型即可，**不要抄代碼**。

## 3. B 的七組「西望」與七色編輯系統：實作矩陣

優先試 **7 組，每組有可獨立識別的生成演算法 + 顏色 token + 獨立版面地位**；對 3 組與 5 組仍保留海報版面 A/B/C 測試權（不要假設七組必定最佳）。

| 組別 | Design OS 色（不可自行重命名／改值） | 西望的「刻線形成機制」 | 首選源碼 | 各自視覺責任 |
| --- | --- | --- | --- | --- |
| 01 · 教會 | `--ws-water` | 流體方向場（direction-field streamlines） | flow-lines + d3-shape | 連續流向、可讀的大形 |
| 02 · 雜誌 | `--ws-first-light` | 同心弧／局部向心場 | d3-shape + hatched | 有印版感的放射與焦點 |
| 03 · 以馬忤斯 | `--ws-pale-gold` | 有漸變密度的網點/stipple | svg-halftone + D3 | 單獨成字，不能照抄多雷 |
| 04 · 橄欖山 | `--ws-olive` | 等值線／沿形曲線 | d3-contour | 有秩序的連續 contour |
| 05 · 黎明書局 | `--ws-harvest` | 平行銅版刻線與線密度梯度 | hatched + d3-shape | 印刷方向與細部節奏 |
| 06 · Cinema | `--ws-crimson` | 交叉線／角度變化 | d3-shape | 緊張的光學明暗交錯 |
| 07 · 白晝咖啡館 | `--ws-daylight-mauve` | 放射線變距 + 局部點密度 | d3-shape + svg-halftone | 疏密聚散的收束 |

**這個配色分配只是沿 Design OS 各版塊色的工程映射；它不要求 7 組一律等大，也不強制固定網格排。** 版面先比較 7 組混排（2 大 + 3 中 + 2 小）、1 主 + 6 輔、斜向編輯序列；同一算法可先調參證明一組是真實可編輯 path，再擴至多組。刻線不能只靠 `<pattern>` 填在 A 的粗字輪廓裡：**每組 B 的字形可從 B 自有的構成骨架出發，刻線的方向和密度必須構成字、控制內白、留足辨識度。**

**線條輸出約束：**
- 每組一個獨立 `<g data-poster-word="1..7" data-engraving-family="...">`，包含「西」及「望」的可辨輪廓、生成刻線 path、OS 色。不要 7 個同一複製字組再換色。
- 所有圖樣採 source-seeded deterministic output、per-group line-density limit 和 SVG path 合併；建構結束後再做 SVGO／重放視覺檢查，避免 7×數千 DOM 節點在小屏卡頓。
- 7 重折疊只控制**入場**，不必把這 7 組「西望」做成相同摺片；舊側條永遠不恢復。
- 顏色先通過對比度測試；七個 token 與海報背景的色彩可讀性須逐項測，不改 OS token 值。
- 由 1648×928／768／390／320 與減少動效真實 Chromium 截圖驗收，還要比較全畫面 + 縮小後單張海報的字辨識度。

## 4. 工程落點與限制

**本輪只研究、比較與記錄，不改 `static/js/p2-vol00-poster.js`，不把這些庫自動加進 `package.json`。**

下一輪新稿應以 `static/scripts/...` 或設計構建腳本等**offline 開發資產**從有授權的輪廓輸出 `static/images/xiwang-campaign-a-v2.svg` 以及 `xiwang-campaign-b-7up-v2.svg`，只在 P2 Draft 的 A/B preview 開關引用；現有修復了顯示問題的 A/B v1、左頁 sevenfold、右頁 5:8 cover、Church / Emmaus 均受保護。禁止未看畫面就宣稱獲獎級、禁止非必要雲端付費依賴。

**實際選定的最短可用工具鏈**：
- **A**：`opentype.js + PathBool.js`，以 `Paper.js / skia-pathops` 精修或檢查；最後只有 SVG `path` 和必要描述。
- **B**：`d3-shape + d3-contour` 當可重用原生幾何內核，參照 `flow-lines + hatched + svg-halftone` 的不同密度／方向機制；`SVGO` 做離線輸出清理。
- **不選**：Halftone Pro proprietary；需要新付費應用的方案；將 Qt／整套 Vue 編輯器／一堆外部 WASM runtime 搬進 P2；僅調 `fill:url(#pattern)` 的「A 改色」方式。
