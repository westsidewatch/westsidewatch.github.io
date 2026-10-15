# Living Water Engraving Grammar — v1 research and SVG contract

Status: research/specification; **v6 is the visual baseline**. This document does not authorize a silent change to the deployed illustration.

## Principle

**遠看是水勢，中看是明暗，近看是皴法。** Preserve the existing upper/lower-screen relationship, central breathing corridor, text safety and the no-figures rule. Engraving is a visual grammar, not a new narrative illustration. No raster AI image.

## Research translated into controllable geometry

| Historical technique | Observed artistic function | SVG parameter / implementation | Guardrail |
| --- | --- | --- | --- |
| Copper burin engraving / 排線 | Pressure and tool shape vary stroke thickness; close hatching increases tonal density | `burinWidthMin`, `burinWidthMax`, tapered segment width; `hatchSpacing` and `hatchAngle` | Do not scale glyphs or distort base curves; avoid uniform dark stripes |
| Crosshatching / 交叉排線 | Crossed directions build deep shadows and form | `crossHatchProbability`, `crossHatchAngleDelta`, `shadowMask` | Limit crossing to localized dark pockets, not text-safe regions |
| Etching / 蝕刻 | Repeated etched lines establish nuanced line-based tones | `etchDensity`, `lineOpacity`, `microGapRate`, `localContrast` | Use vector line structure; do not simulate aquatint as a flat opaque overlay |
| Aquatint tonal logic | Fine grain creates a wash-like tonal field | `tonalField(x,y)` drives *line density/width/opacity*, not a solid gradient | No flat fog masking the engraving |
| 披麻皴 | Long, gently irregular parallel strokes describe volume and direction | `fiberLength`, `fiberCurvature`, `fiberAlignment`, `fiberBreakRate` | Follow local flow tangent; no random mountain texture |
| Chinese water-line brushwork / 水紋 | Rhythm, compression, release, and void suggest current | `flowAmplitude`, `flowWavelength`, `convergence`, `eddyStrength` | Main currents remain readable at small scale |

Sources: The Met, *Engraving* (https://www.metmuseum.org/it/perspectives/materials-and-techniques-printmaking-engraving); The Met, *The Printed Image in the West: Engraving* (https://www.metmuseum.org/de/essays/the-printed-image-in-the-west-engraving); National Palace Museum, *董源《夏口待渡圖》* (https://digitalarchive.npm.gov.tw/Collection/Detail/15658?dep=P); National Palace Museum, *巨然《層巖叢樹圖》* (https://digitalarchive.npm.gov.tw/Collection/Detail/14441?dep=P). Historical descriptions support technique analogies, **not** the numerical defaults below, which are original engineering proposals.

## Generator API (design proposal)

```ts
type EngravingParams = {
  seed: number; aspect: number;
  flowAmplitude: number; flowWavelength: number; convergence: number;
  eddyStrength: number; // 0..1; low by default
  hatchSpacing: number; hatchAngle: number;
  crossHatchProbability: number; crossHatchAngleDelta: number;
  burinWidthMin: number; burinWidthMax: number;
  etchDensity: number; localContrast: number; microGapRate: number;
  fiberLength: number; fiberCurvature: number;
  fiberAlignment: number; fiberBreakRate: number;
  centralVoidHalfHeight: number; textSafeZones: Rect[];
};
type Stroke = { d: string; width: number; opacity: number; layer: 'flow'|'tone'|'cun' };
```

**One generator, one SVG asset, one authoritative CSS reference.** All strokes derive from the same deterministic flow field; no separate independently scaled background layers.

```js
const tangent = normalize(derivative(flowField, x, y));
const local = clamp01(tonalField(x, y));
const density = lerp(densityMin, densityMax, local);
const width = lerp(burinWidthMin, burinWidthMax, local);
const opacity = lerp(opacityMin, opacityMax, local);
const cunDirection = rotate(tangent, smallSignedDeviation(seed, x, y));
const keep = !insideCentralVoid(x,y) && !insideTextSafeZone(x,y);
```

## Three viewing-distance tests

1. **Far / 水勢:** at 25% zoom or thumbnail, large-scale current should remain recognizable without becoming a dark band. Compare v6 against candidate side by side.
2. **Middle / 明暗:** at 100%, identify several coherent light/dark regions created by stroke structure, not broad painted color fields.
3. **Near / 皴法:** at 200%, observe tapered/broken fine strokes and locally aligned fiber texture; avoid noise, banding, moiré, and hairline loss.

Acceptance: same composition at full and split viewport widths; central corridor remains open; headings and scripture legible; no people/animals; no obsolete asset reference; new asset path/version when promoted; verify deployed HTML + SVG, not GitHub source alone.

## Recommended next experiment

Branch from **v6**; add a localized tonal-field / copper-burin tapered-stroke prototype first, not a wholesale redraw. Produce a separately addressable v7 candidate and compare at 25%, 100%, 200% before promotion. If any viewing-distance test regresses, keep v6.
