# DORÉ LIVING RETRIEVAL — EVIDENCE LEDGER

Date: 2026-09-11
Status: BOUNDED_COMPONENT_VERIFIED
Parent workstream: `SEARCH`
Sweep checkpoint: `DORE-MEMORY-SWEEP-01-CHECKPOINT-77-2026-09-11.md`
P01 impact: NONE

## Original objective

Make fuzzy/context retrieval begin before explicit search while keeping the passive path light, deterministic and non-authoritative; normalize provider-specific document/memory payloads into one Doré Search result contract before products consume them.

## Current implementation evidence

- `dore_core/retrieval/living.py` implements the retrieval planner and orchestrator.
- Passive association/CJK/natural-language retrieval is lexical/BM25-first and does not wake memory or a large model by default.
- Explicit search may add semantic retrieval and strict memory recall; deep retrieval is separately explicit.
- Prepare/Live/Present behavior is constrained by `SearchContextPolicy`; Present performs no retrieval and Live suppresses ambient retrieval.
- Embedded product context can filter results through `apply_bible_context_result_policy`.
- `dore_core/retrieval/results.py` normalizes heterogeneous document/memory payloads, ranks/deduplicates results and preserves source/lane provenance with `authority: false`.
- Commit `b86c7c2c1c6de5a106eb4e6368cfdb394b1b2b5d` introduced the provider-neutral result layer, routed `context.fuzzy-search` through Living Retrieval and added discoverable result-layer acceptance tests.
- Commit `ea9c8c07ac5477eb9c074ca64478b1570b9c17ff` changed passive fuzzy retrieval to reduced lexical/BM25-first routing and added acceptance coverage for the light passive path.
- GitHub Actions run `34190793706`, display title `[DORÉ A2A] context.fuzzy-search passive BM25 acceptance`, completed with `conclusion: success` against head SHA `ea9c8c07ac5477eb9c074ca64478b1570b9c17ff` on 2026-09-08.

## Completion judgment

### Bounded milestone

`Living Retrieval lexical-first + provider-neutral result contract` = **VERIFIED_COMPLETE / COMPONENT**.

This is a component milestone only. It does **not** imply that Doré Search cognition, semantic relevance, production precision/recall, cross-product UX, or the broader fuzzy-search research program is complete.

## Current quality

Strong architectural qualities:

- passive retrieval is intentionally cheap and deterministic;
- retrieved material never gains authority merely by being retrieved;
- provider names are hidden behind a stable product-facing result contract;
- provenance survives normalization/deduplication;
- memory is not awakened for passive pre-search;
- search behavior is context-policy aware rather than globally always-on.

Current limitations/debt:

- association/CJK routing relies on hand-maintained lexical cue lists and phrase heuristics;
- the verified acceptance is bounded to the component contract, not broad real-corpus relevance;
- no evidence here proves semantic lane quality, multilingual ranking quality, latency/cost under representative production scale, or longitudinal user usefulness;
- this component must remain subordinate to the Search cognition/evaluation gates already tracked in the Master Register and `ME-006`.

## Durable learning

`ambient retrieval should spend the smallest capability that can surface useful evidence; explicit intent may widen the lane.`

`retrieval evidence != authority.`

`product surfaces should consume one stable Doré result contract, not substrate-specific payloads.`

## Revisit trigger

Reopen this component when any of the following becomes true:

- repeated false-positive/false-negative evidence shows the lexical cue heuristics are inadequate;
- a materially better lightweight multilingual tokenizer/ranker can reduce complexity or improve recall without waking a larger model;
- production telemetry shows passive retrieval latency/noise harms writing/study flow;
- Search service-boundary convergence removes duplicated retrieval logic elsewhere and requires this contract to change.

## Current disposition

Keep as-is and maintain as a regression gate. Improve only from measured relevance/latency failures or deliberate Search service-boundary convergence. Do not reopen it merely because broader Search remains unfinished.
