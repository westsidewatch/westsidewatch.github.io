# Dawn Shared Resource Layer — Full-Library Editorial Scan v1

Status: ACTIVE
Started: 2026-09-24
Canonical substrate: `static/dawn-library/living/root.json` + 21 Living Library shards
Canonical Works at start: **203,448**
Concept authority: `docs/projects/dawn-library/EDITORIAL-PROJECTION-CANON.md`

## Purpose

Understand the shared site-wide canonical resource layer before imposing products on it. The scan does not create a second identity system. It discovers reusable editorial projections over canonical Dawn Works/resources and exposes acquisition gaps, especially Chinese gaps.

The current four projection families are defined by dominant medium/editorial mode:

1. **Curated Collections / 策展集 — image-led synthesis.** Images, maps, manuscripts, photographs, objects, diagrams and other visual evidence lead the route. Text/video may support it. Jerusalem 3000 / Jerusalem Map Atlas is the first production reference.
2. **Cinema / 天堂電影院 — video-led synthesis.** Film, documentary, sermon, lecture, interview, archival footage and other moving image lead the route. Images/text may support it.
3. **Spectrum / 光譜 — text-knowledge-led thematic synthesis.** Books, articles, primary texts, scholarship, references and textual relationships lead a subject direction, continuum, contrast or knowledge topology.
4. **Three Morning Stars / 三晨星 — book-led durable selection.** Primarily identifies books/book-like Works that deserve durable editorial attention and explains why; it is not a rating system.

These are porous reusable projections, not exclusive silos. The same canonical resource may be called by several projections and by any site consumer without duplication.

Chinese acquisition runs in parallel and is driven by gaps exposed by the scan.

## Hard boundaries

- Dawn shared substrate remains the only Work/resource identity authority.
- Scan outputs are projections; they do not create duplicate Works or separate product databases.
- Projection membership is downstream of admission and never becomes an admission gate.
- Chinese discovery/admission is prioritized, but authority / rights / relevance gates are not lowered.
- Wikisource remains permanently forbidden.
- Political / ethnic / war controversy material remains outside Dawn canonical admission under the existing policy.
- Existing engineering projects are not pulled into editorial projections merely because research overlaps. Mature engineering outputs may be called later.

## Baseline snapshot

- Canonical Works: **203,448**
- Shards: **21**
- English (`eng`): **198,556**
- Chinese (`chi`): **2,994**
- Additional Chinese-like codes currently visible: `cmn` **62**, `zh` **1**; normalization must be measured before any language-growth claim.

### Existing knowledge-map roots

| Root | Works |
|---|---:|
| 聖經 | 27,692 |
| 釋經 | 3,383 |
| 神學 | 3,029 |
| 聖經世界 | 2,070 |
| 教會歷史 | 5,497 |
| 基督徒生命 | 14,452 |
| 教會與事奉 | 6,228 |

These are starting coordinates, not the final editorial structure.

## Scan passes

### P0 — Corpus integrity + language + medium normalization — ACTIVE
Measure all 21 shards, deduplicate language aliases, normalize/identify medium types, identify missing/unknown metadata, and establish trustworthy denominators for text, book, image/visual and video resources.

### P1 — Topic / period / author / medium topology — ACTIVE
Build distributions and co-occurrence maps from the actual Works/resources. Detect oversized pools, thin but important areas, isolated islands, bridge Works, and medium density by subject. Video candidates are projected toward Cinema; visual/image candidates toward Curated Collections; text-knowledge topology toward Spectrum; book-like Works toward Three Morning Stars.

### P2 — Chinese gap map — QUEUED
For every meaningful cluster and projection, calculate whether a Chinese reader has the required roles. Measure Chinese visual/image, video, textual-knowledge and book gaps separately rather than treating “Chinese resources” as one number.

### P3 — Spectrum candidates — QUEUED
Generate text-knowledge-led candidate spectra only where the corpus shows a real continuum or productive contrast. Each candidate must cite supporting Works/resources and expose Chinese textual gaps.

### P4 — Curated Collection + Cinema candidates — QUEUED
Generate image-led Curated Collection candidates and video-led Cinema candidates from medium-rich clusters. Require a coherent subject route and rights-safe access. Jerusalem 3000 is the first Curated Collection reference implementation, not a template to copy mechanically.

### P5 — Three Morning Stars candidates — QUEUED
Identify durable book/book-like Works through authority, historical influence, usefulness, distinctiveness, evidence quality and relationship density. Store reasons and evidence; never collapse this into a numeric star rating.

### P6 — Website / consumer guidance — QUEUED
Publish only mature examples. Dawn Library and other consumers may freely call one projection or combine several while preserving canonical identity underneath.

## First editorial hypotheses to test, not assume

The baseline suggests several areas large enough to inspect first:

- 聖經文本 → 譯本 → 單卷研究
- 釋經方法 → 註釋 → 聖經神學
- 基督論 → 救恩論 → 聖靈論
- 第二聖殿 → 考古 → 地理 → 古代近東
- 初代教會 → 教父 → 中世紀 → 宗教改革 → 復興 → 宣教史
- 禱告 → 靈修 → 門徒訓練 → 聖潔 → 苦難
- 講道 → 教導 → 敬拜 → 宣教 → 牧會

They become products only after shard-level evidence confirms them and medium structure is understood.

## Chinese acquisition queue v1

Acquisition priority is not “more Chinese books” in the abstract. For each confirmed subject/projection, fill missing roles according to dominant medium:

1. **策展集 / image-led:** 中文圖集、地圖、手稿、攝影、博物館／考古圖像、合法視覺資料與中文圖說。
2. **天堂電影院 / video-led:** 中文講道、課程、紀錄片、訪談、影像史料，以及可靠中文字幕／中文入口。
3. **光譜 / text-led:** 中文入口文本、經典譯著／原著、工具書、索引、研究、論文與中英橋接。
4. **三晨星 / book-led:** 值得長期保留的中文書、重要譯本、關鍵版本／edition 與合法閱讀 pointer。
5. **Shared bridges:** 同一 canonical subject/Work 的圖片、視頻、文字與書籍互相指向，讓不同產品自由調用。

## Progress ledger

| Pass | State | Evidence / output |
|---|---|---|
| Concept update | PASS | Four medium-led projections fixed in `EDITORIAL-PROJECTION-CANON.md` |
| Baseline | PASS | 203,448 Works / 21 shards; language and seven root counts captured from Living root |
| P0 | ACTIVE | full shard scan + language/medium normalization |
| P1 | ACTIVE | topic/period/author/medium topology; Cinema video projection added |
| P2 | QUEUED | — |
| P3 | QUEUED | — |
| P4 | QUEUED | Jerusalem 3000 retained as image-led Curated Collection reference; Cinema candidates added |
| P5 | QUEUED | — |
| P6 | QUEUED | — |

## Completion rule

This project is not complete when a report exists. It is complete when the shared corpus has produced evidence-backed image-led Curated Collection, video-led Cinema, text-led Spectrum and book-led Three Morning Stars examples; Chinese acquisition has materially filled the highest-impact medium-specific gaps; and real site consumers can call these projections without duplicating the underlying resources.
