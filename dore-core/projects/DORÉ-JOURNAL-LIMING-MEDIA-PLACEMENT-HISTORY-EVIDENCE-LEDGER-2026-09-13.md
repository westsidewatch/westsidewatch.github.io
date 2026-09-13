# DORÉ JOURNAL + LIMING MEDIA PLACEMENT HISTORY — EVIDENCE LEDGER — 2026-09-13

Status: COMPLETE / BOUNDED HISTORICAL RECONCILIATION
Sweep: `MEM-SWEEP-01`
P01 impact: NONE

## Evidence reviewed

- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md`
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-INVENTORY-2026-08-24.json`
- current canonical Master Register interpretations for `JOURNAL-PRINT`, `LIBRARY-INGEST`, `LIBRARY-V1`, and `DAWN-LIBRARY`
- Checkpoint 92 Cloudflare/R2 migration reconciliation

## Historical finding

The 2026-08-24 Journal + Liming media audit is a legitimate bounded `VERIFIED_COMPLETE` milestone for its original question: at that repository snapshot there were zero eligible local Journal/Liming content-media binaries to migrate, so zero R2 writes, zero D1 media rows and zero GitHub binary deletions was the correct governed result. Structured editorial/catalog data (`data/volumes/vol-00.yaml`, `data/resources.json`, `content/journal/_index.md`) correctly remained in GitHub rather than being moved merely because R2 existed.

This is an important positive result: **zero migration can be a completed migration decision when placement policy and inventory prove that moving data would make architecture worse.**

## Current-state reconciliation

The historical inventory must not be read as present product truth.

The current Master Register records a materially later Dawn/黎明書局 state with a real storefront/autonomous catalog substrate, 34 published / 33 verified / 1 pending books, 220 mapped storefront books, 129 source covers and 21 direct publications. Therefore the 2026-08-24 statements that Liming/Dawn had no local cover/image binary collection and that future owned/downloaded cover/media handling was only prospective are now **historical snapshot claims, not current-state claims**.

The old placement principle remains useful, but the inventory conclusion is superseded by later product growth:

- versioned structured editorial/catalog source belongs in GitHub when atomic review with code/content matters;
- independently addressable binary media should use governed asset storage/registry rather than becoming a second untracked Git master;
- the existence of a future R2 namespace in an old memo does not itself prove that today's Dawn cover/publication pipeline uses that exact namespace or registry shape;
- current storage/runtime truth must come from current Dawn/R2/D1 evidence, not from the 2026-08-24 zero-migration inventory.

## Classification

- 2026-08-24 Journal + Liming media inventory/audit milestone: `VERIFIED_COMPLETE` (historical bounded milestone).
- Its zero-binary inventory result: `SUPERSEDED AS CURRENT STATE` by later Dawn Library growth.
- Its generalized placement doctrine: `RETAIN / CORE ARCHITECTURAL LESSON`.
- Any claim that present Dawn media already conforms to the exact future `library/media/...` + `liming_resource_ids_json` design: `UNKNOWN_NEEDS_EVIDENCE` unless supported by current implementation/runtime evidence.

## Revisit judgment

No immediate migration project should be reopened from this old milestone. A revisit is justified only if current Dawn/Journal media evidence shows one of these conditions:

1. duplicate canonical masters across GitHub/R2/D1;
2. missing rights/provenance/content-hash registry data;
3. production media delivered from an obsolete or public path contrary to current policy;
4. cover/publication assets that cannot be traced from product identity to canonical storage;
5. current asset growth making old placement assumptions operationally false.

## Durable lesson

**Placement decisions are access-pattern and canonical-identity decisions, not storage-fashion decisions.** Do not migrate structured source merely because object storage exists; do not leave independently addressable binary media in Git merely because it began there; and never carry a zero-inventory historical snapshot forward as product truth after the product has materially grown.

## P01 isolation

No P01 file, state, source order, deployment, credential, binding, subtitle job, or runtime action was changed by this reconciliation.
