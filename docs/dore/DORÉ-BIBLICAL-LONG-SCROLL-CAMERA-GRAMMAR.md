# DORÉ Biblical Long Scroll — Camera Grammar & Trajectory Baseline

> Status: EXPLORATION BASELINE / DERIVED SPECIFICATION  
> Project: DORÉ Biblical Dynamic Long Scroll  
> Related narrative source: `DORÉ-BIBLICAL-LONG-SCROLL-NARRATIVE.md`  
> Date: 2026-09-10

## 0. Core decision

The virtual camera is not a secondary effect. It is the principal spatial narrator of the long scroll.

When the full camera trajectory is drawn, the long scroll is largely described: where the viewer begins, what is noticed, what is ignored, where a miracle becomes visible, how one Doré anchor is left, how the interstitial biblical world is crossed, and how the next canonical Doré composition is revealed.

Therefore the project must not begin by animating all 241 works independently. It must first design a continuous **Camera Path Bible**.

The long scroll is treated as one impossible virtual production in which the camera can behave like dolly, crane, steadicam/TRINITY, handheld, aerial, macro, orbit, push-in, pull-back, rack-focus and track-follow, while preserving a single continuous biblical journey.

## 1. Film research translated into project rules

### 1.1 1917 — continuity through camera handoff

The key lesson is not merely “one shot.” The camera changes physical mode while preserving the viewer’s spatial continuity: low/high, following, circling, crossing terrain, moving between handheld/stabilized/crane/vehicle-like motion.

**Doré rule:** a single virtual camera may change rig grammar without visually resetting the journey.

### 1.2 Rope — hidden transitions through occlusion

A foreground body/object can occupy the frame and hide a temporal or spatial transition.

**Doré rule:** robes, rock, darkness, cloud, doorway, tree trunk, wing, water, smoke or another full-frame occluder may carry the viewer from one canonical anchor/world-state into another.

### 1.3 Match-on-action / graphic match

A motion or shape can continue across a change of place/time.

**Doré rule:** walking foot, lifted hand, flowing water, moving cloth, bird wing, circular light, road curve, arch, staff, tree, star or cross-shape can become the bridge between different illustrations.

### 1.4 Virtual camera rigs

Unreal’s Rail + Crane and Blender’s Follow Path confirm a mature production model: define a spline/curve, animate camera position along it, and independently control look target, focal length, focus, roll and elevation.

**Doré rule:** every scene must be describable as camera trajectory + target trajectory + lens trajectory, not just a CSS transform.

## 2. Camera path data model

Every trajectory segment should eventually be machine-readable.

```yaml
shot_id: GEN-001
scripture: Gen.1.1-5
anchor_in: null
anchor_out: DORE_CREATION_OF_LIGHT
camera:
  start_position: [x,y,z]
  end_position: [x,y,z]
  spline: []
  rig_mode: drift|dolly|crane|track|orbit|macro|handheld|aerial
  speed_curve: []
  look_target: []
  focal_length_mm: []
  focus_distance: []
  aperture: []
  roll: []
world:
  light_state: []
  life_state: []
  word_state: []
  miracle_state: []
transition:
  method: occlusion|match_action|graphic_match|path_continuation|light_bridge|world_morph
  carrier: null
settle:
  canonical_dore_frame: true
  duration_or_scroll_span: null
reduced_motion:
  fallback: null
```

The important point: **camera movement, lens movement and world movement are separate tracks**.

A camera can remain still while light moves. A person can move while the camera holds. A camera can move while the Doré composition remains settled. A focal-length change must not be confused with moving the camera forward.

## 3. Directing rule: motivated camera

No camera movement exists merely because movement looks impressive.

Before every movement, answer:

> Why does the camera move now?

Valid motives include:

- Glory: follow or discover the living golden engraving-light.
- Grace: reveal the exact place where life/healing begins.
- Word: create the quiet visual field in which Scripture is discovered.
- Event: follow the decisive action recorded in Scripture.
- Transition: find the physical/visual carrier into the next biblical space.
- Revelation: pull back or change elevation so a previously hidden Doré composition becomes recognizable.

If no narrative motive exists, the camera should remain still.

## 4. Micro-action principle

Large Doré compositions should not be filled with generic motion.

**Macro composition stays Doré. Micro action carries life.**

The camera is what makes a small action monumental.

Examples:

- a lame man: knee accepts weight → foot presses ground → first step;
- breaking bread: thumb pressure → crust separates → hands pause;
- healing: a finger touches cloth → eyelid opens → hand uncurls;
- resurrection: first breath / first finger movement before full bodily action;
- water miracle: a local water surface changes before the larger world responds.

The camera may push from a canonical wide frame into a detail too small to be noticed in the original print, allow the micro-action to occur, and then follow that action into the next space.

## 5. First camera: Genesis opening

### Shot ID: GEN-001 — BEFORE LIGHT

**First camera position:** not in front of the complete Doré engraving.

The project should not begin by showing the entire `Creation of Light` illustration as a poster.

The first camera is placed **inside near-total engraved darkness**, close enough that the viewer initially reads only black hatching / cloud texture and cannot yet identify the full image.

This means the first visual experience is not “Here is Doré’s Creation of Light.” It is: **darkness exists, then light is spoken into it.**

Suggested starting geometry:

- camera height: indeterminate / non-human scale;
- lens: telephoto-to-normal equivalent at first (compressed, no spatial certainty);
- frame content: black engraving strokes, perhaps 90–98% darkness;
- movement: almost none;
- living world: none yet;
- gold: none yet;
- scripture: not yet visible.

The opening must permit stillness.

### GEN-001A — WORD DISCOVERED

In the darkness, Scripture appears quietly rather than entering like a title card:

> 「神說：要有光，就有了光。」

The words should feel discovered within the dark field, not overlaid as UI.

Potential mechanisms to test later:

- letters latent in the engraving texture;
- text revealed by local reduction of darkness;
- linework resolving into characters;
- text existing in depth and becoming legible only as focus changes.

Do not lock one mechanism yet.

### GEN-001B — FIRST MOTION

The first motion in the entire work is the first golden engraved stroke.

It does not flood the screen.

A single line becomes alive.

Then another.

Then the movement propagates through Doré’s existing ray logic.

Camera remains almost motionless at first. This is essential: **the viewer must know that light moved before the camera did.**

### GEN-001C — FIRST CAMERA MOVEMENT

Only after the light has begun does the camera move for the first time.

**First trajectory:** a very slow reverse + slight crane rise, following the expansion of the golden engraved rays.

The camera is not “zooming out” digitally. It is physically retreating through reconstructed depth while focal length changes only minimally.

As it retreats:

1. isolated hatching becomes cloud mass;
2. cloud mass becomes spatial environment;
3. golden rays gain direction and volume;
4. the raised figure becomes partially legible;
5. only near the end does the full Doré composition become recognizable.

The first full Doré frame is therefore a **revelation produced by camera movement**, not the opening image.

### GEN-001D — FIRST SETTLE

The camera reaches the canonical `Creation of Light` composition and settles.

For a brief span, motion reduces sharply.

The viewer is allowed to see the engraving as an engraving.

But the golden line remains alive. The persistent Light state has now been born and must not reset for the rest of the work.

## 6. First trajectory sketch

Conceptual top/side path:

```text
[BLACK HATCHING]
      C0
      •
      |
      |   almost still
      |
      • C1   first golden stroke lives
       \
        \
         \        slow retreat
          • C2  + slight rise
           \
            \
             • C3
              \
               \
                • C4  canonical Doré frame revealed
                   [SETTLE]
```

This is intentionally simple. The opening should not demonstrate camera virtuosity. It establishes the constitution:

1. Word is present.
2. Light moves first.
3. Camera responds to light.
4. Doré world is discovered.

## 7. The camera path must be planned BEFORE miracle animation

For every miracle, first decide where the camera is and what it is looking at.

Example method for a lame man (generic grammar, not canonical sequence assignment):

```text
Doré wide anchor
   ↓ slow push
waist / legs
   ↓ macro focus
knee takes weight
   ↓ camera tracks foot
first step
   ↓ follow walking action
road fills frame
   ↓ environment transforms while movement continues
new biblical road-space
   ↓ crane/pull-back
next Doré anchor revealed
```

Only after this path exists should the body animation be produced.

This reverses the common AI workflow. We do **not** animate a picture and then decide how to show it. We first direct the shot, then create only the movement the shot actually needs.

## 8. Full-scroll planning deliverable

Before production-scale animation, create a complete **Camera Path Atlas** from Genesis to Revelation.

The atlas must include for every major biblical segment:

- entry camera position;
- canonical Doré anchor(s);
- principal look target;
- camera spline;
- lens/focus trajectory;
- Scripture appearance point;
- Light trajectory;
- Grace/Life/Miracle micro-action;
- transition carrier;
- exit path;
- next reveal;
- settle frame;
- mobile camera variant;
- reduced-motion equivalent.

The trajectory atlas, not the 241-image list, becomes the true production storyboard.

## 9. Immediate next exploration

The next pass should build the first real trajectory sequence through early Genesis rather than continue abstract theory:

1. Creation of Light — first camera birth;
2. Formation of Eve;
3. Expulsion from Eden;
4. Cain and Abel;
5. Flood / Ark / Dove;
6. Babel.

For each: draw entry → attention → micro-action → Scripture → transition → exit → next-anchor reveal.

Only when these six prove a continuous camera grammar should the same method scale through Abraham, Exodus, Kingdom, Prophets, Gospels, Acts and Revelation.
