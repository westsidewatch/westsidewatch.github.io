# Doré Universal Source Enumerator v1

Status: ACTIVE ENGINEERING
Date: 2026-09-25

## Purpose

Close the only missing 1→N boundary in Universal Source Core.

Existing canonical contract remains unchanged:

`Probe → Capability Envelope → Universal Dispatcher → Consumer Admission`

Enumerator is a thin upstream Core capability:

`Collection / Catalog / Provider → N Source Pointers → existing Universal Source contract`

It is NOT a new ingestion pipeline.

## Core invariant

**Capability grows; operational burden shrinks.**

A new provider, catalog, playlist, archive, collection or format must not create a consumer-specific pipeline when its structure can be expressed as source enumeration plus the existing Universal Source contract.

## Input

A collection-level source claim, for example:

- catalog page
- collection landing page
- pagination root
- sitemap/feed
- structured list
- provider API endpoint
- archive index
- playlist/channel/index
- manifest containing child resources

## Output

`dore.source-enumeration.v1`

The output is request-scoped and contains only source pointers and discovery evidence required to hand each child source to the existing Probe.

Minimum child pointer:

```json
{
  "sourceUrl": "https://provider.example/item/123",
  "providerId": "123",
  "label": "optional provider label",
  "discoveredFrom": "https://provider.example/collection",
  "evidence": "link|structured-data|api|feed|sitemap|manifest|pagination"
}
```

## Hard boundaries

Enumerator MUST NOT:

- download or rehost source media;
- become canonical identity authority;
- infer rights from availability;
- perform Dawn Work/Edition/Resource admission;
- duplicate Probe extraction;
- duplicate Dispatcher routing;
- persist a second library/catalog database;
- create provider-specific consumer pipelines;
- bypass Wikisource prohibition;
- bypass Dawn relevance/editorial policy.

## Enumeration strategies

Provider-neutral strategies, attempted from strongest evidence to weakest:

1. structured collection/API records;
2. manifests/feeds/sitemaps;
3. semantic HTML item links and pagination;
4. embedded structured data;
5. runtime-required collection expansion through the existing runtime boundary.

Provider-specific knowledge may improve detection, but MUST compile into the same `dore.source-enumeration.v1` output and never leak into Dawn/Cinema/Multiwrite consumer logic.

## Deduplication

Enumeration deduplicates only source pointers/provider identities within the request. It does NOT decide whether two sources represent the same canonical Work. That remains Dawn/canonical identity authority.

## Backpressure

Large collections are streamed/page-bounded. Enumerator may emit continuation state, but consumers never need to understand provider pagination.

## Chinese acquisition consumer

Chinese acquisition becomes a workload, not an architecture:

`Chinese discovery → Enumerator → N pointers → Probe → Envelope → Dispatcher → Dawn admission → canonical delta → Resource Fabric delta`

The legacy 35-row seed materializer is not the production growth path. Reappearance of 35→21 is treated as wrong-entry regression, not progress.

## Acceptance

v1 is accepted only when all are true:

1. one collection source expands to multiple distinct pointers;
2. pointers feed the existing Probe without a new consumer-specific adapter;
3. pagination/continuation does not leak into Dawn;
4. no source body/media is stored merely to enumerate it;
5. rights remain unknown unless separately admitted;
6. duplicate collection links collapse without canonical Work inference;
7. at least two heterogeneous collection shapes pass the same contract;
8. Dawn can consume the resulting dispatches unchanged;
9. Cinema can consume video pointers unchanged;
10. the 35-row Chinese seed path is not required for production enumeration.

## First production proof

Use the already discovered Chinese source families as workload evidence. Do not create a Chinese-specific enumerator. The first proof must demonstrate collection expansion feeding Universal Source directly and report actual enumerated pointer count separately from canonical admission delta.
