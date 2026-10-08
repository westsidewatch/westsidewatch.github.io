# Westside Editorial Typography Authority

## Fonts
- English display, headings, navigation and folios: Bodoni Moda, regular 400. Never synthesize bold.
- English editorial small-cap labels: authentic Bodoni Moda SC, regular 400. No browser-synthesized small caps.
- Chinese realm and UI: Chiron Hei HK WS. Realm headings use the strongest approved weight 600; speaker/subject names use 200.
- Chinese long-form reading: Noto Serif TC, 400 / 600.

## Semantic scale (responsive)
| Role | Size | Weight | Case | Tracking |
| --- | --- | --- | --- | --- |
| Realm Chinese | clamp(36px, 4.2vw, 68px) | Chiron 600 | native Chinese | .12em |
| Realm English | clamp(72px, 10vw, 160px) | Bodoni 400 | Title Case, preserve proper name | -.04em |
| Speaker / subject Chinese | clamp(25px, 2vw, 38px) | Chiron 200 | native Chinese | normal |
| Editorial label | clamp(11px, .85vw, 14px) | Bodoni Moda SC 400 | Small Caps | .1em |

## English case authority
- Realm identity and navigation: preserve the official Title Case (e.g. Olive Mountain, Journal).
- Editorial metadata, folio labels, issue identifiers: true Small Caps when intentionally assigned to the editorial-label role.
- UPPERCASE only for explicit abbreviations, established acronyms and original brand spellings; no global text-transform uppercase.
- Article titles: retain the editorially approved capitalization; running prose uses sentence case.
- Never silently rewrite proper nouns, Bible names, author names or titles.

## Integration
The shared runtime authority is `static/css/typography-sitewide.css`. All live renderers should reference these tokens instead of hardcoding responsive sizes. Do not apply global geometry overrides to Sites surfaces. Generated SVG and raster cover typography must be verified independently: CSS tokens cannot change lettering baked into an image. A CSS weight value alone does not prove that the requested font instance loaded; verify actual computed font and rendered result.
