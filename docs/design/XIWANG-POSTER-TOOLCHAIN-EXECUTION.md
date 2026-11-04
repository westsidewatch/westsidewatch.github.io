# 《西望》Poster Toolchain — 從工具研究到真正執行

**2026-11-03 · Design OS 編輯手冊的執行章節；僅針對 A/B 原生 SVG 海報製作。**
**Authority:** [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) → [Poster Generation Resource Atlas](P2-XIWANG-POSTER-GENERATION-RESOURCE-ATLAS-20261103.md) → 本工作流。這不是第二套 OS；既有 P2／右側 5:8 正式封面／Church／Emmaus／首頁七重折疊的 runtime 不因此改動。

## 一、核心修正：書籤不等於執行工具

過去的失敗：收錄了專業海報、漢字字骨、線場、套印、版式與 SVG 工具，但執行時跳過「選用→實測→輸出」而直接生成點陣效果圖。結果只得到類似海報的視覺草圖，未實際使用工具設計可編輯字骨、七層字內刻線與 P2 可用母本。

**新停止線：** 每輪海報製作前，先走工具路由；實驗記錄須分開標示 `researched`（讀過文檔）、`available`（在當前執行環境可用）、`executed`（有命令/操作與實際輸出證據）、`reviewed`（人工評價已完成）。沒有可查證的操作與輸出，禁止把它寫成「使用了工具」；沒有 browser proof，禁止聲稱「最終驗收通過」。

**使用者的圖像參考**是構圖/刻線準則，不是可直接挪用的字稿或背景。**圖像生成**只准用於明確授權的概念比較；最終交付是 build-time 原生 SVG；不得把生成的 raster 誤充 SVG 字骨。主站不添加任何付費／未知 runtime 依賴。

## 二、每次開始海報工作時必須先做的路由

| 階段與決策 | A：單組正立巨字「西」上「望」下 | B：七組正立「西望」同版心疊合 | 可核對的證據 |
| --- | --- | --- | --- |
| **0. Editorial direction** | 讀 [mono-color-skill 的 SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md)，選一個視覺事件、留白區、紙／墨角色；無需生成 raster | 同樣取其「一個視覺主題、結構性留白、精簡資訊」；**不得套用其兩色上限取消 B 的七個 OS 語義色** | 策略稿：核心視覺事件、留白比例、取捨、色彩的設計理由 |
| **1. Letterform** | 用 [KAGE Editor](https://github.com/kurgm/kage-editor)／[Kumiko](https://github.com/chiakich/kumiko-font-editor) 拆分筆段，或 [Inkscape](https://inkscape.org/) 原創兩字輪廓；選真正可執行、可輸出 SVG 的方案 | 七組各自具可見但克制的字骨差異；不要拿 A 的 outline 換七種顏色 | 字段 SVG/path + 使用哪個編輯器、版本/操作、輸出路徑 |
| **2. Constructive geometry** | [skia-pathops](https://github.com/fonttools/skia-pathops)（BSD-3-Clause）清理 union/difference、字洞；[Graphite](https://github.com/GraphiteEditor/Graphite) 可作外部形變實驗 | 同樣處理七組獨立字形與 inner counters | 字形黑白試驗 + 輪廓/字洞 QA，不僅是有文字的截圖 |
| **3. Engraving within glyphs** | 不需要，A 要先單色成立 | [d3-shape](https://github.com/d3/d3-shape)／[d3-contour](https://github.com/d3/d3-contour) 生成七類實際線場；[penfill](https://github.com/piLeoni/penfill) 是待實測的字洞區域候選；[vpype](https://github.com/abey79/vpype) 可後製路徑。**線條必須在字內，字洞留白；所有字組 0° 傾斜** | 線場 source/seed、七個 `data-word-layer`、裁切方式與字洞/小尺寸實圖 |
| **4. Composition** | 以 [flowshape](https://github.com/Jossifresben/flowshape) 的版式資料/比例與越界拒絕方法做不同構圖，再按 OS 校正；不必安裝整個 engine | 以一個連續張力、疏密與版面主次整合七層；不可變七行彩色單字 | 同等尺寸 A/B 版式比較，解釋失敗方案 |
| **5. Native export** | 獨立可編輯 `.svg` | 7 個獨立 word layers 的 `.svg`，刻線無字外延伸 | SVG 原始檔、重建步驟、授權和 hash；可用 SVGO/PathOps，但不得破壞 ID |
| **6. True review** | 與正式右 5:8 封面合成對照 | 同左 | 1648、768、390、320px、200% zoom、reduced-motion、鍵盤、正逆捲動、實際 browser 圖像；OS 10 項 rubric + 藝術判定 |

此表是「**應該調用**」的路由，不是「已安裝／已成功用過」的聲明。當工具不可用時：先記錄實際缺口，再選有同等能力與清楚授權的本地替代並執行；不能只寫一段假裝使用了 d3 / penfill / Inkscape 的描述。

## 三、Mono-color Skill 的確切定位與授權

- **專案**：[yanliudesign/mono-color-skill](https://github.com/yanliudesign/mono-color-skill)（README 標示 v1.2.0）；[SKILL.md](https://github.com/yanliudesign/mono-color-skill/blob/main/SKILL.md)、[Visual references](https://github.com/yanliudesign/mono-color-skill/blob/main/REFERENCES.md)。
- **適用**：編輯海報的 *art-direction* 決策。其單/雙油墨、主輔印版、25–55% 有意義留白、單一視覺焦點、不自動做舊、不複製參考，可幫助約束過度複雜的 B。
- **不適用**：不能把它當作「直接生成可編輯七層 CJK SVG 刻線」的引擎；其範例圖片不是可再用字骨；其中一/雙色油墨預設不高於現有 B 七個 Design OS 版塊色彩的人工決定。可以先作限色構圖對照，再回到 B 的七色語義層；不要硬把七色全部變成高飽和面積。
- **授權**：`LICENSE` 為 MIT（軟體／Skill 指令），保留原著作權及授權聲明；`ASSET-LICENSE.md` 明確指出 `examples/` 原創圖像不屬於 MIT，不可未授權商業重製；12 張第三方參照圖權利仍屬原作者。**只連結／借規則，不把第三方圖像拷到主站。**
- **啟動條件**：任何「雜誌海報、單雙色套印、編輯印刷、字即海報」任務，先讀其 `SKILL.md` 並抽取適用章節；它不會因為手冊有連結就被 AI 自動安裝或調用。Claude Code 可獨立安裝於本機 `~/.claude/skills/mono-color`；其他代理需明確讀取來源，並保留 Westside Design OS 權威。

## 四、可執行入口與失敗處理

工具路由查核入口：`node scripts/xiwang/poster-toolchain.mjs plan a` 或 `plan b`。它檢查當前執行環境有無優先工具／模組，印出適用任務和缺口，**不假裝安裝、也不會自行出圖**。

每一輪以 `node scripts/xiwang/poster-toolchain.mjs init b /tmp/xiwang-b-receipt.json` 建立空白執行記錄；逐階段填入 `status=executed`、實際操作/命令、輸出檔案及評價。最後執行 `node scripts/xiwang/poster-toolchain.mjs verify /tmp/xiwang-b-receipt.json`。驗證器拒絕沒有實際存在的證據檔案或未完成階段。實驗證據放隔離 Draft，不以 `static/images/xiwang-poster-*-v2.svg` 的舊稿當作新稿。

**注意：** 自動驗證僅能核對記錄/檔案存在與某些 SVG 語義，不能證明字形藝術品質，更不能取代人類視覺驗收；任何編輯器操作、安裝或圖像對照仍需要在可用環境真正執行。

## 五、下輪 B 海報第一個實作回合（不是再次搜工具）

1. 以 `mono-color-skill` 規範做**一頁不出圖的藝術方向記錄**：單一「西望」主視覺、暖紙白或有理由的中性灰、7 色低面積語義、明確留白、只有必要刊次資訊。
2. 實際執行一個可重現的七組字骨/線場原生 SVG 方案。先試一組字的 inner counters + flow/wave，與另外一組 dot/concentric 的真實路徑；成功再擴至七組。不可用單張 raster 替代。
3. 線條只存在字內、七組均正立、穿插同一版心，**不傾斜、不獨立排七行、不用黑底，不加版塊小圖示／城牆／目錄**。最後再評 OS 字重、對開裁切和整體廣告海報的主次。
4. 只有 tool receipt、SVG 原件、真實瀏覽器預覽和人工評價全部齊備，才可將候選提交藝術驗收；CI 通過並不等於達標。

**Release boundary:** 本章只指示在 P2 Draft 進行 *offline* 工具使用，並不授權修改 P2 顯示 JS/CSS、右頁、Church、Emmaus、正式主站或七重折疊運作。
