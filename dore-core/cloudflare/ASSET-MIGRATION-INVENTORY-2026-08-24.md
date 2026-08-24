# Doré Asset Migration Inventory — 2026-08-24

Status: **PRIORITY A COMPLETE / PRIORITY B DEFERRED**

## Closure summary

The first governed media-migration milestone is complete.

- Priority A canonical media migrated/verified in R2 + D1: **7 assets**.
- Obsolete Matthew 3 motion revisions deleted from GitHub: **3 assets** (`r2`, `r3-mobile`, `r4-mobile`).
- Priority A unresolved items: **0**.
- Canonical/active GitHub source copies retained temporarily: **7**, intentionally, because runtime delivery has not yet been switched from repository paths to an R2-backed public delivery layer. They are rollback copies, not competing masters.
- Priority B shared UI/site identity assets remain in GitHub pending a separate runtime-placement decision.
- Search/corpus JSON remains explicitly outside this media milestone.

The production PASS receipt is:

`dore-core/cloudflare/receipts/ASSET-MIGRATION-PRIORITY-ONE-RESULT.json`

## Backend policy

### KEEP IN GITHUB
Assets tightly coupled to code/UI/versioned identity:
- `static/images/westside-watch-morning-star.svg`
- `static/images/westside-watch-masthead.svg`
- `static/images/westside-watch-masthead-landscape.svg`
- small UI/runtime fixtures whose binary must change atomically with code.

### PRIORITY A — COMPLETE IN R2
The following logical assets are now registered as active R2 assets and verified searchable through the Asset Registry:

1. `ONE-MAT-03-BAPTISM-COVER-MOTION`
   - R2: `one/share/matthew-03-baptism-motion-r5-mobile.gif`
2. `ONE-JUDE-01-MICHAEL-MOSES-STUDIO`
   - R2: `one/studio/jude-01-michael-moses-dore-studio-r2.png`
3. `ONE-OBA-01-DORE-STUDIO`
   - R2: `one/studio/obadiah-01-dore-studio-r2.png`
4. `ONE-REV-02-DORE-FINAL`
   - R2: `one/studio/revelation-02-dore-final-full.png`
5. `ONE-MAT-03-JOHN-BAPTIST-PREACHING-RESTORED`
   - R2: `one/restorations/183-john-baptist-preaching-restored-r1.png`
6. `ONE-MAT-03-BAPTISM-JESUS-RESTORED`
   - R2: `one/restorations/184-baptism-of-jesus-restored-r1.png`
7. `ONE-MAT-03-BAPTISM-MOTION-SOURCE`
   - R2: `one/motion/matthew-03-baptism-dove-removed-r1.png`

All seven passed registry search verification after migration.

### OBSOLETE — REMOVED
Matthew 3 motion revisions:
- `static/one/share/matthew-03-baptism-motion-r2.gif`
- `static/one/share/matthew-03-baptism-motion-r3-mobile.gif`
- `static/one/share/matthew-03-baptism-motion-r4-mobile.gif`

Only final `r5-mobile` remains as the canonical Matthew 3 cover motion.

### PRIORITY B — DEFERRED BY DESIGN
Shared/site identity assets remain in GitHub for now:
- `background.jpg` — 2,533,396 B
- `static/images/damascus-gate.jpg` — 1,496,447 B
- `static/images/jerusalem-wall.png` — 1,002,028 B
- `static/images/temple-stone-light.png` — 2,410,484 B
- `static/wechat-qr.png` — 1,805,205 B
- ONE cover textures/frames.

These are not moved solely because of size. They are runtime/UI identity assets and must be evaluated together with the eventual R2 public-delivery/proxy layer so that moving them does not create brittle runtime dependencies.

## Runtime/reference audit result

The active ONE cover architecture is centrally governed by the canonical 241 Doré registry, Round 3 chapter mapping, ONE Studio registry and `ONE_COVER_POLICY`. Historical/local illustration writers are retired and must not be reintroduced.

Exact repository-code searches for the seven Priority A filenames returned no current direct textual runtime references. Therefore the GitHub copies are not treated as independent canonical masters, but they remain during the rollback window until R2-backed delivery is a first-class runtime path.

This prevents a false cleanup where a successful R2 write is followed by deletion before the website can actually serve the R2 object.

## Structured data — separate milestone
Large JSON search/corpus artifacts such as:
- `static/dore/search-index.json`
- `static/dore/original-index.json`
- `static/dore/entity-index.json`

remain outside this media migration. Their placement must be decided by access pattern, build atomicity and Search runtime requirements, not by file size alone.

## Storage namespaces
- `one/studio/...`
- `one/restorations/...`
- `one/motion/...`
- `one/share/...`
- `journal/...`
- `devotional/...`
- `library/media/...`
- `_system/...`

## Safety invariants
- One canonical binary backend per governed asset.
- Asset Registry owns storage backend, locator, content hash, provenance, rights, preservation class and product relationships.
- Permanent/canonical assets are never auto-deleted.
- Reproducible derivatives are preferred cleanup targets.
- GitHub rollback copies are temporary compatibility copies, not independent masters.
- Final GitHub binary removal requires a verified R2-backed runtime delivery path.
- GitHub and R2 must never silently diverge as competing masters.

## Next milestone
Build the R2-backed asset delivery/runtime layer, switch governed ONE media references to registry-driven delivery, verify website rendering, then remove the seven redundant GitHub rollback binaries where safe. After that, evaluate Priority B site/UI media and the broader Journal / Liming Library media inventory under the same governance rules.
