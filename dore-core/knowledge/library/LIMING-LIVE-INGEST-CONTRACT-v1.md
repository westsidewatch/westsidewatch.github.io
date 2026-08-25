# 黎明書局 Live Ingest Contract v1

Status: ACTIVE
Date: 2026-08-24

## Purpose

Doré must be able to turn discovery into a live, reusable library bridge without waiting for a human to hand-edit `data/resources.json`.

The live path is:

`discover → verify source → classify → write Liming Registry → build teacher/series/scripture/product edges → expose to Liming/ONE/Search → use → feedback → Doré learns`

This is the same Westside Watch bridge architecture, not a new product or a new Doré identity.

## Storage boundary

- External videos/PDFs/books remain at their original or authorized source whenever reliable linking is sufficient.
- D1 stores the bridge: identity, metadata, provenance, rights/access state, Morning Stars, Chinese accessibility, Scripture relationships and product relationships.
- R2 is reserved for Westside-owned/derived assets or materials that genuinely require durable self-hosting.
- GitHub stores contracts, schema logic, seed/audit evidence and code, not the growing live catalogue itself.

## Doré write authority

Doré may write discovered resources to the live registry through authenticated `POST /api/dore/library/resources` using the existing `DORE_HEARTBEAT_TOKEN`.

Default discovery state is `candidate`. A resource may be written directly as `published` only when the governing rule already establishes the editorial class and the source is verified sufficiently for that use. The Three-Morning-Star master-teacher layer is such a governed class, but source/rights provenance must still be recorded.

Doré must never treat `found on the web` as equivalent to `official`, `authorized`, or `safe to republish`.

## Required record

Every live resource must preserve at least:
- title
- creator/teacher when known
- series when known
- resource type
- language
- canonical/source URL
- source class (`official`, `authorized`, `institutional`, `library`, `third-party`, `unverified`)
- rights state (`official-share`, `public-domain`, `licensed`, `link-only`, `restricted`, `unknown`)
- Morning Stars level
- Chinese accessibility state
- catalogue status
- Scripture refs when identifiable
- product relations
- provenance
- discovery/verification timestamps

## Two principal reorderings

The same resource graph must support at least two product views:

1. **黎明書局** — teacher → series → work/episode/resource.
2. **ONE** — Bible book → chapter/passage → relevant resources across teachers/series.

No duplicate catalogue should be created merely to support another ordering.

## Subtitle/translation feedback

English-world resources without adequate Chinese accessibility may enter the subtitle queue with the same `resource_id`.

`Liming resource → subtitle job → transcript/proofread → translation → Scripture alignment → human review → Chinese accessibility update → library/product availability → learning feedback`

A subtitle job must not create a second unrelated resource identity when it is a derived accessibility layer of an existing library item.

## Scale objective

This live bridge is a prerequisite for large-scale Chinese accessibility work. Doré should be able to discover a Three-Morning-Star resource, catalogue it, recognize that Chinese access is missing, queue translation/proofreading work, and later return the reviewed Chinese layer to the same resource graph.
