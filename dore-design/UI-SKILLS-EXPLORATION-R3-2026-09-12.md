# Doré UI Skills Exploration R3 — Taste Memory, Comparative Judgment, and Lightweight Design Intelligence

## Thesis

Doré should not internalize UI taste as a fixed style preset. It should internalize a lightweight judgment process:

`context → alternatives → comparison → winner/loser reasons → evidence → scoped memory → retrieval → fresh verification`

External UI skills remain teachers and references. Durable product taste must be learned from Doré's own real surfaces, outcomes, corrections, and rejected directions.

This follows the project principle that Doré becomes lighter as capability grows: the system should store compact decisions and retrieve only relevant precedent, rather than accumulate giant prompts or a universal style bible.

## Round 7 — Taste is comparative, not absolute

The strongest signal from variant/prototype guidance is that one cannot learn taste from three cosmetically different options. Variants must answer the same brief differently on one primary axis such as structure, density, emphasis, or type. The useful learning object is not the winning screenshot; it is the comparison relation and the reason.

Doré contract:
- never store `this layout is good` without context;
- store `A beat B for this surface, goal, viewport, content shape, and axis because ...`;
- retain the losing reason, because rejection memory is often more reusable than the winning artifact;
- a later surface may legitimately reverse the old preference if its context differs.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel/variant
- https://www.ui-skills.com/skills/emilkowalski/prototype

## Round 8 — Rejection memory is first-class

Generic AI output tends to recur because rejected ideas disappear. Doré should retain compact rejection events:
- what was rejected;
- on which surface;
- why it failed;
- whether failure was brand, hierarchy, motion, typography, accessibility, performance, or context mismatch;
- whether the rejection is local or reusable.

Examples of useful rejection memory:
- repeated equal cards flatten hierarchy on a weighted editorial surface;
- arbitrary rounded containers weaken Living Water's quiet architectural identity;
- decorative perpetual motion is noise where no state/relationship is communicated;
- visually dramatic variants that fail keyboard/mobile/reduced-motion floor are not candidates.

A rejection must not silently become a global ban. Scope is mandatory.

## Round 9 — Dual-channel critique prevents self-confirmation

A strong critique pattern uses independent judgment channels instead of letting one model both author and approve its own work. UI Skills critique guidance explicitly separates design assessment from detector/browser evidence.

Doré adaptation:
- Channel A: visual/design director assessment;
- Channel B: deterministic/runtime evidence (geometry, viewport, DOM states, contrast, motion markers, screenshots where available);
- synthesize only after both exist;
- disagreement becomes an explicit unresolved item, not averaged away.

This protects Doré from converting eloquent explanation into fake evidence.

Source:
- https://www.ui-skills.com/skills/pbakaus/critique

## Round 10 — Motion needs a shared vocabulary before a shared system

A design agent cannot reason consistently about motion if each task uses vague language such as `more natural`, `more cinematic`, or `less stiff`. UI Skills animation-vocabulary converts felt descriptions into named motion concepts.

Doré should maintain a compact motion lexicon for project use:
- stagger
- crossfade
- shared-element / spatial continuity
- arrest
- settle
- overshoot
- spring / timing
- interruption
- reversal / return
- parallax / current
- mask reveal
- assembly / convergence

For every named motion contract, retain:
- semantic purpose;
- allowed triggers;
- expected enter/settle/exit behavior;
- interruption rule;
- reduced-motion equivalent;
- known project examples.

Source:
- https://www.ui-skills.com/skills/emilkowalski/animation-vocabulary

## Round 11 — Taste memory must not become style lock-in

Some external taste skills expose fixed global dials such as design variance, motion intensity, and visual density. These are useful as temporary analysis coordinates but dangerous as permanent Doré identity: a church page, Dawn Library, Search, and Doré Folio should not share one hard-coded density or motion score.

Doré rule:
- use such dimensions as descriptors, never global commandments;
- store them per surface/context when useful;
- prefer project identity evidence over imported default aesthetics;
- do not inherit fashionable defaults such as mandatory bento, huge rounding, fashionable type stacks, or perpetual motion.

Source contrast:
- https://www.ui-skills.com/skills/leonxlnx/taste-skill-v1
- https://www.ui-skills.com/skills/taste

## Round 12 — Critique requires observable evidence and explicit severity

Design review guidance consistently distinguishes blocking/major/minor/polish and asks for specific fixes rather than vibes. Doré should encode a design-health observation as:

`surface + state + finding + severity + evidence + owner capability + proposed correction`

A production/deploy PASS cannot satisfy a visual PASS. A beautiful screenshot cannot satisfy interaction/accessibility PASS.

Sources:
- https://www.ui-skills.com/skills/superfuture/design-review
- https://www.ui-skills.com/skills/pbakaus/critique

## Round 13 — Micro craft is better learned through deltas

The most reusable craft lessons often come from very small before/after deltas: optical rather than mathematical centering, concentric nested geometry, image-edge treatment, enter/exit asymmetry, focus/active state, and motion examined at reduced speed.

Doré should save the minimal correction and the perceptual reason, not only the final CSS value. CSS values are local; perceptual relations transfer.

Source:
- https://www.ui-skills.com/skills/jakubkrehel/make-interfaces-feel-better

## New architecture: Doré Taste Memory

### 1. Pairwise Comparison Ledger
Store:
- surface_id
- task/context
- primary_axis
- candidate_a / candidate_b
- winner
- winner_reason
- loser_reason
- brand_fit
- usability_floor_passed
- viewport/content constraints
- evidence_refs
- confidence
- scope (`local`, `surface-family`, `brand-pattern`)

### 2. Rejection Ledger
Store rejected direction + reason + scope. Rejections are retrievable warnings, not automatic bans.

### 3. Motion Vocabulary Ledger
Store canonical motion term, semantic purpose, interruption contract, reduced-motion equivalent, and project examples.

### 4. Design Observation Ledger
Store severity-ranked observations independently from comparisons. Observations can later support or overturn a preference.

### 5. Retrieval policy
For a new task:
1. infer surface family and task intent;
2. retrieve only a small number of context-near comparisons/rejections;
3. never retrieve all taste memory;
4. treat retrieved preference as precedent, not authority;
5. require fresh evidence before promotion.

## What must NOT be built

- no universal `Doré taste score` that collapses brand/context into one number;
- no global fixed motion/density/variance dials;
- no giant prompt containing the full history;
- no automatic promotion from preference memory;
- no storing screenshots alone as learning without reasons/evidence;
- no turning one successful Candidate 1 fix into a global design token without repeated evidence.

## Next capability target

The next generation of Doré UI intelligence should prove four things on real surfaces:
1. it can retrieve a relevant prior design decision without copying the old layout;
2. it can explain why a previously rejected direction is or is not relevant now;
3. it can reverse an old preference when context changes and preserve the contradiction honestly;
4. it can make the same high-quality comparison on a surface it has never seen before.

Graduation is not `looks like Doré`. Graduation is `can make a context-sensitive design decision, preserve authored identity, show evidence, and learn the result without becoming heavier`.
