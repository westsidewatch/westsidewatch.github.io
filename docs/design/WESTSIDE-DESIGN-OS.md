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

**Typography families and weights — audited 2026-10-21.** English display: Bodoni Moda; English genuine small caps: Bodoni Moda SC; Chinese display: Chiron Hei HK WS (昭源黑體). The Journal / Vol.00 Chinese reading role **currently resolves to Chiron Hei HK WS**, because a later OS CSS declaration sets --ws-type-reading-zh to --ws-type-display-zh. The canonical source token JSON and legacy CSS still name Noto Serif TC; this is unresolved source/runtime drift, not an approved second reading system. Standard Chinese weights: 200 airy, 400 standard, 600 anchor; heavy section headings have an independent role. Do not stretch or synthesize fonts; test English extended body copy before naming an English reading family.

**Scripture-reference semantic role.** The Design OS currently defines `--ws-type-scripture-reference-size:clamp(13px,.9vw + 8px,17px)`, and `.ws-scripture-reference` consumes that token. The English scripture quote role is `--ws-type-quote-en-size:clamp(19px,1vw + 13px,27px)`. These are existing shared roles; they do **not** prove that the homepage currently consumes them.

**Sevenfold Dawn homepage — audited current implementation (not a new design specification).** In `static/css/sevenfold-dawn.css`, the Chinese scripture uses `clamp(19px,1.24vw,26px)`; the English scripture uses `clamp(17px,1.1vw,23px)`; its `cite` has `font-size:inherit!important`, overriding the shared `.ws-scripture-reference` font-size so the reference currently inherits the English scripture size. At a 1648px-wide viewport, these CSS formulas yield approximately 20.4px Chinese, 18.1px English and 18.1px reference, before browser verification. This local sizing is **migration debt** against the shared semantic authority, not a second sanctioned scale.

**Change control.** Any future normalization must map the homepage scripture's three roles to Design OS semantic tokens, with scoped overrides only if approved. Do not silently change the already accepted composition. The English text was deliberately broken into two lines (`The night is far spent.` / `The day is at hand.`). Keep Chinese, English, citation, navigation, video, slogan and vertical positioning unchanged unless specifically requested. Measure rendered computed font sizes and viewport bounding boxes before/after any typography or geometry change; avoid unrelated CSS overrides. This memo records the rules only and does not authorize a visual change.


## Editorial Manual — award-calibre precedents and UI Skills (2026-10-17)

**Authority and location.** This is a chapter of **Westside Design OS**, not a new or parallel design system. The operational editorial manual lives at [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md). Its evaluations and precedents are guidance for design decisions; normative typography, palette, spacing and motion authority stays with Design OS tokens, scopes and runtime defined above.

**Typography integration rechecked 2026-10-21.** Runtime imports Bodoni Moda / Bodoni Moda SC, Chiron Hei HK WS and the legacy Noto Serif TC font; its later Chinese reading-family override selects Chiron for Sites. Source token and runtime currently conflict. Semantic sizes and weights remain defined, but the actual computed font needs verification by route. The legacy [WESTSIDE-EDITORIAL-TYPOGRAPHY.md](WESTSIDE-EDITORIAL-TYPOGRAPHY.md) documents additional editorial usage and genuine italic/Small Caps rules but contains a superseded claim that `typography-sitewide.css` is the independent runtime authority. It is a historical/detail reference; any conflict is resolved in favour of Design OS. Never write a second type scale, rewrite global `:root` for local composition, or overwrite approved surface assets.

**Sources incorporated, not discarded.** The OS editorial manual synthesizes the award-calibre precedent corpus, Doré UI Skills explorations R1–R4, Italian editorial grammar and existing magazine typography study. Original research remains in place as an evidence/archive layer. The manual identifies the selection and verification process and links to source-level findings rather than duplicating every case or importing an external visual style.

**Release contract.** Editorial changes must use OS scope tokens, preserve actual copy and approved visual assets, compare relevant variants or prior screenshots, review mobile/desktop/reduced-motion/contrast, and pass existing CI plus visual inspection. Green CI alone does not prove design quality. Do not add another CI job just for the manual.


## SVG exploration research index (2026-10-17)

SVG performance, animation, path geometry, clipping and open-source references are indexed in [SVG-EXPLORATION-LIST.md](SVG-EXPLORATION-LIST.md). This is a research list inside the existing Westside Design OS authority, not a new OS, runtime, or CI. Preserve the approved P2 V75 water and door composition; require measured traces before production performance changes.

**Pending PR #1352 Chinese font source normalization (2026-10-21):** The canonical JSON `font.reading-zh` and `font.display-zh` now agree on the previously effective Chiron Hei HK WS (昭源黑體), with Noto Sans TC/sans-serif fallbacks. Generated CSS is updated; the OS umbrella and typography migration bundles no longer write competing family declarations. The earlier conflict described above is historical. Real deployed font loading, non-Sites reader comparison and longform CJK/English readability **remain unverified**. Do not promote these changes merely because CI is green.

## Normative Chinese/English headline grammar and 12-role scale (2026-10-22)

The user's rule is now explicit: **all Chinese true primary display titles 900**, paired with **visually larger English Bodoni Moda 400** (the genuine finest Bodoni available); **all other non-body Chinese editorial headings 200**, enlarged enough to function as headings. Long-form prose and accessibility-critical small controls retain 400. The earlier practice of using 600 for a main title or 200 for a main masthead is superseded. HTML H-levels alone do not decide primary vs subordinate status.

Twelve detailed responsive display, chapter, article, feature, subhead, standfirst, byline and Contents sizes now come from the canonical Design OS JSON typeScale group and are emitted by its existing generator. Broad older tokens stay as compatibility sizes, not a new local authority. The normative role matrix, numeric min/max/leading/tracking values, pairing ratio, examples and migration conditions are in [WESTSIDE-EDITORIAL-TYPOGRAPHY.md](WESTSIDE-EDITORIAL-TYPOGRAPHY.md). The branch-only /experiments/editorial-type-hierarchy-lab.html displays the actual weight, size, font-family and responsive wrap; it is NOT the final magazine visual design. No protected brand SVG or Olive portrait is to be silently altered.

Release only after verifying 200/900 true Chiron font faces, main vs supporting role markup on P2 and live Journal, 390/768/1648px and 200% zoom, real multi-line headings, and unchanged body/functional readability. The old 600 selectors and some generic title 200 selectors are migration targets, NOT proof the entire site has already adopted the grammar.

## WESTSIDE WATCH Magazine Stylebook — direct production authority (2026-10-22)

**Use the existing [WESTSIDE-EDITORIAL-MANUAL.md §6F](WESTSIDE-EDITORIAL-MANUAL.md) as the first page of magazine production.** This is a concrete edition-style art-direction book: publication proposition, immutable DNA, cover/Contents/longform/atlas/witness/silence, bilingual hierarchy, continuous digital spread, semantic color/image families, figure/caption/notes, motion, responsive rules, actual production cards and approval gates. Existing §6D–6E (books and 32 production-sheet index) are its archival/reference layer, not the art director's default entry. This does NOT create a second OS or permit local font/color globals. Publication-specific new ratios and concept art remain [TRIAL] until screenshots and editorial signoff; all existing tokens, canonical manuscript assets and the one §6A award rubric are unchanged. Not a visually approved final magazine edition.

## The magazine production-design book within the same OS (2026-10-22)

**The magazine project's first deliverable is the fully detailed, executable Westside editorial design manual, not a sequence of prematurely polished screenshots.** The single existing [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md) now contains **§6E Magazine design-book study → Westside full-spec production handbook**. It reviews published editorial-design books, identifies source evidence by access level, maps publication anatomy, image/crop rules, grids, live bilingual type, responsive article templates, real Contents, figure/caption/source credit, motion, accessibility and award-grade review into explicit decisions and tests.

**This is a study/production-handbook draft, not a newly approved artistic identity.** No extra CSS, tokens, CI, second manual or page runtime is introduced. Book study examples and numeric geometry envelopes are marked [TRIAL] until actual material is reviewed and signed off. Preserve existing homepage full-bleed movie and the frozen P2 scene while the publication identity is unresolved.

## The Westside magazine identity study — 2026-10-22

A first formal source-led study of **42 verified research paths across independent magazines, literary publishing, art books and digital editorial**, including 14 deeper A/B-tier design analyses, is now incorporated directly into [WESTSIDE-EDITORIAL-MANUAL.md](WESTSIDE-EDITORIAL-MANUAL.md), **§6D. Doré exploration — Westside Watch Magazine Art Direction**. The user's intended synthesis is classical foundations (true Doré engraved line, papyrus/archival material in meaningful settings, actual Bodoni Moda serif) **expressed through** modern graphic design (Chinese 900/200, seven semantic section colors, editorial-scale motion, unequal grids). The working term **Engraved Editorial Modernism** is a creative research direction, **not** an additional visual-management system, confirmed brand slogan, or authorization to edit existing immutable assets.

The 12-role type scale already in this OS is a technical baseline, not a completed Westside magazine style. New magazine-specific magnified type proportions and classical-modern pair arrangements must be selected after real visual comparisons: Monumental Engraving vs Living Atlas vs Cine-Folio, with actual 87–90% P2 hold, 100% open and a genuine longform article opener for each. The same one OS controls approved fonts, semantic roles, colors and scopes; original research links remain evidence only. Do not promote candidate proportions into global tokens or merge PR #1352 without design signoff, real content and mobile checks.
