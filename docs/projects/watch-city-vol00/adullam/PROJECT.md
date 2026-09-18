# Adullam / 亞杜蘭洞 — Readable Pulpit

Status: ESTABLISHED
Parent: 《守望，一座光明的城》Vol.00
Product role: Doré shared capability consumer and growth field
Editorial surface: Westside Watch / WALK / 亞杜蘭洞

## Definition

亞杜蘭洞不是「人物文章＋配圖＋視頻」欄目。

它是一個 **可閱讀講台（Readable Pulpit）**：把傳道人已經傳講的道，從公開網路、本地影音、講義、照片、圖表與其他散落媒介中重新形成一座可保存、可閱讀、可聆聽、可搜尋、可追溯、可再次出版的講台。

傳道人不是被報道的對象；所傳的道才是正文。

## Product promise

對普通教會，使用必須足夠簡單：

1. 拖入 MP3 / MP4 / PDF / Word / PPT / 圖片，或貼入 YouTube / Podcast / Web URL。
2. Doré 辨認講員、經文、講題、系列、時間、來源關係，生成帶 timestamp 的逐字層。
3. 使用者以最少確認完成 identity / series / metadata 校正。
4. 形成可閱讀講道頁：原聲、閱讀稿、經文、講義、圖表、系列、相關信息。
5. 經明確確認後，可發布到 Adullam Archive、教會網站，以及外部影音／音頻平台；外部發布不得自動越權。

工具的工作是整理沒有整理好的資料；不得要求教會先把資料整理好才能使用。

## Authority model

### ORIGINAL
原始影音、原始講義、原始照片、原始逐字證據。不可由 AI 偷偷改寫。

### EDITED READING
只為閱讀進行可追溯的標點、段落、章節與必要口語整理。任何內容必須能回到 Original 的精確時間／頁面／區域。

### DORÉ LAYER
經文座標、來源關係、背景材料、跨講道關聯、Corpus Intelligence 與 Emergence。不得冒充講員原話或講員神學。

若證據不足：NOT FOUND / UNVERIFIED。禁止生成替代 authority。

## Core data path

Person
→ Ministry / Period
→ Series
→ Sermon / Course
→ Session
→ Segment
→ Scripture
→ Claim
→ Evidence Node
→ Evidence Cluster
→ Source

同一講道的完整影音、音頻、剪輯、逐字稿、轉載與重新命名版本不得被機械地視為多篇講道。

## Addressable evidence

文字不是影音的替代品，而是影音的地址系統。

每個可引用片段至少保留：
- source identity
- speaker
- start / end time，或 page / region
- transcript / visible content
- provenance
- confidence / verification state
- canonical relation

照片中的圖表、PDF 頁面、影音時間段都應可成為 Evidence Node。

## Emergence upgrade

Adullam 將 Doré Emergence 從 content relation 推進到：

**Context → Canonical Relation → Evidence Cluster → Temporal / Spatial Address → Emergence**

浮現不是補充一個「相關視頻」。它可以讓同一信息在不同年份、不同講台、不同媒介中的證據安靜出現，並讓讀者直接回到講員自己的聲音、講義或圖表。

目標：讓一位傳道人的講道生命在閱讀過程中自己顯現。

## Founding corpora

### 黃淑華牧師
用途：稀疏、散落、跨教會、跨年代 corpus。
研究主線：
- 多倫多／北美華人靈恩與先知性服事歷史
- 五重職事與恩賜學
- 《啟示錄》系列
- 公開與本地未上網影音
- 講義、筆記、課堂照片與圖表
- 同一信息跨年份的演變與重現

不得以編輯者自己的《啟示錄》理解代寫黃牧師的講道。

### 江秀琴牧師
用途：高密度、系列化、大型 corpus。
主要壓力測試：
- 大規模 discovery
- 去重與 Sermon Identity
- 系列恢復
- 原始來源辨認
- 跨年份版本
- 長期主題與用語的 corpus-level 關係
- 大量影音／文字的可閱讀導航

不得預先決定其代表主題；由原始 corpus 證據形成編輯判斷。

## Technical exploration seeds

優先吸收成熟技術與方法，而非另造平行系統：
- oral-history synchronized transcript / timestamp indexing
- W3C Web Annotation / media fragments
- IIIF Presentation / annotation model
- ASR transcript as searchable data layer
- corpus segmentation / entity and scripture linking
- provenance-aware evidence graph
- duplicate / near-duplicate media identity
- multimodal document and diagram extraction
- semantic retrieval with deterministic lexical/provenance floor

這些能力應優先濃縮進 Doré 既有 Source Probe / Source Capability Envelope / Media Intelligence / Publishing / Emergence，而不是建立 Adullam 專用孤島技術棧。

## Editorial surface

Westside Watch 的「亞杜蘭洞」是 Readable Pulpit 的出版窗口。

一期的理想閱讀結構：
極短人物／事工坐標
→ 信息核心
→ 原始講台影音／聲音
→ 系列結構
→ 講義／筆記／圖表
→ 經文索引
→ 跨年份相關信息浮現
→ 完整來源與 provenance

文章不是替傳道人寫講道，而是打開一座講台。

## v0 acceptance

v0 必須用兩個 founding corpora 真實驗收，而不是只完成 schema 或 demo。

PASS 至少要求：
- 本地影音可 ingest，且不要求先人工整理 metadata
- Web / YouTube 等公開來源可進同一 source model
- transcript 可回跳精確原聲
- 同一講道多版本能聚合而不重複計數
- 講義／圖片／圖表可與影音片段對齊
- Scripture coordinates 可檢索
- Evidence Node / Cluster 保留 provenance
- Doré Layer 不污染 Original
- 可形成漂亮、簡單、可用的閱讀講台頁
- 黃淑華與江秀琴兩種不同 corpus 都能成立
- Emergence 至少完成一次跨時間／跨媒介 evidence relation 的真實呈現

## Non-goals

- 不做 AI 仿寫講員
- 不把人物採訪當核心
- 不把普通 RAG 摘要當成講台
- 不建立另一個影音託管平台
- 不以自動生成取代原始證據
- 不因技術方便犧牲出版美感

## Product principle

**A living, readable pulpit.**

把講過的道保存下來，把保存的道重新讀出來。
