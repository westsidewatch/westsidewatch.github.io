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

## 2. Principle

The editor becomes the working studio for both websites and books.

A draft exists only when the relevant product can be inspected in its real publication surface.

For visual/web work, prose or source data alone is insufficient. It must be renderable in Doré Design as an editable publication surface with same-source HTML Preview/Export.

For long-form books, the editor must support direct writing, revision, source-aware notes, protected authorship, bilingual development and eventual print output.

## 3. Shared model: content + provenance + presentation + output

Every editorial unit must keep four separable concerns:

- `content`: text, headings, quotations, notes, captions, Scripture, Hebrew/Greek strings;
- `provenance`: who authored/edited it, when, source class, protection state, claim class;
- `presentation`: page/spread/section placement, typography, grid, image/material treatment, interaction and responsive behavior;
- `output`: web HTML, responsive webpage, paged book, PDF/print, Journal or other publication target.

Visual edits must not silently mutate manuscript content.
Content edits must not silently destroy publication layout.
Output-specific behavior must not fork the canonical content into uncontrolled copies.

## 4. Product mode A — Visible Web Editor

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

## 5. Product mode B — Book Publishing Editor

The editor should support both highly visual books and text-led books.

Shared book capabilities:
- book/project library;
- chapter/section tree;
- manuscript blocks;
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

## 6. Author-protection model

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

## 7. Revision safety

Every save must create a local revision snapshot.

Required layers:

1. current local workspace;
2. immutable revision history;
3. project/book manuscript snapshots;
4. export snapshots for HTML/print proofs;
5. optional Git canonicalization for accepted milestones.

The user's writing/design must remain recoverable even if the current workspace is corrupted or an AI suggestion is rejected.

## 8. Book 01 mode — Visual Book Studio

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

## 9. Book 02 mode — Longform Manuscript Studio

Book 02 needs a writing-first editor mode.

Required capabilities:
- chapter tree;
- long-form rich/plain structured text editing;
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

## 10. Editing states

Core editing states:

### WRITE
Direct manuscript/content editing. User-created text defaults to protected.

### SUGGEST
Doré/Assistant creates suggestions, alternatives, annotations or proposed replacements without altering protected text.

### DESIGN
Visual/layout editing. Text can be flowed into publication components without changing canonical source unless explicitly edited in WRITE mode.

### PREVIEW
Actual publication output generated from the same source: webpage, HTML book, responsive surface or print representation.

## 11. AI suggestion protocol

A proposed rewrite of protected user prose must be represented as a diff/suggestion:

- source block remains intact;
- candidate block links to source block;
- reason is recorded;
- style rule invoked is recorded;
- user can Accept / Reject / Merge manually.

No auto-accept.

## 12. Local backup requirement

Because the editor is local-first, its data is itself a local backup, but this is not sufficient alone.

Required:
- atomic saves;
- timestamp/revision snapshots;
- periodic project/book manuscript exports;
- checksums for protected blocks;
- recovery test.

A protected block checksum changing without explicit user mutation is a hard failure.

## 13. Integration with current Doré Design 1.0

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

## 14. Product architecture principle

Do not build three separate products named website editor, book editor and Journal editor.

Build one **Doré Design Publishing Studio** with shared core services and publication-specific modes.

Shared core:

**Project → Content → Provenance → Design System → Composition → Interaction → Preview → Revision → Export/Publish**

Publication modes:
- `WEB`
- `BOOK`
- `JOURNAL`

Later modes may be added only if they reuse the same core rather than fork it.

## 15. Completion gates for current publishing integration

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
