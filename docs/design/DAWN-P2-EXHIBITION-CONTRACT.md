# Dawn Library → P2 curated-exhibition contract

Status: experimental, isolated P2 05 preview. This is a reusable **presentation capability**, not a second catalog or a new Design OS.

## Intent
Every approved 黎明書局「策展集」 may use the same P2 viewer and be directly browsed without hand-coding a new animation. A collection is **not** eligible merely because a folder or dataset exists; it requires verified, visual, source-linked editorial selections. Do not claim all existing collections have been migrated.

## Publish once, present anywhere
1. The editorial owner selects genuine interior images, photography, archaeological plates, manuscript leaves, maps, or other visual material from the **identified source work**. Curator confirms attribution, license, image availability, and the item's identity. No generic covers or invented pairings.
2. Publish `static/dawn-library/p2-exhibitions/<slug>.json` with `schema:"dawn.p2.curated-exhibition.v1"`, `id`, `title`, `subtitle`, `sourceCollection`, `curationStatus`, and an `items` array. Every item needs `id`, `title`, `media:{src,source,alt,type:"image"}`, `destination`, plus useful `caption`, `kind`, `workId`, `year` and rights evidence if available.
3. Register `{id,title,manifest,status}` in `static/dawn-library/p2-exhibitions/index.json`. The P2 viewer has no collection-specific JS or CSS.
4. Open `/experiments/p2-0105-dawn-preview.html?collection=<slug>&d=28.4`. The same P2 entrance renders that selection. Future integration should expose a "在 P2 中瀏覽" affordance on published collection pages; the preview remains separate until visual approval.

## Motion and access
- P2 05 uses the same approved MERSI-style clipping/translation primitive; left channel scrolls **up**, right **down**, independently, with no decorative center seam, 3D book flip, fake page borders or added linework.
- One scroll position drives both channels. Backward input restores the same image and clip. No time-based slideshow competes with the scroll owner.
- The middle two horizontal squares enter the existing chapter second layer. Selecting a left/right image goes to that artwork's **actual collection reader or source work** via `destination`, never merely to a generic homepage.
- The `media.source` records the original image/source URL, even when the preferred click route is a site-owned reading surface.
- Keyboard, source links, image failures, reduced motion, screen width and touch/scroll review are release gates.

## Example and limitation
`jerusalem-3000.json` currently contains a **first verified set of five maps** already in the site's existing `/dawn-library/collections/jerusalem-3000/maps/` reader. These are not twelve separate books. Twelve visually differentiated source-verified books/plates (photography, portraits, archaeology, art, manuscript, architecture and historical images) remain a **separate editorial curation acceptance gate**. Never promote the five-map data-bridge exercise as completion of the twelve-work exhibit.

## Acceptance
Verify all linked source images actually load and match their named work, rights/attribution, corresponding reader deep links, desktop/mobile and reverse-scroll behavior in the browser. Successful CI is not a visual acceptance.
