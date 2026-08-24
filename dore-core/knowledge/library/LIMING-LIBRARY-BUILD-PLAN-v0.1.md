# 黎明書局 / Liming Library — Doré Build Plan v0.2

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

## Phase 1 — Audit and learn the existing library code

Treat `data/resources.json` as the current collection seed and existing IDs as historical evidence of an emerging library coding system, including recovered ranges such as `001–021`, `021-B–029-B`, and later departmental ranges.

Before renumbering anything, Doré must reconstruct what the existing codes mean, where they are stable, where they collide or encode multiple concepts, and what migration constraints exist.

For every existing resource, progressively establish or normalize:
- stable resource_id and legacy_id / aliases where needed
- title / aliases / languages
- resource_type
- creator / institution
- source URL / canonical location
- provenance
- authority/evidence class
- copyright/license/access status
- date/edition/version where applicable
- Scripture links: book/chapter/verse/passage
- entity links: people/place/event/topic
- domain links: biblical world/history/theology/church/visual/language/etc.
- usefulness / limitations
- product relationships: ONE, Journal, Bible Search, Church, Visual, Stories, Social, subtitle/language tools
- Journal relationships: movement, column, interlude, cadence
- prior use / derived outputs
- review status / reviewed_at

### Coding-system objective

The coding system must eventually answer **「它是誰？」** reliably: unique identity, stable reference, provenance, version and migration history. Coding is infrastructure, not the whole knowledge model.

No destructive renumbering until a compatibility map and migration test exist.

## Phase 2 — Restore and deepen the three editorial knowledge logics

The existing library already defines three active organizing logics. Doré must learn them, use them in real work, and improve them from evidence rather than flattening them into ordinary tags.

### 1. 三晨星 / Three Morning Stars

Question: **「它值不值得被帶到前面？」**

Morning Stars are an editorial selection and attention mechanism. Resource presence does not equal endorsement; Morning Star selection records why a resource is unusually useful, timely, illuminating or worth presenting for a bounded context.

Doré should learn from human selections and later propose candidates with explicit reasons and confidence, while high-impact theological/editorial promotion remains human-governed.

### 2. 光譜 / Spectrum

Question: **「它在學習道路與知識結構的哪裡？」**

Spectrum is not merely a difficulty label. It should progressively express position across useful learning dimensions such as entry → intermediate → advanced → academic, while also allowing the library to distinguish kinds of engagement where evidence supports it: textual, historical, theological, devotional, practical, visual, linguistic and other meaningful axes.

Doré's task is to discover which dimensions are genuinely useful from actual library use, not to create uncontrolled metadata.

### 3. 策展集 / Curated Collections

Question: **「它應該和誰一起，帶人往哪裡走？」**

Collections create bounded learning paths. They connect resources around Scripture passages, questions, themes, people, places, historical contexts, ministry needs or editorial projects and should record sequence/rationale rather than merely membership.

### Four-part distinction

- **編碼 Coding** — 它是誰？
- **晨星 Morning Stars** — 它值不值得被帶到前面？
- **光譜 Spectrum** — 它位於知識／學習道路何處？
- **策展 Collections** — 它和誰一起，帶人往哪裡走？

Doré must progressively integrate these four functions without collapsing them into one field.

## Phase 3 — Relationship graph / knowledge context

A resource is not considered fully catalogued merely because it has a category. Doré should be able to traverse evidence-backed relationships and answer questions such as:
- What resources support Matthew 3 and baptism geography?
- What visual sources are safe/useful for a Selah interlude?
- What resources used by ONE can support an Elim devotional?
- Which Journal article or social item already used this resource?
- What source supports a Bible Search/Brain answer and how authoritative is it?
- Which visual asset is public-domain, licensed, original or AI-generated?
- Which resources explain a church/Bible term likely to be misheard in subtitles?
- What learning path should follow from a search result without pretending that retrieval itself is interpretation?

Relationships must distinguish observed/source-backed links from Doré inference. Inference may be proposed; durable promotion requires evidence appropriate to impact.

## Phase 4 — Collection development

After audit/schema stabilization, expand deliberately across:
1. Scripture texts and original languages
2. Bible dictionaries, concordances, cross references and textual tools
3. biblical geography, maps, archaeology and material culture
4. ancient Near East, Second Temple Judaism, Greco-Roman world
5. commentaries and interpretive traditions
6. theology and church history
7. Chinese Christian terminology and resources
8. prayer, devotion and spiritual formation
9. church teaching/ministry resources
10. visual culture: art history, public-domain archives, maps, manuscripts, architecture, clothing, objects
11. audio/language/subtitle/translation references
12. Westside Watch's own approved outputs as internally produced resources with provenance

Acquisition is driven by learning gaps and product needs, not collection-size vanity.

## Phase 5 — Active product use and feedback

Library success is measured by use, not collection size. Doré should retrieve and connect resources during real work in ONE, Journal, Bible Search, church ministry, Visual and language/subtitle workflows.

Product roles should remain distinct:
- **ONE** uses the library to deepen chapter study, context, maps, cross references and learning paths.
- **Bible Search** uses it to improve evidence, entity/context expansion and responsible next-step discovery without hiding the Scripture result.
- **Subtitle/language tools** use it as a church/Bible lexical and contextual authority layer for recognition, correction and disambiguation.
- **Journal/editorial work** uses it for research packets, source trails, visual provenance and curated reading roads.

Every reviewed use should return signals to the library: useful, weak, outdated, duplicate, missing context, licensing problem, better edition, new relationship, failed inference, new derived asset or new learning gap.

## Phase 6 — Automation candidates

Once registry, coding and retrieval contracts are stable:
- weekly/monthly curation;
- Three Morning Stars candidate selection;
- Spectrum placement suggestions and review queues;
- collection/path proposals;
- Journal research packets;
- daily devotional research packets and later full bounded workflow;
- ONE chapter resource packets;
- Bible Search answer evidence packets;
- subtitle terminology/context packets;
- visual-source packets;
- copyright/license review queues;
- stale-link/version checks;
- code/relationship integrity audits.

## Non-negotiable boundaries

- Scripture remains central; tools do not replace Scripture.
- Resource presence does not imply endorsement or truth.
- Source, interpretation, Westside editorial viewpoint and Doré inference remain distinguishable.
- Copyright/license state must be preserved for visual and textual resources.
- Doré may curate aggressively but promotes durable knowledge cautiously.
- Human authority remains for high-impact theological/editorial decisions.
- Existing library codes and editorial logic are institutional history: understand before changing.
- Do not optimize for number of resources, tags or graph edges. Optimize for trustworthy structure, retrieval, learning and reuse.

## Milestones

### `LIBRARY / M1 — Existing Collection Understood`

Pass when Doré can take the existing Resource Master and reliably explain:
- the major resource groups and recovered coding ranges;
- what the existing codes appear to mean and where uncertainty remains;
- the Three Morning Stars / Spectrum / Curated Collections workflow;
- what representative resources are for;
- what is missing;
- how representative resources connect to at least ONE + Journal + Bible Search/Research without inventing relationships.

### `LIBRARY / M2 — Coding System Reconstructed`

Pass when Doré can document the current coding grammar, identify collisions/ambiguities, preserve legacy compatibility, and propose a tested forward-compatible scheme without destructive renumbering.

### `LIBRARY / M3 — Editorial Intelligence Operational`

Pass when Doré can use Morning Stars, Spectrum and Collections on real resources with explicit rationale, distinguish these three functions, and pass human review without treating them as generic tags.

### `LIBRARY / M4 — Knowledge Graph Useful`

Pass when evidence-backed library relationships materially improve at least three live workflows among ONE, Bible Search, Journal, Church, Visual and subtitle/language tools, with provenance and feedback returned to the Resource Master.

### `LIBRARY / M5 — Learning Institution`

Pass when Doré's autonomous learning routinely leaves useful library sediment, library gaps can trigger new research, product use feeds corrections back into the library, and the resulting system demonstrably improves Doré's future research and product support.

At M5 the desired loop is operational:

`Doré learns → Liming Library becomes more ordered → products become more capable → use exposes gaps/errors → Doré learns again`
