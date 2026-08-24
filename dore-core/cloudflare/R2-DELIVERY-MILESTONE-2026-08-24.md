# Doré / ONE — Private R2 Delivery Milestone

Status: **COMPLETE / PASS**
Date: 2026-08-24

## Result
Cloudflare R2 `westside-assets` is now the canonical binary backend for the migrated Priority A ONE media set. R2 remains private; browser/product delivery is mediated by the Pages Function `/api/dore/assets/file?code=<ASSET_CODE>` and resolved through D1 `asset_registry`.

## Production acceptance
- Private R2 delivery endpoint deployed and reachable.
- 7/7 canonical migrated assets delivered through the endpoint.
- 7/7 delivered bytes matched their registered SHA-256 values.
- ONE page HTTP verification passed.
- Active ONE references were switched from GitHub binary paths to stable asset-code delivery URLs.
- Post-switch reference audit found 0 active GitHub references to the seven rollback binaries.
- 7 GitHub rollback binaries were removed only after R2 delivery verification.
- Post-removal R2 delivery verification passed 7/7.
- Canonical Doré Original Library 001–241 was not modified.

## Runtime files switched
- `static/one/one-baptism-motion.js`
- `static/one/one-baptism-motion.css`
- `static/one/one-studio-assets.js`
- `static/one/one-cover-policy.js`
- `content/website/dore.md`

## Governance
- Stable public identity is `asset_code`, not an R2 object path.
- D1 owns storage locator/hash/metadata; R2 owns the media binary.
- R2 public bucket access remains unnecessary and disabled by design.
- Historical publisher receipts may retain old source-path evidence; they are archival records, not runtime references.
- Original Doré 241 source library remains source-locked and outside this migration.

## Evidence
- `receipts/R2-DELIVERY-MILESTONE-PASS.json`
- `receipts/R2-CUTOVER-REFERENCE-AUDIT.json`
- `receipts/R2-POST-DELIVERY-CLEANUP-RESULT.json`

## Deferred to later milestones
- Priority B shared site/UI images.
- Journal media.
- Liming Library media.
- Search/corpus structured data runtime.
