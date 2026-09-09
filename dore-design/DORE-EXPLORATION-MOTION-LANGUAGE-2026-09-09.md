# Doré Exploration — Motion Language for New Westside

Date: 2026-09-09
Status: EXPLORATION RECORD — NOT YET ARCHITECTURE

## Research question

New Westside has already accepted that the site should feel alive. The open problem is no longer whether it moves, but:

> **how it moves, what moves, who controls the movement, at what speed, and what editorial meaning that movement produces.**

The key correction is to treat this as a **Motion Language**, not a collection of animation effects.

## Core hypothesis

Motion should be semantic.

Different editorial currents may inhabit the same spatial architecture while carrying different temporal identities:

- fast current = breaking / rolling news / 三更報導 / live developments;
- medium current = current issue / editorial browsing / features;
- slow current = theology / reflection / prayer / long-form visual essay;
- near-still current = archive / sacred pause / text-led reading / memorial or contemplative content;
- cinematic current = Scripture Cinema / major feature opening / designed narrative sequence.

The metaphor of living water is therefore expressed through **different flow rates**, not literal water graphics.

> **Same river, different current speeds.**

## Mature precedents and transferable principles

### 1. MERSI — motion as one coherent physical vocabulary

The MERSI 2026 case study is especially mature because its movement is not decorative. The project cover is a transitional object; it flips and becomes the next space. Project layouts progressively reposition from a freer composition into an ordered grid. Horizontal project reading continues the same editorial/architectural language.

Its implementation also shows a useful division of labor:

- GSAP / Flip / ScrollTrigger for deliberate high-value transitions;
- Lenis for scroll coordination;
- Taxi.js for page transitions;
- Splide only for a specific news slider;
- everything else custom vanilla JS.

Transferable rule:

> **Use a small number of recurring physical verbs — open, flip, expand, align, flow, return — instead of many unrelated effects.**

Source: https://tympanus.net/codrops/2026/07/27/between-print-and-digital-the-making-of-mersis-website/

### 2. MacGuffin — motion direction carries information meaning

MacGuffin deliberately assigns horizontal movement to magazine/article navigation and vertical movement to practical/informational content. This is important because axis direction is not an effect but part of information architecture.

Transferable rule:

> **Every direction of movement should have a stable semantic role.**

Source: https://www.itsnicethat.com/articles/double-click-may-2022-online-magazine-digital-310522

### 3. More or Less — scale change creates tempo

The More or Less digital magazine uses very large photography, tiny-to-huge scale changes, and viewport-relative sizing to create a dynamic reading rhythm. The key lesson is that motion sensation can come from **scale rhythm and composition**, not constant animation.

Transferable rule:

> **Temporal energy can be produced by changes in scale, density, crop and spacing even when an object is not continuously moving.**

This is important for quieter New Westside currents.

Source: https://www.itsnicethat.com/articles/double-click-may-2022-online-magazine-digital-310522

### 4. The Irregular Times — movement can encode editorial attitude

The Irregular Times uses movable and animated elements to express play and rebellion. It also warns that dynamic sites quickly accumulate overwhelming assets, requiring strict content and asset organization.

Transferable rule:

> **Motion personality should derive from the editorial identity of a section, but the more expressive the surface becomes, the stricter the underlying content system must be.**

Source: https://www.itsnicethat.com/articles/double-click-may-2022-online-magazine-digital-310522

### 5. Noon — continuous navigation with no dead ends

Noon’s redesign was conceived as a fluid archive where visitors can continue from images to words and sidestep into contributors without reaching dead ends. Its visual system is intentionally restrained so that ambitious navigation remains understandable.

Transferable rule:

> **Continuous motion must preserve continuous orientation. Fluidity without navigational continuity becomes confusion.**

Source: https://www.itsnicethat.com/articles/double-click-july-digital-160719

### 6. SFMOMA — clarity first, motion second

SFMOMA’s digital-publication framework combines immersive cover imagery, scrolling, in-page navigation and publication-specific color identity. The key lesson for motion is that immersive visual identity remains anchored by explicit table-of-contents / in-page navigation.

Transferable rule:

> **The site may move continuously, but the reader’s current location and available next actions must remain visually explicit.**

Source: https://mw18.mwconf.org/paper/the-next-generation-of-digital-publishing-integrated-strategies-for-online-scholarly-content-at-sfmoma/index.html

### 7. Codrops preview-to-content patterns — object continuity

Magazine/blog transition experiments show a recurring pattern in which a preview object grows, moves or reveals into the full article rather than disappearing into a hard page cut.

Transferable rule:

> **When an 8:5 is selected, preserve object identity through the transition so the visitor feels they entered the object rather than left the homepage.**

Sources:
- https://tympanus.net/codrops/2021/04/07/preview-to-full-content-page-transition/
- https://tympanus.net/codrops/2022/07/06/how-to-create-a-cover-page-transition/

## Candidate New Westside Motion Grammar

This is a hypothesis for Storybook testing, not production authorization.

### Motion property 1 — speed

Each editorial current receives a constrained speed class rather than arbitrary animation duration:

- `urgent` — fast, news/live current;
- `active` — medium, contemporary editorial/current issue;
- `measured` — slow, feature/interview/essay;
- `contemplative` — very slow, theology/prayer/archive;
- `still` — no autonomous movement;
- `cinematic` — scene-based timing rather than constant velocity.

The exact numerical speeds should be derived through prototypes and perception testing rather than assigned now.

### Motion property 2 — agency

Every moving object must declare who controls it:

- `system-led` — autonomous but interruptible;
- `scroll-led` — movement follows visitor scroll;
- `gesture-led` — drag/swipe;
- `sequence-led` — art-directed timeline;
- `still-until-focus` — motion begins only on focus/hover/entry.

Autoplay should never eliminate user agency.

### Motion property 3 — continuity

An 8:5 object can behave as:

- independent cover;
- visually linked neighbor;
- seamless strip segment;
- transitional object into deeper content.

Not every row should loop infinitely. Infinity is a narrative choice, not a default.

### Motion property 4 — attention

Only a small number of currents should command attention at the same time.

Candidate law:

> **the whole website may be alive, but only one foreground motion should dominate a viewport at a time.**

Nearby currents may drift slowly, pause, or reduce contrast while the active field becomes dominant.

### Motion property 5 — pause

Pause is part of the language, not a failure of animation.

Use pause for:

- long-form reading;
- theological weight;
- prayer;
- key Scripture moment;
- image inspection;
- transition from breaking news to developed analysis.

### Motion property 6 — acceleration / deceleration

Editorial meaning can be encoded through temporal change:

- breaking news can enter quickly then settle;
- a major feature can slowly gather visual weight;
- Scripture Cinema can move through broad narrative tempo changes rather than uniform speed;
- entering an article should usually decelerate into readable stillness.

## Motion map candidate

A useful Storybook matrix is:

| Content current | Default temporal character | Main agency |
| --- | --- | --- |
| Scripture Cinema | cinematic / variable | sequence + user override |
| 三更報導 / rolling news | urgent | system-led + pause/drag |
| current Journal features | active | scroll/gesture-led |
| interviews / profiles | measured | gesture-led |
| theology / Bible study | contemplative | scroll-led |
| prayer / memorial / archive | near-still | user-led |
| Dawn Library | measured / tactile | gesture-led |
| ONE deep research | still / precise | user-led |

This table is not a final IA mapping. Real current site sections must continue to be read from the repository before production naming.

## Storybook experiments required

### Motion Prototype M1 — same geometry, six speeds

Use one identical 8:5 strip with six constrained temporal characters. Test whether speed alone communicates editorial tone or becomes gimmicky.

### Motion Prototype M2 — foreground / background hierarchy

Place 4–5 moving currents in one vertical viewport sequence. At any moment allow only one dominant current; others drift or pause. Test whether the page feels alive without becoming visually noisy.

### Motion Prototype M3 — fast news current

Prototype 三更報導 / rolling news as a genuinely faster current with large cover objects, timestamps and developing-story states. Verify that it feels editorial rather than ticker-like.

### Motion Prototype M4 — slow theology current

Use nearly still 8:5 covers with long visual dwell times and very restrained transitions. Test whether stillness reads as intentional weight rather than broken animation.

### Motion Prototype M5 — cover-to-world recursion

Homepage 8:5 -> enter -> new opening 8:5 -> lower related wall. Preserve the selected object across the transition. Test whether repeated recursion remains understandable after two or three levels.

### Motion Prototype M6 — reduced motion

Every semantic movement must have a non-autonomous equivalent that preserves order, identity and access. Reduced-motion cannot be a separate content architecture.

## Failure modes to reject

- every row moving at the same speed;
- every row moving continuously;
- Netflix-like autoplay carousels;
- ticker behavior for serious editorial content;
- visual motion with no semantic relation to content;
- full-viewport movement that destroys reading focus;
- animation that hides navigation state;
- page transitions that make users wait;
- animation engine becoming the content model;
- literal water effects used as substitute for the Living Water idea.

## Current synthesis

The strongest new candidate statement is:

> **New Westside is not a website with animations. It is a publication whose content has temporal behavior.**

The design language should therefore describe content in both spatial and temporal terms:

`where it lives + how it looks + how it moves + who controls it + how it becomes still + how it opens into the next space`.

The Living Water idea becomes credible when different content behaves like different currents while remaining part of one navigable world.

## Engineering boundary

Do not install a motion stack or freeze numerical speeds from this record.

Correct path:

`Doré Exploration -> Storybook motion prototypes -> human critique -> motion vocabulary -> Design constraints/tokens -> promotion gate -> production`

The Doré learning object for this round is:

`site should move -> motion is not one effect -> editorial identity implies temporal identity -> constrained motion grammar -> prototypes -> critique -> retained capability`
