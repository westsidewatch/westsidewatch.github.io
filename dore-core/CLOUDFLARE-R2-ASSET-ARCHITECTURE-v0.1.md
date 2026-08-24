# Cloudflare R2 / Doré Asset Architecture v0.2

Status: RECOVERED AND CONFIRMED OPERATING DIRECTION
Date: 2026-08-24

## Purpose

Preserve the Cloudflare/R2 architecture established during Doré's infrastructure expansion so it remains durable across conversations and future implementation work.

## Core architecture

- **GitHub = institution memory / source of truth**
  - code
  - architecture
  - policies and schemas
  - approved content / knowledge snapshots
  - asset metadata where versioned durability is useful
  - decision history

- **Cloudflare = Doré operational infrastructure**
  - not Doré itself
  - not Doré Knowledge
  - replaceable infrastructure beneath Doré

- **Cloudflare R2 Standard = brand-level binary Media / Visual Asset Library**
  - original/master images and other binary media
  - one shared brand asset layer rather than separate product image repositories

- **Cloudflare CDN + custom domain = production delivery/cache layer**
  - `r2.dev` is for development/testing, not the intended production endpoint

- **Cloudflare Images Free = optional image transformation/optimization layer**
  - R2 remains the binary source of truth for growing media
  - transformations are used selectively for responsive/optimized variants

- **D1 / structured runtime store = runtime registries and relationships where appropriate**
  - Asset Registry
  - Resource Registry
  - usage relationships
  - operational state

- **Workers / Pages Functions = bounded capability gateway**
  - upload/register/retrieve/verify assets
  - retrieve registry information
  - publish/prepare derivatives where authorized

- **Doré = Asset Creator + Librarian + intelligence/learning/editorial layer**

- **Consumers = Journal / ONE / 黎明書局 / Church / Bible Search / Social / future brand products**

## Free-tier premise recorded at design time

The architecture was selected with R2 Standard's free tier as the starting operating envelope:

- 10 GB-month storage
- 1 million Class A operations/month
- 10 million Class B operations/month
- Internet egress from R2 is free

These are billing/free-tier allowances, not a 10 GB technical bucket-capacity limit. The architecture must not assume unlimited free storage or unlimited free operations.

The design estimate used during planning: at roughly 2 MB per master image, 10 GB is about 5,000 images. Web-optimized masters can substantially increase the count.

Social distribution generally should upload/copy the media file to the social platform rather than hotlinking R2 for every impression. Once a file is hosted by Instagram/Threads/WeChat or another platform, audience impressions there normally do not translate one-for-one into R2 reads.

For first-party websites, production delivery should use a custom domain and Cloudflare cache/CDN in front of R2 so cache hits do not unnecessarily become origin-object reads.

## Storage-pressure policy

Treat the 10 GB free allowance as an external billing threshold, not an operating target. Internal operations should stay below it with safety margin.

Recommended policy:

- **70%**: advisory review — report growth rate, duplicates, large masters, stale derivatives and test assets.
- **80%**: active cleanup queue — remove safe redundancy, expire temporary assets and regenerate rather than store low-value derivatives.
- **90%**: protective mode — block non-essential large uploads unless explicitly approved; preserve permanent assets and unique originals.

Automatic cleanup may remove only assets that are provably safe to recreate or discard. It must not automatically delete the only copy of an original, licensed source, human-approved master, historically significant asset, or provenance evidence.

Storage classes:

1. **Permanent** — original brand work, approved masters, irreplaceable/public-domain source captures where preservation is justified, critical provenance evidence. Never auto-delete.
2. **Regenerable** — thumbnails, transcodes, responsive derivatives, cached variants. Prefer transformation/rebuild over permanent duplication.
3. **Temporary** — generation candidates, failed/test outputs, staging and intermediate files. Give TTL/cleanup eligibility.

Doré's Asset Librarian responsibilities include deduplication, compression/optimization, preservation class, reuse tracking, usage monitoring, cleanup candidate generation and safe reclamation.

## R2 + Images relationship

Operating model:

`Doré creates/selects master → rights/provenance check → R2 master storage → Asset Registry → custom-domain/CDN delivery → optional Images transformation → product/social use → usage feedback`

Do not use Cloudflare Images hosted storage as the architectural source of truth. The intended design is **R2 stores growing media originals; Images Free may transform selected images**.

## Brand-level asset organization

Prefer one brand-level asset library, with logical namespaces such as:

```text
assets/
  shared/
  dore/
  one/
  journal/
    daily-devotional/
    interlude/
  liming-library/
  church/
  search/
  social/
```

`shared/` is important: a Matthew 3 baptism image, for example, may be reused by ONE, Journal, Search, church teaching and Liming Library rather than copied into five product repositories.

## Asset Registry principle

R2 stores binary objects; it does not define their meaning or reuse rights. Important assets should have structured records including, as appropriate:

- `asset_id`
- `storage_backend` (`github` or `r2`)
- `storage_locator` (repo path or R2 object key)
- title / asset type
- creator / source / source URL
- provenance
- copyright status / license
- generated_by / created_at
- Scripture references
- topics / people / places
- products using the asset
- Journal columns / social uses
- alt text
- status
- preservation_class
- content_hash
- supersedes / superseded_by

Doré should know not only where an asset is, but what it depicts, why it exists, its rights state, where it has been used, whether it can safely be reused and which storage backend is authoritative for that asset.

## Precise GitHub vs R2 placement policy

The architecture is intentionally hybrid. **Some images belong in GitHub; most growing editorial/media assets belong in R2.** Placement must be decided by lifecycle and coupling, not file type alone.

### Store in GitHub when the asset is tightly coupled to code/version history

Typical GitHub assets:

- logo and identity marks;
- favicon/app icons;
- small UI icons and ornaments;
- fixed CSS/background textures;
- tiny framework/demo fixtures required by tests;
- a small number of canonical interface illustrations whose exact binary must change atomically with code;
- assets required for build/bootstrap/fallback before Cloudflare/R2 is available;
- audit fixtures or historical binaries whose Git SHA is itself part of the verification contract.

GitHub assets should be relatively small, infrequently changed and meaningful to version together with the repository.

### Store in R2 when the asset has an editorial/content lifecycle

Typical R2 assets:

- Doré-generated visual masters;
- Journal / Daily Devotional media;
- ONE chapter illustrations and growing chapter media;
- Liming Library visual resources where binary storage is permitted;
- church event/editorial photography;
- social production masters;
- maps/scans/visual references that are not code-coupled;
- audio and later other large media;
- high-resolution originals whose derivatives are consumed by multiple products.

These should not require a Git commit/site deployment whenever added or replaced.

### Decision rule

Ask in this order:

1. **Must this exact binary version atomically with code/UI?** → GitHub is usually correct.
2. **Will this asset grow as content/editorial output or be reused across products?** → R2 is usually correct.
3. **Is it a unique original/master with long-term media value?** → R2 master + durable metadata/snapshot in GitHub where appropriate.
4. **Is it only a derivative or cacheable variant?** → do not duplicate unnecessarily; transform/regenerate.
5. **Does runtime depend on it before R2 is reachable?** → keep a minimal GitHub fallback only if genuinely required.

### One authoritative binary

Do not keep independent production masters in both places merely "for safety." Every asset record should identify one authoritative binary backend.

Allowed exception: a deliberate, documented archival or bootstrap copy with a different role. In that case the Asset Registry must say which copy is production-authoritative and why the second copy exists.

### Cross-backend consistency

When GitHub and R2 must cooperate:

- use stable `asset_id` rather than raw path assumptions;
- store `content_hash` for verification;
- record backend and locator explicitly;
- product code should resolve through the Asset Registry/canonical policy when practical;
- migrations must preserve legacy locator mapping until consumers have moved;
- no silent duplication, no ambiguous authoritative copy.

A useful shorthand retained from the original discussion:

> **GitHub = 圖書目錄；R2 = 書庫。**

But this shorthand is not absolute: GitHub may also hold a small number of code-coupled binaries when version control is the correct lifecycle.

## Doré automation significance

R2 was chosen not only for storage economics but because it supports Doré's future autonomous workflows:

`Doré output → PUT object → register metadata → verify → stable asset reference → immediate product use`

This is preferable to:

`Doré output → modify repository → commit/push → deployment → obtain media URL`

for recurring generated/editorial assets.

A Daily Devotional workflow is a representative target:

`cadence → Scripture/theme → Doré research + Liming Library → editorial draft → evidence/boundary check → visual selection/generation → R2 → Asset Registry → Journal/social variants → publish/prepare → verify → record usage → learn`

## Relationship to Liming Library

R2 and Liming Library must not be conflated.

- **R2** stores binary assets.
- **Liming Library** is Doré's knowledge-resource institution and learning output system.
- **Doré Knowledge** stores governed understanding.
- **Doré Memory** stores durable experience/context.

A visual or source in R2 may be represented and related through Liming Library, but storage location is not knowledge classification.

## Long-term architectural boundary

Cloudflare is Doré's **operational substrate**, not Doré's identity or brain. If the infrastructure provider changes later, Doré, Liming Library, institutional knowledge, schemas and relationships must remain portable.

The architecture therefore optimizes for:

1. $0-compatible starting scale where current free allowances suffice;
2. no throwaway architecture when the brand grows beyond free allowances;
3. shared assets instead of product duplication;
4. provenance and rights awareness from day one;
5. Doré-controlled automation and reuse;
6. precise hybrid GitHub/R2 placement with one authoritative binary per asset;
7. proactive storage optimization and safe capacity guards;
8. clean separation between institutional truth, operational storage and knowledge organization.
