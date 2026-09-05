# Doré Image Research Foundation — 2026-09-05

Status: ACTIVE RESEARCH BASELINE
Purpose: identify mature public mechanisms worth digesting into Doré Image.

## Research rule

This project does not copy a repository wholesale merely because its outputs look good. Each source is evaluated for one or more reusable mechanisms:

- visual grammar representation;
- reference/style extraction;
- composition planning;
- renderer orchestration;
- structural control;
- self-critique/correction;
- vector/web asset production;
- provenance/reproducibility;
- license and operational fit.

When an upstream project is incorporated, Doré must retain attribution/license information and separate copied code from reimplemented ideas.

## A. Founding style-system references

### 1. yanliudesign/mono-color-skill

Role: primary starting point.

Key mechanisms to digest:

- style as an explicit executable grammar rather than a prompt adjective;
- machine-readable recipe manifest;
- design-system catalogs for color, typography, composition, carriers and rhythm;
- deterministic defaults;
- explicit negative-space and focal-event decisions;
- originality firewall: references are grammar, not templates;
- output includes image + production prompt + recipe.

Doré judgment: **ADOPT ARCHITECTURAL PATTERN / DO NOT COPY HOUSE STYLE AS DORÉ IDENTITY.**

License: MIT at the reviewed repository revision.

### 2. jiemianduan/poster-style-transfer

Role: reference grammar extraction.

Key mechanisms:

- extract reusable Poster Style Spec;
- distinguish hard locks, soft locks and replaceable content;
- transfer layout/type/color/hero/texture rules while replacing proprietary or theme-specific content;
- variable templates and fidelity rubric.

Doré judgment: **HIGH-VALUE INPUT for a general `style-spec` compiler.**

License: MIT at the reviewed repository revision.

### 3. howardz27/poster-generator-skill

Role: brief-to-production orchestration.

Key mechanisms:

- source -> analysis -> structured content -> prompt -> rendered output audit trail;
- content-density and channel-aware composition;
- renderer-agnostic skill architecture;
- multiple aspect ratios and multilingual handling.

Doré judgment: **ADOPT WORKFLOW/AUDIT IDEAS; avoid poster-only product framing.**

License: MIT at the reviewed repository revision.

### 4. jas0nh/zine-poster-skill

Role: controlled editorial channels and reference preservation.

Key mechanisms:

- isolated visual channels so contracts do not leak between styles;
- faithful-photo vs semantic-distillation modes;
- provider-agnostic generation contracts;
- explicit upstream-license ledger.

Doré judgment: **USEFUL for style-family isolation and provenance discipline.**

## B. Agentic design and critique references

### 5. l1anch1/VibePoster

Role: multi-agent design pipeline.

Observed architecture:

`User Input -> Planner -> Visual -> Layout -> Critic -> Poster`, with intent parsing, RAG/brand context, image generation/understanding, layout commands and rejection/retry.

Doré judgment: **HIGH-VALUE for planner/critic separation and brand-context retrieval.** Doré Image should not need its full stack or PSD-centric product shape.

### 6. ckryptickunal/PosterBoy

Role: autonomous design direction and correction loop.

Observed architecture includes separate vision, creative-direction, copy, typography, layout and critique roles.

Doré judgment: **USEFUL as evidence that generation quality improves when visual understanding, art direction, typography and critique are separate decisions.** Avoid unnecessary agent proliferation; Doré may implement roles as stages instead of literal agents.

## C. Rendering/orchestration layer

### 7. ComfyUI

Role: local node-based generative renderer and workflow runtime.

Doré use:

- candidate local/free renderer adapter;
- reusable workflow graphs;
- model/control adapters can be swapped without changing Doré visual grammar;
- supports image generation, image-to-image, inpainting and control ecosystems.

Doré judgment: **PRIMARY renderer-runtime candidate for local experiments**, subject to actual Mac hardware/resource acceptance.

### 8. NeoAnthropocene/comfyui-mcp-multiagent

Role: agent-to-ComfyUI bridge.

Key mechanisms observed publicly:

- high-level `generate_image`;
- ControlNet-conditioned generation;
- IP-Adapter reference guidance;
- asset viewing;
- regeneration with parameter overrides;
- remote or local ComfyUI targeting.

Doré judgment: **VERY HIGH-VALUE integration reference** because it closes `agent -> generate -> inspect -> regenerate` without forcing Doré to manipulate raw ComfyUI graphs for every request.

### 9. Hugging Face diffusers

Role: Python-native model/pipeline abstraction.

Doré use:

- alternative renderer adapter for deterministic scripted pipelines;
- useful for tests, model research and environments where ComfyUI is too heavy or indirect.

Doré judgment: **SECONDARY CORE ADAPTER**, especially for reproducible automated tests.

## D. Reference/structure control

### 10. ControlNet family

Role: structure-preserving generation from pose, depth, edges, normals, line art and similar conditions.

Doré judgment: **FOUNDATIONAL** for website/product imagery because art direction must control geometry rather than rely on prompt luck.

### 11. IP-Adapter / reference-image adapters

Role: image-prompt/reference guidance for subject/style composition.

Doré judgment: **FOUNDATIONAL** for learning and transferring a Doré-owned visual grammar across new subjects without rebuilding a model for every task.

### 12. thedeoxen/refcontrol

Role: newer reference + structure fusion for FLUX-family pipelines.

Observed mechanism: preserve identity/style from a reference while following pose/depth/lineart/canny/normal control.

Doré judgment: **RESEARCH TRACK**, valuable because reference and structure control need to coexist. Do not make Foundation depend on one young model family.

### 13. LoRA / adapter personalization research

Relevant directions include CRAFT-LoRA, LoRAShop and other recent content/style personalization work.

Doré judgment: **PHASE-2+**. First prove that a Doré style grammar plus reference/control adapters can deliver repeatable product quality. Train a Doré-specific LoRA only if evidence shows prompt/spec/reference control cannot hold the visual identity reliably.

## E. Raster-to-vector and web-element track

### 14. VTracer

Role: raster-to-vector conversion.

Doré use:

- convert generated flat marks, ornaments, silhouettes and line graphics into editable SVG candidates;
- post-process before insertion into Doré Design.

Doré judgment: **HIGH-VALUE for WEB ELEMENT pipeline.** Generated vector output still requires structural cleanup and visual inspection.

### 15. SVG-native generation inside Doré Design

Role: direct structural design for simple geometry.

Doré judgment: **PREFERRED over diffusion for simple web elements.** Lines, frames, dividers, typographic shapes, light beams, geometric marks and many ornaments should be generated as SVG/layers directly. Image generation should be used only when painterly/illustrative complexity warrants it.

## F. Immediate synthesis

Doré Image should not be a monolithic image model. The mature architecture suggested by the research is:

```text
Intent / real product need
        ↓
Doré visual brief
        ↓
Style Spec + Recipe Manifest
        ↓
Composition / structure plan
        ↓
Renderer selection
  ┌─────┼─────────────┐
  │     │             │
ComfyUI Diffusers   SVG-native
  │     │             │
  └─────┼─────────────┘
        ↓
Candidate assets
        ↓
Vision inspection + product-fit critic
        ↓
Correction / regenerate / vectorize
        ↓
Accepted asset package
        ↓
Doré Design / website integration
        ↓
Real-product verification
        ↓
Learning retention
```

## G. Research priorities

### Priority 0 — now

- convert `mono-color-skill` architectural lessons into Doré's own generic style-spec and recipe schema;
- establish `Doré Original` as a style family, not a single prompt;
- establish renderer-adapter boundary;
- establish image critique/retry evidence format;
- establish web-element output contract.

### Priority 1 — first working render

- detect available local Mac hardware and feasible model/runtime;
- choose smallest practical free/local render path;
- build one ComfyUI or diffusers adapter;
- run a real ONE/Westside asset task;
- insert accepted output into Doré Design.

### Priority 2 — control and repeatability

- reference-image style guidance;
- ControlNet/line/depth/pose path;
- inpainting/outpainting;
- responsive crop generation;
- VTracer/SVG cleanup;
- candidate scoring and automated correction rules.

### Priority 3 — native Doré visual memory

- build example/decision corpus only from accepted Doré outputs and rights-safe references;
- compare style-spec transfer across unrelated subjects;
- evaluate whether LoRA training materially improves identity consistency;
- if justified, train and version a Doré-specific adapter with explicit dataset provenance.

## H. Explicit exclusions for Foundation

Do not:

- make paid API access a prerequisite;
- bind Doré Image to one vendor/model;
- define Doré Original as imitation of one living or historical illustrator;
- equate a prompt library with a visual system;
- claim self-generation before Doré can actually call a renderer;
- promote a visual style merely because a single attractive sample exists;
- flatten all website graphics into AI-generated raster images when SVG is structurally superior.
