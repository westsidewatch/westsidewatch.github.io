# Westside Surface Responsibility Map

Status: canonical architecture rule

## Core rule

Pages and sections do not own shared resources. Shared resources belong to Dawn. Surfaces own only selection, ordering, editorial context, interaction and presentation.

A resource must not be renamed or duplicated merely because a surface consumes it.

## Shared foundation — Dawn

Dawn is the site-wide resource authority for books, video, audio, images, maps, manuscripts, articles, sermons and future resource types.

Shared entities include speakers, authors, ministries, churches, biblical persons, places, scripture coordinates, series and themes.

Shared relationships connect resources to entities. Provenance, authority, language and rights travel with the resource.

Consumers must query scoped indexes/selections. A page must not load the complete resource corpus by default.

## Surface responsibilities

### Church
Official institutional presence. Static-first. Future interaction may be added without turning Church into a resource authority.

### Journal
Independent magazine/publication system. Owns issues, sections, stories, editorial sequencing and edition snapshots. It references Dawn resources but does not own them.

#### Adullam Cave / 亞杜蘭洞
A Journal section and editorial surface. It may select and embed sermons, video, books and other Dawn resources. It is not the name of a Chinese-sermon resource collection and must never rename imported ministries/channels as Adullam resources.

### Dawn Bookshop / 黎明書局
Reading and book curation surface. It discovers, selects and publishes editorial paths through shared resources. It must not become the universal knowledge database.

### Paradise Cinema / 天堂電影院
Viewing and audiovisual curation surface. It selects video/media resources and builds programmes, features and Bible-world viewing experiences. It must not own the canonical video corpus.

### Olive Mountain / 橄欖山
Lower-level knowledge and ministry outlet. Primary public surface for Chinese sermons, teachers, ministries, teaching series, biblical teaching, theology and structured knowledge. It relieves Bookshop and Cinema from having to expose raw knowledge/resource inventories.

Olive Mountain consumes Dawn resources; it does not own them.

### Daylight Café / 白晝咖啡館
First-class site section for Christian life information: family, work, reading, music/film, city life, events and practical Christian living. It is released from the former large-resource structure. Future community capabilities may include comments, discussion, members, threads and forum functions, but the current publication architecture remains static-first.

### ONE
Scripture-oriented consumer. Queries shared resources by book/chapter/verse, biblical event, person, place and theme. ONE does not maintain duplicate canonical copies of shared resources.

### Search
Cross-site discovery consumer over Dawn indexes and publication indexes.

## Required flow

Source acquisition -> Dawn Resource Registry -> Entity/Relation Graph -> Derived scoped indexes -> Editorial selections/queries -> Surface presentation

Never:

Source -> private section database -> duplicated copy in another section

## First migration case

Chinese sermons currently accumulated under Cinema data are the first migration corpus for Dawn Resource Registry v1.

Target behavior:
- canonical sermon/video/source records live once in Dawn;
- Olive Mountain exposes the ministry/teacher/knowledge view;
- Cinema can curate the same videos for viewing programmes;
- Journal/Adullam can select individual resources editorially;
- ONE can retrieve them through scripture/theme relations;
- no consumer loads the entire corpus unless explicitly building an offline index.
