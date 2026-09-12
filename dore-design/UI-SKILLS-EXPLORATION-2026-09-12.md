# Doré UI Skills Exploration — 2026-09-12

Purpose: turn the UI Skills reference into a compact, evidence-backed capability curriculum for Doré Design. This is not a style transplant. Doré keeps its own visual language; the imported value is judgment, motion discipline, systems thinking, accessibility, performance, critique, and verification.

## Round 1 — Routing and minimum necessary skill loading

UI Skills is a catalog for design engineers and agents. Its core operating model is: route by topic/context, load the smallest relevant skill, then implement. The catalog spans Accessibility, Motion, Systems, Visual, Interaction, Performance, Craft, Taste, Typography, Testing, Tooling, and Frontend Architecture.

Source: https://www.ui-skills.com/
Source: https://www.ui-skills.com/agents/claude-code

Doré lesson:
- do not throw a giant design prompt at every task;
- classify task intent first;
- load only the smallest capability bundle;
- make the selected capability explicit and testable;
- prefer reuse of existing project tokens/components/motion language over generic regeneration.

## Round 2 — Motion as a system, not decoration

The Motion catalog separates animation creation, animation review, animation-system architecture, performance, reduced-motion, GSAP primitives, transition polish, and interaction motion. The strongest recurring principle is that motion must communicate state, hierarchy, relationship, or spatial continuity; it must also be interruptible, reversible where appropriate, and measurable on target devices.

Sources:
- https://www.ui-skills.com/skills/motion
- https://www.ui-skills.com/skills/performance
- https://www.ui-skills.com/skills/pbakaus/animate

Doré lesson:
- every animation needs purpose, entry, settle, interruption, exit/return;
- animation tokens should be coherent across a surface;
- avoid one-off timing/easing patches unless a local art-direction exception is intentional;
- prefer compositor-friendly transforms/opacity; isolate expensive blur/filter/shader work;
- `prefers-reduced-motion` should preserve meaning while reducing spatial movement;
- test actual desktop/mobile hardware, not only static correctness.

## Round 3 — Polish and anti-generic judgment

The Visual/Craft/Taste catalogs repeatedly reject generic AI UI signatures: uniform card grids, excessive rounding, random spacing, default type, shadow-heavy surfaces, repeated section templates, generic hero compositions, and decorative motion with no purpose. Strong interfaces use hierarchy, rhythm, intentional typography, controlled spacing, and project-specific identity.

Sources:
- https://www.ui-skills.com/skills/visual
- https://www.ui-skills.com/skills/craft
- https://www.ui-skills.com/skills/taste
- https://www.ui-skills.com/skills/jakubkrehel/better-ui
- https://www.ui-skills.com/skills/anthropics/frontend-design
- https://www.ui-skills.com/skills/addyosmani/frontend-ui-engineering

Doré lesson:
- preserve Westside Watch / Living Water identity instead of importing a fashionable generic shell;
- typography is active composition, not filler;
- section rhythm must vary without losing the system;
- optical alignment and nested geometry matter as much as nominal CSS values;
- polish should be evaluated at slow speed and in edge states;
- use realistic content early because text length and image aspect ratios expose weak composition.

## Round 4 — Systems, layout, typography, and tokens

The Systems catalog emphasizes reusable architecture and token discipline. A useful pattern is primitive → semantic → component tokens. Interface-design guidance also stresses a pre-code intent checkpoint: user goal, hierarchy, palette, depth, typography, and spacing should be explainable before implementation.

Sources:
- https://www.ui-skills.com/skills/systems
- https://www.ui-skills.com/skills/nextlevelbuilder/design-system
- https://www.ui-skills.com/skills/dammyjay93/interface-design
- https://www.ui-skills.com/skills/pbakaus/typeset

Doré lesson:
- encode visual decisions as tokens/contracts where repetition exists;
- distinguish raw values from semantic roles and component-specific usage;
- use 4/8-based spacing unless the existing Doré composition intentionally establishes another rhythm;
- define typography roles and measures, not only font families;
- establish a surface depth strategy instead of mixing borders, shadows, blur, and tints arbitrarily.

## Round 5 — Accessibility is part of craft

Accessibility guidance consistently prioritizes native semantics, keyboard completion, visible focus, accessible names, logical focus order, readable contrast, meaningful reduced-motion behavior, and minimum target sizes. The best rule is to prefer platform-native behavior over custom recreation unless there is a strong reason.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel/better-accessibility
- https://www.ui-skills.com/skills/ibelick/fixing-accessibility
- https://www.ui-skills.com/skills/addyosmani/accessibility

Doré lesson:
- every interactive surface must survive keyboard-only use;
- icon-only controls require names;
- hover-only meaning is insufficient;
- custom motion cannot erase state or trap focus;
- mobile tap targets and zoom behavior are acceptance criteria, not post-polish extras.

## Round 6 — Critique and verification loop

Design-review and testing skills treat UI quality as something that must be checked, not merely authored. Findings should be ranked by severity and paired with concrete fixes. Visual quality should be tested across hierarchy, type, spacing, color, motion, responsiveness, states, accessibility, and brand consistency.

Sources:
- https://www.ui-skills.com/skills/superfuture/design-review
- https://www.ui-skills.com/skills/testing

Doré lesson:
- every candidate needs review before promotion;
- distinguish blocking, important, and polish issues;
- compare against the product's own design evidence rather than generic taste alone;
- use screenshot/visual regression and runtime markers where practical;
- a successful build/deploy is not proof of visual success.

## Doré capability bundles to internalize

1. `ui.intent-route` — infer task intent and load the smallest relevant capability set.
2. `ui.visual-hierarchy` — hierarchy, rhythm, spacing, optical alignment, typography, surface depth.
3. `ui.motion-system` — purpose, timing, easing, interruption, settle, return, reduced motion.
4. `ui.interaction-quality` — hit areas, hover/press/focus, keyboard, state transitions, feedback loops.
5. `ui.design-system` — tokens, component contracts, semantic roles, responsive rules.
6. `ui.performance` — compositor-friendly motion, layout-thrash avoidance, target-device measurement.
7. `ui.accessibility` — semantics, names, keyboard, focus, contrast, motion accessibility.
8. `ui.critique` — severity-ranked review with exact fixes and brand consistency.
9. `ui.visual-verification` — runtime/screenshot/regression checks before promotion.
10. `ui.taste-anti-slop` — detect generic AI patterns and preserve authored identity.

## Immediate application target

Candidate 1 is the first live proving ground because it already exposes the right failure modes: geometric precision, multi-piece assembly, drift/arrest/return, visual hierarchy, mobile behavior, and deployment/runtime verification.

Acceptance for Doré UI growth is not 'knows UI terminology'. It is:
- identifies a real visual defect before being told the exact CSS value;
- distinguishes deploy failure from design failure;
- fixes geometry without degrading motion language;
- keeps motion coherent across pages;
- preserves brand identity while improving craft;
- verifies responsive/accessibility/performance states;
- learns from the result and reuses the successful pattern instead of re-solving it from scratch.
