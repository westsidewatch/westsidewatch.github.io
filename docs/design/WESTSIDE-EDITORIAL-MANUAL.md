# Westside Design OS — Editorial Manual

Status: **operational chapter of the single Westside Design OS**, not a parallel visual authority.  
Audience: Church, First Look, Journal, Olive Mountain, ONE, Dawn Library, Cinema, Search, tools, and Doré Design agents.  
Source of truth: [WESTSIDE-DESIGN-OS.md](WESTSIDE-DESIGN-OS.md) → `design-system/tokens/westside.tokens.json` → `static/css/westside-design-os.css` → approved `data-ws-scope` overrides.

**工作指令快速索引：** 使用者說「多雷探索」時，立即按本手冊 [§9 多雷探索 / Doré Exploration](#9-多雷探索--doré-exploration) 執行；正式定義見 [`MASTER_SITE_ARCHITECTURE.md` §9](../MASTER_SITE_ARCHITECTURE.md)。此詞不是 Gustave Doré 的藝術風格，也不是「多雷搜索」。

## 1. Authority, layers and safe integration

This manual merges design **judgment, editing and verification** into the existing OS. It is a Markdown reference, **not loaded by public pages**. Nothing in it authorizes an extra CSS entry point, a new global palette, a competing type scale, a second CI pipeline or a site-wide geometry patch.

| Layer | Existing authority | Editorial manual action |
|---|---|---|
| Normative tokens: font, color, weight, spacing, motion | `design-system/tokens/westside.tokens.json`; `design-system/scopes.json` | **Refer to**, never redefine |
| Loaded runtime | `static/css/westside-design-os.css` | Preserve existing stylesheet links/import order |
| Surface geometry and transitions | Existing owning CSS/JS files; `data-ws-scope` | Review locally; no universal overrides |
| Editorial font detail | `docs/design/WESTSIDE-EDITORIAL-TYPOGRAPHY.md` | Keep as detailed reference; defer to OS on conflict |
| Award precedents and UI Skills | Research documents in `dore-design/` | Interpret into review criteria and exercises |
| Acceptance | Existing OS, first-look, build and deployment checks + actual browser visual inspection | Do not replace visual QA with CI status |

**Integration verified 2026-10-17:** The OS runtime already defines Bodoni Moda, genuine Bodoni Moda SC, Chiron Hei HK WS, Noto Serif TC, Chinese 200/400/600 weights and responsive `--ws-type-scale-*` semantics. Hence the old typography document's `typography-sitewide.css` authority statement is **superseded** by the OS umbrella and compatibility-runtime contract. It is not grounds to migrate or change working entry points.

**Entrypoint rules.** Hugo templates load OS through `layouts/_default/baseof.html`; standalone P2 loads `/css/westside-design-os.css` followed by its own `/css/p2-living-water.css`. Other standalone HTML is guarded by `scripts/check_design_os_entrypoints.py`: the OS stylesheet and `body[data-ws-scope]` must both exist. A manual consolidation **must not touch those references, their sequence, or any HTML/CSS/JS**.

## 2. Editorial hierarchy and real reading

Typography is architecture for reading, not decorative text. Decide the reader's sequence before choosing font sizes.

1. **Identity:** ecclesial/realm name, issue or section identity; usually one visual anchor.
2. **Primary heading:** one clear top-level editorial proposition.
3. **Section headings:** lower scale/weight than the primary title unless an explicit art-directed composition justifies parity.
4. **Body/metadata:** sufficiently legible at the actual viewport; time, author, source and captions must remain discoverable.
5. **Citation/folio:** distinct semantic typography and stable positioning; never compete with the content.

Select from the OS semantic scale; surface owners may bind scope-specific roles. Do not make a new `--root` type system and do not stretch fonts. Chinese 200 is for airy, sufficiently large editorial display; not tiny administrative descriptions. Chinese anchor 600 is for short structural titles, not whole paragraphs. English Roman/Italic Bodoni and real Small Caps retain distinct semantic roles.

Composition is measured by *text length, optical alignment, baseline, measure, contrast and breathing room*. A technically right-aligned row may still have a broken time-to-event association when the two columns are visually detached. Negative space needs a function, not merely width.

## 3. Award-calibre precedent method

The award corpus is a **research evidence bank**, not a list of winners to imitate or a claim of affiliation with Awwwards, Webby, FWA, Red Dot or D&AD. The internal phrase “Red Dot-level or reject” describes a design ambition, not an official certification.

For every candidate, document:

`reference → concept → spatial/narrative mechanism → typography/hierarchy → IA/reading path → transferable primitive → constraint → failure mode → OS-scope application → experiment`.

Transfer useful mechanisms, not surface styling:

| Precedent from award corpus | Transferable editorial insight | Guardrail |
|---|---|---|
| **The Boat** | Scroll, illustration and prose can form a single authored reading sequence | Motion must follow reading, not obscure it |
| **We Choose the Moon** | Canonical chronology can itself become information architecture | Provide clear wayfinding and overview |
| **Museum of the World** | Time and semantic relationships can spatialise a large collection | Maintain legibility and access to details |
| **Bear 71** | A linear story and an explorable information system can coexist | Avoid burying core actions behind immersion |
| **Species in Pieces** | Signature interaction comes from subject-specific metaphor | Reject ornamental effect without meaning |
| **Bascule / Microdot** | Scroll or timeline can become expressive navigation | Novelty does not excuse scroll lock or exclusion |
| **KUUM / Communication through the Ages** | Subject geometry and visual invariants can drive transitions | Preserve spatial continuity and orientation |

For Westside, engraving line, paper, dawn, water and scripture chronology may define transitions. They must **not** be used to justify content invisibility, long empty scroll bands or read-blocking animation.

## 4. UI Skills routing and acceptance

Load only the skills needed for the present defect. Imported Skills are **inspiration and decision aids**, not an installed guarantee or a replacement for Westside's OS.

| Task | Capability bundle derived from Doré research | Expected artifact |
|---|---|---|
| Layout and typography | `ui.visual-hierarchy`, `ui.design-system`, `ui.taste-anti-slop` | Type-role map, grid and optical alignment measurements |
| Motion and transitions | `ui.motion-system`, `ui.motion-forensics`, `ui.performance` | Purpose/timeline/interruption/return/reduced-motion review |
| Usability and accessibility | `ui.interaction-quality`, `ui.accessibility` | Reading order, focus/keyboard, contrast and small-screen test |
| Final polish and release | `ui.critique`, `ui.visual-verification` | Severity-tagged review and before/after screenshots |
| Variant exploration | `variant` / `prototype` / pairwise Taste Memory | A/B comparison on **one meaningful axis**, including rejection reason |

This incorporates UI Skills explorations R1–R4: route the minimum capability, test motion separately from motion authoring, deliberately break at edge states, compare against the current version, and record contextual outcomes and uncertainty. Do not generate cosmetic alternatives solely to accumulate screenshots; do not compress all user tastes into one global score.

For code and motion, make the change-level critique concrete: **block / important / polish / approve**, with a reproducible defect, owning file, anticipated visual delta and evidence.

## 5. Editorial composition and motion grammar

Follow the experimental Italian editorial grammar as a **method**, not a second visual system:

- Begin with a one-sentence visual proposition and dominant reader task.
- Map composition grid, content priority, focal point, text-safe zone, cropping, paper/ink roles and deliberate blank regions.
- Keep live text in semantic HTML/CSS; image-generation prompts describe text-free artwork.
- Compare supported composition families (quiet field, overscale tension, two-scale encounter) within the same approved OS palette and fonts.
- Motion must explain state, route, hierarchy or narrative passage; prefer existing OS motion primitives and surface-owned implementation.
- Static composition must read correctly **before** motion begins and after it settles.
- Never add a new global cascade override to patch a single screen; use the owning `data-ws-scope` and stylesheet.

Review at desktop, tablet and phone widths; normal and reduced motion; initial, mid-scroll, end, interruption and return. Browser measurements and screenshots are distinct from build-status success.

## 6. Unified editorial review / promotion gate

Record one **evidence-led** review per change, using the project skill's existing directional rubric (0–2 each across **meaning, subject, composition distinction, typography, two-ink discipline, hierarchy, interaction meaning, mobile, accessibility, editability**; 20 possible). Its original exploratory threshold is **15/20** with no zero for meaning, distinction, accessibility or editability. This is a **local creative-review screen, not an official award score or a substitute for acceptance tests**. Surface-specific feasibility, reading and performance are independent release gates.

1. **Brief:** reader goal, real copy, current viewports, locked assets and immutable sections.
2. **Before:** fetch the actual current file and prior approved screenshot; record measured DOM and type metrics.
3. **Candidate:** smallest coherent scoped change, with OS-approved tokens; preserve all source content.
4. **Evidence:** before/after and desktop/mobile screenshots; accessibility, keyboard, zoom, scroll and reduced-motion behavior.
5. **Judgment:** rubric + blocking issues + any A/B winner/loser reasoning in context.
6. **Promotion:** existing OS contract and build/CI, Cloudflare preview and **actual browser visual check**. Green CI cannot override a known visual defect.
7. **Learning:** record what worked, what failed and where; keep source research linked rather than creating a second authority.

## 7. P2 Church / Sunday schedule — Italian editorial folio

The P2 split composition preserves its water engraving, rise and opening doors on the left and the warm-paper schedule on the right. **The previous requirement to keep seven gold right-aligned headings is withdrawn** by the 2026-10-17 editorial review; it must not be treated as a locked visual asset.

- **Separate, untouched church identity:** church logo, English church name and street address are outside the Sunday programme's editorial scope. Preserve their current sizes, typography, spacing, alignment and markup; do not treat them as a schedule header.\n- **Protected:** original service times, seven worship texts and their order, ministry copy, scripture, church-name artwork, left water and door mechanics, existing OS tokens and palette.
- **Reading hierarchy:** issue/date folio → one Chinese main title → ministry context → seven numbered programme rows → next-service details → scripture.
- **Italian editorial grammar:** use a three-column folio (01–07 / tabular time / left-aligned programme), restrained hairlines, editorial whitespace and optical left alignment. English Bodoni for metadata and times; Chiron Hei HK WS for Chinese heading and reading; avoid artificially stretched type.
- **Color:** ink is the programme text; the approved palette remains available for subtle accents. The old repeated gold right-aligned headline treatment is not mandatory.
- **Implementation:** owning `static/css/p2-living-water.css` only; do not create another runtime, modify OS globals, replace engraving artwork or interfere with scroll/door choreography. CSS counters supply numbers without altering source copy.
- **Proportional folio (2026-10-17):** make the schedule-owning right pane an inline-size container; use percentage-based inner gutters, container-relative column proportions and `cqi` fluid type with readable clamp bounds. Do not use CSS `transform:scale` on typography or the entire schedule. Preserve whitespace on both sides at any zoom and stack columns below the narrow-container threshold.\n- **Scripture:** the theme scripture remains left-aligned editorial reading; the independent Acts 4:12 closing citation is centered, including its reference.\n- **Acceptance:** actual 1648×928, 768px and 390px previews, 200% zoom, longest-row wrapping, keyboard and reduced-motion review, plus existing CI. A green CI alone does not certify editorial quality.

## 8. Research retained as source-of-evidence

These files remain archived intact; they do not operate as independent OS authorities:

- [Westside Editorial Typography](WESTSIDE-EDITORIAL-TYPOGRAPHY.md)
- [Doré Award-Calibre Digital Art Direction Corpus](../../dore-design/AWARD-CALIBRE-DIGITAL-ART-DIRECTION-CORPUS-2026-09-09.md)
- [UI Skills Exploration R1](../../dore-design/UI-SKILLS-EXPLORATION-2026-09-12.md), [R2](../../dore-design/UI-SKILLS-EXPLORATION-R2-2026-09-12.md), [R3](../../dore-design/UI-SKILLS-EXPLORATION-R3-2026-09-12.md), [R4](../../dore-design/UI-SKILLS-EXPLORATION-R4-2026-09-12.md)
- [Executable Italian Editorial Grammar](../dore/italian-editorial-executable-grammar.v1.md)
- [Magazine Kinetic Typography Reference](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md)
- [New Westside Editorial Web Skill](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/SKILL.md) and [Visual Grammar / Creative Rubric](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/references/visual-grammar.md)
- [Editorial Web Maturity Study](../../dore-design/knowledge-lab/research/editorial-web-maturity-study-20260901.md)
- [Camera and Attention Grammar](../../dore-design/DORE-EXPLORATION-CAMERA-ATTENTION-GRAMMAR-2026-09-09.md)

## 9. 多雷探索 / Doré Exploration — 固定工作指令

> **權威與用途：** 本節是「多雷探索」在編輯與視覺工程中的就地操作入口，依據 [`MASTER_SITE_ARCHITECTURE.md` §9](../MASTER_SITE_ARCHITECTURE.md)。正式定義仍以該架構文件為準；此處不建立第二套 Design OS、產品或工具。

### 9.1 明確定義與消歧

**「多雷探索」是 Doré 面對當前具體問題時啟動的全面外部學習／方案發現程序。** 它是約定的**工作指令**，而不是主站公開欄目、單一工具，**不是「多雷搜索」的同義詞，更不是要求研究 Gustave Doré 的人物或木刻風格**。即使工作涉及版畫、植物或雕刻，也必須按此工作指令的系統性研究流程執行；若需要查藝術史，僅屬本次探索的一部分。

**收到「多雷探索」時：先明確當前問題、目標和已鎖定的資產，再查世界已有的方案及實例；不可只從名稱或當下題材猜測含義，也不可在未查手冊時自行把它解釋為 Doré 畫風。**

### 9.2 八項不可省略的探索原則

1. **全網研究：** 不局限於專案或單一來源，全面尋找已有的相關方案、工具、框架、實作、範例與資料。
2. **開源優先：** 優先核實成熟開源專案、公開資料、可自行部署元件、現成 libraries / frameworks 和已有實現。
3. **成熟優先：** 對照真實使用案例、維護與版本狀態、社群、生態、穩定性、已知問題與長期可用性；不因新奇而優先採用。
4. **免費優先：** 評估實際授權、使用與持續成本；遇付費方案須同時比較免費替代品。
5. **輕量與低資源：** 檢查 CPU、RAM、儲存、前端負載、依賴數量與部署複雜度。
6. **穩定與易維護：** 比較故障排查、升級風險、相容性與維護成本。
7. **優先利用現成能力：** **先研究世界上已經有甚麼，再決定我們需要自己做甚麼**，避免重造已有系統或憑空硬製造型。
8. **最後回到 Doré Core：** 對照既有 Memory / Context / Retrieval / Knowledge / Search、Provider、Research、Graph、工具和產品 adapter，判定直接復用、以 adapter 接入、必要改造或最後才自行開發。

### 9.3 實際執行及成果格式

`現有問題與保護邊界 → 全網樣本／實作搜尋 → 有來源的成熟度、開源、授權、成本、負載及維護比較 → 與既有 Doré Core 和當前工程對照 → 可直接採用／adapter／改造／自研的決策 → 在原工程隔離試作 → 原版對照與實際畫面驗收 → 記錄選用及否決原因`。

每次探索至少回答：**已經有哪些成熟成果？哪些開源、真正免費、輕量且可靠？哪個最接近當前需要？如何與現有資產直接整合？哪些根本不必重造？** 對沒有核實的候選標記「待驗證」，不能宣稱已安裝、已驗收、已整合或已部署。研究結果應附可追溯來源及採納／排除理由，而非只羅列名詞或圖片。

### 9.4 視覺與 SVG 母本的應用（P2 工作例）

- **先找成熟樣本再描畫／轉譯。** 橄欖枝裝飾、七種供應植物雕版、印刷版芯與編目語言，均先比對可追溯的真實作品、比例、刀法、構圖和可使用的權利，再依現有版面需要轉為可控 SVG；不以公式生成的大量路徑冒充成熟造型。
- **先盤點既有工具及原稿。** 複用 P2 已保存的成長線條、活水流場、V10／SVG-075 刻線經驗及晨星表面刻線方法；先查工具能力與限制，必要時才研究外部開源套件。
- **保護原版並同步推進。** 五張原始 V1 母本是對照基線；加層、裁切、動效或線條生長不得在未驗收時替換已成立構圖。藝術母本與 P2 版面適配分層，五個版塊維持共同版本與比較節奏。
- **用真實畫面裁決。** 來源可信、程式可運行、路徑數增加或 CI 綠燈，均不能取代 V1／新稿並排、真實遮罩、手機、動態、反向滾動和效能檢查。藝術效果未改善則否決，不宣稱完成。

**權限界線：** 「多雷探索」本身不授權更改主站資訊架構、替換已驗收設計、擅自合併分支或新增全站 CSS／JavaScript 入口；涉及正式頁面的修改仍須遵守本手冊第 1、6 節及現有 Design OS 與發布驗收程序。

### 9.5 GitHub 工程讀寫能力：每次施工必須實測，不得無根據否認

**已驗證事實（2026-11-07）：** 在 Westside Watch 對話工程環境中，ChatGPT 曾透過已連接的 GitHub 工具成功讀取、建立、修改及提交本倉庫檔案。可用操作包括 `mcp__GitHub__fetch_file`、`mcp__GitHub__create_file`、`mcp__GitHub__update_file` 及 `mcp__GitHub__get_pr_info`。已實際寫入 `westsidewatch/westsidewatch.github.io` 的 Draft PR #1385（分支 `draft/p2-0104-olive-entry-20261105`）；例如提交 `143f414d6f848c0cd87942d0e6c242ea6cdf0aae`。**因此不可因對話變長、思考強度改變或不確定工具名稱，就自行聲稱「我沒有 GitHub 寫入權限」。**

**每次進入工程、尤其在 Medium／High 切換或對話續接之後：**
1. 先查當前工作階段實際可用的 GitHub 工具，再以 `get_pr_info` 確認 PR、Draft 狀態、head commit 與施工分支；必要時 `fetch_file` 讀取現有檔案和最新 blob SHA。
2. 如果 `update_file`／`create_file` 可用且操作在已授權的 Draft 工程範圍內，就直接修改、提交、核對 commit 與測試；不要讓使用者反覆提醒已有寫入能力，也不要退回只提供 patch 或施工規格。
3. 若工具在**當前工作階段經過實際檢查後**確實不可用，才準確報告這一事實；不得把「尚未核查工具」誤說成「無權限」。
4. 將**讀寫能力**、**特定分支的修改授權**、**CI 通過**與**Cloudflare 部署完成**分別核實；工具可用不代表永久可用，寫入成功亦不代表通過藝術或部署驗收。
5. 保護正式主站與已發布 01–03：P2 04 工作僅限已授權的 Draft PR；未經要求不可合併 main、改寫既有正式版本或更改已核准的十二張海報及英文排版。

**錯誤案例：** 2026-11-06 至 11-07 曾在已多次成功提交 GitHub 的前提下，錯誤答覆「沒有寫入工具／不能修改倉庫」，經使用者要求重新檢查才承認工具存在。這是未核查造成的能力判斷錯誤，**不能證實**由 High／Medium 切換造成。今後必須以工具實測取代猜測。

**Revision rule:** update the relevant chapter *here* for any new editorial judgment; update OS tokens only if an approved cross-surface token truly changes. Never import original research documents as CSS/JS, and never replace an existing HTML asset merely to attach the manual.


## 10. 伯利恆一日 / Bethlehem — A Day / Scripture Calendar

**正式名稱與資訊架構：** `伯利恆一日 / Bethlehem` 是 Journal/WATCH 的固定欄目；`A Day` 是其每日／即時內容形式，**不是**第十三個欄目。「每日靈糧」只作內容功能描述。詳見 `docs/MASTER_SITE_ARCHITECTURE.md` §2–3。

**現已作為獨立工程立項：** `docs/projects/scripture-studio/SCRIPTURE-STUDIO-PROJECT-CHARTER-2026-11-08.md`。它包含經文印記藝術母本、直接在發布表面編輯的 Scripture Editor、以及伯利恆一日聖經日曆的審核與每日定時發布。此章為編輯權威，該 Charter 為具體產品交付與工程界線；不創建第二套 OS。

### 10.1 每日三層內容——作品、主文、分享

1. **今日經文作品：** 當日選經可有三節，但只擷取其中最有力量的一節、半節或若干**準確原文字詞**，以 Scripture Seal 藝術 DNA 呈現為作品級經文；不強制把全部所選節文放進作品。陰陽印版、中英字體配對、疏密與版心秩序保持品牌一致；每日可有不同構圖，不堆疊外框、裝飾線、`THE WORD / 經文` 等多餘標籤。
2. **當日主文經文：** 當日選定的**全部節文**以正確順序、準確譯本與可追溯出處呈現（選三節就提供三節），可作乾淨的通用 Folio 閱讀。藝術節錄不可冒充完整引文，不可把 AI 轉述當成聖經原文。
3. **當日理解／分享：** 根據經文上下文、日期與節期背景形成清楚的編輯／牧養理解；與聖經引文清楚區隔。編輯審核人確認神學與來源後才能發布。

### 10.2 每日內容如何形成

採用 `America/Toronto` 本地日期，優先核對教會年、當日節期／節日／紀念日、教會當年主題、一般每日讀經脈絡。節期標籤必須有可靠出處，不虛構固定的節期選經規則。人工或研究工具可提出候選經文及素材，但經文原文必須來源驗證，分享與設計經過明確審核。

### 10.3 高頻使用形成識別

**作品級的不是每天三節經文全部，而是每天從其中提煉的一個文字作品。** 每日持續呈現印記系統的同一套字體、字重關係、雙語視覺節奏、陰陽與留白 DNA，逐年累積成 Westside Watch 可按日期檢索、收藏、回顧、分享的**聖經日曆**。作品可以混排，日常閱讀版式從完成的作品萃取 DNA，但不強制混排。

### 10.4 出版與編輯器界線

伯利恆一日須能在可見編輯畫面完成：選經→標出作品重點→即時排版預覽→編輯主文與理解→審核→設定發佈日期時間→每日定時發佈→永久日期頁與檔案。**每日定時發佈必須以已核准的不可變版本為依據，不自動杜撰當日經文或無人審核的分享。** 發布失敗不能以未審內容代替；排程要支援多倫多夏令時間、重試、避免重複刊登及版本紀錄。

現階段為**工程立項與編輯規範**，尚未聲稱編輯器、每日排程或日曆已上線。不得因編輯手冊文字直接覆寫已驗收主站／P2 頁面。

