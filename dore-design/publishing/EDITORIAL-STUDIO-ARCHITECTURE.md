# Westside Publishing Editorial Studio Architecture

Status: CANONICAL IMPLEMENTATION SPEC
Established: 2026-09-04
Parent: `dore-design/publishing/PUBLISHING-PROGRAM.md`

## 1. Product direction

Doré Design is not only a layout tool and not only a book-specific utility.

Its long-term product direction is a **directly visible publishing editor** with two primary first-class products:

1. **Visible Web Editor** — visually edit real webpages and inspect the actual HTML/web result immediately.
2. **Book Publishing Editor** — write, edit, design, preview, version and export books/Journals from the same editorial environment.

The two modes share one core idea:

> **The publication surface is part of the source of truth. What cannot be directly seen, edited and previewed is not yet a finished draft.**

The editor should therefore evolve toward a local-first hybrid of visual web editor, long-form manuscript editor and publication studio rather than split into unrelated tools.

## 2. Direct-on-publication principle

The product must change the user's mental model from **writing a source file that later becomes a book** to **writing directly on the book itself**.

Word/Markdown/code remain valid import/export/interchange formats, but they are not the primary user experience.

Canonical product sentence:

> **使用這個編輯器，就是在你的書上直接寫。**

The visible book/web publication is the working object, not a detached mockup. The same canonical project state should drive editing, preview, revision, translation companions, design and final outputs.

For books this means the author can place the cursor in the actual chapter/page reading surface and continue writing there. For visual books it means design decisions are made on the actual spread/publication surface. For websites it means the visible editable page corresponds to the real web output rather than a separately reconstructed mockup.

## 3. AI-native publishing studio

AI is not a replacement author and not an opaque rewrite button. It is a set of explicit publishing collaborators connected to the canonical book/project.

AI-assisted capabilities may include:
- proofreading and typo detection;
- grammar and style diagnostics;
- source/fact/claim checking workflows;
- terminology consistency;
- Chinese ↔ English companion drafts;
- bilingual alignment;
- comments and rewrite suggestions;
- chapter/structure analysis;
- bibliography/footnote assistance;
- index/glossary assistance;
- image/art-direction suggestions;
- cover concepts and cover-design generation through Doré's visual resources;
- typography/layout alternatives;
- HTML/web adaptation;
- print adaptation;
- accessibility checks.

All AI work must respect provenance and Author Lock. Protected human text is never silently overwritten.

The product value is therefore not merely “AI writes text.” It is:

**Author's canonical work + visible publication surface + protected provenance + specialist AI collaborators + Doré design intelligence + multi-format publishing.**

## 4. Doré resource integration

The editor becomes the product surface through which Doré's accumulated resources become useful to an author/designer.

Potential resource layers:
- design-system knowledge;
- Storybook visual-learning evidence;
- Brand Bible / VI / CI research;
- typography and color systems;
- publication templates;
- image/material/art-direction knowledge;
- language/style guides;
- 黎明書局 research loop;
- source/provenance research;
- bilingual editorial methods;
- book-cover design experiments;
- web/HTML/print rendering systems.

Doré should expose these as purposeful editorial/design capabilities, not as an internal knowledge dump.

## 5. Shared model: content + provenance + presentation + output

Every editorial unit must keep four separable concerns:

- `content`: text, headings, quotations, notes, captions, Scripture, Hebrew/Greek strings;
- `provenance`: who authored/edited it, when, source class, protection state, claim class;
- `presentation`: page/spread/section placement, typography, grid, image/material treatment, interaction and responsive behavior;
- `output`: web HTML, responsive webpage, paged book, PDF/print, Journal or other publication target.

Visual edits must not silently mutate manuscript content.
Content edits must not silently destroy publication layout.
Output-specific behavior must not fork the canonical content into uncontrolled copies.

## 6. Product mode A — Visible Web Editor

The editor should become capable of opening a real webpage/project and allowing direct visual editing of the page that will actually render.

Required direction:
- live page tree / route tree;
- direct selection and manipulation of visible elements;
- text/content editing in context;
- layout/grid/spacing/typography controls;
- responsive desktop/tablet/mobile views;
- image/material/component controls;
- interaction/motion states;
- component/source linkage rather than screenshot-only editing;
- same-source HTML Preview and export/build output;
- compare/revision history;
- protected production boundaries and explicit promotion.

The key product distinction is **what-you-see is the actual webpage state**, not a detached mockup whose HTML is rebuilt elsewhere later.

For New Westside, this means Storybook/Doré experiments can mature into visible editable pages before any production promotion.

## 7. Product mode B — Book Publishing Editor

The editor should support both highly visual books and text-led books.

Shared book capabilities:
- book/project library;
- chapter/section tree;
- manuscript blocks;
- direct writing in the rendered reading/page surface;
- spreads/pages;
- figures/captions/notes;
- comments and suggestions;
- source/provenance panel;
- typography and publication styles;
- bilingual paired content;
- print preview;
- HTML book preview;
- PDF/print export path;
- Journal adaptation surfaces;
- revision history and recoverability.

The book editor must not be a separate disconnected app. It should reuse the same Doré Design engine, project model, preview/export architecture and visual editing concepts.

## 8. Author-protection model

Human-authored material requires explicit protection.

Recommended block fields:

- `id`
- `book_id`
- `chapter_id`
- `type`
- `text`
- `language`
- `authorship`: `USER | DORE | ASSISTANT | MIXED`
- `protected`: boolean
- `protection_scope`: `TEXT | BLOCK | CHAPTER`
- `created_at`
- `updated_at`
- `source_ref`
- `revision`

### Hard rule

If `authorship=USER` and `protected=true`, automated agents must not replace, delete, normalize, shorten, translate in-place, or silently edit the protected text.

AI may:
- comment;
- propose an alternate version;
- create a linked suggestion;
- add margin notes;
- flag factual/theological/style concerns;
- create an English companion draft in a separate block.

AI may not write over the source.

### Explicit unlock

Only a user action in the editor may unlock protected human text for direct mutation. An automated tool call must not remove protection.

## 9. Revision safety

Every save must create a local revision snapshot.

Required layers:

1. current local workspace;
2. immutable revision history;
3. project/book manuscript snapshots;
4. export snapshots for HTML/print proofs;
5. optional Git canonicalization for accepted milestones.

The user's writing/design must remain recoverable even if the current workspace is corrupted or an AI suggestion is rejected.

## 10. Book 01 mode — Visual Book Studio

Book 01 needs a publication-first editor mode.

Required surfaces:
- manuscript outline;
- spreads/pages;
- gate/chapter-transition surfaces;
- diagrams/specimens;
- Storybook experiment import/reference;
- Journal special layouts;
- HTML Preview;
- HTML Export;
- print preview/PDF proof path.

Canonical acceptance:

**No preview, no draft.**

A visual proposal is only a draft when it is visible in the editor and inspectable through same-source HTML Preview.

The user must be able to comment on or directly adjust:
- hierarchy;
- typography;
- page/spread sequence;
- color/material;
- image placement;
- gate/threshold behavior;
- desktop/mobile transformation;
- print equivalent.

## 11. Book 02 mode — Longform Manuscript Studio

Book 02 needs a writing-first editor mode.

Required capabilities:
- chapter tree;
- long-form rich/plain structured text editing;
- direct writing in the actual book reading surface;
- fast append-at-cursor writing by the user;
- source/footnote side panel;
- inline Hebrew/Greek support;
- comments and suggestions separate from source text;
- human-protected blocks;
- AI draft blocks;
- compare/revision view;
- Chinese/English paired view;
- claim labels: `TEXT / LEXICAL_FACT / INTERPRETATION / THEOLOGICAL_SYNTHESIS / HISTORY / AUTHOR_HYPOTHESIS / DEVOTIONAL_APPLICATION`;
- chapter word/character counts;
- export to clean manuscript Markdown/HTML/print.

The user must be able to keep writing directly inside Doré Design without needing to edit JSON or code.

## 12. Editing states

Core editing states:

### WRITE
Direct manuscript/content editing. User-created text defaults to protected.

### SUGGEST
Doré/Assistant creates suggestions, alternatives, annotations or proposed replacements without altering protected text.

### DESIGN
Visual/layout editing. Text can be flowed into publication components without changing canonical source unless explicitly edited in WRITE mode.

### PREVIEW
Actual publication output generated from the same source: webpage, HTML book, responsive surface or print representation.

## 13. AI suggestion protocol

A proposed rewrite of protected user prose must be represented as a diff/suggestion:

- source block remains intact;
- candidate block links to source block;
- reason is recorded;
- style rule invoked is recorded;
- user can Accept / Reject / Merge manually.

No auto-accept.

## 14. Local backup requirement

Because the editor is local-first, its data is itself a local backup, but this is not sufficient alone.

Required:
- atomic saves;
- timestamp/revision snapshots;
- periodic project/book manuscript exports;
- checksums for protected blocks;
- recovery test.

A protected block checksum changing without explicit user mutation is a hard failure.

## 15. Integration with current Doré Design 1.0

Current Doré Design already has multi-page workspace, local revision history, direct manipulation, HTML Preview and HTML Export. The publishing/web studio should extend this system rather than create disconnected editors.

Required implementation direction:
- evolve from page-only workspace to multi-project `WEB | BOOK | JOURNAL` workspace types;
- extend schema beyond `text/rule/block` toward manuscript-aware nodes, linked content blocks and real web components;
- keep page/canvas editing for visual publication;
- add route/navigation model for webpages;
- add book/document navigation for publications;
- add provenance/protection metadata;
- add long-form editor pane;
- ensure Preview/Export consume the same canonical workspace/manuscript state;
- preserve current undo/history behavior;
- never weaken production-site protection.

## 16. Product architecture principle

Do not build three separate products named website editor, book editor and Journal editor.

Build one **Doré Design Publishing Studio** with shared core services and publication-specific modes.

Shared core:

**Project → Content → Provenance → Design System → Composition → Interaction → AI Collaboration → Preview → Revision → Export/Publish**

Publication modes:
- `WEB`
- `BOOK`
- `JOURNAL`

Later modes may be added only if they reuse the same core rather than fork it.

## 17. Mac application / commercial-product direction

The local-first architecture is compatible with a future packaged macOS application.

Potential commercial product proposition:

> **Write on the book itself. Design on the publication itself. Let AI assist around your authorship without taking ownership away from you.**

A future Mac product may combine:
- local project/manuscript storage;
- visual web/book editing;
- protected human authorship;
- revision/history;
- AI provider/model connections;
- optional user-supplied API credentials or product-managed AI plans, subject to provider terms and cost controls;
- Doré specialist resources/skills;
- bilingual editorial assistance;
- cover and publication design;
- HTML/PDF/print/web publishing.

Commercialization must remain a separate product/legal/security milestone. It requires licensing review, privacy/security design, API-provider terms, cost accounting, sandboxing, code signing/notarization, update architecture, backup/recovery and payment/subscription decisions before release.

Do not assume current local prototype is commercially ready.

## 18. Doré model evolution

The product should keep Doré's **orchestration/intelligence layer** concept separate from the underlying foundation model.

Doré can become increasingly capable by combining:
- durable domain knowledge;
- learned editorial/design methods;
- retrieval and source provenance;
- specialist skills/tools;
- user-approved style systems;
- visual/browser evidence loops;
- project memory;
- one or more external or local foundation models.

A paid Mac app can fund model/API usage and future training/research, but charging for the app does **not by itself turn Doré into a foundation model**. A true independently trained large model would be a separate technical and financial program involving data governance, training infrastructure, evaluation, safety, inference and substantial compute.

Nearer-term product architecture should therefore be model-agnostic: Doré is the publishing/design intelligence and orchestration layer, while foundation models are replaceable providers behind explicit interfaces.

## 19. Completion gates for current publishing integration

The current integration milestone is not complete until:

1. both books can be opened as named editor projects;
2. Book 01 can render at least one complete editable spread and same-source HTML preview;
3. Book 02 can import/open substantial manuscript text and allow direct user continuation;
4. user-created protected text survives AI edit attempts byte-for-byte;
5. AI suggestions can be created without mutating protected source;
6. local history can restore prior manuscript state;
7. Chinese/English paired blocks are representable;
8. preview/export are deterministic from the same source;
9. no production homepage mutation occurs.

The broader product direction is fulfilled only when the same editor can reliably serve as both a directly visible webpage editor and a real book-publishing editor without sacrificing source integrity, revision safety or publication fidelity.
