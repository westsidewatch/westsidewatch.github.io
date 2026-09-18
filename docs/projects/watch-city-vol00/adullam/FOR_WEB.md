# Adullam for Web — Founding Editorial Prototype

Status: ACTIVE PRODUCTION
Parent: Adullam / Readable Pulpit
Founding corpora: 黃淑華牧師、江秀琴牧師

## Principle

先做 for Web，不把「網站內容」與未來「教會講台工具」割裂。

Web 是 Readable Pulpit 的第一個完整 publication surface；工具工程則從真實 Web consumer 反推 substrate。任何為黃淑華／江秀琴建立的 sermon identity、series、scripture coordinate、timestamp、evidence、map、media relation，都應可被未來 Adullam Tool 直接消費。

Westside Watch 的 Adullam 可以複雜、深、具有完整 editorial design；未來教會工具的操作面保持簡單。兩者共享 canonical sermon/evidence substrate。

## Web metaphor

Westside Watch Journal 是一本在線上打開的雜誌。

Adullam 不是普通 article detail page，而是可翻閱的 magazine sequence：
Spread → Turn → Spread → Emergence → Deep Material → Return → Turn.

桌面以 double-page spread 為核心閱讀單位；手機重新裝訂，但保留頁序、節奏、圖文構成與出版身份。

## Founding issue A — 黃淑華

Editorial goal: 不是人物專訪；打開她的講台。

Research pressure:
- 散落、跨年代、跨教會來源
- 《啟示錄》課程／講道
- 本地未上網影音
- 講義、圖表、照片
- 北美／多倫多事奉史料
- 同一思想跨時間 evidence

Web sequence candidate:
1. Opening spread — minimal preacher/ministry coordinates
2. Preacher Map — editorial double-page spread
3. Pulpit entry — 原聲進場
4. Revelation corpus — series / sessions / chronology
5. Readable sermon — timestamp-synced text
6. Notes & diagrams — image/page evidence
7. Emergence spreads — scripture / same theme across years / places
8. Sources & provenance — deep layer, not visual clutter

## Founding issue B — 江秀琴

Editorial goal: 讓大型 corpus 自己顯出講台秩序，不預設代表主題。

Research pressure:
- 高密度 corpus
- 系列 identity
- 重複影音／文字版本
- 原始來源與轉載來源
- 跨年份發展
- sermon ↔ training course ↔ publication relations
- corpus-level thematic navigation

Current public evidence already shows structured 「內在生活／等候神」 materials across church series, training courses, audio/video and published practice materials. This is a research lead, not yet a final editorial thesis.

Web sequence should be derived from corpus evidence after discovery; do not force Huang's layout onto Jiang.

## Preacher Map

「傳道人地圖」是每期 Adullam 的固定 editorial element：一張真正的 magazine double-page spread。

It is NOT primarily a web map widget.

Canonical relation:
Preacher × Place × Time × Ministry × Sermon × Evidence.

Print/static state must already be a complete beautiful spread. Web adds temporal expansion:
- hover/touch place
- reveal date / ministry / sermon evidence
- play exact audio/video segment
- open related sermon
- return to the same spread

No place lights up without evidence.

Each preacher's map may have a different composition. Editorial role is fixed; visual template is not.

## Emergence on Web

Emergence dimensions:
- Semantic
- Temporal
- Spatial
- Evidential

Priority in preacher pages:
1. preacher's own material
2. Scripture
3. same series
4. same idea across time
5. notes / diagrams / media
6. necessary external context

Emergence must not interrupt the pulpit. It appears at the right reading/listening moment and remains optional.

## Web components that must feed the future tool

Every component built for Web should expose or consume reusable canonical objects:

- Sermon
- Series
- Speaker
- Scripture Coordinate
- Media Source
- Timestamp Segment
- Evidence Node
- Evidence Cluster
- Place
- Ministry Event
- Document / Handout
- Diagram / Image Region
- Editorial Spread

Do not hard-code Huang/Jiang content into presentation components.

## Tool-forward constraint

While building Web, continuously ask:
- Could a church create this object by simply dropping in MP3/MP4/PDF/image or URL?
- Can Doré infer most metadata and ask only for confirmation?
- Can this same sermon later become Preaching Mode without rebuilding?
- Can map/scripture/media be dragged into a future sermon manuscript as intelligent objects?
- Can the final church Web Book consume the same substrate?
- Is Original kept separate from Edited Reading and Doré Layer?

If not, Web implementation is creating editorial debt.

## Immediate production order

1. Corpus discovery for both preachers in parallel.
2. Establish source records and sermon/series identity candidates.
3. Build the first real Web spread from evidence, not placeholder content.
4. Build Huang's Preacher Map spread from verified place/time evidence.
5. Build Jiang's first corpus-navigation spread from verified series evidence.
6. Introduce timestamp readable-pulpit surface.
7. Add Emergence only after the underlying evidence relation exists.
8. Use every friction discovered here as requirements for Adullam Tool.

## Acceptance

The Web phase passes only when:
- both preachers have real evidence-backed publication surfaces;
- pages feel like an online-opened magazine, not a CMS archive;
- the preacher's own preaching dominates;
- map is a genuine double-page editorial spread;
- original media can be reached from editorial claims;
- the same data objects are reusable by the future tool;
- no AI-generated substitute is used for missing sermon authority;
- beauty remains a hard gate.
