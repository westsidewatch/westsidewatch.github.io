# First Look Motion contract

Status: specification only. Homepage PR #1304 remains unmerged pending rendered visual acceptance.

## Design OS authority
Motion vocabulary belongs to the existing Design OS. Page-specific stylesheets retain ownership of static geometry. No second CSS authority, independent CI gate, or duplicated animation controller.

## Shared motion primitives
- Plane: related brand elements translate as one unit.
- Reveal: a clipped layer, doorway, page or light field exposes content.
- Anchor: important typography stays at measured stable coordinates.
- Media: retain the same video or iframe node and source across transitions.
- Reverse: one timeline handles opening, closing and interrupted actions.

## First Look variants
| Surface | Choreography | Preserve |
| --- | --- | --- |
| Home | Sevenfold descending layers | Film iframe and scripture |
| Church | Quiet opening doorway | Church imagery and solemn rhythm |
| Magazine | Editorial page turn | Magazine layout and hierarchy |
| Emmaus | Engraving revealed by light | Dore illustration and scripture |
| Olive Mountain | Immersive horizontal corridor | Twelve speaker posters and featured video |
| Dawn Library | Folio page reveal | Library naming and catalog |
| Paradise Cinema | Cinema screen reveal | Existing player instance |
| Daylight Cafe | Daylight field reveal | Content and contrast |

## Implementation sequence
1. Finish homepage browser QA at desktop, mobile and 4K: closed, intermediate, open and reverse frames.
2. Extract only tested primitives into Design OS Motion, without altering public pages.
3. Pilot Church and Olive Mountain as two different variants of one controller.
4. Extend to the remaining First Look surfaces after individual visual acceptance.

## Accessibility and geometry
Honor reduced motion, keyboard activation, Escape, focus return, image aspect ratios and stable text metrics. Verify layout through the existing Design OS geometry diagnostic. Do not merge #1304 before visual acceptance.
