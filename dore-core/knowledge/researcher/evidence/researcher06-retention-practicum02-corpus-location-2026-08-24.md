# Researcher 06 Retention Practicum 02 — Corpus Location Evidence

Date: 2026-08-24
Status: PASS — authoritative corpus located; harness execution dependency identified

## Sensory priority check
`dore-core/memory/sensory-active.json` contains no `RESEARCHING` signal without a `brain_node`. The existing Mary signal remains `CONSOLIDATED -> research.nt.mary-count`, so no live sensory task preempted this practicum.

## Authoritative browser Scripture corpus located
The current Doré Bible Search build contract generates `static/dore/search-index.json` with schema `dore.browser-search-core.v1` and asserts at least 31,000 verses plus canonical references including John 3:16 and Jeremiah 33:3.

The generator is `scripts/build_dore_browser_search_index.py`. It constructs each verse as:

- canonical ref `r` (`bible.ref.BOOK.CHAPTER.VERSE`),
- book `b`, chapter `c`, verse `v`,
- Chinese text `z`,
- English text `e`,
- book names `n`.

Pinned witnesses/snapshots in the generator:

- Chinese: CUV Traditional 1919 from `midvash/bible-data`, snapshot `d9fe1779447717bbfcb578e505b893125cad581c`, public domain.
- English: World English Bible Updated from `ringletech/webu-open-bible`, snapshot `44ce9156b77649adf11c0bbcee89c1d80e2c1f1c`, CC0-1.0.
- Hebrew morphology: OSHB/WLC snapshot `3d15126fb1ef74867fc1434be1942e837932691f`.
- Greek morphology: MorphGNT/SBLGNT snapshot `aaed91e57c8e4a8dc9a2383e129ca5e75fe6393d`.

This is sufficient provenance to define the contiguous-window candidate source without inventing a new Bible corpus.

## Current retrieval limitation confirmed
`static/dore/dore-search.js` builds `state.byChapter` from `state.data.verses`, but free-text `textSearch()` scores every verse independently. The range parser can return an explicitly requested verse range, but free-text candidate generation does not construct adjacent 2- or 3-verse windows. Therefore the cross-verse limitation is an implementation/retrieval gap, not evidence of missing biblical knowledge.

## Authorized harness design now fixed
A non-production Probe A harness should:

1. read `static/dore/search-index.json`;
2. group verses by `(book, chapter)` and numeric verse order;
3. generate contiguous windows of length 1, 2, and 3 only within the same chapter;
4. retain component canonical refs for provenance;
5. score each window with the same normalized lexical/fuzzy evidence family used by current verse search;
6. compare top-K recall against verse-only retrieval under one frozen candidate budget;
7. use fixtures whose expected references are used only for evaluation, never candidate generation;
8. preserve the first failures rather than tuning on the held-out partition.

## Dependency boundary
The GitHub connector exposes repository files but does not provide a repository checkout or code-execution action. `static/dore/search-index.json` is a multi-megabyte generated one-line JSON artifact and the file-content endpoint does not return its body through this connector. Consequently an honest full-corpus measurement cannot be executed inside this automation run without fabricating results.

This is an execution/tool dependency, not a Researcher 07 learning deficit and not a human-approval boundary.

## Result
PASS for the authorized `LOCATE_AUTHORITATIVE_SCRIPTURE_CORPUS` action.

The build/execution half remains pending. No product-readable brain knowledge changed, so no Brain -> Product regression is warranted.

## Next action
`BUILD_AND_EXECUTE_NON_PRODUCTION_CONTIGUOUS_WINDOW_RETRIEVAL_HARNESS_WHEN_REPOSITORY_EXECUTION_OR_FULL_CORPUS_BYTES_ARE_AVAILABLE`.

Do not open Researcher 07 from this dependency. Do not modify production Search merely to make the practicum pass.