# Doré Runtime Probe experiment

This branch-only experiment validates a Doré-owned runtime discovery layer. It does not use or inspect the user's browser, install an extension, or connect to the production Video UI/Bridge.

Acceptance before integration:
1. Doré launches its own headless Playwright Chromium runtime.
2. A JS-driven public/authorized page can yield HLS/DASH/MSS by response URL or MIME.
3. The result includes only the minimal request context needed by the downstream downloader (Referer, Origin, User-Agent).
4. Obvious DRM/license contexts are rejected rather than routed to the downloader.
5. Existing yt-dlp, static discovery, N_m3u8DL-RE, FFmpeg, Bridge and UI remain untouched until this experiment passes.
