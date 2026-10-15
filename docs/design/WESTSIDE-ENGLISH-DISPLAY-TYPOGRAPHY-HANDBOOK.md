# Westside Watch — English Display Typography Handbook

Status: Design OS editorial manual · living reference · 2026-10-14
Owner: Westside Design OS. This document is a handbook within the existing OS, **not** another CSS authority, subsystem, or CI gate.

## 00. 本手冊的地位與使用方法

這是 **Westside Design OS 內部唯一的英文大標題編輯設計訓練與實戰手冊**，適用首頁、First Look、Journal、專題、作者、人物、黎明書局、橄欖山、教會、天堂電影院及工具層。它不是新增 CSS 系統、CI 或獨立設計權威。每次新頁面開工，先依本手冊決策；完成後把經驗回寫此一 MD。排版師、AI agent 和開發者使用相同規則。

**規範狀態標籤：** `[OS]` 已採納的本站規則；`[STUDY]` 經來源目錄或公開說明支持、但尚未逐頁讀完的研究線索；`[EXPERIMENT]` 待實際頁面對照驗證的數值或構圖。不得將建議比例冒充書籍原文或業界強制標準。

## 01. 核心參考與來源紀錄

**Bodoni Editorial Book** — 本站首個批准的視覺啟發參考；大型 Didone 字母作為版面主體、半版面英文構圖、留白與輔助資訊形成節奏。尚未核實具體書目、作者、出版年份及授權，不能虛構出處或聲稱已逐頁閱讀。保留名稱並等待原始作品頁面驗證。[STUDY]

以下來源已核實書目或官方內容介紹，但**不代表已閱讀全書**：

| 書籍／作者 | 可核實資料 | 本刊研究任務 |
| --- | --- | --- |
| *Editorial Design: Digital and Print* — Cath Caldwell / Yolanda Zappaterra | Laurence King, 2014, ISBN 9781780671642；https://us.laurenceking.com/products/editorial-design | 封面、開篇、內容結構、圖片與文字、數位與紙本編輯系統 |
| *Thinking with Type*, 3rd ed. — Ellen Lupton | Princeton Architectural Press, 2024；https://ellenlupton.com/Thinking-with-Type | 字距、字偶距、階層、對齊、網格、視覺群組 |
| *The Elements of Typographic Style* — Robert Bringhurst | Hartley & Marks；https://www.canadiantypography.ca/en/resources/book/the-elements-of-typographic-style-131 | 字體節奏、比例、閱讀與內容的關係 |
| *Making and Breaking the Grid* — Timothy Samara | Rockport；https://assets.peoplesgdarchive.org/item/18714/making-and-breaking-the-grid | 網格的建立與有意識突破、非對稱布局 |
| *Grid Systems in Graphic Design* — Josef Müller-Brockmann | 書目與版次待逐一核實 | 網格、比例、空間模組；不得把數值規則直接歸因於作者 |
| Alexey Brodovitch / *Harper's Bazaar* | 作品與各期版權資料待核對 | 雜誌跨頁、極端留白、字體與圖像的戲劇性互動 |
| *Eye* / *Emigre* / *The New Typography* — Jan Tschichold | 具體期號／版本待核實 | 字體實驗、現代主義、反例與可讀性邊界 |

**研究筆記格式：** 書名／版次／頁碼或作品期號／來源 URL／圖片授權狀態／原作具體觀察／可轉移規則／不宜照搬之處／Westside 實驗 URL／前後截圖／驗收結論。沒有頁碼或原圖時只可記為研究假設。

## 02. 版面出現英文時的第一個判斷

[OS] **先判定文字角色，再決定字級。** 不能因為是英文就全部放大。從下表依序選擇，遇到同一畫面多個標題時只能有一個主要焦點。

| 文字角色 | 視覺功能 | 常用位置 | 建議處理 |
| --- | --- | --- | --- |
| Brand / masthead | 識別，不是每次的內容焦點 | 頁首、首頁角落 | 固定識別比例，避免與主題大標搶位 |
| Display / hero | 以字母形成主畫面 | 全屏 First Look、專題首屏 | 全版或半版大型字母；可用明確的換行設計 |
| Feature opener | 引領長篇文章 | 雜誌專題開篇、章節開頭 | 1/2–2/3 版面的文字主體，與導語形成層次 |
| Section heading | 分隔內容層級 | 第二層欄目、書局分類 | 正常大標，短而明確；不得每節都用全版 |
| Article title | 識別文章 | 列表、卡片、文章頁 | 以閱讀和掃描優先；只在文章開篇升格 |
| Person / author name | 人物識別與主視覺 | 橄欖山人物、作者專頁 | 人名可放大，但不能遮臉、手、關鍵身體輪廓；已有海報資產優先 |
| Pull quote / scripture | 情緒或思想重心 | 經文頁、見證、引言 | 挑出焦點短語放大，保留完整語義與來源 |
| Deck / standfirst | 解釋主題 | 主標下方或側欄 | 顯著小於主標；不可冒充第二個主標 |
| Eyebrow / kicker | 欄目、編號、文類 | 頂部、主標上方 | 小字、真 small caps（適用時），避免巨大化 |
| Navigation / CTA / folio | 操作與定位 | 導航、按鈕、頁碼 | 維持 UI 尺度，不使用封面級字體 |
| Caption / credit | 來源與輔助 | 圖下、頁腳 | 清晰優先；不得以細小到無法閱讀為代價 |

## 03. 什麼時候需要大字母排版？

[OS] 同時符合以下多數條件才啟用 **monumental display**：

1. 這一屏是開篇、封面、專題轉場、人物主題或值得停留的經文／宣言，而不是普通內容列表。
2. 有一個可清楚提煉的短語；通常 1–8 個英文單字較容易形成強圖形，長句應先編輯分層。
3. 文字本身有足夠的內容重量，能成為主圖而非裝飾。
4. 版面至少能留出可辨識的對照空間：中文、照片、刻線、導語或安靜留白。
5. 不會損害資訊取得、點擊操作、字體辨識或響應式閱讀。

[OS] **不使用**：密集導航、搜索結果、工具表單、連續多個列表標題、長篇正文、需快速掃描的資訊頁、狹小且無法安全重組的容器、缺乏實質焦點的普通小節。

[OS] 同一屏的大字母主視覺最多一組。相鄰多屏需要節奏：大型 → 正常 → 大型或大型 → 留白／圖像 → 正常，不應連續堆疊巨字。

## 04. 位置手冊：全版、半版、正常標題及其他

以下比例是本站**設計起點**而非書籍定律，須用實際字形寬度與頁面截圖修正。[EXPERIMENT]

| 版位 | 適用條件 | 文字佔位建議 | 對齊／構圖 | 禁忌 |
| --- | --- | --- | --- | --- |
| 全屏主視覺（Full-bleed） | 封面、First Look、節期宣言 | 主字群佔內容區寬約 65–95% | 單一焦點、可局部越界但不能失去必要內容 | 每行自動換行、壓住導航 |
| 左半版（Left-half） | 右側有人物／中文／圖像 | 約 42–62% | 左邊大字，右邊保留安靜區 | 字擠成一字一行 |
| 右半版（Right-half） | 左側圖像或人物需優先 | 約 42–62% | 大字右置、留足安全邊界 | 壓人臉、遮手 |
| 上半版（Upper field） | 下方是圖片、影片、內容索引 | 高度約 30–55% | 靠上或居中，基線和下方內容呼應 | 主標侵入功能區 |
| 下半版（Lower field） | 上方已有強視覺，如教會藍色幕布 | 高度約 30–55% | 與頁腳、經文形成上下節奏 | 內容太低被裁切 |
| 置中宣言（Centered statement） | 短句、莊嚴場景 | 約 45–80% | 中軸、少層級、穩定 | 多行字長參差且無節奏 |
| 偏心／不對稱（Asymmetric） | 義大利雜誌式專題 | 約 45–70% | 主字群與對角輔助文字形成張力 | 隨機空白或無對齊基準 |
| 縱向字母（Vertical display） | 封面邊欄、人物海報 | 依字形和容器 | 真正縱向編排或逐字構圖，保證閱讀方向 | 用 transform 拉伸／壓扁字 |
| 圖像疊字（Overlay） | 圖像有足夠負空間 | 隨圖片安全區 | 明確對比和遮罩策略 | 擋臉、肩膀、手及重要內容 |
| 正常文章大標（Standard H1） | 文章、普通二層頁 | 依欄寬，通常 1–3 行 | 以易讀、內容層級為先 | 因品牌風格而過度巨大 |
| 區塊標題（Section H2/H3） | 清單、分類、工具 | 短行，尺寸遞減 | 可掃描的固定節奏 | 把所有 H2 當封面 |
| 引言／經文焦點（Pull quote） | 具有關鍵詞的長句 | 放大選中的 2–6 字詞 | 全文保留可讀；焦點可獨立成行 | 破壞語義、誤引經文 |

## 05. 字體系統：既有 OS 不得重建

[OS] 英文大標統一採現有 `--ws-type-display-en`（Bodoni Moda，normal 400），必要的斜體只在已批准的設計中使用；英文字標籤依 `--ws-type-display-en-sc`。不可人工加粗、拉寬、壓扁、假 small caps。中文字大標題最重，其餘非正文極細；長篇正文按閱讀字體與字重處理。所有字體、顏色、尺寸語義變數依 Design OS。

[OS] 調字距先看實際字形：Bodoni 大尺寸常需要光學微調，但**不能把固定負 letter-spacing 套到所有尺寸**；連字、標點、斜體、數字需分別檢查。使用真字體測量，禁止用 `ch` 當作保證不換行的依據。

[EXPERIMENT] 以**文字群組**設定三層尺度：hero 約正常文章大標的 1.7–3 倍、support 約 hero 的 25–55%、metadata 約 hero 的 12–22%。這是候選比例，不是硬編碼。最終字級由容器寬度、字形測量、行數和留白共同決定。

## 06. 分行與文字編輯：禁止意外孤字

[OS] 排版順序：**完整原文 → 語義分組 → 可批准的斷點 → 版位 → 真實字形測量 → 響應式重組**。禁止先寫 `white-space:nowrap` 再任意裁切，也禁止把英文整段放大後交給瀏覽器自動決定主標構圖。

[OS] 把語義上不可拆的片語標記為 inline phrase group（例如 `shall flow`、`living water`），必要時用不可斷行空格或語義 span。長片語不能硬塞時，切換已批准的分行方案，**不是讓單個字掉到下一行**。單字獨立成行只可作為有意義的編輯決定（例如刻意強調 `Grace`），必須在稿件中註明。

[OS] 至少提供三種響應式候選：wide（主視覺分行）、medium（收字級或重新分行）、narrow（降低巨字比例、改單欄或重新選擇焦點）。瀏覽器縮放等同於容器變窄，需要重新排版。英文 `text-wrap:balance` 和 `pretty` 是輔助，不是防孤字保證。不可依賴 CSS 字元數 `ch` 取代實測。

[OS] 經文不得刪改字詞、變更標點或為了美觀改寫引文。可透過結構標記控制排版，完整原文和可訪問閱讀順序不變。

### John 7:38 的批准候選

- 語義群 1：`He that believeth on me,`
- 語義群 2：`as the scripture hath said,`
- 語義群 3：`out of his belly shall flow`
- 語義群 4：`rivers of living water.`

可把群 1 在 `believeth / on me,` 分行，但必須**明確批准**，不是偶然擠出來；群 3 不可拆成 `shall / flow`。群 4 可分成 `rivers of / living water.`，因為這是有意識的兩行主標構圖。中文翻譯為獨立次要文字，極細且有句尾防孤字規則。

## 07. 圖片、刻線、中文、留白的組合

[OS] 先安排不可遮擋區（人物臉、手、經文、導航、CTA），再配置字母和背景。圖像與字母可以相互遮擋**只有在具體資產經批准**且仍可辨識時才允許。既有十二講員海報及其英文字體與人物比例關係不得被全站 UI scale 任意破壞。

[OS] 雕刻線、幾何、材質必須是 Design OS 現有語法。大字母與刻線的對比可以透過疏密、方向、明暗建立，但不能另起配色。中文不是填空物件：位置由語義與閱讀順序決定。留白應當能解釋其功能（呼吸、轉場、聚焦、平衡），而非未使用的空間。

## 08. 具體工作流程（人與 Agent 共用）

**輸入卡**：頁面／版位、英文原文、中文對應、重要性、視覺資產、不可遮擋區、可用容器寬高、操作元素、當前 Design OS scope。

**決策順序**：
1. 確定此處屬於 §02 的哪一種文字角色。
2. 依 §03 判斷需要 monumental 還是 standard title；寫一句理由。
3. 從 §04 選一種主要版位，最多一種變體，不堆砌多套系統。
4. 依 §06 編輯英文的語義群與批准斷點；標記不可拆詞。
5. 依 §05 設定字體階層；依 §07 安排圖片、中文、刻線。
6. 實作時僅使用 Design OS token 與頁面 scoped geometry；避免多套競爭的 `!important`。
7. 對相同文字生成 wide / medium / narrow 三組排版。
8. 在**已部署的 PR 預覽**核對實際截圖，不以 CI PASS 當成設計 PASS。
9. 修正到符合 §09 後，再申請合併；不能自行合併尚未批准的版面。
10. 將成功與失敗案例回寫 §10，成為下一次自動決策的先例。

**輸出卡**：選用版位／不選其他版位的原因／語義分組／字級比例／中英文層級／容器斷點／前後截圖 URL／驗收結果／Design OS 更新位置。

## 09. 驗收矩陣

| 檢查 | PASS 條件 | FAIL |
| --- | --- | --- |
| 語義 | 原文完整，斷行經批准 | 單字意外回行、改寫引文 |
| 字形 | 真實 Bodoni，無拉伸／假粗 | 字形變形、假 small caps |
| 比例 | 主標明顯但不壓其他層級 | 所有字都巨大或毫無主次 |
| 安全區 | 人像、導航、中文、CTA 可讀 | 互壓、裁切、溢出 |
| 刻線 | 不搶文字、屬於 OS 色材 | 新造配色或高干擾背景 |
| 響應式 | 寬／中／窄與瀏覽器縮放都合理 | 任一尺寸孤字或截斷 |
| 來源 | 學習成果可追溯 | 虛構書目、頁碼或規則出處 |
| 工程 | 一套權威、PR 截圖可見變化 | 多組 `!important` 互相覆蓋 |

**建議驗收樣本** [EXPERIMENT]：390、700、820、1024、1440、1920 CSS px；瀏覽器 80%、100%、125%、150% 縮放；另外驗證半屏與整屏。對實際產品以容器尺寸優先，不把此組數字寫死成所有頁面的媒體查詢。

## 10. 常駐能力：練習、記錄、回歸

### 訓練任務 A — 同一句英文，六個位置

對同一句真實標題各做：全版、左半版、右半版、上下半版、正常文章標題、人物圖像疊字。每個版本記錄版位理由、斷行、閱讀順序、中文字位置、響應式結果。目標不是全部採用，而是能說明**為何某版不適合**。

### 訓練任務 B — 同一版位，三種文字長度

短（1–3 詞）、中（4–8 詞）、長（9 詞以上）各做三組容器尺寸。對長標題先編輯焦點，不靠暴力縮小全部文字。

### 訓練任務 C — 失敗反證

故意製造孤字、過度壓縮、文字壓人、中文搶位、刻線干擾、假粗等案例；記錄原因與可重複的修正方法。每次新設計先比對失敗庫。

### 訓練任務 D — 書籍學習回寫

每核實一個實際作品頁面，填 §01 研究筆記格式，再挑選一條原則在本站同一頁 A/B 對比。區分「書中觀察」「本站推導」「已驗證的 OS 規則」，禁止混淆。

### 記錄模板

```md
### Case ID / date / page / PR
- Source evidence (book/edition/page or URL):
- Typography role and chosen placement:
- Why monumental / why normal:
- Exact English wording and approved phrase breaks:
- Chinese role, image and safe areas:
- OS tokens / scoped layout:
- Wide / medium / narrow screenshots:
- Browser zoom and container measurements:
- FAIL observations:
- PASS evidence:
- Reusable rule to add or amend:
```

### 版本管理

本 MD 是長期手冊；任何新設計都能引用它。修改已驗證規則時要附案例與原因；未經驗證的內容保留 [EXPERIMENT]，不可悄悄升級成 [OS]。不另建管理入口，不新增獨立 CI；已有 Design OS 驗收可引用手冊標準。

## 11. 對應現有工程

- Design OS 總綱：[`WESTSIDE-DESIGN-OS.md`](WESTSIDE-DESIGN-OS.md)。
- 編輯字體既有權威：[`WESTSIDE-EDITORIAL-TYPOGRAPHY.md`](WESTSIDE-EDITORIAL-TYPOGRAPHY.md)。
- 唯一 runtime 入口：`static/css/westside-design-os.css`。
- Canonical token 資料：`design-system/tokens/westside.tokens.json`。
- 首個實戰：PR #1325 的約翰福音 7:38 半屏版面；**尚未通過英文孤字與完整視覺驗收，不可當成成功案例。**


## 12. 第二輪研究（2026-10-14）：編輯節奏、跨頁構圖與響應式字母

### 12.1 證據層級

本輪閱讀了下列**公開文章、作者原文及出版商介紹**；沒有取得或通讀全部付費書籍，因此只記錄有來源可核查的內容。書籍尚待逐頁閱讀的規則繼續標記 [STUDY]；本站據此制定的操作政策標記 [OS]；數值及新版型標記 [EXPERIMENT]。

| 來源 | 已核實觀察 | 對本刊的可操作轉化 |
| --- | --- | --- |
| Ellen Lupton, *Thinking with Type*, 3rd ed., 2024（作者介紹） https://ellenlupton.com/Thinking-with-Type | 研究 kerning、tracking、balance、grid、alignment、Gestalt | 對大字母先做字形、留白、群組關係檢查；不把字級當唯一尺度 |
| Ellen Lupton, *White Space*（作者原文） https://ellenlupton.com/White-Space | 網格支撐非對稱與留白；留白是有意安排的構圖要素 | 主標佔半版時，另一半必須有明確的安靜功能，不強行填滿 |
| Cath Caldwell & Yolanda Zappaterra, *Editorial Design: Digital and Print*（出版商及章節目錄） https://www.laurenceking.com/products/editorial-design ; https://www.oreilly.com/library/view/editorial-design/9781780676265/ | 封面、出版物內頁、建立版面、編輯技能是不同研究對象 | 不以一套 hero 字級覆蓋封面、文章、目錄及工具頁 |
| Andy Clarke, *Art Direction for the Web*（出版社章節介紹） https://www.smashingmagazine.com/2019/04/art-direction-release/ | 包含網格、字體、圖片、CSS 排版與多裝置藝術指導 | 把「何時／為何使用巨字」寫入版位決策，不只記錄技術 |
| Andy Clarke on Bea Feitler（有原作案例的研究文章） https://www.smashingmagazine.com/2019/10/inspired-design-decisions-bea-feitler/ | 單頁需精心構造，同時要有前後頁節奏；文中提供《Harper's Bazaar》案例 | 新增連續屏節奏審核：巨字後不必仍是巨字 |
| Andy Clarke on Otto Storch（有《McCall's》案例） https://www.smashingmagazine.com/2020/03/inspired-design-decisions-otto-storch/ | 大標與圖片可統一跨頁；中縫與跨欄成為設計要素 | 網頁半版要考慮欄間距與跨欄，而非只按 50/50 切割 |
| Andy Clarke on Herb Lubalin（含作品案例） https://www.smashingmagazine.com/2020/04/inspired-design-decisions-herb-lubalin/ | 字母排列、字距與行距能形成可辨認的圖像構圖 | 設立 phrase-as-shape 版型，先定語義，再定字群形狀 |
| Andy Clarke on Neville Brody / *The Face* https://www.smashingmagazine.com/2020/03/inspired-design-decisions-neville-brody/ | 有網格作結構，局部可打破；文字出血及縱向標題屬特定藝術指導 | 只有非關鍵裝飾性文字可經批准出血；不變形字形 |
| Andy Clarke on *Avaunt* magazine https://www.smashingmagazine.com/2019/06/inspired-design-decisions-avaunt-magazine/ | 模組網格可支持多樣化標題與圖像比例 | 同一 OS 的不同欄位布局不等於新增設計系統 |
| Andy Clarke on *Pressing Matters* https://www.smashingmagazine.com/2019/07/inspired-design-decisions-pressing-matters/ | 複合網格和不同大小的區塊形成快慢節奏 | 封面、長文、索引的字母密度應有對比 |
| Matthew Butterick, *Practical Typography*, headings / hard line breaks https://practicaltypography.com/headings.html ; https://practicaltypography.com/hard-line-breaks.html | 標題層級宜精簡；有意義的斷行可避免不合邏輯的最後一行 | 正常標題優先清楚；巨字需人工批准換行點 |
| Butterick, kerning / letterspacing https://practicaltypography.com/public/kerning.html ; https://practicaltypography.com/letterspacing.html | kerning 與整體 tracking 不同；小型大寫字母可適當加 tracking | Bodoni 大寫與小寫分別處理，不能所有尺寸共用一個負字距 |
| MDN, text-wrap / container queries https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap ; https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Containment/Container_queries | balance 有行數限制，容器查詢按容器尺寸而非 viewport | 禁止只靠 balance 防孤字；半屏需基於實際容器重排 |
| Andy Clarke, Benton Modern responsive case https://www.smashingmagazine.com/2015/05/benton-modern-typography-case-study/ | 同一 HTML 可做形式化與表現性兩種響應式排版 | 語義內容不因布局切換而複製、刪改或失序 |

### 12.2 本刊新增：Editorial Rhythm（連續頁面節奏）

[OS] 編輯設計單位是**相鄰的 3–5 個畫面**，不是一張截圖。設計一個巨字首屏時，必須同時檢查上一屏和下一屏的文字重量、留白、圖片與行為。用以下角色編排，不是用固定模板重複：

- **Accent**：巨字主視覺；使讀者停留，只有一個強焦點。
- **Bridge**：中等標題或短導語；建立語義過渡。
- **Reading**：正常文章標題、正文與圖片；以閱讀效率為先。
- **Quiet**：安靜留白、細標籤或獨立圖像；恢復視覺呼吸。
- **Index**：可掃描目錄、卡片、工具導航；不使用整版巨字。

[EXPERIMENT] 以 `Accent → Quiet → Reading`、`Accent → Bridge → Index`、`Reading → Accent → Reading` 作為首批節奏候選。並非強制每三屏循環；真正規則是相鄰畫面的注意力層級不得機械重複。

### 12.3 新增版式判斷：文字是圖像還是標籤？

[OS] 大標題可以作為**視覺主圖**，但它仍然是文字，必須有可讀的語義。使用前回答：

1. 讀者先看字，還是先看人物／影片？誰是主角？
2. 字母的整體外形（長條、方塊、階梯、斜向）是否有意設計？
3. 哪些短語可以成行，哪些不能拆？
4. 字母是否佔用唯一的可操作空間或人物安全區？
5. 另一半版面是必要的輔助資訊，還是刻意的留白？
6. 縮窄後要重新分行、降低尺度、改位置，還是退回正常標題？

若無法回答第 2、3 題，先用正常標題，不得僅把字級放大。

### 12.4 六個版位的具體排版動作

| 版位 | 優先方法 | 可批准的戲劇性處理 | 何時退回正常字級 |
| --- | --- | --- | --- |
| 封面／全屏 | 以一個語義群作主圖；輔助資訊退至邊界 | 大字母跨欄、留白包圍、明確分行 | 主標過長、與主導航衝突 |
| 左／右半版 | 用字群的真實寬度定欄，對側留出圖片／中文 | 主字群非對稱、與對角小字平衡 | 實際字群寬度不足而形成孤字 |
| 上／下半版 | 同時測高度、行數、頁腳安全區 | 標題與上下場景呼應 | 高度不足或主標壓到頁腳 |
| 普通文章 H1 | 清晰的 1–3 行標題，與導語成組 | 少量字距與行距調整 | 幾乎所有普通文章都應使用此角色 |
| 人物標題 | 遵守已批准的人像與海報安全區 | 人名與人物層次交錯（資產特批） | 遮臉、手、肩，或失去姓名辨識 |
| 引言／經文 | 將真正焦點詞放大，其餘降級但保留原文 | 片語作字母圖形，譯文形成對位 | 語義無法合理拆分、引文被截斷 |

### 12.5 Responsive Art Direction：不是只縮放

[OS] 大字母標題的媒體查詢不是唯一依據。**先以實際容器可用寬度測量**，再考慮裝置寬度。不同頁面同為 820px viewport，左側還有側欄、或僅佔半版時，字體可用寬度完全不同。

[OS] 標題有三種**不同的排版狀態**：
- `monumental`：寬容器，字母作主圖，編輯批准的分行。
- `editorial`：中容器，維持焦點與對位，但可重組分行及欄位。
- `reading`：窄容器，回到清晰標題；完整內容仍在。

[OS] 過渡條件應由**文字實測寬度、行數、可用高度、其他內容安全區**決定，而非只憑固定 700px／1024px。使用 `@container`、`cqi`、`clamp()` 時仍需提供 fallback。瀏覽器 `text-wrap:balance` 可協助普通短標題，不能代替經文或巨字的語義分行審核。

[OS] 禁止 `transform:scaleX/scaleY` 改變字形比例；禁止只為消除孤字而不合理地縮小整個版面。字距以字體本身 kerning 為起點，再做具體光學判斷；對不同長度標題不要盲套同一負 tracking。

### 12.6 本輪反證：為什麼普通標題不能照搬巨字規則

Butterick 的標題建議偏向克制與清楚，而 Lubalin、Brody 的案例鼓勵表現性排版；**兩者並不矛盾**，因為面對不同版位。[OS] 普通 H1／H2 先遵守資訊層級，巨字是編輯批准的藝術指導例外。若每個 H2 都巨大，真正的封面主標反而失去特殊性。

### 12.7 John 7:38 實戰驗證卡（尚未 PASS）

- 角色：下半屏 scripture editorial / asymmetric half-spread。
- 主要焦點：`rivers of living water.`；可選擇 `rivers of / living water.` 的**批准分行**。
- 前置句：`He that believeth on me,` 必須作為可讀的語義群；是否分為兩行須由版式批准，不得因字寬偶然換行。
- 中間句：`as the scripture hath said, out of his belly shall flow`；保證 `shall flow` 不分離。
- 中譯：極細，從屬但清晰，不作裝飾性填充。
- 背景：刻線作低干擾材質，不能壓字。
- 需驗證：全屏、約 820px 半屏、窄屏、125%／150% 縮放；保存同尺寸前後截圖。
- 失敗標記：目前歷史截圖出現 `flow` 孤行及字群被動換行；不可以 CI PASS 宣稱設計成功。
- 下一次實作前，先給出 `monumental / editorial / reading` 三個經批准的分行方案，再調整 CSS。

### 12.8 常駐訓練的新增考題

- **辨識題**：隨機挑 10 個站內英文標題，分類為封面、半版、文章 H1、section、人物、引言或 UI；寫出不使用巨字的理由。
- **構圖題**：相同標題在左半版、右半版、下半版各排一次，必須標出安全區與字群輪廓。
- **節奏題**：連續 5 屏只能有 1–2 個 Accent；比較讀者注意力路徑，不以漂亮截圖代替整體體驗。
- **反證題**：用 820px 半屏及 150% 縮放測試；任何孤字、字形拉伸、中文壓字、刻線干擾即 FAIL。
- **回寫題**：每次研究必須增加可查證來源、具體版位判斷、失敗反例及至少一個待測實戰案例。禁止只增加風格形容詞。

本輪研究**只更新本手冊**，不改動尚未批准的 PR #1325 視覺版面；不新增 CSS 權威、第二套設計系統或獨立 CI。


## 13. 第三輪研究：Lubalin 字母造形 × Feitler 編輯節奏 × 可實作的 CSS

### 13.1 研究範圍與證據

本輪專攻兩種互補能力：**把英文字群排成可辨識的視覺形狀**，以及**讓不同頁面的文字重量形成節奏**。來源採用公開案例分析，不宣稱已取得原作印刷檔、閱讀完整專書或驗證每張圖片的版權。

- Herb Lubalin 研究案例與現代 CSS 解構：Andy Clarke, “Inspired Design Decisions: Herb Lubalin,” *Smashing Magazine* (2020), https://www.smashingmagazine.com/2020/04/inspired-design-decisions-herb-lubalin/ 。關注字距、連結字形、尺度對比、排版即圖像。[STUDY]
- Bea Feitler 研究案例與響應式藝術指導：Andy Clarke, “Inspired Design Decisions: Bea Feitler,” *Smashing Magazine* (2019), https://www.smashingmagazine.com/2019/10/inspired-design-decisions-bea-feitler/ 。關注整個編輯序列的視覺節奏，以及跨頁中的圖片／文字協作。[STUDY]
- Ellen Lupton, *Thinking with Type*, https://ellenlupton.com/Thinking-with-Type 。補足字形、群組、視覺階層與對齊的分析詞彙。[STUDY]
- MDN `@container`: https://developer.mozilla.org/en-US/docs/Web/CSS/CSS_containment/Container_size_and_style_queries 。為網站的版位響應提供技術參照。[STUDY]
- MDN `text-wrap`: https://developer.mozilla.org/en-US/docs/Web/CSS/text-wrap 。`balance` 是輔助，不是保證保留語義片語的工具。[STUDY]

**轉化原則：** Lubalin 的字形實驗不等於本站可以任意變形 Bodoni；Feitler 的印刷跨頁也不能直接照搬到窄屏。以下是本站從參考案例提出的規範與實驗，不是引用作者原話。

### 13.2 Lubalin 路線：Phrase as Shape

[OS] 英文大標在構圖前先寫一張「文字形狀卡」：

| 檢查項 | 決策問題 | 交付物 |
| --- | --- | --- |
| Meaning | 哪個片語承擔真正重點？ | 原文與焦點片語 |
| Silhouette | 字群應形成矩形、階梯、楔形或垂直軸？ | 2–3 個黑白線框草圖 |
| Optical spacing | 哪些字母組合產生過密／過鬆？ | 實際字體下的檢查截圖 |
| Contrast | 字級差異是否真的產生層級？ | Hero／support／metadata 比例 |
| Counterspace | 字群外的留白是否支撐內容？ | 中文／圖片／CTA 安全區 |
| Semantics | 分行是否保留完整語義？ | 經批准的 phrase breaks |
| Reflow | 窄容器如何改形狀？ | 三種狀態草圖 |

[OS] 優先從 **字群比例、留白、字距、斜體對比、對齊方式** 建立形狀；不拉伸 glyph、不任意重疊關鍵字、不用不可訪問的 CSS 偽元素替代原文。

#### 四種字群造形

- **Block / Monument**：兩三行相近寬度，形成完整的文字塊；適合封面與強主題。[EXPERIMENT]
- **Stair / Cascade**：有意識的短長交替；適合人物、專題開篇，但不得造成孤字。[EXPERIMENT]
- **Hinge / Pivot**：一行小字引導下一行巨字；適合經文焦點與標語。[EXPERIMENT]
- **Counterpoint**：英文字群與中文短句或人物在對角位置互相平衡；適合半版。[EXPERIMENT]

### 13.3 Feitler 路線：Spread Sequence 而非重複 Hero

[OS] 每個第一眼頁面必須附「前後畫面」的節奏標記：`accent`（巨字）、`bridge`（過渡）、`quiet`（留白／圖像）、`reading`（正常標題與正文）、`index`（導航／索引）。同一個 Design OS 允許不同編輯角色使用不同字體尺度。

[EXPERIMENT] **五屏節奏表**（設計起點，不是固定輪播公式）：

| 屏 | 角色 | 英文處理 | 中文處理 |
| --- | --- | --- | --- |
| 1 | Accent | 大字母作主視覺 | 少量輔助，避免雙主角 |
| 2 | Quiet | 小型標籤或不出英文大標 | 靜謐文字或圖像 |
| 3 | Reading | 正常 H1 + 導語 | 可讀正文 |
| 4 | Bridge | 中型章節標題 | 短句對位 |
| 5 | Accent / Index | 依內容價值決定是否再次巨字 | 清楚索引或輔助 |

[OS] 此表不取代頁面內容決策。只有內容本身值得成為焦點，才使用 Accent；不可為湊節奏強制放大。

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

### 13.6 技術模式 C：編輯節奏作為內容資料，而非新增設計系統

```json
{
  "pages": [
    {"slug": "first-look", "editorialRole": "accent", "headlineMode": "monumental"},
    {"slug": "church", "editorialRole": "quiet", "headlineMode": "standard"},
    {"slug": "journal", "editorialRole": "reading", "headlineMode": "standard"},
    {"slug": "feature", "editorialRole": "bridge", "headlineMode": "editorial"}
  ]
}
```

這是**內容審核資料示例**，不是要求新增 runtime JSON 或管理檔。真正使用時，頁面可用既有 scope 或 CMS 元資料表達；所有字體、顏色、尺度的共享值仍由 Design OS 控制。

### 13.7 這一輪新增的驗收

1. **Shape check**：字群輪廓是否在遠觀時成立？與留白、圖片是否有可解釋的關係？
2. **Meaning check**：大字母是否仍能正確讀出完整標題？不可意外拆開 `shall flow`。
3. **Sequence check**：同一瀏覽路徑中，相鄰 3–5 屏是否有快慢節奏，而非全部巨字？
4. **Container check**：對 390／700／820／1440px 等實際容器做截圖；不得用 viewport 寬度冒充內容欄寬。
5. **OS check**：沒有硬編碼新字體、新色彩、新系統；沒有堆疊 `!important` 補丁。
6. **Evidence check**：沒有逐頁閱讀的書籍，不可寫成「書中第 X 頁指出」；技術示例未部署就必須標示為示例。

### 13.8 下次實戰：同一英文標題的三個候選

以 John 7:38 現有內容建立 **Block / Hinge / Counterpoint** 三個草圖，並保留中文、刻線、頁腳不變。先對比文字群組形狀與孤字，再決定一種，不能同時引入三套生產 CSS。將最終版寫成一個 scoped composition，通過實際部署截圖與縮放驗收後，才把它升格為 [OS] 的成功案例。

本輪只補充研究、HTML/CSS 示範與驗收方法；沒有改動 PR #1325 的預覽頁，也沒有新增獨立管理工程。


## 14. 第四輪：Bodoni 大型英文字母的光學排版（研究與實戰）

本章屬於現有 Design OS 英文大標手冊，不建立第二套字體管理或獨立 CI。區分 **[OS] 本站採納規則**、**[STUDY] 待進一步驗證的來源觀察**、**[EXPERIMENT] 待實測的技術候選**。本輪未取得所有印刷專書全文，不能冒稱逐頁閱讀。

### 14.1 參考資料與核查事項

- Bodoni Moda 字體資料：https://fonts.google.com/specimen/Bodoni+Moda ；原始碼與版本：https://github.com/indestructible-type/Bodoni 。研究 Didone 字形的高對比筆畫、字偶與不同大小的顯示效果。實際網站所載字體檔、italic 和可變軸須另行核實。[STUDY]
- Matthew Butterick, *Practical Typography*：https://practicaltypography.com/kerning.html 、https://practicaltypography.com/letterspacing.html 、https://practicaltypography.com/line-spacing.html 。區分字偶距、整體字距與行距。[STUDY]
- Ellen Lupton, *Thinking with Type*：https://ellenlupton.com/Thinking-with-Type 。研究字形、視覺群組與字體層級。[STUDY]
- MDN：font-kerning https://developer.mozilla.org/en-US/docs/Web/CSS/font-kerning ；font-optical-sizing https://developer.mozilla.org/en-US/docs/Web/CSS/font-optical-sizing ；font-synthesis https://developer.mozilla.org/en-US/docs/Web/CSS/font-synthesis ；hanging-punctuation https://developer.mozilla.org/en-US/docs/Web/CSS/hanging-punctuation 。研究瀏覽器實作與相容性。[STUDY]
- W3C CSS Fonts Level 4：https://www.w3.org/TR/css-fonts-4/ 。用於檢查字體特性及相關規範。[STUDY]

### 14.2 五個不能混淆的決策

| 技術 | 目的 | 本站規則 |
| --- | --- | --- |
| Kerning | 修正 AV、To、Wa 等字偶的視覺間距 | [OS] 先用真字體 kerning，再考慮人工調整 |
| Tracking | 調整整行字母疏密 | [OS] 不用單一負 letter-spacing 套全部字級 |
| Optical sizing | 依字體支援的光學尺寸調整字形 | [EXPERIMENT] 先核實 font face 是否含 opsz |
| Line spacing | 調整多行大標基線與呼吸 | [OS] 按版位與字形測量，不照搬封面行高到正文 |
| Optical alignment | 標點、圓形字母與欄邊的視覺齊整 | [OS] 原文標點保留；調整須局部驗證 |

**操作次序 [OS]：** 核對字體 → 確認原文與語義分行 → 決定欄位和字級 → 設行距 → 檢查 kerning → 微調 tracking → 校正邊緣 → 多尺寸驗收。不能用壓縮字形、變形或無限縮小字體修復版面錯誤。

### 14.3 字體正體、斜體和大小寫

[OS] 英文大標採現有 Design OS Bodoni Moda、正常 400 字重。斜體只在確實載入真 italic font face 時使用；不得用 skew 製造斜體。不得合成粗體或 small caps。標題採用的 Title Case、sentence case、真 small caps 必須依內容角色選擇，不可全站強制大寫。經文大小寫和標點不得為視覺效果任意改寫。

[OS] 正斜體的切換必須有語義焦點，如強調 “living water.”；不能每個詞隨機切換。特別檢查斜體尾端與標點、相鄰字母是否碰撞。

### 14.4 四種版位的光學優先順序

| 版位 | 先檢查 | 再調整 |
| --- | --- | --- |
| 全屏巨字 | 語義分行、整體字群外形、留白 | 字級、字偶、邊緣光學對齊 |
| 左右半版 | 真實容器欄寬、中文與人物安全區 | 分行、字級、局部字距 |
| 正常文章 H1 | 易讀性、行數、標題階層 | 行高、必要時 balance |
| Small caps 標籤 | 真字體是否存在、資訊可辨識 | 合理 tracking、基線對齊 |

### 14.5 CSS 範例 A：光學排版的安全起點

以下為**尚未部署的 scoped 實驗示例**；共享字體與顏色仍以 Design OS token 為準。

```css
.ws-display-optical {
  font-family: var(--ws-type-display-en);
  font-weight: 400;
  font-synthesis: none;
  font-kerning: normal;
  font-optical-sizing: auto;
  font-variant-ligatures: common-ligatures;
  letter-spacing: normal;
  line-height: 1.02;
}
.ws-display-optical--monumental { line-height: .98; }
.ws-display-optical--standard { line-height: 1.12; }
.ws-display-optical em { font-style: italic; }
```

`font-optical-sizing:auto` 只在實際字體具備相應光學軸時生效。不能因為 CSS 屬性存在就宣稱視覺改善。[EXPERIMENT]

### 14.6 CSS 範例 B：標點懸掛及回退

```css
.ws-display-punctuation { hanging-punctuation: last allow-end; }
@supports not (hanging-punctuation: last allow-end) {
  .ws-display-punctuation { hanging-punctuation: none; }
}
```

[EXPERIMENT] 此屬性需要實際目標瀏覽器支援驗證。不得用偽元素重建經文標點，亦不可在全站套用負 margin 假裝已完成光學對齊。

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

### 14.8 測量與驗收

[OS] 每個大型英文字母案例都記錄：實際 font family、字重、字體樣式、是否有真 italic／opsz；原文及批准斷點；容器寬度；標題實際邊界和溢出；各行字寬與孤字；中文、圖片、刻線、CTA 安全區；同尺寸前後截圖；最終 PASS/FAIL。

```js
// DevTools diagnostic example, not production runtime.
const title = document.querySelector('.ws-optical-title');
if (title) {
  const box = title.getBoundingClientRect();
  const css = getComputedStyle(title);
  console.table({
    font: css.fontFamily,
    weight: css.fontWeight,
    style: css.fontStyle,
    kerning: css.fontKerning,
    opticalSizing: css.fontOpticalSizing,
    width: box.width,
    scrollWidth: title.scrollWidth,
    lineHeight: css.lineHeight,
    letterSpacing: css.letterSpacing
  });
}
```

`scrollWidth` 可檢查溢出，**不能單靠它偵測孤字**；仍須用 Range 行框、截圖或人工審核。驗收至少覆蓋約 390、700、820、1440px 的實際容器，以及 100%、125%、150% 縮放。CI PASS 不是視覺 PASS。

### 14.9 四項常駐練習

1. 同一句 “living water.” 比較正常字距、人工 tracking 與真斜體，逐一核對字形、空白與標點。
2. 在半版測 “He that believeth on me,”，禁止 “on” 或 “flow” 意外獨佔一行。
3. 對比 “rivers of / living water.” 的兩行巨字與一行正常 H1，說明版位與內容角色差異。
4. 以同一真實頁面測 125% 和 150% 縮放，記錄何時必須從 monumental 切換為 editorial 或 reading。

**反證：** 字體沒有 opsz 時不能聲稱 optical sizing 有效；瀏覽器不支援 hanging-punctuation 時不能聲稱標點已校正；若縮字距造成字母碰撞或增加孤字風險，該版本 FAIL。

### 14.10 本輪結論與下一步

[OS] **先確保字形真實、語義正確、版位合理，再進行光學微調。** Bodoni 的高對比字形可以成為本刊視覺特色，但字體工程不可替代編輯判斷。下輪應以實際載入字體、半版寬度與對照截圖驗證以上候選，再將成功數值或行為提升為可復用的 OS 規則。

本輪只補充手冊，不修改未獲批准的 PR #1325 視覺頁面，也不建立第二套系統。
