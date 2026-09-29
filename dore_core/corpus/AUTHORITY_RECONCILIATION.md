# Doré Corpus Authority Reconciliation

Status: implementation contract.

## Goal

Move Dawn Library admission from manual book-by-book approval to corpus-scale compilation. Source scale may be tens or hundreds of thousands of records; human review must be limited to identity/rights/boundary exceptions.

## Pipeline

1. Source adapters ingest EEBO-TCP, PRDL, Open Christian Data, CatholicCorpus, CCEL/PTA and Open Library bulk records.
2. Deterministic routing removes Bible text and sends commentary/exegesis to ONE/Bible-world.
3. Rights/readability gates shrink the candidate pool.
4. Exact identifiers and normalized Work keys collapse obvious duplicate records.
5. Multi-field entity resolution scores title/alternate title, creator, date, publisher and identifiers.
6. Authority reconciliation uses PRDL + Open Library Work/Edition/Author identities where available.
7. High-confidence matches merge automatically beneath one canonical Work.
8. Probable/ambiguous matches enter an exception queue.
9. Only verified Works are promoted; editions/witnesses retain their own rights, scans, title pages and provenance.

## Open-source patterns absorbed

- Open Library: Work / Edition / Author separation and bulk-dump ingestion pattern.
- dedupe: learned structured-record entity-resolution pattern; optional implementation adapter, not a product dependency.
- OpenRefine reconciliation: candidate scoring, external authority reconciliation, confidence thresholds and human review for the middle band.

Doré owns the stable interface. No site surface depends directly on any of these projects.

## Confidence policy

- exact external/shared identifier or exceptionally strong multi-field match: auto-collapse candidate records;
- probable match: reconcile against PRDL/Open Library authority before merge;
- ambiguous match: exception queue;
- weak match: keep separate rather than risk false merge.

False merge is more damaging than temporary duplication.

## Scale rule

The unit of work is a batch/corpus, not a book. Reports should expose source-record count, route counts, candidate Work count, automatic merges, new Work candidates, exception count, rights holds and ONE/Bible-world routes.

## Cover / visual rule

Covers, title pages and scans belong to concrete Edition/Witness identities. A canonical Work may select a representative visual for discovery UI, but Doré never invents a historical cover for an abstract Work.

## Translation handoff

After canonical admission, eligible readable witnesses can pass to Doré Language Faculty for source / zh-Hant / bilingual reading. Translation is a reading projection and never creates a new Edition.
