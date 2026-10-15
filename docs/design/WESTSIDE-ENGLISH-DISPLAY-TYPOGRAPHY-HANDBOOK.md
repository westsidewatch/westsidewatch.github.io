# Westside Watch — English Display Typography Handbook

Status: Design OS editorial manual · living reference · 2026-10-14
Owner: Westside Design OS. This document is a handbook within the existing OS, **not** another CSS authority, subsystem, or CI gate.

## 01. Founding reference: Bodoni Editorial Book

**Bodoni Editorial Book** is the first approved visual reference for the Westside Watch oversized English display composition study. Preserve this name in the editorial reference register. Its precise edition, author, publisher and URL have not yet been independently verified; do not invent attribution or treat the reference as a licensed asset.

Study focus: monumental Didone letters across half a spread; typography as the image; deliberate interplay of large letterforms, negative space, captions and the second language. Reference is for compositional learning, **not** for copying pages or redistributing artwork.

## 02. Publication identity and hierarchy

- English display: existing Design OS **Bodoni Moda**, regular 400, never artificially bold, stretched, or compressed.
- Use true Bodoni Moda small caps only for metadata and explicitly designated labels.
- Chinese large display titles: approved strongest weight; other non-body Chinese: ultralight; reading prose retains reading styles. Follow Design OS tokens, not local hardcoded font declarations.
- Editorial contrast comes from **size, whitespace, crop, baseline and hierarchy**, not additional font families or new colors.
- English oversized type is a recurring signature of the journal, home, first looks, topic openings, authors, bookshop and church editorial pages. Each surface may have its own composition, but shares the same rules.

## 03. The English display composition grammar

1. **Edit before layout.** Identify the semantic phrases and rhetorical stress; the visual break must not create accidental isolated words.
2. **Compose the spread, not a paragraph.** Design a dominant typographic shape occupying approximately half a composition; balance it with whitespace and subordinate bilingual material.
3. **One focal phrase.** Select one primary phrase, one supporting line, and a tertiary citation/label. Do not enlarge all words equally.
4. **Intentional line breaks.** Explicitly define approved phrase boundaries at the editorial level. Preserve semantic units such as “shall flow” and “living water.” Do not rely on random browser wraps to invent the composition.
5. **Responsive recomposition.** At narrower container widths, switch between approved layouts or use container-aware fluid sizes. If a semantic phrase cannot fit, reduce the group’s font size or change composition; do not force a single-word widow or overflow.
6. **Measure with the actual font.** Bodoni glyph widths, italic metrics, kerning, optical spacing and letter combinations determine usable line length. Character counts alone do not.
7. **Allow dramatic crop only when intentional.** Never clip Bible text or essential navigation accidentally. Cropped decorative display is a separately approved treatment.
8. **Keep hierarchy legible.** English display, Chinese translation, scripture citation and entry link must each retain an accessible reading order.
9. **Use existing engraving as a material layer.** Texture should respond to the type’s geometry, not compete with it. Use approved Design OS colors only.
10. **One authority.** Shared typography and semantic line-break policies live in Design OS. Page-specific art direction uses scoped component layout, without repeated competing `!important` overrides.

## 04. Approved composition families to research and prototype

| Family | Editorial behavior | Use |
| --- | --- | --- |
| Half-spread monumental | Oversized English letters anchor 40–65% of available width; other text remains subordinate | Cover, First Look, scripture editorial |
| Staggered headline | Two or three intentionally offset phrases, each with an approved break | Feature opener |
| Asymmetric quiet field | One dense letterform cluster opposing deliberate open space | Church, testimony, contemplative content |
| Letterform and engraving | Didone letter strokes interact with the site's engraved lines without reducing readability | Editorial signature |
| Bilingual counterpoint | English as large composition, Chinese as a quiet typographic counterweight | Magazine and church |

These are **layouts within one OS**, not separate design systems.

## 05. Current case study — John 7:38

Existing wording is authoritative. Avoid a browser-generated lone “flow” or “on” line. Treat these groups as semantic units:

- “He that believeth on me,”
- “as the scripture hath said,”
- “out of his belly shall flow”
- “rivers of living water.”

A deliberate visual break may split a long unit only at an approved phrase boundary. In particular keep “shall flow” and “living water.” together. Responsive sizes must be checked at the actual half-window width (~820px), full desktop, tablet, mobile and browser zoom; CI passing does not prove visual quality.

## 06. Study curriculum and evidence ledger

1. **Bodoni Editorial Book** — founding reference; capture verified bibliographic details and representative compositional observations.
2. **Brodovitch / Harper's Bazaar** — examine scale, white space, image/type relationships and spread rhythm; verify individual examples before attributing.
3. **Emigre, Eye, and editorial typography criticism** — compare intentional display breaks, optical spacing and readable contrast; distinguish historical practice from site policy.
4. **Bringhurst, _The Elements of Typographic Style_** — study typographic rhythm and line composition; document applicable rules with page/edition after source verification.
5. **Müller-Brockmann, _Grid Systems in Graphic Design_** — study modular and asymmetric grid choices, including when editorial compositions deliberately depart from a strict grid.
6. **CSS Fonts, CSS Text and CSS Containment specifications** — map design intent to reliable web typography: font metrics, `text-wrap`, line breaking, container queries and responsive behavior.

For each verified source, record: title, author, date/edition, source URL, legal image-use status, three transferable principles, one anti-pattern, one Westside application, and screenshot-based results. **Do not assert a source has been studied until it has actually been consulted.**

## 07. Acceptance rules

- No isolated single-word line unless explicitly approved as a deliberate editorial statement.
- No distorted or synthesized type.
- No text overlaps, hidden scripture, accidental crop, or unapproved palette.
- Compare at multiple viewport widths and zoom levels using the actual deployed PR preview.
- Preserve a before/after screenshot of the same viewport; a successful build alone is not design acceptance.
- Update this handbook when a successful design rule becomes reusable; update OS runtime only for proven shared behavior.

## 08. Integration

Canonical OS overview: [WESTSIDE-DESIGN-OS.md](WESTSIDE-DESIGN-OS.md).
Existing editorial type authority: [WESTSIDE-EDITORIAL-TYPOGRAPHY.md](WESTSIDE-EDITORIAL-TYPOGRAPHY.md).
Runtime authority: `static/css/westside-design-os.css`.

The current church layout remains an **unmerged PR preview**. Handbook creation does not imply approval or merge of that layout.
