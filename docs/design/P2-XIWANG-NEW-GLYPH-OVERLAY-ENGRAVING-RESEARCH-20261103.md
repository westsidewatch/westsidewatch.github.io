# 《西望》大字海報｜重新製字與七層疊合刻線 — 多雷探索（二次定向）

**2026-11-03；research only / no renders / no new SVG / no P2 runtime changes.**  
此文件為使用者最新藝術指示，**取代**過去的 A2 機械大黑字及 B2 七排橫向彩色字組的設計方向。已淘汰的刊頭／西望 SVG 僅是歷史研究證據，**不可複用其中任何字形 path 作為新稿字骨**。保留已有 v1/v2 檔案以便工程回退，但不視為可改造母本。

## 研究主題：不是效果，而是《西望》兩字的重新製作

**A（單一巨字海報）**：一組繁體「西」「望」，上西下望，字字豎正；需要設計獨立的字骨、內白、筆畫收束、上下視覺重心與幾何關係。前幾輪「Noto 拉大／黑體直接改角／在淘汰的刊頭 SVG 上描畫」均告失敗。A 不使用毛筆字，不靠線紋，幾何化也不可犧牲「西望」在三秒內可辨。

**B（七層重疊海報）**：使用者給的深灰原參考海報，其精髓是**大字、網點、同心曲線、方向線、放射線，形成一個有疏密張力的連續編輯構圖**，而不是七條各自獨立、等寬、等大的色彩字樣。七組「西望」各自有不同的**字形細節、刻線生成邏輯及 Design OS 色**，但必須全都**豎直（0° 旋轉）、在同一畫面層疊／穿插、有共同版心與重心**。允許精準控制的平移和尺度變化，不得排成七個互不相關的橫向商品標籤；背景無底紋、無放射裝飾，**刻線全部受字形區域約束且避開字內孔洞**。七個顏色是七個版塊的 OS tokens，而非自行發明的霓虹色。疊合時必須能辨別七個字組的出現層次；首讀為西望。

**不要混淆兩種「七」**：首頁七重折疊（seven full-plane fold reveal）是既有的捲動進場機制；B 的七個有色刻線字組是靜止海報的藝術構圖。前者不能變成七條彩帶，後者不能被做成七張並排的條碼。右側 5:8 正式封面、03 Emmaus Doré、教會及 OS 都不動。

## 外部成熟代碼與新發現：按「實際問題→代碼→風險」對照

| 課題 | 候選與原始來源 | 具體適用能力 | 狀態／風險 |
| --- | --- | --- | --- |
| **重新製作漢字形** | [FontForge](https://fontforge.org/docs/scripting/python/fontforge.html)；[source license](https://github.com/fontforge/fontforge/blob/master/LICENSE) | 可單獨調 Bézier contours、`contour.balance`/`harmonize`/`simplify`、判自交、輸出 SVG；適合作為**字形雕刻台** | **優先成熟工具**；FontForge 整體 GPLv3-or-later，作獨立本地工具使用，不將其程式碼複製入主站 |
| 字形 source／外形分析 | [fontTools pens](https://fonttools.readthedocs.io/en/latest/pens/index.html)／[fontTools](https://github.com/fonttools/fonttools) | 從**另行選定且授權清晰的字型／原創路徑**提取、分析、重組每一個子構件 | **優先成熟工具**，MIT；它不會自行產生高品質新海報字 |
| 幾何重組與負形 | [skia-pathops](https://github.com/fonttools/skia-pathops)；[PathBool.js](https://github.com/r-flash/PathBool.js) | Boolean difference、union、intersection；處理複合字孔與筆畫交接 | **採用成熟 pathops 為可靠後端**（BSD-3-Clause）；PathBool MIT，作者明言早期開發，作可視化探索／交叉驗證 |
| **無外部底紋的真刻線** | [penfill](https://github.com/piLeoni/penfill) | `Region(outer,holes)`，直接在字形幾何之內產生 zigzag、concentric、stipple、waves、sunburst、cross，支援自訂 `pattern`，**輸出已經裁切好的 strokes**，不用依賴在瀏覽器做 pattern mask | **最契合 B 機制的新研究候選**，MIT/Apache-2.0；GitHub 專案較新（查得 18 commits），先測字洞／尖角／窄筆，不能稱已成熟驗收。npm/PyPI 發行狀態須先實查，不可假定包管理器可直接安裝 |
| 跟隨字形本身的刻線 | [d3-contour](https://github.com/d3/d3-contour)，[d3-shape](https://github.com/d3/d3-shape) | 值場等值線、波浪／方向線／徑向曲線，交給幾何 clipping，再受字形的內白與筆段朝向約束 | 已有成熟生態，仍只在構建時使用；不能隨意填滿背景 |
| 細線輸出與性能整理 | [vpype](https://vpype.readthedocs.io/en/latest/)，[線條整理方法](https://github.com/abey79/vpype/blob/master/docs/cookbook.rst) | `linemerge`／`linesimplify`／multi-layer SVG；後製 7 層密集刻線，控制檔案大小與過量 DOM | 成熟 CLI，僅 build-time，不能過量優化致字內角點破壞 |
| 漢字骨架的進一步探索 | [FANGCUN](https://github.com/beastt1992/fangcuntw) | KAGE/GlyphWiki 基礎的繁體漢字參數化 stroke skeleton，理論上可控制端點／轉角／字重 | **僅研究**：README 明確出現 `[FILL]`、`[VERIFY]`，稱屬實驗系統；數據授權需核對，不能當成已核實、可直接使用的字母本 |
| 生成式 glyph 模型 | [VecGlypher](https://github.com/xk-huang/VecGlypher) | Apache-2.0 的以 SVG path tokens 為序列的研究程式，可參考字形變化機制 | **僅研究**：re-implementation，僅兩筆公開提交；其 README 未確認指定繁體「西」「望」的品質與現成訓練權重，不當成成熟可施工開源服務 |
| 字筆順研究 | [KanjiVG](https://kanjivg.tagaini.net/svg-format.html) | 區分筆畫及結構件的 SVG 資料模型 | **不作正式母本**：其資料是 CC BY-SA 3.0，主要為日語書寫與筆順，不能不核實字形及授權便導入 Westside 海報 |

## 真正縮小與原參考差距的設計措施

**A** 不再問「該套哪個濾鏡」，而是讓「西」與「望」各有可編輯的**原創部件**。先制定兩字 shared stroke grammar（轉角、切面、弧面、末端、內白）再在 FontForge／pathops 重畫，最後作 optically centered 的巨字滿版構圖。無論幾何如何誇張，**必須先單色、無效果地成立**。不能以 rejected SVG 或舊海報描成新稿。

**B** 先有 7 層可維護的輪廓及 shared editorial skeleton（不是同一張黑體輪廓七次複製；需每層有可見但克制的字骨差異）。每層單獨定 `region(xi, wang, holes)`，再生成個別方向線／网點；**線條出字即被裁切，不要再採「整頁生成刻線→clipPath」的做法**。最後以同軸正立的多層印版形式疊合，七色只是幫助讀者辨認層次而非各組獨立排列的理由。若高密區難讀，以 line spacing、opacity 和 knockout 區域平衡；背景始終乾淨。

### 與參考差距的量測方式

1. **可讀性**：縮圖與 1648 實寸第一眼辨識「西望」，而非某種字體特效／七段彩色品牌 logo 清單。
2. **七層**：一個聯結的整幅構圖內看得到各刻線系統，**七層全都 0° 傾斜**，重心沒有七次平移導致坍塌。
3. **線條的所有權**：字外無刻線、字內孔洞沒有錯填、細線不依附一張混亂紋理底圖。
4. **源碼清晰**：7 個 `data-word-layer`，各自的顏色 token、字骨、行為和 line family；靜止畫面也成立，七重折疊入場另由原 scroll owner 控制。
5. **工程**：獨立 build-time native SVG，1648／768／390／320、反向滾動、reduced motion、Chromium/Safari 真截圖；字骨與版式須人工確認，CI 不等於藝術驗收。

## 狀態與保護

**2026-11-03：完成研究及選型／語義修正，沒有製作任何圖片或字稿，沒有改 P2 poster JS/CSS/SVG，也沒有合併主站。** 前版 A2/B2 仍在 Draft 供回退，但**藝術上已被否決**。下一輪如要製作，請以本研究為設計 authority，勿再引用舊稿的 path 當作新母本。
