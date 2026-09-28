# Westside Surface Responsibility Map

Status: canonical architecture rule

## Core rule

Pages and sections do not own shared resources. Shared resources belong to Westside Core. Surfaces own only selection, ordering, editorial context, interaction and presentation.

A resource must not be renamed or duplicated merely because a surface consumes it.

## Shared foundation — Westside Core

Westside Core is the neutral site-wide resource authority for books, video, audio, images, maps, manuscripts, articles, sermons and future resource types. It is not Dawn Bookshop / 黎明書局 and does not belong to any publication surface.

Shared entities include speakers, authors, ministries, churches, biblical persons, places, scripture coordinates, series and themes.

Shared relationships connect resources to entities. Provenance, authority, language and rights travel with the resource.

Consumers must query scoped indexes/selections. A page must not load the complete resource corpus by default.

## First-level public surfaces

### LivingWaterWest
Official institutional presence for Living Water Assembly West. `LivingWaterWest` is the canonical visible surface name; legacy filesystem and URL paths may remain during migration. Static-first. Future interaction may be added without turning LivingWaterWest into a resource authority.

### Journal
Independent magazine/publication system. Owns issues, sections, stories, editorial sequencing and edition snapshots. It references Westside Core resources but does not own them.

#### Adullam Cave / 亞杜蘭洞
A Journal section and editorial surface. It may select and embed sermons, video, books and other Westside Core resources. It is not a Chinese-sermon resource collection and must never rename imported ministries/channels as Adullam resources.

#### Emmaus / 以馬忤斯 — Journal section
The Journal may retain a section named 以馬忤斯. This is a publication-section identity, distinct from the first-level Bible-study surface below. Internal identifiers must distinguish them (for example `journal:emmaus` and `surface:emmaus`); visible naming may be identical.

### Dawn Bookshop / 黎明書局
Reading and book curation surface. It discovers, selects and publishes editorial paths through shared resources. It must not become the universal knowledge database.

### Paradise Cinema / 天堂電影院
Viewing and audiovisual curation surface. It selects video/media resources and builds programmes, features and Bible-world viewing experiences. It must not own the canonical video corpus.

### Olive Mountain / 橄欖山
Knowledge and ministry outlet. Primary public surface for Chinese sermons, teachers, ministries, teaching series, biblical teaching, theology and structured ministry knowledge. `中文講道` is a resource/content classification, not a public surface name. Olive Mountain relieves Bookshop and Cinema from exposing raw knowledge/resource inventories.

Olive Mountain consumes Westside Core resources; it does not own them.

### Daylight Café / 白晝咖啡館
First-class site section for Christian life information: family, work, reading, music/film, city life, events and practical Christian living. It is released from the former large-resource structure. Future community capabilities may include comments, discussion, members, threads and forum functions, while the current publication architecture remains static-first.

### Emmaus / 以馬忤斯 — Bible-study surface
First-level public surface for everything explicitly organized around Bible study. Emmaus is the visible navigation identity; ONE is no longer a first-level surface.

Emmaus contains and coordinates:
- ONE — Bible-study/navigation tool;
- Doré Folio / 多寫 — notes, writing and study-work tool;
- Scripture / 經文;
- Bible-study materials / 查經資料彙集;
- biblical people and places;
- historical/background material;
- maps;
- cross references / 串珠;
- Gospel harmony / 四福音合參;
- future Bible-study tools and study-oriented views.

Emmaus does not own duplicate scripture, map, person, place, sermon or book databases. It organizes Westside Core resources through a Bible-study context. Tool-specific state and interaction logic may remain tool-owned.

### Search
Cross-site discovery consumer over Westside Core indexes and publication indexes.

## Tool identities below surfaces

`ONE` and `Doré Folio / 多寫` are tools within Emmaus, not first-level public surfaces. Their existing paths may remain during migration; navigation and presentation should progressively expose them through Emmaus.

## Required flow

Source acquisition -> Westside Core Resource Registry -> Entity/Relation Graph -> Derived scoped indexes -> Editorial selections/queries -> Surface presentation

Never:

Source -> private section database -> duplicated copy in another section

## Migration principle

Resource migration is site-wide, not limited to sermons. Existing Bible Index, shared authority entities, reusable book/video/image/map data and cross-surface relations must be audited for Westside Core. Surface-owned editorial/product data and runtime/tooling/queue data remain outside the canonical shared-resource authority.

Olive Mountain is the primary public outlet for sermon/ministry/knowledge resources; Paradise Cinema may curate the same video resources; Journal/Adullam may select them editorially; Emmaus may retrieve them through scripture/theme relations. No consumer loads the entire corpus unless explicitly building an offline index.
