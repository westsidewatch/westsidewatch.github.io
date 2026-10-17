# Westside Design OS

Status: canonical umbrella authority.

Westside Design OS is the only management system for visual tokens across the public site and tool layer. Typography, color, material, spacing, composition primitives and motion tokens belong under this authority. Existing typography/color files are compatibility runtimes during migration; they are not independent management systems.

## Scope contract

1. Global tokens are defaults, not mandatory page values.
2. Every public surface and tool receives a `data-ws-scope`.
3. A scope can override approved semantic tokens locally. A local adjustment must not rewrite `:root`.
4. Component overrides live below their owning scope.
5. Tools use the same OS and may have independent scoped values.
6. Raw font families, palette literals and competing type scales outside Design OS are migration debt and will be blocked after migration.
7. Composition-specific geometry may remain local when it is not a reusable design token.
8. Generated SVG/covers must consume exported Design OS values or declare an explicit immutable-art exception.

## Authority

Canonical source data: `design-system/tokens/westside.tokens.json`.
Scope registry: `design-system/scopes.json`.
Runtime entry: `static/css/westside-design-os.css`.

Legacy `typography-sitewide.css` and `westside-color-authority.css` are imported by the runtime entry while their declarations are progressively generated/migrated. New management must not be added to those files independently.

## Geometry diagnostics (built into Design OS)

Precise CSS positioning is verified through the shared OS diagnostic `scripts/design-os-geometry-audit.mjs`, with its usage and measurement contract in `docs/DESIGN-OS-GEOMETRY.md`. The targets JSON is a per-surface measurement configuration, **not** a competing positioning system. This tool is invoked during existing Design OS acceptance for layout changes; it does not introduce a separate CI workflow or independent required check. Record measured viewport bounding boxes, computed styles, overlap and tolerances before accepting positioning changes. Correct the owning surface stylesheet instead of layering new overrides. No new public runtime or CSS cascade layer is introduced.


## Typography size authority and homepage scripture memo (2026-10-14)

**Source of truth.** `design-system/tokens/westside.tokens.json` is the canonical Design OS token source; `static/css/westside-design-os.css` is the current runtime type-scale authority. Semantic type roles are `--ws-type-scale-display-xl/lg/md`, `--ws-type-scale-title-lg/md/sm`, `--ws-type-scale-reading-lg/reading`, `--ws-type-scale-ui`, `--ws-type-scale-meta`, and `--ws-type-scale-micro`. These are responsive `clamp()` values, not one fixed pixel size. Pages and tools must consume approved semantic roles through their own scoped values; do not create a second typography management system or rewrite global `:root` for a local adjustment.

**Typography families and weights.** English display: Bodoni Moda; English small caps: Bodoni Moda SC; Chinese display: Chiron Hei HK WS (昭源黑體); Chinese long-form reading: Noto Serif TC. The standard Chinese weight roles are air 200, standard 400, anchor 600. Never stretch fonts or simulate italic/small caps. Existing family files are migration runtimes, not independent authorities.

**Scripture-reference semantic role.** The Design OS currently defines `--ws-type-scripture-reference-size:clamp(13px,.9vw + 8px,17px)`, and `.ws-scripture-reference` consumes that token. The English scripture quote role is `--ws-type-quote-en-size:clamp(19px,1vw + 13px,27px)`. These are existing shared roles; they do **not** prove that the homepage currently consumes them.

**Sevenfold Dawn homepage — audited current implementation (not a new design specification).** In `static/css/sevenfold-dawn.css`, the Chinese scripture uses `clamp(19px,1.24vw,26px)`; the English scripture uses `clamp(17px,1.1vw,23px)`; its `cite` has `font-size:inherit!important`, overriding the shared `.ws-scripture-reference` font-size so the reference currently inherits the English scripture size. At a 1648px-wide viewport, these CSS formulas yield approximately 20.4px Chinese, 18.1px English and 18.1px reference, before browser verification. This local sizing is **migration debt** against the shared semantic authority, not a second sanctioned scale.

**Change control.** Any future normalization must map the homepage scripture's three roles to Design OS semantic tokens, with scoped overrides only if approved. Do not silently change the already accepted composition. The English text was deliberately broken into two lines (`The night is far spent.` / `The day is at hand.`). Keep Chinese, English, citation, navigation, video, slogan and vertical positioning unchanged unless specifically requested. Measure rendered computed font sizes and viewport bounding boxes before/after any typography or geometry change; avoid unrelated CSS overrides. This memo records the rules only and does not authorize a visual change.


## Editorial Manual — award-calibre precedents and UI Skills (2026-10-17)

**Authority and location.** This is a chapter of **Westside Design OS**, not a new or parallel design system. The operational editorial manual lives at [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md). Its evaluations and precedents are guidance for design decisions; normative typography, palette, spacing and motion authority stays with Design OS tokens, scopes and runtime defined above.

**Typography integration verified.** Current Design OS runtime `static/css/westside-design-os.css` already defines Bodoni Moda / Bodoni Moda SC, Chiron Hei HK WS and Noto Serif TC; weight roles 200 / 400 / 600; and responsive `--ws-type-scale-*` semantic sizes. The legacy [WESTSIDE-EDITORIAL-TYPOGRAPHY.md](WESTSIDE-EDITORIAL-TYPOGRAPHY.md) documents additional editorial usage and genuine italic/Small Caps rules but contains a superseded claim that `typography-sitewide.css` is the independent runtime authority. It is a historical/detail reference; any conflict is resolved in favour of Design OS. Never write a second type scale, rewrite global `:root` for local composition, or overwrite approved surface assets.

**Sources incorporated, not discarded.** The OS editorial manual synthesizes the award-calibre precedent corpus, Doré UI Skills explorations R1–R4, Italian editorial grammar and existing magazine typography study. Original research remains in place as an evidence/archive layer. The manual identifies the selection and verification process and links to source-level findings rather than duplicating every case or importing an external visual style.

**Release contract.** Editorial changes must use OS scope tokens, preserve actual copy and approved visual assets, compare relevant variants or prior screenshots, review mobile/desktop/reduced-motion/contrast, and pass existing CI plus visual inspection. Green CI alone does not prove design quality. Do not add another CI job just for the manual.
