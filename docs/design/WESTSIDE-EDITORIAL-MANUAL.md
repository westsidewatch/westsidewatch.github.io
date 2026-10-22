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

**Font audit 2026-10-21:** English roles use Bodoni Moda and true Bodoni Moda SC. Chinese Journal / Vol.00 reading **currently resolves to Chiron Hei HK WS**, because the later Design OS runtime declaration overwrites the earlier Noto Serif TC reading variable. The source token JSON and legacy stylesheets still specify Noto Serif TC. This source/runtime mismatch remains open; it does not prove that Noto is the live Journal reading face. Hence the old typography document's `typography-sitewide.css` authority statement is **superseded** by the OS umbrella and compatibility-runtime contract. It is not grounds to migrate or change working entry points.

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


## 6A. Award-calibre release objective — Awwwards / Webby Awards / FWA (2026-10-21)

**User-set quality objective:** design every relevant First Look, Church, Journal, magazine and connected surface to a standard competitive for recognition by **Awwwards, The Webby Awards and FWA**, and self-critique, reject or iterate until evidence supports promoting the work. This is an **internal aspiration and release gate**, never a representation of endorsement, nomination, judging outcome or guaranteed award. A green build / deployed URL does not satisfy this objective.

**External lenses, adapted to the single Westside Design OS:**

- **Awwwards** [published evaluation](https://www.awwwards.com/about-evaluation/): Design 40%, UX/UI 30%, Creativity 20%, Content 10%. Apply this as a design/usability/content balance, not as a fabricated actual jury score.
- **Webby Awards** [current judging criteria](https://www.webbyawards.com/judging-criteria/): structure/navigation, visual design, content, functionality, interactivity and the *overall experience*. Great typography without a readable route or usable interface fails.
- **FWA:** benchmark distinctive digital interaction, original conceptual execution and expressive technical craft. Do not claim the FWA has endorsed Westside or that an internally invented numerical scale is an official award rule.

**Required routed skills (from §4 and `new-westside-editorial-web/SKILL.md`):** `ui.visual-hierarchy`, `ui.design-system`, `ui.taste-anti-slop` for composition; `ui.motion-system`, `ui.motion-forensics`, `ui.performance` for the scroll and door sequence; `ui.interaction-quality`, `ui.accessibility` for use; and `ui.critique`, `ui.visual-verification` for final rejection/approval. The project skill's [visual grammar rubric](../../dore-design/knowledge-lab/skills/new-westside-editorial-web/references/visual-grammar.md) remains the internal 10 × 0–2 review across meaning, subject, distinctive composition, typography, two-ink discipline, hierarchy, purposeful interaction, mobile, accessibility and editability.

**Promotion rule:** 15/20 remains the exploratory minimum in §6; for *award-calibre release review*, aim for **at least 18/20**, with no zero and no unresolved **block** finding. This tougher threshold is a **Westside internal heuristic**, not an award prediction. Independently require no known failures in meaningful scroll progression, motion reversibility, editorial readability, contrast, keyboard/focus, reduced motion, tablet/phone, and browser performance.

**Iteration loop:** `actual deployed view at defined viewport → score + defect (block/important/polish) → smallest coherent owner-file change → compare before/after and static/mid/final states → reject or retain → repeat`. Prioritise the single most consequential defect per round; preserve originals, real copy, protected assets and source-of-truth. Do not inflate a score by ignoring difficult tests. An untested checkpoint must say **NOT VERIFIED**, not **PASS**.

**Evidence:** baseline and new browser screenshots at approximately 1648×928, 768px and 390px, plus 200% zoom, keyboard access, contrast, long text, reduced motion, initial/mid/final scroll and return; geometry audit and Core Contract/build/preview outputs. If the execution environment cannot obtain browser screenshots, keep the result **visually unverified** and the PR unmerged. A user screenshot can establish a *before* defect but cannot substitute for an *after* screenshot.

**Maintainability:** keep one design authority and existing CI only. Put acceptance notes in a review file/PR, not in a parallel OS, CSS runtime or new required workflow. The gate is about improving original art direction and usability, not merely adding effects or making award-looking visuals.


## 6B. Publication-first architecture —「讓整座網站成為一本雜誌」(2026-10-21)

### 6B.1 北極星：先定義任務，才設計版面

**全站最高層的 Layout / First Look / P2 命題：不是讓網站「像雜誌」，而是把它當作真正可出版、可閱讀、可翻閱的刊物系統來編輯。**

> **每一個版塊都必須成為具有自身主題、編輯秩序與刊物性格的一本雜誌；全站則是一個完整的 Westside 出版世界。**

此命題是單一 Westside Design OS 下的**編輯判斷與設計方法**，不是新的字體、色彩、CSS、JS 或獨立 Design System。網站功能仍須可用；「成為雜誌」不可成為隱藏導航、犧牲搜尋、影片、查經或閱讀可及性的藉口。

**P2 的特別使命：**它是全站 First Look 的「雜誌化示範／閱讀入口」，必須讓讀者從每個版塊獨特的內容與媒材，一眼辨認**這是什麼版塊、為何值得閱讀、為何它是一種刊物**。P2 不只是教會頁，也不能把所有版塊強迫成同一種教會刊或單一三欄模板。教會的活水／聚會、Westside Watch 的守望／城市、橄欖山的人物、Cinema 的放映、ONE 的查經，各自成為不同的出版物形態，卻共享一種可信的編輯品質。

**一秒辨識三問（缺一即不得開始美化）：**
1. **身份：**不看導航仍能判斷目前是教會、雜誌、人物、電影或查經嗎？
2. **刊物：**有清楚的主題、主副標、圖文角色、閱讀次序、期號／索引／欄目等適合該內容的出版結構嗎？
3. **獨特性：**把內容換成其他版塊後，這個構圖是否仍毫無變化？如果是，代表它只有共用網站模板，尚未產生該版塊自己的 editorial direction。

### 6B.2 「雜誌」不是固定三欄，也不是裝飾

**版面角色比欄數重要。** Cover（封面）、Opener（卷首／主題經文）、Feature（主報導／人物）、Contents（目錄）、Folio／Imprint（期號／出處）、Archive／Desk（索引／工具）都是可選擇的編輯功能，不是每一屏都必須堆滿的清單。一個版塊應有一個主要編輯命題和一個主要視線入口。

**比例先於裝飾。** 分欄由角色、實際文字、圖像主體及安全區倒推。可探索不對稱三欄（例如左 29 / 中 45 / 右 26），但比例只是**待驗證的候選值**，不是全站固定 Token 或通用答案。左右留白要有受力、方向、節奏和跨欄呼應；禁止為填空而加沒有編輯意義的刻線、標籤、徽章或背景物件。靜止截圖首先必須是一張有主題力量的作品。

**中英雙語是兩種排版聲部。** 英文的 Roman、Italic、真正 Small Caps 與中文的粗／細、題名／長文角色應產生尺度對照，不得只做逐字翻譯式對排。採用唯一 Design OS 當前有效的 Bodoni Moda／Bodoni Moda SC、昭源黑體及既定 semantic tokens；原文件列出的 Noto Serif TC 是尚未清理的來源／舊字體宣告，不得再直接稱為雜誌實際閱讀字體；不得變形拉伸字體，不得以極細微字假裝精緻。先測真實標題、最長篇名、行距、孤行、英文換行、對比，再調裝飾與動效。

**把既有資產當作編輯素材庫。** 首頁影片、晨星、活水刻線、城牆、人物圖、原始 Logo SVG、經文及期刊文章都可被重新編輯成封面媒體、特寫、跨頁、導讀或時間性的 opener；不必每頁重新生成素材。但要追溯原檔與授權，保護已批准資產，控制下載成本，提供 poster／靜態替代、reduced motion、字幕／文字等，不可把重用影片等同於加滿版背景影片。

### 6B.3 參考案例：轉譯機制，不複製外形

2026-10-21 用戶提供的四組視覺參考是**方法案例**，不是應複製的頁面：

| 參考畫面 | 值得移植的編輯機制 | Westside 的轉譯方式 |
| --- | --- | --- |
| Self / Esteem 的三欄版 | 各欄有獨立職責，比例與線條先決定閱讀，空白服務內容 | P2 先命名每個區域的職責，才確定比例、標題與邊界 |
| The Cut 的圖文與 Credits | 超大英文標題、攝影、署名與白場形成主從；資訊密度有章法 | 中文短主題與英文展示聲部、首頁影片截幀、真實文章導讀和出處分工 |
| 實體雙頁／黑底閱讀器 | 頁脊、翻閱、雙頁先建立閱讀的物理邏輯 | 「先形成可觀看的跨頁，再打開／翻頁」；轉場前後兩種靜態畫面都必須成立 |
| It's Nice That 的跨列主視覺 | 圖像是敘事事件，大字與資訊卡只是必要的編輯層 | 讓教會洋流、晨星或首頁影片成為有內容意義的主要媒體，而非無主題的背景 |

**每次研究必須留下：**參考 → 它解決的閱讀問題 → 空間／字體／圖像／動效機制 → Westside 自己的故事及可用資產 → 不適用的部分 → 原創構圖候選 → 驗收證據。嚴禁直接描摹截圖。

### 6B.4 標準工作流程（所有版塊／P2 均適用）

**0｜讀權威與鎖定範圍 — 不先改 CSS。** 閱讀本手冊、Design OS、專案 Skill 與相關版塊的稿件地圖；確認正式已批准的 Logo、照片、影片、經文、頁面入口及動畫不可被覆蓋的範圍。列清楚本次是主站、First Look、P2 實驗或其他版塊。先核對原有 PR / main 與實際頁面，避免另造第二系統、誤碰其他工程或一行一個 commit。

**1｜編輯命題卡 — 用一句話定義畫面任務。** 寫出「讀者是誰／第一眼該懂什麼／應產生什麼情緒／下一個閱讀動作是什麼」。為每個版塊命名它的**刊物類型**，例如教會主日的 weekly folio、Westside Watch 的封面與目錄、橄欖山的人物特刊、Cinema 的放映手冊、ONE 的研經筆記。先列獨特點、內容來源及禁用的 generic 形式。

**2｜編輯內容地圖 — 先決定內容，再決定三欄。** 抽取現有正式文章、標題、作者、欄目、視頻和圖片；分配 Cover／Opener／Feature／Contents／Folio／CTA 的功能。未寫好的文章可以顯示已確認的標題，但**不得虛構稿件**。標出中英文的語意角色及真實閱讀路徑，先完成紙面線框和目錄資訊架構。

**3｜原創 Art Direction — 先做有辨識度的靜態封面／跨頁。** 最多比較 2–3 個**結構上真正不同**的構圖命題；每一個要有主視覺、字級對比、圖像裁切、留白受力、比例、光／紙／墨關係與視線順序。可嘗試 29/45/26，但必須和等權或其他候選比較而不是盲用。需要一眼能辨認的縮圖輪廓，不接受只是舊 DOM 加 CSS 變體。

**4｜先確定終態，再設計轉場。** 一次完成的靜止畫面，必須本身像一份值得出版的編輯作品；之後再設計影片、滾動、折幕、頁脊、開門。為每個可停留節點命名畫面職責，例如「教會完整對開 → 晨星帶西望升起的雜誌封面雙頁 → 左右展開露出真實封面／目錄」。上一頁未完成時下一頁不得搶先開始；除有明確敘事用途的 deliberate hold 外，不准有無變化的滾動死區。滾回須可逆、過場不能打斷閱讀。

**5｜桌面與手機分別編輯，不准整頁縮放。** 桌面可採有主次的非對稱多欄、帶影片的主視覺跨頁；手機在 P2 開門後**只顯示可讀的核心中欄**，封面與目錄按垂直順序閱讀，雙側識別／引言退為封面小資訊或轉場中的短暫角色，不能縮成微型三欄。斷點應改變**內容優先級與排版結構**，不是對桌面截圖做 transform:scale。必要時封面與目錄可自然滾動，不能把整期文章擠進固定一屏。

**6｜在唯一 OS 和既有 owner 檔案實作。** 語義 HTML 承載真實文字，原圖與 approved SVG 原樣引用；使用 scoped styles、semantic type/color/motion tokens；元素相對安全區和欄寬定位。首頁影片的重用需保留封面 poster、效能及使用者控制，不能自動播放有聲音。已有主日洋流、七色折幕、晨星和城牆的資產／方向規範應被尊重。只新增為實現這個 direction 所必需的程式，不加全站新入口、第二 CI 或另一套 CSS authority。

**7｜一輪完整交付＋視覺自檢，不分碎片提交。** 先讓頁面從入場到終態可用，再對照實際桌面／平板／手機畫面逐一檢查：封面辨識、真實目錄可讀、跨欄比例、重心、字形、長標題、安全區、圖片與影片裁切、底部城牆有無拼貼、動效可逆、鍵盤／焦點、reduced motion、200% zoom。使用已部署截圖（包括開門前／後），不能把 CI 綠燈當成設計通過。發現失敗就定位原因、在 owner 檔案修復並重驗，最後一次性匯報已完成的整個階段。

**8｜評審／淘汰／晉級 — 以出版物身份驗收。** 用 §6A 的 award-calibre 目標、現有 Skill 的 10 項 rubric 和獨立功能檢查：是否一眼像該版塊獨有的雜誌、是否可閱讀、是否與全站形成同一出版語法、是否有無意義元素、真實證據是否充足。將缺陷分為 block／important／polish，附實際視窗與前後圖、原因、修正、拒絕方案、剩餘問題。未達內部 ≥18/20、存在 block 或未取得真實新版截圖時，保持 **NOT VISUALLY APPROVED / DO NOT MERGE**，不要宣告已獲獎級品質。

### 6B.5 P2 具體交接與可重用模板

**P2 不是「一張三欄海報」。** 它至少有兩個不同但連續的完整出版畫面：

- **主日／教會態：** 洋流成為編輯的主要材質，右側日程是真實的 weekly folio；要讓讀者看出教會身份、主日資訊與閱讀秩序。
- **87–90% 左右對開態：** 晨星＋原始「西望」向量字形與 Romans 13:12 構成一張完整、可停留的封面跨頁；不是等待 100% 的過場空場。
- **100% 展開態：** 桌面為識別場／主要編輯封面＋目錄／經文 opener 的非對稱跨頁。中欄封面與目錄可以上下成頁，但不規定全站所有版塊都用同一種結構；手機為**單欄封面＋目錄閱讀體驗**。
- **下一個版塊：** 沿用閱讀／翻頁的出版邏輯，**不沿用一模一樣的三欄皮膚**；改由自身的主題、媒體與內容決定下一本刊物如何出場。

**可復用的是方法，不是版式成品：** 每個新 First Look／P2 版塊交付一張 Direction Card、一份真實內容清單、靜態關鍵畫面、跨頁到終態的 motion storyboard、桌面與手機編輯閱讀版、source-asset map 和有證據的 rubric review。各版塊內容與主視覺不可被「全站統一」沖淡。

**拒絕信號：** 只有均勻三欄；只加大英文卻沒有文章；用城牆／刻線／色帶填空；相同版型任意換名；封面漂亮但目錄不讀；手機變成縮略桌面；影片僅作無意義背景；過場無效滾動；未跑視覺驗收便宣布「設計完成」。

**版本與工作節奏：** 設計原則寫回本手冊；項目具體決策與失敗證據寫在原 PR 的 review；代碼只在目前 owner 位置修改。每個完整階段應自行完成實作、可執行檢查與能取得的視覺驗收，集中提交，處理 CI 失敗後再通報；不能無止境地以「下一輪」代替交付。


## 6C. Longform publishing & professional typesetting —「多雷探索」source check (2026-10-21)

### 6C.1 P2 不能只帶來封面；真實雜誌的幾萬字正文必須同時進入設計

**Design scope:** The P2 First Look, Westside Watch issue / volume, cover + contents, article entry, **actual longform reading surfaces**, illustrations, quotations, Scripture, references, footnotes, editorial appendices, search/TOC, and book/PDF export must be designed from **one content authority** and **one Westside Design OS**. Do not complete the P2 card layout only to discover later that 20k–50k-character features cannot be read. Those character counts are **test fixtures**, *not* claims that specific manuscripts have been counted.

The governing idea is **one publication, different reading states**:

| Layer / reader job | Deliverable | P2 / Journal relationship |
| --- | --- | --- |
| Discovery / first glance | P2 issue identity, feature media, brief editorial teaser | Leads to a real issue; P2 **does not carry tens of thousands of words inside a fixed viewport** |
| Issue / curation | Cover, masthead, issue title, full verified TOC, four movements, interludes, editors' selections | Genuine navigation with stable links to real articles and their writing/publishing status |
| Feature / web reader | Semantic longform article, headings, reading column, images, captions, citations, pull quotes, footnotes, video, TOC/progress | Primary **continuous, responsive reading**; no forcibly paginated narrow-phone miniature |
| Folio / page-proof | Spread, page counter, alternating pages, running heads, footnotes, widows/orphans, printable spreads | Opt-in preview / print/export, derived from canonical article HTML, **not a second author copy** |
| Editorial production | Source/provenance, user Author Lock, art-direction decisions, version and visual QA | Doré selects layouts with constraints but never silently rewrites protected prose |

**Actual source audit:** `layouts/vol-00/single.html` currently renders `.article-body .prose` plus a supporting rail; `layouts/journal/list.html` is primarily an issue entry. `content/vol-00/` has brief publication-entry files; **do not infer that manuscripts already exist there**. Real long drafts may live in other book/editorial stores. First resolve the existing manuscript's **canonical source path and permissions**; link a publication consumer rather than copy, truncate or invent content. The [Vol.00 editorial canon](../projects/watch-city-vol00/EDITORIAL_MAP.md) keeps the approved 4–4–2–2, three video/music interludes, feature titles and source boundaries.

### 6C.2「多雷探索」不是泛泛找靈感，而是找可調用的排版引擎

Use the repository's [Doré Explore Trigger](../../dore-core/evolution/DORÉ-EXPLore-TRIGGER-v0.1.md): MEMORY CHECK → 1–3 evidence waves → Doré fit → **USE / ABSORB / EXPERIMENT / WATCH / REJECT** → smallest integration / measured acceptance → evidence return. Criteria are free/low-cost, small enough to run locally when feasible, mature, stable, replaceable, simple, safe, documented; **AI-invocable CLI/API/MCP/HTML-CSS or JSON control is a key selection criterion**, not a claim of autonomous perfect art direction.

**Previous research recovered (2026-10-07/15):** DesignCraft, Folio and Vivliostyle/Paged.js had already been discussed in Doré Exploration, together with layout-candidate search, asset-safe crop and scoring. Their actual decisions were **not recorded in the existing Editorial Manual**, and repository text search did not find an authoritative written integration of those product names. The 2026-09-04 [Editorial Studio architecture](../../dore-design/publishing/EDITORIAL-STUDIO-ARCHITECTURE.md) already insists on one canonical manuscript, provenance, presentation, output, live preview and Author Lock. **Recover and extend that design; do not invent a second editorial studio.**

#### Verified capability map — research, not installed dependencies

| Open-source candidate | Verified entry / licence | Good at | Doré decision / risks |
| --- | --- | --- | --- |
| **Native HTML + CSS + Hugo / OS** | Existing site `layouts/vol-00/single.html`, `static/css/westside-design-os.css`; [CSS text line-breaking](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/line-break) | Semantic uninterrupted article reading, `lang`, bilingual CJK line rules, section anchors, tables, responsive images, accessible footnotes, embedded media, built-in browser text selection/search | **USE now** as web authority. Current templates are a baseline, not a tested longform art-direction engine. No need to download a new giant frontend framework. |
| **[Paged.js](https://github.com/pagedjs/pagedjs)** / [CLI](https://github.com/pagedjs/pagedjs-cli) | MIT; JS `Previewer` API and optional Puppeteer PDF CLI | CSS Paged Media flow, repeated headers/folios, print-proofs from the same HTML | **USE in isolated prototype / export pass**, not as a mandatory runtime for every scrolling article. Test CJK punctuation, footnotes and 50k-char speed/overflow first. |
| **[Vivliostyle](https://github.com/vivliostyle/vivliostyle.js)** / [CLI](https://docs.vivliostyle.org/en/cli/getting-started/) | Core/Viewer/CLI AGPL-3.0; HTML+CSS, CLI, viewer, PDF / EPUB / WebPub | Mature paged book/issue workflows, facing-page spreads, richer footnote and print options | **EXPERIMENT alongside Paged.js** with the *same source fixture*; choose based on fidelity, performance, export and a **licence review before embedding/redistribution**. Do not silently mix AGPL runtime into the public production bundle. |
| **[DesignCraft](https://github.com/storytold/designcraft)** / [MCP](https://github.com/storytold/designcraft/blob/main/docs/mcp.md) | MIT / Apache-2.0; `designcraft-cli mcp`, JSON controls, headless render to PNG, PDF / IDML export | Page/spread composition, threaded text frames, master pages, text wrap, magazine sample, agent-driven layout proposals | **EXPERIMENT in Doré's offline design studio**: test actual native fonts, 50k Chinese characters, fidelity of import/export, speed, stability. The project's documented features are **claims awaiting Westside runtime verification**, not evidence it can replace live Hugo article HTML. |
| **[Typst](https://github.com/typst/typst)** | Apache-2.0; CLI, PDF + other export formats | Alternative strongly typed book/PDF production, scripted print styles | **WATCH / OPTIONAL fallback** if CSS pagination demonstrably fails. Additional markup/conversion cost; not a replacement for canonical web HTML. |
| **[WeasyPrint](https://github.com/Kozea/WeasyPrint)** | BSD; HTML+CSS→PDF CLI / Python | Headless PDF generation, book proofs, CI scripting | **WATCH / comparator** for PDF fidelity if Paged.js/Vivliostyle fail; not an on-screen art-direction tool. |
| **[Folio](https://github.com/Jorgut/folio)** | MIT; Skill/templates; HTML/PPTX/PDF/Figma/IDML | Condensed *promotional* editorial briefs and cover/feature pitch variants | **ABSORB layout-selection methods only**: the author explicitly marks 50+ pages / very long documents as unsuitable; not a 30k-word magazine body composer. |

**Selection principle:** Today's mature tools split into **(a) web reading**, **(b) CSS pagination and export**, **(c) art-directed spread design**. There is no verified single free library that can automatically turn tens of thousands of mixed Chinese/English words into award-quality responsive *web*, print, issue index and cover all at once. The AI role is **constrained layout selection + source-safe adaptation + evidence-led rejection**, not unattended template dumping. Never mislabel a proof engine as a full design director.

**Licensing / dependency gate:** Save direct upstream URLs and pinned versions/SHAs; verify redistribution implications (especially AGPL) with the actual embedding/deployment plan. CLI used offline for candidate previews is a different architecture from embedding its JavaScript bundle into the public site. No install or package-lock change follows from this research chapter.

### 6C.3 Longform layout grammar — real paragraphs, real references, real images

**Editorial design choices must be made per article archetype, not per arbitrary word count.** A history/archaeology essay with maps, a witness/person profile, a theology argument, and a Scripture/sermon study require distinct lead-feature art direction. All share semantic source types:

`Article → chapter/sections → paragraphs → evidence/citation → figure/caption → quote/pullquote → note/footnote/endnote → media/interlude → related items → edition imprint`.

- **Screen reading:** use one readable measure-controlled prose column. On Journal / Vol.00 the effective Chinese reading role presently resolves to Chiron Hei HK WS (昭源黑體) through the later Design OS override, normally at a readable 400 weight. Bodoni Moda / Bodoni Moda SC remain the English display and small-cap families. A dedicated English long-body family is **not yet authoritatively established** and needs testing. Do not force Noto Serif TC or a new English font from an article-local override; reconcile source token JSON, runtime and legacy CSS first. Verify actual rendered font, 390px and 200% zoom on long authentic prose. Do not make 3 fixed columns for a 50k-character phone article.
- **CJK / bilingual detail:** apply `lang="zh-Hant"` / `lang="en"` on actual blocks, test `line-break: strict`, legal `word-break` and fallback fonts, Chinese punctuation line boundaries, brackets/quotation marks, mixed scripture verse references, italic Latin only, hanging-punctuation support *where browsers truly support it*. Never justify mixed-script paragraphs blindly or stretch glyphs.
- **Rhythm:** opener / standfirst / body / subsection / pull quote / annotated diagram / full-width photograph / footnotes / closing. Place interruptions where they advance argument; for very long text allow quiet, efficient stretches of reading. Avoid parallax, scroll-jacking, constantly moving type behind paragraphs or huge artwork every screen.
- **Evidence:** figures must keep caption, source and alt; maps, timelines, diagrams, Scripture variants and Greek/Hebrew snippets need stable references. Footnotes must remain linkable (backref); no citations only in mouse hover. Provide article-local TOC/anchor navigation, reading progress with a real denominator, return-to-place and keyboard navigation **only if independently tested**. Don't fabricate reference numbers/page numbers before pagination.
- **Editorial safety:** source language, ownership, Author Lock and translation variants remain attached to stable block IDs. Layout metadata can change independently; protected prose cannot. Render the same canonical content to web and print adaptors; no parallel hand-edited article copies.
- **Layout data:** an article/section has a named layout family, subject/image references, text-length & heading metrics, break opportunities, figure placements, semantic typography roles, optional pull-quote slots and responsive variants. Doré may propose options, but the actual renderer verifies overflow and human editors can override decisions.
- **Printing:** page numbers/running heads, facing-page offset, recto opening rules, breaks before major parts, orphan/widow prevention, footnote fit, bleeds and PDF legibility belong in the isolated paged-export mode. Do not apply print pagination CSS to the continuous reader.

### 6C.4 Unified project implementation order — P2 re-art-direction + real Journal, together

| Gate | Coherent engineering deliverable | Must prove before passing |
| --- | --- | --- |
| **A — Content inventory & authority** | Find authentic longform manuscript(s), real lengths, attachments, image licences, footnotes and editorial states; make a 5k / 20k / 50k CJK-character **synthetic test fixture** only for performance. Map official Vol.00 title, TOC and links. | No fictional article; no content moved from its source or silently rewritten; no orphaned path. |
| **B — Shared art-direction blueprint** | Design P2 as a *magazine invitation*, Vol.00 as an issue, and each feature as a reading experience; determine cover, Contents, recurring article families, folio and media. Study 2–3 truly distinct static layouts at desktop and mobile. | All three levels read as one publication; no P2-only beautiful facade with generic article pages. |
| **C — Longform reader FIRST functional baseline** | Extend the owning Hugo `layouts/vol-00/single.html` / article components using OS tokens, semantic HTML and a readable CSS measure. Article-local TOC and citations are data-backed. | Actual or legally safe fixture survives long Chinese text, mixed Latin/Scripture, 30+ headings, tall images, captions, anchors, focus, return nav, text selection, 200% zoom, 390px. |
| **D — Professional layout proof comparison** | Feed identical canonical HTML+CSS fixture to Paged.js and Vivliostyle in **separate nonproduction experiments**. Evaluate DesignCraft MCP for art-directed special spreads only. Folio not used for longform. | Measure time, memory, page overflow, font fallback, CJK punctuation, footnote position, captions, widows, PDF fidelity, accessibility and file size. Pick at most one primary paging pipeline; record why others lost. |
| **E — P2, issue and reader integration** | Connect discovery→issue TOC→long feature→next feature with stable real links. Optionally reuse existing homepage video/poster in the *appropriate* cover/section, no duplicate content. Introduce motion only after accepted static frames. | Desktop multi-column for teasers but mobile full-width continuous reading; P2 phone opens only its readable centre; no dead scroll, protected original animation assets remain. |
| **F — Award-calibre verification and promotion** | Side-by-side desktop 1648×928 / tablet 768 / mobile 390, 200% zoom; true 20k/50k fixture and real article; print proofs; contrast/keyboard/reduced-motion/long-scroll performance; actual images; CI and deployment. | Existing §6A rubric ≥18/20, no 0 or block, **actual visual evidence**, documented regressions and approved canon. Otherwise **NOT VERIFIED / DO NOT MERGE**. |

**Acceptance metrics to measure, not guess:** longest article scroll depth and time-to-content, client JS weight added by optional renderer, paged preview wall-clock time and peak memory, blank/overflow pages, exact CJK line breaks at standard widths, screenshot diffs of sample figures, total interactive errors, PDF font embedding/links and mobile usability. Compare cold/hot cache separately. Report results as measurements or **NOT TESTED**, not imagined percentage gains. Avoid forcing one giant manuscript into a single JS-rendered DOM if performance deteriorates; preserve the addressable section structure.

**Doré-fit decision as of this research:** **USE** existing OS + Hugo semantic longform web reader; **EXPERIMENT** Paged.js for professional book-like proof and Vivliostyle for full publication; **EXPERIMENT** DesignCraft as the agent-driven special spread/cover composer; **ABSORB** Folio's short-form layout selection rather than longform rendering; **WATCH** Typst and WeasyPrint as secondary print pipelines. No engine chosen as production dependency until the same real sample passes the above gates.

**Workflow and scope:** The 6B publication-first workflow is extended, **not replaced**. This is one OS and one linked P2 + Journal project plan, with shared canonical manuscript and scoped output adapters. Keep any future implementation in owning layouts/CSS/CLI tasks, not new competing design management software. The research itself modifies **this Markdown manual only**, not production code or installed dependencies. Project PR evidence belongs to its existing review file and project tracker, not a new release CI.

### 6C.5 Font-authority audit — 2026-10-21

**Journal/Vol.00 effective path:** layouts/_default/baseof.html classifies both as Sites surfaces. They load static/css/westside-design-os.css and static/css/westside-typography-enforcement.css, without the non-Sites assets/css/typography-system.css. The OS runtime declares Noto Serif TC early, then explicitly overrides --ws-type-reading-zh to var(--ws-type-display-zh), whose later value is Chiron Hei HK WS. Enforcement consumes this resolved variable for .prose paragraphs. It is therefore incorrect to document Noto Serif TC as the active Journal Chinese reading face.

**Still unresolved:** design-system/tokens/westside.tokens.json, static/css/westside-design-tokens.css and assets/css/typography-system.css retain Noto Serif TC. Non-Sites reading surfaces can differ. Existing source/runtime drift must be resolved in the single Design OS rather than in an article-specific patch. Actual browser font loading and final English long-body typographic choice have not been independently verified.

**Action gate:** Before professional 20k/50k-character publishing tests, audit computed font-family and loaded fonts for Journal, Vol.00, general book reader and tools, reconcile canonical JSON with runtime intent, validate both scripts at desktop, phone and 200% zoom. This documentation-only check does not reassign runtime tokens and is NOT a visual acceptance pass.

### 6C.6 Chinese reading font source-of-truth repair — pending cross-surface visual QA

The 2026-10-21 P2 typography normalization moves the **existing effective Chinese reading decision** (Chiron Hei HK WS / 昭源黑體, 400 for long body) into canonical `design-system/tokens/westside.tokens.json` for both display and reading family roles. The generated CSS is updated by the existing Design OS generator. The OS umbrella and legacy compatibility bundles no longer redeclare conflicting `--ws-type-reading-zh`/display family values; article `.prose` explicitly consumes the reading role and the enforcement selector consumes the same source.

**Change exposure:** the Journal / Vol.00 Sites CSS resolves to the same intended Chiron family as before. Non-Sites pages could previously resolve to Noto Serif TC; they will now resolve to Chiron where using the OS token and **must be checked** in actual browser after this change. Noto webfont imports remain temporarily for explicitly authored legacy consumers, not as an approved primary reader choice. This is not authorization to replace Chinese type with Song/Kai or introduce a new English font.

**Gates:** generated tokens check, existing Design OS/First Look contracts, cross-surface actual computed family and loaded font file, long Chinese text (20k–50k test fixture plus real articles) at phone/tablet/200% zoom, English longform typesetting choice after real body-copy trials. Tests with fallback fonts do not prove the Chiron webfont loaded. Until these pass, **FONT VISUAL QA OPEN / NOT APPROVED**.

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
