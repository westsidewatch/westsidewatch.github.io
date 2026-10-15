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
