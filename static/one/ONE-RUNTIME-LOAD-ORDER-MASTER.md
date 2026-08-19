# ONE — Runtime Load Order Master

Status: **MANDATORY / CANONICAL**

This rule exists to prevent a Bible book from being present in source data but unavailable or non-clickable in ONE at runtime.

## Core rule

Bible-book registration is a **content/runtime responsibility**, never a cover-policy responsibility.

Every book module that is intended to be online must be loaded explicitly in `index.html` before `one-cover-policy.js` and before `one-app.js`.

Do not use `document.write()`, dynamic script injection, delayed preload, cover-policy bootstrap, or a book-local workaround to make a book available.

## Canonical order

1. `one-data.js` and established book modules.
2. Newly published book-data modules, explicitly listed in `index.html`.
3. Doré original registry and immutable 241-plate inventory.
4. Book-specific Doré audits/mappings that depend on the registry.
5. Geography/chronology corrections that must exist before rendering.
6. ONE Studio fixed-asset registry.
7. `one-cover-policy.js` — presentation/illustration resolution only; it must not load books.
8. Runtime registration audits.
9. `one-app.js`.
10. Post-app synchronization only where a canonical shared system still requires it.

## Availability invariant

For every online book `N`:

- `ONE_DATA.books` contains the canonical book metadata;
- `ONE_DATA.studyBooks[N]` exists before `one-app.js` executes;
- `studyBooks[N].chapters.length` equals the canonical chapter count;
- `chapterStudies` contains the same number of chapters;
- the cover rail therefore marks the book `has-study`, enables the confirmation action, and can enter chapter 1 without any later network registration step.

A book must never become clickable only because an illustration resolver, map module, or cached secondary script happened to execute.

## Cache rule

Whenever the runtime load graph changes, update the affected script cache key in `index.html`. A new book is not considered published until the HTML entry point points at the new registration graph.

## Regression rule

A load-order change is a shared-system change. Before merge, verify:

- newly added books are available and chapter counts match;
- representative previously completed books remain registered;
- Doré originals still resolve after registration;
- maps and chronology remain independent of book availability;
- `one-cover-policy.js` contains no book loader or dynamic registration code.

## Current correction

The 2026-08-18 epistle rollout exposed the failure mode this rule forbids: book data was correct, but registration was nested inside `one-cover-policy.js`. The canonical correction moves registration into the explicit `index.html` load graph and removes nested loaders from both cover policy and the Pentateuch Doré audit.
