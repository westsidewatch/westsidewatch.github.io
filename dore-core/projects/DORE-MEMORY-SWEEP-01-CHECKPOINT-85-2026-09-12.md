# DORÉ MEMORY SWEEP 01 — CHECKPOINT 85 — 2026-09-12

Status: COMPLETE / BOUNDED BATCH
Sweep: `MEM-SWEEP-01`
P01 constraint: subtitle critical-path state was not modified.

## Evidence reviewed

Multiwrite / 成書 Book Intelligence and governed BookModel integration milestone:

- merge commit `98f44c4363efb65d88ce43fd8dbd5a208ff29d4d` (PR #673 final integration of PR #662);
- merged `dore-core/runtime/book-publishing-capability.v1.json`;
- merged Capability Registry entries `publishing.book-intelligence` and `publishing.book-compile`;
- merged `local/dore-local/book_intelligence_capability.py`;
- Firefox Companion/site capability bridge additions for `publishing.book-intelligence`;
- self-hosted Mac resident-model E2E workflow introduced for this integration.

## Findings

1. Book Intelligence / BookModel is no longer merely proposed architecture. The final merge records clean integration after real Mac resident model-backed E2E acceptance and merges the provider-neutral Core adapter, capability registration, native/site bridge, governed publishing contract and dedicated resident E2E workflow.
2. The strongest bounded completion claim is: **model-backed Book Intelligence crossed the real local A2A execution plane and fed the governed Multiwrite publishing spine while preserving author-thesis authority and provider neutrality.** This is a legitimate `VERIFIED_COMPLETE / COMPONENT` milestone inside the larger 成書 workstream.
3. The larger 成書 product is not `VERIFIED_COMPLETE`. The contract names `web`, `epub` and `pdf` targets and a pipeline through editorial/theology/design/publication QA, but this merge alone does not prove production-grade final artifacts across all three targets, automated cover/art direction, complete rights behavior, or repeated real-book publication/readback.
4. Durable authority learning is explicit: mechanical repair may be silent; generated completion remains proposed; substantive authorial change, rights-uncertain publication and irreversible public action remain human-authority boundaries; public `publicationMetadata` is allowlisted separately from private `internalProvenance`.
5. The merge closes an older evidence gap around whether the local resident-model path was only simulated for this capability. It must not be generalized to every Doré capability without separate evidence.
6. No superseded/retired implementation is justified. Retain the provider-neutral Core boundary and A2A bridge; do not regress to browser/provider-specific direct inference.
7. No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition was discovered.
8. No P01 subtitle runtime, blocker, ordering, binding or resume condition was modified.

## Current classification

- Book Intelligence local Core/A2A milestone: `VERIFIED_COMPLETE / COMPONENT`.
- Governed BookModel / EditorialReport / BookBuild spine: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` as part of 成書.
- Full autonomous digital-publication outcome: `ACTIVE_PARALLEL / UNKNOWN_NEEDS_EVIDENCE` until real end artifacts and publication QA are persisted.

## Revisit / retention judgment

Retain the merged architecture. Revisit only if provider neutrality breaks, author authority is violated, artifact projections leak internal provenance, or later publication evidence exposes a structural limitation.

The next proof should be product-level rather than another architecture-only test: take one real manuscript through the governed pipeline and persist resulting web + EPUB + PDF artifacts, editorial/theology/design/rights decisions, publication QA, and readback/identity evidence.

## Durable linkage

The next safe canonical-register bookkeeping pass should advance the Sweep frontier through Checkpoint 85 and record this bounded 成書 component milestone without promoting the whole publishing workstream. A dedicated publishing evidence ledger can consolidate future end-artifact proof.

## Sweep disposition

Sweep 01 remains `ACTIVE_PARALLEL`. This bounded batch does not justify `VERIFIED_COMPLETE` and creates no user-notification condition.