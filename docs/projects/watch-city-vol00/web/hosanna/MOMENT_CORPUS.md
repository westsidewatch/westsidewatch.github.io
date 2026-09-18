# Hosanna Moment Corpus — research ledger

Status: ACTIVE EVIDENCE BUILD
Consumer: Vol.00 immersive home + 《一萬年的建城禮》 opening
Rule: no screen source becomes a rendered montage asset until work identity, exact Moment, served copy, time address and publication rights state are all resolved.

## M001 — La Vie et la passion de Jésus Christ

- Production: Pathé Frères
- Date: 1902–1903 / released 1903
- Directors: Lucien Nonguet / Ferdinand Zecca
- Surviving Commons copy: 43:54
- Moment identity: **L’Entrée à Jérusalem**
- Filmographic position: tableau 14 in the 32-tableau listing
- Pathé catalogue number: **855**
- Dramatic evidence: crowd at the city gate; Jesus arrives riding an ass; crowd greets him / waves branches.
- Rights: surviving Commons file is presented as public-domain material.
- Publication state: **SOURCE VERIFIED / EXACT TIMECODE PENDING**
- Do not render yet.

Evidence pages:
- Wikimedia Commons: https://commons.wikimedia.org/wiki/File:La_vie_et_la_passion_de_Jesus_Christ_(1903).ogv
- GRIMH / filmography: https://www.grimh.org/index.php?Itemid=886&id=1468&lang=fr&layout=edit&option=com_content&view=article
- Reference-copy scene description: https://www.dailymotion.com/video/x6bftxb

Editorial value: this is exceptionally strong for the opening corpus because the triumphal entry exists as a discrete early-cinema tableau. It gives the montage a genuinely early screen-era instance rather than beginning with modern biblical cinema.

## M002 — From the Manger to the Cross

- Production: Kalem Company
- Date: 1912
- Director: Sidney Olcott
- Location significance: filmed in Egypt and Palestine; surviving/reissue titles explicitly identify Jerusalem/Bethlehem and other Palestine locations.
- Commons source already identified in sequence manifest.
- Rights: underlying U.S. film is public domain.
- Moment identity: triumphal-entry sequence **not yet frame/time verified in the current evidence pass**.
- Publication state: **CANDIDATE / MOMENT EXTRACTION PENDING**
- Do not render yet.

## Montage grammar learned from M001

The corpus should not be cut merely by film title. Each Moment must expose reusable sub-actions:

1. city / gate expectation
2. crowd gathers
3. rider / ass appears
4. branches rise
5. garments / ground gesture where present
6. Hosanna / acclamation
7. movement across threshold

Future screen Moments can be aligned by these actions. This permits cross-era cuts to preserve one continuous editorial action while image era, actor, camera and production change.

That is the key Montage Emergence rule:

**same biblical action coordinate, changing cinematic evidence.**

## Next evidence pass

1. frame-resolve M001 start/end in the Commons 43:54 copy;
2. extract only an approved publication derivative;
3. frame-resolve M002;
4. widen corpus by cinema era while preserving rights state separately from research value;
5. only after at least three publishable Moments exist, tune montage rhythm against the Doré Original camera path.


## Evidence pass 2026-09-18 — M001 hardened

The Commons source is now independently verified as:

- original file duration: **43 min 54 s**
- source resolution: **210 × 160**
- Pathé production, dated 1903 on the Commons record
- Commons licensing: public domain in country-of-origin jurisdictions with life+70 or less; public domain in the United States because of pre-1931 publication; Public Domain Mark 1.0 / free of known restrictions
- Pathé series description: **32 tableaux**

The historical catalogue evidence resolves the exact Moment identity more strongly:

- **L’Entrée à Jérusalem**
- tableau **14**
- Pathé catalogue **855**
- catalogue year for this tableau: **1902**
- listed physical length: **20 m**

This corrects an important distinction: the assembled film/source is conventionally dated 1903, while the entry tableau itself is catalogued to 1902.

### Exact-timecode gate remains CLOSED

No start/end timecode has been written into the manifest. Catalogue order is not enough to infer a frame address in the surviving 43:54 assembled copy, because early exhibitors could use different selections/orderings and surviving editions can differ.

Therefore M001 is now:

**WORK VERIFIED → RIGHTS VERIFIED → MOMENT IDENTITY VERIFIED → TIMECODE NOT VERIFIED → NOT RENDERABLE**

This is the correct state. The homepage runtime will continue to refuse it until the actual surviving file is frame-resolved.

### Earlier-screen discovery

The early-film catalogue index also exposes multiple distinct Jerusalem-entry titles, including:

- `Entrée à Jérusalem` — Pathé / earlier Passion grouping
- `L’Entrée à Jérusalem` — Pathé / La Vie et la Passion de Jésus-Christ
- `L’Entrée à Jérusalem` — Gaumont / La Vie du Christ
- `Entrée de Jésus à Jérusalem` — Léar / Scènes de la Vie du Christ
- `Entrée à Jérusalem` — Passion de Nancy / Bonne Presse

This changes the corpus strategy: the montage should not assume a 1903 starting point. The screen-history layer can potentially reach further back into the first decade of cinema, provided an extant view and publishable rights state can be verified.

Research evidence:
- Wikimedia Commons source/rights: https://commons.wikimedia.org/wiki/File:La_vie_et_la_passion_de_Jesus_Christ_(1903).ogv
- GRIMH Pathé catalogue 851–866: https://www.grimh.org/index.php?Itemid=230&catid=63&id=991:1896-1906-films-pat-851-866&lang=fr&option=com_content&view=article
- GRIMH 32-tableau ordering: https://www.grimh.org/index.php?Itemid=804&catid=63&id=1468:1896-1906-films-pat0871-0941&lang=fr&option=com_content&view=article
- GRIMH title index / earlier variants: https://www.grimh.org/index.php?Itemid=680&catid=63&id=11649:1896-1906-films-liste-a&lang=fr&option=com_content&view=article


## Evidence pass 2026-09-18 — M001 source binary resolved

The Commons record identifies Internet Archive as the source. The corresponding Archive item has now been resolved directly:

- Archive identifier: `LaVieEtLaPassionDeJsusChristpassionAndDeathOfChrist1903`
- Archive runtime: **43:55**
- downloadable OGG derivative exposed by Archive
- downloadable 512KB MPEG-4 derivative exposed by Archive
- exact MPEG-4 derivative path resolved as `LaVieEtLaPassionDeJsusChrist1903_512kb.mp4`

The source page confirms this is the same Pathé/Nonguet/Zecca film and exposes the downloadable derivatives. Commons independently supplies the public-domain rights evidence.

### Retrieval boundary encountered

The current execution environment can resolve the exact Archive derivative URL but cannot follow the Archive binary CDN redirect. Therefore this pass **does not invent a timecode** and **does not manufacture a substitute clip**.

M001 is now:

**WORK VERIFIED → RIGHTS VERIFIED → MOMENT IDENTITY VERIFIED → SOURCE BINARY RESOLVED → BINARY RETRIEVAL BLOCKED HERE → TIMECODE NOT VERIFIED → NOT RENDERABLE**

This is a useful engineering distinction: future Doré Source Probe / browser-runtime handling should treat a resolved binary whose CDN redirect is unavailable to a static fetcher as a retrieval-capability boundary, not as missing evidence.

Evidence:
- Internet Archive item and derivatives: https://archive.org/details/LaVieEtLaPassionDeJsusChristpassionAndDeathOfChrist1903
- Wikimedia Commons rights/source record: https://commons.wikimedia.org/wiki/File:La_vie_et_la_passion_de_Jesus_Christ_(1903).ogv


## Evidence pass 2026-09-18 — the montage moves back to 1897

The previous working assumption that the usable screen-history line begins with Pathé 1902/1903 is now superseded.

### M000A — Léar / Kirchner, 1897

GRIMH documents a discrete `Entrée de Jésus à Jérusalem` in **Scènes de la vie du Christ**, made by Albert Kirchner (Léar) with Henri Levesque's Passion staging in approximately March–April 1897. Contemporary evidence lists the entry view at approximately **40 metres**.

This is not merely a later filmography title: contemporary 1897 sale evidence for the Passion cycle includes `Entrée de Jésus à Jérusalem`.

State:

**IDENTITY VERIFIED → PRODUCTION DATE VERIFIED → HISTORICAL WORK PUBLIC DOMAIN → EXTANT MOVING-IMAGE COPY NOT YET RESOLVED → NOT RENDERABLE**

Evidence: https://grimh.org/index.php?Itemid=713&id=5299&lang=fr&layout=edit&option=com_content&view=article

### M000B — Hatot / Lumière, 1898

GRIMH's Passion study documents a Lumière `L’Arrivée à Jérusalem` made by Georges Hatot, and compares its staging directly with a later Gaumont remake, `L’Entrée à Jérusalem`. Hatot's 1948 recollections identify Gaston Breteau in the Passion and describe the Gaumont work as a remake of the earlier Lumière Passion.

State:

**IDENTITY VERIFIED → 1898 LAYER VERIFIED → HISTORICAL WORK PUBLIC DOMAIN → EXTANT MOVING-IMAGE COPY NOT YET RESOLVED → NOT RENDERABLE**

Evidence: https://grimh.org/index.php?Itemid=127&catid=84&id=17023%3Ales-passions-1897-1906&lang=fr&option=com_content&view=article

### Editorial consequence

The opening montage no longer has to pretend that cinematic memory begins in 1903. Its desired chronological floor is now:

**1897 Léar → 1898 Lumière/Hatot → 1902 Pathé → later screen eras**

But chronology alone does not admit an image. Production stills and catalogue illustrations remain evidence only. The homepage must wait for an extant moving-image copy before representing either 1897 or 1898 as cinema.

This makes the eventual first cut much stronger: if an extant 1897/1898 view is resolved, the Vol.00 homepage can begin almost at the birth of narrative cinema itself, then let the same biblical entry recur through more than a century of screen history.
