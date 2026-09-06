# Multiwrite Bible Notes × ONE × Doré Retrieval Fusion v1

Status: CANONICAL PRE-IMPLEMENTATION ARCHITECTURE
Established: 2026-09-05

## Decision

Do not build “多寫查經筆記”, “ONE 搜索”, “ONE 筆記”, and “Doré Search 模糊搜索” as four independent features and then connect them with links.

They are three product surfaces over one Doré Scripture knowledge/workspace capability:

- **ONE = read/explore Scripture context**;
- **多寫查經筆記 = capture/develop the user’s own study and writing**;
- **Doré Search = retrieve/associate/re-enter Scripture, notes and research from incomplete human memory**.

The shared object is not a page and not a search result. It is a **Scripture-anchored knowledge artifact** governed by Doré Core.

## Evidence that constrains the design

1. Multiwrite’s current product direction is direct-on-publication: the visible publication is the working object, with content/provenance/presentation/output kept separable, protected human authorship, revisions, suggestions and source panels. Bible Notes must inherit this model rather than become a textarea bolted onto ONE.
2. ONE already has a canonical 66-book / 1,189-chapter identity and shared chapter study schema. Its Search roadmap explicitly requires Search/Atlas/Graph to consume the same Canon Index and forbids a separate search-only chapter registry.
3. ONE’s canonical study objects already contain story, background, connections, harmony, questions, timeline and map data. Notes should anchor to these identities; they must not copy/fork ONE’s Scripture corpus.
4. Doré Local already has a primitive fuzzy-recall path: Chinese n-gram/token extraction, coverage scoring, conversation-window recovery and original-history preference. This is useful seed behavior but is not yet sufficient for Scripture-note retrieval.
5. Doré capability embodiment requires one persistent intelligence, sparse capability activation and typed shared state instead of Search/ONE/Multiwrite acting as mini-agents.

## Product ownership

### ONE owns
- canonical Bible navigation and book/chapter identity;
- reader/study context presentation;
- chapter modules, maps, chronology, cross-reference/graph views;
- the visual action “在此處寫筆記 / 查看相關筆記”.

ONE does **not** own the note database or a private semantic search engine.

### Multiwrite owns
- note writing/editing experience;
- notebook/notebook-section organization;
- direct writing, block structure, quotations, headings, tags and manuscript promotion;
- protected human text, revision history, compare/restore;
- turning notes into outlines, lessons, articles, sermons, book material or Journal material.

Multiwrite does **not** own a second Bible corpus or a second Scripture search implementation.

### Doré Core owns shared semantics
- `ScriptureAnchor` identity resolution;
- note provenance and authorship semantics;
- retrieval/fuzzy matching;
- Bible Intelligence entity/topic/relationship expansion;
- cross-product artifact IDs;
- ranking/explanation contract;
- permissions and verification;
- promotion from note -> writing artifact without losing source lineage.

### Doré Search owns a surface, not the intelligence
Doré Search is the general conversational/search entrance to the same retrieval capability. ONE and Multiwrite can call the same capability without opening the Search UI.

## Canonical shared artifacts

### ScriptureAnchor

```json
{
  "canon":"protestant-66",
  "book":40,
  "chapter":6,
  "verse_start":25,
  "verse_end":34,
  "one_id":"40:6",
  "selection_text":null
}
```

Chapter-only anchors are valid. Verse/range anchors refine them. `one_id` must resolve through ONE’s Canon Index; no product may mint an alternate Matthew identity.

### StudyNote

```json
{
  "schema":"dore.study-note.v1",
  "id":"note:...",
  "notebook_id":"bible-study:...",
  "title":"...",
  "blocks":[],
  "anchors":[],
  "entities":[],
  "topics":[],
  "authorship":"USER",
  "protected":true,
  "provenance":{},
  "created_at":"...",
  "updated_at":"...",
  "revision":1
}
```

`anchors/entities/topics` are retrieval metadata around the human text. Doré may suggest or infer metadata, but must not silently rewrite protected note content.

### RetrievalHit

Every fuzzy result must preserve why it matched:

```json
{
  "artifact_id":"note:...",
  "kind":"study-note",
  "score":0.0,
  "signals":["exact-scripture","lexical","entity","topic","semantic","cross-reference","recent-context"],
  "matched_anchors":["40:6"],
  "snippet":"...",
  "explanation":"..."
}
```

No opaque “AI says relevant” ranking.

## What “模糊搜索” means here

The user often remembers meaning, fragments or relationships rather than exact words. Therefore fuzzy retrieval must support:

1. **Exact identity** — “馬太福音六章”, “太6:33”.
2. **Imperfect quotation** — “先求神的國那一段”, even if wording differs.
3. **Concept memory** — “父對兒子說的話”, “一天的憂慮一天當就夠了跟國度的關係”.
4. **Entity/place memory** — “基列雅比那次沒有去打便雅憫”.
5. **Relationship memory** — “那個和主禱文欠債有關的筆記”.
6. **Personal-note memory** — “我以前寫過世界的豐盛和枯乾反過來那段”.
7. **Cross-Scripture memory** — retrieve notes anchored elsewhere when explicit cross-reference/Bible Intelligence evidence connects them.
8. **Writing reuse** — “找我所有關於五穀新酒的筆記，整理成一篇文章”, where retrieval finds candidates and Multiwrite performs composition.

## Retrieval pipeline

Use a layered, cheap-first pipeline rather than sending every query to a large model.

`query -> normalize -> Scripture/entity resolution -> lexical candidates -> graph/topic expansion -> semantic candidates -> rank -> explain -> open artifact`

### L0 deterministic
- Bible reference parser and aliases;
- exact title/text/token/Chinese n-gram search;
- canonical book/chapter/verse IDs;
- note tags/anchors/entities;
- explicit ONE cross-reference edges;
- chronology/place IDs;
- recency/notebook filters.

### L1 semantic reflex
Use local/free semantic representation only when L0 is insufficient. It expands paraphrase/concept matches but never creates canonical theological facts. Candidate generation can be semantic; truth/provenance remains attached to source artifacts.

### L2 Doré judgment
Use deliberative reasoning only for genuinely ambiguous requests such as “我以前有一個想法，大概是約旦河東的豐盛反而代表世界，你幫我找”. L2 resolves intent and re-ranks/explains bounded candidates; it does not search by hallucinating missing notes.

## Ranking principle

Recommended ordering is not one universal vector score. Combine typed evidence:

`exact Scripture > exact/near lexical > user-owned anchor/entity > explicit Scripture graph > topic/entity semantic > broad embedding similarity`

Context can adjust, not erase, this order. In ONE, current book/chapter gets a bounded context boost. In Multiwrite, current notebook/project gets a bounded boost. Doré Search remains global by default.

This is deliberately different from ONE’s image policy: fuzzy semantic matching is appropriate for *retrieving candidate notes*, but must never silently assert a canonical Scripture relationship or reuse an image as source truth.

## The fusion interaction

### From ONE
User is reading Matthew 6.

- “筆記” opens the same `StudyNote` workspace in a compact Multiwrite surface, pre-anchored to `40:6`.
- “相關筆記” calls `retrieval.fuzzy` with current Scripture context and returns existing notes.
- Opening a result can expand into full Multiwrite without copying the note.
- A note link back to ONE reopens the canonical chapter/verse context.

### From Multiwrite Bible Notes
User writes freely.

- Scripture references typed/pasted are resolved to `ScriptureAnchor` suggestions.
- Doré may suggest related ONE chapters, maps, chronology, original-language material, Library sources and the user’s prior notes.
- These suggestions remain side evidence; they do not overwrite writing.
- Selecting “在 ONE 中查看” opens the canonical ONE context.

### From Doré Search
User asks in natural language.

- Doré retrieves Scripture + ONE study context + user notes + Library/research according to scope.
- Results retain type/provenance and can open directly in ONE or Multiwrite.
- “繼續寫這篇筆記” routes to the same note artifact in Multiwrite, not a new chat copy.

## ONE’s two missing features become one Doré integration

ONE currently lacks Search and Notes. Do not implement them as two unrelated ONE modules.

The integration is:

`ONE context -> Doré Scripture Workspace`

with two actions:

- **Find** = retrieve across canonical Scripture context and user knowledge;
- **Write** = create/update a Scripture-anchored artifact.

Both share the same `ScriptureAnchor`, capability router, provenance and deep-link identity. This is the seam that makes the features feel native rather than pasted together.

## Capability set

First implementation should expose these Doré-native capabilities:

- `scripture.resolve` — text/reference -> canonical anchors;
- `study.note.create`
- `study.note.update`
- `study.note.get`
- `study.note.list`
- `retrieval.fuzzy` — cross-artifact candidate retrieval with typed signals;
- `study.related` — current Scripture/note -> bounded related artifacts;
- `study.promote` — note/selection -> Multiwrite writing artifact preserving lineage;
- `product.open` — typed deep link to ONE/Multiwrite surface.

Do not create `one.search`, `one.notes`, `multiwrite.search`, `multiwrite.bible-search` as separate implementations. Product-specific commands may be aliases/routes only.

## Storage boundary

One durable local index should hold shared artifact metadata and retrieval fields. Product-owned content may remain in its canonical store, but every indexed artifact needs:

- stable ID;
- kind;
- owner/product;
- authorship/protection;
- Scripture anchors;
- entity/topic metadata;
- provenance/source refs;
- revision/content hash;
- searchable text projection;
- deep-link target.

Search indexes are rebuildable projections, never source of truth.

## Learning return path

This project is a high-value Core training ground:

- user corrections to bad fuzzy matches -> retrieval regression set;
- accepted related-note suggestions -> ranking evidence;
- rejected suggestions -> negative evidence;
- repeated Scripture alias resolution -> compile into L0;
- repeated semantic routes -> compile toward L1;
- Multiwrite note-to-article/lesson flows -> Editor capability learning;
- ONE navigation failures -> canonical identity/deep-link regression.

The user’s theological conclusions remain user-authored evidence; Doré learns retrieval/routing/editorial method, not doctrinal authority from frequency alone.

## First engineering slice

Build the shared spine before UI polish:

1. `ScriptureAnchor` parser/resolver against ONE Canon Index identity.
2. `StudyNote` schema + local CRUD + immutable revisions/protected text checksum.
3. shared searchable artifact projection.
4. `retrieval.fuzzy` v0 using deterministic reference/entity/token/n-gram signals plus explicit ONE graph signals; preserve current complete-recall lessons.
5. deep-link contract ONE <-> Multiwrite.
6. minimal ONE “筆記 / 相關筆記” entry and Multiwrite “查經筆記” workspace consuming the same artifacts.
7. regression set of real fuzzy queries before adding embeddings.
8. only after deterministic baseline is measured, add local semantic retrieval if it improves recall without unacceptable false positives/resource cost.

## Acceptance

The first fusion milestone passes only when all are true:

1. A note created from ONE appears in Multiwrite as the same artifact ID.
2. Editing it in Multiwrite is visible from ONE without copy/sync duplication.
3. An imprecise query can retrieve a known note and show why it matched.
4. Exact Scripture identity outranks broad semantic similarity.
5. ONE Search and Multiwrite search use the same retrieval capability/index.
6. No second Bible chapter registry exists.
7. Protected human note text cannot be silently mutated by Doré.
8. A note can deep-link to ONE and ONE can deep-link back to the note.
9. Search index can be rebuilt from canonical artifacts.
10. No paid API is required for baseline operation.

## Architectural sentence

**ONE supplies the biblical place where thought begins; Multiwrite supplies the place where thought becomes durable writing; Doré supplies the memory and associative retrieval that lets the same thought be found again.**
