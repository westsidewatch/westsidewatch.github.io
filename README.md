# Westside Watch

Westside Watch — A Bible study and community publication project.

The official publication site is built with Hugo without a third-party theme. The existing `join/` invitation remains available as an independent page.

## Canonical architecture entrypoints

For current system structure and cross-project engineering context, start here:

- `docs/MASTER_SITE_ARCHITECTURE.md` — canonical main-site structure.
- `docs/dore-exploration-global-index-2026-09.md` — global indexing, Bible Index, engineering index, Doré Memory and A2A exploration record.
- `docs/dore-memory-core-boundary.md` — Memory Core provider boundary.
- `docs/a2a-reliability-atlas-v1.md` — A2A reliability map.

The repository contains many project-specific records. These entrypoints are intended to prevent architectural context from being reconstructed from old branches, PR descriptions, or chat history.

## Local preview

Install Hugo Extended, then run:

```sh
hugo server -D
```

The site is deployed automatically to GitHub Pages when changes reach `main`.

## Editorial structure

- `content/` — issues and articles
- `layouts/` — page templates and partials
- `assets/css/` — the design system and styles
- `static/` — images, fonts, and other files copied as-is

## Brand foundation

- First Light Gold 100 — `#A2872A`
- Gold 80 / Warm Gold — `#B79838`
- Gold 30 / Morning Gold — `#D2BC69`
- Watch Night Blue — `#102A43`
- Living Paper White — `#FAF9F5`
- Ink Black — `#252525` (taken from the PDF swatch; the printed HEX repeats Living Paper in error)
- Olive Branch — `#738A5A`
- Living Water Blue — `#5B8FA8`
- Harvest — `#B8944A`
- Crimson Robe — `#A14D57`

Temple Stone is a material system with Light, Classic, and Aged variants, not a single flat brand color.

The current font stack is a system-safe placeholder. Replace it with the licensed webfont files used by `join` when those assets are available.
