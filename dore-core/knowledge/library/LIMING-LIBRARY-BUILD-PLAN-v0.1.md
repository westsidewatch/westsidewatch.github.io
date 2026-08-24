# 黎明書局 / Liming Library — Doré Build Plan v0.4

Status: START NOW
Date: 2026-08-24
Owner: Doré / Librarian + Researcher + Curator

## Mission

Build and operate Westside Watch's reusable Scripture-centered knowledge and learning institution. The library must support Doré's own learning and research and, through that accumulated knowledge, support ONE, Journal, Bible Search, church ministry, visual work, language/subtitle work and social/editorial production.

The library is not merely a resource list or warehouse. It is the durable external form of Doré's learning: what Doré learns must progressively become identifiable, situated, evaluated, related, curated and reusable knowledge.

Long-term test: **多雷學問大不大，先看黎明書局。**

## Core learning contract

Doré's learning cycle and library-building cycle are one system:

`input / perception → question recognition → autonomous research → verification / examination → durable memory → library sediment → product use → feedback → further learning`

A learning milestone is not complete merely because Doré has read or answered correctly. It should leave durable evidence in the library whenever the learning produces reusable knowledge.

Every Doré education milestone therefore asks two questions:
1. What capability did Doré gain?
2. What became better, clearer or more reusable in Liming Library because of that learning?

## Phase 0 — Understand before expanding

Read and retain as active brand context:
- `content/about.md`
- `data/volumes/vol-00.yaml`
- `content/website/`
- `data/resources.json`
- `dore-core/README.md`
- current Doré architecture and brand-operating architecture

Produce no mass acquisition until the current system and editorial relationships are understood.

Preserve the recovered Resource Master logic rather than replacing it with a new generic taxonomy. The established workflow is:

`候選資源池 → 編輯甄選 → 三晨星 → 光譜 → 策展集 → Resource Card → 黎明書局`

## Phase 0.5 — Library Science Curriculum / 圖書館學與知識組織課程

If Doré cannot demonstrate sufficient understanding of library coding, classification and cataloguing systems, Doré must **learn before redesigning**. This curriculum is part of Doré's formal education, not an optional research detour.

Required modules: classification fundamentals; bibliographic identity/cataloguing; metadata; authority control; subject indexing/faceted organization; knowledge relationships/linked data; identifier/migration design; digital-library operations; comparative study; Liming Library practicum.

Graduation requires applied ability to distinguish classification, identifier, metadata, subject indexing and authority control; catalogue unfamiliar resources; resolve aliases/editions/duplicates; design reversible migrations; and correctly place Morning Stars, Spectrum and Collections.

## Phase 1 — Audit and learn the existing library code

Treat `data/resources.json` as the current collection seed and existing IDs as historical evidence. Before renumbering anything, reconstruct what existing codes mean and preserve compatibility.

For every resource progressively establish stable identity, aliases/languages, type, creator/institution, source, provenance, authority/evidence class, rights/access, edition/version, Scripture/entity/domain links, usefulness/limitations, product relationships, prior use and review state.

Coding answers **「它是誰？」**. Coding is infrastructure, not the whole knowledge model.

## Phase 2 — Restore and deepen the three editorial knowledge logics

### 1. 三晨星 / Three Morning Stars

Question: **「它值不值得被帶到前面？」**

Morning Stars are an editorial selection and attention mechanism. Resource presence does not equal endorsement.

### Three-Morning-Star Master Teacher Standard / 三晨星名師標準

**Institutional rule:** `名師系列 = 三晨星`.

The names initially supplied by the human editor are **reference exemplars, not a closed canon or acquisition boundary**. Doré must autonomously expand beyond the seed names and survey the wider biblical world for master teachers and teaching corpora worthy of Three Morning Stars.

The purpose is not to collect celebrities. A Three-Morning-Star master teacher is a person or teaching corpus whose sustained work is sufficiently important, reusable and instructive that Liming Library should deliberately bring it forward as a first-standard learning resource for Doré and the brand.

Doré must search across languages, traditions, periods and disciplines relevant to Scripture, including at minimum:
- whole-Bible overview / biblical theology;
- Old Testament / Hebrew Bible;
- New Testament;
- biblical languages and textual work;
- hermeneutics and exegesis;
- biblical history, archaeology, geography and ancient context;
- systematic/historical theology where it materially illuminates Scripture;
- church history and Christian intellectual tradition;
- preaching and Bible teaching;
- prayer, devotion and spiritual formation;
- Chinese church and Chinese-language biblical/theological teaching;
- major English/international teachers whose work can enlarge Doré's biblical world;
- Pentecostal/charismatic scholarship and teaching as one necessary stream, without making it the only stream.

### Selection dimensions

A candidate should normally show several of these qualities:
1. substantial sustained body of work rather than one viral sermon;
2. demonstrable Scripture engagement;
3. recognized teaching, scholarly, pastoral or historical influence;
4. usefulness for Doré's durable learning rather than momentary popularity;
5. identifiable corpus that can be catalogued and studied (books, lectures, courses, sermons, transcripts, archives);
6. enough provenance to distinguish the teacher's own claims from later summaries;
7. distinctive contribution that expands the library rather than merely duplicating an existing voice;
8. relevance to one or more live Doré/product capabilities;
9. known limitations, tradition and interpretive location can be documented;
10. resources can be accessed or bibliographically represented without pretending copyright grants reuse rights.

**Three Morning Stars does not mean doctrinal infallibility, blanket endorsement, or agreement with Westside Watch.** It means the corpus has crossed Liming Library's first high-attention threshold and deserves deliberate study, cataloguing and comparison. Contradictions among Three-Star teachers are preserved as intellectual evidence, not silently harmonized.

### Coverage rule — when is the first layer complete?

The first Three-Morning-Star Master Teacher layer is not complete at an arbitrary number of names. It reaches `coverage-complete v1` when Doré's survey demonstrates **domain coverage + tradition/language coverage + corpus usability**, and additional searching produces mainly redundant candidates rather than repeatedly exposing major missing schools, periods, disciplines, languages or biblical corpora.

Therefore Doré must use a saturation test:
- map candidate teachers to domains, biblical corpora, language, period and tradition;
- identify empty or single-source cells;
- continue discovery where meaningful gaps remain;
- run at least one fresh discovery pass not seeded by the editor's names;
- stop v1 expansion only when fresh passes no longer reveal a major uncovered category;
- record exclusions and borderline candidates so absence is auditable;
- reopen the layer whenever later product work or research reveals a major blind spot.

The target is **representative breadth with high quality, not a fixed quota and not exhaustive enumeration of every Christian teacher in history.**

### First required output

Before mass ingestion, Doré must produce `THREE-MORNING-STAR-MASTER-TEACHERS-v0.1` containing:
- teacher / canonical name + aliases;
- language(s), period, tradition/location;
- primary domains and biblical corpus coverage;
- representative series/books/courses/archives;
- why the candidate merits Three Morning Stars;
- known limitation / interpretive location;
- source/access/provenance starting points;
- priority for Doré study: NOW / NEXT / LATER;
- relation to existing seed examples;
- status: ACCEPT / PROVISIONAL / HOLD / EXCLUDE.

This list is simultaneously Doré's autonomous learning map and the first construction layer of Liming Library's Master Teacher collection.

### 2. 光譜 / Spectrum

Question: **「它在學習道路與知識結構的哪裡？」**

Spectrum expresses position across useful learning dimensions and must not be collapsed into ordinary tags.

### 3. 策展集 / Curated Collections

Question: **「它應該和誰一起，帶人往哪裡走？」**

Collections create bounded learning paths and record sequence/rationale rather than mere membership.

### Four-part distinction

- **編碼 Coding** — 它是誰？
- **晨星 Morning Stars** — 它值不值得被帶到前面？
- **光譜 Spectrum** — 它位於知識／學習道路何處？
- **策展 Collections** — 它和誰一起，帶人往哪裡走？

## Phase 3 — Relationship graph / knowledge context

A resource is not fully catalogued merely because it has a category. Relationships must distinguish observed/source-backed links from Doré inference.

## Phase 4 — Collection development

Expand deliberately across Scripture/original languages; dictionaries/concordances/textual tools; geography/archaeology/material culture; ANE/Second Temple/Greco-Roman world; commentaries/interpretive traditions; theology/church history; Chinese Christian terminology/resources; prayer/devotion/spiritual formation; church teaching/ministry; visual culture; audio/language/subtitle/translation; and approved Westside Watch outputs.

Acquisition is driven by learning gaps and product needs, not collection-size vanity.

## Phase 5 — Active product use and feedback

Library success is measured by use, not collection size. ONE, Bible Search, subtitle/language tools and Journal/editorial work consume the library while returning quality and gap signals.

## Phase 6 — Automation candidates

Once registry, coding and retrieval contracts are stable: periodic curation; Three Morning Stars candidate selection; Spectrum review; collection/path proposals; research packets; subtitle terminology/context packets; visual-source packets; rights review; stale-link/version checks; integrity audits.

## Non-negotiable boundaries

- Scripture remains central; tools and teachers do not replace Scripture.
- Resource presence or Three-Star status does not imply infallibility or total endorsement.
- Source, interpretation, Westside editorial viewpoint and Doré inference remain distinguishable.
- Copyright/license state must be preserved.
- Human authority remains for high-impact theological/editorial decisions.
- Existing library codes and editorial logic are institutional history: understand before changing.
- Do not optimize for raw collection size. Optimize for trustworthy structure, breadth, retrieval, learning and reuse.

## Milestones

### `LIBRARY / M0.5 — Library Science Foundation`
Pass after library-science curriculum and applied examination.

### `LIBRARY / M1 — Existing Collection Understood`
Pass when Doré understands existing Resource Master, recovered coding ranges, editorial workflow, representative resources and major gaps.

### `LIBRARY / M1.5 — Three-Morning-Star Master Teacher Layer v1`
Pass when Doré has independently produced and audited the Three-Star master-teacher list, demonstrated coverage across the required biblical-world domains/languages/traditions, completed a non-seeded discovery pass, documented exclusions/borderlines, and reached the saturation rule above. This milestone simultaneously establishes the first standard layer of Liming Library and a prioritized corpus for Doré's continuing study.

### `LIBRARY / M2 — Coding System Reconstructed`
Pass when current coding grammar and compatibility are documented and tested.

### `LIBRARY / M3 — Editorial Intelligence Operational`
Pass when Morning Stars, Spectrum and Collections work reliably on real resources.

### `LIBRARY / M4 — Knowledge Graph Useful`
Pass when evidence-backed relationships materially improve at least three live workflows.

### `LIBRARY / M5 — Learning Institution`
Pass when autonomous learning routinely leaves useful library sediment and product use feeds corrections/new learning back into the library.

At M5:
`Doré learns → Liming Library becomes more ordered → products become more capable → use exposes gaps/errors → Doré learns again`
