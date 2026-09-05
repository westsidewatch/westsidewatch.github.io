# DORÉ IMAGE → DESIGN NATIVE PLACEMENT EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_EVIDENCE_RECONCILED
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Related work: `CAPABILITY-RUNTIME`, `VIS-GRAMMAR`, Doré Image, Doré Design, A2A control plane
P01 impact: NONE

## Bounded evidence reviewed

- commit `dcb99d2b99e161f7f390c2fef99ef0ded7586e27` — resident Doré Design promoted from synthetic to the first concrete A2A production consumer;
- commit `48e0f326dac3f0374abbaddbba5b0656108f18ea` — renderer-neutral `DesignAsset` / `DesignImageShape` state and lightweight-canvas knowledge retained in Doré visual core;
- commit `1b1cf9416d9862443b91c157d9c31a92744df137` — native image asset/node support, direct generated-image placement into Doré Design workspace, deterministic rendering/verification and removal of the one-shot migration helper/workflow;
- current sparse-capability runtime canonical addendum;
- current GitHub receipt surface for the bounded commits.

## What is now legitimately complete as a bounded submilestone

### Native Image → Design state contract
`VERIFIED_COMPLETE_SUBMILESTONE / REPOSITORY_IMPLEMENTATION`

Doré now has a concrete renderer-neutral state path:

`generated image artifact → DesignAsset → DesignImageShape → Doré Design workspace → deterministic SVG/render verification`

Generated images no longer need to cross an implicit/manual download-upload boundary to become design content. Image assets are first-class workspace records with identity/provenance, and image placement is a normal Design shape referencing `asset_id`.

### Resident Design production-consumer promotion
`VERIFIED_COMPLETE_SUBMILESTONE / REPOSITORY_IMPLEMENTATION`

The A2A/capability runtime now registers resident Design handlers that fail closed for real mutations when the Mac Design service is unavailable, require workspace revision advance, and read real `/api/verify` output after mutation. Synthetic Design behavior remains available only where appropriate for non-resident/offline compatibility.

## Architecture retained

The mature visual-core rule is now explicit:

- Doré workspace/application state is the source of truth;
- asset identity and shape geometry are separate;
- images are ordinary design shapes after acceptance;
- canvas/interaction engines are replaceable projections, not the stored design model;
- deterministic export/verification remains separate from interactive canvas rendering;
- manual Image→Design file transfer and prose-based separate-agent handoff are rejected directions.

This is durable capability knowledge, not merely a one-product patch.

## Supersession / retirement judgments

1. **Manual generated-image download/upload between Doré Image and Doré Design** — `SUPERSEDED` as the governing design path.
2. **Renderer-owned persistent state (Konva/tldraw/Polotno/ComfyUI as Doré design truth)** — `SUPERSEDED / REJECTED_DIRECTION`.
3. **One-shot native image workspace migration helper/workflow** — `RETIRED-AS-ACTION` after the target workspace capability was incorporated and the helper/workflow removed in the merged implementation.
4. **Synthetic Design as the production visual consumer** — `SUPERSEDED` for resident Design mutations; retained for bounded offline/non-mutating compatibility where explicitly required.

## Evidence boundary

This batch does **not** prove:

- a real resident Image provider generated a purpose-built Westside asset;
- real vision observations judged that asset;
- critic/correction/regeneration occurred on real pixels;
- a real accepted asset was automatically placed into the live Mac Design workspace and visually approved there;
- sustained Image→Design runtime reliability;
- whole-system A2A, Companion, sparse-capability, VIS-GRAMMAR or Brand completion.

The code/tests and merged architecture are strong implementation evidence, but the current bounded commit surfaces do not provide persisted live-runtime acceptance sufficient for those stronger claims.

## Current quality judgment

This is a material improvement over the earlier handoff architecture because it removes an artificial human/file-transfer seam and preserves durable identity/provenance through Design. It also protects replaceability by keeping the canonical workspace independent of the future interactive canvas engine.

The remaining weakness is real-media acceptance. The next high-value proof is not another abstraction: it is one real purpose-built Westside asset completing the entire live loop.

## Smallest useful next proof

Use one purpose-built Doré-derived Westside asset—prefer a **light texture** or **Bethlehem-star website grammar asset**, not an original Doré artwork—and persist:

1. real local/resident generation;
2. durable fetched bytes + checksum/provenance;
3. real vision observations;
4. critic judgment and at least one correction iteration if required;
5. accepted artifact identity;
6. automatic native placement into Doré Design;
7. workspace revision advance + deterministic verification/readback;
8. before/after visual acceptance evidence.

That packet would verify the real Image→Design visual-production loop as a bounded milestone, not Brand V1 or whole-system visual completion.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified.
