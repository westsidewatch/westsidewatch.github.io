# Doré Search v1 — Shared Discovery Layer

Status: Phase 0.3 / architecture contract
Parent: Dawn Library Genesis Project #273

## Why this exists
Doré Search is not a Dawn Library search box. It is a shared discovery organ for Doré, Dawn Library, ONE, Journal and future Knowledge Brain/Long-Term Memory.

The historical Dawn Library architecture already required a shared resource layer and search, while the living-resource model required resources to be repeatedly mobilized into Morning Star, Spectrum, Collections and downstream content. Doré Search makes discovery reusable instead of rebuilding search per product.

## Product invariant
Search must be able to move from retrieval into context:

`query -> understand intent/entities/question -> search internal + external sources -> normalize/provenance -> dedupe -> detect curated context -> rank/routes -> return evidence + exploration paths`

A Curated Set is not merely a result card. When a query matches an existing curated knowledge context, Search may route into that context and answer/explore inside it.

## Source lanes
### Internal
- Dawn Library Resource Master / future catalog
- Morning Star selections and reasons
- Spectrum structures
- Curated Sets
- ONE
- Journal
- Doré Knowledge Lab / Skills / failure and experience memory where appropriate

### External federation — free/public/local-first
Initial qualified providers:
- Open Library — book/work/edition/author/subject discovery. Use low-volume real-time API, cache results, do not use it as a bulk backend.
- DOAB — open-access book metadata via OAI-PMH; metadata feeds are CC0.
- Crossref — public scholarly metadata search/filter/facet, no signup required for REST API.
- OpenAlex — scholarly graph/discovery candidate; keep free-tier dependency non-critical.
- Library of Congress — books/maps/manuscripts/photos and cultural-heritage discovery candidate.
- IIIF providers — manifests/collections for cultural objects and images.
- Zotero Local API — future local stewardship/catalog lane, only after local capability is verified.

No paid AI API is allowed as a required search dependency.

## Normalized result envelope
Every provider adapter should normalize into a common evidence envelope rather than forcing one universal bibliographic schema:

- result_id
- source_provider
- source_record_id
- canonical_url
- title
- creators[]
- resource_type
- language[]
- publication/date
- identifiers (ISBN/DOI/OLID/OCLC/etc.)
- subjects/topics[]
- abstract/description (when licensed/available)
- access (open/borrow/metadata-only/local/etc.)
- rights/license
- provenance: provider, retrieved_at, source URL/record, transformations
- relationships[]
- internal_matches[]
- curated_set_matches[]
- morning_star_matches[]
- confidence is about record matching/normalization, NOT theological/editorial truth

## Search modes
1. `DISCOVER` — broad discovery across lanes.
2. `LOOKUP` — exact ISBN/DOI/title/person/resource lookup.
3. `EXPLORE` — expand a question into related people, texts, maps, works, topics and paths.
4. `CURATED` — detect/use existing Curated Sets as knowledge context.
5. `INTERNAL` — search only Westside/Doré knowledge.
6. `VERIFY` — cross-source identity/provenance verification before catalog admission.

## Routing principle
Do not call every provider for every query. Route by intent/resource type and cost. Prefer local/internal first when the question is about known Westside knowledge. Use external federation for discovery or verification. Cache external metadata. Heavy/bulk harvesting is a separate ingestion process, not interactive Search.

## Editorial separation
Retrieval relevance must never silently become editorial judgment.
- Search finds and verifies candidates.
- Morning Star selects/recommends under an explicit editorial lens.
- Spectrum exposes truth/learning structure.
- Curated Sets construct knowledge context and learning paths.
- Permanent Three Morning Stars represent collection/canonical status, not search score.

## Doré Brain relation
Search is the recall/discovery pathway, not the memory store itself. Long-Term Memory may later use Search to reactivate semantic, episodic, procedural and curated-context structures. Search results become memory only after the appropriate evidence/editorial/learning process.

## Minimal engineering sequence
1. provider registry + normalized result envelope
2. internal search adapter
3. Open Library adapter as first external book-discovery experiment
4. DOAB + Crossref adapters
5. dedupe/identifier resolver
6. query router
7. curated-context detector
8. provenance/evidence output
9. acceptance tests using real biblical/theological queries
10. only then connect Dawn Library UI

## Acceptance for v1
A single query can return normalized, provenance-preserving results from at least one internal source and two external source families; duplicate works can be recognized by identifiers/strong matching; Curated Set matches are surfaced separately from ordinary results; no paid API is required; repeated calls can be cached; failures in one provider degrade gracefully rather than fail the whole search.

## Learning record
This architecture was not started by writing a generic search box. It followed: recover Dawn Library DNA -> research mature free discovery sources -> distinguish editorial curation from retrieval -> identify Search as a reusable Doré capability -> define source/routing/evidence contracts -> smallest adapter experiment. This sequence is part of the material Doré should later learn from.