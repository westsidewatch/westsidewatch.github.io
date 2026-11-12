# Scripture Studio｜雙向經文鉛字印章：多雷探索 R1（2026-11-11）

## 指令定義與保護邊界

依據 `docs/design/WESTSIDE-EDITORIAL-MANUAL.md §9` 與 `docs/MASTER_SITE_ARCHITECTURE.md §9`，「多雷探索」為當前問題啟動完整外部方案發現流程，**並非 Gustave Doré 木刻風格，也不是「多雷搜索」**。不得在未驗證前宣稱得獎或完成。

鎖定：Isaiah 62:6 CUV/KJV 原文、既有七柱截圖僅為歷史對照（**不是設計限制**）、單母版旋轉 90°、Bodoni Moda SC 與 Chiron 900/200、Title Case + true Small Caps、單一中英出處「以賽亞書 Isaiah 62:6」、本地字型。不得改動主站 P2 或已驗收資產。

## 從實際作品研究到工程可移植規則（17 件）

| ID | 實例與原始連結 | 可移植構圖機制 | 判斷與禁忌 |
|---|---|---|---|
| 01 | [Cooper Hewitt — Wijdeveld / letterpress mosaic](https://www.cooperhewitt.org/2015/05/10/hendricus-theodorus-wijdeveld-letterpress-printing/) | 字本身組構建築型墨塊，母版每個欄距有承重關係 | adopt：不可複製幾何花紋 |
| 02 | [El Lissitzky — For the Voice](https://www.moma.org/collection/works/14473) | 字級差與負空間形成可讀抽象構造 | adapt：宗教經文不可破壞詞序 |
| 03 | [Jan Tschichold — Plakate der Avantgarde](https://www.moma.org/collection/works/7292) | 軸線、非對稱平衡、兩墨色 | adopt：不是空泛模仿紅黑色 |
| 04 | [Paula Scher — Public Theater](https://www.moma.org/collection/works/8840) | 以文字密度形成整體量體並創建明顯閱讀入口 | adapt：不同字體混搭不適用既定 OS |
| 05 | [Wolfgang Weingart — Swiss Poster](https://collections.lacma.org/object/207620) | 細分字距與構圖深度而不靠插畫 | adapt：不要可讀性下降與任意疊字 |
| 06 | [Studio Dumbar — ATypI](https://studiodumbar.com/work/atypi) | 大與小、柔與硬、輕與重的有意對抗 | adopt：不是仿製視覺色彩衝撞 |
| 07 | [Studio Dumbar — INTO](https://studiodumbar.com/work/into) | 文字重量的光學漸變形成概念 | adapt：OS 900/200 不任意伸縮字形 |
| 08 | [XYG Window — Chinese Seal](https://designawards.core77.com/Visual-Communication/114321/XYG-Window.html) | 印章語法抽象為可擴展的現代身份 | adopt：避免對篆書或窗花照搬 |
| 09 | [Design Trust — Ink and Architecture](https://designtrust.hk/homemade_designers/052-ink-and-architecture/) | 印記與建築式配置可具雙重閱讀 | adapt：不引入不相干的外加景觀 |
| 10 | [Met — Marinetti Words in Freedom](https://www.metmuseum.org/art/collection/search/345679) | 字形與數字成空間，經文出處可作結構節點 | reject literal：拒絕破壞聖經原文順序與意義 |
| 11 | [Grolier Club — Concrete Poetry](https://grolierclub.omeka.net/exhibits/show/after-words/experimental-typography--lette) | 詩的形體本身是版面；注意視覺與文學一致 | adopt：不可只做圖形拼字 |
| 12 | [MAMCO — Concrete Poetry](https://archive.mamco.ch/expositions/fichiers/About_Concrete_Poetry_ENG.html) | 有意義的空間張力，而非強迫填滿 | adopt：不機械追求 100% 佔有率 |
| 13 | [LSU Library — The Word Made Flesh](https://guides.lib.lsu.edu/BookArts/Typography) | 可在密集文字場中建立次級訊息 | adapt：不能使原經文難讀 |
| 14 | [Hamilton Wood Type — New Impressions 2024](https://woodtype.org/blogs/news/a-closer-look-at-letterpress-techniques-in-the-2024-new-impressions-exhibit) | 字模、遮罩、分層及印刷張力 | adapt：不要靠印刷仿舊紋理假裝成熟 |
| 15 | [Japanese Typography — Huber field study](https://typography.japan.signalwerk.ch/) | 直排旁線是資訊強調，不是水平底線直接旋轉 | adopt：中英文雙軸需各自辨認 |
| 16 | [Typotheque — CJK Typesetting Principles](https://d2jttos6a7myat.cloudfront.net/articles/typesetting-cjk-text) | CJK em-square 與垂直、標點正確性優先 | adopt：不要打亂直排標點 |
| 17 | [MoMA — Dieter Roth Gorgona](https://www.moma.org/interactives/exhibitions/2013/dieter_roth/works/gorgona/) | 標點與空白能形成主體圖案 | adapt：僅作反例檢驗，不為造型編造文字 |

## 三條路線，拒絕「只放大來源」

A / **Architectural masonry（砌字印面）**：由經文字數和字形決定的若干文字帶形成錯開的上／下階梯與承重空間，以文字重心與階梯輪廓作主要標識；經文來源依同一印面端柱合併，不重複章節；雙方向使用同一座標，僅 OS 指定閱讀權重視覺變化。

B / **Counterform chamber（留白內室）**：將一條較寬空隙用作刻意的中軸負空間，與兩組不同密度的文字形成建築入口；這是「留白具有作用」而非平衡漂亮的字距。需保證每個字、詩行與詞序沒有被修改。

C / **Typographic field（字海）**：以緊密且不規則節奏的英文字/中文字帶建立密度，出處不是附屬標籤而是墨色密度中的視覺秩序；比對時不能以重疊和誤讀作為充滿。

## 採用技術／不再重造

- 使用現成 DOM 排字、CSS writing-mode、getBoundingClientRect、Canvas/SVG 之後續真正墨跡檢查；不引入新依賴、不另開字型系統。
- 在原生成器上加入有限的空間語法選擇和連動的候選搜索評分，而非把 17 個案例各自硬編成模板。
- 各方案採同一份來源文字、一份母本，同一旋轉法；文字原文完整性單獨驗收。
- 拒絕單純加大出處、添加無意義金框／背景紋理、大面積黑底、合成 Small Caps、任意歪斜變形。

## 本輪客觀門檻與未解風險

1. A/B/C 真正是不同的間距、重心與留白語法，而非同樣畫面換顏色。
2. 兩個方向均不出界、不碰撞，中英文原文重構為 PASS，引用名稱與章節只出現一次。
3. 字型確實載入；需要真實 Chromium 桌面／手機／放大視覺證據與墨跡面積 QA；沒有實測不得宣稱已符合獲獎水平。
4. 對照手冊 §6：十項 0–2 分（意義、辨識、構圖、字體、雙色、層級、互動、手機、無障礙、可編輯），探索候選門檻 15/20，沒有重要項目零分，但不能替代正式藝術審核。

**狀態：外部研究完成、方向已轉譯；原工程迭代及實際畫面驗收進行中。**
## 使用者更正：取消任何固定字柱數（2026-11-11）

**約束更正：** 首頁、各版塊主題經文、各工具／項目經文長短不同；使用者從未批准「七柱」作印章規範。舊七柱僅是一個歷史樣本；不可以任何固定柱數規定或單一詩節的結構限制設計。生成器以字詞 token 數、字框／墨跡、雙向旋轉、完整性與構圖策略計算候選數目；為短句、長句與中英文長度失衡提供不同布局；不可為填滿強行刪改經文。V32.0 開始將固定 signatureSets 改成長度驅動的可變字柱搜尋，後續仍須補全跨經文字型資源與瀏覽器驗收。

## 工程記錄回溯：既有聖經合理斷句工具，優先復用（2026-11-11）

**重要糾正：禁止再自己發明單詞數、漢字數或任意美術斷句作為語義引擎。** 已存在 `static/experiments/scripture-studio-poetry-v18.html`（歷經 V16 → V17 → V18）：

1. V16：原文維護、中文及英文「|」人工審定詞組鎖定、語義單位完整性；不為填印面拆詞。
2. V17：**離線 USFM 詩行子集適配器**，支援 `\\id`、`\\c`、`\\v`、`\\q1–3`、`\\b`、`\\p`；保存來源與原詩行；沒有詩歌標記、存在不支援標記時拒絕；不是完整 Bridgeconn Grammar。
3. V18：在來源詩行之下由編輯批准的次級合法斷點（預設不啟用）；保留「他們晝夜必不靜默。」「呼籲耶和華的，」「ye that make mention of the LORD,」等保護詞組；可逆原文重構。V18 QA 記錄報告 Chromium 15/15 基礎測試通過，但不可外推成 V32 排字已驗收。
4. V14 硬約束 `scripture-studio-v14-hard-constraints.md`：H2 語義先行、H4 同條字帶多次中英轉換、H6 實際 advance 非均分嚴格過半、H7 無預設字帶數、H8 不縮字。

**尚未完成的接入：** V32 系列目前自行使用 `z/e` 硬編詞組及簡單 `editorialBreakCheck`，並未把 V18 的 USFM 來源、翻譯版本、合法斷點和審核狀態接入成權威語義節點。正確鏈路應為「聖經原文／USFM → V18 詩行／來源 → 人工核定語義原子 → V14 H1–H8 約束求解 → 同字帶中英多次交錯 → 旋轉雙印 → 字型及視覺驗收」。如無核定合法斷點，停止生成並回報，不能自行拆詞。

**立即修正設計審查：** 不將 V32.2 的簡單語義單位與同帶雙語檢查當作已滿足 V14 或 V18；其真正有效性待接入後實測。

## 2026-11-11｜V33.0 設計方向判決（依工程入口優先序）

**當前主線：Bible-first, constraint-first, composition-second。** 先由 V18 的 USFM/詩行/編輯合法斷點產出不可拆的雙語語義節點，再經 V14 真正的 H1–H8，最後才以設計研究 A/B/C 語法搜尋完整的字面；拒絕把放大書卷名、增加邊框、變更不等距欄距當作獲獎級設計進步。

### A/B/C 路線取捨

- **A／砌字印面：優先實驗。** 經文語義容許的字帶節奏、雙語交錯轉換與密度直接形成視覺形體；不指定字帶數，保留實際英文與中文順序，先驗證無碰撞和成片文字的墨跡外接輪廓。
- **B／負空間內室：有條件採用。** 只有當負空間真正對應自然詩行與語義停頓，才引入非對稱空間；不能用中央大空白掩蓋不合格版心。
- **C／字海：暫緩。** 在 H1–H8 尚未全通過之前，高密度擁擠與大文字面積非常容易造成字詞碰撞、錯誤斷句，先不作主線。

### V33.0 已實作（非發布驗收）

- 同一標稱字號：取消英文 62% 調節與英文主讀的 96%/60% 字號變更，保留 OS 字體及中文 900/200 字重差。
- V14 H4 的多次語言轉換嚴格過半、H6 的實際字面中英份額不均分嚴格過半：改為候選淘汰條件，而非美感分數的偏好。
- 無合法候選時停止展示舊候選，清楚回報 `NO_LEGAL_V14_CANDIDATE`，不再為了填滿版面任意拆詞。
- 生成器提供 V18 詩行／USFM 工具入口，並標記 `V18_APPROVED_BREAKPOINTS_NOT_CONNECTED`；不假稱目前硬編詞組就是核定的聖經斷句。

### 下一工序與驗收

1. 讀取 V18 `parsePoetryUSFM`、來源校驗與合法次級斷點模型，復用同一份審核後資料；產生含 provenance、translation、span、approvedBreaks 的可核對語義節點。不可以人工重打一套簡化版語義分詞來冒充接入。
2. 在 V33 求解器新增 H1/H2/H3/H5/H7/H8 的實際可觀察驗證（H4/H6 只是已增加的局部 gate），尤其兩種方向的閱讀順序、真實座標、無裁切及原文逐字可逆。
3. 以《以賽亞書》62:6、短句、長句（如路加 24:27）作壓力測試；前述字體子集僅覆蓋目前樣章，不能將其視為多卷聖經字型資產已解決。
4. 真實瀏覽器桌面、390px 手機和列印校樣的對照截圖；確認後才按 20 分內部藝術評分及外部設計標準進行選拔。

**目前狀態：V33.0 工程程式已提交、純靜態語法與規則存在性核查通過；尚無真實瀏覽器畫面、通用語義接入、完整 H1–H10 或獲獎品質驗收。**
