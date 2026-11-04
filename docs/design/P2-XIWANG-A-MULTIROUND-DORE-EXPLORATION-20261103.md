# P2｜《西望》A 巨字海報 — 多輪「多雷探索」與開源製字工具決策

**2026-11-03 · 工程前研究，禁止出圖／禁止沿用淘汰字形。**  
**目前狀態：已完成前三種不同方向的搜尋與第四輪原始碼／授權核對；工具組合僅列為優先測試，不宣稱「滿意」或「已經設計出西望」。**  
**優先級：此文件與 2026-11-03 最新用戶要求，高於既有 A1/A2 / discarded wordmark 的藝術定向；既有 preview 和右側正式封面不改。**

## I. 不再誤解「多雷探索」

按 `WESTSIDE-EDITORIAL-MANUAL.md`：真正的「多雷探索」是找到成熟作品與**可核對的開源工具／實際演算法**，比較免費成本、來源、授權、維護、可重用能力；提煉版面機制，再落到 Design OS 與真 P2 驗收。不是搜尋 Doré 插圖，更不是每次用一般黑體再加兩道斜切。

**新規（持續約束 A 後續工程）：**
- **必須多輪，不見滿意工具不草率結案：**每輪解決不同失敗根因（結構資料、字骨可塑性、節點與負形、工程品質），不能把不同搜尋關鍵詞但同類功能算作新方法；若「西」「望」的**原創結構試作**仍普通或不可辨，立即回到下一輪工具與參考探索，禁止只在現有 SVG 加濾鏡。
- 候選須有實際專案來源、授權、作者是否仍維護、功能是否完整、是否真有程式碼、是否能在 macOS 使用／離線輸出 SVG、是否會增加 P2 runtime／授權成本。
- **兩個字、豎直、各自完整：**A 不是設計一套字庫，而是設計一組現代宣傳海報字標：上「西」下「望」，不用毛筆、不要現成黑體等比放大、不要傾斜、不要多雷圖像。
- **舊 SVG 明確淘汰：**`xiwang-ink-vector.svg`、右側刊頭曾用「西望」舊字稿、`xiwang-poster-a-v2.svg` 和此前所有 rejected lettering 只作歷史失敗基線，不是可再利用的 path skeleton。
- **不出圖 ≠ 不研究**：研究／代碼核查可持續，但沒有授權的字庫、未完成的生成器、黑箱商用特效不可冒充「找到成熟開源工具」。

## II. 四輪獨立探索結果

### 第一輪｜漢字真正的筆畫構件／骨架：避開「只改整字輪廓」

| 來源 | 核實結果 | A 用途與處置 |
| --- | --- | --- |
| [Skel Sans](https://github.com/pacpapapa/skel-sans) | OFL-1.1；繁體中文；幾何骨架重建，有 Vanilla / Claw / Wiggle / Zigzag 與 wght/wdth/slnt。**實際 Git tree 只有九項、README／LICENSE／樣圖，沒有生成器代碼**；大型已編譯字體另在 Releases | **保留設計原理研究，降級為「非開源生成器」**。不可直接把既有 Noto 派生骨架當作最終「西望」 |
| [FANGCUN 方寸](https://github.com/beastt1992/fangcuntw) | **更正：**MPL-2.0；Git tree 僅 17 項，但包含 **3,609,463 bytes 的 index.html 單檔程式**，不是只有說明文件。[公開的互動 App](https://fangcuntw.vercel.app/) 呈現繁體字骨、參數、KAGE 匯入與 SVG／海報輸出；README 仍有待驗證欄位 | **升級為必須實測的候選**；原始碼存在不代表已核實「西望」的獨立修改、字內白、SVG 匯出與重建流程 |
| [KAGE Python](https://github.com/HowardZorn/kage-engine) | **真正有程式碼**：`kage/kage.py`、Sans/Serif 繪筆系統、逐字生成 SVG ；GPL-3.0，GitHub 最後推送 2023-12，字形數據需另從 GlyphWiki 提供 | **保留結構參考/可執行對照**。可研究部件與筆畫建立方式，**不直接搬其成品或舊字稿作海報正式母本**；外部 tool 與資料授權分別核對 |
| [HanGlyphComposition](https://github.com/googlefonts/HanGlyphComposition) | Google Fonts 提供 deep components 和結構資料；GitHub 網頁註記 archived/read-only | **部件關係研究用**，不是已維護的 SVG 字形設計器 |
| [Chinese Hershey Font](https://github.com/LingDong-/chinese-hershey-font) | MIT、單線漢字資料與轉換工具，但程式基於 Python 2，最近推送 2019 | **筆畫中心線研究**；不能當作符合本次字形品質的直接輸出 |
| [Make Me a Hanzi](https://github.com/skishore/makemeahanzi) | 筆畫 path 與中／繁體字資料；資料授權要逐檔閱讀，基本定位是書寫資料而非海報字型 | **只研究筆畫拆分**，不擅自把字庫資料作正式插圖資產 |

**淘汰邏輯：**「支援大量繁體漢字」不等於「有成熟的可改造原創字形演算法」。這是以前探索不夠深入最重要的誤判。

### 第二輪｜當代藝術字／字形編輯平台：區分可雕刻與只加特效

| 來源 | 能力與限制 | A 適用性 |
| --- | --- | --- |
| [Fontra](https://github.com/fontra/fontra) | GPL-3.0，2026-11 仍維護，可編輯 Bézier/二次曲線、部件、字重來源、PathOps；能以 Fontra Pak 在 macOS 使用。仍是 developing font editor | **有用的深度字形編輯對照工具**；若需真正模組化漢字版型，可試。單為兩個巨字，未必比直接 SVG 向量繪製更節省 |
| [Shift](https://github.com/shift-editor/shift) | MIT/Apache-2.0，2026-11 持續維護，支援字形外框與來源軸、UFO/Designspace/Glyphs；但 README 明言 alpha，proofing/kerning planned，macOS 13+ | **較新候補**，不能把 alpha 當作定稿字形工具可靠性保障 |
| [FontForge](https://fontforge.org/) | 成熟 FOSS 字形編輯器，可精修輪廓、交接、輸出 glyph，但主要是整套字體工程工作流 | **技術候補**，只為兩字用它全套 font project 未必最適合 |
| [GlyphDrawing.club](https://github.com/hlotvonen/glyph-drawing-club) | MIT、格網型文字組合／模組化實驗，最後推送 2023；字形符號排版，不是現代漢字筆畫輪廓生成器 | **不採作字骨引擎**，可研究模組排列的編輯原理 |
| [TYPE-O](https://github.com/lnyssen/type-o) | MIT、現成變數字體的 fracture/stencil/swell 等效果；內建字體列表主要為 Latin，並未確認支援完整繁體「西」「望」 | **排除作 A 主引擎**：字體效果鏈不等於新的獨立漢字結構 |
| [bianzhidai 2.0](https://github.com/sdfggvfvj/bianzhidai-2.0) | 用 Glyphs sources 製作多種裝飾字體，repo LICENSE 無標準 SPDX 定論，且 Glyphs 編輯依賴不是免費開源工具鏈 | **只研究模組化展示**，不複製來源、不當作滿意工具 |

### 第三輪｜真正可塑造筆畫與字內白的向量編輯引擎

| 來源 | 經官方文件核對的功能 | A 決策 |
| --- | --- | --- |
| **[Inkscape](https://inkscape.org/)** | 成熟 FOSS SVG 向量編輯器；官方文件確認 **Shape Builder、Path Union/Difference、Power Stroke、Bend、Envelope Deformation** 等 Live Path Effects。2026-05 發布 1.4.4 支援 macOS | **目前首要製字工作台**：不需要製完整字庫，就能在「西」「望」兩字上直接建立原創形體、調角、調弧、非等線筆畫、負形與重心 |
| **[skia-pathops](https://github.com/fonttools/skia-pathops)** | BSD-3-Clause；Skia 的 path union/difference/intersection/xor；有 Python API，可 build-time 清理交集／孔洞 | **首要幾何品質後端**；必須先由設計師確定字形，程式不會自動做出藝術字 |
| [Paper.js](https://github.com/paperjs/paper.js) | MIT；成熟 path 建構、變形、Boolean，便於用程式批量驗證 2 個可獨立改動的漢字部件 | **候補**：若 A 需要系統化幾何參數探索可用，不能取代手工 optical proof |
| [PathBool.js](https://github.com/r-flash/PathBool.js) | MIT；可操作 SVG path boolean，但其自身說明仍早期開發 | **備援／比較**，不再作字形研發唯一核心 |
| [fontTools SVGPath](https://fonttools.readthedocs.io/en/latest/svgLib/path/) | MIT；SVG parse/path 的 pen protocol；可由 Python 處理可重建輪廓 | **轉換／檢驗**，不是創意幾何引擎 |

**此輪的轉折：A 是只有兩字的海報字標，不是要產生幾萬個中文字。** 因此「完整字型生成器」很可能不如「手工可控的向量字形工作台 + 可重現幾何程式」有效。

### 第四輪｜原始碼存在性、授權與可部署核查

- **Skel Sans 的重要糾正**：有可用的 OFL 1.1 字體，但其 GitHub repo **沒有字骨生成程式碼**。不能再宣稱已找到可直接安裝的 Skel Sans 筆畫重構演算法。
- **FANGCUN 原始碼的更正**：repo 有 3.6 MB 單檔 index.html 程式碼，不是無源碼；公開 App 呈現繁體字參數編輯與 SVG 輸出介面。但 README 的資料集／參數欄位仍待核對；必須對實際「西」「望」進行操作測試，才能評判工程可靠性。
- **KAGE 的能力與代價**：有真可執行 Python repo，卻較老且 GPL 程式碼與 GlyphWiki 字形資料的授權是兩回事，適合作部件拆解對照，不應偷渡進本站 runtime。
- **Inkscape 的工程落點**：不需進入 PR runtime；原生 SVG 每個字獨立 path，將非標準 Live Path Effect 在輸出時正規化，交給 PathOps 清理；任何外部編輯器都不嵌進 P2。
- **授權成本**：上列優先方案為免費開源工具；母本全新構造、不使用淘汰舊字形，既可避開舊稿失敗，也降低外部字型使用條款風險。

### 第五輪｜真正能操作漢字筆畫／部件的開源工具（重要補充）

這輪專門查找是否能直接操作漢字的筆畫及構件，並核對原始碼存在性、授權、維護、和 Mac 使用條件。

| 來源 | 核查證據 | A 的實際適用性 |
| --- | --- | --- |
| **[KAGE Editor](https://github.com/kurgm/kage-editor)** | 真正有 98 項 repo tree、React/TypeScript 原始碼；可選筆畫、部件、修改控制點及起收、拆解、重排、顯示中心線。GPL-3.0，2026-06 有推送，作者宣稱測試 macOS Chrome / Firefox / Safari | **優先 CJK 筆畫建構候選**；不將 GPL 程式植入 P2，不能把內建預設 KAGE 字形不修改就當作原創巨字 |
| **[Kumiko Font Editor](https://github.com/chiakich/kumiko-font-editor)** | MIT、約 1020 個 repo tree entries，2026-09 推送；原生 React/TypeScript + IDS 漢字部件組字、節點輪廓編輯與 UFO/GitHub 工作流。README 明言現階段以「補字」為主 | **第二個優先 CJK 字骨候選**；要實測全新「西」「望」的字骨構件和輸出 SVG，而不只是對普通字庫補字 |
| **[Graphite](https://github.com/GraphiteEditor/Graphite)** | MIT/Apache-2.0、真 Rust/TS 程序式向量節點程式、2026-11 推送，約 1615 個 repo tree entries；公開 Alpha | **幾何變形的有力候選**；適合大量非破壞性曲線和負形試驗，但不是 CJK 部件專用工具 |
| **[FANGCUN](https://github.com/beastt1992/fangcuntw)** | MPL-2.0；雖只有 17 個檔案，但確有 3.6 MB 單檔 JavaScript/HTML App；公開網站展示 KAGE 匯入、繁體參數、SVG 海報匯出，README 仍有待核對數據 | **升為優先操作試驗**，必須驗證新字骨的筆畫重組而不僅是現成字型風格調參 |

**第五輪的工具鏈修正：**不能再僅以 Inkscape + PathOps 結案。先由 KAGE Editor／Kumiko／FANGCUN 三種真正 CJK 原生結構方案提出全新「西」「望」筆段，再由 Graphite／Inkscape 研究幾何負形、承重及曲面，skia-pathops 做布林可靠性檢查。任何來源只會把舊黑體加粗、加切線，應退回下一輪探索。

**目前仍未通過完整新字稿的實際試驗**，因此以上都是查證過原始碼／授權的優先候選，不能宣稱已找到藝術上滿意的工具。
## III. 條件性優先組合，不冒稱已完成

**方案 I（首選真實試做）：Inkscape SVG 手工字骨 + skia-pathops + fontTools SVGPath**。  
以最簡單的中心線及原創筆段開始，設計「西」上框承重、四周內白，再從「望」上下構件的可讀關係入手。Shape Builder 先作真正 union/difference；Power Stroke 研究非均勻筆畫重量；光學內白與二字重心須人工校準。輸出獨立 `xi`、`wang` 原生 SVG 路徑，以 PathOps 驗證孔洞和相交關係。

**方案 II（獨立驗證）：KAGE 筆畫模型作部件研究 + Fontra（或 Shift）精修 + PathOps**。  
不複製 KAGE 成品輪廓，不依賴 GPL 整合；主要比較部件語法是否比方案 I 更適合創造漢字獨特幾何字骨。若它只做出又一種機械黑體，必須淘汰。

**方案 III（嚴格備援）：Paper.js 以完全原創的筆畫／曲面模組生成路徑，再導回 Inkscape 做 optical adjustment**。  
適合真正需要参数化的楔形、弧線與留白系統；不使用 Noto 抽出再粗暴切角作捷徑。

### 「滿意工具」的真實停止條件（沒有通過就繼續探索）

1. **原始碼／工具真的能用**：不是只有 README、二進位字體、論文、影片，必須在目前環境真正執行兩字的 SVG 構造流程。
2. **創作的是字骨，不是濾鏡**：兩字各有可編輯部件／真正內白／光學承重；不能靠等比拉伸黑體和 4 個斜切片段過關。
3. **真實「西望」測試**：兩個繁體字必須能在 1648、768、390、320px 看懂，失敗就換方向；靜止單色海報先成立，再談色彩與七重折疊。
4. **與右封面成立**：P2 原版對開、右頁 5:8 正式封面不變；能顯出「左現代宣傳字標 × 右精工正式封面」。
5. **工程和權利清楚**：完整獨立 SVG paths（可反覆生成、無資料授權不確定部分）、沒有部署付費依賴、可進可退的 Draft 預覽，Chromium 真實截圖與眼睛共同判斷。
6. **失敗後不能只微調**：如果方案 I 的字骨評價仍是「普通字體加效果」，立即回到下一輪參考樣本與工具研究；不能繼續交付同類字稿宣稱進度。

**此輪只探索／寫文件，沒有產生任何畫稿、圖片、新母本 SVG，也沒有修改 P2、首頁或右側封面。**
