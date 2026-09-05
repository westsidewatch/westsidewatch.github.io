# DORÉ DESIGN 2.0 interaction dependency lock

Production rule: no `latest` CDN URLs and no remote runtime dependency.

Approved upstreams:
- `moveable` — Daybrush — MIT — pinned baseline `0.53.0`.
- `selecto` — Daybrush — MIT — pinned baseline `1.26.3`.

Integration policy:
1. DORÉ owns canonical document state; interaction libraries are replaceable projections only.
2. Obtain exact tagged browser distributions and record SHA-256, upstream tag/source and license/NOTICE before activation.
3. Serve only local vendored/bundled copies from Resident; never fall back to CDN.
4. Adapter feature-detects the verified local library and may fall back to DORÉ's zero-dependency pointer implementation.
5. Published pages never include Moveable/Selecto or any editor runtime.
6. Penpot, OpenPencil, Puck, GrapesJS and similar systems remain harvest/reference sources unless a later ADR proves a bounded component dependency is necessary.
