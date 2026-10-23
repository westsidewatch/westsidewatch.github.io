# Westside Design OS — Editorial Manual

Status: **operational chapter of the single Westside Design OS**, not a parallel visual authority.  
Audience: Church, First Look, Journal, Olive Mountain, ONE, Dawn Library, Cinema, Search, tools, and Doré Design agents.  
Source of truth: [WESTSIDE-DESIGN-OS.md](WESTSIDE-DESIGN-OS.md) → `design-system/tokens/westside.tokens.json` → `static/css/westside-design-os.css` → approved `data-ws-scope` overrides.

**西望雜誌實作入口（2026-10-22）：** 直接閱讀 [§6F WESTSIDE WATCH Magazine Stylebook — Working Edition 01](#6f-westside-watch--西望雜誌視覺規範書--magazine-stylebook-working-edition-01-2026-10-22)。§6F 是規範與製作卡入口，§6E／§6D 是研究與技術證據庫；本手冊全程仍屬單一 Design OS，**未批准的藝術方案不因寫入手冊自動獲批**。

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


### 6D.5b Case study: The World of Interiors — square as a selective image register, not a global layout (2026-10-22)

**Decision status:** research evidence + Westside exploratory hypotheses ONLY. The user singled out the **square composition** as a promising, recognisable trait; this is **not** a selection of the current A/B/C/Cine-Folio/Square Folio overall art direction, not a ban on rectangles/full-bleed media, and not a binding rule that all covers or articles must be square. The current full-bleed film homepage, approved water/door/star choreography and original logo remain locked.

**Source / date / evidence type:** The World of Interiors official [2022 redesign conversation with Hamish Bowles and GTF co-founder Huw Morgan](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles), [2022 launch letter](https://www.worldofinteriors.com/story/welcome-new-website), [1982–2023 cover archive](https://www.worldofinteriors.com/story/covers-archive), current official [subscription cover-plus-spread examples](https://www.worldofinteriors.com/info/subscribe), and a current [digitally republished Roy Lichtenstein studio photo essay](https://www.worldofinteriors.com/story/roy-lichtenstein-new-york-manhattan-studio) (originally May 2004, republished April 2026). Textual claims from the official editor/design interview are first-party; descriptions of crops and ratios are **visual interpretations of the publicly displayed cover/spread illustrations**, not verified CSS measurements of every live viewport. Some **square web preview assets surround an upright printed cover**; a square promotional container does not prove the printed cover or source photograph is 1:1. Do not invent a native 1:1 ratio where it is not evidenced.

**Verified design intent rather than style imitation:** In 2022 Graphic Thought Facility (GTF), Ben Weaver and the editorial team looked at the magazine's early 1981–82 issues for type clarity and image prominence. Huw Morgan describes letting strong photography breathe (including an almost whole-spread photo), controlled typography permitted to break a rigid grid, and Contents with overscale page numbers counterpointing legible fine typography. The team explicitly distinguishes print from digital while seeking a coherent editorial *identity*, not identical page mock-ups. The new web edition both reinterprets print features and produces digital-first pieces. **Transfer editorial mechanisms, not GTF typeface, cover design or picture assets.**

**Five distinct visual units to study, without forcing a uniform box:**

| Unit | In the WoI evidence | Westside editorial experiment (hypothesis) | Failure to reject |
| --- | --- | --- | --- |
| Square **image plate** | A contained, visually stable photograph or preview can focus attention amid white/colour grounds; a square preview is not necessarily an original square photo | Test one 1:1 Doré-line / archival-detail plate, on a paper or ink field, with precise source/caption | Automatically cropping people, gates or architectural evidence to 1:1; forcing all images square |
| Square **editorial field** | A graphic image *within* a page can feel like a bounded focal object; this is a compositional extrapolation, **not** a claim that WoI always centers a square text card | Test a true 1:1 focal zone, with text outside as needed; allow center, offset and overlapping placements | Mistaking a single center box plus two decorative wings for a finished identity |
| Portrait/landscape **rectangle** | Printed cover images and spreads visibly preserve strongly varied proportions and photographic subjects | Use portrait for people/architecture, landscape for scenes/sequence, tall type when semantically warranted | Sacrificing photograph/story proportions to keep identical modules |
| **Full-bleed** image/film | Editorial interview expressly praises an almost whole-spread photograph with room to breathe; site film supplements print | Preserve the current homepage's full-bleed video; reserve immersive compositions for selected cover/feature moments | Downgrading the approved video homepage into a square picture in order to enforce a house style |
| **Article reading field** | Digital-first features and re-published archival photo essays retain text, photographer attribution and image captions | Calm longform web reading with evidence images in their appropriate aspect ratios; square can return as a detail/section pause | Compressing real 20k–50k prose into one 1:1 card, missing captions, or re-creating a printed page at phone width |

**Mechanisms of coherence across these image shapes:**
1. **Editorial hierarchy, not geometric repetition:** subject image is given a clear job (cover statement, archive witness, narrative spread, detailed illustration); square/rectangle/full-bleed are shifts in emphasis.
2. **Consistent lettering and information craft:** WoI's printed masthead/headline identity, page-number scale, captions and white margin are the recurring visual *voice*. Westside uses **its own** approved Bodoni Moda / Bodoni Moda SC, Chiron 900 primary / 200 supporting / 400 reading, official 西望 SVG, semantic ink/paper and source-credit grammar; no copied WoI font.
3. **Negative space as a picture frame:** some images are contained and surrounded by air; others intentionally break their boundaries or own most of a spread. Both can feel editorially coherent.
4. **Alternate tempo:** bounded square = concentrated pause; broad rectangular spread = narrative space; full-bleed = cinematic/monumental emphasis; then calm reading. This is a *Westside sequencing hypothesis*, not a claimed WoI fixed formula.
5. **Digital reinterpretation:** preserve provenance and editorial tone while allowing responsive ratios and page flows, not a virtual paper screenshot. Never upscale, non-uniformly stretch, repeat/tile or hide the source picture merely for CSS symmetry.

**Westside candidate to test, not yet approved:** A continuous **single** Doré/architectural image across the *entire* full-open P2 backing plane, with a selected square-shaped focal cover/engraving/typographic area (not necessarily dead-center). The visible left/right parts of the plane must be **one uninterrupted underlying image**, not independently painted side columns. A square *visual* focal point can coexist with larger rectangular editorial content and a full-bleed entry. Treat the backdrop as an actual subject image, not decorative wallpaper; crop via image subject/safe-zone study and source checks. A true accessible 4-movement/12-subject/3-interlude Contents, quoted scripture and longform link need real space **outside** a small square if necessary. Test against an image-led wide rectangle and full-bleed editorial variant; three sibling tests of *one* publication identity, **not** three accepted formats or a fourth live system. Keep article body a legible reading width.

**Proposed comparative acceptance, before any P2 promotion:** use the same source asset / exact editorial content and confirm 1:1 vs non-square candidates at 1648×928, 768×1024, 390×844, 200% zoom and reduced motion. Judge central visual dominance, coherent background across both sides, actual image detail/no subject cuts, optical relationship to giant Bodoni and Chiron 900/200, readable publication Contents/CTA, mobile editorial order and connection to the existing full-bleed home movie. Publish real screenshots before assigning an internal score. **Do not modify approved homepage, P2 motion or global Design OS tokens in this evidence-only pass.**


### 6D.5c The same story across three geometries — award-calibre experimental gate (2026-10-22)

**Implemented only in the existing isolated studio:** \`/experiments/p2-magazine-art-direction-studio.html?view=geometry&shape=square|wide|full\`. Three alternatives are **shape variables in one design experiment, not three accepted designs** and not acceptance of Folio. The already approved full-bleed homepage film and live P2 motion must remain unchanged. A/B/C remain navigable.

**One authored content/data set:** official masthead SVG; the existing \`/images/home-opening-engraving.jpg\` (never labelled archaeology photography); authentic \`The Gate / 城門口的人\` manuscript opening; complete canonical four-movement, twelve-desk, three-interlude Contents; Roman 13:12 English excerpt, and same links and source captions. The geometry experiment reuses the **same semantic DOM/copy** and only changes CSS media crop/proportion/layout. Square = 1:1 primary image with the **same continuous image underneath across left/right** (not unrelated panels); wide = 1.95:1 main plate; full = full-bleed picture. Reading/Contents below the hero are identical. Mobile keeps image → heading → original text → Contents in editorial order without three-column miniaturization.

**Explicit §6A award-calibre gate:** Awwwards external evaluation lens Design 40%, UX/UI 30%, Creativity 20%, Content 10%; Webby navigation/visual/content/functionality/interactivity/overall experience; FWA original digital interaction and technical narrative, with no invented official FWA weights. The **existing** Westside 10 × 0–2 internal rubric evaluates meaning, subject, compositional distinction, typography, two-ink discipline, hierarchy, interaction, mobile, accessibility and editability. **18/20 or more, no zeros and no unresolved block** plus real accessibility/performance/editorial review is an internal promotion aspiration, never an award forecast. A successful build is not visual approval.

**Visual evidence required before choosing square:** deployed screenshots at 1648×928, 768×1024, 390×844 and 200% zoom for all shapes; same source bytes/real text, source subject-safe crop, index completeness, Bodoni 400 / genuine Chiron 900/200/400, reader contrast, one background image across both square-side fields, focus/toggle accessibility, reduced motion, geometry sizes and initial/return controls. Compare thumbnails and *reader task*, not styling complexity. Preliminary code implementation is **NOT VISUALLY VERIFIED / DO NOT MERGE** until actual screenshots and review. No shape promoted to a global Design OS token.


### 6D.5d The failed wide-image screenshot and the first art-direction correction (2026-10-22)

**Actual user screenshot, not a guessed DOM rendering:** 2048×1152 pixel captured browser image, selected **wide 1.95:1**. The experiment was visibly contained in a comparatively narrow central canvas (roughly 52% of screenshot width), with oversized empty grey side gutters. Both an outer tinted engraving background and inner engraving plate repeated the identical pictorial subject; giant white THE GATE. crossed very busy figure detail without a meaningful text-safe region; lower Contents became visually miniature against the headline, so the contrast read as demo-hero vs dashboard rather than a coherent high-end publication. This is **a rejected snapshot**, not acceptable 18/20 evidence. Do not mislabel it the square variant.

**One coherent correction, no new OS:** The existing geometry studio now uses a **single actual image element** \`/images/home-opening-engraving.jpg\` in every shape; no duplicated image wallpaper or image shadow. Square (1:1) is the primary framed *witness*, offset against Bodoni Roman 400 with its own paper/ink reading field. Landscape uses one wide media plate and brings the grand typographic headline **below**, rather than across its busiest figures. Full-bleed alone allows type over one underlying image with a contrast scrim. Wide and full display a restrained **1:1 issue/dossier folio marked 03** as a recurring navigational square, not a second picture or an instruction to crop all photographs. The original artwork itself is not falsely described as archaeological evidence. The geometry-only workspace now expands to the available viewport; prior A/B/C proof layouts are untouched. The first Chinese display sentence of the real manuscript takes over the summary instead of an invented English standfirst, with no repeated first sentence in the paragraph. Provenance is visible outside the image, not as tiny white text over dark grain.

**Still critical:** A global 1:1 rule is expressly rejected. A square must be chosen when it concentrates a subject or gives the reader a useful edition/dossier frame. Landscape and full-bleed remain equal, available editorial tools. The small numbered square must be removed if visually ornamental or distracting when actual screenshots are compared. Do not solve a poor crop with background tiling, a second image layer, aggressive sepia, distorted type or ever-more decoration.

**Evidence/rejection gate:** Check this same real manuscript and source at 1648×928, 768×1024, 390×844, 200% zoom, keyboard and motion reduction against the user's previous screenshot. Do not call the result award-quality without revised deployed screenshots. The existing §6A rating still requires ≥18/20, no zero/block, and independent content, navigation and performance evidence; screenshots and published CI are both necessary. Original full-bleed homepage film, live P2 scroll geometry, church water/doors, 12 portraits and editorial content remain unchanged. **NOT APPROVED; PR UNMERGED.**

### 6D.6 Required next workflow — selection before implementation

1. **Real reference montage:** create a comparative source board with at least 12 clear interior-spread images and 6 functioning digital editorial pages; log provenance/date, page type, device, negative examples. No direct copying of licensed images into Westside assets.
2. **Freeze publication editorial content:** use the actual `docs/projects/watch-city-vol00/EDITORIAL_MAP.md` 4–4–2–2 issue map and three interludes, plus a real article excerpt (not invented titles) and authorized video/engraving sources. Compare use of portraits/stills against safe crops and copyright.
3. **Make 3 materially distinct art-direction prototype spreads** A/B/C above (real content), one 87–90% held screen and one 100% screen **per candidate**, plus an article opener. Static appearance is reviewed before running any animation.
4. **Editorial jury / contrast:** compare against the supplied Real Review-like multi-column, The Cut opener, print longform and It's Nice That image triptych screenshots. Score identity, novel classical-modern synthesis, focal direction, serif scale, Chinese 900/200 hierarchy, archival authenticity, useful negative space, index/reading handoff, responsiveness and motion as narrative.
5. **Choose one** and integrate it into the existing P2 proof. Then adjust only justified scoped Design OS sizes, position rules and assets; do not accumulate independent alternative live systems or 100+ micro-commits.
6. **Test a real article as part of the same design package**, with 390/768/1648px and 200% zoom; verify genuine fonts, actual text, longform accessibility, video fallback, reduced-motion and generated PDF/print only where applicable. P2 and print must be one editorial identity, not a screenshot of each other.
7. **Sign-off gate:** record actual browser screenshots, exact branch/deployment, checks and editorial choice in `P2-MAGAZINE-ART-DIRECTION-REVIEW-1352.md`. Only after genuine improvement should the candidate become normative Design OS grammar. Until then **STYLE EXPLORATION / NOT APPROVED / DO NOT MERGE**.

**Research-derived maxim:** The magazine is recognized not by three columns, old paper, or giant type in isolation, but by **editorial sequencing and consistent authorship of visual decisions**: a distinctive opening, factual imagery, readable text, meaningful pauses and surprising scale shifts. Classicism supplies the long memory; modernism supplies a sharp editorial act.


## 6E. Magazine design-book study → Westside Watch complete editorial specification handbook (R1, 2026-10-22)

**This chapter is the PRIMARY deliverable of the magazine design project.** It is part of the **existing single Westside Design OS Editorial Manual** and must evolve into its fully detailed, reference-backed production book. It does not establish a parallel brand book, a second type scale, another CSS system, another CI, or a style preference before art-direction sign-off. **Do not build isolated page ornament before defining its editorial job and publication context.**

### 6E.0 The crucial shift: from visual inspiration to a reproducible design book

A capable magazine art director must be able to answer, **for every page**:

1. **What is the content / reader's task?** What does the reader seek, learn, compare, navigate, or remember?
2. **What is the proposition?** One subject-specific idea and one visual narrative—not “old illustration plus big Bodoni”.
3. **Why this image?** Source, rights, subject, viewing distance, cropping and factual role.
4. **Why this hierarchy?** Identify identity, main story, deck, display, body, caption, folio, navigation and sources.
5. **How is the layout made?** Coordinates, grid, reading measure, image ratios, live type, whitespace and exceptions.
6. **How does it move?** The answer may be **it does not**. Motion must clarify a narrative transition, state or navigation.
7. **How is it built and edited?** Semantic HTML, existing OS tokens, scoped owner CSS, authoring and responsive flow.
8. **How is it judged?** Actual 1648 / 768 / 390px and 200%-zoom reader evidence, crop and text testing, no unresolved block, §6A art-direction sign-off.

**A finished specification is not a screenshot:** it contains a decision rule, permission/exception, measurable implementation guidance, real-data sample, regression evidence and responsible owning file. The reference/precedent gives *reasoning*; Westside produces its own *rule*; only tested rules graduate to normative status.

**Status key used in this book:** **[BASE]** already approved/reused OS authority; **[METHOD]** immediately applicable decision/QA procedure that doesn't choose a style; **[TRIAL]** numeric range or composition hypothesis for local tests only; **[OPEN]** not resolved, requires actual image/content research and visual sign-off; **[BLOCK]** cannot be promoted until resolved. Never silently reclassify a [TRIAL] as a global token.

### 6E.1 The researched book shelf: what has actually been verified

This is **publisher/author catalogue and accessible chapter-index research**, **not** a claim that the entire copyrighted books have been acquired or read cover-to-cover. We can apply grounded mechanisms and examples; deeper chapter-specific conclusions require source passages, permitted samples or actual study pages.

| Ref | Book / authority | Verified evidence | Extracted method, NOT replicated styling | Westside implementation question |
| --- | --- | --- | --- | --- |
| B01 | Cath Caldwell, *Editorial Design: Digital and Print*, 3rd ed., Laurence King, 2024 ([publisher](https://us.laurenceking.com/products/editorial-design-third-edition)) | [Publisher] revised case studies and exercises; independent publishing, print and digital integration | Treat issue identity, photography, text and production as one brand-editing problem | Can a reader recognize Westside without being shown its logo? |
| B02 | Sue Apfelbaum / Juliette Cezzar, *Designing the Editorial Experience*, Rockport, 2014 ([contents](https://www.oreilly.com/library/view/designing-the-editorial/9781592538959/)) | [Accessible contents] Reader, time, identity, anatomy, typography, layout, prototype, production, cases | Design the **whole reading system**, not a heroic opening alone | What exactly happens from cover → Contents → article → end → next? |
| B03 | Timothy Samara, *Making and Breaking the Grid*, 3rd ed., Rockport, 2023 ([publisher](https://www.quarto.com/books/9780760381939/Making-and-Breaking-the-Grid-Third-Edition)) | [Publisher] column/compound/modular grids and deliberate departures | Establish a working grid **before** making one purposeful violation | Which image/text edge, axis or hierarchy earns a break? |
| B04 | Josef Müller-Brockmann, *Grid Systems in Graphic Design* ([publisher/catalog](https://www.typotheque.com/books/grid-systems-in-graphic-design)) | [Publisher/retailer] grid construction as a practical organisational tool | Use tracks, measure and shared alignment as stable *infrastructure* | What holds together square, wide, full-bleed and longform? |
| B05 | Richard Rutter, *Web Typography* ([author TOC](https://book.webtypography.net/)) | [Author] chapters on paragraph measure, leading, tracking, numerals, hierarchy, responsive type and fonts | Translate print craft into **rendered** CSS and genuine font-face checks | What survives on 390px and 200% zoom without faking printed paper? |
| B06 | Ellen Lupton, *Thinking with Type*, 3rd ed. ([author](https://ellenlupton.com/Thinking-with-Type)) | [Author/publisher description] spacing, hierarchy, grids, alignment, Gestalt | Use contrasting scales and proximity to explain relationships | Are large English titles a deliberate semantic act or visual noise? |
| B07 | Jeremy Leslie, *The Modern Magazine*, Laurence King, 2013 ([magCulture](https://magculture.com/collections/newest/products/the-modern-magazine)) | [Publisher/studio catalogue] 750 captioned examples, essays including design × content and print × digital | A magazine identity can remain recognizable while channels and image shapes vary | Does our editorial identity survive format shifts? |
| B08 | Graphic Thought Facility / *The World of Interiors* redesign ([first-party interview](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles)) | [Direct practitioner account] 1981–82 issue archive, restrained graphic tools, clarity, image prominence, Contents and digital continuity | Conserve useful heritage, reinterpret narrative **rather than cloning printed pages** | Does an occasional square image have a purpose, without suppressing landscape/full-bleed? |
| B09 | W3C *Requirements for Chinese Text Layout* ([CLREQ](https://www.w3.org/TR/clreq/)) | [Open living technical standard] CJK spacing and punctuation/line-break requirements | Chinese typesetting has its own rules, not translated English line wrapping | Are punctuation, 讀者/引文/經文 and mixed-script lines genuinely correct? |
| B10 | W3C WCAG 2.2 ([normative criteria](https://www.w3.org/TR/WCAG22/)) | [Open standard] text resize, reflow, contrast, focus and reading requirements | Use independent measurable accessibility floors; not a brand preference | Can a reader enlarge the page and operate Contents/CTA by keyboard? |
| B11 | MDN *text-wrap* ([reference](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/text-wrap)) | [Open implementation doc] balanced headlines, long text, support variability | Treat balancing as progressive enhancement with tested fallback | Does a two-line Bodoni headline remain credible at each width? |

**Research provenance rule:** each future book note must list precise edition, author, publisher/ISBN if available, page/chapter actually accessed, evidence type (publisher / accessible sample / author / third-party review / own observed page), mechanism learned, translation and explicit failure mode. Copyrighted page spreads are **references**, not assets to reproduce in the site.

### 6E.2 How to make a style decision — eight fields in a mandatory art-direction brief [METHOD]

Record for every cover, category opener, index, illustrated story and longform article:

| Field | Mandatory question | Required deliverable |
| --- | --- | --- |
| SUBJECT | What real chapter/article/event does it illustrate? | Exact source content ID, story proposition and provenance |
| READER | Scan / select / watch / read / compare / study? | First action, second action and reading continuation |
| IMAGE | Evidence / narrative / portrait / cinematic / ornament? | Primary image ID, rights status, meaningful subject-safe region |
| FRAME | Square / portrait / wide / full-bleed / none? Why? | Composition sketch with 1:1 and non-square rejection reasons |
| LETTER | What is English doing that Chinese is not, and vice versa? | Exact title text; English and Chinese sizes/roles, alignment and line cuts |
| FIELD | Why this paper, line, background and occupied/empty region? | Defined anchoring edges, measure, breakpoints and contrast |
| TRANSITION | What information does the transition communicate? | Start/end/return/interruption/reduced-motion states, or “none” |
| AFTER | What is the reader's next meaningful action? | Real Contents, reading, references, previous/next, end mark only if justified |

Reject vague briefs such as “Italian magazine vibe” or “more ancient” without a subject, typographic hierarchy, action or source. Aesthetic descriptions are never sufficient instructions for implementation.

### 6E.3 Master-page anatomy — a living editorial **language**, not one immutable template [METHOD]

**Required publication roles**, not required visual blocks: publication masthead; issue/series identity; article/section identity; source media or its absence; lead statement; author/date/source metadata; Contents/route; article body; notes/captions/credits; references; next reading path; article end. The **same role can appear in a different relative position** depending on section. Never duplicate text/images purely to fill a three-column display.

| Editorial surface | Primary object | Supporting roles | Special constraint |
| --- | --- | --- | --- |
| Issue First Look | One artwork/moving scene + issue claim | Official masthead, controlled CTA, real edition path | Original homepage full-bleed movie is **LOCKED**; typography proposals separate and deferred |
| Magazine opening after P2 doors | One authentic editorial encounter | Four movements, 12 desks, 3 interludes, meaningful reading path | Do not reinstate independent coloured triptych; preserve existing P2 choreography |
| Section opener | Section proposition + dominant image/type | Series, index, navigation | A visually different section is not another design system |
| Table of Contents | Find and choose, quickly | Movement numbers, story title, one optional teaser | Editorial typography must improve navigation, not conceal it |
| Photo/engraving feature | Subject image with attributable meaning | Label, source, caption, next image | Cropping must preserve historical or compositional evidence |
| Longform (20k–50k characters) | Readable continuous paragraphs | Chapter headings, figure/caption, scripture, footnotes, index | No obligatory three columns, forced magazine pagination or scrolling hijack |
| Archival/map page | Legible object at useful scale | Zoom/text transcription, time, location, citation | “Old map” is documented evidence, not a decorative pattern |
| Closing | Confident conclusion + next route | Credits, references, related article; possible inherited end mark | End mark must use proven original asset; do not recreate by guesswork |

The old three equal panels failed because they made **zones** prior to making **reader tasks**. A real magazine may use columns, a central square, asymmetry or no columns whenever the hierarchy requires them.

### 6E.4 Geometry: from story content to grid and bounded exceptions [METHOD + TRIAL]

**Construct in this order**: (1) content hierarchy and the reader's task → (2) **choose a continuous digital spread as the wide-screen composition field where editorially justified** → (3) available inline size, safe area and imaginary compositional axes (not binding gutters) → (4) main content measure and independent image/text/object layers → (5) deliberate cross-axis shape placement and supporting tracks → (6) image/subject crop *only when a photographic frame is involved* → (7) optical alignment, layering and tested exceptions. See **§6E.29–31: Digital Spread Composition** for the governing full-canvas grammar. The R3/R4 crop forensics are a supporting image-specialist tool, **NOT a substitute for spread-level design**. A 12-track CSS grid is a convenient *layout tool*, **not** an obligation to show twelve identical cards. Geometry can be asymmetrical when actual title/photographic content motivates it.

**Starting study envelope ONLY [TRIAL]**; none of these values are approved site tokens or a promise of ideal design:

| Parameter | Desktop initial candidate | Tablet initial candidate | Phone initial candidate | Rejection test |
| --- | --- | --- | --- | --- |
| Outer space / safe inset | 3–7vw | 4–6vw | 16–24px | Text or crop collides with viewport edge; optical imbalance |
| Reader text measure | 30–40 **CJK ideographs** on typical body line, test against actual font | 24–34 | 17–28 | Breathing / scrolling effort / repeated eye loss; **actual rendered count matters** |
| Body font size | Consume existing OS reading token, not a hardcoded new scale | Same semantic role | Same semantic role | Chiron loaded? comfortable paragraph at actual device/zoom? |
| Editorial track | 6/8/12 as helpful, unequal spans allowed | 2–6 as helpful | **Single narrative flow** | Semantics force mobile into tiny side-by-side print facsimile |
| Square plate | True 1:1 image when the image needs concentrated attention | preserve purposeful object fit | preserve picture's readable subject | Crops faces/architecture/subject; becomes every story's template |
| Wide plate | Source-sensitive landscape, e.g. exploratory 1.5–2.2:1 | adapt based on image | full-width field if useful | Drops essential scene relationship at crop |
| Full-bleed | Image or approved video owns a deliberate chapter moment | bounded when needed | reading navigation and caption remain discoverable | Just a stretched image, no visual subject or safe text |
| Narrative whitespace | Express separation/anticipation/reading rhythm | shorter pauses | no empty “scroll to content” canyon | Cannot explain what the blank space accomplishes |

**No numeric range above becomes production authority without** a named example, browser screenshot, optical measurements and explicit editorial sign-off. Do not equate a desktop width divided by font size with a Chinese character count: verify actual glyphs in the real paragraph and line breaks.

**Alignment protocol:** start from the baseline edges of headline and prose, then try a controlled collision, inset, or offset. If headline blocks faces or disappears behind a plate, declare **BLOCK** and reject. Leaving large English letters clipped is allowed only with preserved word comprehension in each reading state; it is not “award creativity” by default.

### 6E.5 Typographic roles — exact **authority**, not a new scale [BASE + METHOD]

**[BASE]** Canonical OS JSON contains the 12 editorial roles; CSS is generated/loaded through the current Design OS. Use **Bodoni Moda Roman/Italic 400**, **Bodoni Moda SC genuine small caps**, **Chiron Hei HK WS 900 primary Chinese**, **Chiron 200 supporting Chinese editorial display**, **Chiron 400 sustained reading**; preserve real body font loading. The older 600 role is migration history, not a design permission to use 600 indiscriminately. Never horizontally/vertically stretch, skew or synthesize styles.

**Pairing policy**:
- English and Chinese are separate roles, not a mandatory duplicate literal translation. The English can lead as a monumental image-form, while Chinese supplies the bold semantic subject; either remains meaningful in DOM.
- In a primary title encounter, English is often visually larger and finer; Chinese 900 is weight counterpoint. The ratio is *chosen per composition*, not a new sitewide 1.7:1 law.
- Chinese 200 needs size and line-height to preserve readability. **200 must never be used** for 11px metadata, fine legal copy, captions or essential controls.
- Bodoni italic is for scripture quotation, epigraph and selected English phrase—not all English, dates or tables.
- Metadata in actual Bodoni SC is typographically distinct from body and control labels; do not make all navigation uppercase.
- If an article title is canonically Chinese, keep a meaningful Chinese H1. Decorative outlined English may be aria-hidden only when the real title remains intact.
- SVG mastheads remain **original assets**. Never retype the logo as a new Bodoni heading to “normalize” it.
- At 200% zoom, allow real reflow; do not shrink or squish the type to preserve a magazine cover illusion.

**Optical review**: inspect cap height vs Chiron ideograph field, punctuation proximity, title line termination, italic passage emphasis, title/subject relationship, and a 3-word vs 18-character real headline at desktop/phone. Do not approve by computed font-size alone; confirm font has loaded and glyph instance is actual.

### 6E.6 Image direction — not a decorative wallpaper service [METHOD]

**Image intake manifest** for every meaningful hero or article plate:

| Field | Value to record |
| --- | --- |
| Stable source ID | Repo asset path + original file/history or authorised external asset + author |
| Authentic subject | What is visibly shown; whether location/time depiction is historical illustration, map, photograph or reconstruction |
| Provenance / rights | Source, attribution, license/permission, reuse condition; UNKNOWN means **BLOCK for publication**, not license guessed |
| Focal bounds | Relative 0–1 rectangle of narrative subject and **subject exclusion zones** for live titles; manually reviewed |
| Output frames | Whether true native square / landscape / portrait; intended crop(s); never claim a digital preview square proves original shape |
| Color/print role | Ink/paper contrast, monochrome intent, engraving line density, optional tint; avoid black+gold pairing banned by existing Design OS |
| Text relation | Text-safe zone; proof title against real rendered source. If no safe zone exists, move text OUTSIDE image |
| Responsive alternate | Test separate art-directed crop **of the same source** when justified, not random CSS background-position |
| Accessibility | Informative alt, decorative empty alt, contextual figure caption and source; avoid both duplicated verbose descriptions and absent evidence |

**One source image may recur across pages** for an archival motif only when genuinely telling a connected story. **Repeating the same picture as wallpaper behind itself is a defect**, not depth. Avoid faux grain over all paragraphs, uncredited art and forced hero aspect ratio where a subject is cut.

**Square rule [TRIAL]:** Use a square to concentrate a historical plate, detail, file or moment; other images remain portrait, wide, panoramic or full-bleed according to subject. A square “03” register becomes meaningful when it actually navigates to Contents; square stamps repeated on every panel are empty ornament. **Never adopt the previously rejected Folio overall direction merely because one square is effective**.

**Doré translation question:** Does line density provide an editorial boundary, a depth plane, a subject-safe silhouette or a readable narrative transition? If merely “turn photo gray + apply sepia + put huge text over it,” **reject**. Never claim illustration is an archaeological photograph.

### 6E.7 Publication rhythm — opening, index, feature, reading, exit [METHOD]

Define the issue as a **sequence of reader intensity**, not one uniform web card template:

| Register | Visual intensity | Reader task | What must be visible |
| --- | --- | --- | --- |
| A / Front matter | High impact permitted | Enter issue; identify its thesis | Authentic masthead, accurate issue text, real entry |
| B / Contents | Controlled, scan-first | Find a movement and story | Four movements, 12 desks, 3 interludes, complete destination links |
| C / Chapter opener | One dramatic accent | Understand a single proposition | One useful headline, image/source, author |
| D / Essay | Calm repeated rhythm | Read thousands of Chinese characters | Comfortable text measure, real figure captions and notes |
| E / Interlude | Deliberate pause | View/listen, then rejoin reading | Film fallback/controls, no autoplay obstruction or dead end |
| F / Back matter | Quiet precision | Verify and continue | Sources, credits, previous/next, genuinely placed terminal mark if approved |

**No “cover only” release:** a proposed cover cannot graduate without at least one real article opener, article middle, full-length reading continuation and ending in the same identity.

**Contents can be visually bold without sacrificing navigation:** Try large movement numerals, asymmetrical white space and type counterpoint; maintain programmatic lists, honest headings and meaningful destinations. Do not fit 12 complex entries into a tiny square or freeze two text columns on a 390px phone.

### 6E.8 Chinese and bilingual composition detail [METHOD + open typography QA]

Ground this chapter in W3C CLREQ (Chinese punctuation and line rules), the actual Chiron font coverage, Bodoni companion metrics and semantic language spans. **Not every English typographic habit transfers to Chinese.**

- Preserve real canonical character forms and accurate scripture references; do not edit a source manuscript to force a nicer last line.
- Keep opening/closing punctuation and quotation marks sensible at line starts and ends; verify mixed-run CJK/Latin wraps, number/book-name cohesion and the real renderer's line breaking. CSS does not guarantee full professional CJK kinsoku behavior in every engine.
- Avoid arbitrary positive tracking in dense Chinese reading. Display-grade spacing is opt-in; the CJK paragraph defaults to readable rhythm rather than “luxury typography” tracking.
- Do not force English hyphenation rules onto Chinese. Check thin spaces, citations, italics, question marks and punctuation beside a genuine Bodoni italic run.
- Scripture: Chinese wording in Chiron 400, Latin/numeric references in authentic Bodoni Italic per the existing typography authority; references stay semantically bound to the correct scripture.
- For long articles, every chapter H2/H3 earns a valid hierarchy; bold 900 applies to actual primary title, not every heading. Chinese supporting display 200 is large enough to read, never a pseudo-hairline at small pixel size.
- **Critical test strings:** 城門口的人 / 守望，一座光明的城 / The Gate / The night is far spent... / 約翰福音 3:16–17 / 一萬年的建城禮 / longest real Contents item. Verify font, punctuation, line break and no overlap at 390px and 200% zoom.

### 6E.9 Longform production grammar: from a 20k–50k-character manuscript [METHOD]

**Schema for a publishable article**, sourced from the existing canonical manuscript, never fabricated decorative prose:

1. Article ID, canonical H1, edition, byline, date, revision/provenance.
2. Deck/standfirst **only if genuinely present or editorially approved**; distinguish prose excerpt from copywriting.
3. Section break hierarchy (H2/H3) and a usable optional local Contents index for long articles.
4. True paragraphs with stable line-height, measure and natural word/character wrapping; no fixed-height text boxes.
5. Meaningful figures as figure + img + figcaption; the image's source and illustration vs factual role are explicit.
6. Blockquote with precise attribution and distinct from scripture reference styling.
7. Notes/references/endnotes with backlinks and accessible anchors, plus names/links in authentic order.
8. Article end, author/source credits, and working previous/next reading route.
9. Loading/performance: image dimensions, progressive assets, media fallback; avoid layout shift and font flash where possible.
10. Print/export is a **separate output mode from the same canonical content**, not a two-page GIF or page-turning web gimmick.

**Representative scoped CSS sketch (example for one owning Journal article stylesheet, NOT a new OS file)**:

~~~css
/* Example only — bind this inside the existing [data-ws-scope="journal"] owner. */
[data-ws-scope="journal"] .ws-magazine-article__reading {
  max-inline-size: var(--ws-type-measure-reading);
  margin-inline: auto;
  padding-inline: clamp(1rem, 4vw, 3rem);
  font-family: var(--ws-type-reading-zh);
  font-size: var(--ws-type-scale-reading);
  line-height: var(--ws-type-leading-reading);
  overflow-wrap: break-word;
}
[data-ws-scope="journal"] .ws-magazine-article__reading p {
  margin-block: 0 1.2em;
}
[data-ws-scope="journal"] .ws-magazine-article__reading figure {
  margin-block: 2.5em;
  margin-inline: 0;
}
[data-ws-scope="journal"] .ws-magazine-article__reading img {
  display: block;
  max-inline-size: 100%;
  block-size: auto;
}
[data-ws-scope="journal"] .ws-magazine-article__reading :is(h2, h3) {
  scroll-margin-block-start: 5rem;
}
@media (max-width: 48rem) {
  [data-ws-scope="journal"] .ws-magazine-article__reading {
    padding-inline: 1.125rem;
  }
}
~~~

The code above is a **demonstration of consumption of existing roles**. It is not applied to production and needs contrast, actual mobile, source CSS selector existence and computed-font checks before implementation. No global new CSS or shadow OS.

### 6E.10 A real art-direction exercise: VOL.00 / 城門口的人 [TRIAL]

**Fixed authentic inputs:** The Gate / 城門口的人; canonical existing manuscript; the actual existing engraving image with honest provenance; current official WESTSIDE WATCH masthead SVG; four movements and twelve desks. The primary story is a **threshold**—the ancient gate as a physical, civic and scriptural encounter, not a square stamp.

**Three different editorial questions, NOT three mandatory templates:**

1. **Archival square / looking inside:** Does 1:1 isolate a meaningful threshold subject (arched entrance/human encounter) **without** cutting people? Type has its own safe field; real city/subject history supports the frame. If it looks like a gallery image alongside giant type and nothing else, reject it.
2. **Wide evidentiary scene / seeing the street:** Does the landscape plate communicate a crowd/approach/route better than a square? Let the image own the width, and find a distinct type axis away from densely inked crowds. The title must remain legible.
3. **Full-bleed passage / crossing:** Does an immersive scene convey entrance/scale, with accessible controls and clear scroll continuation? One image, one intentional text-safe region. The published homepage full-bleed film is protected; this test **does not modify that homepage**.

For each, deliver a **direction card**: 1 sentence idea, source-asset sheet, thumbnail silhouette, 1648/768/390 rough geometry, one real article middle view, one end state, text/image collision boundaries, 200%-zoom exception handling and exact reject reason. If none wins, advance research—not ornament.

### 6E.11 Motion / digital page behavior, with static parity [METHOD]

A literary-magazine animation should alter **reader understanding**: ocean → church opening → edition publication, source engraving reveal, source figure annotation, Contents progression. Keep to one coherent temporal argument; **all content must remain readable as a fully static page** with reduced motion. Avoid scroll locks, video backgrounds behind dense articles, gratuitous easing or forced chapter transitions.

**Motion specification tuple** to write for any transition: triggering reader action; source state; destination state; element transformations; meaning; latency/performance acceptance; keyboard and focus route; back/reverse path; interrupted mid-scroll behavior; reduced-motion/static fallback; owning file and regression screenshots. Never build a bespoke global motion library for a single page.

### 6E.12 Editorial color and surface discipline [BASE + METHOD]

**[BASE]** All colors come from existing Design OS tokens and semantic branches. A “warm paper” may be used only to express surface depth; it is not automatic texture wallpaper. “Classical” ≠ sepia; “modern” ≠ a dark UI.

- Establish one dominant paper/surface role and no more than two major ink plates per view **as a creative starting discipline**, while allowing functional diagrams/illustrations and section colors where meaning demands.
- Reserve section palettes for section identity; do not display all seven realm colors in every magazine image or secretly introduce an eighth style.
- Source engravings can stay natural monochrome; any tint must preserve line meaning and contrast; source work stays unchanged.
- Do not turn a small square 03 into black+gold luxury cliché. Existing global black+gold prohibition remains in force.
- Captions and legal/source text must meet accessible contrast, not merely look subtle at one screenshot.
- Before new tokens, test whether current tokens and opacity/mix support the role; if this is purely editorial composition, put it in local owner CSS only after approval.

### 6E.13 The details most magazine “mood boards” fail to specify [METHOD]

These are **required questions in a full-details design book**; no invented pixel authority:

| Detail | Design rule | Proof |
| --- | --- | --- |
| Optical heading alignment | Align an actual glyph/cap edge to meaningful object/text axis, not CSS box alone | Before/after line overlay |
| Cover crop | Record original image rectangle, focal region and exclusion region for every responsive state | Annotated subject-safe desktop/phone captures |
| Standfirst | Declare whether true source text, edited deck or quotation, and keep it distinguishable | Editorial provenance check |
| Byline/author | Genuine name, role, date; no microscopic 200-weight metadata | Zoom and multi-line author test |
| Figure numbering | Canonical sequential figure IDs; alt/caption and source | Cross-reference between prose and figure |
| Folio and issue number | Orient reader and navigate; placement stays subordinate to primary story | Keyboard/focus and “where am I?” test |
| End mark / city-wall battlements | Historical original asset **must first be recovered** and authenticated; candidate for ending, not a global divider | Source asset audit, closing prototype after style decision |
| Line / rule weight | Meaningful relation or interval; don't outline everything | Simplified page without line comparison |
| Image/caption spacing | Closely associate caption with image; not adjacent story | Capture with long caption and unusual crop |
| Heading wrap | Preserve complete content; optical balance before forced break | 3/9/18-character Chinese + Latin title captures |
| Chapter anchors | Semantically named, stable and keyboard navigable | Keyboard jump and return |
| Pull quote | Only from real article, attributed; not fabricated marketing copy | Search source manuscript and editorial approval |
| Notes and references | Bi-directional accessible anchors and readable context | Navigate note → paragraph on phone |
| Pagination / depth | Browser article is a reading stream, not imitation printed folios | Mid-article screenshot and return |
| Read-more / next | Working destination and meaningful reader continuation | Link validation |
| Long loading / media | No invisible article, blank scroll canyon or large shift after load | Network/cache throttling and visual compare |
| Motion | Communicates change of state; no loss on interrupted/returned scroll | Begin/mid/end/reverse + reduced motion |

### 6E.14 Engineering and accessibility proof — measurable acceptance [BASE + METHOD]

Accessibility baseline: W3C WCAG 2.2 **1.4.3** ordinary text contrast ≥4.5:1 (large text ≥3:1); **1.4.4** text can resize to 200% without loss; **1.4.10** ordinary vertical content reflows at 320 CSS px without two-dimensional scrolling; **1.4.12** text spacing overrides do not clip content; **2.4.7** visible keyboard focus. These are technical standards, **not** overall proof of good art direction. Distinguish a 824px effective-width screenshot from actual browser 200% zoom.

**Mandatory visual review matrix** for an actual selected candidate:

| Test | Dimensions / state | Evaluate |
| --- | --- | --- |
| D1 | 1648×928 desktop, first screen | Publication identity, title word integrity, image subject, real CTA |
| D2 | 1648×928 mid article and end | Actual paragraph measure, source/captions, transitions and ending |
| T1 | 768×1024 tablet, entry + Contents | Scale shift, content order, no dead zones |
| M1 | 390×844 phone, entry + longform | Single reading route, image legibility, active navigation, no microcopy |
| M2 | 320 CSS px reflow | No 2D horizontal scrolling for normal article content |
| Z1 | Real 200% browser zoom | Full text and controls without collision, clipping, lost content |
| K1 | Keyboard-only sequence / visible focus | Logo, TOC, article, footnotes, return, no trap |
| R1 | Reduced motion and media failure | Same reading content and source access |
| A1 | Full text + source + alt/credits | No invented prose, wrong title, missing copyright or attribution |
| P1 | Cache / network / font fallback | No unreadable font, image jump or hidden content |
| C1 | Existing build/Core Contract/Design OS/preview | Green CI, but **cannot override a visual block** |

**QA artifact format:** one real versioned screenshot per state, name/commit/viewport/time, measured font and box bounds, reader-task success, contrasts, image crop diagnostics and block/important/polish severity. A screenshot without a named purpose is not a QA result.

### 6E.15 Honest self-review and release gate [METHOD]

The user-set goal remains **award-competitive quality** with self-critique and repeat iteration, guided by Awwwards Design 40 / UX 30 / Creativity 20 / Content 10, Webby full experience and FWA originality. No award result, nomination, official juror score or guarantee is implied.

- **Concept study:** 10 × 0–2 internal grammar scale from the existing project skill. Exploration minimum 15/20 only.
- **Candidate promotion:** internal aspiration **≥18/20, zero zeros, no unresolved BLOCK**, PLUS independent browser reader-path, motion, accessibility, performance, real content, evidence and art-director approval.
- **Reject even an attractive screenshot** if 03 index does not navigate, THE GATE loses letters, actual CJK prose wraps badly, the source image is unverifiable, a phone hides Contents, full-bleed does not truly span the viewport or the beautiful grid cannot serve a real article.
- **Do not sign off concept by CI** or assume the release is approved when one of three ratios passes. Reject without adding five ornamental variants; return to book method or source-image study as needed.
- **Frozen until selected:** original homepage film/full-bleed opening, known water-to-door-to-P2 motion and protected twelve-portrait assets.
- **Do not merge** the ongoing magazine research PR solely to save prose; the documentation can be reviewed in the branch while the visual concept remains unselected.

### 6E.16 How this chapter grows into the **complete** Westside magazine production book

**This first round is an operational draft, NOT a claim that a complete production book or final visual brand has been delivered.** The next source-work chapters, ordered by creative dependency rather than smallest cosmetic task:

| Priority | Future chapter | Source of data | Deliverable required for “done” |
| --- | --- | --- | --- |
| 1 | Editorial brand premise / signed artistic proposition | History/source art and real magazine reader mission | Brand thesis, three independent direction cards and one accepted silhouette with rejection evidence |
| 2 | Original Doré-image art direction | Licensed originals, engraving line/subject/lighting studies | Subject-safe maps, figure and crop conventions, image treatment decisions, asset provenance |
| 3 | Master grid and composition atlas | Real Contents, chapter, cover and feature data | Measured grids, exceptions, 1648/768/390 drawings with semantic hierarchy |
| 4 | Complete type manual for 12 semantic roles | Existing Design OS typography authority, actual browser fonts | Role-by-role specimens with exact font, optical balance, CJK breaking, prohibited examples, scoped code |
| 5 | Issue/section color and image-handling manual | Existing single-OS tokens, seven semantic realms | Functional palette usage and image-treatment/contact-sheet evidence |
| 6 | Complete longform and scholarly apparatus | Real manuscripts, images, scripture, citations, 20k–50k-character test | Full middle/end layout with figures, caption, notes, footnotes, references and next |
| 7 | Editorial motion and navigation grammar | P2 approved flow plus real reading tasks | Timelines/states/reduced-motion story, keyboard route, measurable performance |
| 8 | Cross-screen / print export grammar | Rendered phone/tablet/desktop/print from canonical source | Role-consistent format system without forcing print page simulation on web |
| 9 | Production handbook and reviewer checklist | Browser measurements, accepted prototypes, design decisions | Exact rule → owning CSS/JS/semantic DOM → screenshot regression → release acceptance |
| 10 | Living exception and archive protocol | Approved design reviews / rejected variants | Versioned examples, reasons, rollback and next editor instructions |

**The most urgent unresolved task is not an article end mark. It is to write and validate the brand's editorial premise and the Doré-art-to-modern-grid translation so that all details are decisions of one identifiable publication.** Only then may specific square-crop use rates, end marks or image proportions become normative.

**Source provenance index:** B01–B11 above; [§6D The World of Interiors](#6d5b-case-study-the-world-of-interiors--square-as-a-selective-image-register-not-a-global-layout-2026-10-22), [§6A award-level gate](#6a-award-calibre-release-objective--awwwards--webby-awards--fwa-2026-10-21), existing [Westside editorial type authority](WESTSIDE-EDITORIAL-TYPOGRAPHY.md) and [single Design OS](WESTSIDE-DESIGN-OS.md). Public links prove title, contents or guidance as marked; full copyrighted text not reproduced.

### 6E.17 Seventeen magazines studied — 16 eligible art-direction references + 1 rejected visual reference (R2, 2026-10-22)

**Editorial selection update (2026-10-22):** **Monocle / M09 = REJECTED for Westside aesthetic, composition and art-direction reference.** The user judged its layouts insufficiently contemporary for the magazine's intended classical × contemporary tension. Its archival interview can remain as **negative research history**, not a source of visual or typographic recommendations. Thus 17 have been researched but **only 16 remain candidates for positive comparison**; the 16 are not automatically approved either. Do not generate new Monocle-like high-density column blocks, colored index rails or info-first covers. A comprehensive production checklist may be developed **independently** of any rejected aesthetic reference.


**研究性質與證據邊界。** 本輪研究的是 17 本具古典／現代張力的實際雜誌，其官方編輯訪談、負責設計工作室、印廠、D&AD／ADC 作品記錄、公開內頁與視覺評論。**它們並不等於 17 本已取得的內部 brand guidelines PDF。** 大部分專有字體、InDesign 主版、精確點數和品牌手冊未公開；本章不假裝讀過私人規格。逐案列出 [E] 能被公開文獻證實的做法；[F] 編輯框架的分析歸納；[D] 影響風格的微細部位；[W] 供西望驗證的轉譯；[R] 不應模仿之處或資料空缺。書刊年代另列，避免把不同改版混合成同一現行制度。所有建議是 **[METHOD]／[TRIAL]**，不能直接更改全站 Token。

#### M01 — The World of Interiors · 2022
**來源：** [1](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles) · [2](https://www.worldofinteriors.com/story/welcome-new-website)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** GTF、Ben Weaver、Hamish Bowles 回查 1981–82 年舊刊：保留清晰的字體秩序與古典氣質。圖片能近乎佔滿跨頁，短新聞 Antennae 在受控版心內容許產品圖突破格線及文字繞排；目錄以巨大頁碼與精細可讀的字形成反差；數位版承接編輯身份但不模擬紙頁。
- **[F] 可重建的編輯框架：** 歷史身份→封面影像→動態密集短訊→寧靜影像專題→可掃讀目錄。固定的是清晰、內容可信與影像主導，不是永遠一種三欄網格。
- **[D] 真正決定風格的細節：** 主體安全區、巨大目錄數字、繞圖注釋、頁面密度切換、圖片周圍的負空間。
- **[W] 《西望》的可操作轉譯：** 《西望》四樂章以目錄數字對應真實文章；門／城／海洋刻線可擔任近滿版歷史見證；方圖只在局部主體需要聚焦時使用。
- **[R] 失效條件與未知數：** 不是復古紙紋＋Bodoni＋正方圖的固定模板；未知其現行自有字體、內頁精確點數和響應式 CSS。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M02 — The Paris Review · Winter 2021
**來源：** [1](https://www.pentagram.com/work/the-paris-review/story) · [2](https://www.dandad.org/work/d-ad-awards-archive/the-paris-review)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Pentagram/Matt Willey 與 Emily Stokes、Na Kim 從 1960–70 年代檔案找回文學性冷靜風格；封面 Founders Grotesk 刊名，重要藝術圖像獲得大面積展示，封面說明轉往書脊；縮小實物、採暖調紙張，易於單手閱讀。
- **[F] 可重建的編輯框架：** 封面只做識別與藝術主題；書脊承擔實體索引；內文延續像書的深讀節奏。印刷材料與資訊位置一起構成規則。
- **[D] 真正決定風格的細節：** 封面行文密度、藝術圖留白、期號／撰稿人書脊、書籍式紙張觸感及裝訂尺度。
- **[W] 《西望》的可操作轉譯：** 讓《西望》刊頁入口對標圖像與主題；數位將書脊功能轉成明確期號／篇目導航，不把小字貼在圖片的灰暗角落。
- **[R] 失效條件與未知數：** 不複製 Founders Grotesk、封面尺寸或紙張視效；原內部格線與精確尺寸未公開。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M03 — The New Yorker · 1925–2014 heritage / modern refresh
**來源：** [1](https://www.stuart-bertolotti-bailey.org/projects/writing/hardy-perennials) · [2](https://www.newyorker.com/video/watch/the-new-yorker-gets-refreshed) · [3](https://www.robertnewman.com/redesigning-the-new-yorker-an-interview-with-creative-director-wyatt-mitchell/)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Rea Irvin 刊名字、Eustace Tilley 和專欄持續形成識別；長文二／三欄依然清晰。創刊時編輯甚至會為『線條應該有何性格』反覆修訂；漫畫對話的斜體與引號，讓修辭節奏和視覺節奏合一。
- **[F] 可重建的編輯框架：** 刊名、專欄、正文、漫畫、圖說和欄間線不是裝飾組合，而是相互支援的出版語氣。
- **[D] 真正決定風格的細節：** 欄間規線形狀、內文行寬、標題字的歷史性、引號及斜體的語義角色、人物插畫。
- **[W] 《西望》的可操作轉譯：** 把經文引註、歷史引語、短行規線、原始城垛止字符當成語義元件研究；先完成全文結構，再定線條和尾碼的形狀。
- **[R] 失效條件與未知數：** 不臨摹 Irvin 字體；不把兩欄印刷正文原樣搬到手機，亦不誤稱已拿到其排版樣式表。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M04 — The Gentlewoman · issue 12 2015 / 2009–21 Ditting era
**來源：** [1](https://www.ssense.com/en-sa/editorial/culture/the-art-of-formal-friction-with-creative-director-veronica-ditting) · [2](https://magculture.com/blogs/journal/details-the-gentlewoman-12) · [3](https://www.dandad.org/work/d-ad-awards-archive/the-gentlewoman)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Veronica Ditting 認為設計是 edited 而非空洞 minimal；封面強人物攝影，頁內常見 Futura、精確用紙；全頁 Part One/Two 節頁建立章節；粗顆粒半色調用於節頁和每篇尾部 References，與正文光滑圖像形成材質節奏。
- **[F] 可重建的編輯框架：** 肖像封面→清晰的 Part 分節→不同密度人物敘事→References 結尾呼應；跨頁編排 flatplanning 也是編輯設計。
- **[D] 真正決定風格的細節：** 分節全頁的資訊量、Futura 字體、半色調密度位置、References 對應、圖片紙張反差。
- **[W] 《西望》的可操作轉譯：** 以四樂章建立版面節奏；每篇引文／史料結尾與開場可有共享規則，不要隨機在文章底塞裝飾線。
- **[R] 失效條件與未知數：** 不要把半色調變全站紋理或照搬 Futura；原專有版心精準尺寸尚未驗證。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M05 — Fantastic Man · 2005–2015/award 2008
**來源：** [1](https://magculture.com/blogs/journal/fantastic-man-22) · [2](https://www.dandad.org/work/d-ad-awards-archive/fantastic-man)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Jop van Bennekom 的書卷式人物長訪談，清晰而有幽默感；其字體與紙種的實物性獲 D&AD 雜誌設計獎肯定。刊名由最早 Times Roman 疊置居中逐步演化，不是每期全盤換風格。
- **[F] 可重建的編輯框架：** 固定聰明、克制、細緻的編輯語氣，容許一個視覺要素逐期遷移；訪談深度比耀眼造型重要。
- **[D] 真正決定風格的細節：** 刊名字的位置微調、頁面分段、不同紙品功能、長訪談語氣與內文易讀程度。
- **[W] 《西望》的可操作轉譯：** 建立『恆定語法／可變構圖』兩張表：OS 字族和真實資料固定，圖片比例、字與圖相接方式可隨主題改變。
- **[R] 失效條件與未知數：** 不強制全刊同一 Square Folio，也不引用未公開內部模板。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M06 — Apartamento · Omar Sosa interview 2012
**來源：** [1](https://www.marklives.com/2012/02/omar-sosa-on-the-apartamento-design-style/) · [2](https://www.oreilly.com/library/view/designing-the-editorial/9781592538959/chapter-68.html)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Omar Sosa 明確說設計從拿到的文章、人物、照片、印材出發，主要靠字體、照片與出版物物質條件；攝影、編輯、印刷技能要協同，不願被稱為單純極簡。
- **[F] 可重建的編輯框架：** 內容來源與人物生活先於網格，照片提供視覺規則；每個故事可選最合適長方／正方／滿版，不是先決定通用卡片。
- **[D] 真正決定風格的細節：** 真實室內和人物的影像誠實、編輯合作流程、圖與文的主體關係、印材限制。
- **[W] 《西望》的可操作轉譯：** 一幅城牆／人群原畫的主體區、留白、安全線先畫出，再決定文字坐標；禁止為了漂亮把歷史證據隨意裁掉。
- **[R] 失效條件與未知數：** 沒有已核證的專用欄數／字號，不用猜出一套 Apartamento 設計 Token。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M07 — Cabana · official publisher/printing case
**來源：** [1](https://cabanamagazine.com/pages/about-us) · [2](https://navapress.com/en-us/portfolio/cabana-magazine)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 每期不同布料封面，特別裝幀、紡織／裝飾邊框、專門紙材與不同內頁圖文處理，為真實設計物件；Nava Press 描述紙張、布封和裝訂研究。印刷半年刊與每日線上內容節奏不同。
- **[F] 可重建的編輯框架：** 有節制的豐盛：裝飾的歷史材質、工藝來源與頁面角色相連，並非全篇鋪花紋。
- **[D] 真正決定風格的細節：** 封布的來源、圖案邊緣、內圖邊框與材料關係、圖像情緒及紙張製作。
- **[W] 《西望》的可操作轉譯：** 採用真實刻線、蒲草紙、城牆材料作圖文範圍提示；原圖證據和正文界限清楚，長文保持安靜。
- **[R] 失效條件與未知數：** 不偽造布料質感、不把裝飾邊框變全站 CSS 邊框，更不複製布料版權圖。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M08 — Kinfolk · Alex Hunting redesign 2021
**來源：** [1](https://www.itsnicethat.com/news/kinfolk-tenth-anniversary-redesign-schick-toikka-publication-graphic-design-230621) · [2](https://www.oneclub.org/awards/adcawards/-award/43105/kinfolk-issue-40-redesign/) · [3](https://alexhunting.studio/blogs/projects/kinfolk)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 為 2021 十周年，Alex Hunting/Schick Toikka 開發 text、deck、display 專用 serif 含 italic，以及 caption/body 支援用 sans，設有特殊大寫連字；移除標誌性的封面白條，改格線容許更大的正文，改善紙張與色彩印刷。此改版獲 ADC 特定獎項。
- **[F] 可重建的編輯框架：** 不是一種 Serif 字級縮放，而是不同光學角色的字型工具箱；圖片與字體在開場和長文使用不同層級。
- **[D] 真正決定風格的細節：** 字面光學差異、標題/導讀/正文/圖說各自角色、連字的非必需性、封面空間。
- **[W] 《西望》的可操作轉譯：** 對應現存 Bodoni Roman／Italic／SC 與 Chiron 900/200/400 的十二語義尺度；區分正文和圖說，不以極細中文做微型 caption。
- **[R] 失效條件與未知數：** 不可挪用專屬字體或把舊白條當《西望》設計；不誤稱有 Kinfolk 精確字號。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M09 — Monocle · REJECTED art direction / archival negative case only (2007–08 / 2017)
**來源：** [1](https://cityofsound.com/2008/04/14/monocle-design/) · [2](https://magculture.com/blogs/journal/monocle-redesigned)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 第一手網站設計筆記具體列出 Plantin、Helvetica Neue、Strasse、四色系統、網格、止字符、引句、地圖、舊式數字和刊名字樣；數位長文不硬切頁，而處理行寬、leading、相關故事和上下文。2017 改版保留識別但縮減字體、加大正文、減密度、允許 off-grid 物件。
- **[F] 研究檔案（非正面風格參考）：** 其資料反映大量資訊模組／欄目／微型標記形成的出版方式，但《西望》不採用這種視覺秩序：密集、規整、以資訊管理優先的圖文框架不符合需要的現代藝術張力。
- **[D] 否決的視覺細節：** 密集的欄格、小型資訊標籤、連續線條與規整編排不應轉化為《西望》的視覺語法。原調查中列出的字體／止字符／地圖項目只是歷史研究事實，不構成採用建議。
- **[W] 《西望》的採用決策：** **拒絕移植** Monocle 的整體排版、字體搭配、資訊密度、網格與微型裝飾。『把每個元件寫進規範』是本工程的獨立治理要求，由 Design OS §6E.19 的 S01–S32 說明，**不是**對 Monocle 視覺的繼承。
- **[R] 正式否決：** **MONOCLE VISUAL REFERENCE = REJECTED**。不得放入《西望》候選風格板、使用它替新稿決定版心／圖片／字體位置，亦不得以它為 18/20 品質對標。2017 紙本不等於今天網站 CSS；任何私人排版手冊仍未取得。
**否決核對：** 後續設計方案／獲獎級自評的正面參考清單中不得出現 M09；保留此案僅便於追溯『成熟的規範仍可能擁有不符合目標的視覺』這一篩選判斷。

#### M10 — Eye · 1990–2024 cover & typography practice
**來源：** [1](https://www.designweek.co.uk/what-makes-a-great-eye-magazine-cover/) · [2](https://www.spd.org/behind-the-scenes/eye-96-and-eye-97)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 紙本大小相對穩定，從 Issue 41 每期更換展示字體，而從 Issue 72 Simon Esterson 更連正文、標題與圖說字體也按當期研究主題變化；封面可以讓字形本身構圖。
- **[F] 可重建的編輯框架：** 持續身份可以來自編集判斷而非死守一套字體；題目與本期視覺需要有因果關係。
- **[D] 真正決定風格的細節：** 期別主題、封面字形手法、標題與圖像是否為同一敘述、固定物理規格。
- **[W] 《西望》的可操作轉譯：** 《西望》不變更已核准 Bodoni/Chiron，但可變化同字族字級與圖像、裁切、版位軸線，形成一期一編輯題的特色。
- **[R] 失效條件與未知數：** 不推薦全站每期換字族，違反唯一 OS 權威。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M11 — Cereal · 2012–2015 founder interviews
**來源：** [1](https://vsco.co/archive/journal/vsco-film-cereal-magazine) · [2](https://magculture.com/blogs/journal/interview-with-rosa-and-rich-cereal)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 創刊人 Rosa Park/Rich Stapleton 先擬主題，通常收斂到四至六組，再做稿件研究與攝影；每章保留參考書目；標誌字母間的分線象徵書架上書的分隔。大量白色空間服務圖片呼吸，封面色調／構圖經過大量比對。
- **[F] 可重建的編輯框架：** 從題目開始，而非先從視覺模板開始；風格經過影像編輯、研究深度、空白節奏形成。
- **[D] 真正決定風格的細節：** 照片色調與主體、遠近景、書目歸檔、空白的功能、封面微妙調整。
- **[W] 《西望》的可操作轉譯：** 每樂章訂編輯命題及參考書目來源；刻線圖需同圖不同構圖對比，不用灰階濾鏡替代圖像研究。
- **[R] 失效條件與未知數：** 不把「簡約」當白色空地；不可假定 Cereal 有固定留白百分比。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M12 — The Gourmand · Lane & Associates studio case
**來源：** [1](https://www.laneandassociates.co/work/the-gourmand-journal) · [2](https://laneandassociates.co/work/the-gourmand-journal)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** Lane & Associates 將飲食視為文化、藝術與人物敘述，以雙年刊節奏容納文學、攝影與圖形；與 Universal Thirst 合作開發專屬字體。
- **[F] 可重建的編輯框架：** 一致性不是食譜卡片，而是每個主題在攝影、字體和文化參照中顯露的編輯觀點。
- **[D] 真正決定風格的細節：** 字體專屬性、作者和攝影的相互說明、圖像詼諧與文章深度的配比。
- **[W] 《西望》的可操作轉譯：** 不同查經／歷史／人物／影視欄目可有不同圖像結構，但同一編輯和字體權威；每一版必須說清圖像如何承擔命題。
- **[R] 失效條件與未知數：** 缺少一手細化版面參數，不能虛構其網格欄數或自訂字體名稱。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M13 — Noble Rot · All Purpose studio redesign 2024
**來源：** [1](https://allpurpose.studio/noble-rot/)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** All Purpose 說明其工作是保留帶有反叛氣質的飲食／葡萄酒文化出版物傳承，同時以鮮活的現代設計語言更新；設計作品有多幅封面內頁圖。
- **[F] 可重建的編輯框架：** 重點是歷史題材可以在現代表現中有活力，語氣和圖像選擇先於僵硬的古典外觀。
- **[D] 真正決定風格的細節：** 刊頁能量、封面敘事、色彩節奏與圖像類型，而不是一套無證據的數值表。
- **[W] 《西望》的可操作轉譯：** 《西望》的歷史內容不必都是咖啡色、嚴肅與厚重；需配合內容選擇明亮或克制視覺。
- **[R] 失效條件與未知數：** 現有官方頁沒有提供字體點數／版心規格；該案僅作藝術方向參考，不可作數值權威。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M14 — L'Express · Mark Porter Associates redesign
**來源：** [1](https://markporter.com/work/lexpress)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 工作室查核雜誌 1960–70 年代的資料；在黑紅／橙、新聞攝影與 sans 的傳統新聞週刊語法內引入現代排版與圖像；重視攤位距離可辨識的標誌和封面。
- **[F] 可重建的編輯框架：** 古典＝找回自己的可信出版 DNA；現代＝依當代讀者與資訊載體重組，而不是全部推翻。
- **[D] 真正決定風格的細節：** 封面遠距辨識、字體密度、圖像新聞性、舊刊歷史元件的保留條件。
- **[W] 《西望》的可操作轉譯：** 只繼承自身的城、晨星、活水、刻線、經文，而非直接套用紅／黑新聞模板；加入縮圖辨認測試。
- **[R] 失效條件與未知數：** 不把政治新聞的急迫排版用於全部沉思文章。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M15 — The New York Times Magazine · April 2026 Gail Bichler / Ben Grandgenett
**來源：** [1](https://www.itsnicethat.com/features/gail-bichler-the-new-york-times-magazine-redesign-publication-spotlight-080426) · [2](https://www.nytco.com/press/the-new-york-times-magazine-unveils-first-redesign-in-a-decade/)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 保留定製 slab 特色，改以 Cheltenham 和 Franklin Gothic 家族的現代設計加入具有文學感的 italic 和特殊字符；延續七欄格線，留一個狹欄放圖說；標準化 caption、引文和規線，把頁碼、欄名、日期移上頂部，留更多上方空間；同一故事支援紙本、數位、音訊和影片。
- **[F] 可重建的編輯框架：** 完整系統跨寫作、委約、發佈格式與每個字型角色；網格是可變內容容器，七欄是這一本的需求，不是萬用答案。
- **[D] 真正決定風格的細節：** 七欄功能（含 narrow caption rail）、小字微規格、頁眉頁腳、引文／圖說、正文可讀、跨媒體模板。
- **[W] 《西望》的可操作轉譯：** 把《西望》12 個字體語義角色與 cap/source/caption/folio 逐一接好；允許 caption 軌道而不是固定三個裝飾面板；保證長文還能閱讀。
- **[R] 失效條件與未知數：** 不照抄七欄、未授權字體或把互動媒體當作每篇都要有的裝飾。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M16 — Delayed Gratification · 2010 Slow Journalism premise
**來源：** [1](https://www.designweek.co.uk/issues/december-2010-online/slow-journalism/) · [2](https://www.slow-journalism.com/)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 慢新聞的編輯命題容納漫畫式敘事、新聞影像、資訊圖和數千字長文；時間尺度和深度先於圖像種類。原訪問頁面在本輪直接開啟受阻，只能以搜尋摘要支持較寬泛的事實。
- **[F] 可重建的編輯框架：** 一致的是時間框架、索引順序與編輯故事深度；各類敘述以合適自己的圖形結構呈現。
- **[D] 真正決定風格的細節：** 事件時序、圖表圖例、相片／圖解來源、跨文章統一說明語法。
- **[W] 《西望》的可操作轉譯：** 城史時代、經文事件和城市時序可形成可引用的圖像／地理／時間模組；不是讓每段故事變隨機照片卡片。
- **[R] 失效條件與未知數：** 原頁不可全文核對，不能用它確認具體字族、精確像素或紙張規格。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

#### M17 — Designlines · Cristian Ordóñez redesign 2019
**來源：** [1](https://www.designlinesmagazine.com/5-questions-cristian-ordonez/)。**證據等級：** 公開一手訪談／工作室或權威報導；細節不限於同一期，已標示時間。
- **[E] 原刊證據：** 先研究受眾與歷史、印材限制才動手；由設計師明說選擇 Graphik sans 和 Archive serif，封面以小寫刊名和滿版圖片提高親近感，室內圖片保留呼吸空間，每篇特寫有一致的局部視覺處理，且刊名須適應網站。
- **[F] 可重建的編輯框架：** 建立完整的編輯品牌規範時，受眾→素材→字體→印刷→數位不是幾個孤立階段，而是互相限制的一個設計決策。
- **[D] 真正決定風格的細節：** 刊名字母大小寫、圖文留白、字型對位、數位可縮放、封面圖片與內頁共同語氣。
- **[W] 《西望》的可操作轉譯：** 讓同一正式刊名在桌面／手機保留原 SVG，出版物的封面／段落／目錄有一個共同視覺邏輯，同時每篇有其特殊構圖。
- **[R] 失效條件與未知數：** 不盲目模仿 Graphic/Archive 或說其詳細標準書已公開。
**驗證任務：** 請在《西望》真正的一篇稿件上展示此案學到的「內容→構圖→具體細節」關係，並用一張正例／反例截圖證明不是仿製其外貌。

### 6E.18 Seventeen-publication synthesis — the rules underneath their differences

| 系統問題 | 代表研究 | 《西望》可立即採用的方法 | 待取證的細節 |
| --- | --- | --- | --- |
| 古典來源的選取 | M01、M02、M14 | 先回溯自己的刻線、城牆、活水、晨星資產；只保留有敘事職能的歷史元素 | 原作來源、年份、可使用權限、描繪內容 |
| 固定識別／變化構圖 | M03、M05、M10 | 固定正式 LOGO、Bodoni/Chiron 和出版物語氣，封面／內頁圖片形狀可變 | 每一期的可變部件批准表 |
| 字體光學角色 | M08、M15 | 正式 12-role scale 分別管理英文 display/italic/SC、中文 900/200/400、正文、目錄、caption | 真實字形載入、中文斷行、放大 200% |
| 網格與例外 | M01、M15 | 依故事和圖片選 6/8/12 工作軌，記錄偏離原因，不把軌道畫成三片色塊 | 標題與圖片避讓、caption 軌、字距尺度 |
| 圖像裁切／真實性 | M06、M07、M11 | 主體識別、光線、刻線密度、可裁區及禁字區決定照片形狀 | 原畫尺寸、來源、授權、主體座標 |
| 目錄／章節 | M01、M04、M15 | 四樂章明確分章，大號號碼只輔助選讀，正文題名／真實鏈接才是主體 | 12 條真實導覽與 3 個間奏 |
| 文章長篇與結尾 | M03、M04、M11、M15 | 正文專心閱讀，來源／註腳／尾部鏈結／城垛止字符都要有信息角色 | 實稿、注釋、出處、原始城垛資產 |
| 數位與紙本 | M01、M02、M15、M17 | 保留出版身份，但不把紙張虛擬成網頁固定分頁 | 行寬、導覽、閱讀恢復、封面來源 |
| 留白和節奏 | M01、M07、M11、M13 | 留白用於隔章、讓史料呼吸、避免密字碰撞 | 手機空白過長及文字太小的負例 |
| 工程治理 | M06、M15、M17 | 每個規格必須有素材來源、HTML 語義、OS token、所有 CSS、手機和截圖回歸 | 實際設計／開發／驗收責任 |

**共同判斷：** 不同刊物即便都用大襯線字、紙色或正方圖片，真正身份來自內容次序、微字體、作品選圖、圖片和引文的對位、章節節奏、分隔線用途以及數位閱讀。New Yorker 引文標點、Gentlewoman 章尾 References、Paris Review 書脊、NYT Magazine 的窄 caption 軌，都是**細節具體構成出版身份**的例證，而非可以任意抽換的裝飾零件。**M09 Monocle 已否決，不得由此段恢復成正面參考。**

### 6E.19 Full-detail specification book — 32 production sheets, not 32 screenshots

**第一目標：** 把下列 S01–S32 都補成可操作的設計規格；每張至少包含：用途與讀者任務、內容來源、正例反例、字體及色彩既有 Token、相對比例與實際尺寸（待實測）、響應式變化、CSS 所有者、無障礙、實際截圖、失效條件、批准狀態。**本輪建立的是完整製作清單與評審方法，不是已經取得 32 張核准版面或一套新 CSS 系統。**

| 編號 | 設計部位 | 必須細化到什麼程度 |
| --- | --- | --- |
| S01 | 刊物品牌命題 | 對象、內容、不同於參考雜誌的理由、正／負面案例 |
| S02 | 編輯語氣 | 歷史、信仰、當代感、中文與英文角色、文字來源 |
| S03 | 官方刊名 | SVG 原圖、清晰空間、深／淺底和小屏 |
| S04 | 封面／First Look | 刊名、主題、圖片、導航、來源、反向動效 |
| S05 | 期號與欄目 | 四樂章、十二欄、三間奏，真實目錄及定位 |
| S06 | 版心座標 | 邊距、工作網格、對齊基線與跨欄例外 |
| S07 | 留白 | 各場景的空白職能、進度節奏和手機轉換 |
| S08 | 打破網格 | 什麼層可覆蓋、主體／文字的安全規則 |
| S09 | 英文展示字 | Bodoni Roman 字形比例、optical alignment、不可拉伸 |
| S10 | 中文主標題 | Chiron 900、短／長題、實際字面及換行 |
| S11 | 中文次級標題 | Chiron 200、大小與行高、禁止極小細字 |
| S12 | 正文 | Chiron 400、字數／行寬、段距和長文續讀 |
| S13 | 中英混排 | 經文、標點、斜體、數字與 CLREQ 驗證 |
| S14 | Deck／引子 | 真正來自文章還是經編輯核准的摘要 |
| S15 | Folio／期號 | 定位、鍵盤可達、真正的連結用途 |
| S16 | 樂章開頁 | 四個樂章可辨認又屬同一本雜誌 |
| S17 | 目錄索引 | 全部條目、可掃讀、真實鏈接和回到目錄 |
| S18 | 圖片與圖說 | 編號、描述、來源、作者、授權、長短圖說 |
| S19 | 素材 manifest | 原圖、歷史可信度、權限、使用範圍 |
| S20 | 方形圖 | 何時聚焦，何時主體被破壞，不能強制使用 |
| S21 | 寬幅／直幅 | 原圖與取景、敘事跨度、縮放與斷點 |
| S22 | 滿版與影片 | 何時沉浸，入口控制、文字安全與退化 |
| S23 | 多雷刻線 | 細節密度、明暗、景深、筆觸、真實圖像 |
| S24 | 史料／地圖 | 時空出處、圖例、縮放和真實／重建區別 |
| S25 | 人物攝影 | 臉部、手部、衣服與內文關係，避免遮擋 |
| S26 | 引文 | 原文校對、真正出處、中文與 Bodoni Italic |
| S27 | 註腳參考文獻 | 跳轉、返回、來源品質、註解體系 |
| S28 | 文章終止符 | 找回早期主站城垛源資產後才定比例和位置 |
| S29 | 編輯動效 | 閱讀意義、時間曲線、返程、中斷和減少動效 |
| S30 | 裝置與縮放 | 1648/768/390/320 實測及真正 200% zoom |
| S31 | 獲獎級審查 | OS §6A 10×2、>=18、零分及 BLOCK 規則 |
| S32 | 工程可追溯性 | 版本、擁有人、文件→Token→CSS→截圖→驗收 |

### 6E.20 Doré engraving as a design *system*, not an antique image treatment

**具體的圖文設計先看四個物理構成：** (1) 作品主體：城門、人群、城市、道路等實際描繪；(2) 明暗構造：光線方向及最安靜的畫面位置；(3) 刻線密度：在縮圖下是否變成灰噪，能否保留可讀圖像；(4) 空間／敘事軸：消失點、門洞、視線和人物朝向能否承擔閱讀方向。

| 實際觀察 | 版面轉譯 | 禁止的失敗 |
| --- | --- | --- |
| 主體靠近門洞 | 把版心和敘事入口對準真實圖像軸 | 為圖像配文捏造不存在的城門 |
| 人群密集交錯刻線 | 英文展示字轉移到紙面或留白上 | THE GATE 末尾字母被圖片遮住 |
| 遠／近處有明顯光區 | 影像的節奏可從全景走向局部 | 同一張刻線當背景重複貼兩遍 |
| 方形裁切保留核心事件 | 可作少量標誌性圖像章節 | 強迫每一篇都有 1:1 封面 |
| 複雜線條近看鮮明、遠看密集 | 按真實顯示面積驗證每張原圖 | 全面套 sepia 或過強對比取代刻線 |
| 圖像與歷史敘述不完全相同 | 有明確 artwork／reconstruction／document 類別圖說 | 將插畫當作遺址照片或歷史證據 |

**原圖裁切工作卡（待真正逐幅核對）：** 記錄原始路徑、作者和權限、像素尺寸、主體矩形座標 (0–1)、不可裁區、文字禁止覆蓋區、可加字的安全區、1:1／寬幅／滿版替代視圖、桌面及手機的圖說／alt、每個版本的正反例截圖。沒有原圖核對的具體框座標，狀態就是 **[OPEN]**，不可杜撰百分比。

### 6E.21 Five cross-publication close-up lessons — how style becomes a decision

**① 一個目錄到底要怎樣有辨識度？** WoI 的巨大頁碼、Paris Review 實體書脊與 Gentlewoman 的 Part 分頁，表示「索引設計」不等於一串大號數字。《西望》四樂章的 01/02/03 可以很美，但首先必須讓人找得到真正文章，並能從文章返回。

**② 遇上繁密刻線與大字，究竟該覆蓋還是分離？** WoI 讓大型圖像呼吸；Kinfolk 則用不同字體光學角色處理展示和正文；Apartamento 先從原圖決定構圖。《西望》應以線條密度和主體安全區決定：有安靜空間才讓 Bodoni 局部進圖；沒有則將字完整置於圖片外。**不能為了構圖衝擊力遮住英文單字。**

**③ 幾萬字的文章如何和封面屬於同一本雜誌？** New Yorker 的引號與語氣、NYT 的 caption 軌、Kinfolk 的不同文字光學角色都不是 Hero 效果。真正一致是標題、欄目、引文、圖說、出處、資料密度和結尾續讀的共同文法；正文不需要每幾段插一張方圖。

**④ 古典不應只是模仿舊物。** Paris Review/L'Express 從自己的檔案中抽出可用歷史，Cabana 的紙材與布封來自真實工藝。《西望》取用自己的多雷資產、史料、城垛與原始動效；不要新增假的皺紙／紡織紋理。

**⑤ 如何避免整本刊物像同一頁的複製？** Eye 容許依主題變換字體，Gourmand 依文化題材變換圖像敘述，Gentlewoman 的篇章卻保持穩定的章節秩序。《西望》在固定 OS 字族和色彩之外，容許題材決定版面軸、圖片比例與強弱，這才是統一而非同一。

### 6E.22 Production proof — make this a usable specification book rather than research prose

**每張規範卡都必須包含：** 故事 ID、原稿來源、圖像／作者權限、使用情景、單句編輯目的、構圖圖示／樣張、所用 OS 字體角色與色彩來源、測過的寬度與字行、本文 HTML 結構和負責 CSS、鍵盤／焦點／reduced-motion、不同裝置的實景截圖、已拒絕方案與原因、測試提交 ID 及批准記錄。若沒有任何一項，標記 [OPEN]／[BLOCK]，不能自動變正式規範。

**順序：** 原稿→圖像主體和來源→編輯命題→網格→中文字和英文的光學對比→目錄／長文連續性→圖說／註腳→動效及返程→桌面／手機／放大檢查→反例對比。不要先選一個預設方塊，再把所有內容塞進去。

**內部門檻：** 依唯一 §6A，Westside 10×2 >=18/20、沒有零分／重大缺陷，還須真的通過正文閱讀、圖片來源、真實 200% 瀏覽器縮放、全鍵盤導覽、低動效及 1648/768/390/320 實測。D&AD／ADC 得獎例不等同自動證明 Awwwards／Webby／FWA；CI 綠燈也不等於藝術指導過關。

**下個規格任務：** 從實際保存且可合法使用的六張古典刻線原圖開始建立第一版 image-forensics atlas（城市全景、人物、建築、明暗、高密刻線、門口/河流）；之後用真實《城門口的人》及另一篇長文把 S01–S32 一項項做成實際正／反例。**本輪 17 案例是公開出版資料建成的研究級體系，不宣稱已核查每本私人內部規範書的全部字體數值，也不宣稱西望已確立最終藝術風格。**


### 6E.23 Doré original-image forensic atlas — six authentic plates, not six generic textures (research R3, 2026-10-22)

**Editorial purpose:** The six original works below are separate **evidence-backed art-direction specimens** to study an authentic relationship between 19th-century engraving and current editorial web composition. These are not six new image files committed to the site, not six fixed magazine templates and not six signed-off artworks for publication. **Do not conflate the site's modern illustrated / generated / derived visuals with verified original Gustave Doré engravings.**

**Source chain:** (a) original work / original publication / artist and possible collaborating engraver; (b) actual institutional or Commons *digital scan* with documented dimensions/rights; (c) local file or remote IIIF reference; (d) proposed design crop; (e) actual browser screenshot; (f) design + editorial approval. A public-domain 1866 *artwork* doesn't by itself authorize silently copying a museum's separately licensed photographic file. Wikimedia Commons' records below provide their own public-domain statements; the **London Museum's image states a separate licensing contact**. Never extrapolate rights from another scan of the same artwork.

**Important art-history nuance from primary scholarly research:** Doré's 1866 Bible plates were a collaborative published engraving process; some original drawings and their engraved descendants differ. His method used **dramatic lighting, characters immersed in landscapes and historical architectural environments**, rather than a uniform texture preset. University research distinguishes 1866 engraved plates from photographed unengraved drawings (1868), and studies *rejected* versions of particular compositions. **Do not label all Doré works as etchings or imply the hand of one artist physically cut every engraving.** See [Utpictura18 / Serge Ceruti, Genesis study](https://utpictura18.univ-amu.fr/en/rubriques/ressources/illustrer-bible/gustave-dore-and-the-book-of-genesis), [London Museum on the drawing/engraving collaboration](https://www.londonmuseum.org.uk/collections/london-stories/gustave-dores-london-pilgrimage/).

#### Six image specimens: original subject → density → shape decision

**D01 — Abraham's faith tested / The Testing of Abraham's Faith, Genesis 22.**
- **Primary record:** [Wikimedia Commons 016 — 1866, original digital 2303×2904](https://commons.wikimedia.org/wiki/File:016.The_Testing_of_Abraham%27s_Faith.jpg). Already catalogued in the **existing repo** at \`static/iiif/visual-dore-gen22-testing-abraham/manifest.json\` with artist, date, PD Mark and Commons source; its IIIF canvas records **2303×2904**.
- **Observed visual grammar from the actual original image:** dark robed Abraham **right foreground** and Isaac **left** bearing the wood, a bright horizontal far distance, palms at upper right, uneven dark vegetation at bottom. **Visual caution:** the inspected public preview visibly shows a younger figure carrying wood and an older robed figure with a staff; the Commons image title broadly identifies Genesis 22, but that does not resolve its precise depicted verse or sequence. **Do not assert a unique moment in the Genesis narrative from the artwork alone.** The automated description claiming a knife, ram and angel in this same pictured file conflicts with the visible preview and must not enter the caption.
- **Subject/crop:** The relationship **two travellers + their wood + bright distant axis** is the minimum semantic unit. Losing the left standing figure or the right elder changes the story. Large Bodoni title is safest on a **separate paper field**, not across garments or palms. Deep contrast belongs to the figures/ground.
- **Candidate magazine use [TRIAL]:** a vertical illustrated encounter or a *bounded, subject-reviewed* square crop for a Genesis study; captions distinguish Doré's pictorial reading of the story from archaeology. Sample credit: “Gustave Doré, The Testing of Abraham's Faith, Bible illustration, 1866; Commons scan, Public Domain Mark.”
- **Rejection [BLOCK]:** a square that cuts either traveller; a metadata caption depicting Isaac's binding, ram or angel if absent from this plate.

**D02 — Tower of Babel / The Tower of Babel, Genesis 11.**
- **Record:** [Wikimedia Commons 010 — 1866, 2297×2897](https://commons.wikimedia.org/wiki/File:010.The_Tower_of_Babel.jpg); [Utpictura18 thematic study](https://utpictura18.univ-amu.fr/notice/20647-tour-babel-sainte-bible-mame-1866-g-dore).
- **Observed:** an enormous central **rising architectural mass**, cloud bands near the upper tiers, miniature workers/scaffolding below, and gesturing figures in the **foreground toward the lower centre/right**. Architecture is the spatial scale; humans provide narrative scale.
- **Subject/crop:** A narrow square centered in the plate is likely to remove either the tower's elevation/clouds or the crowd/foreground reaction. Portrait or near-full-plate treatment better preserves *vertical aspiration*. A wide panoramic crop must be specified as **detail only**, not “the entire Tower of Babel.”
- **Composition transfer [TRIAL]:** let vertical architecture set title alignment and narrative scale. The cloud band may offer an **apparent** low-contrast type possibility but requires actual local hatching/contrast test; safer to put a giant Bodoni title in a neighboring quiet field.
- **Rejection:** crop retaining only a generic stone tower, stripping the human scene or giving a misleading “reconstructed original city” geographic caption.

**D03 — People mourn over Jerusalem's ruins / Lamentations 1.**
- **Record:** [Wikimedia Commons 124 — 1866, 2357×2927](https://commons.wikimedia.org/wiki/File:124.People_Mourn_over_the_Destruction_of_Jerusalem.jpg).
- **Observed:** a towering pale, curving **stone wall on the left**, somber sky/structures **upper right**, a densely grouped set of **mourners across the lower half**. Light/dark are asymmetrical; wall can be bright but still richly textured.
- **Subject/crop:** Preserve *wall + collective grief* if presenting the whole narrative. A 1:1 crop may become a **separate study of masonry or one grief grouping** only when explicitly labelled “detail” with an accessible full-image route. Main title should never erase figures' faces or the emotional body gestures.
- **Westside role [TRIAL]:** best positive example of **historical city, human subject, texture and a specific architecture-dependent type-safe decision**; not evidence that the site is showing an actual photograph of ancient Jerusalem.
- **Rejection:** mistaking a broad pale stone area for automatically safe typography; caption claiming a documentary depiction of a precise ruin.

**D04 — Finding of Moses / Exodus 2.**
- **Record:** [Wikimedia Commons 031 — 1866, 2353×2921](https://commons.wikimedia.org/wiki/File:031.The_Finding_of_Moses.jpg).
- **Observed:** vulnerable infant and basket **low left**, figures kneeling/reaching near **left middle**, richly dressed attendants and vertical ceremonial forms across **centre/right upper region**, reeds toward left.
- **Subject/crop:** The physically smallest object is narratively **most essential**. In square crops, a “well-balanced” selection that excludes the left/bottom basket is editorially **false** even if the adult figures look excellent. Print/image editing is subordinate to meaning.
- **Westside role [TRIAL]:** define **subject-weighted cropping**: focal item importance is not proportional to pixel area. Preserve text/image unity with image as evidence and Chinese article meaning outside the human scene.
- **Rejection:** crop losing infant; text overlay on faces, hands and basket; unverified Egyptian-historical costume accuracy.

**D05 — The Red Sea / drowning of Pharaoh's army, Exodus 14.**
- **Record:** [Emory University / Pitts Digital Image Archive — Red Sea](https://dia.pitts.aws.emory.edu/image_details.cfm?ID=17072), title, artist and scripture explicitly catalogued. Emory credits an additional engraving signature to **Adolphe François Pannemaker**, illustrating the difference between Doré's authorship and the engraver's craft. **High-resolution request at this archive may require payment; we have not obtained it or rights to its hosted scan.**
- **Observed in publicly available pictured versions (not yet pixel-verified against an acquired institutional high-res):** masses and horsemen/figures in dense lower region, a wide water/sky contrast, motion against steep waves or shoreline, central atmospheric brightness.
- **Subject/crop:** An isolated 1:1 figure crop likely destroys the **collective horizontal action**; a panoramic or full image and slow narrative widening better transmit crossing/disaster. Identify whether scene shows **drowning**, **parting** or **Israel safely on shore** before writing an exact source caption; they are not identical image moments.
- **Westside role [TRIAL]:** link directly to the existing site's **water-to-door** idea only at the level of visual meaning (separation, depth, revealing/reversing), never replace the approved live ocean artwork nor claim its imagery is Doré's plate.
- **Rejection:** a “Red Sea” chapter with stock sea image presented as Doré, or unlicensed museum reproduction ingested.

**D06 — Over London-by Rail / urban panorama, 1872.**
- **Records:** [Science Museum Group collection 1872](https://collection.sciencemuseumgroup.org.uk/objects/co8014229/over-london-by-rail-engraving-london-england-1872-print), [London Museum](https://www.londonmuseum.org.uk/collections/v/object-490986/over-london-by-rail/), [British Museum description](https://www.britishmuseum.org/collection/object/P_1979-0407-16-31).
- **Observed:** an **arch / rail construction acts as a natural image frame**, dense brick chimneys and close roof-lines, many small yards/figures, receding urban depth and a smoke-inflected industrial sky. This is **Victorian London**, not biblical Jerusalem.
- **Subject/crop:** Preserve the large structural arch and **depth corridor** for the full image; a square cut only makes sense if presenting a distinct *detail* of the domestic/urban system. Never suppress its authored location to make it pass as generic historic-city evidence.
- **Westside role [TRIAL]:** learn how a **real architectural opening** frames layered city scale. Translate visual grammar to the *layout* of Westside historical city material, **not** transplant London roofs and railway into a Jerusalem article. A real article must use a thematically and historically correct source artwork.
- **Rights [BLOCK for using the London Museum digital photo]:** London Museum explicitly labels **digital image © London Museum** and requests image licensing. Keep a research link; do not import their hosted scan into the site.

#### Local repository asset audit — authorship is not style similarity

| Actual resource in repository | Present / verifiable | Authority | Publication decision |
| --- | --- | --- | --- |
| \`static/iiif/visual-dore-gen22-testing-abraham/manifest.json\` | **YES**, inspected IIIF Presentation 3 metadata and 2303×2904 canvas | Doré / Commons 1866 / PD Mark specified; remote image by Commons Redirect | **[SOURCE-VERIFIED]** for original-image identity, continue actual scan/crop and proper credit |
| \`static/images/home-opening-engraving.jpg\` | **YES**, GitHub directory lists 159048 bytes; source used by prototype | **Artist/provenance not verified** from repo metadata | **[BLOCK]** on calling it “Gustave Doré original”; treat as **existing Westside engraving-style source asset**, no invented identification |
| \`static/images/jerusalem-wall.png\` | **YES**, directory lists 139243 bytes | Author/scene accuracy/rights unknown | **[OPEN]** existing graphic treatment, **not automatically genuine Doré** |
| \`static/images/temple-stone-light.png\` | **YES**, directory lists 2410484 bytes | Author/scene accuracy/rights unknown | **[OPEN]** architectural/light study only until source proven |
| \`static/images/olive/*-editorial.png\` and \`static/dore-design/runtime/olive-editorial-covers.v1.json\` | **YES**, editorial speaker art files + manifest marked \`user-supplied-editorial-artwork\` and \`identitySynthesis: true\` | User-originated designed portrait assets, not historic nineteenth-century wood engraving plates | **[ASSET-PROTECTED]** preserve all 12; **not original Doré evidence** |

**Honesty gate:** Before calling a local file a “Doré original,” the artwork, image source file and bibliographic record must match. Size, grayscale and hatch look are never enough. We verified six original artworks **by outside public records**, but only **one site IIIF manifestation** of those six exists in the checked local directories. No binary images were newly uploaded/copied to the site in this research round. Images embedded in search-result thumbnails are *visual reference*, not pixel-exact crop coordinates.

### 6E.24 Source dimensions and cropping math: square is a costly choice

A square taken from a **portrait scan** at native width W and height H (H>W), without scale interpolation:
- center square source rectangle = \`x=0, y=(H-W)/2, width=W, height=W\`;
- fraction of total **vertical narrative** removed = \`1 - W/H\`;
- each end loses \`(H-W)/(2H)\` *if* the crop is centered.

| Original record | Source W×H | Top clipped by default center square | Bottom clipped | Total height lost |
| --- | --- | --- | --- | --- |
| D01 Abraham | 2303×2904 | 10.35% | 10.35% | **20.70%** |
| D02 Babel | 2297×2897 | 10.36% | 10.36% | **20.71%** |
| D03 Jerusalem mourning | 2357×2927 | 9.74% | 9.74% | **19.47%** |
| D04 Finding Moses | 2353×2921 | 9.72% | 9.72% | **19.45%** |

**[METHOD]** The percentages are *source geometry*, not visual-subject inspection scores. The 1:1 crop must be **moved according to the protected subject** and/or represented as an explicit detail plate. Even when centered, removal of 19–21% of vertical content can eliminate the child, horizon, people or tower. For 1.95:1 wide and full-bleed, compare **actual viewport/source frame geometry** rather than extrapolating the portrait crop to a desktop rectangle. Cropping cannot be approved from CSS alone; record before/after images with actual fixed source and story label.

**No arbitrary “subject safe percent”:** Find semantic focal points first and mark [OPEN] normalized coordinates. Pixel-level title exclusion requires the actual source raster file, not a 500px thumbnail or a presumed “bright area.” The CSS composition system shall consume approved coordinates only after review. A score cannot be generated from invented boxes.

### 6E.25 A reusable Doré-to-Westside image analysis card (mandatory for each sourced plate)

Each original-image specimen becomes one **operational S19/S20/S21/S23 specification card**, not another template layer. Use the existing editor/document hierarchy:

\`\`\`text
original_id:        D01–D06 / original title & edition
narrative_event:    What exact action / emotional change is pictured?
authorship:         Designer/illustrator + known engraver signature if identified
source_record:      Institutional permanent URL or Commons file revision
rights_for_file:    PD / institution-licensed / unknown + evidence
local_asset:        repo path / IIIF manifest / research-only, no file
original_pixels:    W x H confirmed or UNKNOWN
focal_subject:      people, object, architecture, light, gestures
narrative_minimum:  elements that must remain together to tell the truth
ink_structure:      hatch dense/light/dark by factual visible regions
depth_axis:         front > middle > far / horizontal > vertical
text_exclusion:     figure, face, hands, key object, signature, horizon
proposed_frame:     portrait / square detail / landscape / full / none
crop_candidate:     normalized x/y/w/h after actual raster inspection
exception:          if safe crop impossible, move title outside image
publication_caption: image is illustration, never archaeological photograph
type_roles:         OS Bodoni Roman/Italic/SC and Chiron 900/200/400
device_tests:       original / 1648 / 768 / 390 / 320 / true 200% zoom
reader_test:        what was lost or learned due to this crop?
quality_gate:       §6A 18/20 + no zero/BLOCK, rights, readability, keyboard
visual_evidence:    actual screenshots and accepted/rejected crop pairs
status:             SOURCE-VERIFIED / CROPPING-PENDING / BLOCKED / APPROVED
\`\`\`

### 6E.26 The first distinct magazine layout grammar produced by this atlas

**A / Witness, no distortion:** Let an original engraving carry an entire historical *event* as a native portrait or large unbroken image. Deep reading begins on quiet paper with correct source attribution. This is often preferable to a dramatic but false crop.

**B / Threshold, subject-based only:** If a true gate, arch or opening visibly organizes the source, position a separately authored editorial text region relative to its **architectural axis**. The article need not repeat the source image as wallpaper; overlap is allowed only when subject/title-safe areas are verified. **A small framed square may be an editorial highlight, never a mandatory template**.

**C / City, depth as navigation:** In panoramic or dense city imagery, transition from an observable outer city silhouette to a human-scale detail or relevant historical map. Label changes in *view* as crop/detail, preserve return to original and accurate chronology. Never use Victorian London to illustrate historical Jerusalem.

**D / Crowd, typography off the picture:** If the hatching is crowded or figures are narratively vital, move giant Bodoni and Chiron 900 **out of the image**. High-impact design comes from juxtaposed scale and negative space, not blocking human gestures. Fit Contents in its own readable register.

**E / Light, restrained reveal:** For real bright/dark engravings, let graphic depth influence scene progression: focus/approach/reveal/back, with full static image parity and reduced motion. Do **not** retune the frozen actual homepage movie or the church ocean/doors until an accepted art-direction prototype exists.

**F / Source and citation as editorial form:** The caption, bibliographic record, edition and optional known engraver are information, not microscopic gray decoration. Historic source identity can itself create a crisp contemporary editorial layer without vintage imitation.

These **six compositional methods are not six approved page skins**. Each must be proven by one real article opening, article middle, full Contents and closing, with at least one rejected alternative image treatment. The studio's prior THRESHOLD concept remains an unapproved trial.

### 6E.27 Award-level Doré image chapter acceptance

- **Art-history accuracy [BLOCK]:** correct Doré image and subject/action, named engraver when attested, accurate original vs digital reproduction attribution; studio can distinguish 1866 Bible, 1872 London, and 1868 unengraved sketches.
- **Modernity [BLOCK]:** does the composition remain recognizable at 160px **without the masthead** and without making a tired book-cover cliché? If not, return to image/content concept. Monocle / M09 remains **REJECTED**, not a positive benchmark.
- **Visual fidelity [BLOCK]:** no figures/object signatures severed, no word occulted by busy hatch, no duplicated engraving wallpaper, no uniform sepia/grain filter on long text, no factual location invented.
- **Digital experience [BLOCK]:** true picture dimensions and source, subject-safe desktop/tablet/phone crop, alt/caption semantics, font metrics and contrast; 320 CSS px + actual 200% zoom + keyboard/reduced-motion parity.
- **User task [BLOCK]:** full narrative from cover → four movements / 12 desks / three interludes → 20k+ characters of genuine reading → credits/end/next. A hero-only screenshot is never a publication.
- **Internal criterion:** the single Design OS §6A applies (10×2, ≥18/20, no zero/critical block), not a pseudo official Awwwards/Webby/FWA award forecast.
- **Unresolved items [OPEN]:** first source raster retrieval and title-safe polygon annotations for all D01–D06, rights checks for non-Commons scans, actual thumbnail comparison, published real device screenshot; no visual acceptance yet.

**This chapter turns archive scholarship into *actionable creative decisions* while maintaining the crucial honest distinction: source document inspected ≠ original image fully decoded ≠ a visually approved layout. Next work can continue in S19/S20/S23 inside this same OS. Do not open a second manual or merge a prototype before an approved publication identity.**


### 6E.28 R4 — source pixels → geometrically exact visible area → subject-safe composition (2026-10-22)

**Scope correction (2026-10-22):** This R4 procedure solves the special case of *image crop safety*. It **does not define the composition of a magazine spread**. A square may be a cross-spread graphic region, a field of type, a cut-through revealing another field, a mask, or a negative-space rhythm even when there is no photographic square crop at all. See §6E.29–31 before prescribing any image ratio, safe-text rectangle or CSS box. A layout can simultaneously use a square cross-axis field, a panoramic image and full-bleed color/engraving without constituting independent panels.


**This is a production method and a book-study chapter, NOT an approved visual direction.** The prior R3 atlas identified six Doré works and their source records; it did **not** acquire six high-resolution raster files nor annotate actual pixels. R4 bridges the gap between an image-source record and a reliable editorial layout decision.

**Primary technical sources:** [CSS Images 3](https://www.w3.org/TR/css-images-3/) on replaced-object sizing, [MDN \`object-fit\`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/object-fit), [MDN \`object-position\`](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/object-position); [W3C CLREQ](https://www.w3.org/International/clreq/) for CJK punctuation/line breaking; [WCAG 2.2](https://www.w3.org/TR/WCAG22/) on readability/resize/reflow/focus; [W3C WAI image-background contrast failure F83](https://www.w3.org/WAI/WCAG22/Techniques/failures/F83).

#### R4.1 Evidence ladder — what may and may not be inferred

| Evidence available | Safe claim | NOT safe to claim | Status |
| --- | --- | --- | --- |
| Original publication or Commons catalog + intrinsic W/H | Work identity, attributed date as catalogued, full source aspect, mathematical crop | Exact subject bounding boxes or uniform hatch/contrast maps | **[SOURCE-VERIFIED]** |
| Public web-preview (e.g. Commons 500×630) visually inspected | **Qualitative** position of subject/figures/bright-and-dark bands, artistic hypothesis | Sub-pixel glyph exclusion polygons, exact original-density values, target-device decoded pixels | **[VISUAL-PREVIEW / TRIAL]** |
| 1:1 preview from an image-search UI | Thumbnail appearance **only**; source may still be portrait | That the full source was square or that important material outside the thumbnail did not exist | **[CROPPED-PREVIEW]** |
| Licensed/full original decoded, provenance retained | Actual W/H, patch luminance/gradient, hand-annotated protected polygons, crop overlays | “This CSS passed” before real browser measurement | **[PIXEL-READY / OPEN QA]** |
| Real browser image, title, caption and responsive screenshots | Visual subject, optical typography and contrast for that *render* | General approved rule for other engravings or legally cleared usage without review | **[RENDER-VERIFIED / review]** |

**Specific R3 correction:** The *Testing of Abraham's Faith* source is listed by Wikimedia Commons broadly as Genesis 22 (file 016). A publicly inspected preview shows **wood-bearing younger figure left** and **staff-bearing older robed figure right**, not the knife/angel/ram asserted in one unreliable auto-description. The publication moment/verse cannot be assigned uniquely from title and preview alone; the R3 “earlier approach stage” assertion was too specific and is now corrected. A caption may name the work and cite Genesis 22, not invent depicted objects or a narrower verse.

**Original vs preview:** The project IIIF manifest records **2303×2904** for D01; Commons itself displays a **500×630** proportional preview, and image-search UIs can crop their tiles to **512×512**. Do not use a square result tile to approve a source's aspect or crop.

#### R4.2 Reproducible crop inverse — source-space geometry, independent of box pixels [METHOD]

Let W,H be **natural image pixel dimensions**; Bw,Bh are the actual rendered *image element's content box* in CSS pixels; px,py are the \`object-position\` fractions (0=start, 0.5=center, 1=end). For \`object-fit: cover\` with no additional transform, clip-path, transform-origin, EXIF rotation discrepancy or CSS borders in the measured content box:

\`\`\`text
scale              s   = max(Bw/W, Bh/H)
rendered source    Rw  = s × W
                   Rh  = s × H
pixel displacement dx  = (Bw - Rw) × px
                   dy  = (Bh - Rh) × py

visible source x0 = max(0, -dx / s)
visible source y0 = max(0, -dy / s)
visible source x1 = min(W, (Bw - dx) / s)
visible source y1 = min(H, (Bh - dy) / s)
visible crop      = [x0, y0, x1 - x0, y1 - y0]
normalized crop   = [x0/W, y0/H, (x1-x0)/W, (y1-y0)/H]
\`\`\`

The formula maps CSS *cover* back to source pixels; it does not choose an artistic crop. Browser-resolved \`object-position\` may use lengths, mixed percentages, logical keywords and transformations; in those cases normalize the actual computed geometry first or measure the browser rather than blindly substituting these equations. The image's **\`object-fit\` determines the clipping**, not whether the page's frame itself is a square.

**Reference implementation for a local research checker, NOT global runtime or another visual OS:**

~~~js
function coverCrop(W, H, Bw, Bh, px = 0.5, py = 0.5) {
  if (![W, H, Bw, Bh].every(n => Number.isFinite(n) && n > 0))
    throw new RangeError("positive source and box dimensions required");
  if (![px, py].every(n => n >= 0 && n <= 1))
    throw new RangeError("fractional object positions must be between 0 and 1");
  const scale = Math.max(Bw / W, Bh / H);
  const renderedW = scale * W, renderedH = scale * H;
  const dx = (Bw - renderedW) * px;
  const dy = (Bh - renderedH) * py;
  const x0 = Math.max(0, -dx / scale);
  const y0 = Math.max(0, -dy / scale);
  const x1 = Math.min(W, (Bw - dx) / scale);
  const y1 = Math.min(H, (Bh - dy) / scale);
  return {
    source: {x: x0, y: y0, w: x1-x0, h: y1-y0},
    normalized: {x: x0/W, y: y0/H, w: (x1-x0)/W, h: (y1-y0)/H},
    scale, clippedAreaFraction: 1 - ((x1-x0)*(y1-y0))/(W*H)
  };
}
// The same source: D01 2303×2904 (actual source record).
// 1000×1000 source view => y ≈ 300.5, h=2303 (20.70% vertical lost).
// 1950×1000 source view => y ≈ 861.49, h≈1181.03 (59.33% lost).
// This is crop arithmetic, NOT a subject-safety score.
~~~

**Crop math with actual recorded D01 size, center alignment (calculated):**

| Display field | Source pixels retained (approx.) | Source normalized vertical interval | Lost source area | Review |
| --- | --- | --- | --- | --- |
| Natural full portrait (contain/full view) | **2303 × 2904** | 0–1 | **0%** | Narrative baseline; no automatic clipping |
| 4:5 portrait with \`cover\` | **2303 × 2878.75** | 0.0043–0.9957 | **0.87%** | Almost whole source |
| **1:1 square** with \`cover\` | **2303 × 2303** | **0.1035–0.8965** | **20.70%** | Verify both travellers and wood |
| 3:2 landscape with \`cover\` | **2303 × 1535.33** | 0.2357–0.7643 | **47.13%** | May fail narrative continuity |
| **1.95:1 landscape** with \`cover\` | **2303 × 1181.03** | **0.2967–0.7033** | **59.33%** | Detail-only hypothesis pending subject study |
| 16:9 with \`cover\` | **2303 × 1295.44** | 0.2770–0.7230 | **55.39%** | Not a “full original” |
 
**The percentages here are mathematically correct for this single *portrait source* and center crop.** A true \`full-bleed\` canvas spanning the viewport is not synonymous with uncut image: under \`cover\`, viewport ratio still crops. If keeping the full image is essential, use \`contain\` or let the image follow native aspect with text outside.

#### R4.3 Protected subjects, exclusion fields and false “blank” regions [METHOD]

Before placing any live type, the art director annotates the original **full-frame** image with **four semantic layers**; never infer them solely from edge density:

1. **Narrative-critical subject masks P:** people and expressive gestures, eyes, face, hands, distinctive objects (Isaac's wood, Moses' infant/basket, Babel's height), historical/directional relationship; a small object may be highest priority.
2. **Compositional-axis lines A:** horizon, vanishing point, gate/arch axis, figures' collective direction and the boundaries of architectural evidence.
3. **Ink-density and brightness zones I:** local luminance, variance and line-edge strength at *effective displayed pixel size*. These are potential readability proxies, not reliable historical semantic labels.
4. **Source, signature and caption material C:** inscriptions and engraver signatures are part of the authored plate; do not crop or cover unless explicitly documented as a selected **detail** view.

Record protected geometry as normalized \`[0,1]\` rectangles or polygons with fields \`meaning\`, \`priority\`, \`annotator\`, \`source_revision\`. **No numeric D01 subject polygons are published in this round** because original high-res source pixels were not successfully acquired in the work container; the Commons preview permits only qualitative orientation. We will not invent precision from a thumbnail.

**Two independent tests are required.**

- **Subject preservation:** the selected source-space crop must contain **all mandatory P/C fields** for a full-scene claim; otherwise explicitly label the view as a detail and link to the full original. A partial face, one missing participant or missing narrative object is a **BLOCK** when pretending to show the complete scene.
- **Text-safe fit:** for every actual displayed text run T (ink bounds or conservative DOM text rectangle with optical safety margin), map T back to image source-space using the displayed transform; do not intersect protected P/C polygons. *Also* sample the final composite background contrast across all text lines. A rectangle simply avoiding faces is not necessarily contrast-safe; a blank-looking bright wall can still have dark hatching.

**Severity model:** \`BLOCK\` = wrong work/action/source, cut indispensable subject, hidden word, missing source clearance, contrast/zoom failure; \`IMPORTANT\` = reading fatigue, density jump, poor optical rhythm, distracting hatch near display; \`POLISH\` = minor alignment after all previous gates pass. Never turn these into an automatic aesthetic numeric score.

#### R4.4 Image “negative space” is not typographic white space

A quiet compositional field is **subjectually** quiet when it doesn't contain necessary action; it may remain **graphically** busy due to fine hatch lines. A texture's mean luminance is insufficient: test local minimum/maximum contrast and luminance variance with target text color at its real font weight and actual downsampled scale. Use grayscale line/edge-response only as a candidate ranking aid; physically inspect all finalists.

**Evaluation order when there is no safe image field:**
1. Move giant Bodoni / Chiron 900 **outside** the engraving into the existing paper/ink register. **This is often the most editorially forceful choice.**
2. If meaningful, crop to a differently labelled **detail** image, retaining the full work alongside or behind an explicit “view original” affordance.
3. Consider restrained, localized color treatment only if it does not erase a historically meaningful image segment and remains legible after the composite.
4. Do **not** rescue a crowded drawing with arbitrary duplicate wallpaper, global blur, repeated sepia, edge stretching, or an opaque black slab across a person's face.

**Do not mask bad typography through contrast-only filters.** The text can be W3C-contrast-compliant and still be editorially false because it hides hands, architecture or an essential object. A dynamic image needs a conservative live sample at each caption/title region after it is rendered.

#### R4.5 Bilingual title placement — different optical occupations, one coherent reading order

Existing authority remains **Bodoni Moda Roman/Italic 400 + genuine SC**, and **Chiron Hei HK WS 900 (main Chinese), 200 (large secondary), 400 (body)**; no font-family changes or new global typography tokens.

| Role | Source relationship | Layout requirement | Optical check / rejection |
| --- | --- | --- | --- |
| Giant English display | Can act as a **graphic counterweight** to dark line masses | Live semantic type, typically an exterior paper region if engraving dense | Does **every letter** remain decipherable? \`GATE.\` must not lose E or stop |
| Chinese main article title | States what the authentic story is about | 900 weight when primary; logical DOM heading remains visible | No line breaks that isolate punctuation; no resizing / stretching letters to fit square |
| Chinese 200 supporting display | Can introduce a calm reading threshold | Large readable size and sufficient line height **outside line-busy areas** | Never tiny 200 metadata; no overlapping extenders/quotation marks |
| Body and source | Research, read, verify | Genuine Chiron 400, open paragraph measure, figure caption adjacent to artwork | Do not set historical-source credit as near-white 10px over intricate hatch |
| Bodoni Italic scripture | An authentic quotation *with exact text and reference* | Semantically bound to citation and visually separate from archival caption | No invented biblical line or isolated unlabelled quotation |
| Folio / small caps | Orientation and action, not luxury decoration | Genuine SC, low hierarchy, anchor to real Contents if interactive | Legible at 390px, focus visible and not hiding artwork signature |

**Collision contract:** \`ImagePlane\` and \`TextPlane\` may overlap **only when** the image contains a deliberately approved text-safe region *and* all heading segments remain optically intact. A print-like giant letter cropped at a page edge must still preserve the word's semantic reading. If source image content must remain intact, prioritize **separate adjacent planes** rather than an overlap effect. Avoid translating English \`text-wrap: balance\` expectations to Chinese automatically: Chinese punctuation and line breaks require CLREQ-informed visual review. Reflow must remain natural at 320 CSS px and actual 200% browser text resize.

#### R4.6 A publisher-level image/text coordinate sheet, with an explicit DOM owner

**The art-direction sheet produces data and layout decisions; the website consumes only approved instances**. A source-linked candidate record could be:

~~~json
{
  "specimen_id": "D01",
  "source_record": "https://commons.wikimedia.org/wiki/File:016.The_Testing_of_Abraham%27s_Faith.jpg",
  "existing_iiif": "/iiif/visual-dore-gen22-testing-abraham/manifest.json",
  "source_dimensions_px": [2303, 2904],
  "work": "The Testing of Abraham's Faith",
  "authorship_source": "Gustave Dore (1866), Commons file record",
  "publication_rights_review": "SOURCE RECORD VERIFIED; FINAL USE APPROVAL OPEN",
  "protected_polygons_normalized": null,
  "artist_inscription_polygons_normalized": null,
  "exclusion_polygons_normalized": null,
  "image_density_zones": null,
  "candidate_shapes": ["native", "square-detail", "landscape-detail"],
  "crop_rect_source_px": null,
  "title_rect_css_px": null,
  "text_type_roles": ["display-en", "display-zh-primary"],
  "desktop_phone_zoom_evidence": null,
  "status": "CROP_GEOMETRY_COMPUTED; IMAGE_ANNOTATION_OPEN; NOT_APPROVED"
}
~~~

**The \`null\` coordinates are intentional**: actual research has not resolved them. No new JSON system is installed, and this specimen is illustrative schema documentation only.

**Once approved**, a scoped source-bearing component might follow this structural contract (one existing Journal owner, **not applied to production**):

~~~html
<article data-ws-scope="journal">
  <header class="ws-editorial-opener">
    <p class="ws-editorial-edition">VOL.00 · THE GATE</p>
    <h1 class="ws-editorial-article-title">城門口的人</h1>
  </header>
  <figure class="ws-editorial-source-image">
    <img src="[verified-image-asset]" alt="[meaningful image description]">
    <figcaption>[actual artwork, date, author, reproducer and source]</figcaption>
  </figure>
  <section class="ws-editorial-reading" aria-label="文章正文">
    [canonical manuscript paragraphs, headings and notes]
  </section>
</article>
~~~

This is an **HTML contract illustration**, not fabricated article copy or an operational source path; the real component must consume actual manifest/verified assets. The title may visually share a composition but stays live, selectable and correctly represented to assistive technology. Image figures keep descriptive captions and own their image metadata. No separate CSS owner created during the R4 documentation round.

#### R4.7 Approval matrix: six different images, three image ratios, four screen states

| Evidence ID | What to test | Must establish | Current status |
| --- | --- | --- | --- |
| A0 | D01–D06 original catalog check | Work/date/medium/digital-file license/author attribution | 6 source records researched; rights status varies |
| A1 | Original full raster + source manifest | Exact decoded pixels, mark whether trim/border/EXIF change crop | **OPEN; no full six-image local acquisition** |
| A2 | High-resolution subject polygons P/C | Subject, gesture, inscription and axis positions from original | **OPEN** |
| A3 | 1:1, portrait, wide controlled crop images | One retained detail and one rejected full-scene candidate per source | **Arithmetic example only** |
| A4 | 1648×928 and 768×1024 browser renders | Exact displayed clip, title-safe margins, optical body/headline | **NOT VERIFIED** |
| A5 | 390×844 and 320px reflow | Chiron 900/200/400, Bodoni and captions legible | **NOT VERIFIED** |
| A6 | Actual browser 200% zoom, not reduced CSS viewport proxy | Full story, safe edges, keyboard/focus, no lost copy | **NOT VERIFIED** |
| A7 | Live background/text contrast | 4.5:1 normal and 3:1 large text where WCAG 2.2 1.4.3 applies, checked at changing image patches | **NOT VERIFIED** |
| A8 | Original scene truthfulness and credit | Thumbnail identifies the true image, complete item and full-image path | **R3 source notes only** |
| A9 | Entire magazine narrative | Cover, Contents, real middle paragraphs, citation, ending and next | **NOT APPROVED** |

**Preconditions for §6A release:** visually unique contemporary magazine identity, true Doré authorship when claimed, artwork-preserving crop, rights/caption accuracy, native type + body readability, accessible source and Contents, all viewport/zoom conditions, then **internal 18/20, no zero, no BLOCK**. Neither crop mathematics nor build success can self-certify creative originality or imply Awwwards/Webby/FWA endorsement.

#### R4.8 One-page decision instructions to use during an art-direction review

1. **Find the subject** in full authentic source before talking about 1:1. Write its true action and most easily lost object in one sentence.
2. **Choose the editorial task** (witness / approach / detail / panorama / pause / source note), then pick a candidate frame that serves it.
3. **Calculate the visible source rectangle** using R4.2 at the actual render box and object position; document exactly what is lost, not just aspect ratio.
4. **Mark protected masks** on the original source. If the draft crop cuts one, do not silently shift it: adjust/larger frame or retitle as a detail.
5. **Place live type** on paper first; move it onto the image only after safe subject-and-contrast proof.
6. **Compare three images**, not just three CSS states: full subject view, the selected crop, and a deliberately rejected crop with reason.
7. **Prove the whole publication** from cover to true Contents to real article reading and closing; then test 1648/768/390/320, actual 200% zoom and keyboard.
8. **Promote only an accepted composition rule** to its existing OS owner. If crop is unsafe or uniqueness fails, reject and return to the idea—not the ornament.

**R4 immediate outcome:** an exact mathematical and editorial protection method can be written **now**; verified per-image polygons and photographic tonal maps cannot be fabricated while the full raster remains inaccessible. This is why this round ends with complete handbook rules and an explicit UNVERIFIED annotation queue, rather than claiming the magazine design has been approved.


### 6E.29 Digital spread composition — a continuous editorial canvas without a physical binding seam (R5, 2026-10-22)

**A new PRIMARY art-direction grammar for Westside magazine, not a new CSS/Design OS:** On a sufficiently wide screen, **begin design research from the relationship across a virtual two-page spread** rather than treating the layout as one portrait image, a centered card, or two independent column-panels. **“Spread” describes compositional scale, not two literal web pages.** There is *no sewn binding, central print loss, compulsory paper fold, even left/right page widths, fixed sheet turn, paper trim or advertising-slot allocation*. A virtual 50% mark can be a **temporary construction axis**; the viewer must not see a simulated printed gutter unless a specific content concept justifies it.

**This is Westside's proposed wide-screen design approach, not a claim that every online magazine in the world is laid out this way.** Some articles are naturally a single continuous reading column. Digital editorial design has fewer *print constraints* but new obligations: scroll continuity, viewport-dependent width/height, interactive controls, keyboard/DOM reading order, responsive re-composition, real image provenance, reduced motion and actual content completion.

**Recovered oversized-English design research:** The repository already contains the authoritative [editorial type scale](WESTSIDE-EDITORIAL-TYPOGRAPHY.md), [magazine kinetic-typography memo](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md), [Italian executable composition grammar](../dore/italian-editorial-executable-grammar.v1.md) and [real type hierarchy laboratory](../../static/experiments/editorial-type-hierarchy-lab.html). **§6E.32** reconciles their English half-spread/monumental-type methods with the digital-spread model. They are cited source assets, **not** an invitation to add another CSS system, remake the approved logo or reproduce old test styling.

**Why the last crop research was insufficient:** §6E.23–28 begins with source W/H and computes the scene's visible rectangle. That protects historical content **inside an image** but does not explain the editorial design of **the whole spread**: where a huge typographic field begins, how a geometric object bridges two zones, what lies behind the object, how one phrase can cross an axis, or how the reader proceeds from image → story → Contents. Crop fidelity remains compulsory when using Doré images, but **the full composition has priority over any one image ratio**.

**Reference boundary:**
- [Pentagram / Citizen](https://www.pentagram.com/work/citizen) records designing the entire magazine's logo, grid, editorial pacing and structure, with a strong **flexible** grid allowing each story a different visual approach. This is **print editorial precedent**, not evidence for its exact live web CSS.
- [Pentagram / No Man's Land](https://www.pentagram.com/work/no-mans-land) documents an intentionally loosened **12-column grid**, asymmetrical margins and differentiated typographic material; again a *print* precedent for structured freedom, not a web implementation.
- [MDN CSS Grid / basic concepts](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Basic_concepts) confirms multiple CSS grid items can overlap a track/area and be layered with \`z-index\`; [line-based placement](https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Grid_layout/Line-based_placement) documents crossing multiple tracks.
- [MDN CSS translate](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Values/transform-function/translate) confirms percentage translations are relative to the translated element's reference box, permitting one square's 50/50 or 30/70 division to be specified **without using guessed viewport offsets**.
- [The World of Interiors / 2022 redesign first-person interview](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles) exemplifies preserving publication character **while** rethinking digital editorial expression. It does not mandate a centered square or literal digital paper spread.
- [Webby Awards judging criteria](https://www.webbyawards.com/judging-criteria/) foregrounds *overall experience*, content, navigation, visual design, functionality and interactivity—an impactful spread that blocks actual reading is not an excellent website.

#### R5.1 Print-spread constraints vs digital-spread opportunities — specify the difference

| Decision | Physical magazine | Digital Westside spread [METHOD] | Risk/gate |
| --- | --- | --- | --- |
| Midpoint | Binding fold/gutter may make central information difficult | Optional \`x=.5\` **invisible compositional axis**, never a fixed “seam” | Fake crease, disconnected halves, wrong typography |
| Opposite pages | Printed left/right pages have physical limits | **One continuous field**; image, shape, headline or negative space may cross the center freely | Overlap cannot obscure real story/interactive actions |
| Page proportions | Trim/print/bleed and paper dimensions chosen in advance | Width is fluid, height can follow narrative and content; no fixed sheet ratio | 90vh emptiness, artificial overflow/scroll lock |
| Editorial grid | Column systems constrained by spread and printer | Shared container grid and independently layered objects; can use 30/70 or 50/50 **field balance**, without visible two-panel borders | Avoid a row of unrelated UI blocks |
| Images | Print image may vanish in gutter | An unbroken panoramic image can continue from left to right; a square can overlay it without duplicating the source | One source, valid image provenance, correct focus |
| Text flow | Text boxes/columns broken by page turn | Longform is a **continuous semantic reading stream** that can leave the dramatic spread at the correct moment | No forced magazine pagination/mobile horizontal reading |
| Captions/folios | Book edges/spine/folio convention | Labels can move to useful image edge, scrolling reference or Contents; keyboard/focus needed if interactive | Ornamental microtext, nonworking navigational stamp |
| Ads/material | Advertising and printer restrictions may determine spreads | No print ad quota, ink limits or binding imposition for Westside's web pages | Digital still has legibility, media, page weight and control demands |

**Key distinction:** A **virtual pair of page regions is a mental aid**, never two fixed independent panels. The frame may be 30/70, 60/40, or a complex overlapping collection, and a panoramic plate may fill the entire union. The actual user reads a digital publication, not a photo of a printed magazine.

#### R5.2 Two distinct 30/70 definitions — do not confuse them

**A. Spread *field share*:**
- A left-domain width of **30% of the whole canvas** and right-domain width 70%. This may establish visual weight, text/figure placement, or image tension. It is an *art-direction hypothesis*, not a required two-column layout.
- The center between the virtual *editorial domains* need not be \`x=.5\`; with 30/70 domains their domain boundary is \`x=.3\`. Neither boundary needs a visual line.

**B. A *single square's* distribution across a virtual center axis:**
- Whole wide canvas width \`W\`; hypothetical center \`c=.5W\` or another deliberate \`c\`; square side length \`S\`; fraction \`p\` of **the square's own width** placed before that reference axis.
- Square left edge \`x_left=c−p×S\`. Right edge \`x_right=c+(1−p)×S\`. Its true height stays \`S\`; **nothing is stretched**.
- **Square 50/50:** \`p=.5\`; half of *the square* belongs to the left of axis, half to the right.
- **Square 30/70:** \`p=.3\`; only 30% of the square falls left of axis, 70% right. The virtual left/right domains can still each occupy half the canvas.
- The square can be a visual frame, a solid color/negative space, a live-text grouping, a figure container, or a **mask/portal on a single image field**. It need not represent a source-image **crop**.

**Exact geometry worked example (illustrative desktop, [TRIAL]):** for \`W=1440 CSS px\`, \`c=720\`, \`S=560\`:

| Distribution across \`c=720\` | Square's left edge | Square's right edge | Square aspect | Semantic effect under review |
| --- | ---: | ---: | --- | --- |
| 50/50 | 440px | 1000px | 560×560 | Stable deliberate center crossing, balanced visual anchor |
| 30/70 | 552px | 1112px | 560×560 | Right-biased movement, room left of image for a large title |
| 70/30 | 328px | 888px | 560×560 | Left-biased movement, potential right-side issue/Contents |
| No square used | — | — | — | Panoramic/full-bleed/vertical story can own the spread |

The **x coordinates are construction measurements**, not approved design values. Always account for page padding and reference axis: \`c\` may refer to a *content container* rather than full viewport. Record which. Without that information “square crosses center 30/70” is ambiguous.

#### R5.3 Seven different square *roles*, beyond cropping photos [METHOD + TRIAL]

| Role | How it occupies a spread | Editorial reason to consider it | Strong rejection condition |
| --- | --- | --- | --- |
| **S1 Portal / opening** | A single square straddles a notional center while a panoramic source continues behind | Concentrate the reader on a meaningful entrance/threshold | Portal reveals nothing or duplicates the original picture as wallpaper |
| **S2 Type field** | Square occupied by **live typography**, with image or paper continuing across its boundaries | Turn an issue claim or authentic headline into a compositional object | Word cut, meaningless isolated letters, fake typographic rendering |
| **S3 Negative-space square** | Square is made from a deliberately unoccupied field amidst otherwise connected visual mass | Give a visual pause or a meaningful point of rest | Empty square used only to look “designed” |
| **S4 Composite boundary** | An actual square delineates a live **change of field**—e.g. engraving detail against original archival description or spatial diagram | Express two credible views of a subject in one spread | One scene misleadingly presented as different historical evidence |
| **S5 Editorial focus** | 1:1 figure/detail bridges domain boundary with supporting title and metadata in separate fields | Center a real source detail while maintaining contextual source access | Essential gesture or source author cropped out |
| **S6 Rhythm/series register** | A square appears in **one or a few** key moments, perhaps split 30/70 and later absent | Establish a recognisable publication accent through *scarcity* | Every story, Contents and tool card has a compulsory square |
| **S7 Spatial motion** | A square can transform its editorial role (e.g. image focus → text field) during a reader-triggered state change | Clarify perspective, step or reading transition | Movement is purely decorative, traps scroll/focus, no static parity |

**No “one master square” rule.** The square is a signature instrument played at chosen moments, beside portrait, panorama, full-bleed, large text-only and quiet longform sections. Cropping is relevant *only* to S4/S5 where an image detail is actively framed.

#### R5.4 The five-layer spread model (one canvas, no three-panel imitation)

1. **Continuity field L0:** continuous background or paper/color field, potentially **one original engraving** across full width; do not duplicate imagery for an inset just to fake depth.
2. **Structural geometry L1:** one or more meaningful shapes (square, rectilinear plate, mask/negative space), chosen for the article's subject and permitted to cross the reference axis.
3. **Artwork/story L2:** verified actual image or true longform story segment; preserve subject, inscriptions, caption rights. A square at L1 does not force L2's native artwork to be cropped.
4. **Live editorial type L3:** original masthead asset, meaningful English/Chinese title, series, issue, source and caption, optically aligned to image and composition rather than placed as generic cards.
5. **Reader continuity L4:** real Contents/article/next route, source, focus, keyboard and equivalent reduced-motion information. L4 may be visually understated but is never optional.

**A continuous cross-axis object is not a third “middle panel”**. The rejected pattern was three independent colored vertical panels with disjoint images/content. In R5 the **relationship between all layers** is the composition; empty space and intentional nonuniform overlap are as important as object placement.

**More contemporary, not more decoration:** An intentional square can coexist with an enormous fully legible Bodoni word and a vivid Doré plate **only when the interaction of their visual masses communicates the subject**. Do not put white letters over the busiest engraved crowds merely to prove a layer stack is technically possible.

#### R5.5 A minimal CSS construction proving both square splits — local specimen only

This is an **example in the manual**, NOT a new global token, live component, or production CSS. The visual DOM order remains logical. All color/type references must consume the existing Design OS. Here \`50%\` refers to **the same containing spread**, and the percentage in \`translateX()\` refers to **the square element's own width** (verified by MDN).

~~~html
<section data-ws-scope="journal" aria-label="單一數位跨頁研究示例">
  <div class="ws-digital-spread">
    <div class="ws-digital-spread__field" aria-hidden="true"></div>
    <header class="ws-digital-spread__heading">
      <p>VOL.00 · THE GATE</p>
      <h1>城門口的人</h1>
    </header>
    <figure class="ws-digital-spread__square ws-digital-spread__square--30-70">
      <div class="ws-digital-spread__square-plate">
        <img src="[approved-original-asset]" alt="[truthful image content]">
      </div>
      <figcaption>[verified source credit]</figcaption>
    </figure>
  </div>
</section>
~~~

~~~css
/* Handbook example only, scoped to an existing Journal owner; no second CSS system. */
[data-ws-scope="journal"] .ws-digital-spread {
  position: relative;
  isolation: isolate;
  display: grid;
  grid-template-columns: repeat(12, minmax(0, 1fr));
  min-block-size: min(88svh, 58rem);
  gap: clamp(0.75rem, 1.6vw, 2.25rem);
  padding-inline: clamp(1rem, 4vw, 4rem);
  /* A virtual center is a coordinate, NOT a border or printed gutter. */
}
[data-ws-scope="journal"] .ws-digital-spread__field {
  position: absolute;
  inset: 0;
  z-index: 0;
  /* Use one coherent Design OS surface / image field, not 3 panels. */
}
[data-ws-scope="journal"] .ws-digital-spread__heading {
  grid-column: 1 / span 7;
  z-index: 2;
  /* The real H1 and reading order stay live and semantic. */
}
[data-ws-scope="journal"] .ws-digital-spread__square {
  position: absolute;
  inset-inline-start: 50%;
  inline-size: min(40%, 34rem);
  translate: -50% 0; /* 50% of square field on each side */
  z-index: 1;
  margin: 0;
  /* Figure remains auto-height; caption is not clipped into 1:1. */
}
[data-ws-scope="journal"] .ws-digital-spread__square--30-70 {
  translate: -30% 0; /* 30% of S left, 70% of S right */
}
[data-ws-scope="journal"] .ws-digital-spread__square-plate {
  aspect-ratio: 1; /* square media FIELD; caption is outside */
  overflow: hidden;
}
[data-ws-scope="journal"] .ws-digital-spread__square img {
  display: block;
  inline-size: 100%;
  block-size: 100%;
  object-fit: contain; /* preserve source until IMAGE crop approved */
}
[data-ws-scope="journal"] .ws-digital-spread__square figcaption {
  margin-block-start: .75rem;
  /* Natural height, not locked to 1:1. */
}
@media (max-width: 48rem) {
  [data-ws-scope="journal"] .ws-digital-spread {
    display: flex;
    flex-direction: column;
    min-block-size: 0;
  }
  [data-ws-scope="journal"] .ws-digital-spread__heading {
    order: 0;
  }
  [data-ws-scope="journal"] .ws-digital-spread__square {
    position: static;
    translate: none;
    inline-size: 100%;
    order: 1;
  }
  [data-ws-scope="journal"] .ws-digital-spread__square-plate {
    aspect-ratio: auto; /* mobile may show the full native image */
  }
  [data-ws-scope="journal"] .ws-digital-spread__square img {
    block-size: auto;
  }
}
~~~

**Implementation qualification:** The **square is the dedicated media field**, not the entire figure and caption. This specimen keeps original source art \`contain\` and uncropped unless an image-specific crop is later approved; its caption flows at natural height **outside** the 1:1 media plate. The figure itself can be taller than square. Without actual artwork and headlines, an absolutely positioned square may collide with live text and a long caption may exceed the stage; the actual \`min-block-size\` and layer relations must be measured in a browser. **Do not paste into production or imply visual approval.**

**Non-image construction:** Exactly the same cross-axis square can be a **live-type field, a clear negative-space field, or a meaningful boundary inside a single continuous engraved scene**. These need no \`img\`, \`figure\` or \`object-fit\` at all. When a title inside a square is the *real* headline, it must be a real live \`h1/h2\` in correct DOM order; \`aria-hidden\` applies only to a decorative duplicate when the complete semantic title remains elsewhere. **The square's compositional distribution is independent of photo-cropping geometry.**

#### R5.6 Responsive art direction: preserve the *relationship*, not the desktop geometry

**Desktop 1648×928:** wide-screen spread can keep a virtual design axis, intentional S1–S7 square crossings, a full-width image or live Bodoni crossing zones. It may be asymmetrical in 30/70/50/50 field balance without ever drawing a crease.

**Tablet 768×1024:** do not mechanically scale all positions by viewport ratio. Reframe a square so its semantic purpose remains (e.g. *focus* next to a caption rather than forced overlap). Allow two-column or near-full-width reorganization only if source title and figure are readable.

**Phone 390×844 and 320 CSS px:** the wide spread is **recomposed as a vertical editorial story** (heading, image/detail, source, real text, Contents), not a screenshot of a two-page printed magazine. There is no requirement to preserve a square, a faux center or 30/70 distribution on phone if it damages meaning. If the square served as a meaningful story portal, its interaction/semantics survive, though its visual framing can change.

**Real browser 200% zoom:** a new narrower viewport is not the same as verifying actual zoom; require no cut-off words, preserved controls/focus and no two-dimensional normal article scrolling. Reduced motion preserves static narrative state and true source/caption routes.

**Two different orders must be checked:** (a) visual gaze sequence across the wide canvas, (b) semantic DOM/keyboard/screen-reader order **independent of absolute positioning**. The DOM must tell the same story in a sensible sequence when all CSS is disabled. Avoid order:2/3 as a repair for an incoherent authored DOM or hidden interactive controls.

#### R5.7 Editorial decision test: is the square *necessary* to the digital spread?

Before approval, the art director must produce four **same-content** comparisons, in addition to crop studies:
1. **One clean uninterrupted spread, NO square** — baseline. Does its image, title and article identity already work?
2. **50/50 crossing** — what did the square make possible that a wide uninterrupted picture couldn't?
3. **30/70 crossing** — how did the shifted square change focal gravity, English/Chinese title order, negative space and the reading route?
4. **One full-bleed / unconstrained field** — does cinematic immersion serve this particular issue better than a square?

**Same manuscript, image provenance and roles must remain fixed.** Compare whole composition—not just zooming one artwork to different crops. Evaluate **spread silhouette at thumbnail, actual source at native size, empty-space intent, font word integrity, image-safe bounds, editorial hierarchy, scroll into real reading and mobile reconstruction**. If a square does not clarify the story or materially strengthen publication identity, remove it. *Sparse, meaningful use* is a design strength, not a missing template.

**A real art-direction study records the layer relations too:** where the image/color passes behind the square, what the two nominal halves contribute, how the figure interacts with the title, which edge anchors the narrative, and why changing the square's distribution from 50/50 to 30/70 changes meaning—not only measured x/y.

**Release criterion:** use the existing §6A award-calibre rubric (>=18/20, no zero or unresolved BLOCK), with genuine print-to-digital translation, content integrity, Webby-style reader experience, contrast and focus tests. CI/build success or a visually striking square cannot self-certify originality.

### 6E.30 Cross-spread design sheets — additions to the existing 32-sheet specification inventory

**The 32 S01–S32 sheets stay the same; we extend their required fields, not create S33/S34 or a second manual.** The layout design sheets gain a specifically digital composition section:

| Existing sheet | Newly required R5 design data | Evidence before promotion |
| --- | --- | --- |
| **S04 First Look** | Whole-canvas proposition; meaningful cross-axis visual relation; what remains continuous | Desktop full viewport, actual title and navigation screenshot |
| **S06 Master grid** | Spread container \`W,H\`, invisible reference axis \`c\`, unequal domain shares, no physical gutter | Annotated grid overlay on **one canvas**, no hard panel barriers |
| **S07 Negative space** | Space as continuous compositional material, including a **negative-space square** | Compare with same spread with negative space removed |
| **S08 Controlled break** | Shape/word/picture cross-axis interval and layer stack, *why it crosses* | No blocked image subject/word/controls |
| **S09/S10 Live English/Chinese display** | Relationship to shapes **and to each other across the whole spread**, optical size/safe fields | Genuine fonts, correct semantic copy, no missing letters |
| **S19/S20/S21 Artwork and shapes** | Distinguish **geometric 1:1 square** from **square image crop**; \`p=.5/.3\` and source subject masks when relevant | Valid source + native image + spread-wide composition |
| **S22 Full-bleed** | Whether image is full width, truly immersive, or continuous behind other layers | No duplicate image; source and caption accessible |
| **S29 Interaction** | If a square appears/reveals/transforms, what reader task changes and how to reverse | Begin/mid/end/reverse/focus/reduced-motion |
| **S30 Device system** | Wide spread → tablet restaging → vertical phone manuscript | 1648/768/390/320 and real 200% zoom |
| **S31 Quality** | Separate scores for **spread-level originality** and actual deep-reading usability | Single §6A rubric, no parallel scoring authority |

**New specification vocabulary [METHOD]:** \`SpreadCanvas\`, \`CompositionalAxis\`, \`FieldBalance\`, \`CrossAxisObject\`, \`ObjectBeforeAxisShare\`, \`LayerRelationship\`, \`ImageSourceCrop\`, \`SemanticReadingOrder\`, \`ViewportRecomposition\`. These are **manual concepts**, NOT installed CSS variable names, framework APIs or new global tokens.

The R3/R4 crop equations remain intact; they answer \`ImageSourceCrop\`, **one field among many**. No automatic “square image whenever there is a square graphic” rule is permitted.

### 6E.31 R5 acceptance / work status — why this matters for an award-calibre magazine

**What R5 actually delivers:** a strong editorial framework for cross-spread composition, precise 50/50 and 30/70 square geometry, alternate square roles, five-layer construction method, source-aware CSS example, responsive/DOM/keyboard contract and revised existing spec sheets.

**What it explicitly has NOT delivered:** one artistically selected full magazine visual language; four same-content annotated 1648px spreads in production; actual approved typography overlap; device screenshots for S1–S7; Awwwards/Webby/FWA prizes; original issue approval. R5 remains **[METHOD] + [TRIAL]**, not signed-off CSS/runtime.

**Negative cases to reject at the editorial review:**
- Spreading two unrelated pages/cards next to each other and labelling them “digital spread”.
- Using a thick printed gutter, crease, page-curl or ornamental center divider merely to imitate a physical magazine.
- Taking a square image crop as proof that the whole spread has a thoughtful composition.
- Forcing every 30/70 square to become a decorative logo-like widget, or repeating it in every article.
- Making a technically valid layered composition that hides Bodoni letters, the subject's face, a source inscription, or the actual Contents action.
- Using desktop absolute positioning as the mobile layout with smaller numbers.
- Claiming a full-bleed cover represents a complete award-calibre magazine when longform reading and navigation remain unresolved.

**Immediate next research inside THIS SAME book:** develop an evidence-backed atlas of complete digital spreads (not crops) showing cross-axis fields, structural squares, word-image alignment and responsive restaging on real magazine/editorial webpages, then translate the most meaningful **relationships** into original Westside design direction cards. No aesthetic approval until the visual atlas and real full-issue user task are examined.


### 6E.32 GitHub oversized-English typography research → current continuous-spread art direction (R6, 2026-10-22)

**Purpose:** Retrieve earlier **actual Westside research** on English text occupying half a composition, monumental Bodoni letterforms, English/Chinese size relationships, and kinetic type as a spatial/interactive device, then integrate it into the R5 **one continuous digital spread** grammar. This chapter is a **cross-reference + executable editorial decision method**, NOT a second type scale and not a declaration that oversized letters by themselves constitute an award-winning visual identity. The existing official magazine logo SVG is protected; the wordmark does not become editable Bodoni by virtue of this research.

#### R6.1 Recovered project sources — evidence/authority hierarchy

| Exact existing repository source | What it already contains | What is authoritative now | How it informs R5 |
| --- | --- | --- | --- |
| [\`WESTSIDE-EDITORIAL-TYPOGRAPHY.md\`](WESTSIDE-EDITORIAL-TYPOGRAPHY.md) | Twelve real editorial type roles; English Bodoni Moda Roman/Italic/real SC; Chiron Chinese 900/200/400; actual size/leading/tracking and code-owner rules | **[BASE]** Single Design OS token values and current font-family decisions; do not override through a page-level duplicate | Select semantic roles first, then let the *composition* determine a particular oversized arrangement |
| [\`WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md\`](WESTSIDE_MAGAZINE_KINETIC_TYPOGRAPHY_REFERENCE.md) | September 2026 Fond / 池底 \`01020304\` experiment; large type becomes *plane, hinge, foreground/background, page transition and navigation*; Codrops KineticTypePageTransition / SuperfluidLayout / FullscreenLayoutPageTransitions mechanics | **[METHOD]** Recovered experimental research. Not a token owner, approved homepage animation or independently accepted style | Compose a still, effective spread first; any motion reveals a meaningful latent relationship |
| [\`italian-editorial-executable-grammar.v1.md\`](../dore/italian-editorial-executable-grammar.v1.md) | Four experimental geometries: overscale collision; quiet-field isolated fragment; monumental interruption; two-scale encounter. Separates image prompt with **no baked text** from live HTML typography; records 0–100 composition coordinates | **[TRIAL]** Example geometry families, not fixed P2 proportions or global geometry authority | Bring intentional image/letter contact and asymmetrical white space into the **full canvas**, not simply a 3:4 poster |
| [\`editorial-type-hierarchy-lab.html\`](../../static/experiments/editorial-type-hierarchy-lab.html) | Existing Journal/Sites branch-only real-font specimen for 900/200/400 and English/Chinese cover/chapter/article hierarchy | **[EVIDENCE SURFACE]** Demonstrates typographic role and font loading, not artistic acceptance of a complete magazine | Re-use for font/weight/line-break QA; assess actual full spread separately |
| [\`dore-design/new-westside/VISUAL-REFERENCE-SYSTEM.md\`](../../dore-design/new-westside/VISUAL-REFERENCE-SYSTEM.md) | The earlier New Classicism + Editorial Modernism + Archival Print + Doré spatial identity investigation; type as monument, marginalia, image collision | **[ARCHIVE]** Its August font suggestions **Cormorant Garamond and Noto Serif TC are superseded** for this project by Bodoni Moda and Chiron | Preserve its *visual research method and anti-fake-vintage insight*, never reinstate old font family recommendations |
| [\`docs/DESIGN-OS-GEOMETRY.md\`](../DESIGN-OS-GEOMETRY.md) | Existing geometry-measurement workflow and Playwright inspection of winning CSS/bounding boxes | **[QA METHOD]** No extra standalone CSS authority or separate CI required | Measure actual title word boundaries/overlap at desktop/tablet/phone/zoom, rather than guessing from mockups |

**Critical split:** Historical research documents can describe different font families or old styles; **the current canonical token JSON + generated Design OS CSS have precedence**. The earlier found large-type designs are *method evidence*, not licence to reintroduce styles no longer selected. No new font files, CSS root declarations, animation libraries or 12-role replacements are proposed here.

#### R6.2 Monumental English text has at least six distinct EDITORIAL JOBS

A giant serif is successful only if its subject/relation justifies its scale. For the **same actual issue/editorial content**, compare these role candidates:

| Role | What the very large English type actually DOES across the continuous spread | Relationship to an image / square | Reject when |
| --- | --- | --- | --- |
| **E1 / Half-spread claim** | Occupies roughly a chosen **visual half-domain** of the whole canvas, providing scale counterpoint to a human-scale image/Chinese title across the other portion | A 1:1 cross-axis square may occupy 50/50 or 30/70 of **its own** width while the English remains live on one side, but not as fixed paired cards | It appears only as a generic left column next to a right image card; no optical alignment/narrative idea |
| **E2 / Full-spread inscription** | Large words/letter groups span most of the **uninterrupted width**, treating language as the visual architecture | A meaningful image/negative square can cross the lettering plane or remain wholly below/above | Letterforms or the authentic word become unreadable; protected picture content disappears |
| **E3 / Type as image-negative field** | An empty or bright geometric shape is defined by letters and surrounding visual mass; type's whitespace is intentional material | Square may be negative space **without a cropped picture**; historical engraving flows past one side | It becomes an empty decorative rectangle, synthetic clipping effect or useless “luxury” border |
| **E4 / Axis-crossing title** | A complete English word or its line groups traverse the invisible editorial axis; Chinese primary title supplies semantic counterweight, not duplicate decoration | Square/right image may overlap a deliberately selected **nonessential** region of text only if the word is fully decipherable | Loss of a letter (e.g. final **E** in GATE), poor Chinese optical balance or collision with a face/gesture |
| **E5 / Navigating type** | Genuine section / story wording is the **actual** selectable title, capable of linking to Contents/story; interaction follows from a still understandable layout | Can expand or shift into the next reading state, subject to keyboard and static parity | Hover-only title, duplicate nonsemantic huge words, missing destination or motion-only meaning |
| **E6 / Chapter-level marker** | Less frequent massive typographic punctuation marks a transition between four editorial movements (not each article paragraph) | Opposes long quiet body reading and selectively framed Doré witness images | Every page ends with the same overscale word, drowning subject distinctions and body continuity |

**Not all six roles need appear.** Overuse weakens identity. The actual story and its reader task choose a role; a longform reading register can (and generally should) remain quiet. The *square* and the *monumental title* are **independent design instruments**; an excellent spread may include either, both or neither.

#### R6.3 A compositional measuring language: not just font-size values

Separate the measurable terms:

- \`canvasW\`, \`canvasH\`: actual **spread composition container** CSS-pixel dimensions (not automatically the browser window).
- \`refAxisX\`: invisible crossing axis as a proportion of \`canvasW\`; **not** a printed gutter.
- \`titleInkBox\`: actual rendered glyph/ink extents, approximated conservatively from browser text rectangles plus visual review. The DOM \`getBoundingClientRect\` box **includes leading and transforms** and is NOT an exact outline of Bodoni ink.
- \`englishDomainShare\`: percent of compositional space that the English *commands*, distinct from actual measured glyph width. 50% can mean visual gravitational mass, **not** a fixed \`width:50%\` panel.
- \`squareBeforeAxisShare\`: fraction of the *square's own width* preceding the reference axis (R5 50/50 or 30/70 examples).
- \`overlapField\`: spatial relation of image, square and English/Chinese type; named as behind / in front / touches / interrupts / knockout / no-overlap.
- \`safeTitleRegion\`: **all-word and original-artwork subject** safety, including source credit and interaction targets; image-lightness is not automatic safe text space.
- \`typeScaleRole\`: one of current Design OS names, not a private pixel number in every experiment.
- \`mobileRecomposition\`: a new vertical editorial reading composition, not a shrunk screenshot of a giant print title.

**Construct in this order [METHOD]:** (1) verified real English/Chinese story copy → (2) editorial reason for the display/title roles → (3) full-canvas figure/whitespace/typography silhouette → (4) first source-image subject and safe-field check when relevant → (5) actual role-size and line-break from canonical OS → (6) square position independently (if it adds editorial meaning) → (7) real 1648/768/390/320/200% browser proof → (8) optional kinetic state transition, with no CSS-disabled content loss.

#### R6.4 Pairing Bodoni and Chiron — preserve tension, not mechanically linked fonts

**Current [BASE] roles from \`WESTSIDE-EDITORIAL-TYPOGRAPHY.md\`:**

- English lead: genuine **Bodoni Moda Roman 400**, **Bodoni Moda Italic 400** only where semantically relevant; real **Bodoni Moda SC 400** for chosen labels. Neither font is artificially stretched or bolded.
- Chinese primary story subject: genuine **Chiron Hei HK WS 900**, where **actual** primary title role is present; non-body secondary display Chiron **200** at legible sizes, body/functional controls **400**.
- The current semantic scales provide **P0 English hero (72–160px)**, **chapter (52–112px)**, **article (56–128px)** and supporting feature (38–80px) ranges; these are existing OS role bounds, not the height limits of a full-spread concept. Huge 200–300px typography in earlier concept tests is **NOT** automatically an approved OS token. Treat beyond-range giant type as a **local art-direction [TRIAL]** requiring explicit later decision on whether it is scene-specific, with no silent global token expansion.
- The earlier reference's **1.6–2.2× visual English/Chinese hierarchy** is a practical **initial pairing hypothesis**, never a law for a digital spread or a licence to manipulate \`scaleX\`/\`scaleY\` on glyphs. At a dramatic issue opener, optical relationship depends on word length, body of ink/void, actual letter shape, Chiron weight and surrounding imagery.
- A Chinese article title can be visually *smaller yet semantically primary*; do not require an invented English translation. English may be an approved editorial display phrase and Chinese the actual H1. Preserve approved capitalization; no blanket uppercase.
- Real Bodoni SC and ordinary Bodoni uppercase are **not interchangeable**, and an SVG masthead is not the same as a gigantic editable English editorial phrase.

**Why this matters with Doré:** A monumental fine-stroke Bodoni title juxtaposed with a dark engraved scene can deliver modernity through **scale contrast and precise avoidance**, not by smearing serif glyphs across dense hatch marks. Overscale collision is a tested compositional proposal, not a default. The true narrative action of the historical image always outranks a graphic experiment.

#### R6.5 Type-as-spatial-structure: tested method from Fond and Codrops, not copied styling

The recovered Fond memo distinguishes:

\`\`\`text
old UI:       content → generic card → hover decoration → page
editorial:    editorial still composition → latent spatial structure
              → purposeful interactive depth → selected title/story becomes reading state
\`\`\`

**Before motion:** A screenshot of the exact same layout must already read as a complete **magazine composition**; compare one at thumbnail scale *without masthead* to ensure the page is differentiated from a generic portfolio. The title must already be legible; animation cannot repair poorly positioned type or a missing story.

**When motion earns its place:** a genuine story/section title becomes a navigation plane, expands to an issue/section opening, then reveals the actual text and Contents path. It must have click+keyboard+focus, forward/back, interrupted scroll, reduced-motion/static parity, and predictable rendering. The Codrops [Kinetic Typography](https://github.com/codrops/KineticTypePageTransition), [Superfluid Layout](https://github.com/codrops/SuperfluidLayout) and [Fullscreen Layout Transitions](https://github.com/codrops/FullscreenLayoutPageTransitions) are **implementation mechanics only**, not a historical or visual identity source. **Do not add these packages during documentation research.**

**Strong anti-pattern:** copying a Codrops demo color/letter animation and overlaying it on a stock Doré-like picture, or placing bold giant letters behind the official homepage film. Preserve the currently approved homepage full-bleed video, static poster assets and P2 motion. The original Fond prototype was experimental; it was **not** a selected magazine homepage direction.

#### R6.6 Four same-copy comparative proofs — the proper next ART-DIRECTION experiment

**Do not build four different magazines**. Keep the **same** authentic \`The Gate / 城門口的人\` story, official masthead, historically sourced image, complete Contents, and reader route. Change *only the arrangement of typography/image/negative space on the one continuous wide canvas*:

| Proof | Graphic thesis / relation | What to record | Reject when |
| --- | --- | --- | --- |
| **A / Half-spread typography** | English fills a visually weighted 50% domain; Chinese headline anchors the story outside any book-like gutter | Actual Bodoni whole-word ink bounds, image focus, Chinese H1 and first reading action | It merely yields left title + right generic image card |
| **B / Axis-crossing monument** | Full-size word / live type crosses the virtual spread axis, with figure/negative space counter-pressure | No false seam, entire word intact, protected source polygons free | A giant decorative word conceals essential picture/story |
| **C / Type and 30/70 square dialogue** | Square straddles an invisible axis, 30% of *its own width* left and 70% right; Bodoni type and Chinese 900 sit in deliberate compositional relation | Square can be image, negative space or type field; compare against square removed | Square adds no meaning; the relationship looks like three unrelated panels |
| **D / No-square continuous inscription** | A panorama/engraving and live English/Chinese title form a whole-spread composition without a square at all | Is the edition still recognizable? Where is the reading route? | No visual identity without repetitive square branding |

**Do not compare only image ratios**. R5 already explains how square/wide/full-bleed photo frames work; the current test is at the **whole-spread typographic level**. Each proof also includes *article opening → actual mid-article body → source/footnotes → last paragraph/continuation*, so large cover lettering cannot be approved while the rest of the magazine becomes a generic blog.

**QA:**
- 1648×928 / 768×1024 / 390×844 / 320px / true browser **200% zoom**.
- Loaded font face (real Bodoni Roman/Italic/SC 400; Chiron 900/200/400), \`lang\`, actual source copy, role mapping; no \`scaleX\`/\`scaleY\` glyph distortion.
- English full-word integrity at screenshot + **thumbnail**; left/right cross-axis position with actual measured boxes, no source-image subject, figure-caption or interactive collision.
- Visual and DOM reading order; keyboard-controlled title-as-link and reduced-motion static parity; **no intro-scroll trap**.
- Internal Design OS §6A: target **≥18/20, no zeros, no unresolved BLOCK**, plus content, editorial full-issue and technical gates. A successful CI or proof page is not an art-direction award prediction.

**Current conclusion [OPEN]:** This source synthesis establishes an executable **cross-spread English oversized-type vocabulary** but **does not approve any of the four compositions** or establish the Westside magazine's final look. Only documented, independently reviewed specimens can promote a [TRIAL] to an actual design rule.

#### R6.7 Mapping the old research to the SAME 32 specification sheets

| Existing sheet | Recovered rule, no new system | Normalized evidence required |
| --- | --- | --- |
| **S04 / Cover** | Massive text can define the spatial entrance, not a card header | Full-spread still screenshot, exact source, real entry link |
| **S06 / Grid** | Text, image and square can cross a fictitious axis | Grid overlays and actual browser boxes, no paper-gutter |
| **S07 / Negative space** | Letter counterspace and a negative square are active form | Cropped/uncropped and square/no-square comparison |
| **S08 / Overlap** | Overscale collision is purposeful and word-safe | Glyph and face/gesture exclusion QA |
| **S09 / English display** | Bodoni 400, genuine Roman/Italic/SC roles and existing role ranges | Real loaded web fonts; short and long title variants |
| **S10 / Chinese primary** | Chiron 900 semantic primary; 200 non-body secondary, 400 body | Mixed-script optical spacing and real body reading |
| **S16 / Chapter opener** | Scale contrast varies with editorial purpose across four movements | No forced giant title in every movement |
| **S19–S22 / Image & geometry** | Square is one cross-spread object, not image crop requirement | Full source vs framed image vs non-image square |
| **S29 / Motion** | Type becomes a meaningful transition plane if useful | Still state, activation, return, reduced-motion |
| **S30 / Device** | Typography re-authored for a narrower reading task | 390/320 and actual zoom, no meaningless giant-word fragments |
| **S31 / Review** | Distinctive compositional relations matter more than pixel magnitude | Existing rubric, full article + interactive reader journey |

**Source preservation rule:** Keep all recovered documents intact as **source-of-evidence**. Only this single Design OS Editorial Manual can designate final editorial rules. If typography scales genuinely change later, edit the canonical OS tokens with dedicated approval and regeneration—not a new standalone “English giant-type OS”. Do not modify an existing magazine page merely because a once-exploratory CSS experiment demonstrated giant lettering.


### 6E.33 R7 — BEGIN WITH THE EDITORIAL PREMISE, not a font / image / grid (2026-10-22)

**Research question:** How does a magazine establish a recognisable visual style, what matters most, and where should an art director begin? **R7 is a priority correction to all R1–R6 technical research.** The project has acquired many valuable answers about *how to implement a spread*, but those answers cannot decide *what one publication should mean*. The first deliverable is still the **complete, actionable Westside magazine design specification book inside the single Design OS**. This chapter defines its creative foundation and order of operations—not another identity system, site redesign or set of ornaments.

**One-sentence core finding:** **Editorial thesis → issue narrative → authentic subject/media language → visual identity invariants and variation rules → complete reader journey → composition + optical craft → responsive interaction / QA → accepted book specifications**.

This order is grounded in public first-party observations, not a claim to have examined private brand manuals:

1. [Society of Publication Designers / 1:1 art-direction interview](https://www.spd.org/1to1): an editor/designer thinks about **each story and the entire issue, the photographic and illustrative strategies, the pacing of images and stories**, before layout. **Implication:** story/issue rhythm is a first-order art-direction input, not the finishing stage after the cover.
2. [Pentagram / Sight and Sound](https://www.pentagram.com/work/sight-and-sound): film culture and **clapperboard graphic language** produce a consistent system of strong typography, grid, pace contrasts, full-bleed/cropped/circular media and section colors. **Implication:** a magazine's *subject* can become its formal grammar, rather than style being imported from another magazine.
3. [World of Interiors / 2022 archive-based redesign](https://www.worldofinteriors.com/story/print-redesign-interview-hamish-bowles): the archive's editorial clarity and recognizable publishing voice were studied before reshaping the current print/digital expression. **Implication:** discover Westside's own assets and historical understanding before applying old-looking filters.
4. [Kinfolk / Alex Hunting Studio 2021](https://alexhunting.studio/blogs/projects/kinfolk): editorial brand redesign included actual issue grids, typographic text-vs-display optical cuts, complementary family metrics and image pacing. **Implication:** after identifying the publication voice, encode it through precise distinct design *roles*, not one image ratio or a generic large-serif preset.
5. [Webby Awards official judging criteria](https://www.webbyawards.com/judging-criteria/): overall experience integrates concept, content, navigation, visual design, functionality and interaction. **Implication:** a powerful opening still image is necessary but insufficient for an award-competitive *digital publication*.

**Do not misread:** The above are **research methods** and examples; Pentagram's clapperboard is not Westside's metaphor. Monocle / M09 remains **formally REJECTED** as a positive art-direction reference. AWW/WB/FWA aspirations are **internal evaluation goals**, not a claim of official scores, recognition or awards.

#### R7.1 The five top-level creative decisions, in strict dependency order

| Priority | The actual decision to make | **Output BEFORE visual styling** | Failing approach |
| --- | --- | --- | --- |
| **P1 Editorial worldview / 刊物立場** | What does Westside choose to observe and communicate, and **why is that not the same as another magazine**? | Editorial proposition (one sentence), reader's question, authentic source boundary, tone, what the publication refuses to do | “Ancient + modern,” “Italian elegance,” “Bodoni + Doré” as if those were sufficient worldview |
| **P2 Whole-issue dramaturgy / 全卷敘事** | What does the reader encounter, accumulate, discover, question, remember, and finally do? | **Vol.00 beat map** of four movements, 12 desks, 3 interludes, with *explicit reveal constraints* | Twelve independent beautiful cover cards and no act-level progression |
| **P3 Own visual material and point of view / 素材立場** | Which historical/art/documentary image types express the issue honestly, and what are their narrative properties? | Verified source manifest, imagery/luminance/ink vocabulary, near/far time scales, real subject/rights and counterexamples | Generic monochrome engraving, fake ruin photo, universal sepia/archival paper |
| **P4 Invariants + variations / 身份與變奏** | What must make *every different kind of article* recognizably Westside, and which compositions may change by story? | Invariant matrix + allowed variations + conditional reuse rules for giant type, square, video and grid | All pages same square/full-bleed hero, or each story an unrelated skin |
| **P5 Full reader experience / 閱讀體驗** | How does the reader actually move from issue → section → story → evidence → references → ending → next? | Representative complete sequence including a source-grounded opener, quiet middle, end, Contents and mobile re-composition | A beautiful top viewport followed by generic blog cards, tiny Contents or no reading route |

**Decision boundary:** Typography, geometry, motion and microscopic elements are **downstream instruments** of P1–P5. They are not deleted: existing R1–R6 research remains the *technical implementation grammar to apply once the intention is chosen*. Do not turn R7 into a new order to randomly change every font, place a square everywhere or add a wall-endmark immediately.

#### R7.2 Where Westside specifically must start: Vol.00's approved editorial canon

**Source-of-truth:** [\`docs/projects/watch-city-vol00/EDITORIAL_MAP.md\`](../projects/watch-city-vol00/EDITORIAL_MAP.md), status ACTIVE EDITORIAL CANON, four acts **WATCH 4 / WALK 4 / WITNESS 2 / WORSHIP 2** and exactly three **Video + Music** interludes. When conflicts arise, later explicit human editorial decisions supersede this map. **Do not invent completion status or fill missing stories.**

**The genuine subject is not merely “a historical city”;** the reader passes through city, being/people, path, historical material, reflection, practical discipleship, witness, worship and a closing prayer. **The editorial reader arc contains intentional information timing.** Elim must make historical fortifications and siege engineering richly intelligible *before* the theological interpretation arrives in Beersheba; Mizpah raises an editorial question while Beersheba later develops the sustained reflection. **Do not prematurely place the final theological answer in the cover, Contents, image captions or generic brand slogan.**

| Beat / issue role | What the **actual source material** asks of art direction | Spatial/visual translation to test, NOT a required template | Critical failure |
| --- | --- | --- | --- |
| **WATCH / observe and investigate (01–04)** | Mizpah raises the question; Gate ties people to the threshold; Carmel develops construction and historical material | Large historical plates, architectural depth, archive evidence, a question/approach, contrast between city-scale and human scale | Oversize typography or a sepia city picture announces the answer without allowing encounter |
| **INTERLUDE I / Selah** | Sensory passage WATCH → WALK, video and music, not a prose article | Change editorial tempo / a *meaningful pause*; static media fallback and return path | Intro animation with no content function or autoplay trap |
| **WALK / lived path, interpretation (05–08)** | Abraham's leaving city, God's provision, detailed Elim siege material, then Beersheba reflection, followed by Bethel life practice | Path/depth/route, clear diagrams/maps/source notes, high-density evidence gradually relaxing into longer, quieter thought and pragmatic reading | All four stories forced into same square opener; “true watchman” verdict telegraphed before Beersheba |
| **INTERLUDE II** | WALK → WITNESS | Let the text/reader's gaze shift from principle to actual person, with Video+Music | Decorated break that strands navigation |
| **WITNESS / lived people (09–10)** | Brother Lawrence, Huang Shuhua and Jiang Xiuqin as **specific** past/present witnesses | Human presence, truthful archival/person sources, names legibly given at appropriate weight, contextual real sermon/media | Generic AI portrait/“historic-looking” identity or invented biographies |
| **INTERLUDE III / Kinneret** | WITNESS → WORSHIP | An intentional tempo/attention shift that works without moving parts | Animation becomes substitute for true worship arc |
| **WORSHIP / conclusion (11–12)** | Cornerstone, crown, prayer, silence and **official Westside logo** finale | Strong but controlled terminal shift: geometry of alignment → crown → prayer → silence, sparse type and true source | Ornamental crescendo or black/gold “prestige” imitation; invented closing text |

**This is a beat-to-art-direction map, NOT a finalized visual story-board.** The exact image assets, rights, prose and states require further review. The point is that typography scale, shape, whitespace and motion should **vary with the reader's position in the narrative**, under one recognizable editorial identity.

#### R7.3 A possible ORIGINAL editorial proposition — explicit [TRIAL], not signed brand copy

For research review only:

> **A contemporary, image-led publication where the long history of cities, gates, building, defence and human lives becomes a way of observing faith, responsibility and what it means to keep watch.** Visual craft alternates **historical scale and individual presence**, **dark engraved mass and space to read**, **monumental inscriptions and quiet inquiry**. The story may move from city-history evidence toward reflection and worship, but the opening does **not** announce the later theological answer.

This is a **working art-direction proposition**, not a published slogan, new masthead, new Christian doctrinal slogan or a completed answer. It must be checked against **Mizpah, Elim, Esther and Maranatha**, because an identity that works only for *城門口的人* or a Doré source plate is NOT a magazine identity.

**Two paired creative tensions that actually follow from the material:**
- **Scale of history ↔ scale of a person.** City, wall, siege, architecture and 10,000 years versus a walker, one kitchen, an individual witness. This can direct contrast between panoramic or full-spread compositions and intentionally close editorial encounters.
- **Witnessed mark ↔ living movement.** Historical trace and engraving stroke versus present navigation, reading, video/musical interlude and living-world action. This can guide when stillness is authoritative and when digital motion adds meaning.

**Things this proposition does NOT imply:** one city illustration on all covers, square boxes everywhere, compulsory huge English across every spread, false archaeological images, conventional Monocle density, a faux parchment texture or literal flip-book spreads.

#### R7.4 The publication's *recognisable identity* is a relationship system — five stable rules, five controlled freedoms

**Candidate identity invariants [BASE where already approved; METHOD elsewhere]:**
1. **One genuine official publication identity:** protected WESTSIDE WATCH / 《西望》 masthead and site-wide OS; never recreate official logo as a Bodoni title.
2. **One actual type family authority:** Bodoni Moda Roman/Italic/true SC for English editorial roles and Chiron Hei HK WS 900 primary / 200 sufficiently large secondary / 400 readable body and functions, no stretched/generative lettering.
3. **One source integrity rule:** artworks/captions/people/scripture/citation represent actual evidence or honestly labelled illustration; no fictitious content or source.
4. **One reader continuity grammar:** cover/Contents/act/real article/figure+credit/notes/ending/next; the longform does not become a disconnected utilitarian template.
5. **One recurring contrast principle for research:** historically weighty evidence or image juxtaposed with crisp contemporary type, navigability and quiet reading—**not** a universal square, blue plate or giant line of text.

**Allowed variations [TRIAL until art-directed evidence]:** image native frame (portrait/square detail/wide/full), chapter density (monument vs atlas vs reading), cross-spread axis/typographic form, local color from existing OS realm palette, a few purpose-specific geometric artifacts and scene-meaningful interaction. They must all pass consistent subject, accessibility, font, content and reading gates.

**The key test:** Remove the masthead from representative static screenshots. Can an editor identify a **family resemblance across a city history, a personal witness and a worship conclusion** *without* confusing them with three templates? If no, improve the underlying relation of material, type and hierarchy—not the size of the logo or number of repeated ornaments.

#### R7.5 First design-study outputs — before touching full-page CSS or a new hero

The *correct first three editorial-design outputs* are text/data/lightweight diagrams inside the manual, not yet polished high-fidelity illustrations:

**Artifact A — The editorial proposition sheet (one page):**
- Fixed source: Vol.00 editorial map; actual article titles/writing status and provenance.
- Reader: What question does the issue invite, when is historical evidence encountered, what may remain unanswered until Beersheba?
- Voice: Historical precision without museum imitation; theological integrity without slogans; contemporary design without generic tech-dashboard motifs.
- Negative list: falsified source, repeated all-page image, decorative large letters without literary reason, three unrelated panels, Monocle as reference, forced book-turning, contentless scroll effects.
- One **working** visual thesis as R7.3, approved/rejected with decision notes.

**Artifact B — The whole-issue visual score (not yet a final layout):**
- Every one of 12 desk entries + three interludes tagged: principal verb, reader job, real image type, evidence density, reading intensity, expected time/attention, natural entry and exit, authorized sources.
- **No arbitrary numeric values** for absent manuscripts. Leave missing copy as OPEN and avoid implying full longform exists.
- Draw a non-literal timeline of *intensity and pauses*, tracking two dimensions: image/interaction force and text/evidence density. The transitions should make the overall publication feel authored rather than uniformly “premium.”

**Artifact C — The **identity stress test** (three different, real content tasks):**
- **City evidence** (Elim / siege history or Carmel / ten-thousand-year city construction): image evidence, diagrams, source credibility, precise captions and a controlled editorial high-density register.
- **Human witness** (Esther / Brother Lawrence or existing Adullam material): truthful person identity, expressive human focus, rich readable text and media provenance.
- **End/continuation** (Horeb / cornerstone or Maranatha / crown+prayer): stillness, closing structural meaning and source/next interaction.
- Also compare the **actual publication front-matter/Contents**. A brand grammar passes only when *all* these surfaces still feel like one magazine without sharing an identical page arrangement.

The gate to detailed type/shape tuning is **not** how many references have been collected. It is the ability to describe *why each of these genuinely different stories should look different and still look like Westside*. After that, R5 cross-spread and R6 monumental English can be used intentionally.

#### R7.6 Sequence and responsibility: from editorial answer to approved production handbook

| Stage | Creative question | Required deliverable and acceptance | If it fails |
| --- | --- | --- | --- |
| **0 / Source** | What is verifiably already written/owned? | Canonical Vol.00 issue map + manuscripts / rights / current state; no fabricated text | Retrieve missing assets rather than make concept art |
| **1 / Proposition** | What is this magazine about as an editorial worldview? | One-page promise and negative criteria in R7.5 A, editor decision | Rewrite proposition, **not** CSS |
| **2 / Whole issue** | What does the entire publication actually *do* over time? | 12+3 beat/attention map, explicit reveal constraints, real reader paths | Reorder editorial *presentation*, preserve approved canon |
| **3 / Visual DNA** | Which **original** imagery/shape/typography relationships carry the proposition? | Invariant/variation matrix tested across three unlike articles | Reject borrowed aesthetics and generic “modern serif” clichés |
| **4 / Spread systems** | How do full-canvas digital spread, figures, giant type and quiet prose implement the DNA? | Three real content **jobs** in independent, meaningful compositions, with mobile transitions | Return to narrative roles; don't tweak an isolated square |
| **5 / Complete sample issue** | Does it work beyond a magazine cover? | First look, real Contents, full sample feature middle, reference/end, interlude, next route | Finish actual reading/navigation before hero polish |
| **6 / Production detail** | Which dimensions, tokens and authoring rules make it repeatable? | Existing S01–S32 sheets, accepted screenshots and scoped owners, not parallel OS | Mark TRIAL/OPEN; no invented global tokens |
| **7 / Award-quality gate** | Is the *whole experience* distinctive and robust? | Existing §6A 10×2 **≥18/20**, no zero or BLOCK; actual desktop/tablet/phone, zoom, keyboard, reduced motion and real content, independent art signoff | Reject; fix original proposition/visual system/UX as the evidence dictates |

**Key stop-work condition:** If stages 1–3 are unapproved, **do not** spend a round polishing a folio, article end mark, a square crop or a 300px headline as if the brand were finalized. They are optional test instruments, not the starting point.

**Research conclusion / status:** R7 provides a defensible **starting logic** and real Vol.00 editorial application; it **does not prove** a finished brand or an Awwwards/Webby/FWA-calibre magazine. Award quality is assessed on the *complete, actually rendered and readable publication*, not on the number of design references, components, CI passes or iterations.


### 6E.34 R8 — Whole-issue editorial visual score: turn the 12+3 canon into art direction (2026-10-22)

**Question beyond R7:** Now that we know a magazine must begin with editorial worldview, **how do we turn an entire ISSUE into a cohesive, non-repetitive visual style?** This R8 produces the missing operative material: a real 12-column / 3-interlude **editorial visual score** and a **cross-subject identity stress test**. It is **not** an approved finished art direction. R7 defines the start; R8 maps each specific story's visual obligations and exposes where a proposed shared style may fail.

#### R8.1 New evidence: editorial narrative generates repeatable visual grammar

The case studies show three mechanisms, each of which must be distinguished from copying a design:

| Evidence / documented external practice | Design rule actually learned | Westside translation | What NOT to copy |
| --- | --- | --- | --- |
| [SPD, Anton Ioukhnovets art-direction interview](https://www.spd.org/1to1): consider every story's photo/illustration/data strategy, **then** entire issue image/story pacing **before starting pages** | **Sequence and subjects precede layout**; art director designs the reader's changing attention, not only front cover | Score each real WATCH/WALK/WITNESS/WORSHIP role across image scale, evidence density, text concentration and transition | A flatplan as a fixed paper page-count or advertising matrix |
| [Pentagram / Citizen](https://www.pentagram.com/work/citizen): Matter issue “past / present / future” uses light / medium / bold typographic weights to create increasing gravity and a flexible grid where individual stories can differ | A **theme-derived** formal progression can make unlike stories belong to one issue | Use a *semantic shift* from historical city/evidence → individual lived experience → prayer/quiet closure; the exact density need not rise monotonically | **Do not** change Chiron / Bodoni weights in an invented 3-stage ladder; existing site font authority remains binding |
| [Emergence Magazine, first-person studio + Webby feature](https://www.webbyawards.com/crafted-with-code/emergence-magazine/); [Communication Arts](https://www.commarts.com/webpicks/emergence-magazine) | Publication mission of **slow consumption** leads to restrained navigation, longform, thoughtful whitespace and restrained transitions across films/audio/words | Keep longform deep reading quiet even while issue/act opening creates visual drama; video/music interludes make real *state transitions*, not blocking experiences | Environmental/photographic aesthetic, motion plugin, faux sacred atmosphere or extra long scroll with no semantic purpose |
| [Pentagram / Sight and Sound](https://www.pentagram.com/work/sight-and-sound): film clapperboard provides issue-specific graphic grammar and section signposting | **Editorial material supplies a formal language** | Original **city/watch/way/people/cornerstone/prayer** objects may supply direction, alignment and depth, while authentic engravings remain credited artwork | Clapperboard stripes or arbitrary category-color repetition |
| [Pentagram / The New Republic, 2020](https://www.designweek.co.uk/issues/2-8-november/pentagram-redesigns-the-new-republic-magazine-to-match-its-forward-thinking-content/): flexible 12-column editorial grid and distinct dynamic web channel expression | Print master/grid can be **translated into web-specific** story hierarchies rather than pixel duplicated | Wide digital spread for editorial impact; vertical, measured longform for reading; avoid bound-paper imitation | Their font palette, exact 12 columns or print news-weekly density |
| [2026 Webby *Magazine or Publication* award gallery](https://winners.webbyawards.com/winners/websites-and-mobile-sites/general-desktop-mobile-sites/magazine-or-publication) | The award category covers **fully online and companion publications**, not just one special animated article | Distinct visual language must succeed as a sustained browser publication, mobile site, reading/interaction system | Nominations falsely treated as design-system proof or a Westside award prediction |

**Two key deductions:** (1) meaningful progression is **not** necessarily a uniform ramp from quiet to loud—change of attention can take multiple forms; (2) modern digital magazine quality is **not** “a printed double spread on a monitor.” R5's **continuous digital-spread** canvas is a visual design opportunity; no print gutter, no fake pages, no fixed columns; the actual article remains a responsive reading stream.

#### R8.2 The visual-score notation — semantic axes, not fake precision

For each source-authorised item, record four independent **qualitative** axes. These are questions for the art director, not a second evaluation rubric or scored award criteria.

- **SCALE**: what is the viewer's actual subject distance? \`city/world\`, \`architecture/threshold\`, \`human\`, \`object\`, \`interior/quiet\`, or mixed. **Not** an instruction to physically zoom a picture.
- **EVIDENCE**: narrative/media evidence demand, such as \`historical/source-dense\`, \`portrait/person-grounded\`, \`theological close reading\`, \`spiritual/reflective\`, \`not yet sourced\`. **Not** arbitrary 1–10 numeric density.
- **VOICE**: what kind of typography is warranted: \`MONUMENT\` (selected issue/feature encounter), \`ATLAS\` (archive/maps/diagram/caption), \`READING\` (calm longform), \`WITNESS\` (accurate names/profiles/sources), \`SILENCE\` (quiet resolution). These are existing R7/§6D concepts and local editorial jobs, **not separate OS themes**.
- **TURN**: what reader transition is necessary at the item's *entry/exit*: \`ask\`, \`investigate\`, \`enter\`, \`build\`, \`leave\`, \`consider\`, \`practice\`, \`meet\`, \`align\`, \`pray\`, \`pause/continue\`.

The pattern belongs to **real editorial intent**; it never replaces manuscript and photo-source discovery. **Never invent font sizes, durations, photo regions or word counts for missing material.** Status \`CANON\` means the *editorial role* is confirmed, not article completion or artwork clearance. The source of truth is [Vol.00 EDITORIAL_MAP.md](../projects/watch-city-vol00/EDITORIAL_MAP.md).

#### R8.3 The complete Vol.00 visual score — the actual 12 desks + 3 interludes

The below is the **first explicit all-issue art-direction assignment**, not one screen with 15 visual cards. It maintains exact source sequence: WATCH 4, WALK 4, WITNESS 2, WORSHIP 2; interludes after 04, 08, 10.

| Story | Canonical role / authenticated title from the editorial map | SCALE → EVIDENCE → VOICE | Formal *possibility* arising from the editorial task, NOT a template | What must NOT be revealed / faked |
| --- | --- | --- | --- | --- |
| **01 · WATCH · Mizpah** | Issue preface; 〈守望，一座光明的城〉; deliberately short. Completion **OPEN** | city → reader's question → **MONUMENT → READING** | **An unanswered visual question**: city at distance, restrained official publication title, a clear route to the full TOC. A giant English inscription is justified only if it deepens the question | **Do not state** Beersheba's later theological conclusion here; no invented body |
| **02 · WATCH · Bethlehem** | Long-term daily-spiritual-nourishment desk; this issue's original piece **OPEN / recover**, do not fill casually | **TBD actual content** → not yet sourced → **READING provisional** | Brief moment of accessibility / a different cadence; no fabricated illustration or “daily reading” screenshot until source recovered | Do not invent a devotion or borrow generic stock Bible content |
| **03 · WATCH · The Gate** | 〈城門口的人〉 + current Jerusalem/Herod drafts; exact approved article title per editor | architecture → historical event + people → **MONUMENT + ATLAS + READING** | One genuine historical threshold as a spatial axis across one digital spread; giant Bodoni with complete word; source art/people outside protected overlap. Square **may** cross axis 30/70, but may equally be omitted | No cropped-out essential people, false archaeology or generic Square Folio repeated later |
| **04 · WATCH · Carmel** | Feature 〈一萬年的建城禮〉, "build", manuscript source exists | city-scale span → archaeology/time/evidence → **ATLAS → READING** | Large chronological/structural comparison and captioned evidence; one image could become wider than a spread; text diagrams and actual source dates must remain legible | Do not substitute gorgeous architectural plates for precise archaeological data |
| **I · INTERLUDE · Selah** | Actual **Video + Music**, WATCH → WALK; not a thirteenth essay | change of attention → audiovisual → **PAUSE / CONTINUE** | Meaningful rest after broad WATCH, before beginning WALK; static fallbacks + a return path | No scroll-lock filler, no fake prose |
| **05 · WALK · Emmaus** | 〈吾珥：離開一座大的城〉, excerpt/consumer from the separate existing book | city → one person leaving → **ATLAS → READING** | **Distance becomes route**: arrival/departure/dwelling / city boundary can influence spread depth and restrained step navigation | Never rewrite source book, invent Ur archaeology or insert a false Abraham portrait |
| **06 · WALK · Elim** | 〈若不是耶和華看守城池——古代攻城技術史〉, detailed  fortification history before conclusion | architecture/engineering → historical/diagram/source-dense → **ATLAS + READING** | **Technical historical density on purpose**: documented walls, maps, sections, siege schematics and archaeology citations; use cross-spread as a single coherent investigation field, not scattered cards | **Do not preemptively display Psalm 127:1 as completed conclusion** before the narrative has earned it |
| **07 · WALK · Beersheba** | Canonical late theological reflection, title/body **OPEN**; responds to Mizpah/Elim | historical accumulated evidence → extended reflection → **READING → QUIET** | Slow down deliberately; fewer graphics, wider conceptual pauses between authentic thought passages. The previous evidence must remain reachable by reference | **Do not** invent title or pretend theology already written; keep late revelation late |
| **08 · WALK · Bethel** | Disciple formation / ordinary life; issue-specific article **OPEN** | individual → ordinary community/routine → **READING + WITNESS** | Practical legibility: life/training/working and shared practice deserve a human-scale page rhythm, sources/routes to real church/ONE resources where present | No fabricated course or article; don't fill with uplifting stock photos |
| **II · INTERLUDE · 遠方無聲鴿** | Actual **Video + Music**, WALK → WITNESS | reflection → change to observed life → **PAUSE / CONTINUE** | Make reader shift from conceptual/communal practice toward a particular person and source | Not automatically a white dove illustration; image/music rights must be checked |
| **09 · WITNESS · Esther** | 〈廚房裡的人｜你當像飛鳥往你的山〉, Brother Lawrence, existing completed/preserved article | interior/human → authenticated historic witness → **WITNESS + READING** | A **small human/private object** or truthful historical material can carry as much significance as a cathedral; portrait/name/source relationships lead, not oversized civic architecture | No speculative photographic portrait of a historical person; maintain actual attributed sources |
| **10 · WITNESS · Adullam** | Present witnesses 黃淑華 and 江秀琴; linked real sermon/series/timecode/evidence material | two real people → archive/video/source → **WITNESS + ATLAS** | A contemporary evidence-rich *human editorial profile*, with readable names, playback/source passage, source time anchors and chronological context | No generic artificial identity-bearing portraits; keep protected artwork and real sermon evidence |
| **III · INTERLUDE · Kinneret** | Actual **Video + Music**, WITNESS → WORSHIP | witnessed life → contemplative arrival → **PAUSE / CONTINUE** | Release accumulated human stories into contemplation, without losing previous/next link or static mode | No generic “dramatic heaven” transition that invents doctrine |
| **11 · WORSHIP · Horeb** | 〈房角石：整座城由此對齊〉 | architecture/object → alignment → **MONUMENT → READING** | **One physical/conceptual alignment axis** can become a whole digital spread organizing title/structure—unlike a literal ornamental centered border | No fake historical cornerstone imagery or claim a source image proves theological meaning |
| **12 · WORSHIP · Maranatha** | 〈冠冕〉 + closing prayer → silence → official Westside Watch logo/crown | object → prayer / quiet → **SILENCE** | **Measured removal of visual information** as the sequence closes; a real ending, credit and continued reader path, not infinite blank space | No invented closing prayer or completed text; logo remains original SVG; no black-gold luxury styling |

**Five transitions matter more than fifteen identical ornaments:** (a) Q introduced **Mizpah →** historical evidence; (b) WATCH broad history **→ Selah →** WALK relational path; (c) Elim's rich material **→ Beersheba** reasoned reassessment with late theological reveal; (d) Bethel **→ Interlude II →** actual people and life; (e) human witness **→ Interlude III →** worship and silence. Never flatten these into uniform page color/box size.

**Explicit temporal nonlinearity:** The issue does **not** become progressively minimalist from 01 to 12. WATCH can range from question to visually dense feature. WALK alternates journey, highly technical Elim, quiet Beersheba and everyday Bethel. WITNESS can combine intimate people with rich source media. WORSHIP may become quiet, but Horeb still calls for substantial structural weight. The score proposes *meaningful contrasts*, not one descending white-space ramp.

#### R8.4 The **identity stress test** — three incompatible-looking stories, one publication DNA

A style is *actually* coherent if it survives vastly different source tasks **without** repeating the same template. Use three separate story-first composition briefs:

| Test | A / Elim — technical historical documentary | B / Esther — intimate witness | C / Maranatha — closing prayer |
| --- | --- | --- | --- |
| Reader first job | Understand how city defence, siege and human engineering really worked | Know one person and a trustworthy historical/literary witness | Follow actual closing text / prayer / silence |
| Dominant media | Authenticated map, diagram, fortification detail, reconstructed cutaway **clearly labelled** | Attributed portrait/object/interior/source text; don't fabricate sitter | Scriptural / textual final movement; perhaps image absent entirely |
| Main scale tension | Whole city / wall → individual soldier / human limits | Domestic object / lived interior → enduring significance | Architectural foundation / crown → near-empty quiet |
| Type hierarchy | Bodoni English can mark a real concept, while Chinese anchors exact evidence; diagram labels require functional clarity | Chinese 900 for true title + readable actual name/attributions, selective Bodoni, no giant letters obscuring person | Possible monumental single phrase **only** if authentic and semantically earned; eventually allow silence |
| Digital-spread opportunity | One coherent broad investigative diagram/plate across virtual axis, not two isolated poster pages | Asymmetric evidence/person/text relationship, square possible but not compulsory | Deliberate formal removal and alignment; no enforced square |
| Reading | Technically dense captions and evidence, then actual Chiron 400 argument | Intimate longform + notes/sources, media if truly present | Short/long closing content as actually written; honest final links/credits |
| What remains IDENTICAL | **One** official masthead, Bodoni/Chiron roles, citation/source schema, meaningful Contents/next, sound image ethics, controlled editorial contrast | **Same invariants** even though image field smaller and rhythm changes | **Same invariants** even when there is no picture |
| Block condition | Unverified city dates, invented map labels, textbook density made unreadable at 390px, preemptive theological conclusion | Fake/hallucinated person, unsupported quote/source, oversized title overwhelms the witness | Fake closing prayer, misleading crown, lost ending/navigation, empty scroll for “atmosphere” |

**This is the proper identity test, NOT** three versions of *The Gate* with square/wide/full crop ratios. It varies the STORY TASK: empirical historic evidence / human presence / concluding contemplation. A positive concept must have both:
1. **Distinct authored visual silhouette** for each true task;
2. **Clearly readable single-magazine family resemblance** in roles, ink/paper logic, type, source treatment, annotation and transition behaviour without the masthead.

A thumbnail exercise is only one visual screening method, not sufficient evidence of quality. Test an actual **issue Contents** and 20k-character *available* article continuation as well. Where actual content is unavailable, mark **OPEN** and use a synthetic body fixture solely for UX performance, never as published prose.

#### R8.5 What FIRST to draw now: three types of art-direction documents, in order

**Sheet A — full-issue VISUAL SCORE**: this R8.3 mapping, with one view of all 15 items. It is *the beginning of art direction*, before cover images. Show genuine reader attention shape across the issue: scene scale, source density, text concentration, silence and transitions; no invented artist quotation, article length or numeric “emotion score.”

**Sheet B — four visual-MATERIAL specimen families** (collect actual source data first):
- **City / stone / architectural evidence:** proper building/defence artefacts, maps and chronological plans; Doré image when demonstrably relevant and credited, rather than substituting source data.
- **Human / life / witness:** identifiable people with authentic photographs/portrait assets and reliable biographies; intimacy and privacy, not a compulsory “historical face” effect.
- **Word / interpretation / scripture:** actual approved text and references; quiet editorial reading and honest quotation, with selective monumental English when meaningful.
- **Transition / absence / time:** real video + music, accessible fallback/controls; silence and empty visual field count as material only when serving narrative.
No new global theme or palette. All specimens use existing OS source/rights and typography authority.

**Sheet C — invariant/variation PROOF MATRIX** across Elim, Esther, Maranatha and front-of-book: what is shared (publication identity, source, type roles, article route) vs different (image, emphasis, shape, act rhythm). Each proof needs a true page **entry, middle, ending**, not only a Hero or identical three-column layout.

**Before production page styling, the art director must answer five veto questions:**
- Is this image/style chosen because of the story, or because it's already a pretty design asset?
- Can the whole spread work *without* the square, oversize typography or ornamental crenellation?
- Are we designing the current issue's **whole reader passage**, or only adding unrelated homepage-style screens?
- Will a reader of 390px and 200% zoom encounter the same sources, legible text and controls?
- Do Elim/Esther/Maranatha feel distinct **and** related without borrowing Monocle's rejected info-grid aesthetic?

#### R8.6 Explicit downstream constraints and §6A promotion gate

**No style token changes before a family resemblance is observed** across at least the three contrasting briefs plus TOC. Preserve current R5 single-spread composition, R6 existing oversized-English, verified Doré image provenance and R4 crop safety as **available instruments**, not identity first principles. The older approved homepage movie and P2 water/doors remain locked. Monocle stays rejected, historic Westside battlement end mark remains deferred pending original asset recovery.

**Production checklist to promote any visual grammar into S01–S32:**
- source ID & image rights → what actual reader should learn → concept (one paragraph) → full-spread composition → calibrated typography roles → verified caption/notes → real transition into longform → exit/next;
- four viewport/zoom checks from existing manual §6A/R4-R6, programmatic keyboard+reduced-motion and screenshot art critique;
- single Design OS authority and page-owned scoped CSS, no new typography/color systems or styling through side-effectful JS;
- internal ≥18/20 (10×2) and no zero / no unresolved BLOCK **for the whole publication experience**; no new invented scoring scale;
- **If the concept fails**, revise its editorial material relationship or issue rhythm. Don't add a stamp, decorative little wall or an extra cover animation to simulate originality.

**R8 status:** This is a **completed content-grounded editorial visual score and working art-direction testing book section**, **not** selected visual identity, final image atlas, completed 32-sheet production manual, accepted screenshots or an award-quality magazine. Editors must review the whole-issue score and trial proposition before implementing or merging creative layouts.

### 6E.35 R12 — Visual art-direction evaluation after real R11 full-section screenshots (2026-10-22)

**Source evidence:** PR #1352 commit `3af52b6`, browser run [39794561051](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/39794561051), evidence artifact [12432813193](https://github.com/westsidewatch/westsidewatch.github.io/actions/runs/39794561051/artifacts/12432813193). Contains 28 complete semantic sections (seven sections × 1648/768/390/320) **in addition** to viewport-context captures. Manifest: 0 objective defects; **human visual quality still NOT APPROVED**. Unverified: true native 200% browser zoom, 20k–50k canonical copy, provenance/rights, actual Elim atlas evidence, real media for all three interludes, prayer.

**Professional primary-source comparison, as working methods rather than visual imitation:**
- [Pentagram / The New Republic](https://www.pentagram.com/work/the-new-republic): one governing magazine identity can give different feature/departments a content-appropriate visual voice. For Westside: do **not** copy its typefaces or open another font authority; differentiate Gate, Elim, Esther through **editorial material and evidence**, not only different English strings.
- [Pentagram / Sight and Sound](https://www.pentagram.com/work/sight-and-sound): visual language derives from actual film equipment/editorial subject. For Westside, documented source engravings, genuine fortress plans, archaeological plate descriptions, source-true captions, oral testimony and prayer should drive composition rather than ornamentally attached boxes. Never invent an archaeological object to fill a placeholder.
- [Emergence Magazine / About](https://emergencemagazine.org/about/): purposeful slow essays, photo essays, films, multimedia and audio; its medium follows story type. Three Westside video/music interludes should be genuine narrative shifts with sourced rights/subtitles/posters, not empty sample players.
- [Webby judging criteria](https://www.webbyawards.com/judging-criteria/): overall experience includes real content, usable navigation, function and interactivity, not visual impact alone. [W3C WCAG 2.2 Reflow guidance](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html): 320 CSS px responsive reflow and actual text enlargement/200% zoom are distinct evidence obligations.

**Observed identity strengths:** 1648px WATCH front contains a strong oversized typographic engraving interaction; full-issue 12-route/4-movement/3-disclosed-interlude structure is real; desktop Carmel reading distinguishes longform from Elim's functional atlas brief; Esther is quieter in English scale and has genuine manuscript excerpt; smartphone is a recomposed single vertical reading route, not a shrunken fixed triptych. Existing Design OS fonts and source assets remain sole authority.

**Observed art direction deficiencies (not theoretical):** the isolated `identity()` has only one content image `/images/home-opening-engraving.jpg`, with expressly unresolved author/source. Elim's `Evidence 01/02/03` is still a content schema, visually closer to a dashboard than an archaeological source plate. Esther has **no rights-cleared person-related image**, so WITNESS is typographic but not yet a person-led image system. Maranatha intentionally discloses missing final prayer; silence cannot yet be approved as an editorial conclusion. Existing micro-source path captions belong to a development proof and may not be final reader-facing design.

**R11 screenshot-driven rejection:** `text-wrap:balance` removed a final 2-glyph widow by making the **Chinese numbers themselves tear across lines** in 390px and 320px cover teasers: `十 / 二個欄目` and `三 / 個視聽間奏`. The old last-line-only assertion falsely passed, reporting six glyphs. **R12 correction** keeps three intact semantic teaser phrase spans with `white-space:nowrap`, balancing only between completed phrases; Playwright now checks phrase integrity and minimal last-line length. No manuscript rewrite, type stretching, global font override, second CSS authority or new workflow.

**Progress verdict:** a distinctive visual **CANDIDATE** at art-direction prototype stage, but not complete issue photography, source evidence, licensed media or genuine longform publishing; **no awarded internal ≥18/20** because material release blockers and true browser zoom remain unverified. Next critical path: actual source plates for Elim, genuine image/person/media provenance, complete article/footnote reader, then 200% native browser and reread/motion audit. Stop creating new shape/style concepts.


### 6E.36 R13 — Framing as Westside DNA, not image crop (2026-10-22)

**Correction of material audit:** ONE already connects Holy Light Bible Geography maps/routes; Jerusalem 3000 already has a reversible spatial/temporal/evidence architecture; ONE has 241 source-locked Doré originals plus separately versioned ONE Studio images and detailed engraving grammar; Olive's historical/person portraits provide an editorial precedent. The isolated magazine visual candidate has not yet *integrated* those holdings into finished plates. This is an editorial design/attribution bottleneck, **not proof that upstream maps and portrait capability are lacking**. Publicly accessible images still need origin, permission, derivative and credit checks for reuse.

**Verified primary reference:** [Pentagram LDF 2026 — Framing LDF](https://www.pentagram.com/work/london-design-festival-2026), Domenic Lippa/team. This year's campaign has a conceptual *invisible frame* representing the Festival as a platform; it can operate over imagery and without imagery. According to the [official creator interview](https://londondesignfestival.com/stories/framing-ldf-by-pentagram), LDF's existing masterbrand/red stay recognizable while each annual campaign reinvents its visual act. **Learn the mechanism (meaning → occlusion/field → adaptation), NOT copy LDF's red, typography, broken letters or poster silhouettes.**

**Research complements:** [Giorgia Lupi / Data Humanism](https://giorgialupi.com/data-humanism-my-manifesto-for-a-new-data-wold) emphasizes context, nuance, uncertainty and densely layered data-based narrative; [Observable Plot's grammar of marks](https://observablehq.github.io/plot/features/marks) binds data values to spatial positions, geometry, marks, strokes and layers. Treat data as *an editorial material with evidence*, not a corporate dashboard or decorative statistical wallpaper. Neither introduces new runtime/visual authority.

#### 36.1 Framing operator for a continuous web-native spread

**Rejected baseline:** resize one source image to a square with CSS and place a large Bodoni word beside it. This is a crop tactic, not an editorial signature. Existing R5 virtual 50/50 and 30/70 across-spread principles remain; there is **no real gutter and no requirement for independent side panels**. A meaningful geometric field can cross that axis and interact with source image, typographic plane, negative space and artful transparency, **not necessarily show a drawn border**. Every square must answer one reader question: why is this framed / obscured / revealed rather than plainly shown?

| Candidate operator | Contextual meaning | Design failure |
| --- | --- | --- |
| **Evidence aperture** | ATLAS: map/fortification/source plate crosses frame boundary; a source-true caption shows what the highlighted fragment evidences | automatic center crop that removes the source legend, walls, names or provenance |
| **Temporal section** | Jerusalem 3000: same camera/coordinate/object IDs inside and outside one frame; build/ruin/buried/rebuild reveal genuine temporal layers | alternate eras made into four unrelated imaginary model images, inference silently called observation |
| **Portrait foreground** | WITNESS: an attributed historical or versioned engraved person occupies foreground; oversized undistorted English type is partly occluded | stolen/unattributed photography, typographic collision that hides the actual person's name |
| **Typographic registration** | MONUMENT: a frame interrupts unmodified Bodoni glyphs or forms from negative space; supporting text remains readable and accessible | meaningless clipped English letters for trend appearance |
| **Cross-spread aperture** | ONE uninterrupted field across virtual 30/70, 50/50, or other justified composition weights | geometric box turns into a fixed left-card/right-card dashboard |
| **Absent-frame pause** | SILENCE's already strong spatial restraint releases framing pressure at the conclusion | forced ornamental squares or reduced genuine prayer readability |

Original 西望 SVG, the single Design OS Bodoni/SC/Chinese roles and palettes, actual engravings' line direction, genuine copy and one clear reading order remain invariant. Style/subject operations vary. **Absence is part of the grammar: do not repeat a decorative square in every page.** This is a testable technique proposal, not the final named Westside DNA.

#### 36.2 ONE / Jerusalem / portrait evidence-to-artwork pipeline

Relevant local anchors: [ONE map catalog](../../static/one/one-map-catalog.js), [ONE two asset libraries](../../static/one/ONE-ASSET-LIBRARIES-MASTER.md), [ONE original-inspired illustration grammar](../../static/one/ONE-DORE-VISUAL-GRAMMAR.md), [Jerusalem 3000](../projects/jerusalem-3000/README.md), [historical evidence object schema](../projects/jerusalem-3000/evidence-schema.json).

**Acquisition → verification:** select already indexed source/map/portrait or city-ledger object; capture creator, exact source, reusable-license status, version, original geometry, protected labels/silhouette, chronology and sources. Holy Light route map N numbered routes must retain N matching legend entries; externally visible GIF is not a blanket license to edit or distribute. When a source is disputed, label alternatives; do not visual-code fabricated confidence percentages.

**Encoding → original plate:** select a **single editorial question** (“what changed?”, “what location supports the claim?”, “who is the actual witness?”). Map source attributes to line trajectory, spatial contour, timestamp, section, typography, brightness/density, disclosure and layer; generate reproducible SVG/Canvas/vector engraving rather than generic statistic widgets. In Jerusalem 3000, take one existing fixed coordinate/camera, linked source ID, era, geometryState and evidence.status = observed / reconstructed / inferred / disputed; export a plate with those metadata rather than overwrite ledger authority. ONE Studio illustrations stay versioned and must not impersonate canonical Doré originals.

**Composition → reader:** place source plate and title in **one continuous spread**; use purposeful aperture/negative space; preserve genuine caption and source expansion route. Recompose for phones, do not scale down desktop; respect visual subject masks, long Chinese titles, keyboard interaction and real browser 200% zoom.

#### 36.3 Controlled test: from visual idea to proof

Compare four **same-source, same-copy** treatments: A plain centered square crop as negative control; B meaningful evidence aperture with linework crossing edges; C cross-spread 30/70 framing/type/negative-space integration; D temporal change or route evidence aperture tied to actual ONE/Jerusalem records. Test a fifth no-square SILENCE to prove identity survives geometry disappearing. Explicit reject criterion: if the reader learns nothing more from B/C/D than A, it is still only styling.

Observe actual 1648, 768, 390, 320px screenshots, genuine browser 200% zoom, source/legend integrity, historical uncertainty labels, human silhouette/text collision, navigation and motion reversibility. Judge *thumbnail distinction without logo* plus the complete article/longform, not just gallery screenshots. Maintain the single §6A 10 × 2 / ≥18/20 no-block rule without pretending to hold an award jury score.

**Next production test:** compose ONE real, source-attributed Elim/Jerusalem evidence plate with the above pipeline, and compare crop-only versus registered editorial framing. This is RESEARCH/TRIAL, not a new OS, not an approved identity or visually finished asset. Preserve SILENCE, Olive poster assets, homepage and P2 motion.


### 6E.37 R14 — Data becomes composition: precise marks, evidence and spatial memory (2026-10-22)

**Aim:** Move beyond R13's framing proposal. Study how the same actual source should yield three materially different editorial propositions without inventing historical geometry. A beautifully cropped square remains a low-information control, **not** an editorial system.

**Four separate professional sources and their different roles:**
1. [Pentagram / LDF 2026](https://www.pentagram.com/work/london-design-festival-2026) and [LDF's own interview](https://londondesignfestival.com/stories/framing-ldf-by-pentagram): a frame is a meaningful, adaptable editorial verb when it refers to the institution's work as a platform. The same mechanism must carry actual meaning at Westside rather than copy a red typography effect.
2. [Jacques Bertin, original analysis of graphic variables](https://classiques.uqam.ca/collection_methodologie/bertin_jacques/representations_visuelles_info/representations_visuelles_info_texte.html): a point, line or region can be mapped through position, size, value, texture, color, orientation and shape. These are not interchangeable decorations: source relationship and reader task determine the encoding.
3. [Observable Plot official marks](https://observablehq.github.io/plot/features/marks): data visualization can layer line, dot, area, text and rule as separate graphic marks; web-native native SVG can apply the **method** without introducing a second chart library or visual authority.
4. [London Charter Principle 4.4](https://www.london-charter.org/documentation.html): computer-based heritage visualization must show whether its subject is surviving material, evidence-based restoration or hypothetical reconstruction, and explain its uncertainty. A gorgeous drawing does not elevate an inferred coordinate into an excavated fact.

#### 37.1 Verified project datum: one real origin, not imagined Jerusalem archaeology

Canonical source: [Jerusalem 3000 David–Solomon landscape](../../preview/jerusalem-3000/data/settlement/david-solomon.v1.json), project schema j3k.david-solomon-landscape.v1. It already has:
- royalCity.davidWall: **7 point entries**, the first point repeated to close a hypothetical defensive outline. This is an internal interpreted coordinate chain in a spring-relative local frame; **NOT surveyed historical wall segments**.
- royalCity.northernWall: **4 point entries** of an additional northern hypothetical segment, with a Solomon-stage display role; the exact ancient fortification remains disputed.
- royalCity.spatial.nodes: **14** scheme-level entries for connectivity, including named entrances, spring, courtyard and northern connections, with many calculated from inferred gates. It is **not** a field-survey road network.
- royalCity.spatial.edges: **13** staged connections; “13” is a code/network count, not a historical count of roads or military entrances.
- The source warning expressly says royal circuits and monuments are unverified, the spring is an approximate modern map point, and extrapolated buildings and roads are illustrative. The whole Jerusalem 3000 project already carries observed/reconstructed/inferred/disputed status and a historical lifecycle system. Its authoritativeness is **in its honesty about what is and is not known**.

This is a suitable FIRST COMPOSITION TEST because the data are accessible and provenance-coded; it is NOT sufficient to publish a finished Elim article on ancient military construction, or a definitive David/Solomon city diagram. Do not manually re-copy the data into a magazine geometry array. Use an existing URL/source adapter and record the exact source revision in any exported plate.

#### 37.2 Five-stage design translation: from data attributes into editorial marks

**1 / Reader question.** Ask a single clear question, e.g. “What changes when a hypothetical northern wall is added to the same source frame?” Reject the non-question “How can this map look cool?”

**2 / Reference frame.** Preserve the source's local coordinate axis and equal unit scale, with one fixed orientation, stable origin, named era and source revision. Never squeeze north-south or east-west distances solely to fill a pleasing square: geometrical aesthetics do not authorize distorted measurements. Wide spreads can change crop and axis placement, but not data semantics.

**3 / Map the source's evidence state to mark behavior.** The placement of an element encodes source coordinates; line continuity encodes relationships; dash/line texture encodes inferred contours; opacity can subordinate contextual alternatives; captions explicitly name status. Historical scientific uncertainty must NOT be implied solely by a pretty gold hue, arbitrary blur or percent without supporting probabilities.

**4 / Editorial composition.** The historic line can cross a registered window, overlap **behind** the full-size English Bodoni type field, or be read as an annotated threshold in a continuous digital spread. The square may sit 30/70 across the virtual composition axis, but the line must keep actual spatial relationships. Do not sacrifice map labels, original legends, source statuses or subject masks to force 1:1 cropping. Chinese heading, CJK dates and real captions remain readable; type glyphs may be occluded deliberately, never stretched.

**5 / Responsive edition.** Desktop treats the whole viewport as one editorial spread without a physical page spine. Tablet rebalances editorial weights; phone presents a re-composed sequence of source diagram → annotated claim → actual prose/source disclosure, rather than a tiny desktop spread. SILENCE's uncluttered conclusion remains a useful no-square identity stress test.

#### 37.3 Same source, three mandatory trials — exactly what should differ

| Mode | Graphic construction using the unchanged David–Solomon source | What the reader learns | Reject if |
| --- | --- | --- | --- |
| A / Crop (control) | Same source polyline seen through an ordinary 1:1 media viewport | Little about full wall or north extension; intentionally exposed limitation | Treated as the distinctive solution merely because image is square |
| B / Evidence aperture | Keep every polyline segment visible; registered square region selectively highlights the relevant part while history lines continue across virtual canvas; masthead/English hierarchy builds negative-space pressure | The frame is a *focused argument* while the source remains continuous | Decoration obscures reference, distorts coordinates or makes selection seem like observed archaeological evidence |
| C / Time section | One unchanged coordinate/camera, David hypothetical outline and Solomon hypothetical northern extension switch/reveal while the source, captions and caveat remain fixed | An explicitly modelled **difference between two interpreted stages**, not absolute archaeological proof | Two unrelated rendered city postcards, false dates/lineage, unexplained fade or irreversible state |

For each output create a plate record with source URL and revision, original extent, era state, interpreted geometry classification, source terms, shown legend and changes applied for editorial composition. A fourth *no-square* control, SILENCE, verifies that the publication identity is not dependent on the presence of a geometric motif.

#### 37.4 Independent proof and creative sign-off

- Production only within the current PR #1352 source owner and existing studio; do not touch homepage/P2/ONE/Olive or modify Jerusalem's source model.
- Test same copy, same source, same ink/font authority at 1648x928, 768x1024, 390x844, 320x720, PLUS native browser 200% zoom (a 824px proxy is not proof). Save full-section images, not only centred viewport crops.
- Verify the line source and source-stated uncertainty remain accessible and correct at A/B/C; for C forward/back toggling is reversible, keyboard-accessible and respects reduced motion.
- Independent optical critique: (a) is the composition recognizable as Westside with the masthead hidden? (b) does frame placement clarify a historical claim instead of decorating it? (c) does negative space remain intentional? (d) is the Chinese/English hierarchy distinctive without sacrificing historical legibility? (e) does the strongest frame make a later frame-free section more powerful?
- A source-derived plot alone is NOT an award-grade feature. Full real article, archival rights, finished visuals and alternate disputed interpretations still need editor review. Keep final art gate under **one Design OS §6A ≥18/20, no block, no faux prize score**.

**R14 conclusion:** The first real source for a composition experiment has been identified and audited in detail. The proposed A/B/C drawing method is now sufficiently specified to implement without gathering new historical source material. The live magazine visual has NOT changed in this research pass; this section is **DESIGN RESEARCH / READY FOR PROOF**, not an invented passing screenshot or completed interactive city atlas.



## 6F. WESTSIDE WATCH / 西望雜誌視覺規範書 — MAGAZINE STYLEBOOK, Working Edition 01 (2026-10-22)

**文件性質：[WORKING NORMATIVE BOOK / EDITORIAL ART-DIRECTION DRAFT]**。本章是西望雜誌的**製作入口**；先回答「此刊物應如何設計」，再由研究庫 §6D–6E 提供源由與驗證方法。此章是既有 **Westside Design OS Editorial Manual 的一部分**，不是第二套 Design OS、另一份獨立品牌手冊、新 CSS 權威、已簽收的藝術風格，也不是新 CI。已批准的全站 token／字重／原始 LOGO、既有稿件及出版順序皆不可由本章自行改寫。

**地位判讀：** **LOCKED**＝已由現有 OS／作者決定的事實及禁止事項；**STANDARD**＝本輪訂出的編輯製作準則，可直接拿來製作和審稿，但不是已驗證的最終美術作品；**TRIAL**＝可實驗的比率、構圖或視覺語法，須有實際圖版和簽核才能升級；**BLOCKED**＝出版／併入正式網站前必須補齊。所有下方相對幾何值都是 **TRIAL**，不能暗中變成全站 token。既有 §6E 的 32 張規格單（S01–S32）保留為**製作核查清單**，但本章是設計決策入口，避免工程師在研究文庫內猜測哪一輪意見有效。

### 本書的閱讀路線／操作索引

| 先要解決的設計問題 | 直接閱讀 | 交付物 |
| --- | --- | --- |
| 為何一眼是西望，而不是一般雜誌？ | 6F.01–03 | 一句出版命題 + 六項身份檢查 |
| 用什麼字、色與跨頁規則？ | 6F.04–06 | 既有 OS role 對應、版心決定與理由 |
| 要設計哪個母版，圖像從何而來？ | 6F.07–09 | 實際作品的 page anatomy / source manifest |
| 四樂章讀起來節奏是否完整？ | 6F.10–13 | 讀者路線、真圖說、可用長文與影音狀態 |
| 如何由一張規範真正交出網頁？ | 6F.14–15 | Art Direction Production Card、跨裝置實景與批准紀錄 |
| 怎樣追溯本書參考與修訂？ | 6F.16；另見 6D–6E | 來源核對、修訂依據、沒有複製其他雜誌版式 |

**第一輪製作順序：** 依本章 §6F.14 為 The Gate／Elim／Esther／Maranatha 分別填寫真實內容的 Production Card → 每張卡只選一種最有理由的視覺聲部 → 使用已有 owner 檔案試排 → 檢查真實桌面與手機截圖 → 記錄拒絕/保留 → 只有經簽收的做法才允許從 [TRIAL] 升級。**不要從 R15 開始增加另一章研究而不產出實際頁面。**

### 6F.01 封面內頁 — 出版身份與一句話的設計命題 [STANDARD]

**出版對象：** 為願意深讀的人製作的、以歷史、城市、聖經、人物與當代生命為題的中文主體／英語輔助的數位雜誌。**敘事承諾：** 讓讀者從可驗證的世界與人的真實生活出發，經過歷史與信仰的思考，進入見證、敬拜、禱告與安靜。不是將歷史資料當作預設答案的裝飾；Vol.00 特別遵守先陳述人的建造／保護之努力、再引出神學思想的敘事節奏。

**原創設計主張（工作描述，非新刊物副標題）：** **古典的記憶，以當代的尺度與空間說話。** 古典來自真實多雷刻線的視覺語法、城牆／地圖／文獻與人類歷史；當代來自極大展示英文字、粗細有張力的中文、跨越虛擬中心的無縫雙頁、關係鮮明的負空間與精確控制的資料轉譯。若移去西望刊名，只有「淺棕底＋復古圖片＋大字」，就是失敗；西望身份必須留在圖文**關係**與整期敘事中。

**西望應有的氣質：** 有思想的雄偉；克制而深刻；史料可信；現代而不時髦；靈性與人的處境相連；安靜不等於空洞。**反例：** 黑金奢侈品皮膚、均等卡片堆疊、仿古裝飾畫框、全站同一三欄、為炫技而截斷的字、虛構古蹟照片、所有段落都「史詩般」巨大、讀者找不到正文。

**品牌常量：** 原始西望 SVG；Design OS 字體與既有語義色；可靠來源與圖說；本期「四樂章／12 欄目／3 個 Video + Music 間奏」；對長文的尊重。**可變量：** 開場鏡頭、是否方框、影像比例、英文字的佔比、動線、跨頁偏移、亮暗與密度。沒有任何單個方塊、版式或人物刻線可以定義整本雜誌。

### 6F.02 出版物的閱讀架構與固定編輯角色 [LOCKED + STANDARD]

**唯一內容權威：** [Vol.00 Editorial Map](../projects/watch-city-vol00/EDITORIAL_MAP.md)。封面（Cover）→ 編輯命題（Issue thesis）→ 可使用的真實目錄（Contents）→ 樂章／章節開頁（Movement / Opener）→ 文章入口（Article lead）→ 連續長文（Reader）→ 圖版及證據（Plate / Evidence）→ 註腳及來源（References）→ 本篇結束／下一篇 → 最終祈禱／安靜／刊物識別。這是**閱讀角色鏈**，不是每篇都必須使用全部視覺模組。

**不可改的 Vol.00 拍子：** WATCH 01–04，WALK 05–08，WITNESS 09–10，WORSHIP 11–12；Selah、遠方無聲鴿、Kinneret 分別作為樂章間 Video + Music，且不計入 12 篇。不要猜補 Bethlehem、Beersheba、Bethel 的未確定稿件。不要讓 Beersheba 要回答的神學命題在卷首或 Elim 提前變成招貼口號。

| 編輯角色 | 一眼必須讀出 | 主視覺行為 | 不可省略 |
| --- | --- | --- | --- |
| Cover / Threshold | 這是哪一期、最值得進入的命題 | 可在超大 English 及刻線／城市之間造成強烈對照 | 原 Logo、主題中文、通往目錄的真實連結 |
| Contents / Navigator | 我要去哪裡？進入的是哪一篇？ | 清楚可掃讀的序號／篇名／四樂章分組 | 12 個真正目標、未刊狀態誠實披露 |
| Movement opener | 下一個樂章與上一個有何差別？ | 尺度、節奏、光／材質可轉折；不必都有方框 | 樂章名稱、閱讀次序與返回路徑 |
| Feature / Historical Atlas | 此圖／資料證明什麼？還有哪些未知？ | 圖片、建築剖面、年代／證據線能成為構圖主角 | 原件來源、證據分類、圖說、放大途徑 |
| Person / Witness | 誰在說話？什麼是真實見證？ | 人物尺度、視線、手勢、刻線與文字共場 | 真實姓名、可信來源、可辨識的身份 |
| Article Reader | 長文閱讀是否安靜、舒服、不走失？ | 明確的文字版心，圖版恰當打破節奏 | 原稿權威、段落、章節、註腳／引用 |
| Interlude | 為何由此樂章進入另一樂章？ | 影片＋音樂構成一次有意義的轉場 | 控制、poster、可播放性、出處、靜態替代 |
| Closing / SILENCE | 思考在哪裡收束，何處留給讀者？ | 留白、節制、最終原文與身份回歸 | 不虛構祈禱，不以空白補缺稿 |

### 6F.03 視覺 DNA：固定六條關係，而不是固定六張畫 [STANDARD]

**DNA-01｜重與輕：** 有襯線大英文（Bodoni Moda 400）與厚重中文主題（Chiron Hei HK WS 900）形成清楚的光學重量差；英文可佔大畫面，中文保留內容的決定權。中文次標採 200，必須夠大才承得住；閱讀文字 400。

**DNA-02｜時間與材料：** 古典不是 Sepia 濾鏡，而是真正帶有年代、史實與圖版脈絡的材料。來自多雷的刻線須尊重構圖、交叉陰影、光源與畫面密度；來自資料庫的線段須保留真實／推定界線。

**DNA-03｜一張無裝訂中縫的數位跨頁：** Desktop 可以把單一圖像／方框／巨大字體配置跨越虛擬中心 50/50、30/70 或其他必要比例。視窗左右是視覺節奏，不是固定兩張紙或三個獨立卡片；幾何能延伸或被切斷，資訊仍有連貫閱讀路徑。

**DNA-04｜空白承擔敘事：** 空間用來建立時間、焦點與沉默；一個好用的空白要能回答「讀者在等待、比較還是安靜？」不為填滿畫面放裝飾小標。SILENCE 的既有空間結構是保留的正面資產。

**DNA-05｜內容生成構圖：** 地圖線穿過框、人物站在字前、城牆時間層交替顯現、引用在視線盡頭收束——是由內容物件的關係產生，而不是每篇套一張 square image。任何框必須說得清「它讓讀者多看懂了什麼」。

**DNA-06｜四種聲部同屬一本刊物：** MONUMENT（少量關鍵開場、英文字與刻線構成姿態），ATLAS（證據及時空圖版帶動布局），WITNESS（真實人物／人聲／姓名優先），SILENCE（安靜的結語）。另有 READING 作為所有樂章共同的長文閱讀狀態；聲部是**功能**，不是新皮膚、第二色盤、第二 OS。

**反向驗證：** 封住 Logo，選同一本期刊的 The Gate／Elim／Esther／Maranatha 四頁：是否互不雷同，卻能感到一致的閱讀態度？若只換文章題名或同一幅古典圖片仍成立，身份不合格。

### 6F.04 字體章：角色、大小權威與中英文張力 [LOCKED + STANDARD]

只調用 [單一 OS tokens](../../design-system/tokens/westside.tokens.json)、[中文與英文十二角色版面表](WESTSIDE-EDITORIAL-TYPOGRAPHY.md)、當前 Design OS CSS。**以下變量為現存 runtime 入口，不是新定義：**

| 版位角色 | 中文/英文規定 | CSS 消費方式 | 完稿檢查 |
| --- | --- | --- | --- |
| Cover/Issue 英文超大字 | Bodoni Moda Roman **400**；可最大至半版，字母本身參與構圖 | --ws-type-display-en + --ws-type-scale-editorial-hero-en | 字形不拉伸；完整詞仍能被辨識，手機重新編排 |
| 主中文大標題 | 昭源黑體 Chiron **900**，內容上的主標才用此身份 | --ws-type-display-zh + --ws-type-scale-editorial-hero-zh / editorial-article-zh | 長短題與標點不得相撞；非全部 H2 都用 900 |
| 英文章節／內頁標 | Bodoni Moda **400**，語義合宜時用 Roman/Italic | --ws-type-scale-editorial-chapter-en / editorial-article-en / editorial-feature-en | 不為平衡畫面而橫壓字體 |
| 中文章節與支持標 | 非真正主標的中文編輯標題 **200**，應具足夠尺寸 | --ws-type-scale-editorial-chapter-zh / editorial-subhead-zh | 不使用 200 製作小注、圖說或控制 |
| 中文引子／署名／目錄 | 對應的 standfirst、byline、contents 角色 | --ws-type-scale-editorial-standfirst-zh / editorial-byline-zh / editorial-contents-zh | 必須能和主標、正文分層識別 |
| 中文正文 | 既定 Chiron **400**，不是標題樣式 | --ws-type-reading-zh + 現有閱讀尺寸／行距 | 真實文章長時間閱讀、標點與字距自然 |
| 英文 Small Caps | 真正 Bodoni Moda SC，不是 CSS 假小型大寫 | --ws-type-display-en-sc | 只用在合適的刊物識別、folio、輔助標籤 |
| 引文與經文英文 | Bodoni Moda 原生 Italic | --ws-type-display-en 的原生 italic face | 經文原文及出處可查；不可與一般 UI 相混 |

**排版作業規則：** 先固定正文讀法，再處理大字；先排中文的真實篇名，再決定英文展示形；字體最大化不等於縮小內文。禁止長標題遮蓋圖例、人名、經文、可互動控制；孤行、中文不可拆分詞、英文標點與光學對齊需逐個 1648／768／390／320 實測。R11 曾發生「十二」及「三個」被斷開，此類錯誤必須作為正式拒絕案例。

**規範示意（使用既有變量，局部 owner selector 範例，不准複製到全站 :root）：**

~~~css
[data-ws-scope="journal"] .edition-cover__en {
  font-family: var(--ws-type-display-en);
  font-size: var(--ws-type-scale-editorial-hero-en);
  font-weight: 400;
  font-stretch: normal;
}
[data-ws-scope="journal"] .edition-cover__zh {
  font-family: var(--ws-type-display-zh);
  font-size: var(--ws-type-scale-editorial-hero-zh);
  font-weight: 900;
}
[data-ws-scope="journal"] .edition-reader {
  font-family: var(--ws-type-reading-zh);
  font-weight: 400;
  max-inline-size: 38em; /* TRIAL：以實際 CJK 字數重測，不是 token */
}
~~~

### 6F.05 色彩／材質章：一套色彩權威與受節制的用色 [LOCKED + STANDARD]

只從 Design OS 使用 Paper / Ink / Water / First Light / Olive / Harvest / Crimson 等既有 token 的對應語義，不再發明「西望香檳金」「西望暖紙白」等競爭性全球值。紙面留白不是「咖啡色背景」，墨色不是只能是純黑；材質要服務刻線閱讀、圖像地位及字體對比。

**建議的作品規律 [STANDARD]：** 多數長文採一種主紙面與主要墨色；必要時加入一種輔助的語義色或刻線層，優先由圖像與排版創造層次。刻線依靠明度與線性密度而不靠統一金色濾鏡。圖示中的金色不可默認代表較高歷史確定性。雜誌頁不須重現首頁七色帶；各版塊可在單一 OS 下具有不同語義色，但不是七個彩色方塊固定羅列。

**禁則：** 全站黑金奢侈品風、任意透明低對比圖說、刻線／紙面重複貼滿造成懷舊壁紙、因背景深色而犧牲可讀性。正文字色須有足夠對比；材質需可退化為純色背景。

### 6F.06 網格／雙頁章：以角色選比例，不以欄數選網頁 [STANDARD + TRIAL]

先決定**內容主場**（圖版／文字／人物／資料）與**讀者下一眼**，再在一整張數位畫布上安排接觸、分離、遮蔽、對角與留白。編輯中心線只是一條可穿越的軸，不是印刷裝訂線；能跨 30/70 的方形，也能跨 10/90 的標題或完整滿幅城牆圖。

**三種可合法使用的網格行為：**
- **秩序場：** 目錄、長文及引文/圖說依穩定 baseline、文本 measure、索引建立可信的閱讀秩序。
- **主題場：** 封面、樂章開頁與資料圖版可用不等寬區域、多軸網格；每處破格必須有明確內容原因。
- **連續跨頁場：** 圖／字／方框等可以是一個橫貫兩側的物件，文字閱讀仍有正確 DOM 次序；移動裝置轉成單欄先後關係。

**操作控制 [TRIAL]：** 初次構圖可用 6/8/12 個隱形工作軌，不能強迫平均；文字閱讀欄寬以真實 CJK 字數測，桌面先比較每行約 30–40 個漢字、手機約 17–28 字；邊距桌面可先考慮 3–7vw、手機 16–24px，均需依真實裝置及閱讀質量修正。這些不是批准的 CSS 全局數值。所有 grid break 必須寫下「原秩序 → 偏移行為 → 讀者收益 → 小屏的重排方式」，否則退回一般版。

**版面允許：** 方框遮蔽圖片、文字站到前景、刻線穿過框、框甚至完全消失；**版面禁止：** 把整段史料或地圖圖例遮斷、三張孤立卡片假裝成跨頁、給每篇同一套不等三欄、手機按比例縮小整本紙刊。

### 6F.07 五種母版：給編輯使用的「構圖規則」，不是五張模板 [STANDARD + TRIAL]

| 母版（role） | 操作次序 | 桌面端空間決策 | 手機端的編輯秩序 |
| --- | --- | --- | --- |
| P1 封面 / Issue identity | 真主題 → 原 SVG → 一幅有權威的圖／媒體 → 大英文 → 中文主標 → 目錄入口 | 可壯觀、可跨頁；主標保持明確語義 | 刊名／主題 → 視覺作品 → 中文及目錄；不保留無效的三欄 |
| P2 索引 / Contents | 12 個確定篇目與欄目排序 → 狀態 → 導覽 → 次要編輯資訊 | 行列、對開可靈活；第一任務是找得到篇章 | 分組單欄／必要的跨欄、完整標籤及返回 |
| P3 敘事特寫 / MONUMENT | 一個核心命題 → 英文展示字與真實圖／刻線建立主從 → 圖說 → 正文 | 可容許大字跨中心；不得吞沒文章 | 分成有意義的前景圖、標題、引子及可讀正文 |
| P4 資料圖版 / ATLAS | 實際來源 → 讀者問題 → 資料圖形 → 證據分類 → 取景框 → 圖說／正文 | 城牆、地圖、年代圖可作完整構圖骨架；容許一張方框跨中心 | 優先清楚圖例、縮放／替代文字、資料來源；不是縮略版 |
| P5 人物與結語 / WITNESS → SILENCE | 真實人物／證言 → 肖像來源 → 視線及文字遮蔽；結語依內容退至空白 | 人物跨字，或全頁不出圖；留白必須有時間與主題理由 | 身份、見證、全文；結束節奏不應靠多次空滾 |

**同一篇文章可先使用 P3 開篇，轉進 P4 證據，回到平靜 Reader，再在結尾使用一個小幅引文。** 每張母版是可以拼接的編輯語法，不是只准一張的固定模板；版型之間的過渡和差異才使刊物成熟。

### 6F.08 圖像藝術指導章：六個可生產的圖像家族 [STANDARD]

| 圖像家族 | 何時使用 | 製作與識別方法 | 確認工作 |
| --- | --- | --- | --- |
| Original Doré | 聖經事件、具有真實原作背景的視覺譜系 | ONE 的 241 幅多雷原作只引用已核對 ID；保留原圖／不冒充其他創作 | 原作者、圖版 ID、出處、來源完整 |
| ONE Studio / Doré continuation | 可用原作繪畫語法改寫的指定敘事 | 使用已存在的 Studio 版本資產、hachure／明暗／主體階層；新作品另立 truthful provenance | 不得冒充原多雷；保留版本、用途和批准 |
| Archaeology / Historical atlas | 真實的城牆、路線、建築、地理史料 | ONE 聖光地理、耶路撒冷 3000 年、合規公開資料；原圖與衍生編輯圖分別標註 | 來源、授權、座標、時間、observed/reconstructed/inferred/disputed |
| Data-derived drawing | 來源自地形、年代、路線、事件與圖例 | 原始 ID 不變、幾何比例不虛構；位置／線型／亮度／疊層有明確資料含義 | 畫面可追溯到同一來源，不製造假的精度 |
| Portrait engraving / witness | 歷史人物、公開講道者與見證故事 | 橄欖山驗證過的單色人物刻線方法；前景可遮大字，但人物權益與相貌可信 | 歷史照片與 AI 詮釋肖像分開標示，十二講員海報資產不動 |
| Film + sound | 三個規定間奏、具來源的動態敘事 | poster-first、播放控制、音訊不自行響起、字幕與靜態摘要 | 有有效可播資產及權利，否則明確寫待發布 |

**每張主圖都要有四個版本角色：** Archive/source（完整原件）、Plate（設計圖版）、Reader fallback（小屏或 reduced motion）、Credit（作者／日期／許可與來源）；並非必須產出四張不同圖片。**圖說最低四問：** 這是什麼？來自何處？哪一年／時代？是確證、重建還是藝術詮釋？只有「Evidence 01」或「古典圖片」的佔位符一律不能正式發表。

### 6F.09 封面、主標、圖版、長文的實際排版語法 [STANDARD]

**封面：** 必須有一期的「主要命題」；可以用一張或多幅圖、字母巨大、刻線與方框協同，但**不把字母放大當作命題**。原 Logo 不可重新繪製；Big English 與重中文應互相形成受力，避免像大型簡報。讀者三秒內須看出 WESTSIDE WATCH、當期主題、從何進入。

**圖文組合：** 圖可以比正文寬；應標示其論述任務（補充、反駁、定位、比較、情緒轉折）。超大圖能出現一次高峰，之後必須回到可讀的正文。圖像的核心主體安全區、歷史文字、比例尺、圖例不得因藝術裁切消失。

**長文：** 只有一個真實 canonical manuscript consumer；主標、引子、署名與正文之間界線清楚，正文使用連續語義段落，適當小節標、腳註、引圖、引文、經文、參考資料。長文沒有必要模仿雙頁固定分頁；讀者可以自然捲動，再在特定圖版返回視覺高峰。**不要用 20–50k 假字數聲稱文章已發布**；必須用真稿及具代表性的長文測試。

**人物：** 面部、手、肩、眼神等必要特徵優先；英文大字可以部分藏在人物背後（正如橄欖山已建立的方法），但姓名與內文不得被遮至無法辨認。人物不能變成任何現代 UI 卡片的圖片頭像。

**SILENCE 結尾：** 保留既有寧靜空間，不強迫套「框」。Horeb 房角石 → Maranatha 冠冕 → 經核定禱文 → 安靜留白 → Logo／Crown 的順序是 Vol.00 的編輯決策。缺正式禱文不能生成假禱文補空間。

### 6F.10 聲部與整期版面節奏 [STANDARD]

| 部分 | 主要閱讀動詞 | 主要聲部與密度方向 | 明確避免 |
| --- | --- | --- | --- |
| WATCH | 看見、尋問、進入城中 | MONUMENT 引入議題，The Gate／Carmel 可展開宏大的城市空間與歷史密度 | 提前劇透整卷最終神學結論 |
| WALK | 出發、建造、守護、考察、思考、操練 | ATLAS 史料詳實；Emmaus／Elim/Bersheba/Bethel 功能不同，不能只換圖 | 所有文章都用同一張城牆，或用圖表代替神學思考 |
| WITNESS | 遇見、聆聽、辨識 | 人物、第一手話語、姓名／證言，視覺可拉近距離 | 模糊的人物來源、無關的復古人像 |
| WORSHIP | 對齊、回應、禱告、安靜 | SILENCE 不需再競逐最大標題；讓負空間與真實祈禱形成結尾 | 把留白誤當尚未製作、無意義的捲動 |

三個 Video + Music 間奏各自明確標註樂章轉變，不是三次重複同款的全幅播放器。期刊的設計不是單頁漂亮程度的總和，而是**閱讀強弱與注意力的作曲**。

### 6F.11 互動／動畫：有內容意義才允許 [STANDARD]

- **入場／開門：** 必須守住首頁與 P2 已有資產與卷軸狀態；西望規範不是授權把流動洋流或開門動畫改成其他轉場。
- **內容揭示：** 動效可從真實的時間、路線、城牆分層、人物前景產生；每次 motion 都必須有一個清楚的靜止閱讀狀態及退回動作。
- **滑動讀者：** 默認原生垂直捲動，不因漂亮的版式鎖住長文；不要使用無意義的 500vh 空白過場。
- **讀圖互動：** 地圖、圖版、來源資訊可以放大、比較、返回；時間線可正向與反向移動；有爭議的重建要能看到圖例或備選方案。
- **可及性：** 鍵盤焦點清晰、按鈕狀態可傳達、prefers-reduced-motion 有靜態替代、影片不自動發聲、沒有必須觀看動畫才能理解的內容。
- **性能：** 圖片以合適尺寸、poster、lazy media 加載；沒有來源或未接入的影片不能用假 spinner 冒充內容。

### 6F.12 網站而不是紙刊：四個編輯尺寸與兩個自由度 [STANDARD]

| 目標 | 編輯/布局規則 | 具體驗收 |
| --- | --- | --- |
| 1648×928 Desktop | 按完整跨頁設計；大字可跨屏，圖版可佔兩邊 | 重要讀圖與中文標題同時可辨，沒有死三欄 |
| 768×1024 Tablet | 重排圖與引子次序、減少層疊，不只是縮小 desktop | 圖例、目錄、目標連結可達，長文 measure 不爆 |
| 390×844 Phone | 首屏單一重點、真實文章單欄；圖版有放大路徑 | 中文數詞不拆裂、caption 緊貼圖、交互控制可用 |
| 320×720 Small | 保持出版信息及縮放能力，即使犧牲戲劇性構圖 | 無水平 overflow、文字不遮人、來源和註腳能看 |
| 原生瀏覽器 Zoom | 100%／200%，並確認更高倍下符合 WCAG Reflow | 不得用 viewport 824px proxy 冒充原生 zoom 測試 |
| Reader motion states | 靜態、動作中、結束、倒退、reduced-motion | 每一狀態有完整閱讀意義，返回不殘留舊層 |

這裡的手機設計**不是單純把雙頁變成單頁**，而是重新確定「先看到證據、文字還是人物」，讓同一個命題在不同視窗以不同閱讀順序呈現。對真正需要二維閱讀的地圖可以設獨立可滾動／放大圖版區域，但不能因此讓整篇文章水平捲動。參照 [W3C WCAG 2.2 Reflow](https://www.w3.org/WAI/WCAG22/Understanding/reflow.html)。

### 6F.13 不可取代的編輯細節：真實文字、圖說、引文、註腳、來源 [STANDARD]

**語義 HTML：** 真正頁面標題為一個可讀 H1；英文字可以作具設計用途的輔助 display，但不能讓裝飾視覺替代中文實際文章題名。每個 figure 的 figcaption 描述事實或解釋，而不是僅列流水號。引用使用可回訪來源，經文有書卷與節次及所用譯本資訊；人名有權威拼寫。註腳可跳往說明並返回當前閱讀位置。目錄的連結永遠指向確實存在的文章／段落，尚未刊出則標示狀態，不製造空連結。

**圖說模板：** 「【編輯編號】物件／事件及視角。年代或時期（如有）；資料來自【作者／館藏／文件ID】，紀錄／重建／推定／有爭議；此圖以【何方式】轉譯。」不必把冗長來源印在大圖上，但必須在圖說或可打開的出處裡保留全文。照片、模型與 AI 製作的詮釋刻線不可混稱。

**文字 QA：** 至少用一個很短的中文主標、真實長標、混合中英人名、帶數字的年代圖說、雙語引文、完整長篇與註腳進行實排；不可只用 Lorem ipsum 或裝飾性的短句驗證。

### 6F.14 從規範書到一張真正頁面：製作卡與責任分工 [STANDARD]

每個被實作的頁面必須交出一張**Art Direction Production Card**，以便編輯、設計、前端與驗收在同一張契約上工作：

| 欄位 | 必填內容 |
| --- | --- |
| Publication / Issue | 西望 / Vol.00 / 樂章 / 欄目 / 真實稿件及版本 |
| Reader Question | 本頁唯一最重要的編輯問題／讀者要獲得的理解 |
| Visual Voice | MONUMENT / ATLAS / WITNESS / SILENCE / READING，選一個主聲部 |
| Layout Roles | 封面、引子、Figure、Caption、來源、正文、出口等必要角色 |
| Hero Subject / Rights | Source ID、原件、可用許可、焦點／禁止裁切區，若沒有圖說為何 |
| Spatial Gesture | 選用秩序／跨頁／遮蔽／負空間／時間圖形；**為何**比普通版更好 |
| Typography & Color | 消費的現存 OS role tokens 與禁用例，不可新起本地全局字色 |
| Responsive Storyboard | Desktop / tablet / phone / 320px + 真 zoom 的內容重排次序 |
| Motion & Fallback | 有何情節目的；靜態仍須可理解 |
| Source & Build Owner | 原稿位置、圖像 registry、HTML/CSS owner、既有 QA 入口 |
| Rejection Gate | 真實截圖問題、accessibility、來源可靠性、稿件忠實度 |
| Approval | PREVIEW / HUMAN REVIEW / APPROVED；評審人及証據 URL |

**第一張已可開工的實例卡：Vol.00 / WALK / Elim / 守城與攻城技術史。** Reader Question：「城牆究竟如何阻擋攻擊，而我們怎樣區分史實與古城假說？」Voice＝ATLAS；開頁可借 MONUMENT 建立歷史張力，但正式史料版必須保留證據線、考古圖、年代與有效長文。ONE 聖光地理和 Jerusalem 3000 可作素材與資料入口；然而前述大衛–所羅門推定牆線是**設計實驗**，不得直接冒充正式攻城史考古證據。主圖、源檔和不確定性應逐一附上；再實測 1648／768／390／320與 true zoom。**這是一張生產任務卡，而非已完成／已簽收的 Elim 作品。**

**第二張寧靜對照卡：Vol.00 / WORSHIP / Maranatha。** Reader Question：「讀完前面人與城的努力後，讀者應如何停留於禱告？」Voice＝SILENCE；不強制引入新幾何或圖片，保留已肯定的留白設計，待真正原稿核定才排出終章。若用相同方框填版，應被拒絕。

### 6F.15 出版／設計驗收：規範不等於畫面，畫面不等於作品 [LOCKED]

**一、文字與真實性：** 真實 canonical source，Vol.00 目錄 4–4–2–2、三個實際間奏、來源／權利／圖說、被標註的未知與候選。**二、藝術性：** 封住 Logo 仍能辨識特殊構圖與閱讀態度；同一書籍的不同聲部差異明確，沒有同一模板機械複製；不是從國外設計案例直接抄色彩、字形或海報。**三、閱讀性：** 長文、手機、鍵盤、註腳、可讀對比、reduced motion、真 zoom。**四、工程證據：** 既有 Design OS authority，唯一 HTML/CSS owner，瀏覽器實際 before/after 與 CI，未通過即迭代，不用新文件迴避問題。

沿用 §6A 現有唯一 10×0–2 rubric：Meaning、Subject、Composition Distinction、Typography、Two-ink Discipline、Hierarchy、Interaction Meaning、Mobile、Accessibility、Editability。內部「獲獎級」晉級要求 **≥18/20、無零分、無未解決 BLOCK，並另通過出版真實性／實際閱讀**；不把這稱為任何獎項官方分數。**目前此 Stylebook 可作有組織的製作指導，但西望藝術風格尚未獲最終簽收；某張試排圖與整期作品也不會因規範完成自動晉級。**

### 6F.16 成熟專著與研究材料的使用權限／版本治理 [STANDARD]

本章骨架根據核對過的書目及公開目錄、作者／出版者說明所推導，**不是宣稱已通讀任何有版權書籍的全文**：

| 專著 | 確認的研究用途 | 西望在本章如何落地 |
| --- | --- | --- |
| Cath Caldwell / Yolanda Zappaterra, [Editorial Design: Digital and Print](https://www.laurenceking.com/products/editorial-design), Laurence King, 2014 | Editorial identity / formats / cover / interior / layout / production 整個刊物的結構 | §6F.01–09 與實際 P1–P5 母版 |
| Sue Apfelbaum / Juliette Cezzar, [Designing the Editorial Experience](https://www.oreilly.com/library/view/designing-the-editorial/9781592538959/), Rockport, 2014 | 誰閱讀、身份、解剖、版式、原型、製作，書的目錄可核實 | §6F.02／13／14 從編輯到設計的角色鏈與卡片 |
| Jan V. White / Alex W. White, [Editing by Design, 4th ed.](https://alexanderwwhite.com/editing-by-design-4th-ed/) | 編輯與設計都須揭示內容核心，內文／圖像與可讀性先於裝飾 | 讀者問題、真實標題、負面控制組與內容忠實性 |
| Timothy Samara, [Making and Breaking the Grid, 3rd ed.](https://www.quarto.com/books/9780760381939/making-and-breaking-the-grid-third-edition), 2023 | 秩序網格與有概念、有目的的破格；更新包含互動場景 | §6F.06 有理由的跨頁打破、而非無限自由 |
| Jeremy Leslie, [The Modern Magazine](https://magculture.com/collections/newest/products/the-modern-magazine), 2013 | Digital x Print 轉譯、雜誌身份、設計與內容相互建構 | 「沒有實體中縫」的 Westside continuous spread＋整期節奏 |

**來源與權威優先序：** 作者及現有 editorial canon → Design OS tokens / type role → 本章正式規範 → §6E 方法／32 張製作規格 → §6D 大量參考與來源紀錄。若衝突，絕不能用新的研究結論覆蓋已保護字體與原稿。本章只是一個**閱讀優先的規範入口**，不新增權限或修改 runtime precedence。

**後續維護規則：** 每次新增真正設計決定，以「原問題→刊物原則→正反案例→實際圖版→截圖→批准/拒絕」更新相關條目；不要再用 R15、R16 無限制堆積獨立研究輪次。已通過的頁面可以逐步把 [TRIAL] 升為 [STANDARD]／[APPROVED SURFACE]，但批准需留明確版本與真實截圖。**先使用這本書製作與拒絕實際頁面，才談修訂這本書。**

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
