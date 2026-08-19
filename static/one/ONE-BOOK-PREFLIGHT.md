# ONE — New Book Preflight

Status: **MANDATORY**

This checklist must be completed **before starting any new Bible book in ONE** and before any substantial rebuild of an existing book.

The purpose is to prevent a known failure mode: the canonical ONE rules already exist, but implementation starts from memory, improvisation or a new local experiment and silently ignores them.

## Required first action

Before writing book data, illustration mappings, map data, timeline data, renderer changes or CSS:

1. Read `ONE-VISUAL-STANDARD.md` in full.
2. Read `ONE-COVER-ILLUSTRATION-MASTER.md` in full. It is the binding cover/illustration layer of the mother rule and has equal project-wide force for cover and illustration decisions.
3. Confirm the current branch contains the latest versions of both standards.
4. Inspect at least one previously completed book that already implements the relevant pattern correctly.
5. Reuse the shared ONE renderer/schema unless the canonical standard explicitly requires otherwise.

Do not start a new book by designing from scratch.

## Canonical new-book production order

For every new Bible book, use this order unless a canonical project-wide rule explicitly requires otherwise:

1. **Audit and activate Gustave Doré originals first.** Before building new visual assets, search the canonical 241-plate Doré Original Library for every plate genuinely belonging to the book and map each verified plate to its correct chapter as `P1 ORIGINAL_LOCKED`. If more than one original belongs to a chapter, retain all originals in the immutable library and deliberately select the strongest chapter-cover assignment without discarding the others.
2. **Build the complete book/chapter study structure.** Register the whole book and all chapters in the shared ONE schema so the book can go online independently of missing generated artwork.
3. **Add geography where the text genuinely requires it.** Maps are a study tool, not a quota. Route-heavy books such as Acts may use geography as a major structural layer; visionary, poetic or epistolary chapters may omit maps when geography adds no real interpretive value.
4. **Add chronology, comparison/harmony, cross-references and other genre-appropriate modules.** Use only modules that genuinely illuminate the text.
5. **Run the canonical cover/body presentation through the shared renderer.** Doré originals already mapped in step 1 must appear automatically through the central cover policy and may never be displaced by local book code.
6. **Record the remaining illustration gaps.** Chapters without a valid Doré original or other approved fixed historical asset enter the Missing Plate backlog; they do not receive provisional substitutes merely to make the book look complete.
7. **Publish the book.** Missing ONE Studio plates do not block book publication.
8. **Only later, when the project enters the visual-production phase, create ONE Studio Doré-continuation plates for the recorded gaps.** Generated plates may fill only genuinely unassigned chapters and must pass the full Doré Studio workflow.

The operational shorthand is:

**Doré originals → complete book data → maps/chronology/other study modules → canonical rendering → missing-plate backlog → publication → later ONE Studio generation.**

The Doré-original audit is therefore not a finishing pass. It is the **first visual action for every new book**.

## Preflight questions

Before implementation begins, answer internally:

- What genre is this book?
- Which canonical modules genuinely apply: map, chronology, comparison/harmony, route, resources?
- Which modules should be omitted rather than filled artificially?
- Which Doré plates are `ORIGINAL_LOCKED` for this book/chapter and therefore untouchable?
- Which historical illustrations are genuinely chapter-specific or valid under the master priority hierarchy?
- Which chapters have no sufficiently strong historical illustration and should remain candidates for future fixed ONE Studio assets rather than receive a forced mismatch?
- Which chapters genuinely need maps?
- What level of chronology precision is historically supportable?
- What existing ONE book provides the best working technical pattern for registration, load order, renderer and mobile layout?

## Non-negotiable inheritance

Every new book automatically inherits, without redesign:

- canonical chapter-cover system;
- dark antique binding field;
- First Light Gold (`#CEBD74`) foil language;
- ornate double-line brand-gold frame and four corner ornaments;
- illustration priority hierarchy and `ORIGINAL_LOCKED` protection;
- fixed-asset / generate-once lifecycle;
- canonical engraving-plate presentation;
- Dawn Morning Star geometry and usage rules;
- cover typography hierarchy;
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

## Doré illustration lane — mandatory but non-blocking

Doré is the canonical production path for **new generated Bible illustration**, but Doré must never become a publication dependency for a Bible book.

During book production, perform only the illustration audit needed to establish the correct state:

1. Identify every Gustave Doré original plate belonging to the book/chapter and preserve every `ORIGINAL_LOCKED` placement. Original Doré always has first priority and may not be regenerated, replaced, reassigned or displaced by a generated asset. **This audit and activation happens before any generated-art decision and before treating the book as visually incomplete.**
2. Identify any other fixed historical asset that is valid under `ONE-COVER-ILLUSTRATION-MASTER.md`.
3. Record chapters that still lack a sufficiently strong illustration as the Missing Plate backlog. **Do not fill those gaps with provisional AI images, fuzzy matches, inherited media or batch-generated placeholders.**
4. Continue the Bible-book production and publication pipeline. Missing generated plates do not block completion or release of the book.

Only when a specific missing plate is actually selected for creation does that plate enter the Doré Studio workflow. Before generating it, read the current Doré living rules, visual grammar, Scripture-to-image reasoning, visual ancestry research and learning log. The plate must pass through Scripture reading → visual ancestry → composition reasoning → generation → human evaluation → learning update. It must never go directly from a chapter reference to an image prompt.

Generated Doré work belongs to the separate ONE Studio / Doré generated-asset library and must never be written into, confused with or used to mutate the Gustave Doré original-plate library. A generated plate remains replaceable and improvable; an `ORIGINAL_LOCKED` plate does not.

Doré's learning may continue independently across books and over time. Human critique, failures and successful discoveries should be fed back into the Doré learning record so later plates inherit accumulated visual knowledge.

**Doré is an illustration-production dependency, never a Bible-book publication dependency.**

**No new generated Bible illustration may enter ONE outside the Doré workflow.**

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

- Doré-original audit was completed before any generated-art decision;
- every verified Doré original belonging to the book is retained in the canonical original library and every selected chapter assignment is `ORIGINAL_LOCKED`;
- book entry works;
- chapter entry works;
- mobile titles remain inside the viewport;
- optional media never controls registration;
- illustrations belong to the correct chapters;
- `ORIGINAL_LOCKED` Doré placements remain unchanged;
- no fuzzy-search or inherited image fallback exists;
- missing Doré-generated plates do not block book publication;
- no provisional or batch-generated AI placeholder has been introduced to make the book appear visually complete;
- cover uses the canonical gilt frame / title / Morning Star system;
- body illustration uses the canonical engraving-plate presentation without distortion;
- maps appear only where useful and render independently;
- chronology is accurate and genre-appropriate;
- Scripture slots contain Scripture/source content only;
- no stale previous-book media appears;
- previous/next chapter navigation works;
- at least one previously completed book still works after any shared-system change.

For any shared-system modification, test multiple genres as required by `ONE-VISUAL-STANDARD.md`.

## Rule maintenance

`ONE-VISUAL-STANDARD.md` is the project mother rule. `ONE-COVER-ILLUSTRATION-MASTER.md` is its locked cover/illustration specification and must be treated as part of that mother rule, not as optional documentation.

When production reveals a better project-wide rule, update the canonical standards deliberately, record the improvement, and apply it prospectively to later books and retroactively where appropriate.

Do not let local exceptions accumulate outside the mother rule.
