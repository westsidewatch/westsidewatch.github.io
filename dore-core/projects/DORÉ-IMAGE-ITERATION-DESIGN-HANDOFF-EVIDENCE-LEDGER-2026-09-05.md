# DORÉ IMAGE ITERATION + DESIGN HANDOFF EVIDENCE LEDGER — 2026-09-05

Status: BOUNDED_RECONCILIATION_COMPLETE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `445c87ea96c61e820beb4af3497d29471592b7e1`;
- `dore_core/capabilities/image_iteration.py` introduced by that commit;
- `dore_core/capabilities/image_handoff.py` introduced by that commit;
- `tests/test_dore_image_iteration_handoff.py` introduced by that commit;
- current sparse-capability runtime addendum and A2A/control-plane reconciliation;
- GitHub commit-associated workflow-run receipt surface for `445c87e`.

## Current classification

### Bounded Doré Image correction loop
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

Repository code now contains a bounded `generate → vision observations → critic → correction direction → regenerate` loop with an explicit iteration cap and explicit stop reasons (`accepted`, `critic-returned-no-correction`, `iteration-limit`). The vision-reader boundary is injectable rather than tied to one provider, which is compatible with the governing sparse-capability model.

### Typed Image → Design handoff
`ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE`

Repository code now contains a typed `dore.design.image-patch.v1` handoff carrying page target, stable asset identity, URI, SHA-256, geometry, fit, semantic role and provenance. The bounded test asserts asset identity/provenance continuity and rejects invalid placement geometry.

### Real visual/runtime acceptance
`ACTIVE / UNKNOWN_NEEDS_EVIDENCE`

The bounded tests use a fake renderer and a synthetic vision-reader callback. No commit-associated workflow run is persisted for `445c87e` in the available GitHub receipt surface. This is therefore implementation + unit-contract evidence, not proof of a live ComfyUI generation, Doré's real vision faculty, a real Design consumer applying the patch, or sustained CI/runtime acceptance.

## Evidence boundary

1. The implementation proves a correction-loop shape, not image-quality competence on real generated assets.
2. The iteration cap is a useful safety/cost boundary and prevents open-ended self-correction loops.
3. The handoff preserves identity/provenance through a typed structure; it does not itself prove that a downstream editor faithfully renders the asset or preserves those fields in persisted product state.
4. `vision_reader` is intentionally an explicit seam. Until a real vision faculty is connected and evaluated, synthetic callback acceptance must not be promoted into autonomous visual review competence.
5. The fake renderer makes the unit behavior deterministic but does not prove ComfyUI/provider availability, output integrity, model suitability or production cost/performance.
6. No evidence in this batch proves the purpose-built Doré visual asset suite (light, Bethlehem star, water, sky/cloud, stone/wall, city-edge, paper/stone textures) has been generated and quality-approved under the current Westside visual principles.
7. No P01 subtitle/runtime/deployment/binding/credential/audio-transcription state was modified.

## Current quality judgment

This is a materially useful architectural submilestone because it closes two previously missing seams: Doré Image can now be expressed as a bounded correction process rather than one-shot generation, and an accepted artifact can cross into Design without free-form conversational handoff or loss of identity/provenance.

The main weakness is that the contract is ahead of real visual proof. The next useful work is not another abstraction layer; it is one real purpose-built Westside asset flowing through real generation, real visual evaluation/correction and real Design application with persisted evidence.

## Durable learned principles

- Visual self-correction must be bounded and expose terminal reasons.
- The critic should consume explicit observations rather than silently coupling to one model/provider.
- Image → Design transfer should preserve stable artifact identity, checksum and provenance.
- Typed handoff is part of one persistent Doré capability runtime, not agent-to-agent conversation.
- Unit acceptance with fake providers proves contract behavior, not real visual competence.
- Purpose-built Doré-derived website assets remain distinct from curated original Doré works.

## Revisit / supersession judgment

- One-shot image generation as the default final-production model is `SUPERSEDED` for Doré Image work that requires quality acceptance; bounded correction is the stronger governing direction.
- Free-form Image → Design conversational handoff is `SUPERSEDED` where the typed patch contract applies.
- The current loop/handoff implementation is not a completed product; retain both as completed submilestones under active visual/sparse-capability runtime work.

## Smallest next proof

Persist one real acceptance packet containing:

1. one purpose-built Westside asset brief (prefer a Doré-derived light texture or Bethlehem-star asset rather than an original Doré artwork);
2. real local/provider rendering through the resident Image path;
3. real vision observations and at least one critic decision, including a correction iteration if the first output fails;
4. accepted artifact identity/checksum/provenance persisted;
5. typed `dore.design.image-patch.v1` applied by a real Design consumer to a bounded specimen;
6. before/after visual evidence and explicit acceptance judgment against current Westside visual principles;
7. CI/runtime receipt for the involved unit/integration path;
8. one negative case showing the iteration cap or invalid handoff refuses safely.

This packet should close only the Image-correction/Design-handoff acceptance boundary. It must not be treated as completion of Doré Visual, sparse runtime, VIS-GRAMMAR or Brand V1.

## P01 isolation

No P01 state or action was modified by this reconciliation.