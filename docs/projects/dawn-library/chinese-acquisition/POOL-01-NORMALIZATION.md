# Chinese Gap Acquisition — Pool Normalization 01

Status: ACTIVE POOL NORMALIZATION
Date: 2026-09-25
Purpose: turn large Chinese discovery sources into machine-processable acquisition pools before title-level reconciliation/admission. This does not create a parallel pipeline.

## Hard gates retained

- Existing Dawn discovery → reconciliation → rights → relevance → authority → canonical admission remains the only admission path.
- Wikisource is forbidden at discovery and admission.
- Political / ethnic / war controversy material remains excluded under existing Dawn policy.
- Discovery authority, access permission and rehost permission remain separate.
- Provider collections are evidence/discovery pools; their contents do not become canonical merely because a provider is trusted.

## Pool schema

Every source family is normalized to:

`poolId / provider / collection / dominantMedium / languages / dateRange / estimatedUnits / enumeration / accessMode / rightsState / semanticSeeds / projectionTargets / processingState`

Processing states:

- `enumerable` — provider exposes item/title lists that can be converted into candidates now.
- `catalog-query` — reliable catalog exists but requires query/export work.
- `pointer-only` — useful provider access; no rehost claim.
- `rights-review` — item/collection rights must be resolved before stronger capability.
- `deferred` — useful evidence but not yet machine-enumerable enough for current batch.

## A. Immediately enumerable pools

### CN-YALE-CCLC
Provider: Yale Divinity Library / Documentation of Chinese Christianity
Collection: Chinese Christian Literature Council — 廣學會 + 基督教輔僑出版社
Dominant medium: book/text
Scale: 1,300+ tracts/books; provider exposes title spreadsheets for CLSC (692) and CCLOC (616).
Enumeration: XLS/XLSX title lists.
Access: provider/special-collections pointer; digital-copy request where applicable.
Rights: rights-review; no blanket rehost.
Semantic seeds: Chinese Christianity, theology, Christian life, evangelism, education, translation, church history.
Projection: Spectrum + Three Morning Stars; selected visual evidence → Curated Collections.
State: enumerable.

### CN-YALE-FMC
Provider: Yale Divinity Library
Collection: China Free Methodist Church / 台灣循理會
Dominant medium: book/periodical
Scale: 35 monographs + 619 enumerated serial issues across 循理週報 / 循理會刊 / 循理報.
Enumeration: provider title spreadsheet + serial ranges.
Access: request/pointer.
Rights: rights-review.
Semantic seeds: Taiwan Christianity, denomination history, ministry, preaching, church life.
Projection: Spectrum + Three Morning Stars.
State: enumerable.

### CN-YALE-CBC
Provider: Yale Divinity Library
Collection: Chinese Baptist Convention / 中華基督教浸信會聯會
Dominant medium: periodical/text
Scale: 252 issues + commemorative publication.
Enumeration: provider collection listing / serial identity.
Access: request/pointer.
Rights: rights-review.
Semantic seeds: Baptist history, Taiwan Christianity, church ministry, missions.
Projection: Spectrum.
State: enumerable.

### CN-YALE-HLTS
Provider: Yale Divinity Library
Collection: Holy Light Theological Seminary / 聖光神學院
Dominant medium: book/periodical
Scale: 45 monographs + five serial titles with substantial issue runs.
Enumeration: provider XLS title list.
Access: request/pointer.
Rights: rights-review.
Semantic seeds: theology, theological education, ministry, Bible study.
Projection: Spectrum + Three Morning Stars.
State: enumerable.

### CN-YALE-REICHELT
Provider: Yale Divinity Library / Institute of Sino-Christian Studies holdings
Collection: Reichelt Collection / 道風山
Dominant medium: book/manuscript/periodical/image
Scale: 101 monographs + 31 manuscripts + 7 serial titles.
Enumeration: provider XLSX book-title list + serial list.
Access: provider pointer/request.
Rights: rights-review.
Semantic seeds: Chinese Christianity, Christianity and Chinese religion, theology, Buddhism-Christianity encounter, Hong Kong, Tao Fong Shan.
Projection: Curated Collections + Spectrum + Three Morning Stars.
State: enumerable.

### CN-YALE-SBOFM
Provider: Yale Divinity Library / Studium Biblicum OFM
Collection: 思高聖經學會 translation documentation
Dominant medium: manuscript/book
Scale: 32 manuscript volumes + 29 Chinese Bible books + directories.
Enumeration: provider PDFs/lists.
Access: provider pointer/request.
Rights: rights-review.
Semantic seeds: Scripture, Bible translation, Chinese Bible, textual history, Catholic biblical scholarship.
Projection: Curated Collections + Spectrum + Three Morning Stars.
State: enumerable.

### CN-YALE-TLC
Provider: Yale Divinity Library
Collection: Taiwan Lutheran Church / 基督教台灣信義會
Dominant medium: periodical/book
Scale: 43 local church publication volumes + 5 anniversary volumes + 27 annual reports + 60 newsletter issues + 345 播種者 issues.
Enumeration: provider title-list PDF + serial ranges.
Access: request/pointer.
Rights: rights-review.
Semantic seeds: Lutheran history, Taiwan Christianity, church life, ministry.
Projection: Spectrum.
State: enumerable.

### CN-ARSI-JAPSIN
Provider: Archivum Romanum Societatis Iesu (ARSI)
Collection: Japonica-Sinica I–IV Chinese materials
Dominant medium: early printed book/manuscript
Scale: collection catalog; around 580 titles including duplicates/reprints/editions, about 520 Chinese; some digital texts exposed online; around 100 texts published in facsimile edition.
Enumeration: descriptive catalogue + Chinese Christian Texts database + provider digital list.
Access: mixed digital/pointer.
Rights: item-level rights/capability review; do not infer rehost from online access.
Semantic seeds: Ming-Qing Christianity, catechism, prayer, Christology, ritual, philosophy, science, Chinese Christian authors, Jesuit mission, translation.
Projection: Curated Collections + Spectrum + Three Morning Stars.
State: enumerable/catalog-query.

### CN-CCT-MINGQING
Provider: 漢語基督教文獻館 / Catalogue of Chinese Christian Texts
Collection: 明清基督宗教漢語文獻總書目
Dominant medium: bibliography/text
Scale: broad catalogue of Christian texts in Chinese during Ming/Qing.
Enumeration: downloadable catalogue + web records.
Access: bibliography/discovery pointer.
Rights: catalogue authority only unless item source independently grants access/rehost.
Semantic seeds: Ming-Qing Christianity, authors, works, editions, translation, theology, prayer.
Projection: discovery bridge primarily; downstream Spectrum/Three Morning Stars after reconciliation.
State: enumerable.

## B. Large catalog-query pools

### CN-YALE-CHINESE
Provider: Yale University Library Chinese Collection + Divinity Library
Dominant medium: book/research/primary source
Scale: major North American Chinese collection; strengths include religion, history, archaeology, art history, literature and language; Divinity Library specifically collects Chinese Christianity.
Enumeration: library catalogue/database query.
Rights: bibliographic authority; access/rehost separate.
Semantic seeds: religion, Chinese Christianity, archaeology, history, art/architecture.
Projection: Spectrum + Three Morning Stars + Curated Collections discovery.
State: catalog-query.

### CN-YALE-DAYMISSIONS
Provider: Yale Divinity Library
Collection: Day Missions / China Records / missionary documents and records
Dominant medium: archive/periodical/image
Enumeration: finding aids, annual reports, periodical title lists, organizational archives, personal papers.
Rights: archive-level/item-level review.
Semantic seeds: missions, China Christianity, people, institutions, places, church history.
Projection: Curated Collections + Spectrum; AV subsets → Cinema.
State: catalog-query.

### CN-RICCI-ARCHIVE
Provider: Ricci Institute at Boston College
Dominant medium: rare book/manuscript/archive/photo
Enumeration: archive/finding-aid research.
Rights: provider/item review.
Semantic seeds: Jesuits in China, Chinese Christianity, rites, missionary sites, manuscripts, historical images.
Projection: Curated Collections + Spectrum + Three Morning Stars.
State: catalog-query.

## C. Visual / AV pool separated from text pools

### CN-YALE-CHRISTIANITY-VISUAL
Provider: Yale Divinity Library Digital Collections
Subcollections: Divinity Library Photographs; former China Christian Colleges and Universities Image Database; Lin Collection of Lantern Slides and Photographs; International Mission Photography Archive; relevant United Board AV materials.
Dominant medium: image/AV
Enumeration: collection/finding-aid and digital-collection records.
Rights: item-level review.
Semantic seeds: Chinese Christian institutions, missions, education, architecture, people, places, historical periods.
Projection: Curated Collections first; moving-image/audio candidates → Cinema.
State: catalog-query.

## Pool priority order

Priority is based on machine-enumerability + Chinese value + ability to strengthen existing Dawn semantic roots, not raw collection size alone.

1. CN-YALE-CCLC
2. CN-YALE-SBOFM
3. CN-ARSI-JAPSIN
4. CN-CCT-MINGQING
5. CN-YALE-REICHELT
6. CN-YALE-HLTS
7. CN-YALE-TLC
8. CN-YALE-FMC
9. CN-YALE-CBC
10. CN-YALE-CHRISTIANITY-VISUAL
11. CN-YALE-DAYMISSIONS
12. CN-YALE-CHINESE
13. CN-RICCI-ARCHIVE

## Deduplication rules before admission

- Normalize traditional/simplified Chinese for matching while preserving provider title form.
- Normalize punctuation, full-width/half-width characters, whitespace and common romanization variants.
- Match on title + author/editor/translator + approximate date + provider identifier; edition-level differences remain edition evidence rather than automatically creating new Work identity.
- Serial issues reconcile first to serial identity, then issue identity; do not inflate canonical Work count by treating every issue as a new conceptual Work unless the canonical model explicitly requires it.
- Manuscript, facsimile, scan and modern reprint of the same intellectual Work must not silently create parallel Works.
- Provider collection membership is provenance, never identity authority.

## Acquisition output buckets

Every enumerated candidate must end in exactly one operational bucket:

1. `MATCH_EXISTING` — enrich existing canonical Work/resource.
2. `NEW_WORK_CANDIDATE` — survives reconciliation and proceeds through admission.
3. `EDITION_OR_RESOURCE` — new edition/image/manuscript/video/pointer for an existing Work.
4. `RIGHTS_DEFERRED` — useful candidate but capability unresolved.
5. `POLICY_REJECTED` — violates standing collection policy.
6. `DUPLICATE` — no new canonical/resource value.

## Immediate next execution

Do not discover another broad source family before processing these pools. Next operation is bulk enumeration of the highest-priority enumerable pools into normalized candidate rows, then reconciliation against the 203,448 canonical Works. Growth is reported only after canonical admission; discovery counts remain separate.
