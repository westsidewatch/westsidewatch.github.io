# Doré Screen Lab — experimental catalog

This project is intentionally separate from the main site's Paradise Cinema. It reuses shared Design OS assets, but has no entry in the site's navigation or cinema catalog.

## Catalog import

Choose a local JSON file on /screen-lab/; the browser reads it in memory. The file is not uploaded or persisted. Format:

```json
[
  {
    "title": "Example Film",
    "type": "紀錄片",
    "year": "2026",
    "description": "Synopsis",
    "poster": "https://example.org/poster.jpg",
    "stream": "https://example.org/video.m3u8",
    "source": "https://example.org/official-page"
  }
]
```

Allowed categories: 電影, 劇集, 紀錄片, 動畫, 短片. Poster and source URLs must be HTTPS. Stream URLs must be direct HTTPS .m3u8, .mp4, .m4v, .webm, .ogv or .ogg media. Providing a URL does not verify rights, CORS, reachability, or playback. The page does not scrape third-party sites or circumvent DRM. Stream playback buffers media normally but does not offer a download function.

The twelve initial cards are **design placeholders**, not actual films. Real cover art and verified stream entries are not yet included.

## QA before merge

1. Confirm /cinema/ and its navigation remain unchanged.
2. Confirm no main-site link to /screen-lab/.
3. Confirm responsive poster grid, search, category filters and detail modal.
4. Import a small authorized catalog JSON; verify poster fallbacks and source handoff.
5. Test an authorized HTTPS HLS and MP4 stream in browsers with differing HLS support; verify error handling and stop cleanup.
6. Confirm shared design tokens resolve correctly; fallback styles should remain readable.

## Browser-side editing

The Add a Film form accepts a title, category, year, HTTPS poster URL, optional direct HTTPS media URL, official source URL, and synopsis. Entries appear immediately in the grid and are kept only in page memory. Use **Export JSON** to save catalog metadata and **Load JSON** to re-import it later. The export contains no video data and excludes the twelve concept placeholders.

A valid HTTPS URL is not proof that its poster is available, that its video is playable, or that the user has redistribution rights. All media must be tested in the target browser. The player reports actual `playing`, `waiting`, `error` and `ended` events rather than assuming that a URL loads successfully.

### Pending acceptance

- Run browser-level responsive and keyboard tests on the PR preview.
- Check cross-origin poster loading and real HLS/MP4 playback against an authorized test source.
- Replace concept entries only with genuine, permissioned titles and poster sources.
- Confirm the existing site remains unlinked to this experiment.
