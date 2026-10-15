# Westside Watch — English Display Typography Handbook

Status: Design OS editorial manual · living reference · 2026-10-14
Owner: Westside Design OS. This document is a handbook within the existing OS, **not** another CSS authority, subsystem, or CI gate.

## 00. 本手冊的地位與使用方法

這是 **Westside Design OS 內部唯一的英文大標題編輯設計訓練與實戰手冊**，適用首頁、First Look、Journal、專題、作者、人物、黎明書局、橄欖山、教會、天堂電影院及工具層。它不是新增 CSS 系統、CI 或獨立設計權威。每次新頁面開工，先依本手冊決策；完成後把經驗回寫此一 MD。排版師、AI agent 和開發者使用相同規則。

**規範狀態標籤：** `[OS]` 已採納的本站規則；`[STUDY]` 經來源目錄或公開說明支持、但尚未逐頁讀完的研究線索；`[EXPERIMENT]` 待實際頁面對照驗證的數值或構圖。不得將建議比例冒充書籍原文或業界強制標準。

### 輕量接入：設計前 30 秒讀取

[OS] **只在新建或重大重排網頁雜誌版面時讀取一次**，日常文字修改、修 bug、CI、部署不觸發。這是設計師／Agent 的知識參考，不是程式執行依賴。

- **先判斷**：標題角色（§02）、是否需要大字母（§03）、版位選擇（§04）。
- **有圖片才看**：人物安全區、候選評分與字形驗證（§18–20）；純文字頁跳過。
- **直接製作**：使用既有 Design OS token、scope 和 CSS；不生成第二份規則、不重新研究、不新增自動檢查。
- **預覽才驗收**：沿用當前頁面已有的 Cloudflare 預覽；實驗室不加入 CI 必過條件。
- **例外才回寫**：只有遇到手冊沒有涵蓋且經實際驗證的新規則，才補入本 MD；一般頁面調整不回寫。

**最小決策輸出**：`文字角色 → 版位 → 人物／操作安全區 → 響應式退路`。無須填表、產生報告、跑完整研究流程或逐章重讀。

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


## 15. 第五輪：英文大標題與圖片的空間藝術指導

本輪研究**圖文主從、半版留白、人物前後景、圖片裁切、文字環繞及候選位置評估**。繼續沿用既有 Design OS；下列 CSS/HTML 是實作示例，未經實際頁面驗收不得標記為已部署。

### 15.1 研究來源及證據界限

- Otto Storch 的跨頁圖片與字母編輯構圖案例：https://www.smashingmagazine.com/2020/03/inspired-design-decisions-otto-storch/
- Bea Feitler 的編輯節奏與圖文關係案例：https://www.smashingmagazine.com/2019/10/inspired-design-decisions-bea-feitler/
- Herb Lubalin 的文字圖像化案例：https://www.smashingmagazine.com/2020/04/inspired-design-decisions-herb-lubalin/
- *Art Direction for the Web* 網頁藝術指導介紹：https://www.smashingmagazine.com/2019/04/art-direction-release/
- MDN：shape-outside https://developer.mozilla.org/en-US/docs/Web/CSS/shape-outside ；clip-path https://developer.mozilla.org/en-US/docs/Web/CSS/clip-path ；mask-image https://developer.mozilla.org/en-US/docs/Web/CSS/mask-image ；object-position https://developer.mozilla.org/en-US/docs/Web/CSS/object-position 。

[STUDY] 上述為公開研究入口，非完整印刷專書逐頁研讀。以下的版位矩陣是本站轉化後的設計判斷，不冒稱是原作者提出的硬性規則。

### 15.2 先判定圖文關係

| 模式 | 主要視覺 | 適用版位 | 限制 |
| --- | --- | --- | --- |
| Type-led | 英文大標 | 封面、經文、宣言 | 文字仍需完整可讀 |
| Image-led | 人物／照片 | 講員、人物專題 | 不壓臉、眼、手及重要輪廓 |
| Counterpoint | 圖文雙主角 | 左／右半版 | 兩側視覺重量平衡 |
| Interlock | 字母與人物交錯 | 特批人物封面 | 須有真實透明前景素材 |
| Text wrap | 圖像形狀引導文字 | 長篇開篇 | 不用於容易產生孤字的巨字 |
| Quiet caption | 圖片主角、英文輔助 | 文章與圖庫 | 正常字級，不強行放大 |

[OS] **圖像安全區優先**：人物臉、眼、手、肩部關鍵輪廓、文字、CTA 和字幕不能因為構圖而意外遮擋。既有十二講員海報的個別已批准例外繼續有效，不得用新規則覆蓋既有資產。

### 15.3 依圖片構圖選擇英文標題位置

| 圖片特徵 | 首選位置 | 退回方案 |
| --- | --- | --- |
| 主體偏右、左側有負空間 | 左半版巨字 | 左側正常 H1 |
| 主體偏左、右側有負空間 | 右半版巨字 | 右側正常 H1 |
| 人物居中、畫面滿版 | 上／下安全區 | 圖外標題 |
| 風景或建築有穩定低細節區 | 天空／牆面區 | 獨立文字欄 |
| 高密度紀實圖片 | 圖外標題 | 文章正常 H1 |
| 透明背景人物 | 特批人物前景遮字 | 半版不交錯布局 |

[OS] 單純的亮度低、色彩均勻不代表安全；圖中仍可能有重要敘事物件。不能只靠亮度或顏色演算法決定最終標題位置。

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

### 15.9 候選版位的最低限度評分

以下僅示範矩形交集與文字寬度，**不是**已完成的圖片辨識或 AI 自動排版系統。

```js
function eligibleHeadlineSlots(slots, subjectBox, titleWidth) {
  return slots.filter(slot => {
    const intersects = !(
      slot.right <= subjectBox.left ||
      slot.left >= subjectBox.right ||
      slot.bottom <= subjectBox.top ||
      slot.top >= subjectBox.bottom
    );
    const fits = slot.right - slot.left >= titleWidth;
    return fits && !intersects;
  });
}
```

[OS] 正式選位還要檢查字群高度、臉與手的禁入區、對比、可讀性、中文與 CTA、語義分行及窄屏裁切。自動評分只能提供候選，最終由編輯驗收。

### 15.10 實戰與驗收

1. **主角判斷**：人物、圖片或英文大標誰先被看到？是否符合內容目的？
2. **安全區**：不能意外遮擋臉、眼、手、重要衣物輪廓及互動入口。
3. **裁切**：desktop、半屏、mobile 的人物比例保持正常；不能拉伸。
4. **對比**：英文在實際圖片的明暗區均清晰；不能靠新增全站配色掩蓋問題。
5. **語義**：標題是可選取 DOM 文字，沒有被遮到無法閱讀。
6. **響應式**：並排不安全時改單欄或圖外標題，不縮扁字母。
7. **節奏**：連續人物頁面不機械套用同一個巨字位置。

**常駐練習**：同一張圖片分別做左半版、右半版、圖外標題；特批人像另測前景交錯。比較實際截圖與縮放結果，記錄選擇理由、失敗方案與 PASS/FAIL，再回寫 §10 案例紀錄。

本輪只補充同一份手冊；未改動 PR #1325 的視覺頁面、既有十二講員海報或全站 CSS runtime。


## 16. 第六輪：主體識別、文字安全區與最佳版位候選評分

本章讓既有 Design OS 的編輯排版手冊具備**可實作的輔助選位規格**。不新增獨立管理系統，不改動已批准的十二講員海報。研究、候選演算法與實測結果必須分開標示：[STUDY] 技術研究、[EXPERIMENT] 未驗證候選、[OS] 正式採納的規則。

### 16.1 技術研究與資料來源

| 研究對象 | 公開來源 | 可用能力 | 限制 |
| --- | --- | --- | --- |
| MediaPipe Object Detector | https://ai.google.dev/edge/mediapipe/solutions/vision/object_detector/web_js | 瀏覽器內物件偵測與 bounding box | 物件框不等於人臉、手或精確輪廓 |
| MediaPipe Face Detector | https://ai.google.dev/edge/mediapipe/solutions/vision/face_detector/web_js | 人臉位置及關鍵點 | 不能辨認人物身分，側臉與遮擋需人工核對 |
| MediaPipe Image Segmenter | https://ai.google.dev/edge/mediapipe/solutions/vision/image_segmenter/web_js | 依模型輸出像素分割遮罩 | 分割類別取決於模型；邊緣可能不準 |
| MediaPipe Pose Landmarker | https://ai.google.dev/edge/mediapipe/solutions/vision/pose_landmarker/web_js | 人體姿態關鍵點 | 手勢細節不能僅靠人體關鍵點保證 |
| OpenCV.js | https://docs.opencv.org/4.x/d5/d10/tutorial_js_root.html | 灰階、邊緣、區域紋理等影像分析 | 低紋理不代表內容上可以覆字 |
| Canvas measureText | https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/measureText | 量測字群寬度 | 不代替 DOM 的實際行高、字體載入及 CSS 布局 |
| CSS Font Loading API | https://developer.mozilla.org/en-US/docs/Web/API/Document/fonts | 等待字體載入後測量 | 必須使用實際生產字體 |
| CSS object-fit/object-position | https://developer.mozilla.org/en-US/docs/Web/CSS/object-position | 圖片裁切與焦點定位 | 偵測框必須映射到裁切後座標 |

[STUDY] 這些是官方技術文檔入口，不代表本站已安裝或驗證上述模型。**第一版優先使用人工標記安全區 + DOM 實測**，避免因模型下載、授權、效能或辨識錯誤拖慢主站。模型可作為未來的可選候選提供者，不能成為頁面顯示的必要依賴。

### 16.2 四層決策架構

1. **Observe**：輸入圖片原始尺寸、可見裁切、人物／物件框、人工指定焦點、明暗及紋理。
2. **Protect**：產生禁入區：臉、眼、手、人物輪廓、重要物件、已批准字樣、CTA、字幕與中文。
3. **Compose**：量測實際字體與批准的語義分行，產生左、右、上、下、圖外及特批交錯等候選。
4. **Evaluate**：先執行硬性安全檢查，再以可解釋分數排序；最後由編輯在實際尺寸截圖中批准。

[OS] **硬性禁入區優先於美學分數**。若候選遮住人臉或讓經文產生孤字，即使對比、留白得分再高也必須淘汰。所有候選失敗時，回退為**圖外正常標題**，不強行覆字。

### 16.3 圖片主體識別：先以可控標記建立基準

[OS] 人工標記是最初的 ground truth。每張圖片可有多個 `protectedRegions`，並區分：
- `face`：臉及頭髮主要輪廓，最高優先。
- `hands`：手勢及手部。
- `subject`：肩、身體和服裝關鍵區。
- `story`：圖片中不可遮擋的文字、物件、符號。
- `ui`：頁面導航、CTA、字幕與譯文（以畫面座標表示）。

[EXPERIMENT] 未來的模型輸出只作**建議框**，須附模型版本、置信度與人工修訂記錄。低置信度、多人像、側臉、深色刻線、手與臉重疊時，必須保守擴大安全區或停止自動覆字。不得把模型的物件類別當作人物身分識別。

### 16.4 安全區資料結構：以圖片歸一化座標記錄

```json
{
  "assetId": "example-portrait",
  "sourceSize": {"width": 1600, "height": 2000},
  "focalPoint": {"x": 0.58, "y": 0.27},
  "protectedRegions": [
    {"kind": "face", "box": [0.39, 0.08, 0.35, 0.28], "source": "manual"},
    {"kind": "hands", "box": [0.44, 0.52, 0.31, 0.22], "source": "manual"}
  ],
  "editorialMode": "image-led"
}
```

[OS] `box` 採 `[x, y, width, height]`，全部在 0–1 範圍內，相對**原始圖片**而非 viewport。這是案例資料示例，**不是要求新增第二套 runtime JSON**。已批准的人物海報可繼續用現有資產資料表達。

### 16.5 關鍵幾何：裁切座標不能直接當作畫面座標

對 `object-fit:cover`，假設原圖 `Iw × Ih`，顯示盒 `Bw × Bh`：

```js
const scale = Math.max(Bw / Iw, Bh / Ih);
const renderedW = Iw * scale;
const renderedH = Ih * scale;
const overflowX = renderedW - Bw;
const overflowY = renderedH - Bh;
// px and py are object-position proportions (e.g. center => 0.5)
const offsetX = -overflowX * px;
const offsetY = -overflowY * py;
const screenX = box.x * Iw * scale + offsetX;
const screenY = box.y * Ih * scale + offsetY;
const screenW = box.width * Iw * scale;
const screenH = box.height * Ih * scale;
```

[OS] 上述適用於常見的百分比 `object-position`、無 transform 的 `cover` 情況；實際還要加上圖片盒的畫面原點。若使用 `contain`、非百分比位置、CSS transform、遮罩或其他裁切方法，必須另行映射，不能直接沿用。映射後應與可見盒相交，移除盒外區域。

### 16.6 保護區膨脹與字群幾何

[OS] 主體框不是可貼字的邊界，必須增加 **clearance**。安全距離應由字級、容器寬度和圖片用途決定；以下為可調整候選，不是全站通用數值。

```js
function expandBox(box, pad) {
  return {
    left: box.left - pad,
    top: box.top - pad,
    right: box.right + pad,
    bottom: box.bottom + pad
  };
}
function overlapArea(a, b) {
  const w = Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left));
  const h = Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));
  return w * h;
}
```

[EXPERIMENT] 首輪可比較 `pad = max(12px, 0.25 × headlineFontSize)` 與更寬安全距離；對臉／手可另加權。不可用 padding 數值替代編輯對肩膀、衣服、手勢的判斷。

[OS] 字群測量須在 `await document.fonts.ready` 後進行。標題的 bounding box **必須包含所有行與斜體外伸、標點、陰影等視覺外延**。Canvas `measureText()` 可預估單行寬度，但正式驗收須用實際 DOM、`Range.getClientRects()` 和截圖；只量 `h1` 外盒不足以證明每一行安全。

### 16.7 候選生成：先排除，再評分

[OS] 先產生 `left-half`、`right-half`、`top-band`、`bottom-band`、`outside-image`。`interlock` 只有特批並具真正透明前景資產時才列入候選。每個候選需附：
- 標題的預估與實際文字盒；
- 所有保護區重疊面積；
- 是否有語義孤字／溢出；
- 圖文對比與局部紋理；
- 與中文、CTA、導航的距離；
- 版面角色（accent、reading 等）及編輯指定偏好。

```js
function rankCandidates(candidates, protectedBoxes) {
  return candidates.map(candidate => {
    const collision = protectedBoxes.some(region =>
      overlapArea(candidate.titleBox, region) > 0
    );
    const rejected = collision ||
      candidate.overflow ||
      candidate.semanticWidow ||
      candidate.uiCollision ||
      !candidate.readable;
    if (rejected) {
      return { ...candidate, eligible: false, score: null };
    }
    const score =
      0.30 * candidate.contrastScore +
      0.25 * candidate.negativeSpaceScore +
      0.20 * candidate.balanceScore +
      0.15 * candidate.rhythmScore +
      0.10 * candidate.preferenceScore;
    return { ...candidate, eligible: true, score };
  }).sort((a, b) =>
    Number(b.eligible) - Number(a.eligible) ||
    (b.score ?? -1) - (a.score ?? -1)
  );
}
```

[EXPERIMENT] 以上五個分數必須先正規化至 0–1；權重是**待校準起點**，不是經實驗證明的最佳係數。`readable`、`semanticWidow`、`contrastScore` 等由獨立檢測或人工輸入，**此函式本身不會計算它們**。禁止用虛構分數假裝已完成自動判斷。

### 16.8 對比度與圖片複雜度的界線

[OS] 在圖片上覆字時，先檢查文字實際覆蓋區域，而不是全圖平均亮度。對比度需採用真實前景文字色與背景像素，並考慮透明度、漸層、圖片縮放及刻線。一般文字以 WCAG 2.x 4.5:1、大字以 3:1 作基本檢查門檻；視覺主標的高對比細筆畫即使通過數值，也須做實際可讀性驗收。

參考：https://www.w3.org/WAI/WCAG22/Understanding/contrast-minimum.html 。

[OS] 紋理／邊緣密度只是輔助指標。低紋理區可能包含人物面部或重要符號，仍屬禁入區；高紋理區也不能單憑分數就判定不可排字。**內容安全優先於影像統計。**

### 16.9 第一階段落地：無模型、無新依賴

1. 選三張**已有授權且可用的站內圖片**：右側人物、左側人物、居中人物各一。
2. 人工標記 face／hands／subject／story 保護框，建立 ground truth。
3. 以實際 Bodoni Moda 400、中文及 CTA 建立可測量的候選布局。
4. 實測 390、700、820、1024、1440px 與 100%、125%、150% 縮放。
5. 用硬性排除與候選排序比較左、右、上、下、圖外。
6. 由編輯批准結果，記錄成功與失敗版位；**只把通過實測的規則寫入 OS**。

[OS] 不應一開始就把 MediaPipe 或 OpenCV 打包進主站。若未來實測證明必要，優先放在既有 Design OS 的編輯／建置流程中做可選分析，前台只使用已批准的版位資料；避免瀏覽器每次開頁都下載模型、耗費資源或產生布局跳動。

### 16.10 驗收與回退

| 測試 | PASS 條件 | FAIL 後動作 |
| --- | --- | --- |
| 主體保護 | 人臉、手、重要輪廓與文字無非批准重疊 | 擴大安全區或移到圖外 |
| 語義分行 | 無孤字、無誤拆經文、無拉伸字體 | 改分行／切換 reading |
| 裁切映射 | 原圖保護框與畫面位置一致 | 修正 object-fit/position 轉換 |
| 文字可讀 | 實際覆字區對比達標且細筆畫清楚 | 換位置，不先改全站配色 |
| 跨尺寸 | 各測試尺寸與縮放下均安全 | 改單欄／圖外標題 |
| 可解釋性 | 每個候選列出淘汰理由及評分來源 | 不批准黑箱結果 |
| 保護現有資產 | 十二講員海報比例與特批構圖不被覆蓋 | 回退新規則 |

**常駐訓練：** 每次新增人物／影片封面，先手動提出三個版位，再由評分器給出排序；比較人工選擇與評分差異。若評分第一名被編輯否決，記錄具體原因並修正安全區或特徵，**不得只調權重使結果看似正確**。

本輪提供的是**規格、算法原型與驗收計畫**；尚未建立真實影像辨識服務、安裝模型或驗收任何站內圖片。PR #1325 的實際視覺頁面保持不變。


## 17. 第七輪：以本站真實資產建立候選版位的第一個可驗證基準

### 17.1 已核實的資產（僅查目錄，未檢視像素）

在本 PR 分支的 `static/images/olive/` 確認以下真實圖檔存在：

- `david-pawson-editorial.png`
- `jiang-xiuqin-editorial.png`
- `watchman-nee-editorial.png`
- 同目錄另有其他講員的 editorial 圖片及 `people-transparent-v1/`。

這三張作為第一輪**不同人物案例候選**；尚未根據圖片像素確認人物在左、右或中央，**不得臆測**。原海報及已批准圖文資產不可直接改寫。

### 17.2 先做可重複的人工 ground truth

[OS] 每張圖片記錄原圖尺寸、顯示裁切、主體／臉／手／重要物件保護框、英文標題內容與其語義分行、中文及 CTA 安全區。未經圖片檢視時，保護框為 `pending`，不得填入假座標。人工標註先於任何模型分數；若模型與人工衝突，暫以人工禁入區為準。

### 17.3 第一階段驗收協定

1. 保留原圖，只在獨立編輯預覽中建立左、右、上、下、圖外五種候選。
2. 載入現有 Design OS 字體，待 `document.fonts.ready` 完成後測量真實文字盒。
3. 根據 `object-fit` 和 `object-position` 將原圖安全框轉換成畫面座標。
4. **硬性排除**：人臉、手、重要輪廓、CTA、中文碰撞；字形裁切；孤字；不可讀對比。
5. 對剩餘候選按留白、對比、平衡、節奏及編輯偏好排序；每個結果列出可解釋理由。
6. 保存 390／700／820／1024／1440px 與 100／125／150% 縮放截圖，並人工決定 PASS/FAIL。
7. 若沒有安全覆字候選，強制回退為圖外標題。

### 17.4 防止評分器自我欺騙

[OS] 評分權重仍屬 [EXPERIMENT]，不得用任意輸入的 0–1 分數冒充實測。**沒有實際圖片分析、字體測量和截圖，就沒有勝出版位。** 不得以 CI 成功替代視覺驗收，也不得以模型信心分數取代人物安全審核。

### 17.5 實作接口（供既有 Design OS 編輯流程使用）

```js
// Pure data contract: all geometry in displayed-container pixels.
function evaluateLayout(candidate, protectedRegions) {
  const intersection = (a, b) =>
    Math.max(0, Math.min(a.right, b.right) - Math.max(a.left, b.left)) *
    Math.max(0, Math.min(a.bottom, b.bottom) - Math.max(a.top, b.top));

  const collisions = protectedRegions
    .filter(region => intersection(candidate.titleBox, region.box) > 0)
    .map(region => region.kind);

  const reasons = [
    ...collisions.map(kind => 'protected-region:' + kind),
    ...(candidate.overflow ? ['overflow'] : []),
    ...(candidate.semanticWidow ? ['semantic-widow'] : []),
    ...(candidate.contrastPass === false ? ['contrast'] : []),
    ...(candidate.measured !== true ? ['not-measured'] : [])
  ];

  return {
    id: candidate.id,
    eligible: reasons.length === 0,
    reasons
  };
}
```

[OS] 這個介面**只做硬性條件驗證**，尚不含真實圖片辨識、對比度採樣或最佳化搜尋。候選需先被實測並由其他流程填入 `measured`、`contrastPass` 和 `semanticWidow`，否則不能被批准。後續將這個可解釋驗證接口整合進既有 Design OS，不建立平行系統。

### 17.6 目前結果與下一個實作關卡

**已完成：** 確認三張真實圖片路徑、確立資料契約、硬性排除函式、驗收矩陣與回退規則。

**尚未完成：** 讀取圖片像素、人工標註保護框、瀏覽器量測、實際候選預覽與截圖。不能宣稱已選出最佳構圖或通過真圖驗收。

本輪僅更新手冊，不修改十二講員海報及 PR #1325 的網站視覺。


## 18. 第八輪：真實人物圖文版位實驗室（已提交原型）

已在同一 PR 分支建立 `static/experiments/editorial-layout-safety-lab.html`。此獨立 scoped 實驗頁使用本站三張既有圖片：`david-pawson-editorial.png`、`jiang-xiuqin-editorial.png`、`watchman-nee-editorial.png`。不修改原圖片或正式橄欖山人物海報。

### 18.1 已實作

- 切換三張實際站內人物圖片，使用 `object-fit:contain` 保持原始比例。
- 編輯英文標題；選擇 `face`、`hands`、`subject`、`story` 四種保護區類別。
- 在圖片顯示區拖曳矩形，人工標記保護區；支援撤銷、清空及按圖片分別保存於當次頁面記憶體。
- 左半版、右半版、上方、下方、圖外五種版位候選；點擊表格列切換預覽。
- 使用矩形交集排除已標記保護區的碰撞；沒有標註時顯示「未驗證」，不宣稱安全。
- 輸出 JSON，方便後續人工複核及導入同一 Design OS 的編輯流程。
- 使用 `ResizeObserver` 隨容器大小重算，提供窄屏單欄布局。

### 18.2 重要限制與後續驗收

[EXPERIMENT] 目前紅色保護框是**相對整個預覽舞台**的歸一化座標，不是原始圖片座標；`object-fit:contain` 出現留白時，標註可能包含圖外區域。正式轉換為可持久使用的資產標註之前，須實作圖片可見矩形映射，並與 §16 的 `object-fit:cover` 轉換區分。

[EXPERIMENT] 目前碰撞計算以預設標題區矩形作粗略判斷，**尚未測量真實文字行框、字體載入、色彩對比、孤字、人物主體或 CTA**。表格只報告碰撞或待驗證狀態，不產生 PASS 結論；「圖外」也需另外檢查版面空間。

[EXPERIMENT] 人工標註只存在當次頁面記憶體，刷新即消失；可複製 JSON，但未接 GitHub 寫入、沒有自動保存或模型辨識。網頁建立成功不等於線上部署與視覺截圖驗收完成。

### 18.3 下一個工程關卡

1. 驗證實際 PR preview URL 可打開並正確載入三張圖片。
2. 修正舞台座標與原圖／可見圖片座標的映射。
3. 等待 `document.fonts.ready`，用 DOM `Range` 量測每行真實字群。
4. 為每個候選加入「硬性排除理由」與明確的 `unknown` 狀態，不得把缺少標註當成安全。
5. 人工標註三張真圖，產生對比截圖並驗收。
6. 驗收通過後再決定是否需要引入可選的 MediaPipe 偵測；主站前台不得被迫下載模型。

**本輪狀態：原型已提交；圖片實際視覺驗收、主體識別及最佳版位選擇尚未完成。**


### 18.4 第八輪續篇：圖片座標與真實字形測量（提交 56fe10b）

已在相同的 `static/experiments/editorial-layout-safety-lab.html` 原型中直接修正，不新增第二套管理系統：

1. **原圖座標**：取得 `naturalWidth/naturalHeight`，對 `object-fit: contain` 算出實際顯示圖片矩形，禁止在留白區開始標註，指標位置換算為 **original-image-normalized** 座標，並在舞台縮放後重新投影。圖外拖動終點會被裁到圖片邊界。
2. **字體就緒後測量**：等候 `document.fonts.ready`，以 DOM Range 收集實際文字逐字矩形並合併行框，檢查文字行是否超出候選矩形；檢查元素 scroll 寬高與單字母行。
3. **可解釋性**：結果表明確呈現 `protected-face/hands/subject/story`、`text-overflow`、`glyph-out-of-slot` 等淘汰理由，及尚未完成的 `contrast-not-measured`、`ui-not-reviewed`、`outside-layout-not-measured`。
4. **不虛報 PASS**：人工框選和字形測量仍不足以證明臉部／手部全數標註，也沒有逐像素覆字對比檢測、CTA 碰撞與人工簽核。因此所有結果最多為「未驗收」，不是正式安全版位。
5. **輸出與保存**：JSON 中寫出原始像素尺寸、圖片座標系、標註來源及 `reviewStatus: pending`，仍僅保存於頁面記憶體，可手動複製，尚無 GitHub 自動寫入。

**限制**：此工具處理的是未旋轉、未變形且採 `contain` 的圖片。依 §16.5，`cover` 必須再納入裁切與 `object-position`，不能混用。本次未實際人工逐張審閱像素、未取得真實瀏覽器截圖，故三張圖片尚無已批准安全區座標和勝出版位；不改動正式人物海報。

**後續正式驗收**：必須以三張人物圖分別框選臉、手、軀幹及敘事重點；五版位逐一比對實際截圖；在 390／700／820／1024／1440px、100／125／150% 縮放下檢查原圖和標題比例、中文、CTA 及可讀性。只有人工批准的結果才可升格為 Design OS 生產參考案例。


## 19. 第九輪：Optical Composition Validation — 真實字形、圖文安全與可解釋的版位比較（2026-10-14）

本輪研究直接接續 §18，沿用既有 Design OS，不新增平行字體、色彩管理系統或獨立 CI。**研究結論與已部署能力必須分開**：本章為 [STUDY] + [EXPERIMENT] 技術設計，未取得三張圖片的實際瀏覽器截圖與人工標註前，不宣稱任何版位 PASS。

### 19.1 研究來源及證據邊界

- MDN TextMetrics：https://developer.mozilla.org/en-US/docs/Web/API/TextMetrics 。`actualBoundingBoxLeft/Right/Ascent/Descent` 描述相對基線的墨跡外包框；`width` 是排版前進寬度，斜體可能超出它。
- MDN measureText：https://developer.mozilla.org/en-US/docs/Web/API/CanvasRenderingContext2D/measureText 。
- W3C WCAG 2.2 1.4.3：https://www.w3.org/TR/WCAG22/#contrast-minimum 。一般文字至少 4.5:1；符合大字定義者至少 3:1。這是基本可讀性門檻，不是高對比 Bodoni 細筆畫必然清晰的證明。
- W3C G145：https://www.w3.org/WAI/WCAG22/Techniques/general/G145 。對比測試應針對文字背後的實際背景。

[STUDY] Canvas 指標比僅測 `Range.getClientRects()` 更接近真實字形，但仍是**墨跡矩形**，不是逐像素輪廓或完整瀏覽器合成結果。CSS `letter-spacing`、font features、fallback、文字換行、text-shadow、transform、可變字軸及瀏覽器抗鋸齒可能造成 Canvas 與 DOM 不一致。不能把 Canvas 數值直接當作最終畫面。

### 19.2 三層字形幾何：advance → ink bounds → painted pixels

| 層級 | 測量方式 | 作用 | 不足 |
| --- | --- | --- | --- |
| Layout advance | DOM Range、`getClientRects()`、Canvas `width` | 行框、換行、可點擊布局 | 不一定涵蓋字形外伸 |
| Ink bounds | `actualBoundingBox*` | Bodoni 字形左右及上下外伸風險 | 仍是外接矩形，不是實際輪廓 |
| Painted pixels | 離屏 canvas alpha mask / 真實瀏覽器截圖 | 精細像素佔用及局部對比 | Canvas 重繪與 CSS 合成可能不同，仍需截圖驗證 |

[OS] 禁止以 `scaleX`、`scaleY`、skew 或合成粗體解決排版；候選必須保留 Bodoni 真字形比例。實際字形測量只用於**判斷是否安全**，不構成任意擠壓字母的授權。

### 19.3 實作範例：取得英文標題的墨跡包圍框

```js
// Diagnostic prototype, not yet wired into the production layout.
async function measureInk(text, element) {
  await document.fonts.ready;
  const style = getComputedStyle(element);
  const canvas = document.createElement('canvas');
  const ctx = canvas.getContext('2d');
  ctx.textBaseline = 'alphabetic';
  ctx.textAlign = 'left';
  ctx.font = [style.fontStyle, style.fontWeight, style.fontSize, style.fontFamily]
    .filter(Boolean).join(' ');
  const m = ctx.measureText(text);
  return {
    advance: m.width,
    ink: {
      left: -m.actualBoundingBoxLeft,
      right: m.actualBoundingBoxRight,
      top: -m.actualBoundingBoxAscent,
      bottom: m.actualBoundingBoxDescent
    },
    font: ctx.font,
    measuredAfterFontsReady: true
  };
}
```

[EXPERIMENT] 此處是以 alphabetic baseline 為原點的**相對**矩形，不是頁面絕對座標；要轉到舞台，仍需真實 baseline、對齊位置、逐行 DOM 行框。若字體尚未真正載入、Canvas 使用 fallback、字距與瀏覽器 CSS 不一致，必須標記 `measurement-mismatch`，不能給 PASS。先以 DOM 行框判斷粗略衝突，再以 ink bounds 補充外伸檢查；需要像素級精度時才測 alpha mask。

### 19.4 人物與英文字母之間的 Clearance

不能只檢查兩個矩形是否交疊。候選需記錄 `face`、`hands`、`subject`、`story` 與標題的最近距離；距離不足即使沒有相交也要標記警告。Clearance 不應採單一固定像素：它與標題字級、人物表情／手勢、圖片密度及不同 viewport 有關。以 §16.6 的 `max(12px, 0.25 × fontSize)` 作**待校準候選**，而非硬性全站規範。現有十二講員海報的特批前後景交錯不能被新評分器覆寫。

### 19.5 聯合排版：英文、中文、CTA、導航一起保護

候選不是只有英文標題：應將 `englishTitle`、`chineseSubtitle`、`cta`、`navigation`、`caption` 及 `protectedImageRegions` 全部映射到同一**顯示容器座標系**，逐一檢查硬性衝突。英文在圖外並不代表整體版面已安全：若中文或 CTA 被擠到視窗外，整體仍 FAIL。

資料契約示例：

```js
const composition = {
  image: { fit: 'contain', objectPosition: [0.5, 0.5] },
  typography: { title: 'DAVID PAWSON', fontRole: 'display-en' },
  blocks: ['englishTitle', 'chineseSubtitle', 'cta', 'navigation'],
  protectedImageRegions: [],
  review: { imageAnnotations: 'pending', screenshot: 'pending' }
};
```

### 19.6 從硬性排除到美學排序

**第一層（必須通過）**：人物禁入區、標題墨跡溢出、語義分行、中文與 CTA、圖片裁切、基本對比、字體真實載入、必要的無障礙要求。

**第二層（可比較，但不自動批准）**：主體與標題視覺重量、負空間、人物視線與閱讀方向、構圖節奏、字群輪廓、圖片敘事與內容角色。每個指標必須附來源：像素測量／DOM 幾何／人工標註／編輯評審。未知項目不得用 0.5 等假分數填補。

排序輸出應保留 `rejectedReasons`、`unknownChecks`、`measurements`、`editorDecision`。只有硬性條件完成且人工批准後，才可標記 `approved`；否則一律 `pending`。沒有安全覆字候選時，退回圖外正常 H1。

### 19.7 三張站內圖片的實證矩陣

| 真實資產 | 左 | 右 | 上 | 下 | 圖外 |
| --- | --- | --- | --- | --- | --- |
| david-pawson-editorial.png | pending | pending | pending | pending | pending |
| jiang-xiuqin-editorial.png | pending | pending | pending | pending | pending |
| watchman-nee-editorial.png | pending | pending | pending | pending | pending |

每張都應記錄：原圖尺寸、人工 face/hands/subject/story 框、英文／中文／CTA 真實矩形、字體資訊、對比、候選淘汰理由，以及 390／700／820／1024／1440px 和 100／125／150% 縮放的對比截圖。**不能將同一人物的主體座標套到其他圖片。**

### 19.8 第九輪反證與後續實作順序

1. 若 Canvas ink bounds 與真實截圖不符，改以實際渲染像素或人工審核為準，不擅自改字體。
2. 若某候選矩形沒有碰撞但視覺上仍壓住手勢、衣物、眼神，記錄保護區漏標，而非調高美學權重掩飾。
3. 若圖上文字符合 3:1 卻因 Bodoni 極細筆畫不清楚，依實際可讀性淘汰，不將合規等同最佳構圖。
4. 若英文安全但中文／CTA 溢出，整體 FAIL。
5. 若手機端需要重新布局，改版位與語義分行，不壓縮字形、不拉伸圖片。
6. 下一次**先實作並驗收**三張真圖的安全區、真實字形測量與截圖；未達標前不再將抽象評分器宣稱為最佳構圖系統。

**本輪結論**：從「標題能否放下」提升為「真實墨跡是否安全、完整構圖是否可讀、編輯選擇是否有可核對證據」。本輪研究已寫入手冊；不代表新測量功能已部署或三張圖片已通過視覺驗收。


### 19.9 第九輪實作紀錄（2026-10-14）

已提交 `7b9e27a`：在 `static/experiments/editorial-layout-safety-lab.html` 加入 Canvas `measureText()` 字形量測，於字體就緒後讀取每個覆圖候選的文字前進寬度、墨跡寬度、上伸與下伸距離，並連同 DOM Range 行框輸出 JSON。使用既有 Design OS 字體，不修改正式人物海報。

此版本是**可執行的測量資料採集**，不是構圖 PASS：Canvas 估計尚未換算為逐像素碰撞，亦未完成人臉、手部和敘事區人工標註；David Pawson、Jiang Xiuqin、Watchman Nee 三張圖片的瀏覽器截圖、對比與人工審核均為 pending。圖外版位仍待完整預覽和量測。

下一個驗收關卡：實際檢視三張圖片、標註保護區、把字形墨跡座標映射至顯示容器、補齊圖外版位，並對 390／700／820／1024／1440px 執行截圖與人工判讀。不得以測量資料或 CI 成功冒充視覺驗收。


## 20. 第十輪：Real Image Composition Validation（2026-10-14）

### 20.1 目標與實際進度

將 §19 的字形測量用於三張真實人物圖片的五種候選版位，區分「程式可執行」「已測量」「人工驗收通過」。本輪在原有 `static/experiments/editorial-layout-safety-lab.html` 實驗頁修改，沒有建立平行 Design OS，也不改動正式十二講員海報。

**已提交**：`7b9e27a` 加入 Canvas TextMetrics 字形估算及 DOM Range 行框 JSON；`cb8dd10` 為圖外候選補上實際預覽及字形測量，並將覆圖標題區與人工保護區相交明確標記為 `possible-protected-*`（保守粗篩，不冒充墨跡精確碰撞）。

### 20.2 三張真圖 × 五種版位

| 資產 | 左半版 | 右半版 | 上方 | 下方 | 圖外 |
| --- | --- | --- | --- | --- | --- |
| David Pawson | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 已有預覽；待截圖 |
| Jiang Xiuqin | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 已有預覽；待截圖 |
| Watchman Nee | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 待人工標註與截圖 | 已有預覽；待截圖 |

**證據界限**：已核實三張圖片的倉庫路徑，但本次未能在執行環境下載並檢視圖片像素，亦未取得瀏覽器實際截圖；因此沒有填寫臉、手、身體保護區的虛構座標，沒有宣布任何勝出版位。圖外預覽不等於圖外排版完成可讀性審核。

### 20.3 正確的構圖驗證次序

1. 讀取每張真圖，人工標註 face／hands／subject／story，按原圖歸一化座標保存。
2. 每個候選先記錄 DOM 行框、Canvas 墨跡估計和標題區矩形。當標題區與保護區相交，標記 `possible-protected-*`；這是保守拒絕，**不能反推字形一定碰撞**。
3. 將字形估計與真實 DOM 基線、字距及換行比對；存在差異時維持 `pending`，不得用 Canvas 單次量測宣布安全。
4. 在 390／700／820／1024／1440px、100／125／150% 縮放取得真實截圖，檢查字母外伸、人物遮擋、中文、CTA、對比和閱讀方向。
5. 在硬性安全檢查通過後，再由編輯比較負空間、視覺重量、敘事與節奏，選擇最佳構圖；若無安全覆圖版位，回退圖外標題。

### 20.4 完成定義與限制

[IMPLEMENTED] 三張資產切換、人工框選、五種版位候選、圖外預覽、DOM 行框、Canvas 字形估算及 JSON 記錄。

[PENDING] 圖片像素審閱、完整人工標註、字形墨跡實際畫面座標與像素級碰撞、真實圖片背景對比、中文／CTA 聯合碰撞、跨尺寸瀏覽器截圖及人工批准。

**第十輪研究結論**：可執行的測量與候選比較工具已進一步建立，但「Real Image Composition Validation」尚未達成完整實證驗收。不得將此章標記為 PASS，也不應再擴充抽象評分理論；下一個工作單位必須是三張真圖的實際截圖與人工構圖判讀。
