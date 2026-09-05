---
name: dore-image
description: Doré's image-making and website-visual-asset skill. Use when a Doré/Westside/ONE task needs original imagery, a visual style system, reference-guided generation, image transformation, illustration, poster/editorial art, hero art, texture, ornament, background, responsive visual asset, or raster/vector web element. Compile a visual brief and Doré style recipe first; never reduce the task to a style adjective or one-shot prompt.
---

# Doré Image / 多雷製圖

## Purpose

Turn a real product need into an original, inspectable, repeatable visual asset.

The skill owns:

`brief -> style grammar -> recipe -> structure -> render -> inspect -> correct -> package -> product insertion evidence`

It does not own final page layout when Doré Design is structurally better suited to the job.

## Operating rule

Before invoking any image renderer, decide whether the task should instead be made directly as structured SVG/layers in Doré Design.

Use this order:

1. direct SVG/structured design if geometry is sufficient;
2. deterministic local image processing if a source image only needs treatment;
3. generative rendering only when semantic/illustrative generation is needed.

## Required run manifest

Every non-trivial run resolves:

```yaml
brief:
  product: <product>
  surface: <surface>
  intent: <intent>
  subject: <subject>
  required_text: []
  references: []
  ratio_targets: []
  vector_preference: <required|preferred|none>
style:
  family: <Doré family or explicit external study>
  visual_thesis: <one sentence>
  palette: <roles>
  line_language: <rule>
  material_language: <rule>
  space_rule: <rule>
  light_rule: <rule>
  type_relationship: <rule>
recipe:
  focal_event: <one event>
  release_zone: <quiet region>
  crop_rule: <rule>
  control_inputs: []
  responsive_derivatives: []
  vectorization: <none|trace|rebuild>
renderer:
  adapter: <available adapter or unresolved>
```

If the renderer is unresolved, do not pretend an image was generated. Produce the manifest and continue renderer reconnaissance as an engineering task.

## Doré Original families

Initial experimental families:

- `DORÉ / SCRIPTURE PLATE`
- `DORÉ / FIRST LIGHT`
- `DORÉ / FIELD NOTE`
- `DORÉ / WEB ELEMENT`

A family is a grammar, not a prompt phrase. Read the family catalog once it exists and preserve its rules across retries.

## Reference handling

Use references to extract transferable visual rules:

- composition geometry;
- hierarchy;
- palette relationships;
- line/material behavior;
- crop/negative-space logic;
- image/type interaction;
- controlled irregularity.

Do not reconstruct unique reference content, logos, signatures, proprietary characters or exact layouts. Replace theme-specific content and change structural variables while retaining only the generalized grammar.

## Candidate protocol

For real production work, default to three candidates unless cost/resource limits justify fewer.

Candidates must vary through bounded structural choices, not random style drift. Preserve stable manifest decisions unless exploration is explicitly requested.

## Critique protocol

Inspect the actual candidate asset before acceptance.

Score:

- brief accuracy;
- subject fidelity;
- hierarchy;
- style coherence;
- product fit;
- technical quality;
- originality.

Record blocking defects. A candidate with a blocking defect cannot pass because the overall impression is attractive.

For `REVISE`, preserve named strengths and target only the defects unless a new concept is required.

## Website asset protocol

For website surfaces, additionally test:

- desktop and mobile crop survivability;
- focal anchor;
- text-safe area;
- transparent-background need;
- file size/performance;
- SVG/vector suitability;
- dark/light background compatibility where relevant.

Do not embed important factual text inside generated raster art if Doré Design/HTML can render it structurally.

## Retention

Only accepted real-product outputs become Doré learning evidence.

Retain:

- brief;
- style spec;
- recipe;
- renderer manifest;
- accepted/rejected candidate reasons;
- correction history;
- final asset hashes;
- placement metadata;
- product outcome.

Do not learn a style rule merely because it appeared in an unaccepted generated image.

## Foundation limitation

As of project establishment, Doré Image is `ACTIVE FOUNDATION`. The skill architecture exists, but self-generation is not a verified capability until M1 supplies a callable renderer and M6 proves the full real-product loop.
