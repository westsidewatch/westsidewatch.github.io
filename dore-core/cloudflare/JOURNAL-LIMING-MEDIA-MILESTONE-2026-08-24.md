# Journal + Liming Library Media Milestone — 2026-08-24

Status: **COMPLETE / PASS**

## Result

The repository-wide placement audit for current Journal and Liming Library material is complete.

### Journal
- `content/journal/` currently contains only `_index.md`; there is no local Journal binary-media collection to migrate.
- The current issue/volume editorial architecture is structured in `data/volumes/vol-00.yaml`.
- That YAML remains in GitHub because it is versioned editorial/build data and should change atomically with site code/content.
- Future Journal photographs, illustrations, issue covers and other independently addressable binaries will use private R2 under `journal/...` and be registered in D1.

### Liming Library / Dawn Library
- `data/resources.json` is the current Resource Master and contains the library system, recovered coding inventory, resource cards and external URLs.
- The current master does not contain a local cover/image binary collection requiring migration.
- `data/resources.json` remains in GitHub because it is structured, reviewable, versioned source data rather than large media storage.
- Future owned/downloaded library covers, scans, diagrams or media derivatives will use private R2 under `library/media/...`; D1 Asset Registry will link them through `liming_resource_ids_json`.

## Migration outcome
- Eligible current local Journal/Liming media binaries: **0**.
- R2 writes required: **0**.
- New D1 media rows required: **0**.
- GitHub binaries removed: **0**.

This is an intentional zero-migration PASS, not a skipped milestone. Moving JSON/YAML merely because R2 exists would violate the GitHub/R2 placement policy.

## Invariants preserved
- Brand/code/UI coupled assets stay in GitHub.
- Doré Original canonical library 001–241 untouched.
- Search/corpus JSON untouched and remains deferred to the data-runtime milestone.
- No GitHub/R2 competing masters were created.

Evidence: `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-INVENTORY-2026-08-24.json`.

## Next milestone
The next storage milestone is the **structured data-runtime audit**: evaluate Doré search/corpus indexes by access pattern, build atomicity, update frequency and size; decide what remains GitHub/Pages and what, if anything, should move behind Cloudflare/D1/R2 without degrading Bible Search or Doré Brain.
