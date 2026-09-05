# Doré Image / 多雷製圖

Status: ACTIVE FOUNDATION
Established: 2026-09-05
Parent system: Doré Core + Doré Design

## Mission

Doré Image is Doré's self-owned image-generation and visual-asset capability.

The fixed goal is not merely to call an image model. The fixed goal is for Doré to understand a visual brief, form an original design grammar, generate or transform imagery, inspect the result, correct it, and deliver reusable production assets into Doré Design and real Westside Watch / ONE products.

The terminal capability target is:

> Doré can independently generate original images and website design elements from an intent or product need, while preserving Doré/Westside visual identity, source truth, editability where appropriate, and machine-verifiable production evidence.

## Why this is a separate project

Doré Design already provides a shared structured workspace, SVG rendering/export, machine inspection and a human/machine editing surface. That is the design workspace and composition engine.

Doré Image is the image-making engine and visual-language compiler that Doré Design does not itself provide.

The two systems therefore have separate responsibilities:

- **Doré Image:** visual brief -> visual grammar -> generation/control -> image critique -> approved image/asset package.
- **Doré Design:** approved asset package + typography/layout/data -> structured editable composition -> render/export/verification.

Doré Image must integrate with Doré Design, not replace it.

## Founding observation

The immediate external starting point is `yanliudesign/mono-color-skill`.

Its important contribution is architectural rather than stylistic: it turns a recognizable visual language into explicit, machine-readable decisions such as subject, intent, representation, palette, plate roles, composition, negative space, focal event, type hierarchy, image treatment, controlled imperfection and originality checks.

Doré Image adopts this principle:

> Style is not a prompt adjective. Style is an executable design system.

Doré Image must therefore learn from mature public work, extract transferable mechanisms, and re-express them as Doré-owned grammars rather than accumulating copied prompts or named-style imitation.

## Non-negotiable product principles

1. **Original grammar, not style mimicry.** References are evidence and grammar sources, never templates to reconstruct.
2. **Renderer-agnostic core.** Doré's visual reasoning and recipe manifest must not be hard-wired to one image model or provider.
3. **Local/free path first where practical.** The base project must not require metered AI/API spending for normal experimentation. Optional render adapters may exist separately.
4. **Generation is only one stage.** Every run must support inspect -> critique -> revise -> accept/reject.
5. **Real product transfer is the graduation test.** A beautiful isolated demo is not enough; assets must survive insertion into Westside Watch / ONE / Journal / book / site production.
6. **Website elements are first-class outputs.** Hero art, section illustrations, ornaments, textures, separators, icon-like marks, background plates and responsive crops belong to the project alongside posters and editorial images.
7. **Structured/vector output when appropriate.** Raster generation may provide visual material, but SVG/vector reconstruction or direct structural composition should be preferred for marks, ornaments, dividers and reusable site elements.
8. **Evidence before capability promotion.** A technique becomes a Doré capability only after repeatable real-work evidence.

## Initial capability classes

- text-to-image;
- reference-guided image generation;
- style-system extraction;
- image-to-image transformation;
- composition/pose/edge/depth control;
- inpainting/outpainting;
- limited-palette editorial and print treatments;
- engraving/linework/halftone/risograph families;
- responsive website asset generation;
- raster-to-vector extraction and cleanup;
- SVG-native ornaments and structural graphics;
- image critique and self-correction;
- visual recipe persistence and reproducibility.

## Doré Original

`Doré Original` is the first native style-system family to be developed inside Doré Image.

It is not defined as "make it look like Gustave Doré" and it is not a single locked appearance. It is a family of reusable visual grammars built from Doré's own product history, Westside visual constitution, ONE, Journal, publishing work, biblical-world research and controlled study of public design/print systems.

The first subfamilies to validate are:

- `DORÉ / SCRIPTURE PLATE` — monumental biblical/editorial imagery, engraved line logic, light architecture, restrained accent color and typographic collision;
- `DORÉ / FIRST LIGHT` — Westside/Journal image language using stone/paper, first-light gold, night-to-dawn tonal structure and strong negative space;
- `DORÉ / FIELD NOTE` — maps, objects, specimens, historical notes and research imagery;
- `DORÉ / WEB ELEMENT` — reusable website visual assets with transparent/raster/SVG variants and responsive crop contracts.

These names are internal product families, not claims of artistic authorship by historical artists.

## Output contract

A mature Doré Image run should be able to persist:

```text
brief/source
  -> analysis
  -> style-spec / recipe-manifest
  -> render-adapter manifest
  -> candidate assets
  -> critique/evaluation
  -> correction history
  -> accepted asset package
  -> Doré Design insertion metadata
```

The accepted asset package should include, where relevant:

- raster master;
- transparent-background variant;
- responsive crops;
- SVG/vector derivative or trace when appropriate;
- palette and typography-role metadata;
- source/reference provenance;
- generation recipe;
- model/adapter/version metadata;
- originality and product-fit review;
- intended placement and safe-area data.

## Foundation acceptance gate

Doré Image Foundation is not complete until one real product task proves the entire chain:

1. Doré receives a concrete Westside Watch / ONE visual need.
2. Doré selects or builds a visual grammar without the user writing the production prompt.
3. Doré produces at least three candidates through a callable renderer.
4. Doré inspects and scores the candidates.
5. Doré performs at least one evidence-driven correction.
6. Doré accepts one asset and rejects the others with recorded reasons.
7. The asset enters Doré Design or the website as a real production element.
8. Responsive/export behavior is verified.
9. The recipe and learning evidence are retained for a later transfer test.

Until that gate passes, status remains `ACTIVE FOUNDATION`.
