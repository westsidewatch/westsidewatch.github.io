# DORÉ LOCAL INTELLIGENCE FABRIC — EVIDENCE LEDGER

Status: ACTIVE_PARALLEL / BOUNDED_EVIDENCE_RECONCILIATION
Date: 2026-09-08
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`

## Scope

This ledger reconciles the first implementation wave of Doré's Local Intelligence Fabric without promoting architecture or commit labels into broader autonomy claims. It is subordinate to the canonical `DORÉ-MASTER-WORK-REGISTER.md` and does not alter the active P01 subtitle critical path.

Bounded evidence reviewed:

- commit `1deb1bebcc5c665d06ab2ea2677862a1687e40c3` — `DORÉ: Local Intelligence Fabric Phase 1`;
- commit `797ecf92d003ef38095e8f5454295b3154b33909` — bounded one-time safe self-maintenance bootstrap / A2A exposure;
- commit `ffab45fafc67fd97606b798bf5d5dc83556153ec` — behavioral/idempotent knowledge-substrate acceptance adjustment;
- current repository evidence exposed by those commits, including the compatibility map, capability/runtime test expansion, native-host maintenance boundary, knowledge-substrate POC and local substrate install/control-plane paths.

## 1. Local Intelligence Fabric Phase 1

### Original objective

Insert replaceable local intelligence/retrieval substrates beneath Doré's existing Capability Bus / Context / A2A boundaries without forcing products to learn physical models, provider endpoints, LongMemory, QMD or other substrate-specific APIs.

### Evidence

Commit `1deb1beb...` adds and tests:

- `dore_core/intelligence/**`, `dore_core/substrates/**`, `dore_core/retrieval/**` paths to the capability CI surface;
- compatibility rules preserving capability IDs, typed artifacts, provenance-bearing read-only context, no direct product→provider dependency and an offline/no-commercial-key core path;
- minimum-capability routing and residency policy concepts;
- LongMemory and QMD adapter/substrate placement rules;
- Living Retrieval and bounded local substrate installation/control-plane coverage;
- Native Messaging production control integration while preserving Doré Core as authority.

The commit itself is strong repository implementation evidence. At the time of this bounded review, the GitHub connector returned no combined-status entries and no workflow runs directly associated with this commit, so this pass does not claim a CI/production acceptance that is not independently persisted.

### Classification

`ACTIVE_PARALLEL`

The **Phase 1 repository implementation milestone is real**, but the broader Local Intelligence Fabric is not `VERIFIED_COMPLETE`. Production/runtime proof, cross-product use, residency behavior under load, failure/recovery behavior and substrate interchangeability remain evidence-gated.

### Current quality judgment

Strong architecture direction: product interface freeze, Doré sovereignty over substrates, minimum-capability routing, residency gating and free-first/offline constraints directly reduce duplication and model/RAM pressure while keeping products stable. The key strength is that external open-source projects are treated as nutrition/substrates rather than replacement identities.

### Debt / revisit triggers

Revisit when any product gains a direct dependency on a physical model/provider/substrate, when RAM residency grows with capability count, when multiple retrieval engines diverge semantically, or when a substrate cannot be replaced without product changes.

## 2. Bounded self-maintenance bootstrap

### Original objective

Allow Doré to maintain its own production checkout through a narrow, reversible operation rather than arbitrary shell authority.

### Evidence

Commit `797ecf92...` adds:

- explicit allowlisting of `system.self-maintain` rather than a wildcard `system.*` surface;
- a clean-worktree requirement;
- safety-branch creation before mutation;
- `git rebase origin/main` with abort/reset recovery on conflict;
- native-host refresh only after a clean successful reconciliation;
- a dedicated `self_maintenance_action.py` path with no `shell=True`;
- tests locking the bounded control-plane and reversible boundary.

### Classification

`ACTIVE_PARALLEL / MAINTENANCE`

This is a legitimate **bounded implementation milestone**, not proof of general autonomous self-modification. The one-time bootstrap and action boundary should be preserved as a safety primitive. A persisted real production execution transcript proving the full clean-worktree → safety branch → rebase → refresh → subsequent autonomous maintenance cycle was not established by this bounded review.

### Current quality judgment

The fail-closed shape is good: clean worktree, no detached HEAD, safety branch, conflict abort, bounded command surface and explicit allowlist materially reduce authority risk. It should not be generalized into arbitrary shell execution.

## 3. QMD / LongMemory behavioral substrate acceptance

### Original objective

Validate useful local retrieval/memory substrates behaviorally and idempotently while keeping canonical Doré knowledge outside substrate authority.

### Evidence

Commit `ffab45fa...` strengthens `knowledge-substrate-poc.py` so that:

- QMD acceptance depends on an actual local BM25 retrieval hit for `嗎哪 曠野` returning the expected `manna.md` / `嗎哪與曠野` evidence, rather than merely command exit codes;
- repeated collection creation is treated idempotently, allowing an already-existing collection while requiring update/search behavior to remain correct;
- LongMemory acceptance detects its stable CLI command surface (`add <text>`, `query <text>`) despite non-conventional help/version exit behavior;
- the LongMemory POC DB remains isolated;
- `canonical_ingest` remains false and substrate `authority` remains false.

### Classification

QMD bounded local retrieval POC: `ACTIVE_PARALLEL` with a behaviorally stronger acceptance contract.

LongMemory bounded CLI/substrate POC: `DISCOVERY / ACTIVE_PARALLEL`; local callable surface is evidenced, but durable Doré memory integration, provenance semantics, recovery behavior and cross-project usefulness are not yet proven.

### Supersession judgment

This evidence supersedes any interpretation that LongMemory or QMD should become Doré's new core identity/store. They remain replaceable substrates below Doré authority. It also supersedes command-exit-only acceptance as sufficient evidence for the POC: retrieval behavior and isolated-authority boundaries are the governing acceptance shape.

## 4. Capability retention

Reusable capabilities retained from this batch:

- product-interface freeze across substrate/runtime changes;
- minimum-capability routing and model-residency separation;
- local/free/offline provider gating;
- substrate authority separation from canonical knowledge;
- behavioral/idempotent acceptance instead of exit-code-only acceptance;
- bounded reversible self-maintenance through explicit capabilities rather than arbitrary shell access;
- fail-closed mutation preconditions and safety branches.

## 5. Missing evidence / next proof

The bounded batch does **not** establish:

1. a production cross-product Local Intelligence Fabric acceptance run;
2. measured RAM/latency evidence proving capability growth does not imply resident-model growth;
3. live interchangeability of QMD/LongMemory adapters without product changes;
4. LongMemory ingestion/retrieval of canonical Doré project history with provenance and conflict rules while preserving canonical source authority;
5. a persisted end-to-end production `system.self-maintain` execution followed by a later autonomous maintenance cycle;
6. materially different-domain blind transfer proving general self-equipping autonomy.

These are evidence gaps, not current human blockers.

## 6. P01 isolation

No P01 subtitle state, runtime, deployment, credential, audio-acquisition or transcription action was changed by this reconciliation. The active subtitle critical path remains governed independently by its canonical runtime state.
