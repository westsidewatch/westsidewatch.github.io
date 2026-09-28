# Westside Resource Authority Audit

Status: framework-rebuild migration authority

This audit defines what belongs in Westside Core, what remains owned by a public surface, and what remains runtime/tooling infrastructure. It precedes physical migration and framework replacement.

## A — Westside Core canonical shared authority

These records are reusable facts/resources and must have one canonical identity independent of presentation surface.

### Biblical / knowledge entities
- Scripture coordinates and canonical Bible references.
- Biblical events.
- Biblical people.
- Biblical places and geographic entities.
- Themes and cross-reference relations.
- Historical/background entities intended for reuse across Emmaus, Journal, Cinema, Bookshop, Olive Mountain and Search.
- Existing `data/bible-index/` is therefore a Core candidate and should be adapted/linked, not rebuilt as an Emmaus-private database.

### People / ministry entities
- Speakers, pastors, teachers, authors.
- Ministries, churches and organizations when represented as knowledge entities.
- Series identities and teaching-series metadata.
- Shared authority aliases and canonical naming records, including reusable material currently represented by `data/context-authority-entities.v1.json`.

### Reusable resources
- Video and sermon source records.
- Audio.
- Books/works when the record is reusable outside Dawn Bookshop.
- Articles when reused across surfaces.
- Images/illustrations when treated as reusable resources.
- Maps and geographic media.
- Manuscripts/documents.
- External-source provenance, rights, language and authority metadata.
- Relations among all of the above.

### Existing data families requiring Core review
- `data/bible-index/` — shared by nature; adapt/link into Core.
- Cinema canonical video/resource records and reusable video moments/Scripture relations — migrate canonical knowledge/resource portions to Core.
- Existing old `data/dawn-resource-corpus/` and `data/dawn-corpus/` — audit item by item because old Dawn naming mixed Bookshop and site-wide meanings.
- Shared authority/entity files — consolidate where genuinely cross-surface.

## B — Surface-owned editorial / product authority

These records define how a surface publishes, selects, orders or presents Core resources. They do not move into canonical shared-resource authority.

### LivingWaterWest
- Institutional page composition.
- Church-specific navigation/presentation.
- Surface interaction configuration.

### Journal
- Publication / issue / section / story structure.
- Edition snapshots.
- Editorial sequencing.
- `journal:adullam` and `journal:emmaus` selections.
- Article layout and issue-specific embeds.

### Dawn Bookshop / 黎明書局
- Shelves, reading paths, editorial selections, Bookshop-specific catalog presentation.
- Book acquisition/review workflow specific to the Bookshop.
- Large OpenLibrary-derived working sets remain Bookshop-owned unless/until individual reusable canonical work/entity records are promoted to Core.
- Files such as `data/dawn-10k-openlibrary-works.json`, `data/dawn-10k-work-queue.json` and `data/dawn-resource-queue.json` must NOT be bulk-moved into Westside Core merely because their contents concern books.

### Paradise Cinema / 天堂電影院
- Programmes, screenings, featured work, viewing journeys and Cinema presentation state.
- Player/view interaction configuration.
- Cinema may consume canonical videos from Core but does not own the canonical video corpus.

### Olive Mountain / 橄欖山
- Public knowledge/ministry navigation.
- Editorial groupings of sermons, speakers, ministries, theology and teaching.
- `中文講道` is a content classification/search facet, not a surface identity.

### Daylight Café / 白晝咖啡館
- Christian-life editorial sections, selections and future community presentation.
- Future forum/member/thread operational data is a separate application domain, not Core resource authority by default.

### Emmaus / 以馬忤斯
- Bible-study navigation and study-oriented selections.
- ONE and Doré Folio tool presentation/integration.
- Emmaus does not own duplicate Scripture, people, places, maps, sermons or books.

## C — Runtime / tooling / queue authority

These are operational artifacts and must stay outside Westside Core canonical resources unless a deliberately published artifact is promoted later.

- Doré upload/runtime state.
- A2A/Gateway state.
- GitHub deployment triggers.
- CI/Gate state.
- Work queues and ingestion queues.
- Generated caches.
- Acceptance/test corpora whose purpose is tooling validation rather than publication knowledge.
- Player/session state.
- Tool-specific user/study state.
- Temporary generation artifacts.

Existing `.dore-upload/`, deployment trigger files, workflow state and queue-oriented files are explicitly excluded from Core resource migration.

## Migration rule

Do not migrate directories by name. Migrate records by authority.

For every legacy record ask:
1. Is this a reusable fact/resource independent of a surface? -> Westside Core.
2. Is this a publication selection/order/layout/product decision? -> owning surface.
3. Is this operational state, queue, cache, test or tooling data? -> runtime/tooling layer.

## First framework-rebuild sequence

1. Freeze this authority boundary.
2. Establish real Westside Core subdirectories for resources, entities, relations and provenance.
3. Adapt existing Bible Index and shared authority entities without breaking current consumers.
4. Promote reusable video/sermon records; expose primarily through Olive Mountain while retaining Cinema/Journal/Emmaus consumption.
5. Separate Dawn Bookshop canonical reusable work records from Bookshop queues/catalog workflow.
6. Generate scoped indexes.
7. Migrate consumers one surface at a time.
8. Only after data authority is stable, replace the publication engine/framework and retire legacy paths.

## Non-negotiable invariant

A framework rebuild must not decide resource ownership. Resource authority is defined here first. The new framework consumes Westside Core and surface-owned editorial data; it does not recreate private copies of shared resources.
