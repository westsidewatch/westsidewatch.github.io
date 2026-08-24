# Doré Asset Migration Inventory — 2026-08-24

Status: ACTIVE / PHASE 1 INVENTORY

## Rule
No bulk move and no source deletion. Doré must classify first, preserve one canonical binary, migrate only when the target backend is justified, verify references, then remove redundancy separately.

## Backend policy
### KEEP IN GITHUB
Assets tightly coupled to code/UI/versioned identity:
- `static/images/westside-watch-morning-star.svg` — tiny canonical brand mark.
- `static/images/westside-watch-masthead.svg` and landscape variant — canonical brand/UI vectors; review later for SVG optimization, not R2 migration by default.
- small UI/runtime fixtures whose binary must change atomically with code.

### R2 CANDIDATE — PRIORITY A
Large, content/media assets that are growing, derivative, share-oriented, or studio-produced:
- `static/one/share/matthew-03-baptism-motion-r2.gif` — 5,463,147 B
- `static/one/share/matthew-03-baptism-motion-r3-mobile.gif` — 5,507,985 B
- `static/one/share/matthew-03-baptism-motion-r4-mobile.gif` — 4,437,855 B
- `static/one/share/matthew-03-baptism-motion-r5-mobile.gif` — 7,819,362 B
- `static/one/studio/jude-01-michael-moses-dore-studio-r2.png` — 4,357,167 B
- `static/one/studio/obadiah-01-dore-studio-r2.png` — 3,521,988 B
- `static/one/studio/revelation-02-dore-final-full.png` — 3,508,250 B
- `static/one/dore-restorations/183-john-baptist-preaching-restored-r1.png` — 3,719,279 B
- `static/one/dore-restorations/184-baptism-of-jesus-restored-r1.png` — 3,701,106 B
- `static/one/motion-assets/matthew-03-baptism-dove-removed-r1.png` — 3,656,398 B

These are first-class R2 candidates because they are media payloads rather than code-coupled UI identity.

### REVIEW BEFORE MOVING — PRIORITY B
Large shared backgrounds / site identity images:
- `background.jpg` — 2,533,396 B
- `static/images/damascus-gate.jpg` — 1,496,447 B
- `static/images/jerusalem-wall.png` — 1,002,028 B
- `static/images/temple-stone-light.png` — 2,410,484 B
- `static/wechat-qr.png` — 1,805,205 B
- ONE cover textures/frames, including `cover-texture-antique-green.png`, `cover-texture-fallback.png`, and frame PNGs.

Decision depends on whether each is canonical UI identity (GitHub) or reusable/growing content media (R2). Do not move merely because it is large.

### STRUCTURED DATA — NOT AN R2 MEDIA MIGRATION
Large JSON search/corpus artifacts such as `static/dore/search-index.json`, `static/dore/original-index.json`, `static/dore/entity-index.json`, reports and inventories require a separate data-runtime review. They may ultimately belong in D1/R2 or build artifacts, but must not be mixed with the media migration because Search depends on their access pattern and atomic build behavior.

## Immediate migration order
1. Inventory references to Priority A files.
2. Compute/record SHA-256 and canonical asset IDs.
3. Upload a single low-risk real media asset to R2 through production Asset Registry.
4. Verify R2 read/hash/metadata.
5. Switch only that asset's runtime reference.
6. Verify ONE/site rendering.
7. Keep GitHub source during rollback window.
8. Only after verification mark GitHub copy as redundant and remove in a separate commit.

## Storage namespaces
- `one/studio/...`
- `one/restorations/...`
- `one/motion/...`
- `one/share/...`
- `journal/...`
- `devotional/...`
- `library/media/...`
- `_system/...` reserved for probes/maintenance.

## Safety invariants
- One canonical binary backend per asset.
- Asset Registry owns `storage_backend`, `storage_locator`, `content_hash`, provenance, rights, preservation class and product relationships.
- Permanent/canonical assets are never auto-deleted.
- Reproducible derivatives are preferred cleanup targets.
- Migration must be reversible until runtime verification passes.
- GitHub and R2 must never silently diverge as competing masters.

## First observation
The repository already contains multiple multi-megabyte GIF/PNG media files, including four Matthew 3 share GIF revisions and several 3–4 MB studio/restoration images. This confirms R2 should first absorb growing ONE studio/share media, while small canonical brand vectors remain in GitHub.
