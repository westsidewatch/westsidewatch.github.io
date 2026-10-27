# Westside Design OS — Editorial Manual

Status: **operational chapter of the single Westside Design OS**, not a parallel visual authority.  
Audience: Church, First Look, Journal, Olive Mountain, ONE, Dawn Library, Cinema, Search, tools, and Doré Design agents.  
Source of truth: [WESTSIDE-DESIGN-OS.md](WESTSIDE-DESIGN-OS.md) → `design-system/tokens/westside.tokens.json` → `static/css/westside-design-os.css` → approved `data-ws-scope` overrides.

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

**Revision rule:** update the relevant chapter *here* for any new editorial judgment; update OS tokens only if an approved cross-surface token truly changes. Never import original research documents as CSS/JS, and never replace an existing HTML asset merely to attach the manual.

## 9. P2 Vol.00 — Scheme 02 masthead and Jerusalem skyline contract (2026-10-26)

**Status:** latest user-selected layout geometry, with artistic review still open. This is a chapter of the single Westside Design OS, not another typography or position system. Old 2026-10-24 cover geometry was superseded and is deliberately *not* retained as an active standard here; Git history preserves the exploratory record.

### Fixed publication geometry

- **Cover:** portrait width:height **5:8**, unchanged and without further format choices. Adjoining **Contents:** independent **1:1** square. They may align as an asymmetric digital spread.
- **Masthead optical fit (2026-10-26 proof, pending editor acceptance):** retain the exact original `/images/westside-watch-masthead-landscape.svg` (LivingWater / WESTSIDE WATCH / 西望) and its intrinsic proportions. Its source SVG has asymmetric transparent side bearings, so raw CSS left/right alignment is **not** equal ink spacing. The proof uses top **0.55%**, left **−1%**, width **103%**, height **21%**, with an X optical shift of **2.8cqi**, always `object-fit: contain`. Judge and align the **visible gold ink** against the two physical cover edges at equal distances. No direct SVG modification, forced text squashing, city repositioning or alternate masthead artwork. This does not replace the fixed 5:8 cover format.
- **Selected colour-breach design:** **Scheme 02 / Architectural overlap**, evidenced by `/experiments/masthead-color-breach-lab.html`, `data-breach="2"`. The original trial's visual band is **30cqi** of the cover width and the physical Jerusalem stone image container begins at **21cqi** (= band minus 9cqi). The subsequent fixed **5:8** portrait means **21 / 160 = 13.125% of cover height** for that *container origin*. This **is not the silhouette crest's painted Y coordinate**; measure actual crenellations in screenshots. Do not substitute a remembered earlier candidate's skyline ratio.
- **True silhouette:** the complete, unwarped sandstone wall with all crenels and notches breaking into an uninterrupted midnight-blue background. No straight left/right rectangles or colour-divider rules remain. The city and gate share one stone source; the alpha cutout defines its skyline only. No other former A/B/C wall-placement toggles on the active P2.
- **Issue-specific composition (2026-10-26, supersedes previous paragraph):** VOL.00 stays in the stone folio. The entire title group lives **within the original gate opening**: separate stacked English lines **CITY / *OF* / LIGHT**, with the intact Chinese title immediately below; the Chinese is entirely above the gate-threshold light projection. Do not shift the approved Scheme 02 battlements or distort image assets to make the typography fit. The **upper** engraved square register belongs to the original v5.3 3D Morning Star, bounded by a fine gold rule; the lower register contains a subordinate **Contents.** and all twelve canonical articles, grouped in four dense yet readable movements. The index remains keyboard-scrollable when needed. The functional seven-colour ribbon is the **original horizontal component rotated intact by −90° as one assembly** and docked to the **left** of Contents. Keep its local `rotateX` 3D flip, original seven small coloured swatches at the short end, the stagger and first-click expand / second-click navigate. Only the **long rear face** changes from mixed gradient to one selected section colour sourced from Design OS. **Never** convert its seven swatches to seven full-height stripes, change the flip to `rotateY`, or introduce an extra “Enter” button.
- **Validation:** four viewports, no image stretching, screenshot comparison of the *actual* topmost and lateral crenel silhouette and the masthead's unaltered ink footprint, LIGHT and gate hierarchy, Contents reading/3D star exclusion zones, keyboard/scroll reversal. CI compares source against this chapter and fails on retired geometry or spurious nav labels. Passing CI never substitutes for editor's visual approval.

**Authority rule:** for this cover, use the last human-selected Scheme 02 plus the later fixed portrait/Contents decision, not an earlier cover composition study. Never import a rejected numeric skyline standard by copying CSS, comments or test assertions.


## 10. 西望雜誌定型研究 — The Paris Review × 四樂章（2026-10-26）

**性質：**本節是 Westside Design OS 唯一編輯手冊內的刊物風格規範。它不是第二套 Design OS，也不改動 `WESTSIDE-EDITORIAL-TYPOGRAPHY.md` 的已核准字體入口。目標是把「光・線・紙・刻・築」變成一整本可持續出版的網絡雜誌語言，不只一張封面。**獲獎級是內部評審門檻；未宣稱本刊已得獎。**

### 10.1 深讀《The Paris Review》：各個編輯部件，而不止封面

研究對照：[Pentagram／Matt Willey 官方重設](https://www.pentagram.com/work/the-paris-review)、[設計師 Matt Willey 官方作品頁](https://mattwilley.co.uk/The-Paris-Review)、[The Paris Review 第 238 期（新設計首期、2021 冬）](https://www.theparisreview.org/back-issues/238)、[第 255 期（2026 春）](https://www.theparisreview.org/back-issues/255)、[D&AD 2022 官方入選紀錄](https://www.dandad.org/work/d-ad-awards-archive/the-paris-review)。D&AD 只證實重設被其 *Magazine & Newspaper Design* 評選收錄，並不替西望背書。

| 刊物部件 | The Paris Review 可觀察的編輯法 | 西望的轉譯／不能照搬的界線 |
|---|---|---|
| 封面與刊頭 | 2021 方案採簡潔、固定識別；主畫作有完整地位；刊期與作者線索部分轉往實體書脊；取材於 1960–70 年代的極簡記憶。 | 西望固定 **5:8 + 官方 SVG 壓頭刊名 + Scheme 02 城牆**；光與門為 Vol.00 自己的封面故事。七色條是可點擊的跨版塊導航，非實體書模擬。|
| 目錄與分類 | No.238 將 Editor's Note、Fiction、Interview、Poetry、Feature、Art、Essay 分類；No.255 類別與作者／作品一眼可循，不拿一堆等大的封面文案充目錄。 | 四個樂章＝四個**主要組別**，I–IV 為固定節奏；欄目序號 01–12 次之，欄目中文／英文再下，作品名最後。閱讀順序不可因平衡畫面而亂排。|
| 編者按 | No.238 目錄為 Editor's Note 留獨立入口；它屬於完整刊物敘事的起點而非版頭裝飾。 | Mizpah 用精短卷首和一個強命題開門，不提早洩露 Beersheba 的神學結論。|
| 長篇小說／散文／特稿 | 連續文字是核心；縮小書本般規格、縮緊內側邊距、選暖紙而降低手持閱讀疲勞；大圖不奪正文秩序。 | Carmel、The Gate、Elim 可採跨頁圖文，進入長文後以穩定閱讀行長為第一原則。大英文只在開篇命題，不能每個段落都大字。|
| 訪談 | “The Art of Fiction/Nonfiction No.…”是一條可持續的欄目識別，人物與採訪內容的關係比裝飾分隔更清楚。 | Adullam 的人物、地點、時段、系列與原聲證據是恒久坐標；問／答排版清楚，講道與資料庫關聯不假扮採訪原文。|
| 詩歌／靈修 | 詩行與留白保留作者自己的斷行，標題／作者／刊期分層；內容不為填滿網格而被拉伸。 | Bethlehem、Elim、Maranatha 保持經文原行／段、章節註記與禱告語氣；不要用大面積中心對齊代替長文可讀性。|
| 藝術 Portfolio | Art 與封面畫作各有署名／類別；圖像可獨立承擔敘述。 | 多雷刻線、考古圖、原件影像、地圖、講員肖像依編輯證據決定尺度；每張都有必要署名，且絕不可拉伸。|
| 篇章間序列 | 紙刊以期號、分類、文章順序建立進入與回返；並非每頁塞相同版式。 | WATCH→WALK→WITNESS→WORSHIP 是敘事弧；三個 Interlude 用 Video + Music 轉調，提供跳過、暫停及 reduced-motion 版本。|
| 卷末、館藏與索引 | 期別和作者可重新被查找；品牌可跨期保持，內容本身可變。 | Vol.00 尾段禱告／冠冕回到刊物識別；每篇有前後篇、卷目錄、來源資訊，不能只靠滾動方向尋找。|

**關鍵轉譯：**《The Paris Review》教我們最重要的不是「留白多」「某款字體」，而是**一個強識別讓內容真正站到舞台中央**。靜態字重、密度、資訊類型分工清楚，紙色是閱讀介面而不是裝飾背景。西望比紙刊多出自由跨頁、功能性書脊及時間性轉場，但不應多出冗餘 UI。

### 10.2 統一的西望排版文法（供十二個欄目共用）

1. **五層情報：** `刊物／期號` → `樂章 I–IV` → `欄目 01–12` → `作品標題` → `正文／引用／出處`。刊物識別是每期不變項；四樂章在整期不換名字／色彩邏輯。每篇可有自己的頁面敘事和圖像，不能重新造刊頭、字體系統或錯的教會名稱。
2. **英中層次：** Display 英文 Bodoni Moda Roman／真 Italic 做結構與句子；中文短標題 Chiron Hei HK WS 600，少量 200 只用在足夠大的空間；中文長文 Noto Serif TC。真 Small Caps 僅當 folio 與欄目元數據。禁止英文字母任意被中文後備字體吃掉；不偽造 Didot／楷體。
3. **比例而非單一字號：** 在欄目首頁 `H0(大英文/命題):H1(中文主題):H2(欄目):body` 以概念比例約 **5:3:1.8:1** 控制視覺階差；允許滿頁或半頁巨字，但正文閱讀體持續穩定。比例是視覺評估目標，不是新 `:root` token。H0 只在內容有足夠論據／影像結構支撐時放大。
4. **跨頁不是紙本裝訂：** 桌面基準為一個自由跨頁，示例可以 **50/50、40/60、30/70**，也可跨中線放置圖片、標語、刻線與圖表；不存在固定裝訂縫。內容區的 readable measure 獨立控制；手機沿故事邏輯重排為單欄。
5. **長文先行：** 中文常規閱讀目標約 **24–38 個漢字／行**（取決於字號與裝置），行高約 **1.65–1.85**，段間距區別於行距；英文文章段落以約 **55–75 字符／行**為參考；不以固定縮放塞進 5:8 視覺框。
6. **圖與字安全區：** 實物、人物、城垛與金光屬內容資產，必須先識別畫面主體、既定 crop、alpha 與遮擋；文字用測量得來的安全區佈局。不可 `scaleX/Y`、背景 `100% 100%`、也不可為了字挪動已批准的城牆。
7. **背景節制：** 午夜藍＝夜與守望、暖紙／蒲草紙＝研讀、黎明金＝顯明／書脊選中態；多雷刻線作視覺證據與邊界。七色交互只取自 OS 固定版塊色，不能每篇再創一組無法統管的顏色。
8. **動效要負責：** 封面／城門是入場，七色書脊是跨板塊導航，晨星是轉場 focal anchor，三個 Interlude 是實際敘事休止；**移動的東西須有可解釋的功能**。首屏靜態也須完成設計，互動不依賴強制長動畫。
9. **每篇的公共工具：** 必有欄目／刊期／作者或來源／前後篇／返回目錄；可用 footnote、圖片署名、音視頻 transcript 和 source-evidence 入口。不要增加各種形式不同的「進入」按鈕。
10. **可變必須可控：** 各期可換封面主畫、藝術主題和分鏡；刊頭、名錄序列、圖像守護、型別字與導航交互屬不可任意飄移的品牌資產。

### 10.3 六種可重用的「跨頁語法」，不是六套新模板系統

| 語法 / 配置 | 視覺與閱讀重點 | 預設適用 |
|---|---|---|
| **A. Thesis / Opening** | 左大英文單句佔 30–45%；右主文／小插圖，次要資訊沿網格；只容一個最強視點。 | Mizpah、Beersheba、Horeb |
| **B. Evidence Atlas** | 原件／刻線／地圖約 60–70%；文字說明 30–40%；引用與圖例不用壓圖。 | The Gate、Carmel、Elim |
| **C. Continuous Reading** | 一至兩條規則正文欄，穩定行長；跨頁圖獨立成節點，邊欄註腳。 | Emmaus、Bethel、卷首長文 |
| **D. Portrait / Dialogue** | 人物主體 40–60%；採訪或關係資料區保持能閱讀的單欄，窄邊標年份與來源。 | Esther、Adullam |
| **E. Scripture / Score** | 保留經文、詩歌／禱告原始斷行；整頁可偏心、空白有節奏，引用用真 Italic。 | Bethlehem、三段 Interlude、Maranatha |
| **F. Full-bleed Revelation** | 單張獲准資產擔主角，文字只在可用安全區；圖／刻線在滾動時逐次顯影。 | 四樂章卷首、Selah、遠方無聲鴿、Kinneret、卷末 |

上述每個 variant 都只設在既有 `data-ws-scope="journal"` 下的單篇／單期 owner class。不要將版式配置升格成整站 `body` 全域覆蓋。正式程式應共用一套語義 `article`／`figure`／`blockquote`／`figcaption`，而不是在新文章複製 1000 行 CSS。

### 10.4 四樂章 × 十二欄目的具體視覺樂譜

**內容權威：** [`docs/projects/watch-city-vol00/EDITORIAL_MAP.md`](../projects/watch-city-vol00/EDITORIAL_MAP.md)，2026-09-22 人類編輯確認，強於舊的 `data/volumes/vol-00.yaml`。四樂章順序固定 **WATCH 4 → WALK 4 → WITNESS 2 → WORSHIP 2**；三 Interlude 不是文章欄。缺稿不准憑設計需要擬造標題。

| 樂章 | 章首視覺拍子 | 欄目分工與首選語法 | 不能失去的編輯意義 |
|---|---|---|---|
| **I. WATCH｜守望** | 高對比午夜藍與刻線；一個有力英文命題與清楚中文大標題。從卷首逐步增長圖文密度。 | **01 米斯巴** A：短卷首；**02 伯利恆** E：經文／靈糧；**03 門** B：人物／城史／三篇既有稿；**04 迦密** B+F：〈一萬年的建城禮〉核心特稿。 | 提問而不搶先回答，讓「建」的歷史重量成立。 |
| **II. WALK｜同行** | 在紙色上由研究轉向人的步行路線；網格具有前進方向，段落較緊而穩。 | **05 以馬忤斯** C：吾珥、同行與查經；**06 以琳** B：攻／守城的真實物證與圖表；**07 別是巴** A+C：全卷神學思考收束；**08 伯特利** C：門徒培訓與真實生活實踐。 | Beersheba 最後揭示真正守望者是神；Bethel 由「明白」走向「生活」。 |
| **III. WITNESS｜見證** | 敘事節奏降速，肖像／原話／原始證據成主角；減少裝飾與大字搶戲。 | **09 以斯帖** D：勞倫斯弟兄，歷史見證；**10 亞杜蘭洞** D+B：黃淑華／江秀琴，地點／時段／講道系列可回溯。 | Past Witness / Present Witness 不混排成空泛人物圖牆，音頻身份與文字編輯層分開。 |
| **IV. WORSHIP｜敬拜** | 從高密度證據進入儀式性停頓；金光不是裝飾而是觀念上的終點。 | **11 何烈山** A+F：〈房角石：整座城由此對齊〉；**12 瑪拉拿** E+F：〈冠冕〉、閉卷禱告與安靜。 | 房角石 → 冠冕 → 禱告 → 沉默 → 西望／冠冕識別；結束不是普通文章 footer。 |

**三個 Video + Music Interlude：** I Selah（WATCH → WALK）、II 遠方無聲鴿（WALK → WITNESS）、III Kinneret（WITNESS → WORSHIP）。視聽篇章最多只保留必要標題、短節錄與片源註記。不要給它們虛構刊目編號。

### 10.5 開源中的「可轉移機制」與選用界線

| 官方開源／作者資源 | 可借鑒的技術部件 | 在西望中的位置／明確排除 |
|---|---|---|
| [Codrops / AnimatedGridLayout](https://github.com/codrops/AnimatedGridLayout) | 網格項目展開為內容的布局動畫 | Contents 欄目點入文章；只改變讀者焦點，避免長時間覆蓋標題。 |
| [Codrops / PageFlipLayout](https://github.com/codrops/PageFlipLayout) | CSS Grid 雙頁結構與 GSAP transition | 取**跨頁 grid 與狀態銜接**，不用假紙張、機械書頁厚度或捲角。 |
| [Codrops / KineticTypePageTransition](https://github.com/codrops/KineticTypePageTransition) | 字體充當過場的空間結構 | 僅四樂章開篇可試用；鉛字「西望」失敗實驗不強制升為共用元件。 |
| [Codrops / SuperfluidLayout](https://github.com/codrops/SuperfluidLayout) | 非固定格的文字與圖像揭露 | B/F 語法過場；不可造成正文漂移、閱讀斷行。 |
| [Vivliostyle / themes](https://github.com/vivliostyle/themes) | 可維護的排版 CSS、引用與長文出版規則 | 學行長、層級、分頁思想；**不新增 runtime 書籍引擎**，除非另立輸出 PDF 需求。 |
| [Paged.js / examples](https://github.com/pagedjs/pagedjs-examples) | 出版品網格、folia、不同文字長度測試 | 作壓力測試樣本與印刷退化參考；不能拿其 print margin 替換網刊自由跨頁。 |

外部專案有不同資產與使用條款；本輪只引用概念與介面，**沒有直接複製任何第三方 CSS、JS、字體或影像**。未來若真要導入程式須先檢查當時的 upstream license、依賴與現有專案兼容性。

### 10.6 工程化的統一模板邊界

以現有 Hugo `layouts/journal/list.html`（刊物索引）、`layouts/vol-00/list.html`（本期閱讀目錄）、`layouts/vol-00/single.html`（正文）與 Adullam 特設頁面為 owner。**不得將它們錯認成同一個首頁頁面**。在它們之間維護少量共享的 layout props：`issue`、`movement`、`column`、`spreadType`、`source`、`media`。這些是編輯資料欄位，不是新視覺權威。

推薦實作輪廓（只是語法參考，需在 owner scope 內實測後才升級）：

```css
:is([data-ws-scope="journal"], [data-ws-scope="vol-00"]) .ws-magazine-spread {
  display: grid;
  grid-template-columns: minmax(0, var(--ws-story-left, 40fr))
                         minmax(0, var(--ws-story-right, 60fr));
  container-type: inline-size;
}
:is([data-ws-scope="journal"], [data-ws-scope="vol-00"]) .ws-magazine-prose {
  max-inline-size: min(100%, 38em);
  line-height: 1.75;
}
:is([data-ws-scope="journal"], [data-ws-scope="vol-00"]) .ws-magazine-image {
  width: 100%;
  height: auto;
  object-fit: contain;
}
@media (max-width: 720px) {
  :is([data-ws-scope="journal"], [data-ws-scope="vol-00"]) .ws-magazine-spread { grid-template-columns: 1fr; }
}
```

注意：此例以容器自定義變數做**局部比例**，不另設一套全站 palette/type；不同內容需要再驗證 50/50、30/70 的閱讀順序。真正實作時不得把比例參數直接放上 `html` 或 `:root`。

### 10.7 客觀驗收（不只是「看起來像雜誌」）

- **封面：**刊名 SVG 真正壓頭，左右以可見字墨視覺等距，5:8 原物件、21cqi 城牆容器、垛口完整；CITY／*OF*／LIGHT 三行與中文全部在**原城門內、門檻投光起點之上**；不靠更換照片或拉伸解決。
- **Contents：**獨立 1:1；上 3D 晨星／細金線、下期號與四樂章／十二欄；四類之間有分層而非十幾個同等大標題；原水平功能書脊作**整體 90° 旋轉**，非七大色塊重排。
- **敘事：**讀者能在 5 秒內知道期號與核心題目、10 秒內辨認四樂章、一次點擊知道當前選中板塊；進入文章後 30 秒沒有被動畫阻斷。
- **文字：**逐篇測最長真實漢字篇名、中英混排、經文／註腳、人物名字、不同引號與長網址，不使用 lorem ipsum 代替驗收。
- **網刊自由跨頁：**桌面 30/70、40/60、50/50 都要證明圖文可自然跨越中心；平板轉為邏輯閱讀順序；手機不橫向溢出，200% zoom 不重疊。
- **版式區辨：**四樂章同一刊物血統、不同節奏；兩個人物章不是以歷史/當代換色取代證據結構，兩篇守城歷史不是同一套大圖背景。
- **動效與功能：**Tab/Enter/焦點、七色書脊第一次展開／第二次 canonical navigate、Back/Forward、scroll 中止、reduced-motion、影音暫停與靜音。所有交互都有可見或可聽回饋。
- **完稿門檻：**實際內容、來源、版式、四屏截圖、瀏覽器視覺驗收、既有 OS CI 皆通過；任何已知 blocking issue 不可因為「本輪學習完成」而標成上線／得獎級。

### 10.8 舊標準與資料源防回流

目前已有具體衝突：`docs/projects/watch-city-vol00/EDITORIAL_MAP.md` 固定 **WATCH → WALK → WITNESS → WORSHIP（4/4/2/2）**，但舊 `data/volumes/vol-00.yaml` 曾排成 **WATCH → WITNESS → WALK → WORSHIP（4/2/4/2）**。即使 P2 首屏設計採用正確版本，`layouts/vol-00/list.html` 若仍讀舊 YAML，刊物正文目錄會錯。**任何設計驗收必須同時檢查 data consumer，而非只核實研究 MD。** 不要再把早期計畫稿提升為活躍編輯權威。若發現未能確證的篇名，以「待編輯核實」呈現，絕不自行填字。


### 10.9 前台文案與內部設計語言的防火牆（2026-10-26 用戶確認）

《西望》的讀者只接觸**刊物自身的編輯內容與真實功能**。設計手冊、實驗室、前端實作、動畫階段、排版研究、資料結構、設計系統與驗收結果屬於後台工作，不可被誤當作目錄、文案、裝飾文字或讀者提示放進正式畫面。這是全站雜誌化的**強制內容準入規則**，不是可自由取捨的版式意見。

- **禁止前台出現：**「WESTSIDE WATCH / SEVEN COLOURS」「WESTSIDE WATCH / LETTERPRESS」「EDITORIAL SHOWCASE」「SCROLL / SEVEN SPATIAL STUDIES」「ORIGINAL HOME FILM」「四樂章 · 十二欄目 · 三段視聽間奏」及任何相同性質的研發、技術、實驗、數量標籤。禁止以中英混排的新詞、pseudo-element `content`、隱藏層回流或仿出版文案迴避。
- **允許：**正式刊名 SVG、Vol.00、已審核主題、Contents、四樂章名稱、真實欄目與篇名、視聽作品**原始**名稱，以及色帶展開後對應 Westside Core 的真實導航名稱。操作提示僅在實際交互需要時以最小幅度出現；`aria-label` 應如實描述可及性與操作，不另造可見文案。
- **來源責任：**前台每段字都必須能指回刊物編輯地圖、正式篇名、核心導航或真正的讀者操作；不能以研究文件、PR 說明、設計草稿、測試腳本充當稿源。
- **實作責任：**直接從 DOM、SVG `text` 和 CSS `content` 刪掉錯誤文案；單純 `display:none` 不算清理。分離讀者可見網站和明確的實驗檢視 UI。CI 在生成預覽前掃描禁詞與實際渲染。
- **回歸：**封面、正方形 Contents、七色書脊、轉場中間格與 100% 定稿格都要檢查，特別防止中間幀從舊元件抽出研發標籤。

### 10.10 P2 實際閱讀密度與動效刊頭的定稿修訂

- 刊頭固定使用同一份已確認的官方橫向 SVG、相同比例與視覺等距；**在 5:8 封面完成收攏前不得以 1:1 半屏倍率突然示人**。中間幀只過渡透明度，不重做其位置、字型或比例；在最終容器到位後才顯現。
- `CITY / OF / LIGHT` 三行的排列及城門定位已確認。允許三行**整組同比放大**以填實原城門內部，中文在同一文字組尾端、光線起點之上；不得移動 Scheme 02 城垛或拉伸素材來替標題騰位置。
- Contents 是一張**能讀完的目錄**：1:1 紙面不變，晨星上移到對比明確的午夜藍獨立版位，星本身仍是原 v5.3；真正的 Contents、四樂章與十二個欄目占據下方主導區。禁止以低對比金色泛光填空。
- 四樂章標題、欄目、文章、間奏須有顯著階層；四欄底線／段落尾點／頁碼形成**可測量的對齊**。下半版沒有內容時不應把其餘資訊擠在中間、讓空洞冒充留白。長真實篇名不得在可用正常桌面尺寸下整塊被截斷。
- 針對 75% 的封面收攏幀與 100% 的最終對頁，分別作視覺驗收；只要看見刊頭不自然放大、目錄文字被捲軸意外裁斷或封面 5:8 變形，即不得宣稱「獲獎級」。


### 10.11 各版塊刻線嚴格分域與雜誌過場（2026-10-26）

**唯一權威**：`static/css/westside-engraving-authority.css`，屬於 Westside Design OS 的版塊視覺語法。城牆、刊頭、晨星、正文版位仍由各自既定資產及編輯規範控制；不另創第二套全站標準。

- **教會**專用長水流與洗禮洋流；**雜誌**專用書頁折線、斜向雕版和紙張結構；橄欖山使用山坡等高線，黎明書局使用書頁紋理，電影院使用幕布和投影光線。任何版塊不得因過場相鄰而挪用前一版塊的刻線。
- **撤銷錯誤跨域方案：**將教會 P2「Fixed Ocean 2.5」620 條水線延伸至《西望》、左右雙色共用水場與相關自動驗收指標，均屬執行錯誤，從本頁移除，不再作為設計方案或 CI 通過條件。
- **雜誌過場**保持已定的方向：午夜藍由上接管日程，黎明金由下接管活水；當純色完成接管後，應有本刊自己的晨星 v5.3、Scheme 02 耶路撒冷石城與書頁斜向刻線進場，而不是延續教會的水紋，也不得用任意紋理填補空白。
- **封面光的參考原則（2026-10-25《西望：城市之光》）：**使用獲選的 02「建築交錯」。光從原城門洞**底部門檻**出來，不從拱門上部或畫外發射；門口亮面、第一折面、向外展開的光面與旁側石影必須共用邊界。主光為乾淨的米白／奶油金幾何折面，旁側是深一級的石材棕灰陰影，保留原石紋質地及清晰的光暗方向。已否決規則「只允許負形、禁止實心楔形」屬誤讀參考圖，撤銷；禁止以均勻短橫線、放射扇、任意 path 數量、裝飾濾鏡冒充光影。文字既定三行與中文都保持在門內、中文位於光源上方。程式檢查只能守住幾何，藝術驗收須真實看圖。
- **保護已確認資產**：Scheme 02 城垛距離與相對位置、官方刊頭 SVG、5:8 封面、1:1 Temple-stone Contents、CITY / OF / LIGHT 三行排法及 v5.3 晨星。28%、45%、58%、97% 皆須實際看畫面，未過藝術驗收保留 draft、不進 main。

### 10.12 P2 Contents 極細字重與開源光效採納門檻（2026-10-26）

- **Contents 是唯一大標題**，真正文章正文不在目錄內。四樂章 `WATCH/WALK/WITNESS/WORSHIP`、十二欄目中英文、篇名清單、章節數字、INTERLUDE、期號和「目錄」全部是極細層，中文使用 OS Chiron Hei HK WS 200，不能被局部覆蓋設成 600/700。這是《西望》Contents 的明確編輯例外；其他版塊的正文 400 和短大標題 600 不受影響。
- **英文字體技術限制**：Bodoni Moda 及 Bodoni Moda SC 目前真實字形的最低重量是 400。附屬英文元素宣告 CSS 200，會匹配到字體已有的最輕 400 字形；不能靠降透明度、模糊濾鏡假裝「極細」，也不能悄悄換掉 Design OS 的官方英文。主大標題 `Contents.` 保持 Bodoni 400。
- **測試全覆蓋：**目錄標籤、四樂章、欄目、英文對譯、文章標題、編號、間奏、期號均需 computed-style 掃描，不只改其中一種。四欄長文在薄字重時保持足夠墨色、可讀字號與鍵盤／觸控捲動，不能以低對比或截斷模擬留白。
- **多雷開源探索（後台、不得上讀者頁）：**[Erkaman / glsl-godrays](https://github.com/Erkaman/glsl-godrays) 使用 light-source occlusion texture 阻止光穿過遮擋物，適合城門的真遮光，但要求 WebGL 多 pass 與精確 2D 門洞 mask。[Taha Bakri / scroll-reveal](https://github.com/tahabakri/scroll-reveal)（MIT）示範 GSAP 鎖定捲動的 SVG 負形視窗與材質揭露，技術上可做「門檻→折面」而不移植 demo 的霓虹美術。[notoriousb1t / polymorph](https://github.com/notoriousb1t/polymorph)（MIT）可 morph 已畫好的相接 SVG 折面，但不會自動做出合格構圖。[pancao / apple-flare-halo-shader](https://github.com/pancao/apple-flare-halo-shader)（MIT）擅長鏡頭耀斑／光譜光暈，與本期印刷石城不匹配，**不採用**。
- **真正採納須先匹配參考：**本期被選中的《西望：城市之光》02「建築交錯」，門檻共邊、米白主光、深一級石影、石紋與方向必須在靜態畫面先成立，再用開源遮罩／遮擋／捲動技術處理過場。絕不可把任意 God Rays、扇形射線、兩塊無意義色面和他版水紋直接貼上。CI 合格不代表藝術合格；沒看過分幀真圖就不准說定稿。

### 10.13 P2 / Vol.00 活躍程式入口與淘汰來源（2026-10-26）

- **唯一活躍畫面：**`static/experiments/p2-double-square-video-lab.html`；只載入 Design OS 和本刊局部 `static/css/p2-vol00-editorial.css`。全部視覺規則在這一份局部樣式，不准把淘汰的 inline CSS、A/B/C 按鈕或 Church ocean 換名放回來。
- **順序：**封面從午夜藍上沿進場 → 官方 SVG「西望」七段鉛字於黎明金紙上逐行套印 → 原 v5.3 晨星起升與封面同屏 → 實體的 5:8／1:1 非對稱對頁定型 → 既有聖殿石紋 Contents 接替鉛字。同一 scroll progress 正反可逆；晨星不得取代正文；下方保留的是原字版極淡紙面壓痕，而非金色光源。
- **封面光：**沿既有 Scheme 02 城門歸一條門檻；SVG `ws-gate-aperture`／`ws-light-floor` 分別約束門洞內部亮度與落在原石牆上的紙面折光。以共邊的投影、較亮內折、較暗石影呈現深度，原 PNG 石材照樣透出；光面的 path 數量、舊座標與橫向扇線**不作獨立藝術標準**。完整原石牆始終是不變的可見材質，透明 cutout 只參與垛口遮罩，兩者以 `cover` 等比裁切。
- **清理權限：**曾有的首頁影片當《西望》背景、不可驗證的 WebGL canvas 仿冒晨星、被隱藏卻會在重新編排時復活的 lead-type/archive CSS、鎖定舊 path 數量或無意義純色塊的 CI 都已淘汰；其歷史只能在 Git 追溯，不能在活躍頁或驗收裡成為替代方案。
- **驗收邊界：**先驗證真正四視口（1648／768／390／320）、進場時序、12 欄可達、中文／英文次級權重宣告 200、原 SVG/城牆尺寸比例、鍵盤、反向捲動及 reduced-motion；再做截圖藝術判斷。未看到瀏覽器實圖、未通過所有現行測試時維持 Draft，不得用來源檢查取代視覺驗收。

### 10.14 實際桌面截圖的閱讀密度修正（2026-10-26）

- **不是四個同樣窄的表格欄**：WATCH、WALK 為左側兩個貫通閱讀欄；WITNESS 在第三欄上半，WORSHIP 在同欄下半。十二欄目的四個樂章仍完整保留。這用四組各四個入口的縱向節奏填補原第三／四欄下半大空洞，保留較密的左頁與右側呼吸。小尺寸恢復兩欄可捲動的布局。
- **極細不等於極小或低對比**：次級內容仍守 200，但正文級的目錄篇名增加可讀字號和行距，不能為了極細而把條目做成網頁縮圖；英文 Bodoni 真實字庫的最低重量限制仍在。
- **門內金光不可露出硬矩形底邊**：門洞與門外的投影必須以**同一條門檻共邊**，光從真城門向外延伸；不能用一個在門檻歸零的透明漸層假裝銜接。門外不得恢復原有硬三角暗楔。CI 只能驗形，需以實際封面畫面驗明藝術效果。

### 10.15 以真城門為光源的封面印刷構圖（2026-10-26，藝術審核中）

- **失效根因：**舊 `ws-gate-threshold-fade` 把門洞亮度在出口削至零；舊 `ws-architectural-light` 又把門外折光透明度削至零。兩層最亮的地方恰好互相消失，只剩貼在米黃色石牆上的一片淡黃，無法成為封面畫作。兩者全部撤銷，不能作為 fallback 復活。
- **現行唯一方向：**保留原 Scheme 02 石門位置、官方完整 SVG 壓頭、CITY / *OF* / LIGHT 三行與 5:8 刊型。石拱負形內有由深赭至鮮明暖金的**實色套印**；門檻與門外共用端點，向右側錯位延展為**單個大尺度非對稱金色版畫形**，左側石影反襯明暗；不可成為居中延伸的黃色「道路」或對稱扇。使用整層 multiply 印墨，讓原石材裂紋透過上色的印刷肌理，不能畫成霧光、鏡頭耀斑、寫實光束或放射扇。
- **參考判斷，不是借用素材：**Malika Favre 為 *The New Yorker* 畫的橋拱封面提供「深色建築成為亮色負形邊界」的比例；Mile Modic 的 *Klasika 25* 提供「小門洞主導整張刊面的強烈單方向光面」；Christoph Niemann 的橋樑封面提供「幾何色面必須被建築結構制約」的準則。沒有下載或直接嵌入它們的圖像；只將這些構圖關係轉換為原石牆上可維護的 SVG 遮罩。
- **驗收須看小尺寸：**門與金光一眼可辨為同一事件，陰影與投影有充分明度、色相差，封面上字仍清楚；Desktop、平板、手機與每一個進場階段必須用真實瀏覽器截圖檢查。未達到藝術標準維持 PR Draft。

### 10.16 Vol.00 第一輪獲獎級細調：光不再遮沒刊物識別（2026-10-26，藝術審核中）

- **來自真實 2048px 對頁的問題定位：**大尺度印金與陰影已產生明確封面焦點，但深赭石影正好墊在左下 `VOL.00` 後面；舊字色深藍、字號約 9px，已失去出版資訊應有的可辨識性。同時，82%「封面＋晨星」的固定刊頭才開始低透明進場，等於封面畫作與正式刊名沒有同時形成完整的編輯單位。
- **調整：**`VOL.00` 所在原截圖石影約 RGB(145,118,88)，原深藍字難辨；在本期略加深的石材暗部上使用接近暖紙白 `#fff8e9`，字號至少 10px、字重仍為 200。正式刊頭與期號作為**同一套印層**，在 82% 視覺停頓前完全顯現，既不讓額外文案回流，也不更改刊頭資產。這是時序、對比與信息階層的修正，**不是**添一個特效。仍須對新實圖的實際背景值驗證小字對比。
- **Contents 微調與真圖回歸：**第三欄 WITNESS／WORSHIP 原本兩組細線緊貼；第一次加 row-gap 的實際預覽又暴露 WITNESS 最後一篇與 INTERLUDE 壓字。保留四樂章、全 12 欄與三欄布局，讓可閱讀 Index 佔 64% 頁高、上段 WITNESS 多分一點行高；第三欄條目不再靠 `space-around` 強行拉散，間奏保持在條目下方。真瀏覽器須以兩者的實際 bounding-box 距離阻擋壓字，仍嚴守次級字重 200。
- **封面特寫續修：**門外金光左界原有 `門檻 → 向左下 → 又突然向右下` 的折返尖角，實圖讀成貼上去的紙片而不是同一束光。將金色印刷面和石影改為**一條共邊、直接貫穿到頁腳的斜切線**，不再引入新的光面數量。左下 `VOL.00` 由孤立的 6% 邊距改為靠近下左裁切邊的 3.4%／3.8% 版心錨點；刊期仍在原石影上，不移到午夜藍／刊頭，也不增補無意義框線。
- **評審方式：**按本手冊 §6 的 10 項內部 0–2 分檢查，視覺辨識、刊頭主從、石材印墨、次級對比、動效停頓、手機與可訪問性分開驗；不得用 CI 數字或本條記錄代替主編的實際畫面定稿。
