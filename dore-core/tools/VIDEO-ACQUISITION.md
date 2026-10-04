# Doré Video Acquisition Adapter v0

Executable local-first acquisition chain:

`URL → route → probe/formats/download`

## Engines

- **yt-dlp** — normal webpages and ordinary media URLs.
- **N_m3u8DL-RE** — active fallback/router for direct HLS/DASH/MSS manifests: `.m3u8`, `.mpd`, `.ism` and manifest endpoints.
- **ffmpeg** — recommended for yt-dlp audio/video merge and media processing.

The normalized Doré contract remains `probe → formats → download`; engine choice stays behind the adapter.

## Local requirements

Python 3 plus `yt-dlp`. Install `N_m3u8DL-RE` on PATH to enable direct manifest acquisition. No paid API is required.

Media is written locally and must not be committed to this repository.

## Boundary

Use for public media or media the operator is authorized to save. DRM/access-control bypass is deliberately excluded.
