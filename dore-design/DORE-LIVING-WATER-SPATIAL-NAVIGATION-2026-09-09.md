# DORÉ Design — Living Water Spatial Navigation

Date: 2026-09-09
Status: Design direction / current source of truth for next prototypes

## North Star
New Westside is a living editorial publication. Motion is not decoration and navigation is not a directory. Content importance, editorial identity, spatial behavior, color world, entry transition, and interior motion all participate in meaning.

The internal quality target remains Red Dot-level art direction. This is an aspirational design gate, not an award claim.

## 1. First layer: Live Weighted Editorial Field

The sketched second screen is not a conventional second-level page. It breaks IA hierarchy intentionally and surfaces what matters across the whole site *now*.

Canonical IA remains intact underneath; the live field does not invent or replace IA.

Core model:

- 8:5 is a spatial/editorial rhythm quantum, not a fixed card component.
- Importance can expand an object to 2x, 3x or more rhythm units.
- Weight controls hierarchy/prominence.
- Velocity controls attention time/dwell: lighter content can pass faster; important content can move slower and remain visible longer.
- Depth/current/lane may vary while horizontal baselines and reading order remain clear.
- One viewport should still communicate primary -> secondary -> ordinary content immediately.
- The field continuously recomposes; this is not Masonry/Pinterest and not cards drifting inside a fixed grid.
- A high-weight object can become the current visual main sentence; later another object can inherit that role.

Editorial recommendation is expressed spatially. The best/current recommendation should already be visible and alive on the main field; the best experience is not withheld until a click.

Working abstraction:

`ContentWeight -> span + velocity + prominence + dwell + depth`

with art-direction overrides rather than a mechanical one-to-one formula.

## 2. Shared world, differentiated worlds

The site keeps a common Living Water brand grammar while allowing each section its own:

- color world / editorial palette
- entry verb
- interior motion identity
- density and spatial rhythm
- image treatment
- typography behavior

Different section palettes remain desirable. The goal is not simple theme swapping but full Editorial Color Identity: foreground, surface, depth, accent, typography, imagery and transition color behavior.

## 3. Semantic entry transitions

Navigation motion can identify content. A single universal page transition is explicitly rejected.

Current transition vocabulary to prototype and compare:

- **Gate / Submerge** — Church / Living Water: enter God's house; threshold, opening gate/door, then quiet depth.
- **Unfold / Enter City** — Dawn Library: publication cover opens and the spatial grammar changes into the library city.
- **Confluence** — Journal/editorial themes: related content gathers into a new editorial field.
- **Source** — Scripture: move upstream toward passage/chapter/source and Scripture Cinema.
- **Gather** — ONE/research: evidence, Scripture and tools assemble into a working research space.

Return is not merely browser Back. It should restore the user's river context, position, weight state and orientation whenever feasible.

## 4. Interior motion identity

Entry transition and interior motion are separate but semantically related.

### Church — Quiet House

Church content is comparatively sparse and should become cleaner, quieter, solemn and contemplative.

Candidate grammar:

`Gate -> Threshold -> Quiet House -> Hold`

The entrance may behave like a large door/gate opening because the church is God's house. Inside, use restrained MERSI-like behaviors as reference: frame, open, reposition, hold. Large quiet fields, deliberate pauses, low object density, slow movement and strong stillness are preferred. Modernity comes from precision and restraint after the spatial design has been established.

### Dawn Library — Living Editorial City

Dawn Library is dense: curated collections, cards, spectrum and editorial guidance. Its interior should not behave like Church.

Candidate grammar:

`Unfold -> 8:5 to 5:8 transformation -> Living City -> continuous street`

Inside the library, the homepage 8:5 rhythm may transform into 5:8 vertical objects. Cards can stand, overlap in depth, vary in height/weight and form walls/towers/streets. Important editorial groupings may join multiple 5:8 units into longer walls. Near/far motion can create the feeling of walking through a long inhabited city rather than browsing a card grid.

The first editorial guidance remains based on the real library structure/content; do not invent IA merely to fill the composition.

## 5. Critical click-through behavior: recommendation -> destination world

Example: a user clicks a current high-weight Dawn Library curated theme directly from the Live Weighted Editorial Field.

The destination must preserve the clicked content as the immediate subject. Do **not** send the user to a generic Dawn Library landing page that requires another click.

Required spatial sequence:

1. The selected curated theme enters Dawn Library through the library-specific transition.
2. At the top of the destination, the selected theme becomes a full-viewport immersive 8:5 opening field.
3. The selected content is immediately consumable. No second click is required.
4. Motion *inside* this immersive 8:5 is primarily horizontal, allowing the user to remain on the page in a quiet, immersive state and watch/read the selected subject through to completion.
5. The user may simply stay there and finish what they came for.
6. Only when the user scrolls downward does the broader Dawn Library reveal itself.
7. Below, the dynamic Living Editorial City / 5:8 wall provides more content and deeper navigation.
8. The user can then choose other themes, editorial levels or content without losing the sense of having entered a coherent world.

This produces two simultaneous navigation modes:

- **direct fulfillment**: the thing clicked is already open and consumable at the top;
- **spatial exploration**: scrolling downward exposes the larger world it belongs to.

This principle should generalize: a deep-linked item from the Live Weighted Editorial Field should become the opening/main sentence of its destination world rather than forcing a landing-page detour.

## 6. Spatial hierarchy model

The current conceptual topology is:

`Scripture Cinema / source opening`

`-> Live Weighted Editorial Field (cross-IA, real-time editorial judgment)`

`-> semantic entry transition`

`-> destination world opening, preserving clicked subject`

`-> section-specific interior motion system`

`-> deeper content / related worlds`

`-> Return / Resurface to remembered river context`

This is recursive rather than a conventional page tree:

`World -> World within World -> Story within World`

but canonical repository IA remains the source of truth for what those worlds actually are.

## 7. Motion principles retained from exploration

- Same river, different current speeds.
- Browsing flows; reading settles.
- Motion is semantic.
- One lead motion/attention per viewport.
- Movement yields to reading.
- Stillness is first-class.
- Objects should persist across entry when useful.
- Direction has meaning.
- Color can participate in transition into another world.
- Website motion language and Scripture Cinema narrative motion remain distinct systems.

## 8. Current implementation/prototype state

Resident comparison baselines:

- Living Water Candidate 01 — first full-page river candidate.
- Living Water Candidate 02 — Living Vinyl Wall / multiple currents; useful baseline but not yet the weighted-flow design.
- Motion P1 — technology playground only; never promote as homepage design.
- Second Layer Spatial Navigation Lab — semantic transition prototypes: Unfold, Submerge, Confluence, Source, Gather.

Next design work should preserve these for comparison rather than overwrite them.

## 9. Next prototypes

### Candidate 03 — Live Weighted Editorial Field
Must prove:
- 8:5 as rhythm quantum rather than card constraint;
- 1x/2x/3x+ spans;
- visible primary/secondary/ordinary hierarchy;
- importance-driven dwell and velocity;
- weight handoff;
- layout recomposition rather than simple transforms;
- clear reading despite continuous flow;
- current cross-IA recommendations using canonical content only.

### Church Interior prototype
Must prove:
- Gate entrance;
- clean color world;
- MERSI-like restrained frame/open/reposition/hold behavior;
- sparse, solemn, quiet interior;
- stillness after entry.

### Dawn Library Interior prototype
Must prove:
- click a curated item from first-layer field;
- clicked item becomes full-viewport immersive 8:5 immediately;
- horizontal internal motion allows direct quiet consumption without another click;
- downward scroll reveals library world;
- 8:5 -> 5:8 transformation;
- staggered dynamic walls/towers/streets;
- editorial hierarchy remains legible within density;
- Living City feeling rather than grid/card catalogue.

## 10. Design rule

Do not optimize the richness away before the design exists.

First build enough composition, motion, color, typography, imagery, spatial depth and mature technology to discover the strongest design language. Then subtract, compress and optimize. Simplicity should be the concentration of design, not the absence of design.
