# Doré Image Roadmap

Status: ACTIVE

## M0 — Project establishment

Acceptance:

- project mission exists;
- research baseline exists;
- architecture and schemas exist;
- Doré Image skill entry point exists;
- renderer is explicitly separated from style grammar;
- Foundation acceptance gate is defined.

Target status after merge: `M0 COMPLETE / FOUNDATION ACTIVE`.

## M1 — Renderer reconnaissance

Goal: determine what Doré can actually execute on the resident Mac without asking the user to become a terminal operator.

Tasks:

- detect Mac architecture, RAM, available storage and current Python/runtime state;
- test ComfyUI feasibility;
- test a minimal diffusers path where feasible;
- inventory already-installed image tooling;
- identify a no-metered-cost default renderer path;
- record model licenses and hardware limits;
- expose one resident callable render command/API.

Acceptance:

- Doré can invoke one renderer through a stable local adapter;
- a generated image can be returned to Doré for inspection;
- run metadata and output hash persist;
- no paid API is required for the acceptance run.

## M2 — Doré Original Spec Compiler

Goal: convert Doré's existing visual knowledge into executable style systems.

First style families:

1. `DORÉ / SCRIPTURE PLATE`;
2. `DORÉ / FIRST LIGHT`;
3. `DORÉ / FIELD NOTE`;
4. `DORÉ / WEB ELEMENT`.

Tasks:

- study accepted Westside / ONE visual work and current visual constitution;
- build machine-readable palette, material, space, type/image, light and texture catalogs;
- build a style-spec compiler;
- define stable defaults and allowed variation;
- define originality firewall;
- define thumbnail/product-fit checks.

Acceptance:

- same brief + same family resolves to a stable manifest;
- different subjects produce different compositions without losing family identity;
- family spec can drive more than one renderer.

## M3 — Generate / See / Correct loop

Goal: stop treating image generation as one-shot prompt execution.

Tasks:

- generate 3 candidates;
- load candidates back into Doré's vision/inspection path;
- score against explicit critique schema;
- preserve strengths and target blocking defects;
- regenerate or edit;
- persist accept/reject reasons.

Acceptance:

- one real task includes at least one automatic correction cycle;
- the accepted candidate scores higher on the stated defect than its predecessor;
- correction evidence is persisted.

## M4 — Control layer

Goal: art direction by structure rather than prompt luck.

Tasks:

- reference-image adapter;
- edge/line control;
- depth/pose control where relevant;
- inpaint/outpaint;
- subject/crop preservation;
- responsive safe-area controls.

Acceptance:

- a controlled output preserves requested structural constraints across retries;
- Doré can explain which control source caused which retained feature.

## M5 — Web Element pipeline

Goal: Doré can make site-native visual components, not only flat poster images.

Tasks:

- transparent-background assets;
- responsive desktop/mobile crops;
- VTracer or equivalent raster-to-vector path;
- SVG cleanup/rebuild;
- direct SVG-native generation for simple elements;
- safe-area and focal-anchor metadata;
- asset naming/versioning.

Acceptance:

- one real Westside/ONE page receives a Doré-created visual element;
- desktop/mobile behavior passes visual verification;
- element remains editable when vector output is appropriate.

## M6 — First real product graduation

Candidate first acceptance task: a bounded ONE or New Westside visual element selected from current production needs.

Required chain:

`brief -> Doré spec -> 3 candidates -> critique -> correction -> accepted asset -> Doré Design/site insertion -> responsive verification -> learning retention`.

Acceptance:

- full chain executes;
- user/product acceptance is recorded;
- accepted recipe can generate a second related asset without restating the entire style manually.

At this point Doré Image may move from `ACTIVE FOUNDATION` to `WORKING PRODUCT FOUNDATION`.

## M7 — Style memory and transfer

Goal: Doré learns from accepted work rather than accumulating random references.

Tasks:

- store accepted manifests and critiques;
- create visual exemplar index;
- link product context and outcome;
- test cross-subject transfer;
- identify drift patterns;
- refine selection heuristics.

Acceptance:

- at least three accepted outputs across two subjects in a family;
- later runs improve or remain stable without user re-teaching the family.

## M8 — Adapter/LoRA decision gate

Train a Doré-specific LoRA or equivalent only if M7 evidence shows visual identity cannot be retained reliably with style specs, references and control adapters alone.

Before training:

- dataset provenance must be clean;
- rights status must be recorded;
- accepted-output corpus must be sufficient;
- baseline without training must be measured;
- success metric must be defined.

No training project exists merely because LoRA is fashionable.

## M9 — Mature Doré Image

Long-term capability:

- Doré chooses between SVG-native, deterministic image processing and generative rendering;
- Doré selects/compiles style grammars;
- Doré generates, sees, critiques and corrects;
- Doré makes production-ready web/editorial assets;
- Doré retains successful decisions as reusable visual capability;
- renderer/model changes do not erase Doré's visual identity.
