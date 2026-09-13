# DORÉ SHARED SCRIPTURE WORKSPACE / ARCHITECTURE FAMILY — EVIDENCE LEDGER

Date: 2026-09-13
Status: ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION / EVIDENCE-GATED
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Bounded evidence reviewed

This ledger reconciles the complete current `dore-core/architecture/` family as one bounded Sweep 01 batch:

- `architecture/CORE-CONSOLIDATION-PASS-01-SCRIPTURE-KNOWLEDGE.md`;
- `architecture/DORE-CAPABILITY-EMBODIMENT-2026-09-05.md`;
- `architecture/DORE-OPERATING-NERVOUS-SYSTEM.md`;
- `architecture/DORÉ-SYSTEM-RELATIONSHIP-MAP-v1.md`;
- `architecture/MULTIWRITE-BIBLE-NOTES-ONE-FUSION-v1.md`;
- implementation evidence in `dore-core/scripture_workspace.py`;
- `runtime/scripture-workspace-capabilities.v1.json`;
- `runtime/scripture_workspace_acceptance.py`;
- current Master Register interpretations for `EVOLUTION`, `NERVOUS-SYSTEM`, `SEARCH`, `ONE`, `MULTIWRITE-PUBLISH`, `DAWN-LIBRARY` and product-registry drift.

## Canonical architecture findings

### 1. One Doré / many products remains governing architecture

The architecture family is internally consistent on the most important system boundary:

- Doré Core owns durable cross-product semantics, memory, provenance, judgment, capability routing, permissions and verification;
- products own UX and product-local state;
- projects are temporary capability-growth programs rather than extra intelligences;
- runtimes/providers are replaceable execution substrates;
- shared faculties should communicate through typed artifacts/state rather than conversational mini-agent handoffs.

This remains `CORE/CONTINUOUS / GOVERNING_ARCHITECTURE`. It is not a closeable project and does not become complete merely because registry/runtime components exist.

### 2. Capability Embodiment is directionally active, not a completed acceptance

`DORE-CAPABILITY-EMBODIMENT-2026-09-05.md` correctly records the sparse-activation target: one Doré should activate only the minimum capability set required for a task, with deterministic/simple work compiled downward from deliberative reasoning where safe.

Later repository work materially implements parts of that direction through the Capability Registry, Reflex routing, A2A lifecycle, typed artifacts and bounded recovery. However the architecture file's own acceptance gates include resource telemetry, dormant-capability overhead, non-visual negative loading, shared artifact inspection and demonstrated downward compilation. This bounded batch found no single persisted acceptance artifact proving the full seven-gate Capability Embodiment contract.

**Classification:** `CORE/CONTINUOUS / ACTIVE_PARALLEL`; bounded implemented components exist, whole architecture acceptance remains `UNKNOWN_NEEDS_EVIDENCE`.

### 3. Operating Nervous System remains foundational and broader than implemented components

The current Master Register correctly keeps `NERVOUS-SYSTEM` active. Cost, rights/provenance, evaluation, observability, authority and capability-frontier doctrine are stronger than any one implementation primitive. Later common-substrate, coordination and runtime milestones do not prove whole-system A0–A4 enforcement, unified cost/rights/evaluation/observability or complete self-maintenance.

**Classification:** `ACTIVE_PARALLEL / FOUNDATIONAL`; no completion promotion warranted.

### 4. System Relationship Map is a valid canonical boundary map, while its machine-readable companion has coverage drift

The relationship map's product/project/runtime distinction remains useful and current. Its machine-readable companion `runtime/product-registry.v1.json` has already been reconciled separately as a real architecture foundation with live coverage drift; therefore the relationship map should not be reopened as a separate implementation project.

**Classification:** relationship doctrine `CORE/CONTINUOUS`; product-registry implementation remains separately `MAINTENANCE / COMPLETED_REVISIT_CANDIDATE` under its existing evidence boundary.

## New material reconciliation: shared Scripture Workspace

### 5. The Bible Notes × ONE × Search fusion is no longer pre-implementation only

`MULTIWRITE-BIBLE-NOTES-ONE-FUSION-v1.md` and `CORE-CONSOLIDATION-PASS-01-SCRIPTURE-KNOWLEDGE.md` were written as architecture/pre-implementation direction, but current code now contains a real shared Core foundation:

- `ScriptureAnchor`, `StudyNote` and `LibrarySourceRef` types;
- `ScriptureWorkspace` backed by the canonical `SharedArtifactStore` SQLite substrate rather than a second writable JSON note store;
- protected USER-authored notes with revision checking;
- Dawn source artifacts and typed `cites` links;
- deterministic L0 fuzzy retrieval over note text, Scripture anchors, entities/topics and source metadata;
- one-time legacy JSON migration into the common substrate;
- a machine-readable capability manifest declaring ONE, Multiwrite, Search and Dawn consumers and explicitly forbidding duplicate `one.search`, `one.notes`, `multiwrite.search`, `multiwrite.bible-search` implementations;
- an executable acceptance harness that checks single SQLite truth, no new JSON note truth, same note identity, Scripture/source preservation, fuzzy re-entry, revision safety, immutable history, shared provenance/links and protected-user defaults.

Therefore the historical label `CANONICAL PRE-IMPLEMENTATION ARCHITECTURE` is stale as a description of total implementation state. The architecture remains canonical, but the work has advanced to a real Core implementation foundation.

### 6. The foundation is not yet a product integration completion

The existence of `scripture_workspace_acceptance.py` is not itself a persisted PASS receipt. This bounded batch found no durable result artifact proving the acceptance was executed at the current head, and no evidence proving the architecture's cross-product acceptance contract:

1. a note created from ONE appears in Multiwrite as the same artifact ID;
2. edits in Multiwrite are visible from ONE without copy/sync duplication;
3. imprecise retrieval explains why a known note matched;
4. exact Scripture identity outranks broad semantic similarity in real product flow;
5. ONE and Multiwrite use the same retrieval capability/index;
6. no second chapter registry/private note truth is introduced by adapters;
7. protected human note text cannot be silently mutated;
8. ONE ↔ Multiwrite deep links round-trip the same artifact;
9. retrieval projections rebuild from canonical artifacts;
10. Search consumes the same Core retrieval path rather than another duplicate implementation.

Browser/Core Search duplication is already a separate known revisit issue, so convergence must be proven rather than assumed.

## Work classification

The shared Scripture workspace / Bible Notes fusion should be represented as a distinct durable work item rather than hidden inside generic `NERVOUS-SYSTEM` infrastructure:

- **Work:** Shared Scripture Workspace / ONE × Multiwrite Bible Notes × Doré Retrieval fusion.
- **Current classification:** `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`.
- **Historical architecture-only state:** `SUPERSEDED` as a total-state description; retained as provenance and governing semantics.
- **Completion state:** not complete.
- **Missing-evidence classification:** `UNKNOWN_NEEDS_EVIDENCE` for executable acceptance receipt and real consumer integration.

## Smallest useful next milestone

Without interrupting P01:

1. execute `runtime/scripture_workspace_acceptance.py` at the current canonical head and persist the JSON result;
2. wire one bounded ONE adapter and one Multiwrite adapter to the same Core `StudyNote` identity;
3. create a note from ONE, edit it in Multiwrite and verify the same artifact/revision from both surfaces;
4. prove ONE/Multiwrite retrieval calls the same Core path and preserve typed match explanations;
5. add a negative test proving protected USER text cannot be silently rewritten and a duplicate private note/search store is not created;
6. only then evaluate Search convergence/deep-link integration as a separate gate.

## Capability retention

This foundation preserves reusable capabilities beyond the eventual Bible Notes UI:

- one canonical user-authored artifact across multiple product surfaces;
- immutable revision/history semantics;
- protected human authorship separated from Doré suggestions and external source authority;
- provenance-bearing source attachment;
- typed links across Scripture, notes and Library sources;
- deterministic cheap-first retrieval before optional semantic escalation;
- compatibility migration from product-local storage into one common substrate without retaining a second writable truth.

## P01 isolation

No P01 subtitle state, deployment, source order, credential, binding, job, blocker, runtime resume condition or critical-path priority was modified by this reconciliation.
