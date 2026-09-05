# Doré Image / 多雷製圖

Status: ACTIVE FOUNDATION
Established: 2026-09-05
Parent system: Doré Core
Runtime faculty: Doré Visual

## Mission

Doré Image is the engineering project that builds Doré's native image-generation capability. It is not a second Doré, a separate visual agent, or a peer intelligence that must converse with Doré Design.

The fixed goal is not merely to call an image model. The fixed goal is for one Doré to understand a visual brief, form an original design grammar, generate or transform imagery, inspect the result, correct it, compose it into structured design, and deliver reusable production assets into real Westside Watch / ONE products.

The terminal capability target is:

> Doré can independently generate original images and website design elements from an intent or product need, while preserving Doré/Westside visual identity, source truth, editability where appropriate, and machine-verifiable production evidence.

## Project boundary is not an intelligence boundary

Doré Core already defines Doré as one persistent intelligence with bounded faculties and adapters, and explicitly states that faculties are not independent agents. The reflex layer already defines the transferable route `STIMULUS -> INTENT -> ROUTE -> EVIDENCE -> OUTCOME -> REFLEX UPDATE`.

Therefore Doré Image and Doré Design remain separate engineering workstreams only where separate code, tests, release discipline or runtime machinery is useful. At runtime they are capabilities of one `visual` faculty.

Normal visual execution must not use a free-form Image-agent <-> Design-agent conversation loop.

Instead:

`product need -> visual intent -> style grammar -> image generation/control -> image critique -> structured composition -> verification -> accepted asset`

All stages share typed task state and are routed by Doré's capability/reflex layer.

Canonical architecture: `dore-core/architecture/DORE-CAPABILITY-EMBODIMENT-2026-09-05.md`.

## Relationship with Doré Design

Doré Design remains a structured visual workspace and manipulation engine: editable pages/layers, shared state, SVG rendering/export, direct human/machine editing and deterministic verification.

Doré Image builds generation/control/inspection machinery that feeds the same Doré Visual faculty.

Runtime capability map:

- `visual.direct` — product/creative intent;
- `visual.grammar` — Doré visual grammar/style recipe;
- `image.generate` — raster/illustrative generation;
- `image.control` — reference/pose/depth/line/inpaint control;
- `image.critic` — visual inspection and diagnosis;
- `design.compose` — structured Doré Design manipulation;
- `design.typography` — hierarchy/type behavior;
- `design.svg` — native vector/site element generation;
- `design.verify` — structural/render/responsive checks;
- `asset.publish` — accepted asset registration/provenance.

These are Doré capabilities, not mini-agents.

## Founding observation

The immediate external starting point is `yanliudesign/mono-color-skill`.

Its important contribution is architectural rather than stylistic: it turns a recognizable visual language into explicit, machine-readable decisions such as subject, intent, representation, palette, plate roles, composition, negative space, focal event, type hierarchy, image treatment, controlled imperfection and originality checks.

Doré Image adopts this principle:

> Style is not a prompt adjective. Style is an executable design system.

Doré Image must therefore learn from mature public work, extract transferable mechanisms, and re-express them as Doré-owned grammars rather than accumulating copied prompts or named-style imitation.

## Non-negotiable product principles

1. **One Doré.** Image and design are faculties/capabilities of one persistent intelligence.
2. **Sparse activation.** Image/design instructions, models and provider schemas stay dormant until routed to a visual task.
3. **Typed state, not conversational handoff.** Normal stages exchange `VisualBrief`, `StyleRecipe`, `AssetCandidate`, `CritiqueResult`, `DesignPatch` and `VerificationResult`, not recursive agent chat.
4. **Original grammar, not style mimicry.** References are evidence and grammar sources, never templates to reconstruct.
5. **Renderer-agnostic core.** Doré's visual reasoning and recipe manifest must not be hard-wired to one image model or provider.
6. **Local/free path first where practical.** The base project must not require metered AI/API spending for normal experimentation. Optional render adapters may exist separately.
7. **Generation is only one stage.** Every run must support inspect -> critique -> revise -> accept/reject.
8. **Real product transfer is the graduation test.** A beautiful isolated demo is not enough; assets must survive insertion into Westside Watch / ONE / Journal / book / site production.
9. **Website elements are first-class outputs.** Hero art, section illustrations, ornaments, textures, separators, icon-like marks, background plates and responsive crops belong to the capability family alongside posters/editorial images.
10. **Structured/vector output when appropriate.** Raster generation may provide visual material, but SVG/vector reconstruction or direct structural composition should be preferred for marks, ornaments, dividers and reusable site elements.
11. **Evidence before capability promotion.** A technique becomes a Doré capability only after repeatable real-work evidence.
12. **Projects train; capabilities remain.** When this project produces a verified transferable ability it must graduate into Doré's capability registry/reflex routing so the active project machinery need not remain in every future task.

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

`Doré Original` is the first native style-system family to be developed inside Doré Image and ultimately retained as Doré Visual capability.

It is not defined as "make it look like Gustave Doré" and it is not a single locked appearance. It is a family of reusable visual grammars built from Doré's own product history, Westside visual constitution, ONE, Journal, publishing work, biblical-world research and controlled study of public design/print systems.

The first subfamilies to validate are:

- `DORÉ / SCRIPTURE PLATE` — monumental biblical/editorial imagery, engraved line logic, light architecture, restrained accent color and typographic collision;
- `DORÉ / FIRST LIGHT` — Westside/Journal image language using stone/paper, first-light gold, night-to-dawn tonal structure and strong negative space;
- `DORÉ / FIELD NOTE` — maps, objects, specimens, historical notes and research imagery;
- `DORÉ / WEB ELEMENT` — reusable website visual assets with transparent/raster/SVG variants and responsive crop contracts.

These names are internal product families, not claims of artistic authorship by historical artists.

## Output/state contract

A mature Doré Visual run should persist only the typed artifacts required by later stages:

```text
VisualBrief
  -> StyleRecipe
  -> AssetCandidate[]
  -> CritiqueResult
  -> accepted AssetCandidate
  -> DesignPatch
  -> VerificationResult
  -> AssetRecord
```

Each artifact must have an ID, schema version, provenance and content hash. Each capability reads only the fields it requires.

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

Doré Image Foundation is not complete until one real product task proves the entire chain inside one Doré capability route:

1. Doré receives a concrete Westside Watch / ONE visual need.
2. The reflex/router activates the minimal Doré Visual capability set; unrelated capability bodies remain unloaded.
3. Doré selects or builds a visual grammar without the user writing the production prompt.
4. Doré produces at least three candidates through a callable renderer.
5. Doré inspects and scores the candidates.
6. Doré performs at least one evidence-driven correction.
7. Doré accepts one asset and rejects the others with recorded reasons.
8. The accepted asset enters Doré Design/the website through shared typed state, without a free-form inter-agent handoff.
9. Responsive/export behavior is verified.
10. Recipe and learning evidence are retained for transfer.
11. A second comparable task demonstrates lower cognitive/runtime overhead through reuse or reflex compilation.

Until that gate passes, status remains `ACTIVE FOUNDATION`.
