# Westside Surface Responsibility Map

Status: canonical architecture rule

## Core rule

Pages and sections do not own shared resources. Shared resources belong to Westside Core. Surfaces own only selection, ordering, editorial context, interaction and presentation.

A resource must not be renamed or duplicated merely because a surface consumes it.

## Shared foundation — Westside Core

Westside Core is the neutral site-wide resource authority for books, video, audio, images, maps, manuscripts, articles, sermons and future resource types. It does not belong to any publication surface.

Shared entities include speakers, authors, ministries, churches, biblical persons, places, scripture coordinates, series and themes. Shared relationships connect resources to entities. Provenance, authority, language and rights travel with the resource.

Consumers must query scoped indexes/selections. A page must not load the complete resource corpus by default.

## First-level public surfaces

### LivingWaterWest
Official institutional presence for Living Water Assembly West. `LivingWaterWest` is the canonical visible surface name; legacy filesystem and URL paths may remain during migration.

### Magazine / 西望雜誌
The canonical Westside Watch magazine/publication surface. Owns issues, sections, stories, editorial sequencing and edition snapshots. It references Westside Core resources but does not own them.

`Journal` is now a legacy migration alias only and must not be presented as the first-level public identity.

#### Adullam Cave / 亞杜蘭洞
A Magazine section and editorial surface. It may select and embed sermons, video, books and other Westside Core resources. It is not a Chinese-sermon resource collection and must never rename imported ministries/channels as Adullam resources. Canonical internal identity: `magazine:adullam`; legacy alias `journal:adullam` may remain during migration.

#### Emmaus / 以馬忤斯 — Magazine section
The Magazine may retain a section named 以馬忤斯. This is distinct from the first-level Bible-study surface. Canonical internal identity: `magazine:emmaus`; legacy alias `journal:emmaus` may remain during migration. Visible naming may be identical to the first-level Emmaus surface.

### Dawn Bookshop / 黎明書局
Books-and-publications surface. Its public responsibility is books, authored works, editions, publications, authors, shelves, reading paths and editorial book/publication selections. Scripture datasets, Bible maps, Bible geography, lexicons, cross references, Bible-study websites and general study/reference resources are presented through Emmaus instead. A Bible commentary or authored Bible publication may still appear here as a book/publication and simultaneously be surfaced contextually in Emmaus.

### Paradise Cinema / 天堂電影院
Viewing and audiovisual curation surface. It selects shared video/media resources and builds programmes, features and Bible-world viewing experiences. It does not own the canonical video corpus.

### Olive Mountain / 橄欖山
Knowledge and ministry outlet. Primary public surface for Chinese sermons, teachers, ministries, teaching series, biblical teaching, theology and structured ministry knowledge. `中文講道` is a content classification, not a public surface name.

### Daylight Café / 白晝咖啡館
First-class site section for Christian life information: family, work, reading, music/film, city life, events and practical Christian living. Future community capabilities may include comments, discussion, members, threads and forum functions.

### Emmaus / 以馬忤斯 — Bible-study surface
First-level public surface for everything explicitly organized around Bible study. Emmaus is the visible navigation identity; ONE is no longer a first-level surface.

Emmaus is the primary presentation surface for ONE, Doré Folio / 多寫, Scripture and translations, Bible-study materials/websites, biblical people and places, historical/background material, maps/routes/geography, lexicons/language data, cross references and Gospel harmony. Emmaus does not own duplicate resources; it organizes Westside Core resources through a Bible-study context.

### Search
Cross-site discovery consumer over Westside Core indexes and publication indexes.

## Tool identities below surfaces

`ONE` and `Doré Folio / 多寫` are tools within Emmaus, not first-level public surfaces. Their existing paths may remain during migration.

## Presentation routing rule

- Book / authored publication -> Dawn Bookshop.
- Scripture / translation / Bible map / Bible place / lexicon / cross-reference / Bible-study dataset or website -> Emmaus.
- Sermon / ministry / teacher / teaching series -> Olive Mountain.
- Film/video as viewing programme -> Paradise Cinema.
- Christian-life information -> Daylight Café.
- Magazine story/issue/section -> Magazine owns the publication context.

The same Core record may be contextually surfaced elsewhere without changing canonical ownership or primary presentation routing.

## Required flow

Source acquisition -> Westside Core Resource Registry -> Entity/Relation Graph -> Derived scoped indexes -> Editorial selections/queries -> Surface presentation

Never: Source -> private section database -> duplicated copy in another section.

## Migration principle

Resource migration is site-wide. Existing Bible Index, reusable book/video/image/map data and cross-surface relations must be audited for Westside Core. Surface-owned editorial/product data and runtime/tooling/queue data remain outside canonical shared-resource authority.

Olive Mountain is the primary public outlet for sermon/ministry/knowledge resources; Paradise Cinema may curate the same video resources; Magazine/Adullam may select them editorially; Emmaus retrieves and presents Bible-study resources through scripture/theme/place/person relations. No consumer loads the entire corpus unless explicitly building an offline index.
