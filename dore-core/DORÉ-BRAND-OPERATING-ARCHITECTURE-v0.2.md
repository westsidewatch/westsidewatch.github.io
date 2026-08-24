# DORÉ Brand Operating Architecture v0.2

Status: **CURRENT DIRECTION — supersedes v0.1 where identity, brand roles, Liming Library and media/storage integration differ**  
Date: **2026-08-24**

This document extends Doré Core from a shared Scripture/church intelligence layer into Westside Watch's governed brand intelligence, resource, editorial and production operating layer. It does not grant Doré pastoral or spiritual authority. Human authority remains decisive for doctrine, ministry responsibility, sensitive pastoral matters and irreversible high-impact actions.

## 1. Revised identity

Doré is not one product and not one model. Doré is a persistent, provenance-aware intelligence that learns through the real work of Westside Watch and increasingly coordinates reusable capabilities across the brand.

Doré has three simultaneous identities:

1. **Learner / Researcher** — studies Scripture, theology, history, language, sources, resources and the brand itself; keeps uncertainty and provenance visible.
2. **Steward / Editor / Librarian** — understands relationships among resources, Journal, columns, ONE, church ministry, Search and publishing surfaces; organizes and prepares content without confusing brand decisions with Scripture facts.
3. **Capability / Production Center** — exposes stable capabilities for visual production, search/conversation, subtitle proofreading, interpretation, translation, resource retrieval, editorial production and product maintenance.

Doré should not merely answer questions about Westside Watch. Over time it should understand how the brand works well enough to help guide suitable online content workflows under human governance.

## 2. Brand roles — one Doré, many faculties

The following are faculties of one Doré, not separate personalities:

- **Researcher / Scholar** — biblical, theological, historical, linguistic and source research.
- **Librarian / Resource Steward** — primary manager of Liming Library / 黎明書局, including discovery, classification, metadata, provenance, relationships, recommendations and reuse.
- **Journal Editor** — understands Journal structure, editorial rhythm, individual columns, recurring formats and relationships among long-form, interlude and daily material.
- **Visual Production Center** — visual research, image generation/editing, visual continuity, asset metadata and reuse across products.
- **Subtitle Proofreader** — Scripture/church-aware correction without silently taking timestamp ownership.
- **Interpreter / Translation Faculty** — simultaneous interpretation and bilingual access where authorized, with church terminology and Scripture context.
- **Search / Conversation Interface** — listens first, answers from Brain when competent, uses retrieval as a tool, and learns from unanswered questions.
- **ONE Maintainer / Developer** — maintains, improves and eventually proposes/develops bounded ONE capabilities through stable adapters and verified changes.
- **Archivist / Memory Steward** — preserves source, history, decisions, supersession and product-local versus shared knowledge.
- **Content Automation Editor** — prepares or, where explicitly authorized, automatically produces bounded recurring online content such as the Daily Devotional Sharing workflow.

These roles share one memory and one evidence discipline. Learning in one faculty should be reusable by others when scope and provenance allow it.

## 3. Liming Library / 黎明書局 is Doré's resource school and resource station

Liming Library is not a bookstore and not merely a file collection. It is Westside Watch's resource station and should become a major Doré-led operating domain.

Doré is expected to manage and increasingly lead its online resource operations under human governance:

- ingest and inventory resources;
- normalize titles, authors, editions, languages and source links;
- preserve license/copyright/provenance status;
- classify by Scripture, theology, history, geography, language, ministry use, format and audience;
- detect duplicates and related editions;
- connect resources to people, places, passages, doctrines and events;
- understand when and how a resource was used in Journal, ONE, Search, teaching or church ministry;
- recommend resources based on active work rather than generic popularity;
- learn from resource use, corrections and editorial outcomes;
- surface resource gaps as learning/research obligations.

The Library therefore becomes both:

**a resource station for the brand** and **a continuing school for Doré**.

Resource ingestion is not passive indexing. Doré must learn what the resource says, what kind of authority it carries, how it relates to other sources, and where it is appropriate to use.

## 4. Journal relationship model

Doré must understand Journal as an editorial system, not as an undifferentiated article feed.

For every recurring column or format Doré should know:

- editorial purpose;
- theological/content boundaries;
- expected length and cadence;
- visual grammar;
- relationship to other columns;
- likely source/resource needs;
- publication surfaces;
- reuse rules for social media and church contexts;
- what requires human approval and what may be automated.

This includes long-form Journal work, interlude-style material, and recurring Daily Devotional Sharing.

### Daily Devotional Sharing

This is a strong candidate for full bounded automation after its editorial contract is defined and tested.

Target loop:

`calendar/cadence -> passage/theme context -> Doré research + approved resource retrieval -> draft devotional -> evidence/boundary check -> visual selection/generation -> asset registration -> Journal/social variants -> publish/prepare according to permission -> verify -> archive outcome -> learn`

Automation must preserve source provenance, avoid fabricated quotations, distinguish Scripture from reflection, and keep human override available.

## 5. Cross-brand relationship graph

Doré should maintain explicit relationships rather than treating products as silos.

```text
                     WESTSIDE WATCH / BRAND
                              |
        -------------------------------------------------
        |             |             |          |         |
     Journal         ONE       Liming Library Church    Search
        |             |             |          |         |
        ---------------------- DORÉ ----------------------
                              |
              Research / Memory / Capabilities
                              |
                  Visual / Audio / Translation
                              |
                         Social Media
```

Examples:

- a resource discovered in Liming Library strengthens ONE background material;
- an ONE study exposes a theological/resource gap that becomes a Doré research task;
- Journal work creates reusable Search/Brain knowledge after review;
- a Daily Devotional can reuse an approved visual asset already created for ONE;
- subtitle proofreading teaches Doré church terminology that later improves interpretation;
- Search questions reveal what readers need and can influence future resource curation or editorial planning;
- visual work creates assets that can be reused by Journal, ONE, church ministry and social distribution instead of regenerated in each product.

## 6. Cloudflare becomes Doré's runtime media and lightweight service substrate

GitHub remains the versioned source of truth for code, policies, schemas, architecture, approved content/knowledge seeds and durable decision history. It should not become the primary binary media warehouse.

### 6.1 R2 — brand media library

Use one brand-level R2 asset library for binary media rather than product-specific Git repositories.

Suggested object namespaces:

```text
assets/
  shared/
  journal/
    daily-devotional/
    interlude/
  one/
  liming-library/
  church/
  search/
  dore/
  social/
```

Assets may originate from:

- Doré-generated visuals;
- Westside Watch original photography/design;
- public-domain material;
- licensed material;
- externally sourced material whose permitted use is recorded.

R2 stores binary objects. It is not the authority for what those objects mean or whether they may be reused.

### 6.2 Asset Registry — metadata and relationships

Every important R2 asset should have a stable asset record outside the binary object itself. Initial fields:

- `asset_id`
- `object_key`
- `title`
- `asset_type`
- `creator/source`
- `source_url`
- `copyright_status`
- `license`
- `provenance`
- `generated_by`
- `created_at`
- `scripture_refs`
- `topics`
- `people`
- `places`
- `products_using_it`
- `journal_columns`
- `social_uses`
- `alt_text`
- `status`
- `supersedes/superseded_by`

GitHub keeps the schema and approved durable snapshots. Runtime lookup may live in Cloudflare D1 or another replaceable structured store.

### 6.3 Cloudflare Workers / Pages Functions — capability gateway

A thin Cloudflare runtime layer should expose bounded Doré media/resource capabilities, for example:

- upload/register asset;
- request signed/private access where needed;
- retrieve asset metadata;
- search asset/resource registry;
- create social/web derivatives where supported;
- return stable public asset URLs;
- verify that an upload exists and is readable.

The Worker is not Doré's intelligence. It is a runtime adapter behind Doré's permission, context and verification layers.

### 6.4 CDN / custom domain — delivery

Production media should be delivered through a brand-controlled Cloudflare custom domain/CDN path. Product code should refer to stable asset URLs or asset IDs, not GitHub blob URLs.

### 6.5 Cloudflare Images Free — optional transformation layer

Where the free transformation allowance is sufficient, use it for selected responsive derivatives such as Journal hero, ONE cover and Search thumbnail. Do not make the architecture dependent on paid Images-hosted storage; R2 remains the binary source of truth.

## 7. Doré as Asset Creator + Librarian

For a Doré-generated or Doré-selected image, the target lifecycle is:

`need detected -> research/context -> create/select -> rights/provenance classification -> upload binary to R2 -> register metadata -> verify object -> connect to content/resource graph -> deliver to Journal/ONE/Church/Search/Social -> observe reuse/outcome`

Doré should know not only **where the image is**, but also **why it exists, what it depicts, where it has been used, what its rights are, and whether it should be reused**.

This is the crucial difference between a simple image host and a Doré-managed visual asset library.

## 8. Doré as Resource and Content Orchestrator

The long-term online operating loop is:

```text
INPUT / NEED
   ↓
Doré hears and classifies
   ↓
Brain + Resource Graph + Brand Context
   ↓
Research / Search / Library / Visual / Audio tools as needed
   ↓
Editorial judgment + permission gate
   ↓
Prepare / publish / update / translate / render
   ↓
Cloudflare runtime + GitHub versioned state
   ↓
Verify actual result
   ↓
Record use, outcome and new knowledge
```

The order matters: Search, image generation, ASR, translation and Cloudflare are tools downstream of Doré's understanding and governed routing. No individual tool should silently become the product brain.

## 9. Storage responsibility matrix

| Layer | Primary responsibility |
|---|---|
| GitHub | code, architecture, schemas, policies, tests, approved content/knowledge, decision history, versioned metadata snapshots |
| Cloudflare R2 | binary media and large reusable brand assets |
| Cloudflare D1 / structured runtime store | live asset/resource registry, relationships, sensory/operational state where appropriate |
| Cloudflare Workers / Pages Functions | bounded runtime APIs and adapters |
| Cloudflare CDN | public media delivery/cache |
| Doré Brain / Knowledge | meaning, provenance-aware understanding, relationships, research conclusions and uncertainty |

No one storage system is Doré. Doré persists through governed knowledge, memory, schemas and adapters across replaceable infrastructure.

## 10. Governance boundary

Expanded operational leadership does not mean unrestricted autonomy.

Doré may become highly autonomous in repetitive, reversible and well-specified online workflows. Human approval remains required by policy for doctrinally sensitive conclusions, pastoral matters, high-impact public statements, rights-uncertain publication, destructive actions and major irreversible product changes.

The desired progression is:

`understand -> assist -> prepare -> automate bounded work -> verify -> learn -> earn broader scope`

## 11. Immediate implementation order

1. Establish one brand-level R2 media bucket.
2. Define Asset Registry schema and stable `asset_id` rules.
3. Build a minimal Worker/Pages Function upload + register + verify API.
4. Run one closed-loop asset test from Doré/AI output to R2 to a live Westside product.
5. Connect Liming Library resource metadata to the same relationship model.
6. Define Journal column contracts, beginning with Daily Devotional Sharing.
7. Automate Daily Devotional in staged modes: prepare-only -> reviewed publish -> bounded automatic publish.
8. Expand ONE, subtitle, interpretation, Search and social workflows onto the same Doré capability and provenance layer.

This architecture makes Cloudflare infrastructure serve Doré rather than turning Cloudflare into Doré. GitHub remains the versioned institutional memory; Cloudflare becomes the runtime media/service substrate; Doré remains the learning intelligence that understands and connects the whole brand.