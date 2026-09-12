# Doré UI Skills Exploration R2 — 2026-09-12

Purpose: deepen Doré from general UI competence into production design-engineering judgment. This round focuses on four weak points exposed by real Doré work: motion forensics, comparative variant judgment, state-break testing, and change-level interface review.

## Round 7 — Motion forensics, not just motion creation

UI Skills separates `animate`, `review-animations`, `improve-animations`, `animation-systems`, and performance-specific motion skills. That separation matters: authoring motion and judging motion are different capabilities.

Sources:
- https://www.ui-skills.com/skills/motion
- https://www.ui-skills.com/skills/emilkowalski/review-animations
- https://www.ui-skills.com/skills/emilkowalski/improve-animations
- https://www.ui-skills.com/skills/mengto/animation-systems

Doré lesson:
- every animation review must inspect purpose, timing, easing, origin, physicality, interruptibility, return path, reduced motion, and GPU/compositor behavior;
- do not treat symmetric timing as automatically correct; enter/exit often need different timing;
- distinguish staged keyframe sequences from interactive state changes that should remain interruptible;
- review at 10% speed or frame-by-frame before changing values;
- motion review produces a verdict: block / important / polish / approve, not vague taste comments.

New capability: `ui.motion-forensics`.

## Round 8 — Variant tournament instead of one-shot generation

The strongest new pattern is `variant` / `prototype`: ask "which of these?" rather than "is this right?". Variants must differ on one meaningful axis such as structure, density, emphasis, typography, or voice. Merely changing accent colors teaches nothing.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel/variant
- https://www.ui-skills.com/skills/emilkowalski/prototype

Doré lesson:
- for high-value surfaces, generate 2–4 materially different, brand-faithful directions;
- vary one primary design axis at a time so the winner teaches a reusable lesson;
- keep accessibility and technical quality as a fixed floor, never as a tradeoff;
- record why a direction wins and persist that reason as design memory;
- promotion happens from evidence, not because the first draft is acceptable.

New capability: `ui.variant-tournament`.

## Round 9 — Break the interface deliberately

`break` treats quality as survival under real states, not ideal screenshots. A component should be rendered through hostile and awkward states: empty, long text, short text, mobile width, keyboard focus, missing image, loading, repeated content, reduced motion, and interruption.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel/break
- https://www.ui-skills.com/skills/testing

Doré lesson:
- every important component needs a state matrix;
- visual defects should be attached to the scenario that exposes them;
- a passing happy path is insufficient;
- failing scenarios should route to the correct owner capability: typography, layout, accessibility, writing, motion, performance;
- after a fix, rerender only the failed scenarios plus one control scenario.

New capability: `ui.state-breaker`.

## Round 10 — Review the change, not the whole product

`interface-review` scopes judgment to what a branch / PR / local change actually caused. This prevents reviews from becoming endless codebase audits and makes UI regression ownership precise.

Source:
- https://www.ui-skills.com/skills/jakubkrehel/interface-review

Doré lesson:
- infer the intended visual change first;
- resolve the changed surface from the diff;
- compare before/after and report only regressions or incomplete intent caused by the change;
- keep correctness/security/general code review separate from interface-quality review;
- limit pre-existing findings to a small courtesy set so signal remains high.

New capability: `ui.change-review`.

## Round 11 — Typography becomes geometry

The UI Skills typography guidance treats text as layout: line length, wrapping, optical weight, tracking, leading, variable font settings, tabular numbers, truncation, iOS input zoom, text contrast, and selection state can all change composition.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel
- https://www.ui-skills.com/skills

Doré lesson:
- typography review must measure line breaks and composition at target widths;
- bilingual Chinese/English pages need independent optical checks rather than one shared numeric assumption;
- text wrapping is part of the layout contract;
- type scale and measure belong in visual regression fixtures;
- typography can invalidate geometry even when boxes are mathematically aligned.

New capability: `ui.type-geometry`.

## Round 12 — Visual polish needs a deterministic micro-pass

`better-ui` / `make-interfaces-feel-better` identifies recurring micro-defects that compound into a low-quality feeling: mismatched nested radii, geometric instead of optical alignment, inappropriate shadows, weak image outlines, non-interruptible motion, overuse of keyframes, poor exits, and subtle transition mismatches.

Sources:
- https://www.ui-skills.com/skills/jakubkrehel/better-ui
- https://www.ui-skills.com/skills/jakubkrehel/make-interfaces-feel-better

Doré lesson:
- add a final micro-pass after structural correctness;
- slow motion to 10% for inspection;
- inspect hover/focus/active/loading/empty states separately;
- use optical corrections deliberately and record them as local authored exceptions when not reusable;
- do not convert every successful local correction into a global token.

New capability: `ui.micro-polish`.

## R2 capability bundle

1. `ui.motion-forensics` — slow-motion review, origin/physicality, timing, interruption, return, performance.
2. `ui.variant-tournament` — multiple meaningful directions, one primary axis, evidence-backed winner.
3. `ui.state-breaker` — hostile state matrix and owner-routed failure diagnosis.
4. `ui.change-review` — diff-scoped interface regression review.
5. `ui.type-geometry` — typography as active spatial geometry.
6. `ui.micro-polish` — deterministic final craft pass.

## First proving sequence for Doré

Candidate 1 remains the correct first laboratory, but R2 changes the test order:

1. Freeze the current good baseline.
2. Run motion forensics on Page 2 and Page 3 at slow speed.
3. Build a state matrix for desktop/mobile, hover/tap, interruption, reduced motion, long labels, and viewport extremes.
4. Use change-review on the next visual patch so only the caused regression is judged.
5. For the next major homepage direction, build a three-way variant tournament rather than one candidate.
6. Promote a winner only after visual, accessibility, motion, state-break, and runtime verification all pass.

## Design-memory rule

Doré should not merely remember a value like `translateY(-50%)`. It should remember the reason:

- the preview axis must preserve optical vertical centering;
- four pieces must read as one precise image before the eye notices animation;
- interruption must not destroy spatial continuity;
- a successful local correction becomes a reusable contract only after it succeeds on more than one surface.

This is the key transition from UI prompt-following to design-engineering judgment.
