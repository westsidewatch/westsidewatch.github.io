# Doré Offline v0.1 — Westside Watch

Independent on-demand presentation tool for Intel and Apple Silicon Macs. No changes to website source, Pages deployment or Doré AI runtime. No automatic ZIP generation.

## Usage

Copy this directory to your Mac. Python 3.8+, Git and Hugo Extended 0.167.0 are required for building a snapshot. Only Python is needed to launch a prepared snapshot. Obtain Hugo from its official release, choosing the Intel macOS build for a 2017 MacBook Pro. No automatic installation or administrator access is attempted.

Open Launch.command (or run bash Launch.command in Terminal), choose 2 while online, then choose 1 to present. Use the browser's native full-screen mode. The service binds only to 127.0.0.1:8765. Keep Terminal open; Ctrl-C stops serving. Disconnect Wi-Fi and repeat the presentation.

Cache and versions live in ~/Library/Application Support/Dore Offline. Git fetch transfers changed Git objects after initial clone; each built snapshot is separate, not a delta-compressed asset store. No background updates. A failed build before activation leaves the previous active version intact. Select an older verified snapshot from the menu. Automatic portable export is not implemented yet.

## Scope

The selected Git commit is built with Hugo production settings and loopback baseURL, then stages ONE, Olive and Shupian using relevant existing deployment steps. Same-site absolute URL mentions in text resources are localized in the generated copy only. A SHA-256 manifest and external URL audit are generated locally. Local server supports byte-range media and CSP blocks external subresources.

This is a first local-build implementation, not a byte-for-byte copy of Cloudflare or GitHub production. CI-only cached/generated clips, external CDN libraries, Cloudflare Functions/API data and remote media are not automatically captured. Static URL audit counts editorial links and is not a browser dependency audit. Do not download external media without permission. CSP can expose missing dependencies rather than mask them.

## Old Mac acceptance (not yet certified)

- Confirm P2 five entries, seven-layer transitions, Merci, white model, church 3D tour, static pages, ONE, Olive, Dawn second/third layers.
- Run with Wi-Fi disconnected; check console and network for missing local resources, external requests, WebGL errors.
- Target 60 FPS for 2D and stable >=30 FPS in 3D; run for 60 minutes. Test built-in display and projector. Record actual CPU/GPU/memory, browser and FPS; do not infer them from CI.
- Native browser only; no Electron and no AI model. Rendering presets, GPU-specific controls, external dependency capture, production artifact parity and one-click export remain follow-up work. Do not silently degrade artwork.

## Tests

python3 -m unittest discover -s local/dore-offline -p 'test_*.py' -v

Synthetic tests cover local references, checksums, loopback HTTP range, CSP and route checks. Full main-site build and physical Intel Mac acceptance are separate gates.
