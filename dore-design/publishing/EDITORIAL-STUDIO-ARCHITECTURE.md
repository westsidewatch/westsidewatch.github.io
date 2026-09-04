# Westside Publishing Editorial Studio Architecture

Status: CANONICAL IMPLEMENTATION SPEC
Established: 2026-09-04
Parent: `dore-design/publishing/PUBLISHING-PROGRAM.md`

## 1. Principle

The editor is not only a layout tool. It becomes the working studio for both books.

A draft exists only when the relevant product can be inspected in its real publication surface.

For Book 01, a visual/design manuscript is not considered a draft merely because prose or source data exists. It must be renderable in Doré Design as an editable visual publication and must have same-source HTML Preview/Export.

For Book 02, the editor must support long-form writing, revision, source-aware notes and bilingual development without allowing AI to overwrite human-authored protected text.

## 2. Shared model: content + provenance + presentation

Every manuscript unit must carry three separable concerns:

- `content`: text, headings, quotations, notes, captions, Scripture, Hebrew/Greek strings;
- `provenance`: who authored/edited it, when, source class, protection state, claim class;
- `presentation`: page/spread/section placement, typography, grid, image/material treatment, interaction and print behavior.

Visual edits must not silently mutate manuscript content.
Content edits must not silently destroy publication layout.

## 3. Author-protection model

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

## 4. Revision safety

Every save must create a local revision snapshot.

Required layers:

1. current local workspace;
2. immutable revision history;
3. book-level manuscript snapshots;
4. export snapshots for HTML/print proofs;
5. optional Git canonicalization for accepted milestones.

The user's writing must remain recoverable even if the current workspace is corrupted or an AI suggestion is rejected.

## 5. Book 01 editor mode — Visual Book Studio

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

## 6. Book 02 editor mode — Longform Manuscript Studio

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

## 7. Suggested editorial interaction

Three editing states:

### WRITE
Direct manuscript editing. User-created text defaults to protected.

### SUGGEST
Doré/Assistant creates suggestions, alternatives, annotations or proposed replacements without altering protected text.

### DESIGN
Visual/layout editing. Text can be flowed into publication components without changing canonical source unless explicitly edited in WRITE mode.

## 8. AI suggestion protocol

A proposed rewrite of protected user prose must be represented as a diff/suggestion:

- source block remains intact;
- candidate block links to source block;
- reason is recorded;
- style rule invoked is recorded;
- user can Accept / Reject / Merge manually.

No auto-accept.

## 9. Local backup requirement

Because the editor is local-first, its data is itself a local backup, but this is not sufficient alone.

Required:
- atomic saves;
- timestamp/revision snapshots;
- periodic book-level manuscript exports;
- checksums for protected blocks;
- recovery test.

A protected block checksum changing without explicit user mutation is a hard failure.

## 10. Integration with current Doré Design 1.0

Current Doré Design already has multi-page workspace, local revision history, direct manipulation, HTML Preview and HTML Export. The publishing studio should extend this system rather than create a disconnected editor.

Required implementation direction:
- extend workspace schema beyond `text/rule/block` toward manuscript-aware nodes or linked content blocks;
- keep existing page/canvas editing for visual publication;
- add book/document navigation above pages;
- add provenance/protection metadata;
- add long-form editor pane for Book 02;
- ensure Preview/Export consume the same canonical workspace/manuscript state;
- preserve current undo/history behavior;
- never weaken production-site protection.

## 11. Completion gates

The integration is not complete until:

1. both books can be opened as named editor projects;
2. Book 01 can render at least one complete editable spread and same-source HTML preview;
3. Book 02 can import/open substantial manuscript text and allow direct user continuation;
4. user-created protected text survives AI edit attempts byte-for-byte;
5. AI suggestions can be created without mutating protected source;
6. local history can restore prior manuscript state;
7. Chinese/English paired blocks are representable;
8. preview/export are deterministic from the same source;
9. no production homepage mutation occurs.
