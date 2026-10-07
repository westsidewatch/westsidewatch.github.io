# Dore Visual Engineer v0.1

A local, deterministic CSS geometry probe for Westside Watch.

## First contract: Candidate 01

Runs the same hover state at 1920×1080, 1680×1050, 1440×900 and 1024×768, then measures the rendered DOM rather than guessing CSS values.

The gate requires:
- large preview top/bottom within 2px of the four-card group;
- large and small windows remain 8:5;
- horizontal living-current animation remains present.

Run:

`npm exec --yes --package=playwright -- node tools/dore-visual/geometry-probe.js http://127.0.0.1:1313/candidate01/walk-worship.html`

This is intentionally a probe/contract layer, not a new layout runtime. It never writes geometry into production pages.
