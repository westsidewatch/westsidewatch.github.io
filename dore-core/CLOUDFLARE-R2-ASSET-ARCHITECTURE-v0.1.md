# Cloudflare R2 / Doré Asset Architecture v0.1

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
  - R2 remains the binary source of truth
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

## R2 + Images relationship

Operating model:

`Doré creates/selects master → rights/provenance check → R2 master storage → Asset Registry → custom-domain/CDN delivery → optional Images transformation → product/social use → usage feedback`

Do not use Cloudflare Images hosted storage as the architectural source of truth. The intended design is **R2 stores originals; Images Free may transform selected images**.

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
- `object_key`
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
- supersedes / superseded_by

Doré should know not only where an asset is, but what it depicts, why it exists, its rights state, where it has been used and whether it can safely be reused.

## GitHub vs R2 boundary

A useful shorthand retained from the original discussion:

> **GitHub = 圖書目錄；R2 = 書庫。**

More precisely:

- GitHub retains code, rules, schemas, durable metadata/snapshots and institutional history.
- R2 retains growing binary media that should not generate meaningless binary Git commits or require a site deployment whenever Doré creates a new image.

Keep small code-coupled static assets such as logos, icons, fixed UI decoration and selected version-bound backgrounds in GitHub when appropriate. Put growing editorial/knowledge/production media in R2.

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
6. clean separation between institutional truth, operational storage and knowledge organization.
