# Westside Editorial Typography Authority

## Fonts
- English display, headings, navigation and folios: Bodoni Moda, regular 400. Never synthesize bold.
- English editorial small-cap labels: authentic Bodoni Moda SC, regular 400. No browser-synthesized small caps.
- Chinese realm and UI: Chiron Hei HK WS. Realm headings use the strongest approved weight 600; airy editorial typography uses 200 across all surfaces; structural hierarchy uses 600.
- Chinese long-form reading: Noto Serif TC, 400 / 600.

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
The shared runtime authority is `static/css/typography-sitewide.css`. All live renderers should reference these tokens instead of hardcoding responsive sizes. Do not apply global geometry overrides to Sites surfaces. Generated SVG and raster cover typography must be verified independently: CSS tokens cannot change lettering baked into an image. A CSS weight value alone does not prove that the requested font instance loaded; verify actual computed font and rendered result.

## Italic typography authority (Bodoni / Didone)
The editorial system uses the genuine Bodoni Moda Italic and Bodoni Moda SC Italic files at weight 400, not artificial oblique. Do not add a separate Didot font family. Use optical sizing appropriate to the rendered size; preserve original italic glyphs, punctuation, and figure design.

| Semantic role | Style | Size | Rule |
| --- | --- | --- | --- |
| English scripture quotation | Bodoni Moda Italic 400 | clamp(19px, 1vw + 13px, 27px) | English quotation text only; do not italicize Chinese scripture characters |
| Scripture reference, including chapter and verse digits | Bodoni Moda Italic 400 | clamp(13px, .9vw + 8px, 17px) | Entire Latin reference including digits, colon, en dash, and Latin book abbreviation is italic |
| Editorial epigraph / pull quote | Bodoni Moda Italic 400 | context-specific heading scale | Use sparingly for quotations and editorial voice, never all body copy |
| Small-caps italic signature / imprint | Bodoni Moda SC Italic 400 | editorial-label scale | Use only when semantically intentional |
| Folio / issue index | Bodoni Moda Roman 400 | folio scale | Keep upright by default; not scripture |
| Chinese scripture text | Noto Serif TC Roman 400 | reading scale | Do not synthetically slant Chinese glyphs |
| Chinese Bible reference | Noto Serif TC Roman 400 + italic Latin digits | reading context | Split reference into semantic spans so only Latin and Arabic numeral runs italicize |

### Scripture reference composition
- Display reference: `約翰福音 <span class="ws-scripture-reference">3:16</span>` (Chinese book name stays upright, digits use genuine Bodoni Italic).
- English display reference: `<cite class="ws-scripture-reference">John 3:16–17</cite>` (the entire Latin reference is italic).
- Preserve semantic text and links, avoid turning citations into images or changing source verse numbers.
- In mixed Chinese paragraphs, the Chinese sentence remains Noto Serif TC; use inline `ws-scripture-reference` only for the numeric/Latin reference.
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

**400 / Standard** is the working voice for Chinese interface controls, descriptive metadata, short body text, explanatory headings, form fields and neutral information hierarchy. For sustained Chinese reading, switch family to Noto Serif TC 400 rather than assuming Chiron 400.

**600 / Anchor** is the structural voice for realm names, major Chinese section markers, selected issue or collection headers, and short hierarchy anchors. It is not the default for every heading and must not spread into long paragraphs.

### Weight and size are independent axes
- A person name is not automatically 200; a realm title is not automatically 600 outside the corresponding visual role. Determine **semantic hierarchy, available space, reading density, and contrast** first.
- Pair a restrained 200 Chinese display with Bodoni Moda Roman or Italic when the composition needs air; pair 600 Chinese structural lettering with thin-stroke Bodoni Moda 400 for intentional contrast.
- The 200 role is available on the homepage, Journal, Archive, Dawn Library, Cinema, Emmaus/ONE, Olive Mountain, Church, magazine layouts and Doré-generated covers. Adoption requires each surface to bind the same shared tokens, not duplicate arbitrary declarations.
- Font size uses semantic type-scale tokens, not a per-component increase to compensate for a heavy-looking fallback font.
- Real browser verification must confirm Chiron Hei HK WS loads the 200 instance: its documented variable weight range is 200–900. A computed CSS weight of 200 does not guarantee the loaded glyphs are Chiron ExtraLight.
- New components should choose among `ws-type-air`, `ws-type-standard`, `ws-type-anchor` or equivalent semantic tokens; never invent a content-specific global weight role.
