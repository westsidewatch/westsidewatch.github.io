# DORÉ IMAGE LOCAL + DESIGN INTEGRATION — EVIDENCE LEDGER

Date: 2026-09-09
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `3d2a288f1875c45c5d6df2df7690c7b1b627236f` — Search AI → resident Image command path;
- commit `2d2bacbb25afaaec9bbe7fafd8bdf55301d762bf` — `image.local.repair` production action + end-to-end generation acceptance contract;
- commits `4fb61eab410203ad28df07145c0c40c31accbac8`, `9658e5d965652dadbd11268897c4d851c6c26232`, `f35753868cc5531004a5c0fade19aafc6e29958a` — stable-diffusion.cpp adapter, installer/self-equipping, model-backed resident routing;
- commits `579d0820c7a6fcef612684a4dcf530ae3a72d87c`, `955fbf1d20b39bbabac8cb4c084b27bdc59adf32`, `f369448abdb7af0562ca2e5766ff61e479cf3594` — acceptance prompt/timeout hardening;
- commits `37e5ad28c187fdad25ef12c56d7b809adcb94410`, `287e08aa1f8d73a9ac8282323321005242b8018a`, `43896eb203503a96c4cb98428da113e788110e0f`, `1db64c2211f86f14def46ea301a1c06c36141889` — Design 2 local-image / cover-image tooling and contract.

## Classification

### Image Local substrate

Current classification: `ACTIVE_PARALLEL / IMPLEMENTED_NEEDS_PERSISTED_ACCEPTANCE_EVIDENCE`.

Repository evidence proves a real model-backed local generation implementation exists. The resident can choose ComfyUI or stable-diffusion.cpp, reports model-backed health, returns artifact hashes/metadata, and the repair action requires a raster artifact (`png/jpeg/webp`), model-backed renderer, SHA-256 and non-trivial byte size before declaring success.

This is materially stronger than the earlier native-SVG fallback milestone. The native SVG path is historical fallback/provenance and must not be treated as equivalent to model-backed image generation.

However, this bounded sweep did not find a durable persisted result object or workflow receipt proving the final model-backed acceptance command itself reached terminal PASS on the Mac. Commits that add/fix the acceptance machinery are implementation evidence, not terminal execution evidence. Therefore `VERIFIED_COMPLETE` is not justified from repository history alone.

### Search → Image path

Current classification: `ACTIVE_PARALLEL / IMPLEMENTED`.

The Search AI command path to resident Image is real implementation work. It should be retained as a reusable capability route, not mistaken for proof that visual quality, Doré style fidelity or production UX are solved.

### Design 2 cover-image integration

Current classification: `ACTIVE_PARALLEL / IMPLEMENTED_NEEDS_END_TO_END_VISUAL_PROOF`.

Design 2 has concrete local-image and cover-art controls, including editable cover image tooling and crop/placement behavior. This proves product integration work, but not the complete target chain `Design → Core → image.generate → Image Local → Artifact → Design Cover` under a persisted live acceptance with visual readback.

## Retrospective evaluation

Original objective: make Doré capable of generating local images without paid API dependency and let Doré products, especially Search and Design/Multiwrite Cover, consume those artifacts.

What was learned: local capability repair/self-equipping, model-backed renderer abstraction, artifact identity/metadata, long-running A2A execution windows, and separation between image-generation capability and design-surface placement.

Weaknesses / debt:

- terminal model-backed acceptance evidence is not durably indexed in the repository;
- visual-style quality is a separate unresolved layer from transport/render success;
- Design integration has implementation commits but lacks one canonical persisted end-to-end visual acceptance receipt;
- earlier native-SVG fallback can confuse historical continuity unless explicitly marked as superseded for quality acceptance.

Revisit trigger: when the purpose-built Westside/Doré visual asset family is generated, use that work as the first real product-quality acceptance rather than another generic test image.

Current disposition: retain and build on the implementation; do not rewrite the substrate. Add durable acceptance evidence and use the new purpose-built Doré website-asset suite as the next quality-bearing proof.

## Missing evidence

Smallest proof still needed:

1. persist one successful `image.local.repair` result showing model-backed renderer mode, raster artifact MIME, SHA-256, bytes and model metadata;
2. persist one end-to-end `Design → image.generate → Image Local → Artifact → Cover` result with the returned artifact visibly placed in the Cover canvas;
3. distinguish transport/render PASS from visual-style PASS; the latter should be evaluated against the current Westside visual grammar and purpose-built asset brief.

No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition is established by this evidence batch.