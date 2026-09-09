# C03 First Layer Scope — 2026-09-09

Current source of truth for this iteration.

## Scope lock
Only build the first layer:
1. Homepage / opening page.
2. The following Live Weighted Editorial Field page.

Do not continue second-layer interiors, Dawn Library city, Church Gate, or semantic destination transitions in this iteration.

## Color lock
Candidate 01's section/color-world direction is approved and frozen for now. Preserve its navy/dark editorial world, paper/light world, olive Watch Prayer world, Dawn Library gold world, and dawn-gold brand accent. Later color experiments must not silently replace this baseline.

## Motion correction
The user's sketch is the source of truth. The target is not ticker, carousel, horizontal card tracks, Masonry, or independently drifting cards.

8:5 is a rhythm unit. Content weight controls spatial occupation. A content item can occupy multiple rhythm units. When weight changes, the composition itself reallocates space and neighboring content yields/reforms. Static frames must already show primary, secondary, and ordinary hierarchy before animation is applied.

Core sentence: **composition flows; cards do not merely flow.**

## C03 first implementation
`living_water_candidate_03.py` deliberately contains only:
- Page 1: Candidate 01-derived Scripture/source opening and color world.
- Page 2: one sticky full-viewport editorial composition whose grid states recompose as scroll progresses.
- No click-through destination behavior.
- No independent ticker/card-loop animation.

This is the first correction pass, not final art direction.