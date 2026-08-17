# ONE — New Book Preflight

Status: **MANDATORY**

This checklist must be completed **before starting any new Bible book in ONE** and before any substantial rebuild of an existing book.

The purpose is to prevent a known failure mode: the canonical ONE rules already exist, but implementation starts from memory, improvisation or a new local experiment and silently ignores them.

## Required first action

Before writing book data, illustration mappings, map data, timeline data, renderer changes or CSS:

1. Read `ONE-VISUAL-STANDARD.md` in full.
2. Confirm the current branch contains the latest version of that standard.
3. Inspect at least one previously completed book that already implements the relevant pattern correctly.
4. Reuse the shared ONE renderer/schema unless the canonical standard explicitly requires otherwise.

Do not start a new book by designing from scratch.

## Preflight questions

Before implementation begins, answer internally:

- What genre is this book?
- Which canonical modules genuinely apply: map, chronology, comparison/harmony, route, resources?
- Which modules should be omitted rather than filled artificially?
- Which historical illustrations are genuinely chapter-specific?
- Which chapters require generated illustrations under the canonical ONE art direction?
- Which chapters genuinely need maps?
- What level of chronology precision is historically supportable?
- What existing ONE book provides the best working technical pattern for registration, load order, renderer and mobile layout?

## Non-negotiable inheritance

Every new book automatically inherits, without redesign:

- canonical chapter-cover system;
- ornate brand-gold frame;
- illustration hierarchy;
- Morning Star rules;
- brand-gold palette;
- chapter module order;
- Scripture rules;
- map schema/renderer;
- Biblical Chronology / time-scroll renderer;
- cross-reference hierarchy;
- navigation and book-entry behavior;
- registry/load-order architecture;
- responsive/mobile heading policy;
- Dawn Library resource-card system;
- regression-first debugging rule.

A new book is new **content**, not a new ONE design system.

## Shared-system change gate

If implementation appears to require changing any shared renderer, navigation logic, registry model, CSS system, map schema, timeline schema, cover framework, typography hierarchy or responsive behavior:

1. Stop treating the problem as book-local.
2. Compare with the earlier working implementation.
3. Decide whether this is a genuine project-wide improvement or a local data problem.
4. If project-wide, update the canonical standard and shared system first.
5. Regression-test representative completed books before continuing the new book.

Never silently alter a shared system just to make one new book work.

## Completion gate

A new book is not complete merely because its own pages look correct.

Before PR/merge, verify:

- book entry works;
- chapter entry works;
- mobile titles remain inside the viewport;
- optional media never controls registration;
- illustrations belong to the correct chapters;
- maps appear only where useful and render independently;
- chronology is accurate and genre-appropriate;
- Scripture slots contain Scripture/source content only;
- no stale previous-book media appears;
- previous/next chapter navigation works;
- at least one previously completed book still works after any shared-system change.

For any shared-system modification, test multiple genres as required by `ONE-VISUAL-STANDARD.md`.

## Rule maintenance

`ONE-VISUAL-STANDARD.md` is canonical but living. When production reveals a better project-wide rule, update the canonical standard deliberately, record the improvement, and apply it prospectively to later books and retroactively where appropriate.

Do not let local exceptions accumulate outside the mother rule.
