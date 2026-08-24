# 黎明書局 / Liming Library — Doré Build Plan v0.1

Status: START NOW
Date: 2026-08-24
Owner: Doré / Librarian + Researcher + Curator

## Mission

Build and operate Westside Watch's reusable Scripture-centered resource institution. The library must support learning and research, ONE, Journal, Search, church ministry, visual work, language/subtitle work and social/editorial production.

## Phase 0 — Understand before expanding

Read and retain as active brand context:
- `content/about.md`
- `data/volumes/vol-00.yaml`
- `content/website/`
- `data/resources.json`
- `dore-core/README.md`
- current Doré architecture and brand-operating architecture

Produce no mass acquisition until the current system and editorial relationships are understood.

## Phase 1 — Audit existing Resource Master

Treat `data/resources.json` as the current collection seed.

For every existing resource, progressively establish or normalize:
- stable resource_id
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
- product relationships: ONE, Journal, Search, Church, Visual, Stories, Social
- Journal relationships: movement, column, interlude, cadence
- prior use / derived outputs
- review status / reviewed_at

## Phase 2 — Relationship graph

A resource is not considered fully catalogued merely because it has a category. Doré should be able to answer questions such as:
- What resources support Matthew 3 and baptism geography?
- What visual sources are safe/useful for a Selah interlude?
- What resources used by ONE can support an Elim devotional?
- Which Journal article or social item already used this resource?
- What source supports a Search/Brain answer and how authoritative is it?
- Which visual asset is public-domain, licensed, original or AI-generated?

## Phase 3 — Collection development

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

## Phase 4 — Active editorial use

Library success is measured by use, not collection size. Doré should retrieve and connect resources during real work in ONE, Journal, Search, church ministry, Visual and language workflows.

Every reviewed use should be able to return signals to the library: useful, weak, outdated, duplicate, missing context, licensing problem, better edition, new relationship or new derived asset.

## Phase 5 — Automation candidates

Once the registry and retrieval contracts are stable:
- weekly/monthly curation;
- Three Morning Stars selection;
- Journal research packets;
- daily devotional research packets and later full bounded workflow;
- ONE chapter resource packets;
- Search answer evidence packets;
- visual-source packets;
- copyright/license review queues;
- stale-link/version checks.

## Non-negotiable boundaries

- Scripture remains central; tools do not replace Scripture.
- Resource presence does not imply endorsement or truth.
- Source, interpretation, Westside editorial viewpoint and Doré inference remain distinguishable.
- Copyright/license state must be preserved for visual and textual resources.
- Doré may curate aggressively but promotes durable knowledge cautiously.
- Human authority remains for high-impact theological/editorial decisions.

## First milestone

`LIBRARY / M1 — Existing Collection Understood`

Pass when Doré can take the existing Resource Master and reliably explain what major resource groups exist, what they are for, what is missing, and how representative resources connect to at least ONE + Journal + Search/Research without inventing relationships.