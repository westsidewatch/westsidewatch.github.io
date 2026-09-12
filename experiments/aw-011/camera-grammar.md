# Doré Film — Camera Grammar v0

This document is not a shot list. It is the directing grammar that sits between narrative intention and Camera Spine construction.

## Core principle

The camera does not reveal space because the model can generate it. The world opens when the narrative earns spatial expenditure.

`Narrative Intention -> Camera Grammar -> Candidate Spine -> World Demand -> Camera–World Score -> Render`

## Grammar rules

### 1. Observe before reveal
Begin from human-scale evidence whenever the story allows it: stone, hand, garment, staff, threshold, animal movement, ground texture, light on a face or object.

Purpose:
- establish documentary presence rather than synthetic spectacle;
- let space emerge through observation;
- naturally bound early World Demand.

### 2. Occlusion is cinematic language, not a cheat
Foreground stone, door frames, shoulders, trees, cloth, architecture and terrain can temporarily conceal space. They should be used when narratively natural, not inserted merely to reduce compute.

### 3. Wide shots must be earned
A wide or panoramic reveal is appropriate when the event itself carries spatial meaning. Exodus-scale, Jerusalem-scale, Crucifixion-scale and apocalyptic scenes may intentionally purchase high World Demand.

Do not optimize away necessary scale.

### 4. Prefer discovery to display
The camera should often discover the world by moving through it rather than presenting a fully exposed generated world immediately.

Typical phrase:
`detail -> occluder -> partial reveal -> human action -> midground -> earned wide`

### 5. Long-take restraint
Favor continuous documentary observation, restrained push/traverse, stable human-scale movement and delayed revelation over constant synthetic camera flourish.

The reference is not imitation of one director or school, but the discipline found in Italian black-and-white documentary/neo-realist long-take language: the camera inhabits a world instead of advertising that world.

### 6. World cost is a directing constraint, not the directing goal
Candidate shots are compared by:

`Shot Score = Narrative Value + Reveal Value + Rhythm Value - Avoidable World Cost`

Only avoidable world cost is penalized. Necessary world cost is accepted when narrative value and reveal value justify it.

### 7. Detail-first does not mean detail-only
The film must preserve contrast between intimacy and scale. If every shot hides the world, the grammar collapses into optimization. If every shot exposes the world, scale loses meaning.

### 8. Camera grammar must remain reusable
The grammar should guide all 241 Doré anchors while allowing local recomputation. Global style is stable; exact Camera Spine coordinates remain scene-dependent.

## Engineering consequence

Camera authoring is no longer:

`script -> hand-authored path`

It becomes:

`script -> narrative intention -> grammar phrase -> candidate spines -> predictive World Demand -> score -> selected spine`

The selected spine then enters the same World Demand / Minimum Evidence / World Memory / Sufficiency pipeline used by AW-011.

## AW-011 lesson

AW-011 is deliberately difficult because the scene is open and has weak natural occlusion. It should remain a stress test rather than be redesigned into an easy shot merely to pass. The lesson from AW-011 is transferred forward: future shots can use natural detail-first grammar intelligently, while large scenes remain available when the story requires them.
