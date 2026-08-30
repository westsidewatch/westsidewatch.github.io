# DORÉ SEARCH STRUCTURED-DATA RUNTIME EVIDENCE LEDGER — 2026-08-30

Status: SWEEP-01 EVIDENCE / UNKNOWN_NEEDS_EVIDENCE
Related work: `SEARCH`, `STEWARDSHIP`, Cloudflare storage architecture

## Bounded evidence reviewed

- `dore-core/cloudflare/ASSET-MIGRATION-INVENTORY-2026-08-24.md`;
- current `static/dore/` directory inventory;
- current `static/dore/dore-search.js` browser Search implementation;
- current canonical `DORÉ-MASTER-WORK-REGISTER.md` Search/storage interpretation.

## Findings

1. The 2026-08-24 asset-migration milestone explicitly excluded Search/corpus JSON from media migration and required a separate structured-data/runtime decision based on access pattern, build atomicity and Search runtime requirements rather than file size alone. That separation remains valid.
2. The current repository still contains three large static browser indexes: `static/dore/search-index.json` (~10.24 MB), `static/dore/original-index.json` (~10.18 MB) and `static/dore/entity-index.json` (~2.86 MB). Their continued presence is therefore not accidental residue; it is the still-unresolved placement family named by the earlier milestone.
3. Current `static/dore/dore-search.js` directly fetches `/dore/search-index.json` during browser initialization and lazily fetches `/dore/original-index.json` when original-language behavior is needed. This is production-coupled evidence that any storage move must preserve browser latency, cacheability, atomic index/version updates and fail-soft behavior; deleting/moving the files merely to reduce GitHub size would break the live Search contract.
4. No repository evidence was found in this bounded pass for the named follow-on structured-data runtime audit, an R2/D1-backed replacement path, a manifest/version handshake, or comparative latency/cache/build evidence proving that another placement is superior.
5. This is not a blocker and does not justify changing `SEARCH` from `MAINTENANCE + DISCOVERY`. It is a bounded `UNKNOWN_NEEDS_EVIDENCE` architecture decision. The current GitHub/static placement should remain the compatibility baseline until a replacement is proven.

## Current disposition

- current static Search/original/entity index placement: `MAINTENANCE / COMPATIBILITY BASELINE`;
- structured-data runtime/storage audit: `UNKNOWN_NEEDS_EVIDENCE`;
- automatic R2 migration by size: rejected;
- revisit trigger: material browser payload/performance cost, repository/build friction, update-atomicity failures, index growth, or a proven server/runtime retrieval path that improves reader behavior without creating competing masters.

## Smallest useful future proof

Run one bounded structured-data placement experiment with the same real Search corpus comparing current static delivery against a candidate runtime path. Persist at minimum: first-load and warm-cache latency, bytes transferred, cache semantics, update/version atomicity, offline/failure behavior, build/deploy coupling, reader-visible Search correctness, and source-of-truth/rollback rules. Only migrate after the candidate is measurably better and production-compatible.

## Sweep judgment

This family is now explicitly accounted for by Sweep 01. No P01 subtitle/runtime state, deployment, binding, credential, ordering or blocker condition was modified.