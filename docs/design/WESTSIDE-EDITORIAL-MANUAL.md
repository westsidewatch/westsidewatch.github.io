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

**比例先於裝飾。** 分欄由角色、實際文字、圖像主體及安全區倒推。P2 雜誌不再以獨立三欄作為候選；探索影像主場與閱讀主場的關係，但比例只是**待驗證的候選值**，不是全站固定 Token 或通用答案。左右留白要有受力、方向、節奏和跨欄呼應；禁止為填空而加沒有編輯意義的刻線、標籤、徽章或背景物件。靜止截圖首先必須是一張有主題力量的作品。

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

**2｜編輯內容地圖 — 先決定內容和閱讀次序，再決定圖文關係。** 抽取現有正式文章、標題、作者、欄目、視頻和圖片；分配 Cover／Opener／Feature／Contents／Folio／CTA 的功能。未寫好的文章可以顯示已確認的標題，但**不得虛構稿件**。標出中英文的語意角色及真實閱讀路徑，先完成紙面線框和目錄資訊架構。

**3｜原創 Art Direction — 先做有辨識度的靜態封面／跨頁。** 最多比較 2–3 個**結構上真正不同**的構圖命題；每一個要有主視覺、字級對比、圖像裁切、留白受力、比例、光／紙／墨關係與視線順序。可嘗試 29/45/26，但必須和等權或其他候選比較而不是盲用。需要一眼能辨認的縮圖輪廓，不接受只是舊 DOM 加 CSS 變體。

**4｜先確定終態，再設計轉場。** 一次完成的靜止畫面，必須本身像一份值得出版的編輯作品；之後再設計影片、滾動、折幕、頁脊、開門。為每個可停留節點命名畫面職責，例如「教會完整對開 → 晨星帶西望升起的雜誌封面雙頁 → 左右展開露出真實封面／目錄」。上一頁未完成時下一頁不得搶先開始；除有明確敘事用途的 deliberate hold 外，不准有無變化的滾動死區。滾回須可逆、過場不能打斷閱讀。

**5｜桌面與手機分別編輯，不准整頁縮放。** 桌面可採影像主場與閱讀主場的非對稱構圖、帶影片的主視覺跨頁；手機在 P2 開門後**按閱讀順序保留圖像、主標題、目錄及內容入口**，封面與目錄按垂直順序閱讀，雙側識別／引言退為封面小資訊或轉場中的短暫角色，不能縮成微型的桌面分區。斷點應改變**內容優先級與排版結構**，不是對桌面截圖做 transform:scale。必要時封面與目錄可自然滾動，不能把整期文章擠進固定一屏。

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

### 6C.7 Full editorial headline size grammar — 2026-10-22

User-approved structure: primary Chinese headlines are Chiron 900, smaller than *much larger, optically delicate English Bodoni 400*; all other non-body Chinese editorial headings and names are genuine Chiron 200, expanded in size and editorial spacing so they do not disappear into prose. Longform body / accessible functional labels remain 400. This is one Design OS source, not additional per-page CSS exceptions: twelve detailed semantic typeScale tokens are generated from the existing canonical JSON and documented with numeric ranges, layouts and migration constraints in [Editorial Typography](WESTSIDE-EDITORIAL-TYPOGRAPHY.md). The P2/Journal prototype and each edition use these semantics; a real magazine's article H2/H3, standfirst, byline, Contents and scripture must not be confused with primary titles. Existing homepage image assets are protected and all real pages must pass before/after screenshots and 200% zoom before adoption.


## 6D. Doré exploration — Westside Watch Magazine Art Direction: **Classical in Soul, Contemporary in Expression** (2026-10-22)

**Research status: art-direction hypothesis / sources indexed, NOT a redesigned or visually approved P2.** This research is part of the **one Westside Design OS editorial manual**. It is neither a second visual system nor permission to alter a protected poster, homepage logo, sevenfold asset, or live site. The separate Design OS 12-role typography scale is only *technical infrastructure*; actual magazine proportions must now arise from an authored visual identity.

### 6D.1 The question changed: from a general type scale to an original magazine

North star: **讓整座網站成為一本雜誌，而不是讓每個網頁看起來都有幾張雜誌截圖。**

**Proposed identity:** **Engraved Editorial Modernism / 刻線現代主義**. Editorial expression: **Classical in Soul. Contemporary in Expression. / 古典為魂，當代為形。** This is a *direction to test*, not a new published strapline or final magazine title. The existing official WESTSIDE WATCH SVG and 《西望》 remain the brand assets and must not be silently replaced.

- **Classical source:** genuine Doré-derived engraved line, primary historical/archival illustration, stone or papyrus-related substrate from the relevant section, bookish precision, Bodoni Moda's fine high-contrast Roman and true Italic, marginalia, folios, civic/topographic histories.
- **Contemporary realization:** 900 Chiron Chinese main names against much larger optically fine English Bodoni 400; Chiron 200 supporting names enlarged to carry heading authority; severe hierarchy, asymmetric grid, seven *semantic* realm colors, image/letter collision evaluated as editorial geometry, a living transition model, restrained motion.
- **Publication promise:** individual issues and each of seven site realms have distinct content and color, but retain **one recognizable grammar** across P2, cover, contents, feature opener, 20k–50k-character actual reading, archive and print.
- **The critical anti-goal:** *classical ≠ generic sepia/Victorian ornament*, *contemporary ≠ giant type + an animation plugin*, *magazine ≠ fixed 3 equal vertical boxes*. Nor should one P2 be mistaken for the whole publication system.

**Prior research recovered, not erased:**
- [New Westside Visual Reference System](../../dore-design/new-westside/VISUAL-REFERENCE-SYSTEM.md): already expresses New Classicism + Editorial Modernism + Archival Print + Doré engraving + Living Wall, with archival material intensity bands and explicit anti-fake-vintage rules. **Its 2026-08 typography candidates (Cormorant / Noto Serif) are superseded by the CURRENT Bodoni Moda / Chiron OS decisions; preserve the historical research, not the old fonts.**
- [Westside Magazine Kinetic Typography Memo](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md): type as hinge/plane/navigation; static composition must succeed *before* motion. Codrops gives animation techniques, never dictates our editorial appearance.
- [Doré Magazine Composition Contract](../dore/MAGAZINE-COMPOSITION-CONTRACT.md): real editorial brief → source retrieval → asset provenance → grammar candidates → rendered comparisons → human editorial signoff, not one AI moodboard result.
- [Existing magazine reference expansion corpus](../../dore-design/knowledge-lab/research/design-reference-library-expansion-20260901.json) and [Brand Bible Reference Registry](../../dore-design/research/BRAND-BIBLE-VI-CI-REFERENCE-REGISTRY-2026-09-03.md): previous large research exists, but often addresses the homepage and generic design-system concerns, not the specific 2026-10-22 P2 + 20k+ magazine publishing question.

### 6D.2 Research method: broad scan, narrow formal analysis, then original syntheses

Reviewed research leads across print independent publishing, literature, fine art, visual archive, filmmaking, and web-native editorial. **A reference gets an 'A' only where a magazine/studio/art-director account or clear interior spreads supply evidence; 'B' means a verified published account / archive; 'C' means a contextual or UX reference without full spread-level validation.** The numbers below are *curation labels*, not award scores or page quality ratings. A source may inform method even when its visual aesthetic is rejected.

For every reference preserve **publication/studio + primary URL + observed device + what NOT to copy + Westside transfer + P2 testing surface**. Evaluate actual printed *interior sequences*, not merely beautiful mastheads. Analyze at least 5 spread states: cover → Contents → section opener → text-heavy article → archive/index. Inspect mobile/web behavior separately from the printed spread. Do not claim a source's image asset is licensed for reuse: links are research only.

#### Deep study A — 14 high-value precedents

1. **Kinfolk / Alex Hunting Studio — A / [studio + photographed spreads](https://alexhunting.studio/blogs/projects/kinfolk)**. Specific finding: they redesigned the editorial grid and built matched Serif/Text, Serif/Display and Sans families. **Transfer:** monumental high-contrast display may vary optically from readable text; true page hierarchy spans headlines *and* long reading. **Do not copy:** beige lifestyle photography or their custom faces. **P2 test:** one classical giant serif phrase juxtaposed with a sharply weighted small Chinese 900 title, *then* a calm readable article page.
2. **MacGuffin — A / [source magazine](https://www.macguffinmagazine.com/about), [magCulture inside spread](https://magculture.com/blogs/journal/macguffin-13)**. An apparently humble topic becomes a rigorous long editorial world; archival photos, visual inventories and unpredictable pages coexist in coherent sequencing. **Transfer:** excavated historical objects, maps, archaeological plates and engraving become genuine *argument and evidence*, not repeating decorative wallpapers. **P2 test:** one old-city engravable plate with archival caption integrated into actual contents.
3. **MUBI Notebook / Pablo Martin — A / [art director interview](https://magculture.com/blogs/journal/pablo-martin-notebook), [official magazine](https://mubi.com/en/notebook/magazine)**. A video-cultural publisher's print identity is consistent with screen/image assets, without turning print into a screenshot of the player; design follows each story and remains typographically distinct. **Transfer:** reuse an **existing approved homepage video or its verified legal still** as the editorial image field, with a true issue opener and readable fallthrough (avoid adding video merely for motion). **P2 test:** 87–90% held composition as independent cover; 100% video-still/engraving/editorial transition.
4. **Real Review / OK-RM — A / [design interview](https://www.itsnicethat.com/articles/real-review-jack-self-ok-rm-18082016), [format analysis](https://bpando.org/2017/09/25/hands-real-review/)**. The *vertical fold and four-page spread* make magazine structure itself the signature; its fourfold reading logic is not an arbitrary row of cards. **Transfer:** P2 door/divide movement can become a credible issue opening/format reveal. **Reject:** copying an A4 fold visual effect or sacrificing mobile access to reproduce physical mechanics. **P2 test:** asymmetrical widths with actual content hierarchy, then natural 1-column mobile.
5. **The Paris Review / Matt Willey, Pentagram — A / [official studio case](https://www.pentagram.com/work/the-paris-review)**. A deliberately modern identity retrieves precedent from 1960s–70s archival issues, uses clean cover discipline and warmer tactile book stock. **Transfer:** historical continuity can be editorially rigorous without looking antique. **Avoid:** reproducing its new sans-serif wordmark or imitating literature-only severity. **P2 test:** warm page/margins with high-density feature after an expressive opener.
6. **The Gentlewoman / Veronica Ditting, Van Bennekom — A / [magCulture close-up](https://magculture.com/blogs/journal/details-the-gentlewoman-12), [designer background](https://thegentlewoman.co.uk/names/veronica-ditting)**. Information, reference pages and small typographic cues are carefully edited, not subordinate to cover glamour. **Transfer:** masthead and tiny archive folios, photo/quote decisions, captions/real contributor records. **Avoid:** aesthetic minimalism emptied of substance. **P2 test:** Contents and P2 side columns work even with genuine longer titles.
7. **INQUE / Matt Willey — A / [designer](https://mattwilley.co.uk/INQUE-Magazine), [editorial review](https://www.creativereview.co.uk/inque-magazine-editorial-design/)**. Big-format experimental literature can give a single giant word or numeral an entire spread while still containing extensive writing. **Transfer:** let *one word / one number / one engraving crop* occupy half the visual field. **Caution:** INQUE deliberately has **no web edition**; treat as print reference, never claim a working digital design. **P2 test:** an oversized short English title that responds to the water/gate field.
8. **Cereal / Studio Faculty — A / [studio breakdown](https://www.studiofaculty.com/work/cereal-magazine)**. Remarkably, they **minimized type-size contrasts** and created hierarchy through negative space, numbering, time-of-day breakers and an eight-column grid. **Transfer:** text can have quiet but high-quality rhythm, and the real Contents sequence can replace decorative labels. **Reject:** imposing Cereal's calm, small type on every Westside dramatic opener. **P2 test:** after the monumental opener, sharply quieter inner reading/contents field.
9. **Fantastic Man / Jop van Bennekom — A / [D&AD record](https://www.dandad.org/work/d-ad-awards-archive/fantastic-man), [studio art direction](https://bureauantoineroux.com/projects/fantastic-man)**. A consistent, bookish editorial tone tolerates changes of palette and headline system from issue to issue. **Transfer:** the seven realm colors operate as *issue registers* within one grammar, not seven CSS brands. **Avoid:** copying ironic men's-magazine mannerisms.
10. **The World of Interiors / GTF — A / [2022 design account](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles)**. Heritage is curated with strong typography, big folio numbers and readable texts; an archival identity remains contemporary across digital and print. **Transfer:** recover old material at meaningful scale without the generic 'aged paper' effect. **P2 test:** arch/topography plate, oversized issue number, legible double-column index.
11. **The Plant / [official publication](https://theplantmagazine.com/about) — B**. A botanical subject is expanded through photography, illustration, literature and reportage. **Transfer:** test organic engraved *source imagery*, not generic pastoral texture; especially relevant to Bible geography and living-water sections. **Avoid:** making the Church page a botanical lifestyle journal.
12. **The Fence / [magCulture five-image review](https://magculture.com/blogs/journal/the-fence-26) — B**. Restricted colors and the occasional huge graphic/brush mark shape a recognizable dense publication. **Transfer:** use existing section ink/paper semantic colors selectively; small text can coexist with intentionally bold editorial interruptions. **Reject:** generic red/black newsprint collage.
13. **Sight and Sound / Pentagram — A / [official redesign](https://www.pentagram.com/work/sight-and-sound)**. Reworked identity for print and screen, aligned to serious film criticism rather than decorative cinema motifs. **Transfer:** editorial video should be part of the same cultural publication, not a disconnected portal.
14. **The Book of the Flower / Pentagram — A / [studio](https://www.pentagram.com/work/the-book-of-the-flower)**. Classical biological/illustration material meets deliberate modern serif, high page-scale contrast and finely controlled absence. **Transfer:** strongest adjacent proof of engraved/archival subject matter carrying a modern publication without a 'vintage filter'. **P2 test:** one monumental engraved plate facing monumental text; not a tiny repeated castle wallpaper.

#### Broader evidence index B/C — verified source URLs and single learning objective

**Independent print / cultural periodicals**
15. [Apartamento — publisher](https://www.apartamentomagazine.com/apartamento-everyday-interiors-magazine-publisher/about/) (B): authentic documentary life/interiors; avoid sterile staged mockups.
16. [Openhouse Magazine](https://openhouse-magazine.com/about/?v=7516fd43adaa) (B): architecture and space as editorial structure.
17. [The Gourmand / Lane & Associates](https://www.laneandassociates.co/work/the-gourmand-journal) (A): one coherent custom type sensibility through real spread types; culinary style itself is not relevant.
18. [Civilization / magCulture issue 1](https://magculture.com/blogs/journal/civilization-1) (B): master the rules of density before deliberately disrupting them.
19. [Frieze magazine](https://www.frieze.com/magazines/frieze-magazine) (B): culture-led image authority; avoid a generic product grid.
20. [Eye magazine](https://www.eyemagazine.com/issues) (B): formal editorial critique and issue-specific graphic personality.
21. [The Paris Review, additional AIGA analysis](https://eyeondesign.aiga.org/whats-past-is-prologue-inside-the-redesign-of-the-paris-review/) (B): compare modern typography against a historic issue archive before editing.
22. [MacGuffin issue 1 / magCulture](https://magculture.com/blogs/journal/macguffin-1) (B): true archive + collage as research, not ornaments.
23. [The Gentlewoman issue 22 / Stack](https://stackmagazines.com/product/the-gentlewoman-issue-22/) (B): portrait, typographic interruption, apparent 'empty' pages with purposeful identity.
24. [Kinfolk 2016 redesign / It's Nice That](https://www.itsnicethat.com/news/kinfolk-redesign-issue-22-211116) (B): typography changes affect feature openers and editorial maturity.
25. [The Happy Reader / magCulture anniversary overview](https://www.itsnicethat.com/articles/magculture-ten-best-designed-indie-magazines-publication-project-061125) (B): heritage paperback references with lively modern editing.
26. [Backstage Talks / Chloe Scheffe](https://www.designandpaper.com/a-gritty-evolution-in-print-backstage-talks-issue-8-designed-by-chloe-scheffe/) (B): contemporary graphic confidence; avoid deriving the classical layer from this source.
27. [The New Yorker / magazine + editorial archive](https://www.newyorker.com/about/us) (B): a drawn visual world can keep editorial identity coherent across issues and platforms.
28. [The New Yorker 3-column redirection](https://www.itsnicethat.com/articles/nicholas-blechman-the-new-yorker-goings-on-about-town-redesign-publication-250618) (B): grid responds to content density instead of a universal fixed column count.
29. [The New York Times Magazine / 2026 redesign](https://d3buuag9gcp8bb.cloudfront.net/features/gail-bichler-the-new-york-times-magazine-redesign-publication-spotlight-080426) (B): expressive large typography *and* credible longform legibility in one publishing ecosystem.
30. [Cultured Magazine / Time Studio NYC](https://www.timestudionyc.com/cultured-magazine) (A image/studio): truly monumental serif letter scale can *become* the visual composition, not a label on a colored rectangle.
31. [Pleasant Place / botanical issue sample](https://publicknowledgebooks.com/products/pleasant-place-issue-2-nasturtiums) (C): expressive colors and plants; reference for imagery only, not an overall identity.
32. [YES & NO / Pentagram](https://www.pentagram.com/work/yes-no-magazine) (A studio): the *editorial premise* determines the graphic system, not the other way around.
33. [Citizen / Pentagram](https://www.pentagram.com/work/citizen) (A studio): a reusable grid, identity and art-direction foundation for future issues.
34. [The Real Review #2 / magCulture](https://magculture.com/blogs/journal/real-review-2) (B): verify the entire multi-page fold, not a single 3-column screenshot.

**Screen-native and transition grammar (compare behavior, not print aesthetics)**
35. [WePresent editorial redesign](https://svo.co/wepresent) (B): modular text/image/video/audio article modules; P2 should open an accessible, flexible article.
36. [NOWNESS](https://www.nowness.com/about) (B): edited moving-image culture; poster/still/frame choice matters as much as cinematic motion.
37. [The Creative Independent](https://thecreativeindependent.com/) (C): dense navigable editorial content and discovery beyond glossy cover.
38. [MUBI Notebook online](https://mubi.com/en/notebook) (B): video culture, cinema criticism, archive, print connection.
39. [Pentagram editorial work directory](https://www.pentagram.com/editorial-design) (C reference-discovery index): future source sampling, not a single finished case.
40. [Siteinspire Editorial category](https://www.siteinspire.com/websites/category/editorial) (C digital-discovery index): collect real working motion and mobile samples before adopting technology.
41. [magCulture archive](https://magculture.com/) (B industry source): continue searching articles + five-image interior reviews; *do not* treat its storefront as an editorial design template.
42. [D&AD independent publishing overview](https://www.dandad.org/annual/2024/editorial/voices-the-new-gen-of-magazine-design) (B industry jury context): motion/video and multi-channel publishing are editorial instruments, not proof of design quality alone.

**User-provided visual references, supplied 2026-10-22:** (U, primary user image evidence; URLs absent, therefore do not invent them) (a) Self Esteem's **uneven three-column** editorial index; (b) The Cut editorial opener with oversized type against genuine article/credit columns; (c) book spread combining archival line/diagram with reading matter; (d) It's Nice That oversized photographic triptych + contrasting white headline block. These are more useful for P2 geometry than most generic magazine landing pages. Preserve them as **observed screenshots**, not claiming licensed source assets.

**Evidence honesty:** these are 42 verified **source paths** across multiple families, **not 42 completely audited publications** and not proof that live websites retained the same layouts since publication. Full inside-page analysis was concentrated in the A-tier studio/interior sources. Case study links, not image copies, are the archive. Further specimens should be tagged with screenshot/date, owner, image rights, page type, class of evidence, method learned and rejection reason.

### 6D.3 The first original Westside grammar — one identity, three editorial modes

**Unifying idea:** a contemporary publication **made of historical traces, monumental lettering, measured reading and light**. The interface itself should look intentionally composed even when no movement is playing. Do not create separate Church OS, Journal OS, Doré OS or print OS; these are compositional states under the same Design OS tokens.

**Mode I — MONUMENT / 紀念碑式開場 (P2 issue, feature opener).**
- One *large* Bodoni Roman headline can fill **half a screen or half a spread**; if the story needs it, a word can crop at the field boundary by deliberate design, not accidental overflow. A smaller Chiron 900 primary Chinese line stands as the visual counterweight. English **400** is truly slender from the Bodoni type design, not synthetic 200.
- One full-bleed engraving, genuine photographic still, antique topographic plate, or video visual takes the other high-gravity field. Engraving may be magnified so ink strokes become spatial rhythm.
- Other text must be sufficiently sparse to make the composition legible and intentional. Tiny Contents text never competes with the issue's main title.

**Mode II — ATLAS / 城市圖譜 (section spreads, indices, illustrated essays).**
- Archival maps, Doré source engravings, chapter numbers, marginalia, precise captions and contemporary ruled layouts combine as *evidence*. 2-ink or restrained section colors carry hierarchy; papyrus/stone appears where relevant, not as universal background wallpaper.
- Expand or contract an asymmetric six/eight/twelve-column grid as needed. A visible **three-column spread** is a meaningful editorial arrangement when it has dominant lead image/text, an index register, and supporting copy. It is **not** three equal blocks with empty decorative columns.
- The seven realm colors act like seven classified registers/inserts of one issue. On a single screen, no obligation to display seven simultaneous colors or reuse the same photo/ornament on each realm.

**Mode III — READING / 長篇閱讀 (20k–50k-character essays).**
- After the expressive opener, the page rests into a genuine calm, measure-controlled reading column. Chiron 400 Chinese text. Supporting Chiron 200 is **larger by editorial semantics**; main Chinese 900 only at true large title moments, not every h2/h3. Bodoni English long-body selection is still open—do not turn every paragraph into Bodoni merely to signal 'magazine'.
- Opening paragraph, chapter transitions, pull quotes, authoritative sources, endnotes, illustration plates, and references need individually tested patterns. Print output and browser reading are distinct render modes from the same canonical text.
- No page-turn simulation or animated texture behind reading. For mobile, the page is one full-width well-spaced article with useful index/anchors.

### 6D.4 What the current P2 still gets wrong — use actual 87%/100% screenshots

This critique is about the **user's real earlier screenshots**, not inferred new renders; no exact pixel measurements claimed.

- **87–90% held cover:** 50/50 mustard/navy columns, a centered static Chinese vertical logo, star, and scripture = three independent posters. They meet at a seam, but the type, engraving and architecture have **no editorial dialogue**. Large blank fields are merely unused area because nothing in the type/asset composition gives them a function.
- **100% opened triple page:** P2 uses near 1/3–1/3–1/3 widths, a mechanically split cover + dense miniature Contents in the center, and rigid sidebars with a repetitive Jerusalem wall wallpaper under all. This feels more like three colored application columns than a magazine's purposefully edited opening spread.
- **The central design error:** a uniform UI grid was promoted to art direction. The official magazine logo and article names are mostly present, but image scale, line treatment, article hierarchy, issue narrative, and the switch from *cover* to *reading* are not conducting the page.
- **The wall asset is evidence of architecture, not a footer pattern.** Do not repeatedly tile crenellations across all panels at a fixed 32px height. Use a properly sourced plate, intentional single architectural landmark/gate and subject-relevant partial crop; preserve asset provenance and use correct responsive scaling/texture seams.
- **Mobile:** P2 previously failed by shrinking a triple spread until text broke. After doors open, **show only the editorial center as a proper full-width magazine reader**; leave left/right atmospheres in the transition/entrance, not as two permanently compressed columns. Keep reduced-motion and keyboard navigation.

### 6D.5 Proportion experiments to do BEFORE changing global type sizes

Three tests of **one** future magazine language, not three conflicting Design OS branches. Percentages below are **first-render hypotheses**, not approved tokens or existing site measurements.

| Candidate | At the 87–90% held transition | At 100% open | What the experiment tries to learn |
| --- | --- | --- | --- |
| **A · Monumental Engraving** | One 42/58 asymmetric spread: giant fine-line serif + light/engraving/vertical 「西望」 respond to each other | one engraving field facing one unified editorial field: central large cover/real editorial lead; sides become marginalia/short excerpt, *not card columns* | Can classical print/image and modern giant headline produce tension without filler? |
| **B · Living Atlas** | One dark/light historical plate rises to cover 35–45%; type becomes the other 55–65%, with a single engraved architectural axis | one archival image field and one contents/editorial field containing contextual notes; no third vertical register or repeating city-wall strip | Can Jerusalem/Doré material become article evidence, not decoration? |
| **C · Cine-Folio** | Verified reused homepage video still is a *print-cover image* with an asymmetrically cropped serif title, not an auto-playing wallpaper | At 100%, source video/still becomes one chapter opener; text and contents move to differentiated page areas with working article link | Can the video-to-print translation feel like the same publication as P2/Journal? |

**Common candidate invariant:** actual official WESTSIDE WATCH logo, approved text, Chiron 900 main and 200 subheads, true Bodoni 400, authentic image asset provenance, seven semantic realm colors (one major field at a time), current church water/door story, reduced-motion support. **No new font or global color OS.** Do not include all visual techniques on the same page.

**Dynamic type proportions, to be derived from selected style:** A single English display letter may occupy 20–50% of screen width or nearly half the page height for an opener; this is an *art-directed exception* to the usual 72–160px display scale, requiring an opt-in and clear crop-safety logic within the existing OS, not arbitrarily increasing `--ws-type-scale-editorial-hero-en` globally. Companions must be legible. Chinese 900 can be smaller and heavier while 200 support titles rise into secondary prominence by spacing and measured size. Update numerical scale *after* picking a candidate, not before.

### 6D.5a Binding composition and homepage boundary — 2026-10-22

Real screenshots reject all **independent three-panel magazine spreads**, including unequal 20:55:25 and 23:53:24 examples. Those proportions above are now historical hypotheses, **not approved layouts**. Keep the current **full-bleed video homepage unchanged**: no changes to playback, framing, sequence, hero crop or motion. Only after choosing one Westside magazine grammar may its homepage *font size, weight and arrangement* be proposed as a separate scoped visual change. For A/B/C, prefer a continuous **primary image/media field paired with one editorial reading field**; place TOC, contextual quote and article entry *within* the reading field rather than inventing a third autonomous color strip. Internal Contents grids are only a text-layout aid, not a triptych. Mobile preserves visible media and content in editorial reading order. This ruling belongs to Design OS and supersedes earlier §6B/§6D tentative 3-column ratios; it does **not** change the unrelated Church service schedule's functional fields. Original homepage/P2 code stays frozen while the isolated proof is visually reviewed. **Not approved to merge.**

### 6D.6 Required next workflow — selection before implementation

1. **Real reference montage:** create a comparative source board with at least 12 clear interior-spread images and 6 functioning digital editorial pages; log provenance/date, page type, device, negative examples. No direct copying of licensed images into Westside assets.
2. **Freeze publication editorial content:** use the actual `docs/projects/watch-city-vol00/EDITORIAL_MAP.md` 4–4–2–2 issue map and three interludes, plus a real article excerpt (not invented titles) and authorized video/engraving sources. Compare use of portraits/stills against safe crops and copyright.
3. **Make 3 materially distinct art-direction prototype spreads** A/B/C above (real content), one 87–90% held screen and one 100% screen **per candidate**, plus an article opener. Static appearance is reviewed before running any animation.
4. **Editorial jury / contrast:** compare against the supplied Real Review-like multi-column, The Cut opener, print longform and It's Nice That image triptych screenshots. Score identity, novel classical-modern synthesis, focal direction, serif scale, Chinese 900/200 hierarchy, archival authenticity, useful negative space, index/reading handoff, responsiveness and motion as narrative.
5. **Choose one** and integrate it into the existing P2 proof. Then adjust only justified scoped Design OS sizes, position rules and assets; do not accumulate independent alternative live systems or 100+ micro-commits.
6. **Test a real article as part of the same design package**, with 390/768/1648px and 200% zoom; verify genuine fonts, actual text, longform accessibility, video fallback, reduced-motion and generated PDF/print only where applicable. P2 and print must be one editorial identity, not a screenshot of each other.
7. **Sign-off gate:** record actual browser screenshots, exact branch/deployment, checks and editorial choice in `P2-MAGAZINE-ART-DIRECTION-REVIEW-1352.md`. Only after genuine improvement should the candidate become normative Design OS grammar. Until then **STYLE EXPLORATION / NOT APPROVED / DO NOT MERGE**.

**Research-derived maxim:** The magazine is recognized not by three columns, old paper, or giant type in isolation, but by **editorial sequencing and consistent authorship of visual decisions**: a distinctive opening, factual imagery, readable text, meaningful pauses and surprising scale shifts. Classicism supplies the long memory; modernism supplies a sharp editorial act.

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
