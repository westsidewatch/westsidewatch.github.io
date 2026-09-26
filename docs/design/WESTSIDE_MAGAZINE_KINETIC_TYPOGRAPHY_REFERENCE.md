# Westside Magazine — Kinetic Typography / Spatial Editorial Reference Memo

Status: reference memo for future Westside Watch magazine design. Not a production implementation and not a new parallel design system.

## Why this memo exists

The Fond / 池底 `01020304` experiment exposed a useful design direction for the future Westside Watch magazine: typography can become the spatial and interactive structure of a publication instead of being placed inside conventional cards, panels, or simulated physical books.

The important distinction is:

- typography itself can behave as page, hinge, foreground, background, transition, and navigation;
- the static composition must already be aesthetically complete;
- motion should reveal an existing spatial logic rather than compensate for weak layout;
- avoid literal book mockups, paper thickness, page curls, generic 3D objects, and generator-style decorative effects;
- visual complexity should decrease as design maturity increases: fewer elements, richer relationships.

## Open-source references worth retaining

### 1. Codrops — Kinetic Typography Page Transition

Repository:
https://github.com/codrops/KineticTypePageTransition

Primary relevance:

- oversized typography becomes the spatial field;
- type moves between background and foreground;
- interaction can transform typography into the transition toward the next content state;
- closest structural reference to the idea that a publication index can itself become a moving typographic object.

Potential Westside use:

A magazine issue / section / article index does not need conventional cards. Large editorial typography can form the page composition, then become the transition into the selected story.

### 2. Codrops — Superfluid Layout

Repository:
https://github.com/codrops/SuperfluidLayout

Primary relevance:

- typography and layout participate in reveal behavior;
- useful reference for breaking rigid rectangular page logic without adding ornamental objects;
- supports the principle that the graphic composition itself can carry interaction.

Potential Westside use:

Issue openers, section transitions, feature packages, and editorial sequences where type and imagery reorganize while retaining a coherent magazine grammar.

### 3. Codrops — Fullscreen Layout Page Transitions

Repository:
https://github.com/codrops/FullscreenLayoutPageTransitions

Primary relevance:

- one selected element can expand into the dominant/fullscreen state;
- surrounding elements can recede rather than simply disappear;
- useful spatial hierarchy for multiple editorial entrances sharing one field.

Potential Westside use:

Several stories can coexist as one composition; hover/focus establishes depth, and selection lets one story occupy the publication field and become the article.

### 4. Codrops — PageTransitions

Repository:
https://github.com/codrops/PageTransitions

Primary relevance:

- mature CSS page-transition mechanics;
- useful as a motion/transition reference library rather than as a visual template.

Potential Westside use:

Borrow proven spatial transition mechanics while keeping Westside's own typography, editorial hierarchy, material language, and Doré-derived grammar.

## What NOT to use as the primary model

Conventional PageFlip / 3D Flipbook libraries are not the preferred foundation for Westside's magazine interface.

Reason:

They usually simulate a physical book through page thickness, shadows, curls, perspective, and literal paper. Westside should instead allow typography, image, negative space, and editorial hierarchy to become the publication's spatial structure.

A physical page-turn effect may still be useful in a narrowly justified context, but it should not define the magazine grammar.

## Design principle extracted from the Fond experiment

The useful model is not:

`content -> card -> hover effect -> page`

It is:

`editorial composition -> latent spatial structure -> interaction reveals depth -> selected element becomes next editorial state`

For typography-led work:

`type composition -> type as hinge/plane/space -> hover reveals spatial relation -> click becomes transition -> article/issue opens`

## Relationship to Italian Editorial Atlas / Doré

These open-source references provide interaction and implementation evidence, not historical or visual authority.

The visual/editorial grammar should continue to come from the canonical Doré / Italian Editorial Atlas research and Westside's own established design language. Open-source code supplies mature mechanics that can translate those grammars into web behavior.

Therefore:

- Italian Editorial Atlas / Doré = editorial and visual grammar authority;
- open-source references = interaction / spatial implementation references;
- Westside = final synthesis and publication identity.

Do not copy Codrops demo styling as the Westside visual identity.

## Future implementation direction

When Westside magazine design returns to this problem, begin by testing a synthesis roughly equivalent to:

`KineticTypePageTransition mechanics + Westside editorial typography + Doré canonical grammar + fullscreen story transition`

Acceptance criteria:

1. Static screenshot is already a complete editorial composition.
2. Typography and imagery have clear hierarchy, breathing space, scale contrast, and mutual response.
3. Interaction reveals depth already implied by the composition.
4. No generic cards unless editorially necessary.
5. No gratuitous 3D.
6. No literal flipbook imitation as the default grammar.
7. Motion serves reading and editorial sequence.
8. The system can continue growing with future issues and sections without redesigning the underlying grammar.

## Origin

Captured from the Fond / 池底 `01020304` spatial typography exploration, September 2026, specifically to preserve the useful findings for future Westside Watch magazine design rather than forcing the current Fond experiment to carry all of them.