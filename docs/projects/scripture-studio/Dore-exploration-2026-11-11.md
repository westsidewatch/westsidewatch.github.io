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
