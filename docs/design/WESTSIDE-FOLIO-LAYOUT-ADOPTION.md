# Folio → Westside Editorial Layout Library

Status: **inventory / adoption contract**, not installed or visually approved.
Upstream: https://github.com/Jorgut/folio (MIT; verify individual image rights).
Upstream research checked: 2026-10-15.

## Decision
Adopt **all Folio layout families as structural candidates**, without adopting Folio's aesthetic defaults or copying the repository blindly. Preserve the full original IDs and provenance. Westside Design OS alone owns type families, colors, Chinese typography, engraving and final art direction. Avoid creating a second design system.

## Upstream inventory (do not add overlapping counts)
- 45 original landscape structures (L01–L45), plus provisional L46–L47 and variants; all retained in candidate index.
- 29 previewed wireframes are a rendered subset/edition, **not 29 additional unique layouts**.
- 23 portfolio-relevant references are selections from the 45, **not 23 extra layouts**.
- Magazine facing-page system, including thesis-led opener, dense reading, image/evidence spreads.
- Editorial longform: opener, image-led section break, narrative page with modular side rail.
- Format studies: 16:9, 4:3, A4, 4:5, 3:4, portrait; not every layout supports every format.
- Vertical-writing studies (Traditional Chinese / Mongolian): experimental, not production-approved.
- Native PPTX/PDF exports exist; exact HTML parity and target-app acceptance may be pending.

## Source families and site mapping
| Folio family | Westside targets | Phase |
|---|---|---|
| Covers / navigation L07–L10, L25 | Journal cover, Vol.00, First Look, scripture covers | P1 |
| Text / viewpoints L11–L13, L34 | Longform, devotionals, sermon introductions | P1 |
| Magazine facing-page | Journal features, Dawn Library, testimonies | P1 |
| Editorial longform | Long articles, Bible studies, archives | P1 |
| Image L01–L06, L26–L33, L35, L38–L40 | Olive Mountain, cinema covers, gallery | P2 |
| People / materials L20–L21, L44 | Speaker portraits, interviews | P2 |
| Data / comparisons L14–L16, L36, L41–L43, L45 | Bible timelines, Jerusalem 3000, research | P2 |
| Process / relationships L17–L19 | Bible relationships, ONE | P2 |
| Business / closing L22–L24, L37 | Colophons, footer/contact structures when suitable | P3 |
| Experimental L46–L47 and variants | Optional only after review | P3 |

## Strict acquisition and implementation gates
1. Inspect upstream source files in `reference-layouts/`, `templates/`, `demos/`, `SKILL.md`, `LICENSE`; map each actual source path to its original ID. README descriptions alone are **not** source import.
2. Preserve original layout geometry and semantics in an isolated test; do not redraw an approximation and call it a Folio template.
3. Bind Westside fonts, palette, Chinese reading rules, engraving and spacing through existing Design OS tokens; do not introduce a competing global system.
4. Test John 7:38 on a **single clean preview** with an actual imported layout before expanding to other sections.
5. Validate live URL response, correct page identity, rendered screenshot, overflow/collision and mobile composition; only then mark `approved`.
6. Keep upstream attribution/license notice. Review individual asset licenses; don't import demo imagery automatically.
7. Production adoption is a separate decision; no unreviewed main-site changes.

## Known limitation
At this commit, only upstream public README inventory has been checked. The GitHub source tree could not be downloaded from this runtime; **no Folio source code, CSS, HTML, or complete template has yet been imported**. The existing John 7:38 clean preview remains a Handbook-based test, **not** a Folio template.
