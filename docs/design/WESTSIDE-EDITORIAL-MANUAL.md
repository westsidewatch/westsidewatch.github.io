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

## 9. 西望雜誌跨期固定刊名系統｜第一輪研究（2026-10-25）

> **性質：研究結論及下一輪設計約束；不是已通過視覺驗收的刊名尺寸。**
> **唯一候選：A 版。B、C 版正式淘汰。** 本章討論封面刊名（cover nameplate / masthead），不是每期重新製作的單張海報 Logo。
> **上位權威仍為 Westside Design OS。** 此處建立編輯決策與驗收方法，不新增字體、顏色或 CSS 權威。

### 9.1 核心出版原則

西望是連續出版物，不是逐期獨立海報。跨期刊名的固定性提供系列識別；封面作品的變化負責表達每期內容。正式品牌改版可以系統性重設刊名和尺寸，但同一設計時期內不應因城牆、人物或當期圖片的位置而任意移動、縮小、重繪刊名。

| 權限 | 跨期狀態 | 內容 |
| --- | --- | --- |
| 永久刊物身份 | 固定；正式改版才改 | 官方中英文組合、字形、可見比例、定位、視覺層級 |
| 發行及期數資訊 | 位置與樣式固定，內容更新 | Vol. / No. / 日期 / 期號 |
| 封面編輯藝術 | 每期開放創作 | 攝影、人物、城牆、刻線、晨星、金光、主題文字、配色 |
| 刊名背景與顏色 | 按被批准的刊頭合約，不隨意更改 | 固定色塊或經明確規定的有限色彩變體 |

**Vol.00 專屬內容不構成品牌幾何基準。** 大馬士革門／城牆、晨星、金光、CITY OF LIGHT 等僅為 Vol.00 的主題作品；下一期即使完全沒有它們，刊名也應維持同一出版身份。先確定刊名系統，再安排當期藝術，而非讓當期藝術倒逼刊名位置。

### 9.2 十四本成熟雜誌的跨期機制研究

以下重點是封面識別的長期機制，不是複製單張封面；不同年代可能經歷正式改版，不應把歷史上的變化誤讀成逐期任意重繪。

| # | 出版物 | 跨期識別機制 | 可轉化為西望的方法 |
| --- | --- | --- | --- |
| 01 | [TIME](https://time.com/vault/year/2025/) | 強勢上沿刊名與紅框共同形成固定封面身份 | 識別容器獨立於當期內容 |
| 02 | [National Geographic](https://www.nationalgeographic.com/impact/article/magazine-cover-photos) | 黃色邊框與刊名長期連續 | 主題攝影不能替代出版身份 |
| 03 | [Vogue](https://www.vogue.com/article/from-the-archives-vogue-looks-back-at-120-years-of-covers) | 大型高對比襯線刊名壓在影像之上 | 刊名具有近乎通欄的權重與古典辨識 |
| 04 | [The New Yorker](https://www.newyorker.com/news/press-room/the-entire-new-yorker-archive-is-now-fully-digitized) | 穩定的藝術封面＋經典刊名 | 不必以大量封面導讀佔據作品 |
| 05 | [Monocle](https://monocle.com/magazine/issues/) | 穩定上沿識別、編輯層級與期數資訊 | 刊名與次級資訊形成長期秩序 |
| 06 | [The Gentlewoman](https://www.dandad.org/work/d-ad-awards-archive/the-gentlewoman) | 固定字標與肖像／色彩格式 | 每期變化來自作品，不是 Logo 移動 |
| 07 | [Apartamento](https://www.apartamentomagazine.com/apartamento-archive-issue/) | 大型字標與生活影像同場 | 圖像可以接近文字，身份仍須可讀 |
| 08 | [Domus](https://www.domusweb.it/en/architecture/gallery/2019/12/17/10-years-of-domus-through-its-covers.html) | 不同設計時期中，刊名與建築／圖形形成出版系統 | 主題建築必須服從已批准的刊名策略 |
| 09 | Wallpaper* | 刊名區與攝影／設計作品的強層級 | 可以研究上沿色面與藝術區的分離 |
| 10 | [Dwell](https://www.dwell.com/magazine/issues) | 大字標與建築攝影共同構圖 | 不以建築頂點決定刊名位置 |
| 11 | [The Paris Review](https://www.pentagram.com/work/the-paris-review) | 2021 年整套改版：刊名、裁切、封面藝術、書脊資訊互相決定 | 刊名可反過來決定整本出版物的結構 |
| 12 | [Kinfolk](https://www.kinfolk.com/product-category/kinfolk-magazines/) | 不同改版階段的識別與影像系統 | 區分正式改版與單期自由設計 |
| 13 | [The Economist](https://www.economistgroup.com/businesses/the-economist) | 小面積但強烈的紅色固定刊名容器 | 品牌識別不一定最大，但應穩定 |
| 14 | [Architectural Digest](https://archive.architecturaldigest.com/issues) | 上方大型 AD 識別與室內／建築圖片並行 | 攝影作品不可取代永久刊名 |

反例／特例需獨立標記：The Architectural Review 歷史上曾有意減少跨期統一封面；[Port 的手寫刊名實驗](https://magculture.com/blogs/journal/port-handwritten-covers)則有意每期改變名稱呈現。這些是具體編輯立場，不是西望新建立刊名時的預設方法。

### 9.3 四種刊名結構原型

1. **Top Masthead Band：** 上沿獨立刊名帶；藝術作品在下方自由更換（Monocle、Wallpaper*、The Paris Review）。
2. **Full-width Display Masthead：** 大型通欄壓頭；主視覺可以延伸到字母後方（Vogue、TIME）。
3. **Framed Editorial Cover：** 固定邊框／版心／安全區建立縮圖辨識（The Gentlewoman、National Geographic）。
4. **Integrated Masthead：** 刊名與作品有穿插或色彩互動，但字形與身份結構仍有規則（Apartamento、Dwell）。

這四種是分析範疇，不是四個需要新建的西望候選。西望仍只保留 A 版，後續在 A 內部研究滿幅壓頭的兩種結構。

### 9.4 官方資產與固定合約

目前官方 SVG：[`static/images/westside-watch-masthead-landscape.svg`](../../static/images/westside-watch-masthead-landscape.svg)，原始畫布 `680 × 190`，`viewBox="0 0 680 190"`。它包含 LivingWater、WESTSIDE WATCH 和「西望」的中英文組合。**使用現有 SVG，不重新打字、不用字體仿製、不為不同期數生成另一個字形。** 若未來需要正式的封面專用組合變體，必須作為刊頭定型決策另外批准，並保存原 SVG 母資產。

待定型的固定合同：

- 依封面本身的座標系鎖定**實際可見字形**寬度、上邊界、左邊界、長寬比例和中英文關係；不能僅依 CSS 容器外框推論。
- 刊名區與期數資訊位必須跨期一致；避免移動城牆時把刊名擠上去、縮小或重新置中。
- 目前午夜藍＋黎明金有潛力，但顏色是否固定、哪些變體合法，仍需跨期測試批准。
- 桌面與手機可改變整個封面的呈現方式，但不能把刊名從封面自己的比例座標中拆出來。
- SVG 的畫布留白和 path 真實墨色邊界必須分開測量。現有 `width:94%`、`height:21%`、`object-fit:contain` 不等於可見字標佔封面 94%。

### 9.5 第一輪結論／尚未通過項目

A 版為唯一候選；不批准永久刊名位置或尺寸，直到完成真實 SVG 墨色邊界量測、封面座標鎖定及至少三期不同藝術題材的測試。這是研究完成，不是封面完工，也不是視覺驗收。

## 10. 西望壓頭式 Masthead 深度研究｜第二輪（2026-10-25）

> **核心命題：刊頭不是附在海報上的 Logo。它是整套出版設計的結構性起點，足以反過來決定裁切尺寸、版面比例、藝術面積、資訊層級和跨期節奏。**
> **已修正的明確使用者要求：禁止先以正方形為限制。過去的 8:5 可以恢復；也可比較其他合理裁切。這是網路刊物，應用可變版型的自由。**
> **沿用目前的中英文組合及官方 SVG。** 不因探索 Vogue 或 The Paris Review 而先重繪 WESTSIDE WATCH／西望。

### 10.1 兩條正式研究道路（均屬 A 版內部）

| 尺度 | A1 — Vogue / L'Officiel 式古典滿幅壓頭 | A2 — The Paris Review 式現代刊名色塊 |
| --- | --- | --- |
| 不變的共同基礎 | 頂部壓頭、左右近乎撐滿、跨期固定字形與光學比例 | 同左 |
| 視覺語言 | Didone／Bodoni 類高對比襯線，刊名與影像交疊 | 強勢刊名佔獨立色面，藝術區與之建立清晰分界 |
| 作品關係 | 攝影、刻線、人物可在刊名後方延續，需維持讀字對比 | 刊名背景不依賴當期作品，色塊下方藝術獲得自主 |
| 重點機制 | 古典傳統與現代影像的穿透式張力 | 古典字形也可以透過現代色面獲得更當代的出版秩序 |
| 失敗風險 | 極細字線與複雜刻線混淆、光學邊界不穩 | 刊名帶過厚、作品空間被壓縮、色塊淪為貼上的裝飾 |
| 目前狀態 | 保留研究，不宣布淘汰 | 優先研究，但未定稿 |

**重要：不要把兩種道路強行等同於兩種字體。** 西望可保留 Bodoni Moda 與官方中英文 SVG，同時借鑑 The Paris Review 的色塊、資訊移動及出版比例策略。

### 10.2 Vogue / L'Officiel：高對比字形為何適合壓圖

Abbott Miller 的 [Eye Magazine 研究](https://www.eyemagazine.com/feature/article/through-thick-and-think-fashion-and-type)指出：Vogue 早期字形多變，約在 1955 年後確立持續使用的全大寫 Didone 式刊名。高對比字體有粗大的主要筆畫與纖細連接線，覆蓋攝影時具有視覺穿透感；這是古典字體能與當代影像並存的結構原因，而不只是「顯得高級」。

[L'Officiel 百年封面回顧](https://www.lofficiel.com/industry-trends/lofficel100-retour-sur-un-siecle-de-couvertures-emblematiques)及[官方各期封面](https://www.lofficiel.com/issues)用於研究穩定刊名與不斷變換的背景／人物之關係。

對西望的轉譯：

- 研究**光學滿幅**，不是機械地設 `left:0; right:0` 或強行橫向拉伸字母。
- 正式字形不可扭曲；字母重要筆畫不得被偶然裁斷。
- 頂部留白與左右視覺邊界要由真實字形邊界及封面比例共同決定。
- 用金色或紙白色字覆蓋多雷刻線時，必須逐一測試細筆畫的對比，不可用單次截圖判斷跨期成立。

### 10.3 The Paris Review：刊頭、尺寸與出版編輯是一個決策

[Pentagram 2021 改版案例](https://www.pentagram.com/work/the-paris-review)由 Matt Willey 與新編輯及藝術團隊共同完成；新刊名使用 Founders Grotesk，封面減少導讀，重要作者資訊與期號被整合進書脊，封面為藝術作品騰出空間，實體尺寸亦改為更接近可單手持握的書本。[主編 Emily Stokes 的說明](https://www.theparisreview.org/blog/2021/11/18/with-cherries-on-top/)提供編輯部自己的判斷。

**關鍵不是哪一個單獨原因「造成」尺寸改動，而是刊頭制定本來就關乎完整出版設計。** 西望應先設計刊名／色面／藝術的空間關係，再反過來決定網刊封面裁切及展開比例；不必服從當前 Vol.00 的既有形狀。

色塊不是一條後貼的裝飾，而應同時完成三項任務：刊物身份與每期圖像分隔、閱讀層級建立、跨期穩定辨識。

### 10.4 創意刊物與獨立雜誌補充樣本

| 樣本 | 可研究的機制 | 對西望的限制／啟發 |
| --- | --- | --- |
| [The Gentlewoman](https://www.dandad.org/work/d-ad-awards-archive/the-gentlewoman) | 固定字標＋肖像／色彩形成系列 | 以少數要素建立長期辨識 |
| [Apartamento](https://www.apartamentomagazine.com/apartamento-archive-issue/) | 大刊名與自由生活影像共存 | 文字與圖片可接近，但不犧牲名稱辨識 |
| [MacGuffin](https://www.port-magazine.com/design/cover-to-cover/) | 巨型 M 作為跨期識別 | 單一圖形能提供系列感，不等於西望要改用字母縮寫 |
| [Magazine B](https://magculture.com/blogs/journal/magazine-b-60-monocle) | 每期不同品牌，B 身份固定 | 當期內容可大幅變化，刊物仍是一套 |
| [Frieze](https://www.pentagram.com/work/frieze) | 從原刊名字形發展品牌專用字體 | Masthead 可以反過來成為 Design OS 字體研究來源 |
| [Sight and Sound](https://www.pentagram.com/work/sight-and-sound/story) | 固定新刊名，封面刊名顏色依內容改變 | 字形固定與色彩可變是分開管理的權限 |
| [The New Republic](https://www.pentagram.com/work/the-new-republic) | 強刊名＋12 欄網格＋依文章語氣選展示字 | 封面身份穩定，編輯字體可以自由 |
| [Citizen](https://www.pentagram.com/work/citizen) | 從刊名、網格、節奏建立第一期與未來期數 | 新刊物的封面必須先考慮長期系統 |

備註：獨立出版的自由不等於每期重繪刊名。[magCulture 對 Port 的例外案例](https://magculture.com/blogs/journal/port-handwritten-covers)應列為有意挑戰固定識別的反例，不當作西望現階段預設。

### 10.5 中文與中英雙語獨立刊物研究

| 刊物 | 核實入口 | 研究重點 |
| --- | --- | --- |
| PPAPER（臺灣） | [官方介紹](https://www.ppaper.net/about/) | 穩定英文刊物身份如何承載多種藝術／設計專題 |
| VERSE（臺灣） | [官方介紹](https://www.verse.com.tw/about-us)、[編輯自述](https://www.verse.com.tw/article/verse-anniversary-2024) | 英文刊名與中文主題、攝影、插畫、印刷實驗的層級 |
| Design360°（廣州） | [官方網站](https://design360.cn/zh/) | 數字／符號／期號的識別結構與設計專業的實驗性 |
| BranD（香港） | [出版方作品](https://www.behance.net/BranDMagazine)、[國際設計協會資料](https://www.theicod.org/en/network/idmn) | 中英雙語、字體主題與特殊印刷；注意歷史各期不一定採同一固定位置 |
| 秋刀魚（臺灣） | [獨立出版聯盟](https://indiepublisher.tw/zh-hant/member/60) | 少量中文字如何與巨大中文專題標題及多變插畫共存 |
| LOST（上海） | [magCulture 封面／編輯分析](https://magculture.com/blogs/journal/magazine-of-the-week-lost) | 中英雙語、影像敘事與出版尺寸；不是滿幅刊頭的直接樣本 |
| 1413（華語創意出版） | [magCulture 主創訪談](https://magculture.com/blogs/journal/echo-wu-1413) | 街頭字形、包裝、舊書與中文日常視覺語彙；作文化語言對照，不冒充固定刊名樣本 |

**中文的幾何問題不能忽略。** 「西望」僅兩個方塊字，WESTSIDE WATCH 是較長的拉丁字母序列。若不改變字形比例，兩者不可能用同一種字距方法同時達成近乎滿幅；也不得用 CSS 拉伸中文字。研究重點是如何在**同一官方組合 SVG**中保留雙語身份與清晰優先次序，而非讓「西望」變成只屬當期的藝術標題。

### 10.6 版型不是方形限制：封面可決定自己的裁切

- **撤銷方形先驗。** 正方形僅可作比較情境，不能當作決定刊頭的既定邊界。
- **恢復 8:5 為候選**，並允許更多按刊頭／藝術／P2 展開需求選出的裁切比例；先確認 8:5 在具體封面與對開場景的軸向和角色，不偷換成某個固定的單頁比例。
- 網刊可按版型重組封面區域，不受傳統裝訂中縫約束；不能機械複製紙刊裁切。
- 用當前中英文 SVG 在多個版型上做**實際排版比較**。未取得跨版型圖證前不定尺寸；現在的 680×190 是資產畫布，不等於實際墨色邊界。
- 正式刊名一旦選定，往後每期在同一封面座標系中保留其光學大小、位置及中英文內部關係；不同設備應整體同比例縮放或用明確批准的封面版型映射，不能任意改放刊頭。
- CSS `object-fit:contain` 受容器及資產兩者比例限制。應實測渲染後的 SVG 可見邊界，不能只讀 `width` 屬性。過去由正方形推算出的 75.2% 僅是假設情境下的容器數學，不得升格為設計限制。

### 10.7 A1／A2 精確試驗合同（尚未批准最終值）

**A1 — 古典滿幅：** 官方 SVG 的中英文組合在頂部獲得近乎整幅的權力，主視覺可進入字後；應測可見字形跨度、上邊界、細筆畫對比、主體遮擋與縮圖識別。

**A2 — 現代色塊：** 同一官方 SVG 在專屬午夜藍／黎明金刊名區內，藝術作品位於下方或以清楚的界面銜接；色面厚度須由刊名實際墨色和整體裁切共同決定，避免過厚條帶。可以研究古典 Bodoni 式字形與 The Paris Review 式現代色面結構的結合，但不是重新生成官方字形。

兩者是**同一 A 版內部**沿一條有意義軸線（影像後置 vs 固定色面）的比較，不復活已淘汰的 B、C。不要把研究圖當成定稿封面。

| 假設期數 | 跨期壓力情境 | 檢驗重點 |
| --- | --- | --- |
| Vol.00 — CITY OF LIGHT | 大馬士革門、建築刻線、金光 | 複雜結構對刊名字線的干擾 |
| Vol.01 — THE HUMAN FACE | 黑白人物肖像 | 頭部／刊名穿插與辨識 |
| Vol.02 — THE WORD & THE WORLD | 純字體、幾何與強烈色彩 | 不依賴城牆及攝影時是否仍能辨認西望 |

至少比較兩條道路 × 三種完全不同的藝術條件 × 候選裁切及手機映射；材料可用現有網頁資產、CSS 色面與占位構圖，不必生成三張新圖片。

### 10.8 真正的出版級驗收，而非元素排列

每次設計須先給出：**刊名優先級 → 裁切／長寬比 → 固定版心與墨色邊界 → 發行資訊位 → 本期藝術安全區 → 主題標題 → 縮圖與裝置測試**。倒序工作會把整張封面做成海報或讓主題資產控制刊名。

封面需要獨立通過以下門檻：

1. 三期連排時，一眼辨認為同一刊物，無需靠 Vol.00 城牆。
2. 永久刊名在每期的實際可見比例、座標、中英文關係一致。
3. 複雜、明亮、極簡三種封面皆可讀；50%／縮圖尺度仍辨識。
4. 桌面、手機以及候選裁切下沒有偶然裁字、拉伸、重疊或死區。
5. 作品有足夠獨立空間；刊名不顯得被圖片推擠。
6. 版面從靜態起始、動效過程到落定皆能讀；不得靠動畫掩蓋不合格構圖。
7. 真實瀏覽器截圖、字形邊界量測與比較驗收通過後，才可批准永久合約。CI 綠燈只是工程條件，不是藝術驗收。

### 10.9 本次決策記錄

- **已確定：** A 為唯一候選；B／C 淘汰；跨期固定刊名是出版基礎；刊頭先於當期封面藝術；不受正方形約束；8:5 可回用、其他裁切可探索；沿用原有 LivingWater／WESTSIDE WATCH／西望組合 SVG。
- **繼續研究：** A1 古典滿幅 vs A2 現代色面；永久可見尺度；中英文在固定刊名中的精確權重；合適裁切與 P2 展開方式。
- **尚未完成：** 原始 SVG 的實際墨色邊界量測、真實封面排版、三期跨期測試、瀏覽器視覺驗收、最終刊名尺寸／位置批准。
- **實施邊界：** 本章只寫入 Design OS 編輯手冊，不修改正式 SVG、P2 HTML/CSS/JS 或任何發行頁；後續設計應使用原來的 OS scope 與既有驗收流程，不新增獨立管理系統或 CI。
