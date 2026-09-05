# DORÉ DESIGN 2.0 interaction dependency lock

Production rule: no `latest` CDN URLs and no remote runtime dependency.

Approved upstreams:

- `moveable` — Daybrush — MIT — target/pinned baseline `0.53.0`.
- `selecto` — Daybrush — MIT — target/pinned baseline `1.26.3`.

The versions above are the last tagged releases verified during the 2.0 engineering pass from the upstream GitHub release records. The current upstream repository may contain newer development code; DORÉ does not follow `master` at runtime.

Vendoring gate before activation:
1. Obtain the exact tagged browser distribution from upstream/package artifact.
2. Record SHA-256, upstream URL/tag and license text in this directory.
3. Serve only the local copy from Resident.
4. Adapter feature-detects the local library and falls back to DORÉ's zero-dependency pointer adapter if absent or invalid.
5. Published pages never include Moveable/Selecto.

This file intentionally does **not** claim a vendored binary exists yet. A missing verified artifact must never be replaced by a CDN fallback.
