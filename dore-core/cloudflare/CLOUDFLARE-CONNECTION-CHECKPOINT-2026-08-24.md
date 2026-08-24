# Cloudflare Connection Checkpoint — 2026-08-24

Status: PASS — first D1 + R2 asset round trip verified in production

## Verified production bindings

- `DORE_SENSORY` → D1 database `dore-sensory`
- `DORE_ASSETS` → R2 bucket `westside-assets`

## Health verification

`/api/dore/assets/health` returned:

- `ok: true`
- `d1_bound: true`
- `r2_bound: true`
- `r2_readable: true`

## First disposable Asset Registry round trip

The production endpoint `/api/dore/assets/roundtrip` was executed once from the first-party Pages site and returned PASS indicators including:

- `ok: true`
- `schema: asset_registry`
- `write: true`
- `d1_registered: true`
- `read: true`
- `hash_verified: true`
- `registry_verified: true`
- `deleted_r2: true`
- `deleted_d1: true`
- `residue: false`
- `clean: true`

This proves the operational chain:

`GitHub code → Cloudflare Pages Function → R2 write → D1 registry write → R2 read → SHA-256 verification → registry verification → R2 cleanup → D1 cleanup → zero residue`

## Milestone

`CLOUDFLARE / ASSET ROUND TRIP — PASS`

The next implementation phase is **production Asset Registry**, not another infrastructure redesign.

## Next phase

1. adopt `dore-core/cloudflare/asset-registry-schema-v1.sql` as the production registry contract;
2. implement governed asset create/read/update/register/use APIs;
3. enforce GitHub-vs-R2 storage backend policy;
4. add hash dedupe and preservation classes;
5. connect Liming Library resource IDs and ONE/Journal/Search/Social usage relationships;
6. add storage usage guard and maintenance queue;
7. use the first real bounded asset workflow as the next acceptance test.

## Cost boundary

Infrastructure is intentionally designed to start inside free allowances. Free status is an operating target, not an assumption of unlimited free usage. Monitor R2/D1/Workers usage and keep model/inference costs separate from infrastructure costs.
