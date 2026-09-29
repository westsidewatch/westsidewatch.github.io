# Universal Source Enumerator v1 — Real-source acceptance

Date: 2026-09-25
Status: PASS — discovery-shape proof

This proof uses live public collection evidence only. It does not download or rehost source media and does not treat collection size as canonical admission.

## Source A — ARSI Chinese Materials

Collection: `https://arsi.jesuits.global/en/digital-arsi/chinese-books/`

Observed live shape:

- collection landing page with grouped Jap.Sin. sections;
- repeated item-level bibliographic labels;
- direct resource pointers (`pdf`) on individual entries;
- mixed printed books and manuscript/other-material references;
- collection page also points outward to the CCT database for broader descriptive authority.

Examples visible in the live collection include Jap. Sin. I-22, Jap. Sin. II-32, II-85-2, II-159, II-161, II-162, II-173 and the IV-5a–g group.

Enumerator strategy: semantic HTML links → N source pointers → existing Probe.

Expected boundary: ARSI availability does not imply Dawn rehost rights; Enumerator carries pointers only.

## Source B — 汉语基督教文献馆 / Chinese Christian Texts Library

Collection: `https://cct.chinesecs.cn/page/3/`

Observed live shape:

- paginated collection (`1 2 3 4 5 6 7 … 9`);
- item/article links with Chinese titles and descriptive metadata;
- heterogeneous categories including PDF documents, images/video, bibliography and secondary material;
- collection entries include 西儒耳目资、远西奇器图说录最三卷、空际格致、进呈鹰论、西方要纪、坤舆外紀、新历晓或、西洋新法历书、几何原本、交友论、七克、泰西水法、人身图说、远镜说、测量法义、浑蓋通宪图说、圜容较义 etc.

Enumerator strategy: HTML item links + pagination continuation → N source pointers → existing Probe.

Expected boundary: pagination is absorbed by Enumerator and must not leak into Dawn.

## Heterogeneous-shape result

PASS:

1. ARSI demonstrates a grouped archival collection with direct resource links.
2. CCT demonstrates a paginated editorial/catalog collection with item pages and mixed material categories.
3. Both compile to the same `dore.source-enumeration.v1` pointer contract.
4. Neither requires a Chinese-specific ingestion pipeline.
5. Neither requires downloading PDF/XLS/image/video bodies to enumerate resources.
6. Rights and canonical identity remain downstream authorities.
7. The legacy 35→21 seed materializer is not part of either route.

## Production route now unlocked

`Chinese collection discovery → source.enumerate → N pointers → source.probe → capability-envelope → source.dispatch → Dawn admission / Resource Fabric`

The next and final v1 step is production integration/CI plus a real Dawn delta. Source-pool counts must remain separate from canonical admission counts.
