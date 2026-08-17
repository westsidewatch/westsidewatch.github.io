# ONE — Canonical Visual & System Standard

Status: **LOCKED / CANONICAL**

This document is the permanent design, content-structure and interaction standard for **all 66 books and all chapters in ONE**. New books and future revisions MUST follow this standard. Do not restart visual, map, timeline, navigation or chapter-structure exploration book-by-book. Any change to these rules is a project-wide ONE system change, not a local book tweak.

## 1. Core principle

ONE is one visual and reading system, not 66 independently designed books.

Every chapter must belong to the same family: **classical engraved biblical imagery + dark antique book texture + Westside Watch brand gold + ornate antique frame + restrained typography + shared chapter architecture**.

Consistency takes priority over novelty.

## 2. Illustration source hierarchy

For every chapter, use this order:

1. **Verified historical illustration exists and genuinely corresponds to the chapter/event** → use the historical illustration.
2. **No reliable corresponding historical illustration exists** → create a new illustration based on the actual content of that chapter.

Never fill a missing illustration by recycling an unrelated biblical scene merely because it is Old Testament or New Testament.

Never inherit the previous chapter/book image as a fallback.

Never use a New Testament image for an Old Testament chapter, or vice versa, unless the design is explicitly presenting a cross-reference rather than a chapter illustration.

## 3. Existing historical illustrations

Historical illustrations are source material, not a separate visual system.

When a verified Doré or other approved historical engraving is used:

- preserve the original narrative image;
- do not redraw it merely to make it different;
- integrate it into the SAME cover system used by generated illustrations;
- apply the same dark engraving treatment, contrast discipline, typography, brand-gold treatment and ornate frame;
- crop/reposition only as necessary for the established cover composition;
- do not allow the historical source to create a visibly different cover family.

The result should feel almost indistinguishable in art direction from the approved generated-cover examples.

## 4. Generated illustrations

When no reliable chapter-specific historical illustration exists, generate the missing image from the chapter itself.

### Required art direction

Generated work must stay extremely close to the approved ONE reference style:

- nineteenth-century biblical engraving character;
- Gustave Doré–like dramatic engraving language;
- black / charcoal / deep sepia dominant image;
- dense etched linework and cross-hatching;
- monumental biblical scale;
- dramatic but controlled light;
- solemn, classical, theological rather than fantasy/concept-art styling;
- antique printed-book feeling;
- no modern cinematic color grading;
- no glossy digital-painting look;
- no anime, graphic-novel, photorealistic-film-still or contemporary fantasy language.

Do **not** continue creatively drifting the style. The approved examples are the target, not a starting point for further stylistic exploration.

### Content fidelity

The generated scene must be derived from the chapter's actual subject, people, geography, action, prophetic imagery and theological emphasis. Do not invent a generic biblical scene simply to fill space.

### One-generation / fixed-asset rule

Generated chapter illustrations are **persistent production assets, not disposable runtime output**.

For every chapter that requires a generated illustration:

1. Read and understand the actual chapter content first.
2. Generate **one deliberate candidate** in the canonical ONE / Doré-like style.
3. Once that candidate is accepted into the repository, it becomes the fixed canonical illustration for that chapter.
4. Store and reference the accepted image as a stable asset; page loads, builds, future sessions and new book work must reuse that exact asset.
5. **Never automatically regenerate an accepted illustration.**
6. **Never generate multiple alternatives by default.** Do not create batches, exploratory variants, alternate compositions or repeated generations merely to “improve” a chapter.
7. If the accepted image is not satisfactory, wait for explicit editorial feedback describing what should change. Only then create a revised version addressing that feedback.
8. After a revision is explicitly approved, that revised image replaces the earlier asset and becomes the new fixed canonical version. Do not continue generating more versions after approval.
9. A code refactor, renderer change, metadata cleanup, book rebuild, cache change or new session must never trigger illustration regeneration.
10. `pendingGeneratedIllustrations` means “a chapter still needs its first canonical asset”; it must never mean “regenerate an existing asset”.

This rule applies to **all current and future ONE books and all 66-book production work**. Illustration generation is an editorial creation step performed once per missing chapter, not an ongoing automated process.

The purpose is stability, cost/control, visual continuity and editorial traceability: each chapter should have one known illustration identity unless a human explicitly requests a revision.

## 5. Canonical ornate frame

The newly approved dark antique cover with the fine **brand-gold double-line frame and floral/baroque corner ornaments** is the canonical frame for ONE chapter covers.

This same frame language applies to:

- historical-illustration covers;
- generated-illustration covers;
- all Old Testament books;
- all New Testament books.

Do not revert illustrated covers to the older plain-line frame.

The frame is decorative but subordinate to the image and title. Keep its proportions, line weight, corner ornament density and antique character consistent across books.

## 6. Brand gold

All cover-system gold must use the established **Westside Watch / ONE brand gold** rather than arbitrary yellow, orange, brass or metallic gradients.

Brand gold is used for:

- frame lines and ornaments;
- book/chapter identification;
- principal cover title where appropriate;
- fine dividers;
- small approved decorative marks;
- the Morning Star when used.

Gold should read as restrained antique print/foil, not luminous modern neon.

## 7. Morning Star

The newly approved refined **Morning Star** form is the canonical ONE Morning Star.

It is a **decorative brand element, not a mandatory badge**.

Use it only when the composition or biblical imagery naturally supports it—for example light, dawn, heaven, guidance, promise, glory or a suitable celestial field.

Do not force the Morning Star into every illustration.

When it is not appropriate inside the narrative image, it may be omitted entirely. A cover remains fully canonical without it.

Do not redesign the Morning Star from book to book.

## 8. Cover typography and hierarchy

Maintain the established ONE hierarchy rather than redesigning each book:

- book + chapter identification;
- concise Chinese chapter title;
- English book/chapter line where the established template calls for it;
- restrained ornamental divider only when useful.

Typography must remain classical and editorial. Do not bake workflow notes into the cover.

Forbidden visible production text includes phrases such as:

- 無可靠插圖
- generated illustration
- fallback
- placeholder
- AI generated

Such information may exist only in internal metadata/documentation.

## 9. Canonical map rules

Maps are a shared ONE study system and are **content-driven, not mandatory decoration**.

### When to use a map

Use a map when geography materially improves understanding, especially for:

- journeys and migrations;
- military campaigns and invasions;
- borders, tribal territories and land division;
- exile and return;
- prophetic oracles involving multiple nations/regions;
- ministry routes;
- missionary journeys;
- city-to-city narrative movement;
- empire relationships where location explains the text.

Do not add a map merely because a place name appears.

### Book-level flexibility

Different books require different map density:

- Genesis / Exodus / Joshua / Judges / Kings / Chronicles: frequent maps where narrative movement requires them.
- Psalms: generally no map; only exceptional teaching need would justify one.
- Isaiah and other prophets: contextual regional/empire maps for relevant sections, not one forced map per chapter.
- Gospels: maps where ministry movement or geography materially helps.
- Acts: map support is especially important and should be extensive for missionary routes and major movements.
- Epistles: generally no chapter map unless historical route/context is genuinely useful.
- Revelation: symbolic geography must not be falsely presented as a literal travel map.

### Shared maps

A historical unit may share one map across several chapters. Reuse is correct when the geography is genuinely the same. Do not manufacture 66 different maps merely to create visual variety.

### Map data and renderer

- Maps use ONE's canonical map schema and common renderer.
- Do not create book-specific map renderers unless the shared renderer truly cannot represent the content.
- `map` is independent from `illustration`.
- A map never substitutes for a chapter cover.
- A cover never suppresses the map.
- Keep source, title, reference, guide, places and route notes explicit.
- Prefer approved stable sources and locally controlled assets where practical.
- If using an external historical map image, verify the exact map ID/URL before release.

## 10. Canonical Biblical Chronology / 時光卷軸 rules

The ONE time scroll is a **context device**, not decorative filler.

### Purpose

It answers: **Where is this chapter in biblical history, and what major events surround it?**

### When to use

Every completed chapter should have a chronology context, but its density varies by genre:

- Narrative/history books: concrete historical events and movement.
- Prophets: anchor the chapter to kings, empires, exile, return and prophetic ministry periods.
- Psalms: use known superscription/historical setting when reliable; otherwise place within the Psalter/book context rather than inventing a precise date.
- Wisdom books: use broad canonical/historical placement when exact dating is uncertain.
- Gospels/Acts: use ministry sequence and major events.
- Epistles: use ministry/mission/church context when historically supportable.
- Revelation: use canonical/apocalyptic context without pretending symbolic visions are ordinary calendar events.

### Accuracy rule

Never create false precision. If the date is disputed or unknown, use a broad period or relative sequence instead of an invented year.

### Shared timeline language

All books use the same visual time-scroll component, typography, horizontal scrolling behavior and event hierarchy. Do not redesign the timeline per book.

### Event selection

Include only events that help orient the chapter. Prefer a small number of meaningful milestones over a crowded list.

The current chapter/event must be visually identifiable as the focus.

### Historical and canonical distinction

When a timeline event is theological/canonical rather than strictly datable, label it appropriately. Do not mix literary sequence and historical date as though they were identical.

## 11. Canonical chapter content order

ONE chapter pages should preserve a predictable study rhythm across all books. The exact presence of optional modules may vary, but the relative architecture should remain stable.

Canonical order:

1. Cover / chapter identity
2. Map — only when materially useful
3. Biblical Chronology / 時光卷軸
4. Scripture
5. 本章故事 / chapter narrative or argument
6. Story route / structure
7. Background
8. Observation
9. Cross references
10. Comparison / harmony when applicable
11. Questions
12. Preparation
13. Previous / next chapter turn

Do not arbitrarily reorder modules book-by-book.

If a module is genuinely inapplicable, omit it cleanly rather than filling it with meaningless content.

## 12. Scripture rules

The Scripture area is sacred source content and must never be confused with editorial explanation.

- Chinese and English Scripture keep their established sources/versions.
- Scripture text, references and source links must be visually distinct from commentary.
- Editorial notes such as instructions, summaries or explanations must never appear in a position styled as Scripture.
- If embedded Scripture fails, provide a working official source link; do not replace Scripture with explanatory text.
- Chapter data must not satisfy a 'Scripture slot' with non-Scripture prose.

## 13. Cross-reference rules

Cross references use one common hierarchy across 66 books:

- reference = metadata;
- theme/relationship = editorial label;
- Scripture quotation = Scripture styling;
- explanation/note = commentary styling.

Never present an editorial sentence as though it were Scripture.

Cross references should quote or link the actual referenced Scripture when the design promises Scripture content.

## 14. Comparison / harmony rules

Use comparison tables only when the genre benefits:

- Gospel harmony: appropriate and important.
- Samuel/Kings/Chronicles parallels: useful where genuine.
- Prophetic or epistle comparison: only when it adds real interpretive value.

Do not force a generic comparison table into every book.

The common renderer and typography should remain shared.

## 15. Navigation and book-entry rules

Book entry behavior is part of the ONE system and must not be modified casually while editing content modules.

- A registered/ready book must remain clickable from the 66-book interface and its cover/frontispiece.
- Chapter availability is determined by valid chapter study data, not by whether an illustration exists.
- Missing optional illustration/map data must never block book registration.
- Registry completeness must validate essential study content only; it must not require fake images or fake maps.
- A content patch must never silently alter book-selection, group-selection or chapter-entry behavior.

## 16. Data registration and load-order rules

This is a critical technical rule.

Book supplements that execute **before a book registry** must write into that book's source object (for example `ONE_DATA.psalms`, `ONE_DATA.isaiah`). They must not assume `ONE_DATA.studyBooks[n]` already exists.

The registry is responsible for exposing the completed source object to `studyBooks`.

After registration, common renderers read from the registered book.

Do not change this pattern book-by-book.

When fixing a bug, first inspect the load order and reuse the previously working pattern before inventing a new data path.

## 17. Asset rules

- Store approved reusable ONE UI assets locally in the repository.
- Avoid canonical UI dependence on remote hotlinks.
- Historical source images may retain source attribution, but production behavior should not depend on unstable redirects if a local approved copy is legally/practically appropriate.
- The approved antique textures are retained as ONE library assets for title pages, dividers, empty/loading states, resource cards and editorial interstitials.
- A chapter illustration must be explicitly associated with its own chapter.
- **Every approved generated chapter illustration must be stored/referenced as a fixed canonical asset and reused exactly; it must not be regenerated on demand.**
- Replacing a generated illustration requires explicit editorial revision, not automatic variation.
- Missing data must not inherit stale assets from a previous book/chapter.
- Keep `illustration`, `map`, `timeline`, `scripture`, `connections` and study fields semantically separate.

## 18. Responsive and interaction rules

Desktop and mobile are the same ONE experience, not separate designs.

- Preserve cover identity and hierarchy on both.
- Never allow mobile to show only the left half of a chapter/frontispiece.
- Fixed aspect-ratio media must scale without distortion.
- Horizontal time-scroll/map content may scroll where appropriate but must remain usable by touch.
- Drag/scroll interactions should be smooth and must not become noticeably heavier after visual scaling.
- Links/buttons that visually appear interactive must actually work.
- Respect reduced-motion preferences.

## 19. Typography, naming and visible terminology

- Use the established ONE Chinese/English typography system across books.
- Do not expose internal implementation terms (`vol`, fallback, generated, registry, etc.) in reader-facing UI.
- Book naming and numbering follow the established format, e.g. `01 創世紀` where that template is used.
- Do not introduce arbitrary colors such as deep blue book names when the ONE system calls for First Light gold.
- Reader-facing labels must describe content, not developer state.

## 20. Resources / Dawn Library rules

Resources are supplementary and must not interrupt the chapter's canonical reading sequence.

- Core Bible-study resources remain in the shared resource system.
- Resource cards must be clickable if presented as links.
- Dawn Library remains the curated resource destination.
- Book-specific resources may be added, but should use the common resource-card system rather than inventing new visual cards per book.

## 21. No-image fallback policy is retired

The antique texture backgrounds created during development are retained as reusable ONE library assets, but **a plain texture is no longer the normal final substitute for a missing chapter illustration**.

For finished chapter covers:

- verified suitable illustration → use it;
- otherwise → generate a chapter-specific illustration in the canonical ONE style **once**, save it as the chapter's fixed asset, and reuse it thereafter.

Antique textures remain valid where illustration is intentionally not the content.

## 22. Cross-book application

This standard applies retroactively and prospectively to every ONE book, including:

Pentateuch; Joshua; Judges; Ruth; Samuel; Kings; Chronicles; Ezra–Esther; Job; Psalms; Proverbs; Ecclesiastes; Song of Songs; Isaiah; Jeremiah; Lamentations; Ezekiel; Daniel; the Twelve Minor Prophets; the Gospels; Acts; Pauline epistles; Hebrews; James; 1–2 Peter; 1–3 John; Jude; Revelation.

Do not begin a new design-system exploration when a new book is produced. Start from this standard.

## 23. Regression-first debugging rule

When something that previously worked breaks:

1. Check whether the earlier version worked.
2. Inspect the earlier working implementation.
3. Restore/reuse the proven pattern before introducing a new architecture.
4. Avoid repeated experimental rewrites of stable shared systems.

A local content issue must not trigger unnecessary changes to global navigation, registry, renderer or interaction logic.

## 24. Quality-control checklist

Before a book/change is considered complete, verify at minimum:

- book can be entered from the ONE cover/66-book interface;
- chapter can be selected and entered;
- cover image belongs to the correct chapter;
- no unrelated or stale image is inherited;
- historical image, if used, is genuinely relevant;
- generated image, if used, reflects the actual chapter;
- generated image is the fixed approved chapter asset and is not being regenerated automatically;
- historical and generated covers belong to the same ONE family;
- canonical ornate gold frame is present;
- brand gold is consistent;
- Morning Star is used only where appropriate;
- map appears where geography materially helps and is absent where unnecessary;
- map data uses the shared renderer/schema;
- chronology is meaningful and does not invent false precision;
- Scripture slot contains Scripture/source links, not editorial prose;
- cross-reference Scripture and commentary are visually distinct;
- optional modules do not block book registration;
- no production/debug wording is visible;
- previous/next chapter navigation works;
- desktop and mobile preserve the same identity and functionality;
- no change has accidentally broken another completed book.

For shared-system changes, test representative genres rather than one book only: at least one Pentateuch/history book, Psalms/wisdom, a prophet, a Gospel, an epistle, and—once available—Acts/Revelation.

## 25. Change control

**This is a locked project-level rule.**

Future implementation work should solve technical problems by returning to this standard and to previously working ONE patterns—not by inventing a new visual or data system.

If a future change appears to require a different art direction, frame, palette, Morning Star, map philosophy, timeline philosophy, chapter order, registry model, interaction pattern or fallback philosophy, stop and treat that as a proposed change to the entire ONE design system. Do not silently change one book.
