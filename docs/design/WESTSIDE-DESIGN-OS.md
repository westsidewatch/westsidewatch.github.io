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


## SVG exploration research index (2026-10-17)

SVG performance, animation, path geometry, clipping and open-source references are indexed in [SVG-EXPLORATION-LIST.md](SVG-EXPLORATION-LIST.md). This is a research list inside the existing Westside Design OS authority, not a new OS, runtime, or CI. Preserve the approved P2 V75 water and door composition; require measured traces before production performance changes.


## Watch Ornament — 城牆垛／城牆戳記（2026-11-24，使用者指定規範）

**全站強制規範：取消所有用於轉跳、進入、閱讀更多、前往其他頁面或外部連結的裝飾性箭頭。** Do not use ↗, →, ←, ↓, ↑, chevrons or generic arrow icons as ornamental link markers. Replace the ornamental navigation mark with the Westside **Watch Ornament（城牆垛／城牆戳記；Printer’s Mark／守望節奏）**. Keep link text, native link semantics, keyboard focus and accessible names. Directional controls whose direction is actual information (e.g. carousel or pagination) must not be confused with decorative link markers; redesign them with explicit text or an approved non-arrow control, without making the ornament imply a direction. Do not alter scripture, quoted text, maps or diagrams containing meaningful arrows.

**Historical identity and provenance.** Recover the existing flat, readily recognisable battlement rhythm rather than inventing a new castle, W favicon, generic icon or abstract decoration. The prior brand standard named this motif Watch Ornament; earlier studies included `▇▆▇▅▇`, `▇▆▇▅▇▆▇▆▇▅` and `▇▆▇▅▇▆▇▅`. The verified original repository implementation is **`▆▇▅▇▆▅`**, in `layouts/index.html` as `.watch-rhythm`, with accessible name “End of section”, in [commit 2f9404e](https://github.com/westsidewatch/westsidewatch.github.io/commit/2f9404e669a452b0f8a6a46ec160379ad70aefec). The same commit also introduced `static/images/jerusalem-wall.png`, a separate wall image, NOT the small mark asset. Preserve the six-part rhythm as the recovered reference geometry; do not equate it with the W icon or morning star. A dedicated SVG master and its optical-size proof are pending visual approval; no new artwork is approved by this memo.

**Two roles, one artwork.** Navigation ornament: a small, flat, non-directional sign adjacent to the actionable text, never a button by itself; use the owning surface’s approved OS ink or accent, restrained scale, no extra box, shadow, rotation or animation. Editorial end mark: the same artwork at the actual conclusion of a Westside Watch magazine article, as a quiet printer’s endmark (終止符／結字符), not a link, header, logo or ornamental rule; non-interactive and decorative for assistive technology. Do not automatically append it after every paragraph. Both roles must resolve to one canonical artwork after approval, not independent per-page glyphs. Use CSS currentColor or equivalent OS semantic color; no font-dependent block-glyph rendering in the final canonical SVG.

**Workchain acceptance.** New or revised public designs must be audited for visible decorative navigation arrows, including markup, SVG icon use, CSS pseudo-elements and generated components. Reject a design that introduces or retains decorative arrows in the revised surface; verify the actual rendered Watch Ornament, its visual restraint and link usability on desktop and mobile. Historical surfaces are migration debt, not an exception to the rule. Do not disturb already approved P2 geometry or motion merely to record this policy; migrate the affected links in controlled implementation after the common artwork is confirmed. This entry records the mandatory policy and recovered reference, not a claim of completed sitewide replacement.
