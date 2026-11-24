# Westside Design OS · Editorial Art Direction R2

**Status: visual review candidate, not award-ready.** This is the owning art-direction specification for the *existing* executable Hugo editorial grammar. The previous seven-page grammar system is retained as the production mechanism. P2, the original church façade, the virtual tour and existing approved publication assets are unchanged.

## Failure diagnosis from actual 2026-11-23 Chromium proof

The earlier seven-cover montage and full-page captures reveal a recurring problem: seven differently arranged templates still look like a family of generic software themes. Chinese and English hierarchy is inconsistent; English appears as a competing second title, muted gold / harvest labels have poor small-type legibility, and Cinema imports the navy-and-gold material that belongs to Westside's magazine rather than its own crimson. Longer text is treated as UI text instead of book reading. These are **design-system integration failures** even when the page can render.

In particular, the preexisting `static/css/westside-typography-enforcement.css` has a necessary site-wide selector that sets normal English headline runs to Bodoni Moda Roman. On our special bilingual magazine headline it overrode the genuine Bodoni Moda SC intended by the grammar. The **approved OS mechanism** is `data-ws-designable`; this is applied only to the editorial title, heading, and folio islands, **not to entire pages or functional controls**. All their families/weights/scales continue to consume the original Westside OS tokens. Do not solve this by globally disabling enforcement, adding arbitrary font files or adding layers of CSS overrides.

## Four external editorial references, each with a distinct job

- [The Paris Review](https://www.theparisreview.org/) and [Pentagram's 2021 rebrand](https://www.pentagram.com/work/the-paris-review): cover art has visual primacy, page numbering is quiet, typography does not fight its art. **Application:** Chinese display title as the only headline anchor; subordinate authentic small-caps English, issue folio and an illustrated, text-led article.
- [Aperture](https://aperture.org/editorial/behind-the-scenes-of-aperture-magazines-design-refresh/): typography, portfolios and image sequencing come from the publication's own design history. **Application:** art plates preserve source ratios and independent captions, instead of generic 1:1 cards or stock images.
- [Emergence Magazine](https://www.webbyawards.com/crafted-with-code/emergence-magazine/): audiovisual, long essays and galleries require their own storytelling layout within one editorial identity. **Application:** page covers and block order vary by true content type, not by palette alone.
- [The Public Domain Review](https://publicdomainreview.org/): historical illustrations belong to document-based and research-based narrative. **Application:** Emmaus and Dawn Library assets need provenance; their real text and works must lead the illustrations.

No images or trademarks from those publishers are copied into our site. These are methods, not graphic skins.

## Actual working typography contract (interior editorial pages only)

| Role | Visual job | Shared OS authority | R2 enforced action |
| --- | --- | --- | --- |
| Chinese cover / H1 | The **primary** headline | Chiron Hei HK WS; `--ws-weight-section`; `--ws-type-scale-display-md` | At least 1.65× the paired English computed font-size on screen |
| English cover subordinate | Small-cap translation, **not** second large headline | genuine Bodoni Moda SC; `--ws-weight-standard`; `--ws-type-scale-title-sm` on desktop; `--ws-type-scale-ui` on narrow screen | Remains secondary on 1440 / 768 / 390 / 320 px; no synthetic small caps |
| Official church Chinese name | Protected source artwork, not retypeset by CSS | existing `living-water-west-church-name.png` | Never substitute a plain text label or stretch the artwork |
| Edition / folio / metadata | Quiet publishing structure | genuine Bodoni Moda SC and OS meta scales | Real 4.5:1 minimum legible label contrast |
| Chinese article | Real long-form reading, not UI placeholder | `--ws-type-reading-zh` and OS reading scales | Narrow readable measure (~33 em), deliberate rhythm, strict Chinese line-break rules |
| Bible text | Original saved letterpress, no counterfeit | V60 Scripture Studio source | True 1:1 square or context-specific full preserved text, genuine Chinese vertical print |

**Context distinction:** The accepted P2/first-layer oversized English stage is a different motion/identity context. This R2 rule applies only to **inner editorial reading covers**, not the established P2 opening animations. Do not rewrite canonical global `--ws-realm-en-size` or the homepage's already accepted composition.

## Palette = semantic responsibility, not seven random color fills

Site-wide paper `--ws-paper` and ink `--ws-ink` are the primary reading field. One owning realm accent is permitted in the heading reference, art apparatus, chapter mark and rule. Use **readable neutral ink** for footnotes, captions, index metadata and tiny labels instead of light realm pigments on white.

| Realm | Own accent | Material role |
| --- | --- | --- |
| Church | `--ws-water` | Translucent living-water glass, only where appropriate |
| The Journal | `--ws-night` + existing `--ws-first-light` | Real midnight-blue issue identity and magazine cover art |
| Emmaus | `--ws-first-light`, `--ws-papyrus` | Papyrus and biblical line-engraving; gold is a rule, not small reading ink |
| Olive Mountain | `--ws-olive` | Authentic botanical / portrait editorial art |
| Dawn Library | `--ws-harvest` | Paper, real works, catalogue and curated engraved plates |
| Cinema | `--ws-crimson` + **neutral `--ws-ink`** | Cinema curtain/screen; **not** Journal's navy/gold palette |
| Daylight Café | `--ws-harvest` | Sevenfold provision, daily-life editorial |

Exceptions require a source-specific explanation in this OS, not inline hex declarations. R2 uses derived `--g-label-ink` from OS ink and the realm accent; this is a **component semantic role**, not a second palette authority.

## Composition quality rather than template duplication

The following is now a real page-production rule, not a PDF mockup:

- **Westside Journal:** a large art-first issue opener, actual index, long-form editorial prose, image proof and V60 source.
- **Church:** original name artwork plus an actual vertical Scripture square; worship and contact context should lead, not random blue cards.
- **Emmaus:** an engraved historical reading aperture and Chinese-first Scripture study; images serve text.
- **Olive Mountain:** sermon portrait leads; Chinese structural headline does not compete with English typography.
- **Dawn Library:** editorial works / curation, verified art and proper catalogue relationships.
- **Paradise Cinema:** neutral dark screen with crimson-specific identity, not the magazine's navy/gold.
- **Daylight Café:** quieter whitespace and sevenfold visual provision, not an empty product listing.

Future release must have **a real polished story in each archetype**. The present proof pages remain only candidate demonstrations; some editorial texts and images are still not good enough for a jury.

## Engineering acceptance is necessary but insufficient

The same Hugo/JSON grammar builds and publishes actual sites. Add a **blocking** Chromium check at 1440, 768, 390 and 320 px for every realm:

1. Exactly seven realms use one renderer; existing approved sources remain unchanged.
2. CJK main heading is genuinely Chiron, 900 (or approved OS section weight), and is at least 1.65 times the English line on editorial interior pages.
3. English heading and folio use real Bodoni Moda SC (check computed style, not label appearance).
4. Metadata's actual painted text has minimum 4.5:1 contrast with its optical background, even in Cinema.
5. Art images render at real nonzero dimensions; image ratios, Chinese lines and labels do not clip.
6. Generated eighth article passes exactly the same renderer; never rebuild it by hand.
7. All seven original P2 and original interactive page sources remain intact.

**Human award-calibre jury:** separately compare seven full-page screenshots with the four reference publishers. A fail in art selection, image/text relationship, compositional tension, typography, spacing, originality or reader journey overrides technical green checks. Leave Draft until the pages feel like the same **real publication**, not seven category themes.
