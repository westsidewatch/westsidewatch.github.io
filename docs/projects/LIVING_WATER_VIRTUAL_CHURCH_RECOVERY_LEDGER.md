# Living Water West — Virtual Church Recovery and Engineering Accountability
2026-11-21 · GitHub repository: westsidewatch/westsidewatch.github.io

## Why this ledger exists
The user reported three **major, separate rework incidents** associated with losing the ability to continue completed ChatGPT Sites projects:
1. The entire Westside Watch website.
2. The film/television website.
3. The Living Water West virtual church.

These are reports of non-recoverability of previous working projects, **not a verified conclusion that the Sites platform permanently deleted their source**. The recovery process must not use Sites again, and no more rework may be delegated to the user.

## Scope of the incident
The original independent virtual church V4.1 was built and reviewed on Nov 19–20, 2026. Its editable Sites front-end remains unavailable; the original full building GLB and earlier Blender construction scripts remain accessible. During GitHub recovery a replacement virtual tour was erroneously presented as though it followed the earlier design:
- It invented a short glass door in front of an existing tall white entrance, corrupting the entrance silhouette.
- It applied shared green foliage material to the entire maple tree, recoloring living bark and fine twigs.
- It proposed new palettes, although the user had already approved colors in the original project.
- It improvised an abbreviated camera route; it skipped the chapel's main rear west-facing entrance, south staff exit, social/cafe descent, north upper floors and ending sky panorama.
- Static syntax tests had been treated as sufficient proof before browser images confirmed the actual building.
- The assistant inappropriately told the user to paste code back into the project.

Each item is an engineering failure and is the assistant's responsibility to repair, not the user's.

## Verified source of truth
- Original full architectural source model from GLB V34: `static/p2-maquette/model-v34.{0,1,2}.part`.
- Model's own original wall/roof/window/door materials take precedence over guessed palette substitutions.
- The Japanese maple is the Innerscene CC0 maple with individually named geometric components:
  - `japanese_maple fine twig bark`, `japanese_maple rough living bark` — **never leaf-colored**.
  - `japanese_maple foliage 1/2/3` — canopy changes **green in spring/summer → red in autumn → deep red in winter**.
  - The construction Blender V24 specifies original burgundy foliage RGB `(.56,.18,.15)`, bark RGB `(.42,.34,.29)`. No numerical values for each four-season stage were recovered from the original Sites front-end, so those exact values must not be fabricated.
- Direct user-approved Nov 20 camera track:
  1. SOUTH full-front panoramic exterior
  2. Truly opening tall south door
  3. Vestibule and flat courtyard
  4. Truly opening NORTH courtyard glass and the chapel **NORTH PUBLIC rear west-facing door**
  5. Walk from the back of sanctuary toward the SOUTH cross, with horizontal cross-shaped sunlight motion
  6. Exit through the chapel SOUTH STAFF door
  7. South foyer, western cafe and its fellowship plaza
  8. C-shaped descending terraces, north side
  9. Climb through upper galleries to third level and overlook courtyard and red maple
  10. Camera rises into sky for the full building panorama
- Each major scene was intended to have a full daylight cycle. Seasons change along the tour: spring light, summer overhead light, autumn angled red maple, winter deep-red maple and snow. Seasonal transitions must not jump abruptly when changing camera chapters.

## Permanent engineering safeguards
- **Never** use ChatGPT Sites for this project or any future project in this account's work.
- GitHub is source control and recovery authority. Both 3D assets and working application code must have accessible, tested versions.
- This is the second-layer interactive virtual church, *not* the first-layer P2 architectural growth maquette. The original maquette and church schedule are outside the recovery edit scope.
- No engineering labels, subtitles, instructions or visible text on the virtual church view.
- Never declare completion based only on source diff/JS syntax. Require actual WebGL browser scene ready and image evidence from start, courtyard, sanctuary, cafe, upper floors, and end panorama.
- Do not represent reconstructed timings as exact original timings when the former Sites source is not accessible.
- No claims of permanent account-level Sites deactivation without a verified setting.
- No telling the user to paste code or personally perform the repair.

## Active files
- `static/p2/church-tour.js` — actual native virtual church.
- `static/p2/church-tour.html` — no text view or Sites redirects.
- `scripts/p2-church-geometry-audit.mjs` — reconstructs GLB node/world geometry and original maple material ledger.
- `scripts/p2-church-tour-contract.mjs` — guards the real doors, route, 3D assets, and absence of Sites dependency.
- `scripts/p2-church-browser-cdp.mjs` — full-browser WebGL visual proof.
- `.github/workflows/p2-church-tour-visual-qa.yml` — CI image evidence.
