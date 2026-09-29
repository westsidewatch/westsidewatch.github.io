# Westside Watch colour authority — no full black backgrounds

This is a hard brand and beauty gate for the entire site.

## Rule

Black or near-black is **not** a Westside Watch brand background. No page, section, application surface, feature band, navigation world, exploration area, card field, or decorative full-bleed block may use black/near-black as its default background.

Canonical visual authority remains temple stone / warm paper, Dawn Gold `#CEBD74`, and text `#252525`. Darkness must come from content, image, shadow, material, or a justified narrative state — never from a generic “cinematic”, “premium”, “tech”, or “dark mode” assumption.

A narrowly scoped media/rendering surface (for example, the inside of a video player where the medium requires it) may be exempt only when the declaration is immediately preceded by a code comment containing:

`brand-dark-exception: <specific reason>`

The exception must not be used for whole sections or page composition.

## Enforcement

`local/dore-local/no_full_black_background_gate.py` scans site HTML/CSS/SCSS and fails on black/near-black background declarations without an explicit narrow exception.

This gate is repository-wide. Product names such as Cinema, Game, AI, Tool, Archive, or Studio do not override it.
