# DORÉ IMAGE / 多雷製圖 FOUNDATION — 2026-09-05

Status: ACTIVE_PARALLEL / FOUNDATION ESTABLISHED
Parent: Doré Core + Doré Design
P01 impact: NONE

## Trigger

Repeated Doré visual/image discussions and prior study of external design resources did not produce a dedicated image-generation project. The missing boundary was projectization: without a persistent capability contract, renderer path, acceptance gate and learning ledger, visual research could not graduate into Doré-controlled image production.

The 2026-09-05 review of `yanliudesign/mono-color-skill` made the missing architecture explicit: a visual style can be represented as an executable skill/grammar rather than as an informal prompt or design conversation.

## Project established

Canonical project directory: `dore-image/`.

Foundation artifacts:

- `dore-image/PROJECT.md` — mission, product boundary and acceptance gate;
- `dore-image/RESEARCH-FOUNDATION-2026-09-05.md` — initial public/open research landscape;
- `dore-image/ARCHITECTURE.md` — brief/style/recipe/renderer/critic/package contracts;
- `dore-image/ROADMAP.md` — M0-M9 execution path;
- `dore-image/SKILL.md` — Doré Image skill entry point.

## Fixed goal

Doré must eventually be able to:

1. receive a real image/visual-asset need;
2. derive a visual brief itself;
3. compile a Doré-owned style grammar and recipe;
4. select an appropriate production path (SVG, deterministic processing, or generative renderer);
5. generate candidates;
6. inspect the actual outputs;
7. critique and correct them;
8. package accepted assets with provenance and placement metadata;
9. insert them into Doré Design / real site production;
10. retain successful visual decisions as transferable Doré capability.

The goal explicitly includes website design elements, not only standalone illustrations/posters.

## Relationship to Doré Design

Doré Design remains the structured composition/editing workspace. Its current project contract already states that full rendered aesthetic readback/correction and full Westside visual competence remain unverified.

Doré Image is created to fill the missing image-making/visual-language layer while preserving Doré Design as the final structural composition environment.

## Founding research synthesis

The first research baseline classifies public work into five mechanism families:

- style grammar and recipe systems (`mono-color-skill`, poster style-transfer/generator skills);
- planner/layout/critic orchestration (VibePoster, PosterBoy);
- renderer runtimes (ComfyUI, diffusers, agent/ComfyUI bridges);
- structural/reference control (ControlNet, IP-Adapter, newer reference-control research);
- raster/vector/web-asset conversion (VTracer plus Doré Design SVG-native path).

No single upstream project is adopted as Doré Image itself. The project integrates mechanisms behind a Doré-owned schema and acceptance loop.

## Capability boundary

Current status does **not** mean Doré can already self-generate images.

`M0` establishes the project and skill architecture only.

The first genuine capability milestone is `M1`: one resident callable renderer that Doré can invoke without requiring the user to act as terminal operator and without requiring a metered paid API for the acceptance run.

The first product graduation milestone is `M6`: a real Westside/ONE task passes the complete `brief -> spec -> candidates -> critique -> correction -> insertion -> responsive verification -> retention` chain.

Until M6 passes, the project remains `ACTIVE FOUNDATION`.

## Immediate next action

Proceed directly to M1 renderer reconnaissance after foundation merge:

- inspect resident Mac hardware/runtime;
- test ComfyUI feasibility;
- test a minimal diffusers/local path where appropriate;
- expose one resident render adapter;
- produce the first machine-inspectable generated asset and persisted renderer manifest.

Do not restart general visual research as a substitute for this execution step. New research should be pulled only when it answers a concrete M1-M6 blocker or materially improves an acceptance criterion.
