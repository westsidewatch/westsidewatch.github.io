# Doré Exploration — Living Scripture River

Date: 2026-09-09
Status: EXPLORATION RECORD — NOT YET ARCHITECTURE

## Why this record exists

This record preserves the current New Westside layout idea before engineering. It is an evolution of the earlier **5:8 vinyl wall**, not an unrelated replacement concept.

The governing phrase is:

> **New Westside is a living river. The river is Scripture.**

The current arrangement is the first concrete spatial model of that idea.

## Evolution from the vinyl wall

The earlier New Westside visual system used upright `5:8` publication objects.

The new move is not to discard them, but to rotate and transform the same visual unit:

`5:8 publication object -> 8:5 Scripture frame`

The decisive change is that `8:5` has two simultaneous identities:

1. **separate:** an independent, clickable scene / article / topic / curation object;
2. **connected:** one frame in a continuous Scripture animation.

Therefore:

`8:5 × N = Bible film / living Scripture current`

The old vinyl wall found the form. The new work gives it a true indexing system: **Scripture itself**.

## Homepage arrangement — current hypothesis

### 1. Largest 8:5 = Bible cinema

The first screen is one very large `8:5` field. It is not a conventional hero block. It is a cinema screen through which the Bible is continuously moving horizontally.

The animation is not required to start from Genesis every time. A visitor may enter the river at a different point on each visit. The Scripture world is understood as already moving before the visitor arrives.

A deliberate `watch from the beginning` mode may allow the visitor to watch the full sequence from Genesis through Revelation, effectively watching a complete Bible film. The website itself is the film; this is not a separate video asset.

### 2. Below the cinema = many horizontal 8:5 currents

Scrolling downward does not mean leaving Scripture.

Below the large cinema, many rows of `8:5` objects extend horizontally. Together they form the evolved vinyl wall and continue vertically down the page.

Each row may correspond to an actual New Westside editorial section, theme, curation, person/place stream, Scripture relation, or another verified part of the real site architecture. **Do not invent or restore obsolete sections from conversational memory; the current repository/site framework is authoritative.**

Each row is horizontally animated, while the page itself extends vertically. The visitor can therefore move through the same Scripture world in both axes.

### 3. Every 8:5 remains individually enterable

Every `8:5` is both part of the continuous animation and an interactive portal. Selecting one can enter the corresponding structured content: article, topic, event, person, place, book/chapter, ONE research layer, or another valid destination.

The important product behavior is:

> **connected = watch Scripture; separated = enter Scripture.**

### 4. Horizontal and vertical motion are one system

Horizontal motion expresses the continuity / time / movement of Scripture.

Vertical motion exposes additional curated views of the same Scripture world.

The page should therefore not feel like `hero + rows of carousels`. It should feel like one living field in which the visitor remains inside Scripture while moving both horizontally and vertically.

### 5. The 8:5 frame is the atomic visual grammar

The `8:5` object is no longer merely a card ratio. It can function as:

- cinematic frame;
- Scripture scene;
- editorial object;
- clickable portal;
- unit of montage;
- unit of continuous composition;
- unit of responsive re-editing.

Adjacent frames may visually connect through horizon lines, architecture, roads, water, engraved darkness, light, paper fields, figures, or engraving density so that the sequence reads as one work rather than as independent thumbnails.

## Design problem now being explored

The technical problem is not simply `how to make horizontal scrolling`.

The real problem is:

> **How can many individually clickable 8:5 objects form multiple horizontally animated rows and a vertically extending site while still reading as one continuous Bible film / living Scripture river rather than as a Netflix-like collection of carousels?**

This requires simultaneous exploration of:

- continuous composition and visual continuity;
- multi-row horizontal motion;
- different row velocities / directions / phase positions;
- a large hero/current that can start at a non-fixed Scripture position;
- full-sequence watch mode;
- click/tap interruption and reliable return to prior position;
- responsive/mobile re-editing;
- reduced-motion and accessibility behavior;
- lazy rendering / virtualization for a potentially large number of 8:5 scenes;
- preservation of Scripture indexing and editorial semantics beneath the animation.

## Doré Exploration Round 01 — comparable design precedents

### A. Existing corpus cases that now become more relevant

Several already-recorded award-calibre references now map more directly to this layout thesis:

- **Bascule** — continuous long-page experience where the scrolling field itself becomes the work; useful for thinking beyond conventional sections.
- **Farawayfarers** — endless horizontal travel with crosslinks and deeper reading; especially relevant to continuous field + individually enterable objects.
- **Microdot** — interface mechanics are derived from the subject's own physical/media grammar rather than imposed as generic animation; reinforces `Doré engraving physics -> motion grammar -> implementation`.
- **We Choose the Moon** — canonical chronology becomes the information architecture; relevant to Scripture as the actual indexing system.
- **Museum of the World** — historical/semantic relationships become spatial navigation; relevant to secondary Scripture/topic/person/place currents.
- **The Boat** — illustration becomes narrative space rather than illustration inside a page.

These are not templates to copy. They validate pieces of the problem.

### B. New comparable references found in this round

#### CANALS

Communication Arts presents **CANALS** as a horizontally scrolling, magazine-like editorial experience about the history of Amsterdam's canals. It is useful because history, editorial art direction and horizontal movement are integrated rather than treated as a gallery effect.

Transferable question for New Westside: can each 8:5 current behave like an editorial spread sequence while still belonging to a larger historical river?

Source: https://www.commarts.com/webpicks/canals

#### Refuseniks & Activists

Awwwards documents a dark archival experience that uses horizontally scrolling historical photographs/documents to narrate a large Cold War migration story. It is relevant to New Westside because archive objects remain individually legible while belonging to a larger historical narrative field.

Transferable question: how can documentary/Scripture objects remain semantically clickable without breaking the sensation of continuous historical movement?

Source: https://www.awwwards.com/inspiration/horizontal-scroll-gallery-refuseniks-activists

### C. Current precedent conclusion

No single reference found so far exactly matches the proposed New Westside system:

`one giant continuously moving 8:5 Bible cinema + many vertically stacked horizontal 8:5 currents + every frame independently enterable + all rows remaining Scripture rather than generic media`.

Therefore this is **not yet a solved-template problem**, but many of its constituent mechanisms are mature.

The next search should continue until either:

1. a genuinely close precedent appears; or
2. evidence becomes strong that New Westside is combining mature mechanisms into a relatively original spatial system.

## Doré Exploration Round 01 — mature implementation mechanisms

### 1. Lenis — strong candidate for the global scroll layer

Lenis is a mature MIT-licensed smooth-scroll library. Its current project explicitly supports native-scroll-based smoothing, vertical/horizontal/nested axes, WebGL/GSAP synchronization, snapping, infinite scrolling, and `prefers-reduced-motion` handling.

Why it fits:

- one scroll model can coordinate the site's vertical river with horizontal/nested currents;
- lightweight and dependency-free aligns with Doré's `more capability, less burden` principle;
- it preserves native scroll semantics rather than replacing the page with an opaque canvas;
- it can be used only where required rather than becoming the content architecture.

It should be tested, not automatically adopted.

Sources:
- https://github.com/darkroomengineering/lenis
- https://github.com/darkroomengineering/lenis#features

### 2. Embla Carousel — strong candidate for independently enterable 8:5 rows

Embla is an MIT-licensed, dependency-free, framework-agnostic carousel engine designed for fluid motion and precise swiping. It has official autoplay support and loop mode.

Why it fits:

- each horizontal current can retain real DOM items and links;
- rows can be independently draggable/swipeable;
- it provides loop/autoplay mechanics without forcing a visual design;
- Doré can own the 8:5 rendering and Scripture semantics.

Important limitation: treating every current as an ordinary carousel would produce exactly the `Netflix rows` failure mode. Embla is therefore a possible **motion/gesture primitive**, not the design model.

Sources:
- https://github.com/davidjerleke/embla-carousel
- https://www.embla-carousel.com/docs/v8/api/plugins

### 3. GSAP ScrollTrigger — strong candidate for cinematic orchestration, not basic layout

ScrollTrigger remains a mature precise tool for scroll-linked timelines, pinned sequences and scrubbed animation. Lenis explicitly documents direct synchronization with ScrollTrigger.

Potential Doré use:

- hero Bible cinema scene choreography;
- match-cut / light / engraving reveal sequences between 8:5 frames;
- controlled transitions when a row becomes active;
- `watch full Bible` mode timeline control.

Do not use GSAP to solve things CSS/layout can already solve. Its role should be high-value cinematic orchestration.

Source: https://gsap.com/docs/v3/Plugins/ScrollTrigger/

### 4. Native CSS Scroll-Driven Animations — strong lightweight baseline

Modern CSS now supports scroll-driven animation timelines, allowing CSS animation progress to be linked directly to scroll progress.

This should be the default comparison baseline before adding JavaScript animation code for simple opacity, transform, reveal and position relationships.

Why it matters to Doré:

> `if CSS can express it deterministically, do not make a runtime animation system guess or carry extra burden.`

Source: https://developer.mozilla.org/en-US/docs/Web/CSS/Guides/Scroll-driven_animations

### 5. IntersectionObserver — viewport activation / lazy river primitive

The browser's Intersection Observer API provides asynchronous visibility/intersection observation without requiring continuous manual geometry polling.

Potential uses:

- start/pause row animation when near viewport;
- lazy-load Doré images;
- hydrate only active currents;
- record which Scripture/current is actually visible;
- reduce CPU/GPU burden deep down a long vertical page.

Source: https://developer.mozilla.org/en-US/docs/Web/API/Intersection_Observer_API

### 6. Swiper / Motion — comparison candidates, not current preference

Swiper is a mature feature-rich slider/carousel system with loop/autoplay/free-mode capabilities. Motion provides declarative scroll-linked animation primitives for React.

They should remain comparison candidates. At present, Embla's smaller headless model appears more aligned with Doré's `own the visual grammar, borrow only the motion primitive` principle, while New Westside is currently Hugo rather than a React-native site.

Sources:
- https://swiperjs.com/swiper-api
- https://motion.dev/docs/react-use-scroll

## Candidate implementation algorithm — not yet engineering authorization

A lightweight architecture worth prototyping is emerging:

1. **Scripture index** assigns every 8:5 item stable semantic coordinates.
2. **Row curator** groups items into verified New Westside rows/themes/sections without changing the Scripture identity of each item.
3. **Phase function** assigns each row an initial horizontal offset; the hero can also enter at a non-fixed Scripture position.
4. **Velocity field** gives rows restrained, intentionally different speeds/directions rather than identical carousel autoplay.
5. **Loop window** repeats/recycles the visible sequence seamlessly when a row is designed as continuous.
6. **Viewport activation** uses IntersectionObserver so only nearby currents animate/hydrate.
7. **Frame renderer** keeps each 8:5 as a normal semantic/linkable DOM object.
8. **Cinematic layer** uses CSS scroll timelines first, then GSAP only for transitions that require art-directed sequencing.
9. **State preservation** records the visitor's Scripture position/current/row before entering an item and returns them to that visual location.
10. **Reduced-motion mode** converts automatic currents to stable manually scrollable rows and keeps every destination reachable.

Conceptually:

`Scripture data -> curator/index -> 8:5 semantic frames -> horizontal current engine -> vertical river orchestrator -> cinematic transition layer`

The animation engine must not become the source of truth. Scripture/editorial data remains the source of truth.

## Template / pattern exploration

The first round did **not** find a mature drop-in template that should be installed unchanged. That is a useful result.

The strongest mature pattern is instead compositional:

- normal semantic DOM content;
- headless horizontal row engine;
- native vertical document flow;
- optional smooth-scroll coordinator;
- scroll-linked animation layer;
- viewport-aware activation;
- WebGL only for specific image/material effects that cannot be achieved cheaply otherwise.

This is more compatible with Doré than importing a large award-site starter template, because the New Westside requirement is structurally unusual and must remain attached to real Scripture/editorial semantics.

## Immediate Storybook prototype candidates

Exploration is not yet authorizing production replacement. The smallest useful Storybook experiments would be:

### Prototype A — one continuous 8:5 Scripture current

Test 12–20 placeholder Scripture frames as one seamless composition. Validate continuous visual connection, independent clickability, keyboard/touch behavior and return-to-position.

### Prototype B — giant cinema + three independent currents

One large 8:5 hero/current plus three horizontal rows below it. Test different phase offsets and velocities while preserving a single visual world.

### Prototype C — vertical travel through moving Scripture

Five or six rows vertically stacked. Only rows near the viewport animate. Test whether downward scrolling still feels like watching Scripture rather than browsing a media catalogue.

### Prototype D — reduced-motion/mobile transformation

Transform the same structured data into a stable touch-first/mobile experience without maintaining a second content architecture.

No prototype is successful merely because it moves. The acceptance question is whether the whole field reads as **one living Scripture river**.

## Engineering boundary

This record does not authorize replacing the homepage or installing Lenis, Embla, GSAP, Swiper or another dependency in production.

The correct flow remains:

`Doré Exploration -> Storybook experiment -> compare mechanisms -> human critique -> promotion gate -> Template Registry / Design -> production`

The important learning artifact to preserve is:

`old 5:8 vinyl wall -> rotation to 8:5 -> Scripture indexing -> continuous current -> multi-row vertical river -> tested implementation primitive -> critique -> retained Doré capability`

This is explicitly a case where Doré should learn from its own previous design rather than restart from a new external template.