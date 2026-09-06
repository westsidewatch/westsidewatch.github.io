# DORÉ Core Consolidation Pass 01 — Scripture Knowledge

Status: ACTIVE IMPLEMENTATION BASELINE

## Purpose

This pass strengthens DorÉ Core while the first shared Scripture workspace is being built. It prevents the upcoming Multiwrite Bible Notes work from creating new product-local brains.

## Canonical ownership

Doré Core owns reusable semantics for Scripture identity, personal study memory, retrieval, provenance, source linkage, capability routing and learning evidence.

ONE owns Scripture reading/exploration UX and continues to supply the canonical 66-book / 1189-chapter identity through its Canon Index.

Multiwrite owns capture, development, long-form writing and publication UX. It does not own a separate Bible-note memory or search engine.

Doré Search owns the natural-language entry surface. Retrieval intelligence belongs to Core.

黎明書局 / Dawn Library owns governed source/resource product behavior and is Doré's principal source-memory and Librarian training domain. It does not own Scripture identity or user notes.

## Shared artifacts

The minimum cross-product artifact vocabulary is:

- `ScriptureAnchor` — stable link to ONE Canon Index identity.
- `StudyNote` — protected user-authored study memory, revisioned independently of product UI.
- `LibrarySourceRef` — provenance-preserving reference to a Dawn Library source; source and interpretation remain distinct.
- `RetrievalHit` — rebuildable search projection, never canonical user content.
- `LibraryLoopEvidence` — evidence about whether a source/retrieval path actually helped a study or writing outcome.

Product UI state, route state, selection state and layout remain product-owned.

## One artifact, many surfaces

A StudyNote created while reading Matthew 6 in ONE must remain the same note ID when opened in Multiwrite or found through Doré Search. Product transfer must use IDs/deep links, not copy the note into another store.

The same rule applies to source linkage: a Dawn source is referenced through `LibrarySourceRef`; source text is not silently copied into personal interpretation.

## Retrieval ownership

`retrieval.fuzzy` is a Core faculty. Search, ONE, Multiwrite and Dawn Library consume it with different scopes and presentation.

Initial ranking must remain cheap and inspectable:

1. exact Scripture identity/reference;
2. lexical/phrase coverage, including Chinese n-grams;
3. personal anchor/entity/topic relations;
4. explicit Scripture graph relations supplied by Bible Intelligence/ONE;
5. linked Dawn Library sources and provenance;
6. topic-semantic similarity;
7. broad semantic similarity only after deterministic retrieval has a real-query regression baseline.

Embeddings or models are optional providers, never the identity of retrieval.

## Dawn Library is an organ, not an attachment

黎明書局 is not a database placed beside the notes feature. It participates in the same cognition loop:

`Scripture -> question -> retrieval -> source -> StudyNote -> writing/use outcome -> library.loop.observe -> verified source/retrieval lesson -> Core capability`.

Its strongest value is not merely collection size. It provides governed provenance, source quality, source relationships, reading history and evidence about which resources actually improved study and writing.

The library loop may learn source-selection and retrieval patterns. It may propose or attach source references with user-visible provenance. It must never rewrite protected user notes or silently promote a source's interpretation into the user's own claim.

## Bible Intelligence relationship

Bible Intelligence and Dawn Library are complementary learning paths:

- Bible Intelligence strengthens canonical Scripture relations: cross-reference, people, place, chronology, original language and explicit graph structure.
- Dawn Library strengthens external source/research relations: books, articles, lexicons, historical material, provenance and source usefulness.

Both feed the same Core retrieval and study workspace. Neither creates a second Scripture registry or note store.

## Promotion boundary

A product discovery is promoted to Core only when its semantics are reusable and verified. Examples:

- a Multiwrite note-edit operation stays product-local until it proves reusable;
- revision/protection semantics are Core because multiple products must preserve the same user-authored StudyNote;
- a ONE visual navigation behavior stays in ONE;
- Canon Index identity is consumed by Core rather than duplicated;
- a Dawn source-ranking lesson can become a Core retrieval rule only after evidence shows repeated usefulness.

## Memory separation

Doré must distinguish at least four truth classes:

1. canonical Scripture/source identity;
2. protected human-authored note/interpretation;
3. Doré suggestions/inferences;
4. rebuildable retrieval/index projections and learned routing evidence.

No consolidation step may collapse these classes into one mutable memory blob.

## Acceptance vocabulary

For this shared system, report separately:

- `source_committed`
- `core_model_pass`
- `core_runtime_pass`
- `consumer_adapter_pass`
- `product_pass`
- `human_use_pass`

A committed architecture file is not evidence that ONE or Multiwrite is integrated. A local deterministic skeleton passing is not evidence that the product UX is finished.

## Current implementation evidence

`dore-core/scripture_workspace.py` is the first stdlib-only implementation skeleton for shared `ScriptureAnchor`, `StudyNote`, `LibrarySourceRef`, revision-safe local persistence and deterministic fuzzy retrieval.

`dore-core/runtime/scripture-workspace-capabilities.v1.json` declares the bounded capabilities and product consumers.

`dore-core/runtime/scripture_workspace_acceptance.py` is the first executable cross-artifact acceptance. It must prove one note retains Scripture identity, Dawn source identity, fuzzy re-entry, revision safety and protected-user defaults.

## Next consolidation cut

After this pass, do not immediately add UI features. First connect the shared runtime to the Doré capability router and establish one canonical storage root/evidence envelope. Then adapters for ONE and Multiwrite can consume the same capability. Doré Search should consume the same retrieval path rather than call a second fuzzy implementation.
