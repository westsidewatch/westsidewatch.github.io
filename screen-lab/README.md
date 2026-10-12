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

## Automated checks

GitHub Actions workflow `.github/workflows/screen-lab-smoke.yml` runs `node --test screen-lab/tests/catalog.test.mjs` for changes to this experiment. This verifies structural and catalog contracts only. It does **not** prove browser rendering, external poster availability, video licensing, network access, or successful HLS playback.

Current curated film records are verified as Blender film titles from the official Blender Studio film index. Their official source pages are linked, but actual poster files and embeddable player URLs have not been verified. Do not label them as playable until browser QA confirms it.

## First verified-pedigree poster

Big Buck Bunny poster: Wikimedia Commons file `Big_buck_bunny_poster_big.jpg`; Blender Foundation; CC BY 3.0. The catalog stores attribution, source, and license URL alongside the poster. Browser rendering of the remote image still requires QA. Other films intentionally keep abstract fallback artwork until provenance and image access are checked. The main site is unchanged.

## Official embedded playback candidate

Big Buck Bunny now links to Blender's public PeerTube video and provides an iframe candidate at `https://video.blender.org/videos/embed/bf1f3fb5-b119-4f9f-9930-8e20e892b898`. PeerTube documents the `/videos/embed/<uuid>` route. The player is loaded only when the user clicks to play, and removed when the detail dialog closes. Embed URLs are restricted to `video.blender.org` and UUID-form paths. **Actual iframe playback and permission to embed must still be confirmed in a browser.** This is not a direct .mp4/.m3u8 stream and does not offer downloading.

## Browser evidence and release gate (2026-10-12)

Chromium desktop/mobile tests and the Big Buck Bunny poster load passed. The Blender PeerTube embed endpoint responded, **but real playback was not confirmed** (`paused=true`, `readyState=0`). The ordinary smoke suite remains a UI/endpoint smoke suite and must not be represented as playback certification. Run `SCREEN_LAB_REQUIRE_PLAYBACK=1 npx playwright test screen-lab/tests/browser.spec.cjs` to turn the real-playback observation into a hard failure until actual `video.currentTime` progression is confirmed. Do not merge this experimental PR on the assumption that its film playback works.
