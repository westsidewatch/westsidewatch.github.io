# Westside Editorial Typography Authority

## Fonts
- English display, headings, navigation and folios: Bodoni Moda, regular 400. Never synthesize bold.
- English editorial small-cap labels: authentic Bodoni Moda SC, regular 400. No browser-synthesized small caps.
- Chinese titles: main/cover/realm/article primary names use genuine Chiron Hei HK WS 900; all supporting non-body Chinese editorial titles use genuine 200 with larger measured sizes. Sustained body and functional UI remain 400. The older 600 anchor is migration debt, not a default headline.
- Chinese long-form reading: Chiron Hei HK WS (昭源黑體) 400 via the canonical Design OS reading token; PR #1352 reconciled old conflicting sources and the desktop browser report confirms the paragraph family and loaded Chiron faces. Non-Journal pages and mobile still require visual QA.

## Semantic scale (responsive)
| Role | Size | Weight | Case | Tracking |
| --- | --- | --- | --- | --- |
| Realm Chinese | clamp(36px, 4.2vw, 68px) | Chiron 600 | native Chinese | .12em |
| Realm English | clamp(72px, 10vw, 160px) | Bodoni 400 | Title Case, preserve proper name | -.04em |
| Airy editorial Chinese | clamp(25px, 2vw, 38px) | Chiron 200 | native Chinese | normal |
| Editorial label | clamp(11px, .85vw, 14px) | Bodoni Moda SC 400 | Small Caps | .1em |

## English case authority
- Realm identity and navigation: preserve the official Title Case (e.g. Olive Mountain, Journal).
- Editorial metadata, folio labels, issue identifiers: true Small Caps when intentionally assigned to the editorial-label role.
- UPPERCASE only for explicit abbreviations, established acronyms and original brand spellings; no global text-transform uppercase.
- Article titles: retain the editorially approved capitalization; running prose uses sentence case.
- Never silently rewrite proper nouns, Bible names, author names or titles.

## Integration
**Current authority (2026-10-17):** Westside Design OS is the sole runtime and token-management authority: `design-system/tokens/westside.tokens.json`, scoped by `design-system/scopes.json`, and loaded by `static/css/westside-design-os.css`. `static/css/typography-sitewide.css` is a compatibility runtime during migration, **not a parallel management system**. See [the OS Editorial Manual](WESTSIDE-EDITORIAL-MANUAL.md) for award precedents, UI Skills and review rules. All live renderers should consume OS semantic type roles instead of hardcoding independent responsive scales. Do not apply global geometry overrides to Sites surfaces. Generated SVG and raster cover typography must be verified independently: CSS tokens cannot change lettering baked into an image. A CSS weight value alone does not prove that the requested font instance loaded; verify actual computed font and rendered result.

## Italic typography authority (Bodoni / Didone)
The editorial system uses the genuine Bodoni Moda Italic and Bodoni Moda SC Italic files at weight 400, not artificial oblique. Do not add a separate Didot font family. Use optical sizing appropriate to the rendered size; preserve original italic glyphs, punctuation, and figure design.

| Semantic role | Style | Size | Rule |
| --- | --- | --- | --- |
| English scripture quotation | Bodoni Moda Italic 400 | clamp(19px, 1vw + 13px, 27px) | English quotation text only; do not italicize Chinese scripture characters |
| Scripture reference, including chapter and verse digits | Bodoni Moda Italic 400 | clamp(13px, .9vw + 8px, 17px) | Entire Latin reference including digits, colon, en dash, and Latin book abbreviation is italic |
| Editorial epigraph / pull quote | Bodoni Moda Italic 400 | context-specific heading scale | Use sparingly for quotations and editorial voice, never all body copy |
| Small-caps italic signature / imprint | Bodoni Moda SC Italic 400 | editorial-label scale | Use only when semantically intentional |
| Folio / issue index | Bodoni Moda Roman 400 | folio scale | Keep upright by default; not scripture |
| Chinese scripture text | Effective Journal reading role: Chiron Hei HK WS 400 | reading scale | Do not synthesize slanted Chinese characters; validate runtime |
| Chinese Bible reference | Effective reading role Chiron 400 + true Bodoni Italic Latin digits | reading context | Split reference so only Latin and numeric runs italicize; verify runtime |

### Scripture reference composition
- Display reference: `約翰福音 <span class="ws-scripture-reference">3:16</span>` (Chinese book name stays upright, digits use genuine Bodoni Italic).
- English display reference: `<cite class="ws-scripture-reference">John 3:16–17</cite>` (the entire Latin reference is italic).
- Preserve semantic text and links, avoid turning citations into images or changing source verse numbers.
- In mixed Chinese paragraphs, the Chinese sentence consumes the effective reading role (currently Chiron in Journal / Vol.00); use inline `ws-scripture-reference` only for the numeric/Latin reference. Do not force the legacy Noto family locally.
- `3:16`, `5:17–20`, `1 Corinthians 13:4–7` must retain their punctuation and ordering. Use nonbreaking spacing where a line break would separate the book name from its chapter number; do not force whole multi-verse references to overflow mobile viewports.
- Do not apply italic to **all** numerals: dates, prices, page numbers, timestamps, navigation counters, and data tables are upright unless assigned a separate editorial role.
- For verse numbers inside a scripture passage, mark each verse numeral semantically and style that numeral in Bodoni Moda Italic; the scripture wording stays upright. Superscript is allowed only if the passage template uses it consistently.
- For Scripture quoted in English, distinguish **quotation text** (italic by editorial choice) from **reference** (italic by rule). For Chinese Scripture, keep quotation text upright, with reference numerals italic.
- Keep canonical Markdown text untouched: styling belongs in renderers/components, not destructive replacement of source text.

### Implementation contracts
- `ws-type-italic-en`: genuine italic Latin text.
- `ws-scripture-reference`: genuine italic Latin reference and digits, with lining/tabular numerals for stable citation alignment.
- `ws-type-quote-en`: English italic quotation.
- `ws-type-editorial-label-italic`: genuine Bodoni Moda SC Italic.
- Never use `font-style:oblique`, `transform:skew()`, or browser-synthesized italics.
- Renderer coverage must include Hugo long-form, ONE Bible references, magazine article templates and Doré-generated HTML/SVG covers; these require separate runtime validation, not merely a token declaration.

## Global weight grammar — weight is a visual function, not a content type
**200 / Air** is a sitewide editorial voice, not a speaker-name style. It is appropriate for spacious Chinese display and secondary headlines, article standfirsts, people and author names, book/film titles in editorial contexts, cover typography, selected navigation identities, pull-quote attributions, and large contemplative captions. Use it where ample size, contrast and breathing room preserve readability. Do not use 200 for dense paragraphs, tiny UI controls, accessibility-critical labels or low-contrast overlays.

**400 / Standard** is the working voice for Chinese interface controls, descriptive metadata, short body text, explanatory headings, form fields and neutral information hierarchy. For sustained Chinese reading, use the OS reading role; in Journal / Vol.00 that currently resolves to Chiron 400. Reconcile the legacy Noto source token before declaring one final authority across all reading routes.

**600 / Anchor** is the structural voice for realm names, major Chinese section markers, selected issue or collection headers, and short hierarchy anchors. It is not the default for every heading and must not spread into long paragraphs.

### Weight and size are independent axes
- A person name is not automatically 200; a realm title is not automatically 600 outside the corresponding visual role. Determine **semantic hierarchy, available space, reading density, and contrast** first.
- Pair a restrained 200 Chinese display with Bodoni Moda Roman or Italic when the composition needs air; pair 600 Chinese structural lettering with thin-stroke Bodoni Moda 400 for intentional contrast.
- The 200 role is available on the homepage, Journal, Archive, Dawn Library, Cinema, Emmaus/ONE, Olive Mountain, Church, magazine layouts and Doré-generated covers. Adoption requires each surface to bind the same shared tokens, not duplicate arbitrary declarations.
- Font size uses semantic type-scale tokens, not a per-component increase to compensate for a heavy-looking fallback font.
- Real browser verification must confirm Chiron Hei HK WS loads the 200 instance: its documented variable weight range is 200–900. A computed CSS weight of 200 does not guarantee the loaded glyphs are Chiron ExtraLight.
- New components should choose among `ws-type-air`, `ws-type-standard`, `ws-type-anchor` or equivalent semantic tokens; never invent a content-specific global weight role.

## Chinese reading source normalization (pending PR #1352, 2026-10-21)

The live Sites font behavior had already selected 昭源黑體 through a late runtime override. The JSON token, generated CSS and legacy style bundles are now reconciled in the pending PR so **Chiron Hei HK WS 400** is the planned Chinese article reading role on Journal and non-Sites readers alike. The earlier Noto Serif TC declarations documented here are historical migration evidence only; do not locally force Noto or add another authority. Actual computed family, downloaded font faces, mobile/200% zoom, long Chinese and long English reading quality are **not yet browser-verified**.


## 2026-10-22 — Normative editorial typography: 900 / 200 / 400

**Single visual grammar:** Every true Chinese PRIMARY masthead or story title uses Chiron 900. Its English companion is visually bigger, optically fine Bodoni Moda 400 (400 is the font's lightest genuine weight, NOT fake 200). All other Chinese NON-BODY editorial titles use Chiron 200, enlarged and separated with editorial spacing so they still read as headings. Long Chinese prose and accessible functional text stay 400. Weight and size are independent variables: never set every H1 to 900 or every H2 to 200 without first deciding the semantic role.

**One source:** The 12 named editorial sizes below are part of the typeScale group in design-system/tokens/westside.tokens.json, generated into static/css/westside-design-tokens.css by the existing OS generator. The old display/title generic scale stays compatible with unconverted pages; do not invent a new per-page type authority.

| Role (prefix: --ws-type-scale-) | Main use | Face / weight | CSS min–max | Leading / tracking |
| --- | --- | --- | --- | --- |
| editorial-hero-en | first-layer English masthead | Bodoni Moda 400 | 72–160px | .94 / -.04em |
| editorial-hero-zh | first-layer Chinese PRIMARY | Chiron 900 | 36–80px | 1.12 / .015em |
| editorial-chapter-en | issue/section English opener | Bodoni Moda 400 | 52–112px | .94 / -.04em |
| editorial-chapter-zh | issue/section Chinese PRIMARY | Chiron 900 | 32–68px | 1.12 / .015em |
| editorial-article-en | lead article English display | Bodoni Moda 400 | 56–128px | .94 / -.04em |
| editorial-article-zh | lead article Chinese PRIMARY | Chiron 900 | 40–80px | 1.12 / .015em |
| editorial-feature-en | supporting English feature title | Bodoni Moda 400 | 38–80px | 1.05 / -.018em |
| editorial-feature-zh | supporting Chinese feature | Chiron 200 | 30–50px | 1.28 / .02em |
| editorial-subhead-zh | section within an article, H2/H3 | Chiron 200 | 24–40px | 1.28 / .02em |
| editorial-standfirst-zh | article standfirst / opener | Chiron 200 | 22–36px | 1.50 / .02em |
| editorial-byline-zh | byline, speaker/editor name | Chiron 200 | 18–25px | 1.28 / .02em |
| editorial-contents-zh | contents index headline | Chiron 200 | 20–30px | 1.28 / .02em |
| reading / reading-lg (legacy) | extended Chinese body | Chiron 400 | about 16–21.6px | 1.82 / 0 |
| ui / meta (legacy) | navigation, functional dates, forms | generally 400 | about 12–16px | 1.42 / 0 |

The size limits assume 16px root rem; the intermediate sizes are fluid clamp() values in the JSON, NOT separate desktop and mobile CSS overrides. Chiron and Bodoni have different visual cap-heights; a numeric font-size ratio is a starting point, not proof of physical rendered proportions.

### Priority and layout

1. **P0 paired primary:** English must lead in size, typically visually 1.6–2.2× the Chinese. The Chinese 900 creates the weight counterpoint. Give the full title room to wrap; never distort it or place a heading across protected image assets.
2. **P0 Chinese-only primary:** 900 is appropriate even without an English translation if that name is actually the screen's main editorial subject. Never fabricate English text just to balance columns.
3. **P1 supporting headings:** Chinese 200 at the enlarged feature / subhead sizes above. Distinguish them from prose using location, generous top spacing, line-height and relation to the following paragraph, NOT by reverting to 600. 200 below about 20px may be too faint: enlarge or use an explicit 400 accessibility fallback.
4. **P2 standfirst, contents and people:** Chinese 200 at their dedicated sizes; functional labels, dates, dense multi-line TOCs and forms may retain 400 when the 200 contrast cannot be made reliably readable.
5. **P3 body text:** Chinese 400, sufficient contrast and a measure-controlled column. English 400 Bodoni Moda is an approved DISPLAY family, not yet an approved longform body family; Georgia is still only a browser comparison.
6. **Small Caps and italics:** Bodoni Moda SC genuine forms at 400, true Bodoni Italic where explicitly needed. Do not synthesize, skew or scaleX/scaleY glyphs.
7. **No accidental double authority:** primary role names and size values are global OS tokens; surfaces choose roles with scoped semantic elements, not ad-hoc root rewrites or arbitrary CSS specificity battles. An h1 is not inherently a primary display identity; an h2 can be a primary heading if the publication structure says so.

### Call sites and compatibility

Use CSS classes ws-editorial-hero-en/zh, ws-editorial-chapter-en/zh, ws-editorial-article-en/zh, ws-editorial-feature-en/zh, ws-editorial-feature-zh, ws-editorial-subhead-zh, ws-editorial-standfirst-zh, ws-editorial-byline-zh and ws-editorial-contents-zh with correct lang. Existing ws-type-pair and ws-bilingual-heading accept data-ws-editorial-hierarchy="primary" on the parent to make their Chinese title 900; supporting pairs retain 200. A standalone primary Chinese heading may also use data-ws-type-role="primary-title" and lang="zh-Hant".

Existing protected Olive portraits, homepage SVG text and individually approved assets are not silently retouched. Older 600-style HTML and styling requires an inventory/migration by its owning surface; do not convert those globally without a before/after visual test.

**Acceptance:** compare 320/390/768/1440/1648 CSS-pixel widths, 200% text zoom, 2-character and 25-character Chinese headlines, English line wraps and actual loaded weight 200 vs 900 (computed values alone are insufficient). Keep body text at 400 during a 20k-character longform test, and test 200% reflow without horizontal scrolling. The new editable lab at /experiments/editorial-type-hierarchy-lab.html is a proof surface, not a claim that every existing page has migrated. Follow WCAG 2.2 Resize Text / Reflow for functional reading text.
