# ONE — Canonical Visual Standard

Status: **LOCKED / CANONICAL**

This document is the permanent visual and illustration standard for **all 66 books and all chapters in ONE**. New books and future revisions MUST follow this standard. Do not restart visual exploration book-by-book and do not introduce a new illustration language without an explicit project-wide decision to revise this document.

## 1. Core principle

ONE is one visual system, not 66 independently designed books.

Every chapter cover must belong to the same family: **classical engraved biblical imagery + dark antique book texture + Westside Watch brand gold + ornate antique frame + restrained typography**.

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

## 9. Maps are independent from covers

A chapter map and a chapter cover illustration are different content types.

- A map must never be used as a substitute for a cover illustration.
- A cover illustration must never suppress a chapter map.
- Geography-heavy books/chapters should show maps in the established chapter study/map renderer when useful.
- Books that do not materially benefit from maps do not need maps merely for symmetry.

Examples: Isaiah requires contextual maps in relevant sections; Psalms generally does not; Acts will require especially strong map support.

## 10. No-image fallback policy is retired

The antique texture backgrounds created during development are retained as reusable ONE library assets, but **a plain texture is no longer the normal final substitute for a missing chapter illustration**.

For chapter covers:

- verified suitable illustration → use it;
- otherwise → generate a chapter-specific illustration in the canonical ONE style.

The antique textures may still be used for title pages, section dividers, loading/empty states, editorial pages, resource cards, interstitials or other places where an illustration is intentionally not required.

## 11. Asset and data rules

- Store approved reusable visual assets locally in the repository; do not depend on remote hotlinks for canonical UI assets.
- A chapter illustration must be explicitly associated with its own chapter.
- Missing data must not inherit a stale image from a previous chapter/book.
- Illustration data is optional during authoring, but a finished book should follow the source hierarchy above and receive a proper chapter cover treatment.
- Do not require fake/recycled illustrations merely to satisfy a registry completeness check.
- Keep illustration, map and study data as separate semantic fields.

## 12. Cross-book application

This standard applies retroactively and prospectively to every ONE book, including but not limited to:

Pentateuch; Joshua; Judges; Ruth; Samuel; Kings; Chronicles; Ezra–Esther; Job; Psalms; Proverbs; Ecclesiastes; Song of Songs; Isaiah; Jeremiah; Lamentations; Ezekiel; Daniel; the Twelve Minor Prophets; the Gospels; Acts; Pauline epistles; Hebrews; James; 1–2 Peter; 1–3 John; Jude; Revelation.

Do not begin a new visual exploration when a new book is produced. Start from this standard.

## 13. Quality-control checklist

Before a book/cover change is considered complete, verify:

- chapter can actually be entered from the book interface;
- cover image belongs to the correct chapter;
- no unrelated or stale image is inherited;
- historical image, if used, is genuinely relevant;
- generated image, if used, reflects the actual chapter;
- historical and generated covers visibly belong to the same ONE family;
- canonical ornate gold frame is present;
- brand gold is consistent;
- Morning Star is used only where compositionally appropriate;
- no production/debug wording is visible;
- map, when required, renders independently in the chapter content;
- desktop and mobile preserve the same cover identity.

## 14. Change control

**This is a locked project-level rule.**

Future implementation work should solve technical problems by returning to this standard and to previously working ONE patterns—not by inventing a new visual system.

If a future change appears to require a different art direction, frame, palette, Morning Star, illustration philosophy or fallback philosophy, stop and treat that as a proposed change to the entire ONE design system. Do not silently change one book.
