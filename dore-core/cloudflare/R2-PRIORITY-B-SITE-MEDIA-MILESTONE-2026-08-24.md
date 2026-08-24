# Doré Priority B Site Media R2 Milestone — 2026-08-24

Status: **COMPLETE / PASS**

## Result

Five large raster/site media assets were migrated from GitHub to private Cloudflare R2 and registered in D1 Asset Registry:

- `SITE-BACKGROUND`
- `SITE-DAMASCUS-GATE`
- `SITE-JERUSALEM-WALL`
- `SITE-TEMPLE-STONE-LIGHT`
- `SITE-WECHAT-QR`

Runtime references were cut over to registry-driven private R2 delivery through `/api/dore/assets/site-file?code=...`. The five redundant GitHub binaries were removed only after delivery verification.

Production receipt: `dore-core/cloudflare/receipts/R2-PRIORITY-B-SITE-MEDIA-PASS.json`.

## Placement boundary retained

This milestone does **not** mean all visual assets move to R2. Code/UI/version-coupled brand assets remain in GitHub, including the Morning Star and masthead SVG family. Small fixtures that must change atomically with code also remain GitHub-owned.

The canonical Doré 241 library was not touched.

## Corrective work during execution

The original ONE migrator intentionally accepted only ONE namespaces, so Priority B site media required a separate governed site migrator and delivery route. Those production routes are retained; temporary trigger/probe workflows were removed after PASS.

## Next milestone

Inventory and classify Journal + Liming Library media under the same placement policy: deduplicate, identify canonical assets, keep code/UI-coupled identity files in GitHub, migrate appropriate content media to R2, register D1 metadata, verify delivery, then remove redundant binaries only where safe.