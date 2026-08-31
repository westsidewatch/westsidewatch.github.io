---
status: current
source_of_truth: current repository structure + current Westside product decisions
updated_at: 2026-08-31
supersedes: homepage-v1 information architecture and any specimen that embeds the journal as homepage content
---

# New Westside — Current Information Architecture

The visual redesign MUST preserve product boundaries before composition work.

## 1. Main Site / Website

Role: the durable Westside city / living editorial surface.

Contains:
- official Westside Watch masthead and durable site navigation;
- Living Wall / black-record-wall editorial surface;
- current signals from Journal, ONE, Living Water West, Dawn Library, Archive and other current Westside content;
- Editorial Gravity, Huarong displacement, crenellation/negative-space architecture and time-flow behavior.

The homepage may show a **Journal portal / current-issue signal**, but MUST NOT unfold the Journal issue itself into the homepage. Journal is one high-gravity territory in the city, not the city itself.

## 2. Journal Index

Route/product boundary: `/journal/`

Role: publication shelf / issue entrance.

The existing repository already has a dedicated Journal content section and `layouts/journal/list.html`. Preserve this separation. The redesign may visually update the Journal index later, but the first recovery rule is: Journal remains its own page.

The Journal index should present the formal publication masthead and issue entrances. It is not the main-site Living Wall.

## 3. Individual Journal Volume

Current volume route/product boundary: `/vol-00/`

Role: a self-contained issue with its own art direction and reading experience.

The repository already has dedicated `content/vol-00/` and `layouts/vol-00/`. Preserve it as a distinct publication object.

Vol.00 visual rule for the current rebuild: **migrate the existing main-site/issue visual treatment first; do not redesign the issue from zero.** Future issues may each have their own theme, layout, color, photography/illustration and motion while inheriting the upper Westside Visual DNA.

## 4. Relationship

Canonical metaphor:

> Website is the city. Journal is each exhibition/event that happens inside the city.

Therefore:

`Homepage / Living Wall` → shows a high-gravity Journal entrance → `Journal Index` → selects/enters an issue → `Vol.00` → actual issue reading experience.

Do NOT use:

`Homepage` = `Journal issue` + `ONE` + `Church` all unfolded as equivalent homepage modules.

## 5. Visual-system inheritance

Shared upper Visual DNA: 光・線・紙・刻・築.

Website-specific editorial grammar: 磚・垛・流 + black-record-wall Editorial Gravity + 5:8 + Huarong displacement + time flow.

Journal: inherits upper Visual DNA but may use issue-specific art direction. The permanent website grammar must not flatten every Journal issue into the same Living Wall layout.

## 6. Immediate correction

`dore-design/new-westside/homepage-v1.html` remains FAIL / ANTI-REFERENCE for both visual quality **and information architecture**.

`COMPOSITION-STUDIES-01.html` is only a style/composition laboratory. Any study showing Journal content inside a composition is NOT permission to merge the Journal product into the homepage.

Before Homepage V2 is promoted:
- homepage contains a Journal portal, not the issue body;
- `/journal/` remains a separate page;
- `/vol-00/` remains a separate issue page;
- Vol.00 is visually migrated/preserved before any major redesign;
- navigation between these three layers is explicit and testable.
