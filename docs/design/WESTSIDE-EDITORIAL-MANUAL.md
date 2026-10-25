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
| 刊名背景與字色 | **每期依主圖與編輯題材取色**；需通過跨期識別及對比驗收 | 色面、刊名字色與作品之色彩關係，固定的是調色／驗收機制而非某種永久色票 |

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
- **顏色跨期可變已由主編確定。** 午夜藍＋黎明金是 Vol.00 當期配色，不是全刊永久色。每期顏色來自主圖，須檢查文字對比、色面與藝術主體的關係。
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

**A2 — 現代色塊：** 同一官方 SVG 在**當期主圖決定色彩**的刊名區內，藝術作品位於下方，並允許局部輪廓經編輯許可穿過色面邊界；Vol.00 才用午夜藍／黎明金。色面厚度由刊名實際墨色和裁切共同決定，避免過厚條帶。保留古典 Bodoni 式字形與 The Paris Review 式現代色面結構的張力，不重新生成官方字形。

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
- **主線已聚焦：** A2 The Paris Review 式色面為骨架，加入西望自己的「主體輪廓有節制突破色面」語法；A1 Vogue／L'OFFICIEL 是局部遮擋的參考而非另開候選。仍待定永久光學尺度、裁切和 P2 展開。
- **已量測／已建實驗：** 官方 SVG alpha bbox 見 §11.2；已建立可切換裁切、越界程度及三期設色的實驗頁（§11.6），並開始真實瀏覽器預覽。**尚未批准：** 實驗的審美評分、P2 正式封面、刊頭永久尺寸／位置。
- **實施邊界：** 本章只寫入 Design OS 編輯手冊，不修改正式 SVG、P2 HTML/CSS/JS 或任何發行頁；後續設計應使用原來的 OS scope 與既有驗收流程，不新增獨立管理系統或 CI。


## 11. The Paris Review 內頁解剖與西望刊頭越界語法｜第三輪（2026-10-25）

**編輯決策。** A 版只保留 The Paris Review 式「固定壓頂刊名／可變主圖」骨架；西望將發展自己的差別語言：作品的主體輪廓**有條件地跨越刊頭色面與作品區的邊界**。Vol.00 是大馬士革門的垛口／塔尖，人物期可以是頭部、抽象藝術期可以是筆畫或幾何；**不是每一期都畫城牆**。城牆不能決定永久刊名座標。

**色彩決策。** 封面刊頭的色面與字色來自該期主圖及其編輯命題，並非全刊永遠午夜藍＋黎明金。Vol.00 的午夜藍／黎明金／砂岩是**本期設色**。在同一跨期正式 SVG、光學位置、期數欄位、封面比例合同下允許各期變色。修改色彩時仍需字形筆畫對比和縮圖驗證。

**排除不適合的引用。** Design360° 曾獲整體雜誌設計獎，但這不意味其刊頭本身優秀。依主編判斷，它不作為西望正向刊頭參考；獲獎與刊頭工藝必須分開評價。

### 11.1 一手材料與可複核的實際內頁

- [Pentagram／Matt Willey 官方專案](https://www.pentagram.com/work/the-paris-review/story)：2021 冬季 238 期整體設計、封面、目錄、文學內頁、藝術跨頁實際圖片；同時列出改版理由。
- [Matt Willey 個人作品集](https://mattwilley.co.uk/The-Paris-Review)：原設計者上傳的 238 期圖片與創作署名，適合作一手視覺核對。
- [AIGA Eye on Design 對 Matt Willey／Na Kim 的訪談](https://eyeondesign.aiga.org/whats-past-is-prologue-inside-the-redesign-of-the-paris-review/)：有原設計者對閱讀、字體、紙張、封面與尺寸的解釋。以下正文細節同時核對 Pentagram 實際頁面攝影，非僅轉述形容詞。

**可核實的字體與物理決策：** 2021 刊名使用 Klim Type Foundry 的 **Founders Grotesk**，內文使用 **Heldane Text**；縮小裁切、緊湊頁邊距、減少一行字數、採用偏暖而柔軟的再生紙。原設計者強調改版首先服務閱讀。這些是原刊的設計史實；**西望沿用自身 Design OS 字體，不引入第二套字體權威**。

### 11.2 官方西望刊頭的可見邊界實測

來源：static/images/westside-watch-masthead-landscape.svg。其本體不可改字或重畫。

| 幾何 | 2026-10-25 本地 raster alpha 量測 |
| --- | --- |
| SVG 畫布 | 680 × 190 |
| 實際可見墨色 bbox | x=1..633，y=10..90；約 633 × 81 |
| 墨色寬度佔畫布 | 93.1% |
| 墨色高度佔畫布 | 42.6% |
| 最下方未使用透明畫布 | 約 99 px |
| 方法限定 | sharp 以 SVG 原尺寸 rasterize；alpha > 32/255 的像素作 bbox；不同反鋸齒器可差約 1–2 px |

結論：容器採「width:94%; height:21%; object-fit:contain」時，是以**680×190 整體透明畫布**決定縮放，並非按 633×81 的字形墨色。此前頂部鬆、橫向不夠滿，不可只調外容器寬度。實驗應保留原始 SVG，改用**可見 bbox 的光學視窗或 alpha mask**作定位和逐期著色；禁止拉伸與重新打字。後續還需大／小尺寸真實瀏覽器截圖確認細筆畫與抗鋸齒。

### 11.3 238 期內頁：六種可觀察的頁式，而非一套到處放大字的模板

| Pentagram 實際內頁樣張 | 版式觀察（視覺分析，非原設計者口述） | 西望可轉譯的語法 |
| --- | --- | --- |
| 卷首工作人員名錄 | 左側整頁雕塑照片，右側上方刊名、下面密集而節制的細小資料欄 | 一頁可擁有完整視覺主體，對頁集中編輯資料；不要每欄都設巨大標題 |
| 238 期 Contents | 左頁強烈彩色圖片，右頁有明確數字「238」，分 Prose / Interviews / Poetry / Art 的密集目錄 | P2 左右形成密／疏差異；本刊 12 欄正式目錄要精準、有閱讀路徑，不是 12 個 UI 卡片 |
| “The Art of Nonfiction No. 11” 開篇 | 左頁檔案手稿／影像，右頁小而居中的篇名與作者，正文延後至下半頁 | 文學／見證開篇使用大面積安靜區，不能將滿版英文巨字用作全刊機械模板 |
| 訪談連續閱讀頁 | 正文字欄穩定、欄寬易讀；對頁一張居中的小型紀實照片及圖說 | 西望長文先優化連續閱讀的行長、對齊與引言節奏；有史料時留原比例及圖說 |
| 跨頁肖像繪畫 | 兩張色彩飽滿的圖像佔據左右大面積，頂部保持一致的淡色留白和小型作品資訊 | 網刊沒有紙本裝訂限制時，作品可跨中軸成為整幅視覺平面；保護主體、來源和作品區 |
| 詩歌對開 | 小型斜體起題、自然行分割、一頁詩長而另一頁極短；留下大片有意義的空白 | 禱告、默想、經文不需虛假的大標語；空白要由文字真實長度與內容決定 |

**關鍵辨別：** 238 期部分卷首圖片是廣告，不能把廣告視覺誤稱為編輯作品；我們研究的是其**對頁的密度對比與排版機理**。而原刊正文頁邊距其實較以往緊湊；詩歌和篇章扉頁的大空白是**內容節奏**，並不等於每頁都有巨大邊距。

### 11.4 古典而現代，真正是兩種讀者速度

- **快讀層：** 封面刊名、期數、Contents、章節或藝術組圖。其現代性來自清楚色面、確定的重心、乾淨幾何、強弱對比。
- **慢讀層：** 採訪、散文、詩歌、見證、資料引文。其古典性來自穩定文本欄、字形細節、內文行長、可讀的斜體和頁面停頓。
- 不可把古典誤解成所有標題都用有襯線超大字，也不可把現代誤解成到處設等寬色塊／卡片／導航條。
- 西望 Design OS 既有英文 Bodoni Moda／原生 SC、中文昭源黑體（Chiron）及長文 Noto Serif TC **維持唯一正式字體配置**。借鑑的是組織關係，不移植 Founders Grotesk/Heldane 至站點。

### 11.5 西望四級「藝術突破刊頭色面」實驗

| 級別 | 主圖／刊頭色面關係 | 出版規則狀態 |
| --- | --- | --- |
| 00 — Separation | 色面與主圖嚴格分開：The Paris Review 的克制基線 | 可靠比較組，不預先決定為最終 |
| 01 — Boundary breach | 少量垛口／頭部／筆畫越過色面下緣；不觸及刊名墨色 | **主推測試**：以最小越界建立西望差異 |
| 02 — Architectural interlock | 較大主體侵入色面，仍避開重要字幹、內空及期號 | 僅在真實主圖有結構理由時採用 |
| 03 — Selective occlusion | 如少數 L’OFFICIEL 封面，主體局部壓在刊名之上 | **例外候選**，不得形成「每期重新畫 Logo」；全尺寸與縮圖認字必須通過才可批准 |

每級應在真實**剪裁比例與對開場景**觀察，不可把「越界程度」誤簡化為改整張城牆高度。永久系統的本質是「**圖像在編輯授權下穿越邊界**」，不是「城牆每期固定侵入 X 像素」。穿越位置應由每期主體識別、文字安全區和視覺重心決定。

### 11.6 三類權限的最終分界

| 永久 fixed | 每期 variable | 條件 conditional |
| --- | --- | --- |
| 官方中英 SVG 原字形；墨色 bbox 基準；光學位置；刊名字形內在比例；期數欄位的相對座標 | 刊頭色面、刊名字色、主圖、封面藝術技法、主題標題、主題敘事與相應圖像對比 | 是否越過色面；穿越的主體部分；是否可以接近或在少數情況遮擋字形 |
| 採同一已選出版裁切作跨期識別母版 | 可在尚未定稿前試驗 8:5／4:3／4:5，不能每期私自更改已批准的封面比例 | 橫／直設備的封面比例映射須經明確跨設備批准 |

**當前實際設計實驗（非正式 P2）：** static/experiments/masthead-color-breach-lab.html 在既有 P2 實驗 PR #1355 分支，使用正版 SVG alpha mask＋現有砂岩城牆 PNG，設 00–03 越界、8:5／4:3／4:5、三期取色與跨期壓力檢查。Vol.01 肖像只是 CSS 幾何占位，Vol.02 是文字抽象測試，均未出版。此文件是**藝術試驗，不是新 Design OS、不另起 CI、不修改正式 P2 動效**。需待真實瀏覽器視覺驗收後才可將位置、尺寸、遮擋上限升格為正式合約。

### 11.7 下一輪內頁實作的四種母版

1. **Front Matter / Contents：** 濃密書目資訊、正式四樂章／十二欄、左側完整藝術主體；不要再加入多餘文案或假的 UI 卡片。
2. **Essay / Interview：** 主標可小且居中／偏置，讓原稿從下方以正常字級進入；文字與史料照片可跨虛擬中軸。
3. **Poetry / Prayer：** 保留經文、詩句真實長度造成的空白；小型斜體英文可擔任高級節奏標誌。
4. **Art Portfolio：** 一幅或兩幅作品建立跨頁的大色面；作品名、來源、版權信息在穩定的細小資料位，不遮人物／主體。

**設計驗收順序：** 一組三期刊頭 → 同期 P2 完整對開 → 4 種內頁跨版 → 連續 10+ 分鐘真實長文閱讀 → 手機、縮圖、鍵盤、200% zoom、反向動效。以現有 Design OS 的獎級評分和 veto 門檻驗收，不設新的平行分數系統。

### 11.8 內頁網格不等於一個套版：從 238 期抽出的「六種頁面工作」

本段中，**觀察**只指 238 期一手樣張的實際畫面；**西望提案**是新的設計決策，並非 Matt Willey 提供的原刊網格數值。禁止把建議比例冒充 The Paris Review 的設計參數。

| 內容角色 | 238 期可觀察的版面行為 | 西望數位對開試作（待測，不是原刊數值） | 禁止的機械模仿 |
| --- | --- | --- | --- |
| Front Matter／刊首 | 目錄資訊緊湊，與對頁強視覺形成反差 | 一側藝術 55–65%，另一側目錄 35–45%；長目錄用真實分類與行距；跨頁不必依紙本中縫對稱 | 左右各塞一排「卡片」、每項都有圖示 |
| Interview／訪談扉頁 | 小型章題與作者偏置或居中，前段大空白後才進正文 | 主標以頁面寬度的約 20–40% 為起點測試；以內容長度決定正文起跑高度 | 每篇都強制半版超大 Didone |
| Continuous Reading／連續閱讀 | 規律的正文欄、連續頁碼、低噪聲跑眉；史料影像以旁頁呈現 | 先試正文單欄 48–68 個拉丁字母／行；中文以實測閱讀舒適度定行長，圖片可按需跨中軸 | 為了「雜誌感」切成難讀的超窄多欄 |
| Poetry／禱告與詩歌 | 行斷與空白服從真實詩句長度，斜體語法克制 | 讓詩行自然結束，另一頁可保持大面積空白；欄位可以不齊底 | 用裝飾符號或假空白堆砌「高級感」 |
| Art Portfolio／藝術作品 | 彩色圖版成為視覺最大層，作品資訊退為細小圖說 | 作品可跨雙頁，依主體安全區用 30/70、50/50 或滿幅；圖說不可浮壓作品主體 | 強制每張圖使用同一裁切框 |
| Editorial Data／人物、署名、圖說、期數 | 字級克制，資料行清楚可掃描，與正文不爭主題權重 | 制定統一小字、跑眉、頁碼與資料位，從 Design OS 引入 token | 每期改一次資料區字形及位置 |

**幾個不可省略的編輯層級：**

1. **Issue / Cover** 將刊名當作最高身份，主題次之；色面／字色由當期藝術定，字形座標不隨題材改。
2. **Contents** 順序先由欄目的真實資訊架構決定，再用粗細、縮排與短規則線區分；不把每一條目當成界面元件。
3. **Section opener** 可有戲劇化的大字、刻線、石材，但要視文章題材；人物訪談的安靜標題同樣是成熟的藝術指導。
4. **Reading page** 讓正文成為視覺主體，浮動大字與動效退出；重要人物名、訪談者、時間、出處在穩定次級欄。
5. **Portfolio / Quote** 作品／引文與內容主體互相成就，圖說及來源應可核查，不因美觀被裁掉。
6. **Page turn / Spread** 認真設計跨頁的密度斷差；一個滿幅作品對一個密集目錄，或兩個安靜詩頁，都是不同的節奏，不能套同一組比例。

**可操作的數位母版：** 在既有 Westside Design OS 網格中建立 `frontmatter`、`interview`、`reading`、`poetry`、`portfolio` 的 *page recipe*，而不是新建一套 CSS 權威。母版只限制閱讀功能與資料位；左右面積、圖像裁切及大字標題的大小是**依內容評分後選擇**，不是硬編寫五個固定模板。對開本身是主畫布，右頁無裝訂中縫，可作 30/70 或 70/30 的長軸構圖；手機應重組閱讀順序，不把兩張縮小紙頁硬擠進窄屏。

### 11.9 歷史縱軸與當期內容橫軸：不要只學一張 2021 封面

- **1973／第 56 期：** [主編 Emily Stokes 的一手回憶](https://www.theparisreview.org/blog/2021/11/18/with-cherries-on-top/)說她和 Matt Willey 都被該期的實體尺度與簡潔感吸引；可見 2021 的「現代」不是排斥傳統，而是重新選取原刊文學出版傳承。
- **2021／第 238 期：** [Pentagram 整體改版](https://www.pentagram.com/work/the-paris-review/story)與 [Matt Willey 的內頁樣張](https://mattwilley.co.uk/The-Paris-Review)可直接觀察 Contents、訪談、詩歌和圖版；這是目前有直接視覺證據的內頁研究主樣本。
- **2025／第 253 期：** [出版方正式目錄](https://www.theparisreview.org/back-issues/253)可核實 Fiction／Interview／Poetry／Portfolio／Art 仍是重要編輯體裁，且主圖與作者逐期變化。**此來源只證實內容架構與跨期性，不足以憑空宣稱第 253 期內頁字距、留白或網格尺寸沒有變。**

再深入必須取得**不同期數的實際內頁樣張**，測同類欄目在不同期數中的字級、欄寬與跨頁變化；目前只批准「第 238 期六種版式觀察」，不批准「全刊逐期內頁系統已完整逆向」。

### 11.10 獲獎級研究的證據與否決門檻

[D&AD 的 Magazine & Newspaper Design](https://www.dandad.org/awards/d-ad-awards/categories/magazine-newspaper-design)明確覆蓋印刷與數位刊物，並有 Digital Publications、Publication Refresh 等不同項目；**某刊得獎不等於每一個刊頭元素值得模仿**。PRINT Awards 曾公開其評審四個角度：[Originality、Innovation、Permanence、Execution](https://www.printmag.com/advertising/the-best-graphic-design-of-the-year-announcing-the-winners-of-the-print-awards/)。西望把它們作研究參照，但最終分數仍歸唯一 Design OS，不另起評分系統。

| 評審視角 | 要驗證的實物 | 一票否決例子 |
| --- | --- | --- |
| Originality／原創 | 不只複製 TPR 色塊，還能指出西望「輪廓跨界」的編輯意義 | 僅把城牆貼在色塊上、毫無主題理由 |
| Innovation／創新 | 對開網刊突破紙本中縫，動態轉場仍保證閱讀 | 動效更搶眼但使刊名／正文不可讀 |
| Permanence／跨期耐久 | 同一 SVG／同一光學座標，三期題材及配色都能站穩 | 每期調大字、挪刊頭、換中英組合以救單張構圖 |
| Execution／工藝 | 光學可見邊界、字距、段落節奏、圖片主體、來源及縮圖均通過實測 | 名字細筆畫被城牆或背景噪聲吞掉；手機正文難讀 |

**目前階段性結論：** 01「微越界」為低干預常規語法候選；在 Vol.00 真實城牆測試中，02「建築交錯」可能比 01 更有完整的城垛與城門表情，因此不能機械规定每期都用 01。03「文字局部遮擋」只作極少數例外且目前 Vol.00 明顯受損。這是待跨期評選的藝術假設，**不是四級效果已獲藝術批准**。批准之前，必須做三期實物、桌面／手機、8:5／4:3／4:5、縮圖，以及 P2 真實對開和內容閱讀驗收。

### 11.11 真實瀏覽器初步驗收記錄（2026-10-25）

測試網址：[`static/experiments/masthead-color-breach-lab.html`](../../static/experiments/masthead-color-breach-lab.html)（PR #1355 的獨立預覽，並未接管 P2 正式封面）。用官方 SVG 原字形、Vol.00 原砂岩城牆素材，在實際瀏覽器切換已修復的控制器；測了至少 8:5 橫幅及 4:5 直幅、Vol.00 建築與兩期占位題材。字形經可見 alpha bbox 裁窗，不再以 SVG 透明尾端決定刊名字形大小。城牆／遮罩素材現採等比 `cover` 裁切，不以 `100% 100%` 拉長石牆。

| 觀察項 | 初步判讀 | 狀態 |
| --- | --- | --- |
| 00 嚴格分區 | 刊頭認字穩定，卻缺少西望與參考刊物的差別 | 可作對照，不優先 |
| 01 微越界 | 兩個主要垛口越過色面，完整保護字形；8:5 縮小時創新可能過於微弱 | 保留低干預候選，仍需縮圖比對 |
| 02 建築交錯 | 城門與塔樓的形體更完整，城垛對色塊形成可辨識的主題介入，刊名仍完整 | **Vol.00 目前較有表現力的候選**，需核對跨期規律 |
| 03 強遮擋 | Vol.00 的城牆侵入 WESTSIDE WATCH 重要字幹，造成識別損失 | **Vol.00 暫不通過藝術驗收**，不能作默認效果 |
| 8:5／4:5 | 同一 SVG 尺度與比例得以跟隨封面座標；原城牆需等比裁切，避免人物或建築因版型改變而變形 | 光學／主體裁切仍待 P2 全對開與手機實機評選 |
| Vol.01／02 占位 | 可變刊頭色塊與字色確實不依賴午夜藍＋黎明金而成立，但占位圖形不是可出版的藝術作品 | 僅通過概念壓力測試，**不是三期正式視覺通過** |

**工藝判斷：** 不將「越界幅度」升格為單一固定百分比。先標註當期藝術輪廓、字形墨色安全區、期數資訊位及裁切視窗，然後在 00–03 級別的編輯授權內尋找每期獨有的穿插點。正式出版只批准一組固定刊頭坐標／裁切合約，**不把試驗控件本身部署到發行頁**。


### 11.12 Vol.00 期號位置與寫法：退出刊頭色面（2026-10-25 第四輪）

**主編新增決策：** Vol.00 不再出現在 WESTSIDE WATCH／西望的刊頭色塊內。選用第 02「建築交錯」方案繼續設計，刊頭區只保留官方中英文刊名；不要讓小型期號破壞刊名和色面形成的完整平面。期號仍屬跨期必需的**出版資料層**，它的位置應從**封面主圖的閱讀結構**確定，並跨期固定，而不是逐期見縫插針。

**資料來源，須區分印刷媒介和數位轉譯：**

- [Pentagram 2021 The Paris Review](https://www.pentagram.com/work/the-paris-review)：改版後把期號和部分作者資訊轉移至**紙本書脊**，釋出封面正面給刊名與藝術作品；這是功能層級重分配，不是單純刪字。
- [AIGA Eye on Design 專訪](https://eyeondesign.aiga.org/whats-past-is-prologue-inside-the-redesign-of-the-paris-review/)：紙本書脊的期號採有辨識力的數字，作者名退為次級小字。西望是網刊，沒有可直接借用的真實裝訂書脊；**不得把紙本形制誤當數位必備條款**。
- [Sheridan《The Elements of Cover Style》](https://www.sheridan.com/magazines-register/the-elements-of-cover-style/)：期號與日期仍是封面出版資訊，但不必搶眼。此原則支持從刊頭色面移走**而非取消**期號。
- [magCulture：Inque #1](https://magculture.com/blogs/journal/inque-1)：有具體將小型刊物資訊放在封面左下角的案例；只作「資料位可以安靜」的參考，不能冒稱其採用和西望一樣的雙語通欄刊頭。

#### A. 位置是出版座標，不是單期補丁

| 假設位置 | Vol.00 的內容關係 | 好處 | 風險和初步態度 |
| --- | --- | --- | --- |
| **P1 下左角，主圖紙色區** | 與右下 CITY OF LIGHT 形成安靜的對角，完全離開頂部刊頭區；期號不壓城門拱心 | 保留城牆的主體表情，資料位易跨期固定，符合左輕右重的封面視線 | **首選候選**；必須檢查 Vol.01 左下大標是否侵占此位 |
| P2 左側主圖中段 | 在砂岩負空間中作小型號碼／出版資訊 | 比最下方更快被看見，未必與底部標題爭位 | 主圖一旦換肖像、滿版攝影或大字母，安全區容易失效；需多期反證 |
| P3 左側邊緣豎排 | 網刊將紙本書脊的檢索作用轉為邊緣 index | 具出版物感，可利用網刊沒有裝訂中縫的自由 | 僅做比較；可能成多餘的裝飾、在手機或縮圖過小，不能假裝是真正的書脊 |

**禁止項：** 回到午夜藍色塊內；靠近刊名字母下緣形成第二條平行字帶；給期號加無故的方框或色塊；因城樓或主題字當期不同而移動正式座標。

#### B. 寫法是編目語義，也是排印設計

| 寫法候選 | 排印邏輯 | 是否變更編目語義 | 初步態度 |
| --- | --- | --- | --- |
| **`VOL. 00`** | 英文 Small Caps／細節字距＋稍大的舊式襯線數字，兩者同一短行；可保留現有 Vol.00 內部識別 | 僅調整空格、字級和組合，不改 Vol.00 身份 | **推薦開始測試** |
| `No. 00` | 傳統文學季刊編號語法；No. 小而克制，00 為主角 | **有變更**：No. 通常是單期號，Vol. 常指卷或系列；未經正式編目確認不可直接替換 | 比較候選，不批准 |
| `00 / VOLUME` | 數字為展示主體，VOLUME 作極小索引標記 | 若只剩 00，在列表與縮圖中可能失去「卷」的判讀 | 藝術／索引變體；一般出版頁需保留完整機器可讀的 `VOL.00` |

**數位可訪問性：** 視覺可用空格與層級拆開 `VOL.` 和 `00`，但可訪問名稱／資料標記仍保留完整 `VOL.00`。不虛構月份、價格、ISSN 或尚未定義的出版日期來填空。

#### C. 02 方案新的九格驗收條件

同一 **02 建築交錯**＋同一官方 SVG／城牆／CITY OF LIGHT，先對照 P1/P2/P3 × 三種字樣；三聯重點方案放在實驗頁內直接並排。每組只變期號，不重排刊名、城樓或主題。測試必須覆蓋：

1. **刊頭清潔度：** 色面上只見中英文刊名；下沿由城垛突破，不能浮出「VOL.00」形成雜音。
2. **閱讀先後：** 刊名第一、主圖與 CITY OF LIGHT 第二、期號第三。期號不是第二個標題。
3. **跨期可用：** 城牆、人物、純文字三種素材不必為期號額外開一個框；期號色彩可按當期主圖獲得局部對比。
4. **裁切可用：** 8:5／4:3／4:5 及對開、手機裁切下不碰作品主體、不墜出安全區。
5. **語義一致：** 在未確定真正出版編目規則前，視覺研究不得偷偷把 Vol. 改成 No. 作正式內容。

**已實作的可切換研究頁：** `static/experiments/masthead-color-breach-lab.html`（PR #1355）加入獨立位置與寫法控件，默認第 02 越界＋P1 下左角＋`VOL. 00`；另有三種配對的同頁對照。這是**期號編輯研究**，不是 P2 正式刊頭尺寸／封面已批准，更未變更全球 Design OS。須憑真實瀏覽器及三期連排再做藝術驗收。
