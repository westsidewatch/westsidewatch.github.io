# Doré Visual Designer 01 — LIGHT-01 Composition Hypotheses

Status: STUDY / PRE-PENPOT
Gate: no production drawing until one hypothesis survives critique.

## Hypothesis A — Threshold / 門隙初光

- Source: outside the upper-left edge, never shown directly.
- Direction: narrow diagonal entry, upper-left → lower-right.
- Occlusion: a dark architectural threshold interrupts most of the source.
- Foreground: near-black engraved edge / jamb, dense linework.
- Midground: Living Paper field receiving only a broken wedge of illumination.
- Background: nearly empty paper; no decorative sky.
- First Light Gold: only on the first 1–3 contact edges where light touches the threshold/paper boundary.
- Depth mechanism: hard near occlusion + softer secondary trace + large quiet field.
- Website crop: survives hero crop, card crop and narrow mobile crop because source remains off-canvas.
- Failure risk: can become generic 'doorway light' or luxury-brand gold stripe if the engraved obstruction lacks spatial specificity.

## Hypothesis B — After the Cloud / 雲後裂光

- Source: above frame, concealed behind an irregular engraved cloud mass.
- Direction: 2–3 non-parallel openings descend into the paper field.
- Occlusion: asymmetrical cloud/ink structure; no evenly spaced rays.
- Foreground: almost none; atmosphere is carried by interruption rather than objects.
- Midground: broken illumination with unequal widths and fading reach.
- Background: Living Paper remains dominant and brightest.
- First Light Gold: tiny accents at the torn edges of the occluder, not inside the whole beam.
- Depth mechanism: unequal ray widths, partial disappearance, line-density falloff, paper brightness.
- Website crop: strongest as section transition and editorial opening; weaker as small icon.
- Failure risk: easily becomes religious clip-art, spotlight rays, or gradient glow. Must avoid symmetry and literal cloud illustration.

## Hypothesis C — Distant City / 城牆以前的光

- Source: low horizon beyond an engraved architectural silhouette.
- Direction: predominantly horizontal/low-angle grazing light.
- Occlusion: city/wall silhouette blocks the source; only edge events and narrow openings reveal it.
- Foreground: sparse dark architectural fragments with varying line density.
- Midground: thin illuminated edges and a few long, broken traces across Living Paper.
- Background: large quiet paper field above; source itself remains unseen.
- First Light Gold: restricted to wall crowns, battlement edges and one or two openings.
- Depth mechanism: silhouette scale, overlapping wall planes, diminishing engraving density, low-angle edge light.
- Website crop: especially suitable to Westside Watch because CITY and LIGHT can later share one grammar without merging asset families.
- Failure risk: may prematurely lock LIGHT to CITY imagery and reduce LIGHT's general reuse.

## Critique matrix

| Criterion | A Threshold | B Cloud | C City |
|---|---:|---:|---:|
| Clear causal light source | 5 | 4 | 5 |
| Occlusion creates depth | 5 | 5 | 5 |
| Living Paper remains light | 5 | 5 | 4 |
| Gold used as event, not fill | 5 | 4 | 5 |
| Avoids generic glow | 5 | 2 | 5 |
| Reusable across website | 5 | 4 | 3 |
| Distinct from later asset families | 5 | 5 | 2 |
| Mobile crop resilience | 5 | 3 | 4 |
| **Total / 40** | **40** | **32** | **33** |

## Selection

**A — Threshold / 門隙初光** advances to LIGHT-01 prototype.

Reason: it expresses LIGHT without depending on SKY or CITY, preserves Living Paper as the luminous field, gives First Light Gold a causal edge-contact role, and remains robust under responsive cropping.

## Mandatory prototype constraints

1. One asset only: `LIGHT-01 / THRESHOLD`.
2. No label/rule/sample-card children inside the asset.
3. No opaque beige rectangle pretending to be the asset.
4. Asset must contain visible rendered geometry with non-zero bounds.
5. At least three spatial layers: occluder, illuminated contact/trace, receiving field relationship.
6. Gold surface area must remain minor relative to Ink Black and negative space.
7. No parallel decorative ray bundle.
8. Must export independently with transparent background.
9. Doré must inspect the exported render before PASS.
10. MCP/tool success alone cannot satisfy any visual criterion.

## PASS gate

LIGHT-01 is not PASS until: Penpot render is visible; independent export is non-empty; visual inspection confirms source/direction/occlusion/depth; the asset works on Living Paper without a display card; and human review accepts it as a usable Westside website visual asset.
