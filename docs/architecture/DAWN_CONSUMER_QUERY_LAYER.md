# Dawn Consumer Query Layer

Status: canonical consumer contract

All site surfaces access shared Dawn resources through a scoped query contract rather than knowing canonical resource file locations.

Browser entry point: `/js/dawn-resource-query.js`

Global API: `window.DawnResources`

Supported access forms:

- `query({ resource: id })` — one canonical resource through the derived by-id view.
- `query({ selection: id })` — one editorial selection.
- `query({ index: 'by-speaker', key: speakerId })` — one scoped derived index.
- Equivalent direct helpers: `resource(id)`, `selection(id)`, `index(name, key)`.

Allowed index families in v1:

- by-type
- by-speaker
- by-series
- by-scripture
- by-theme
- by-place
- by-ministry
- by-language

## Hard constraints

1. Ordinary surface rendering must not request the complete Dawn corpus.
2. Consumers must not encode paths to canonical resource files.
3. Consumers may own presentation and editorial selections, never canonical shared resource records.
4. A missing index is a build/data problem; the consumer must not fall back to loading the whole corpus.
5. Existing legacy paths may remain during migration, but new shared-resource integrations use this query layer.

## Surface intent

- LivingWaterWest: explicit editorial selections and individual resources.
- Journal / Adullam: frozen editorial selections plus individual citations/embeds.
- Dawn Bookshop: book/type/theme/author-oriented derived views and curated shelves.
- Paradise Cinema: video/type/speaker/series/scripture/theme views and programmes.
- Olive Mountain: speaker/ministry/series/scripture/theme knowledge views.
- Daylight Café: Christian-life themes, resource types and editorial selections.
- ONE: scripture/place/theme/resource lookup.
- Search: generated search indexes, never canonical-corpus page loads.

The query layer is intentionally small and framework-independent so it can operate on the current static site and remain usable when the publication engine later moves to Astro.
