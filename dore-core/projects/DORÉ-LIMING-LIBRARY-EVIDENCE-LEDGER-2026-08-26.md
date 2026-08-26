# DORÉ LIMING LIBRARY EVIDENCE LEDGER — 2026-08-26

Status: ACTIVE EVIDENCE / SWEEP-01
Related work: `LIBRARY-INGEST`, `3MS`, `LIBRARY-V1`, `MEM-SWEEP-01`

## Purpose

Record the bounded evidence reconciliation for Liming Library ingestion/runtime and its adjacent media-placement history without inflating implementation into production verification.

## Evidence reviewed

- `data/resources.json` — current Resource Master / Dawn Library structured source.
- `functions/api/dore/library/resources.js` — D1-backed resource registry/read-write API.
- `data/liming-dore-ingest-seed.json` — two three-star David Pawson seed resources with rights/provenance/product/scripture metadata.
- `.github/workflows/dore-liming-ingest.yml` — authenticated production-ingest/readback workflow.
- commits `24737d39435348ea7c7f33c7d18cf5f12c52e9d1`, `beec925a69f4b056bda7ceb51553ce1a374bb017`, `a776b7a3bd4e2c23f53a6efebbc9fd2a792cba2e`, `f2192c5f4ad38cd6cce27c68fce809f6633b9335`, `3d069c43ca07288d14acda4d486364fb7e37ae29`.
- GitHub Actions run history for the workflow-introduction commit and all recorded `workflow_dispatch` runs visible in the repository.
- `dore-core/cloudflare/JOURNAL-LIMING-MEDIA-MILESTONE-2026-08-24.md` and `JOURNAL-LIMING-MEDIA-INVENTORY-2026-08-24.json`.
- commit `2dcfef6499a8b46c66aee1150796662776f1f594`.

## 1. Resource Master remains a real structured source

`data/resources.json` explicitly identifies itself as `Resource Master`, defines the Library vision, layered architecture, editorial rhythm, workflow, categories, source domains and activation surfaces. The file is structured/versioned source material rather than a binary-media store.

Current classification: `CORE/CONTINUOUS` source-of-truth role inside the Library system. This does not mean the current public presentation is complete.

## 2. Live-ingest implementation is materially beyond a paper contract

`functions/api/dore/library/resources.js` implements:

- D1 tables `liming_resources` and `liming_resource_edges`;
- stable `resource_id` generation from source URL;
- unique `source_url` identity and upsert semantics;
- source-class and rights-status validation;
- candidate/reviewed/published/retired lifecycle states;
- Morning Star score and Chinese-access metadata;
- Scripture, Teacher, Series and Product relationship edges;
- provenance and discovery metadata;
- authenticated POST/PATCH writes using `DORE_HEARTBEAT_TOKEN`;
- public query filters for text, creator, series, Scripture book/chapter, stars and status.

`data/liming-dore-ingest-seed.json` supplies two concrete published three-star resources linked to David Pawson, official/authorized sources, `link-only` rights, Scripture-book coverage, products and provenance policy.

`.github/workflows/dore-liming-ingest.yml` is executable automation, not merely prose: it waits for the deployed endpoint, POSTs every seed through the authenticated production API and then asserts that at least two published three-star David Pawson resources are readable from the public API.

Therefore the previous shorthand `contract/registry/binding foundation exists` understated implementation maturity. The Master Work Register has been reconciled accordingly.

## 3. Production verification is still missing

No successful `Doré Liming Library Ingest` Actions run was found in the reviewed run history.

Chronology matters:

- the API registry commit `24737d...` and seed commit `a776b7...` predate the workflow-creation commit `f2192c...`;
- the workflow's push trigger watches changes to the API or seed, so those already-completed earlier commits could not trigger a workflow that did not yet exist;
- querying Actions by the workflow-introduction commit `f2192c...` returns only the Hugo deployment run, not a Liming ingest run;
- the repository's recorded `workflow_dispatch` runs reviewed in this batch contain no Liming Library ingest run.

This means the code contains a strong intended production verification, but the Sweep does not infer that it has actually executed successfully.

Current classification for `LIBRARY-INGEST`: `ACTIVE_PARALLEL`.

Missing-evidence boundary: one real authenticated ingest/readback run demonstrating stable identity/dedupe, rights/provenance retention, relationship edges and published-query visibility without duplicate creation.

This is `UNKNOWN_NEEDS_EVIDENCE` for runtime verification, not an environment or human-decision blocker.

## 4. Journal + Liming media-placement milestone is historically complete

`JOURNAL-LIMING-MEDIA-INVENTORY-2026-08-24.json` records `status: PASS` and a governed zero-migration result:

- current Journal local content-media binaries: 0;
- current Liming local media binaries requiring migration: 0;
- R2 writes required: 0;
- new D1 media rows required: 0;
- GitHub binary deletions required: 0;
- `data/resources.json` remains in GitHub because it is structured/versioned source data;
- future independently addressable Library media belongs under private R2 `library/media/` with D1 relationships;
- Doré Original canonical 001–241 and Search/corpus JSON were explicitly left untouched.

The companion milestone file records `COMPLETE / PASS`, and commit `2dcfef...` persisted the closeout.

Current classification: `VERIFIED_COMPLETE` for the bounded Journal/Liming media-placement inventory milestone. It is not evidence that Library V1, Library ingestion runtime, Journal media production, or all future Library media migration are complete.

### Retained capability

- classify structured versioned source separately from binary media;
- allow a correct zero-migration outcome rather than moving data merely because R2 exists;
- preserve one canonical master instead of creating GitHub/R2 competitors;
- predeclare future R2 namespace and D1 relationship requirements without prematurely migrating absent media.

### Revisit trigger

Reopen this placement judgment when Liming or Journal gains owned/downloaded covers, scans, diagrams, photographs, illustrations or other independently addressable binaries, or when access/update patterns make the current GitHub structured-source placement materially inappropriate.

## 5. Superseded / retired judgment

No evidence in this bounded batch justifies retiring Resource Master, the D1 resource registry or the ingest workflow. The D1 registry is an operational enrichment/runtime layer around structured Library source and discovered resources, not evidence that `data/resources.json` should be discarded.

No new `SUPERSEDED` or `RETIRED` work item is declared from this batch.

## 6. Current next milestone

Run the existing Liming ingest workflow (or equivalent production-safe verification) and persist evidence for:

`authenticated write → stable source identity/upsert → rights/provenance retained → Teacher/Series/Scripture/Product edges → public published readback → repeat ingest without duplicate identity`

Only after that evidence exists should the bounded live-ingest runtime be considered for `VERIFIED_COMPLETE`.

## P01 protection

No P01 code, runtime state, deployment path, configuration, ordering or blocker state was changed by this evidence review.