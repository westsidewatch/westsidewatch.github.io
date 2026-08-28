# DORÉ SCRIPTURE SEARCH INPUT EVIDENCE LEDGER — 2026-08-27

Status: ACTIVE_EVIDENCE_LEDGER
Sweep: `MEMORY-CONSOLIDATION-SWEEP-01`
Source family: foundation / Search input literacy

## Bounded evidence reviewed

- `dore-core/knowledge/foundation/search-input/SCRIPTURE-SEARCH-INPUT-LITERACY-1.0.md`
- `dore_core/search/service.py`
- `static/dore/dore-search.js`
- `dore-core/tests/search-browser-negative-relevance.mjs`
- canonical `DORÉ-MISSING-EVIDENCE-REGISTER.md` entry `ME-010`
- canonical `DORÉ-MASTER-WORK-REGISTER.md` Search interpretation

## Governing contract

`Scripture Search Input Literacy 1.0` is a foundation micro-unit, not a generic Search-complete claim. Its graduation contract requires unseen transfer across real-world reference forms, including:

- full Chinese names and common abbreviations for all 66 books;
- Arabic and Chinese chapter numbers;
- explicit chapter/verse wording;
- verse ranges and punctuation/range variants;
- two- and three-reference inputs;
- mixed single/range references;
- deduplication of overlapping multi-reference results;
- transfer without book-specific patches.

Classification of the curriculum artifact: `CORE/CONTINUOUS` foundation doctrine.
Classification of graduation: `UNKNOWN_NEEDS_EVIDENCE`.

## Implementation reconciliation

### Core Python service

`dore_core/search/service.py` contains real reference-normalization infrastructure:

- traditional/simplified Chinese folding;
- Chinese numeral parsing through hundreds;
- explicit reference mode;
- a `BOOK_ALIASES` table;
- chapter/verse normalization for some Chinese and Arabic forms.

However, the current implementation does **not** satisfy the micro-unit graduation contract:

1. `BOOK_ALIASES` contains only a small subset of books/aliases rather than all 66 books and their common Chinese abbreviations.
2. `_normalize_ref` handles single chapter/verse forms but has no range grammar equivalent to the micro-unit's `羅3:12-16`, `帖後3：15-19`, `帖後3章8節到10節` requirement.
3. It has no multi-reference parser/splitter for two- or three-reference queries.
4. It therefore has no implementation-level overlapping multi-reference deduplication path.
5. Forms such as bare Chinese chapter notation (`帖後三`) and `賽三第四節` are not demonstrated by this service's current regex/alias coverage.

This is implementation evidence of partial literacy, not graduation evidence.

### Browser Search implementation

`static/dore/dore-search.js` is stronger in several bounded ways:

- aliases are populated from live verse metadata plus an additional full-name/selected-abbreviation table;
- reference parsing supports Arabic verse ranges;
- Chinese numeral chapter/verse forms with `章` / `節` are supported;
- common dash/tilde/`至`/`到` variants are normalized.

But the browser path also does **not** prove the full micro-unit contract:

1. `parseReference` is a single-reference parser; the reviewed implementation does not expose a two-/three-reference query grammar satisfying the micro-unit examples.
2. No bounded evidence in the reviewed test family proves overlapping multi-reference deduplication.
3. Selected explicit Chinese short aliases exist, but the sweep did not find a persisted all-66-common-abbreviation acceptance fixture.
4. The negative-relevance regression is useful Search-quality evidence, but it is not a substitute for the foundation micro-unit's exact unseen-transfer graduation test.

## Architecture relation to Checkpoint 19

This bounded family reinforces the Search service-boundary drift already recorded by Sweep Checkpoint 19:

- Core Python and browser Search both implement reference intelligence;
- their grammars and alias coverage differ;
- neither path has persisted parity evidence against the micro-unit contract.

This does not justify retiring either live path. It strengthens the future requirement that Search convergence include a **shared reference-input acceptance corpus** so both implementations cannot silently diverge.

## Current judgment

- `SEARCH`: retain `MAINTENANCE + DISCOVERY`.
- Scripture Search Input Literacy curriculum: retain as valid foundation doctrine.
- Micro-unit graduation: retain `UNKNOWN_NEEDS_EVIDENCE` (`ME-010`).
- No `VERIFIED_COMPLETE`, `COMPLETED_REVISIT_CANDIDATE`, `SUPERSEDED`, or `RETIRED` promotion is justified.
- No new standalone canonical workstream is required; this evidence belongs beneath `SEARCH` and foundation learning.

## Smallest useful future proof

Create one shared, product-neutral acceptance fixture containing unseen cases across all 66-book alias families and the exact format classes in the micro-unit, including at minimum:

- Chinese and Arabic chapter forms;
- single verse and verse ranges;
- punctuation/range variants;
- two-reference and three-reference queries;
- mixed single/range queries;
- overlapping references with deterministic dedupe;
- negative malformed/ambiguous cases that must abstain.

Run the same fixture against the canonical Core parser and the live browser/parser boundary, persist parity/pass-fail output, and only then award a bounded `SCRIPTURE_SEARCH_INPUT_LITERACY_1_0_COMPLETE` milestone if every graduation requirement passes without book-specific patches.

## P01 protection

This reconciliation changed no P01 code, runtime state, deployment, binding, credential, subtitle ordering, or blocker state. The existing P01 environment dependency remains unchanged.

## Sweep source-family accounting

The `dore-core/knowledge/foundation/search-input/` family is now explicitly accounted for by Sweep 01. Its current evidence boundary is partial implementation + ungraduated foundation contract, with `ME-010` remaining the canonical missing-evidence guardrail.

## Checkpoint 24 revalidation — 2026-08-28

Fresh bounded revalidation covered the complete `dore-core/knowledge/foundation/search-input/` family (currently the single `SCRIPTURE-SEARCH-INPUT-LITERACY-1.0.md` micro-unit), its existing `ME-010` guardrail, and the canonical Search interpretation.

The micro-unit still self-identifies as `FOUNDATION MICRO-UNIT / NOT GRADUATED` and explicitly requires unseen transfer across different books/format variants, two- and three-reference inputs, mixed single/range references, overlapping-result deduplication, and no book-specific patches. No independent graduation/pass artifact was found in this bounded recheck.

Current disposition remains evidence-correct:

- curriculum/doctrine: `CORE/CONTINUOUS` foundation learning;
- graduation claim: `UNKNOWN_NEEDS_EVIDENCE` under `ME-010`;
- live `SEARCH`: remain `MAINTENANCE + DISCOVERY`;
- completed-work/revisit/superseded/retired additions: none;
- canonical Master Register: no row/status change warranted because its current Search classification already preserves the correct boundary.

This checkpoint also confirms that the earlier service-boundary drift finding remains material: Core and browser parsing capability cannot be treated as one graduated faculty until one shared acceptance corpus proves parity against the micro-unit contract.

P01 protection rechecked: no subtitle-path code, runtime state, deployment, binding, credential, ordering, or blocker state was modified by Sweep 01.