# P2 04 — Olive Mountain: reference-led engraved invitation, V13 (Draft)

Status: **art-direction experiment only**. The accepted 3:4 speaker-poster imagery,
English lettering, twelve-speaker order, and 03 MERSI scroll geometry are protected.
No main-branch publication is authorized.

## Problem, not a path-count exercise

The V10 ornamental stripe was compressed into ~66 px; multiplying stroke widths
did not make a recognizable mountain. V11's repetitive synthetic tree/branches
still appeared mechanical. The surrounding P2 04 stage used a full-viewport
`--ws-ink` (#252525) ground, contradicting the Design OS
`static/css/westside-design-os.css` rule **“No black-and-gold variant”**.
An artwork's number of paths and a green CI badge are not art-direction approval.

## Mature samples found by Doré Exploration

1. **William Miller, *Olea europaea longifolia*, *The Botanical Cabinet*,
   plate 456 (1820)**. Its naturally uneven long-leaf silhouette, branch
   junctions, and botanical engraving detail are the visual/anatomical
   reference. Source & PD status:
   https://commons.wikimedia.org/wiki/File:Loddiges_456_Olea_europaea_drawn_by_W_Miller.jpg

2. **John Douglas Woodward / Charles Cousen, *Jerusalem from the Mount of Olives*
   (1881–1884)**. Composition reference: recognizable cultivated olive trees,
   a real hillside, terraces and distant Jerusalem; a geographically specific
   place instead of a generic decorative zig-zag. Source:
   https://commons.wikimedia.org/wiki/File:Jerusalem_from_the_Mount_of_Olives_(NYPL_b10607452-80257).jpg
   Rights record: https://old-digitalcollections.nypl.org/items/510d47d9-5d9b-a3d9-e040-e00a18064a99
   These original images are **research references only** in V12;
   their scanned JPEG pixels are NOT embedded or secretly fetched at runtime.

3. **OpenClipart, *Olive branch in yellow* (item 81199, Public Domain/CC0)**,
   2019 archive. This is the actual vector source adapted into the V12
   editable SVG. The original authored olive-leaf shapes have been separated
   from the old background rectangle, stripped of fixed color/gradient
   definitions, and registered in the invitation's geometry. Source & grant:
   https://freesvg.org/olive-branch-in-yellow
   Accessible archived source in:
   https://github.com/Vrroom/vectorrvnn/tree/main/data/PublicDomainVectors/81199-Olive-branch-in-yellow
   The vector is used under the source artwork's **public-domain** status;
   the third-party host repository's GPL-2.0 program license is NOT assumed
   to be the license for this separately credited OpenClipart dataset asset.

## Executable Design OS constraints

- The final 04 stage, first invitation, left/right invitation carriers:
  `background:var(--ws-olive)` (canonical #738A5A).
- Typography for the enlarged scene uses `--ws-paper` where necessary for
  contrast; engraved foil uses `--ws-morning-gold` and its relief uses
  `--ws-paper`, never a local invented dark-green/black gradient.
- The tiny developer control strip can still use the OS ink for readable UI;
  there must be **no large 04 black-on-gold environment**.
- `04-olive-botanical-gallery-v12.svg` remains a pure vector alpha master;
  CSS mask color is supplied by OS. It is not the ONE scripture-cover ornament.

## The composition under evaluation

- A coherent physical invitation with a detailed *Olea* engraving, not
  a repeated row of formula-generated "olive" twigs or a gold railway.
- The approved 3:4 portrait remains an independent **foreground print**,
  with complete English lettering and original relative scale.
- Exactly one independent page title `OLIVE MOUNTAIN`; the cards carry
  only a restrained one-line speaker caption.
- 03 source remains untouched. The 03 → 04 physical material handoff and
  reversible MERSI scroll semantics remain under existing tests.
- **Reject** this version if screenshots still show an empty card-edge
  stripe, poor botanical recognition, illegible foil, or any full black
  stage. Code acceptance is necessary but not sufficient.


## V13 current candidate: historic vector, registered correctly

**Source of actual SVG botanical paths:** [johnny_automatic, *olive branch*, Openclipart #7331](https://openclipart.org/detail/7331/olive-branch), adapted from Walter Crane's *Line and Form* (reprinted in 1914; originally published 1900). The specific SVG is also available under the [FreeSVG public-domain record](https://freesvg.org/johnny-automatic-olive-branch-1). Full native paths are retained in `static/images/p2-realms/v15/04-olive-historic-engraving-v13.svg`. The lightly outlined city/terrain marks are a secondary working study after Woodward/Cousen (1881), not an exact facsimile of the 1881 engraving.

V12's branch is archived but **rejected** because its full-height diagonal art was obscured by the protected portraits and exposed broken foliage in the middle of the two speakers. V13 uses a 600×90 horizontal master, a 70px card-local headpiece, separate layers for the original 3:4 poster and one global chapter heading, and exact OS `--ws-olive`, `--ws-morning-gold`, and `--ws-paper`. The shared field is OS olive, never the old black `--ws-ink` field, in accordance with the site's **No black-and-gold variant** rule.

**Unresolved art concern:** The botanical is now historical and recognizable, but the simplified city skyline and hillside fine lines remain a design judgment. It must be refined against actual archival engravings before this section is marked award-calibre or merged; a passing Chromium geometry suite is not an artistic verdict.
