# Doré Image Studio / 多雷製圖

Status: ACTIVE — foundation phase

Owner: `dore-design`

Product: New Westside / 新西望 and Dawn Bookstore / 黎明書局

## Mission

Doré Image Studio is the visual-production arm of Doré. It produces original
editorial artwork and reusable website elements in one recognizable language:
Living Paper, engraved light, watchfulness, scripture, city, road, wall, gate,
book, water, seed, and dawn.

It is not an image prompt collection. It is a governed pipeline:

`research → rights check → visual brief → generate/transform → derivatives → Storybook review → approve → website`

## Two production lines

1. **Editorial artwork** — hero images, article covers, posters, illustrations,
   chapter openers, journal plates, and social crops.
2. **Website elements** — dawn star, rays, dividers, ornaments, bullets,
   engraved initials, section marks, paper textures, borders, masks, loading
   states, empty states, and responsive decorative fragments.

Both lines use the same visual constitution, but website elements must also be
small-size legible, performant, accessible, responsive, and composable.

## Visual constitution

- One unmistakable subject or focal event; avoid decorative collections of shapes.
- Engraving is a reproduction language: carved line, cross-hatching, paper
  knockout, controlled ink density, dry edge, and restrained registration drift.
- Prefer Living Paper plus one dominant plate and one narrowly assigned accent
  plate. The substrate is not another ink.
- The accent plate has a job: first light, scripture marker, annotation, or one
  collision. It is never scattered decoration.
- Type and image must establish a relationship: cross, interrupt, reveal, crop,
  or share an edge. Safe headline-left / picture-right is a rejected default.
- Preserve a large release zone. Empty paper must control pace, not indicate
  unfinished work.
- Do not copy a source artwork or a living artist's distinctive composition.
  Public-domain material may be transformed, but provenance remains attached.

## Asset classes

| Class | Examples | Required delivery |
| --- | --- | --- |
| `hero` | watchman, founded city, open road | master PNG/WebP, desktop/mobile crops, alt text |
| `cover` | article and journal plates | 4:5 and 1:1 crops, title-safe zone |
| `symbol` | dawn star, gate, lamp, book, water | SVG or transparent PNG, 16–128 px tests |
| `ornament` | rays, rules, corner marks, initials | light/dark variants, repeat behavior |
| `texture` | paper, ink grain, hatch field | seamless tile, opacity guidance, size budget |
| `source` | public-domain scan or CC asset | original file, source URL, creator, license proof |

## Definition of done

An asset is not complete until all gates pass:

1. Source or generation provenance is recorded.
2. Rights status is `approved`; search-result thumbnails are never production assets.
3. One semantic role and one intended placement are named.
4. Visual review passes at full size and thumbnail size.
5. Website assets pass transparent-edge, contrast, responsive, and performance checks.
6. Storybook includes light/dark, desktop/mobile, and failure-state specimens.
7. Alt text or `decorative: true` is declared.
8. A human promotes the candidate from `candidate` to `approved`.

## Work packages

### WP1 — Foundation

- Asset manifest and rights policy.
- Search-source catalog with per-item license verification.
- Storybook asset gallery and approval states.
- Naming, versioning, hashing, and derivative lineage.

### WP2 — Dawn element family

- Morning star: primary mark, tiny icon, watermark, inverted version.
- First-light rays and horizon dividers.
- Watchtower, gate, road, scripture/book, living water, seed, and lamp.
- Paper and hatch textures with explicit usage density.

### WP3 — Editorial image families

- Watchman on the wall before dawn.
- Road toward a founded city.
- Scripture opened in the dark.
- Church/common-life scenes without stock-photo advertising poses.

### WP4 — Website adoption

- Replace generic CSS geometry only after an approved Doré asset exists.
- Keep semantic HTML and text independent of decoration.
- Serve responsive WebP/AVIF where appropriate; retain PNG/SVG masters.
- Record every consuming component in the asset manifest.

## Metrics

- 100% assets with source/generation provenance and rights status.
- 0 unverified search downloads in production.
- 100% website assets represented in Storybook before adoption.
- At least three materially different candidates before approving a visual family.
- No asset promoted solely because generation succeeded.
- Homepage decorative payload target: under 500 KB initially, with exceptions reviewed.

## First backlog

1. `dawn-star-01`: engraved morning star; 16, 24, 48, 96 px and watermark tests.
2. `watchman-dawn-01`: convert the current engraving into two controlled plates.
3. `first-light-rule-01`: repeatable horizon/ray divider.
4. `living-paper-01`: seamless paper substrate with no fake antique staining.
5. `scripture-mark-01`: book/page ornament for Bible-study modules.
6. `city-gate-01`: navigation and section-transition mark.
## Required additions beyond image generation

- **Rights ledger:** license evidence, attribution text, personality/trademark flags.
- **Derivative graph:** source → crop → plate separation → optimized website file.
- **Accessibility:** meaning, alt text, decorative status, contrast and motion fallback.
- **Performance:** dimensions, byte budget, responsive sources and lazy-load policy.
- **Design QA:** thumbnail focal event, one-ink/two-ink discipline, originality check.
- **Operational safety:** allowlisted providers, download limits, MIME verification,
  malware scanning, and no credential-bearing URLs in manifests.
- **Editorial governance:** scripture/context accuracy and a human approval gate.
