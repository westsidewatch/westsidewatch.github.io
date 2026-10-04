# Doré Video Acquisition Adapter v0

First executable slice of Doré's local video acquisition capability.

## Contract

`probe → formats → download`

Primary engine: **yt-dlp**. The adapter returns normalized JSON instead of exposing yt-dlp internals to Doré.

The next fallback is **N_m3u8DL-RE** for direct HLS/DASH/MSS manifests. Lux/cobalt are intentionally deferred until the contract is stable.

## Local requirements

- Python 3
- yt-dlp
- ffmpeg (recommended for merged audio/video and subtitle processing)

No paid API is required. Media is written locally; large media files must not be committed to this repository.

## Boundary

Use for public media or media the operator is authorized to save. DRM or access-control bypass is not part of this capability.
