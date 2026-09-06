# DORÉ VISUAL ASSET / SHAPE STATE EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `48e0f326dac3f0374abbaddbba5b0656108f18ea` (`Absorb lightweight canvas patterns into Doré visual core`);
- `dore-image/LEARNED-CANVAS-ARCHITECTURE.md`;
- `dore_core/capabilities/image_handoff.py`;
- `tests/test_dore_image_design_asset_shape.py`;
- current sparse capability runtime / Image→Design handoff interpretation.

## Current classification

### Renderer-neutral visual asset / shape state
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

A concrete state-boundary milestone is now implemented. Accepted generated image artifacts can compile into a durable renderer-neutral `DesignAsset` plus a normal `DesignImageShape` that references the asset by stable identity and carries canonical geometry/fit/role. The persistent representation is owned by Doré rather than a canvas engine.

### Interactive canvas engine choice
`READY / OPTIONAL IMPLEMENTATION DETAIL`

Konva is retained only as a possible interaction projection if the existing Design UI later needs richer hit-testing/drag/transform behavior. It is not Doré's storage format, brain, or canonical workspace state. No new canvas-engine adoption project should be inferred from the retained knowledge file.

## Evidence boundary

1. `DesignAsset` preserves renderer-neutral asset identity, URI, checksum and provenance.
2. `DesignImageShape` preserves canonical geometry and references `asset_id` rather than serialized renderer objects.
3. `DesignImagePatch.to_asset_and_shape()` creates both records from the accepted Image→Design handoff without a manual download/upload seam.
4. Tests verify artifact→asset/shape compilation and explicitly verify the serialized native state does not contain `konva`, `polotno` or `tldraw` identity.
5. The retained architecture keeps deterministic export separate from interactive canvas projection and requires render-time asset byte resolution.
6. The same retained rules bound memory by loading only active-page assets and preserve CORS as part of the asset contract.
7. This batch does **not** prove live interactive canvas behavior, transform normalization in a real UI, browser CORS/export acceptance, a real purpose-built Westside asset moving through the full Image critic→Design application path, or latest-head CI PASS.

## Current quality judgment

This is a strong architectural convergence step because it removes a recurring source of future lock-in: generated-media identity and layout state no longer need to inherit a specific canvas library's object model. It also makes the existing purpose-built Doré website-asset direction more implementable: light textures, Bethlehem-star variants, water/sky/wall forms and other accepted generated assets can enter Design as ordinary typed assets/shapes rather than as special-case agent output.

The weakness remains real-product acceptance. The state contract is implemented and unit-tested, but no persisted evidence in this batch proves a real generated Westside visual asset was reviewed, accepted, inserted, manipulated and deterministically exported through this path.

## Durable learned principles

- Application/workspace state is authoritative; canvas nodes are projections.
- Asset identity and shape placement are separate durable records.
- Accepted generated images become ordinary design shapes, not a second design system.
- Renderer choice remains replaceable and must not leak into persisted schema.
- Manual Image→Design download/upload is a superseded default direction.
- Deterministic export/verification remains separate from interactive canvas screenshots.
- Visual memory use should remain sparse: resolve/load visible assets on demand rather than preloading the library.

## Supersession / revisit judgment

The following directions are now explicitly `SUPERSEDED` as default architecture:

- persisting a canvas library's serialized node tree as Doré workspace truth;
- making ComfyUI, Konva, Polotno or tldraw the owner of Doré design state;
- manual generated-image download/upload between Doré Image and Doré Design;
- treating Image and Design as separate prose-conversing intelligences.

Do not retire SVG/deterministic export or the current Design UI. Revisit the interaction-engine choice only when a concrete production manipulation gap exists.

## Smallest next proof

Use one real purpose-built Westside asset—prefer a Doré-derived light texture or Bethlehem-star grammar—and persist:

1. real generation and durable bytes/checksum/provenance;
2. real visual observations and critic decision;
3. correction/regeneration if required;
4. accepted `DesignAsset` + `DesignImageShape` identity;
5. actual Design insertion and geometry manipulation;
6. deterministic export/render verification;
7. before/after acceptance evidence;
8. proof that renderer-specific objects do not become persistent workspace state.

## P01 isolation

No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state, ordering or blocker was modified by this reconciliation.
