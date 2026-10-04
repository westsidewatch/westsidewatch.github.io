# Westside Chromatic Field — Color Authority

**Status:** canonical visual authority  
**Formula:** **Identity × Material × Light = Surface**

This document governs color across the current first-level architecture:
LivingWaterWest / Magazine / Bible / Sermon / Book / Cinema / Life / Search.

## 1. Authority hierarchy

1. **Foundation** — Living Paper, Ink, Watch Night and the shared light/gold family.
2. **Chromatic identity** — one branch identity per first-level content surface.
3. **Material** — Dore engraving, paper, Temple Stone, papyrus, water, curtain, botanical/domestic surfaces.
4. **Illumination** — Dawn, Sacred, Scripture, Hillside, Reading, Projection, Daylight.
5. **Semantic role** — atmosphere, surface, raised, line, identity, interaction, deep, text, shadow.

Pages MUST request semantic roles. Pages MUST NOT invent local theme colors when an authority token exists.

## 2. Branch map

| Surface | Chromatic authority | Material authority | Light authority |
|---|---|---|---|
| LivingWaterWest | Living Water Blue #5B8FA8 + white/gold | Temple Stone + water + Dore engraving | Sacred |
| Magazine | First Light Gold #A2872A | editorial paper + Dore engraving | Dawn |
| Bible | Papyrus field / Pale Gold #CEBD74 | Temple Stone + papyrus + Dore engraving | Scripture |
| Sermon | Olive Branch #738A5A | landscape engraving | Hillside |
| Book | Harvest #B8944A | paper + engraved object | Reading |
| Cinema | Crimson Robe #A14D57 | curtain + Dore engraving | Projection |
| Life | Daylight Mauve, OKLCH field | botanical/domestic engraving | Daylight |
| Search | no branch color | neutral utility surface; provenance may inherit source branch | neutral |

Bible is deliberately material-led rather than a flat-color theme. Life occupies the missing low-chroma mauve field; its production tonal family is generated perceptually, not chosen as an isolated purple.

## 3. Dore material rule

Engraving is part of color, not decoration. Every major branch background may combine:
**base color → assigned Dore engraving → branch light field → content**.

Each branch owns an engraving territory/corpus. The Color Authority owns opacity, blend and illumination. A page may select an approved engraving asset but may not create arbitrary gradients or tint recipes.

## 4. Color hierarchy

Color follows the existing **Silence / Voice / Event** hierarchy:
- **Silence 70–90%**: paper/material/image space.
- **Voice 10–25%**: ink + branch identity + structural lines.
- **Event ≤5%**: active, focus, playback, current section, momentary light.

Branch color is identity, not permission to flood an entire reading surface.

## 5. Tonal families

Every chromatic anchor generates perceptual tonal roles rather than hand-mixed RGB variants:
**atmosphere → surface → raised → line → identity → interaction → deep → text → shadow**.

Generation uses OKLCH/OKLab relationships so illumination and shadow remain recognizably within the same family. White/black opacity overlays are not the primary method for producing a tonal family.

## 6. Forbidden combinations

1. **Dark + Gold dominant theme is forbidden.** Watch Night/Ink/black may not pair with gold as the dominant identity treatment.
2. **Branch collision is forbidden.** Two first-level branch colors may not compete for identity on one surface.
3. **Decorative theology is forbidden.** Crimson, gold, water blue and other semantically loaded colors are not arbitrary decoration.
4. **Full flood is forbidden by default.** Branch color does not automatically become a long-reading background.
5. **Color-only state is forbidden.** Active/focus/status meaning must also have form, text, line, position or another non-color cue.
6. **Local raw color drift is forbidden.** New ad-hoc HEX/RGB theme colors require promotion into this authority or removal.

## 7. Motion + light

Motion may change illumination, reveal material, or alter engraving visibility. It MUST NOT change a branch into another branch's identity color.

Dawn / Flow / Reveal / Gather consume this authority; they do not own separate palettes.

## 8. Accessibility and responsive use

Body text and essential UI must preserve WCAG-readable contrast. Fine Cormorant display work should exceed bare minimum contrast where practical. On smaller screens, reduce large color fields and material density before reducing information clarity.

## 9. Search and cross-surface content

Search has no independent branch color. Results may carry a restrained provenance accent from their source branch. Tool chrome remains neutral.

## 10. Governance

The canonical implementation is `static/css/westside-color-authority.css`. New visual work must consume its tokens. Existing surfaces migrate progressively; migration must preserve functionality and information architecture.


## 11. Executable Color Operating System

The authority now exposes a uniform runtime contract for every branch:

`atmosphere → material → surface → raised → structure → identity → interaction → deep → text → engraving`.

Components consume semantic variables and `data-ws-zone` roles; anchors are not component APIs. Doré linework derives from each branch's engraving role. Shared navigation remains neutral and reveals branch identity only for current-state signals.

Responsive material density and increased-contrast behavior are part of the authority. New pages must not bypass this contract with local theme literals.
