# Doré Exploration — Camera / Attention Grammar for New Westside

Date: 2026-09-09
Status: EXPLORATION RECORD — NOT YET ARCHITECTURE

## Research turn

The Motion Language exploration has reached a more precise question:

> **Motion is the visible result; the deeper design problem is how New Westside directs looking.**

The site should not merely move. It should have **camera sense**: a deliberate way of deciding what the visitor sees first, from what distance, for how long, what enters peripheral attention, when the visual field cuts or reframes, and when motion yields to reading.

This does not mean turning the site into a literal movie interface. The goal is to translate cinematic attention control into editorial/spatial web behavior.

Candidate progression:

`motion effects -> motion language -> camera grammar -> attention choreography`

## Why Horeca matters

The Horeca 2026 case study is useful because its strongest interactions have explicit camera logic rather than generic movement:

- feed cards emerge from deep Z-space toward the camera;
- the nearest card becomes active and changes the background image;
- scaling text remains pivoted around a precise visual point;
- sticky structures alter what remains in the visual frame while scroll continues;
- performance improved when nonessential animation work was removed.

The transferable lesson is not `use 3D cards`.

It is:

> **Every major motion should answer a camera question: what should be foreground, what should recede, where should the eye lock, and when should the frame hand attention to the next subject?**

Source: https://tympanus.net/codrops/2026/06/10/building-horeca-advanced-motion-design-in-webflow-without-the-performance-trade-offs/

## Mature precedents — camera + editorial clarity

### 1. Sons & Daughters — directional reframing for documentary narrative

The Sons & Daughters digital publication combines vertical and horizontal scrolling to tell a photographic family/history story. The underlying content remains editorial and documentary, but changes in direction function as narrative reframing rather than decorative scroll effects.

Transferable principle:

> **A change of movement direction can function like a camera cut or change of scene when it corresponds to a narrative shift.**

For New Westside, a horizontal Scripture current can hand off to a vertical editorial field, or a lower current can shift from browsing to a focused story opening, provided the semantic change is clear.

Source: https://www.commarts.com/project/38653/sons-daughters

### 2. Into the Amazon — cinematic immersion plus editorial discipline

National Geographic's Into the Amazon combines cinematic video, WebGL scroll animation, parallax, data visualization, strong photography and a clean editorial typography system. The relevant point is not technical spectacle; it demonstrates that a cinematic field can remain legible and publication-like when hierarchy, typography and content structure stay disciplined.

Transferable principle:

> **Cinematic immersion should increase attention, not replace editorial hierarchy.**

Source: https://www.commarts.com/webpicks/into-the-amazon

### 3. The Spark — camera path as world/story structure

The Spark uses a vertical city whose spatial gradient carries narrative meaning. Early prototypes tested a moving camera and scroll pacing; character timing and body language were then calibrated until key moments could communicate stakes with almost no copy.

Transferable principle:

> **The camera path can carry meaning before text does.**

For New Westside, visual approach, distance, framing, stillness and transition can establish whether a current is urgent, monumental, intimate, contemplative or investigative before the visitor reads labels.

Source: https://tympanus.net/codrops/2026/01/09/the-spark-engineering-an-immersive-story-first-web-experience/

### 4. Bisous — carefully orchestrated motion inside editorial composition

Bisous describes its interface as a cinematic/editorial experience built from minimalist layouts and carefully orchestrated motion. Motion is used to make browsing instinctive while a stable editorial composition keeps the visual field precise.

Transferable principle:

> **Camera feeling does not require visual clutter. Precision, timing and restraint can produce cinematic perception.**

Source: https://tympanus.net/codrops/2026/06/29/inside-bisous-designing-an-editorial-experience-for-cinematic-cgi/

### 5. Arab Spring Break — axis change as narrative rupture

The interactive story Arab Spring Break changes normal downward scrolling into left-to-right movement when the protagonist enters Libya. The shift corresponds to a seismic narrative change, while a small persistent navigation remains available.

Transferable principle:

> **A camera/axis change is strongest when reserved for a meaningful editorial rupture.**

This argues against continuous arbitrary axis switching across New Westside. Camera grammar should be sparse and semantic.

Source: https://www.commarts.com/project/23891/arab-spring-break

## Candidate New Westside Camera Grammar

The following is a vocabulary for Storybook testing, not a final system.

### 1. Establish

Show the world before demanding action.

Possible use:
- Scripture Cinema opening;
- a major issue/feature entrance;
- a section with strong local art direction.

Behavior:
- large 8:5 field;
- little competing UI;
- restrained persistent orientation anchor;
- enough dwell to understand visual identity.

### 2. Track

Move alongside a current while preserving subject continuity.

Possible use:
- Scripture chronology;
- rolling news/current developments;
- editorial sequence;
- Dawn Library browsing.

Tracking should feel like following, not swiping through cards.

### 3. Push in / approach

Increase scale, contrast, depth or visual dominance as an object becomes the lead current.

Possible use:
- one 8:5 becomes the current focus;
- related material gathers around a feature;
- a news development becomes foreground.

The implementation may be 2D scale/crop, not literal 3D camera movement.

### 4. Hold

Stop reframing and allow attention to settle.

Possible use:
- theology;
- prayer;
- long-form reading;
- key Scripture scene;
- image inspection.

Hold is a camera state, not absence of design.

### 5. Cut

Change the visual grammar quickly when the editorial state genuinely changes.

Possible use:
- breaking event;
- salvation-history rupture;
- shift from overview to testimony/reportage;
- an intentional edition/section boundary.

Cuts should be rare. If everything cuts, nothing feels important.

### 6. Dissolve / confluence

Allow one current to merge into another without a hard replacement.

Possible use:
- Journal feature meets Scripture coordinate;
- 三更報導 gathers historical/theological background;
- book/research objects enter a feature field;
- related content emerges spatially.

This may become one of the strongest nonliteral forms of the Living Water metaphor.

### 7. Pull back / resurface

Restore wider context after deep reading.

Possible use:
- article -> current;
- ONE -> publication field;
- story -> homepage wall.

This should preserve prior spatial position so the visitor feels they resurfaced into the same world.

### 8. Rack focus / attention handoff

One current remains present but loses dominance while another becomes sharp/active.

Possible use:
- viewport conductor transfer;
- fast news gives way to slower feature;
- background current stays alive without competing.

This is a key candidate for coordinating many simultaneous 8:5 currents.

## Camera grammar is not the same as 3D

A major constraint:

> **Camera sense should be achievable through ordinary editorial tools before 3D/WebGL is considered.**

Camera perception can come from:
- scale;
- crop;
- overlap;
- depth ordering;
- contrast;
- blur/clarity;
- sticky framing;
- whitespace;
- typography scale;
- motion direction;
- timing/easing;
- object persistence across transitions.

WebGL/3D is justified only when these cannot express the intended art direction.

This keeps Doré aligned with the principle: more capability, less burden.

## Attention choreography — the deeper system

The camera grammar implies a state machine for attention:

`establish -> approach -> foreground -> hold/read -> handoff -> resurface`

The visual field can be globally alive while local attention remains controlled.

Candidate viewport rule:

> **At any moment, one subject is framed, one or two are context, the rest are atmosphere or dormant.**

This is stronger than merely limiting animation count. It makes the entire page behave like an editor/director deciding what deserves the reader's eye.

## Relationship to the 8:5 system

The 8:5 remains the recurring spatial/editorial object, but it now gains camera roles.

An 8:5 may be:
- establishing frame;
- tracking frame;
- foreground cover;
- held reading image;
- transition object;
- confluence surface;
- resurface destination.

Therefore 8:5 is not only a ratio or cover. It is also a **camera-compatible editorial frame**.

The same object can participate in different states without losing identity:

`8:5 in wall -> 8:5 foreground -> 8:5 opening field -> article -> resurface to same 8:5`

This strengthens the MERSI-like cover continuity while giving it a New Westside-specific motion/attention logic.

## Relationship to different flow speeds

Camera and current speed should be separate properties.

Example:
- 三更報導 may have fast current velocity, but the camera may `hold` on one critical developing story;
- theology may be near-still, but the camera can slowly `push in` to create depth;
- Scripture Cinema may have a measured tracking speed with occasional decisive cuts at narrative ruptures;
- Journal features may be active but use gentle rack-focus handoffs.

So:

`temporal character != camera behavior`

The design system needs both.

## New Storybook experiments

### C1 — camera grammar without 3D

Use only HTML/CSS/native scroll to demonstrate establish, track, push-in, hold, cut, dissolve and pull-back across 8:5 objects.

Acceptance: users should perceive clear camera/attention behavior without WebGL.

### C2 — foreground/background rack focus

Four simultaneous currents. As viewport leadership changes, transfer scale/contrast/motion priority while keeping neighboring currents spatially present.

Acceptance: feels cinematic and calm, not like UI zoom effects.

### C3 — news camera vs news speed

Build a fast 三更報導 current, then hold the camera on one major story while the current context remains alive around it.

Acceptance: urgent without ticker behavior.

### C4 — Scripture Cinema shot grammar

Build a short Genesis-to-Exodus sequence using only 5-7 shot behaviors. Test whether a restrained camera vocabulary produces a stronger Bible-film feeling than continuous uniform pan.

### C5 — cover-to-opening continuity

One lower-homepage 8:5 cover becomes a full opening field through object persistence and reframing, then settles into reading.

Acceptance: `entering the object`, not `loading another page`.

### C6 — confluence shot

A Journal feature remains foreground while related Scripture/ONE/book objects approach from neighboring currents and settle into a readable relationship.

Acceptance: related content feels like currents meeting, not recommendation cards appearing.

## Failure modes

Reject:
- constant fake camera motion;
- every section using zoom/parallax;
- 3D added only for modernity;
- camera motion with no editorial reason;
- excessive depth causing motion sickness;
- scale changes that destabilize typography;
- cinematic openings that delay access to content;
- arbitrary horizontal/vertical switching;
- many simultaneous focal points;
- transitions that destroy canonical navigation or browser behavior.

## Current synthesis

New Westside's desired qualities — contemporary, immersive, dynamic, clear, editorial — are increasingly converging on one design problem:

> **The site needs not only a spatial system and a motion system, but a way of directing attention through that moving space.**

The strongest candidate formulation is:

> **Motion Language tells content how to move. Camera Grammar tells the visitor how to look. Editorial hierarchy decides why.**

This gives a three-layer system:

`Editorial meaning -> Camera / attention choreography -> Motion implementation`

The desired modernity should come from the precision of this translation, not from adding more effects.

## Engineering boundary

Do not freeze this into production camera tokens or select a permanent 3D stack yet.

Correct path:

`Doré Exploration -> Storybook camera prototypes -> human critique -> retained camera/attention vocabulary -> Motion + Design constraints -> promotion gate -> production`

Doré learning object:

`site moves -> currents gain temporal character -> viewport gains conductor -> camera directs attention -> camera grammar becomes constrained design vocabulary -> prototype -> critique -> retained capability`
