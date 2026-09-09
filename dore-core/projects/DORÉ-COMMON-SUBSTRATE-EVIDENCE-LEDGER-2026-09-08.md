# DORÉ COMMON SUBSTRATE EVIDENCE LEDGER — 2026-09-08

Status: ACTIVE / SWEEP-01 EVIDENCE / CORRECTED 2026-09-09
Parent checkpoint: `DORE-MEMORY-SWEEP-01-CHECKPOINT-49-2026-09-08.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Correction checkpoint: `DORE-MEMORY-SWEEP-01-CHECKPOINT-51-2026-09-09.md`

## Scope

Bounded reconciliation of the current shared artifact Common Substrate foundation. This ledger does not change P01 subtitle priority or runtime state.

## Correction of the 2026-09-08 interpretation

The first version of this ledger incorrectly described `dore-core/runtime/common-substrate.v1.json` as a four-workspace (`scripture`, `design`, `video`, `code`) intervention registry and cited `.github/workflows/dore-common-substrate.yml`. Direct re-read of the current canonical files and the originating implementation commit disproves that description:

- `common-substrate.v1.json` defines `dore.common-substrate.v1` as **one local SQLite artifact truth with many product projections**;
- its source-of-truth primitives are artifacts, immutable revisions, typed links and provenance edges;
- its artifact kinds include study notes, Scripture anchors, library sources, conversation messages, research evidence, writing/design artifacts and learning evidence;
- its product-boundary rule explicitly forbids ONE, Multiwrite, Search, Dawn Library or Doré Local from becoming a second shared-memory brain;
- no current `.github/workflows/dore-common-substrate.yml` file exists.

The earlier four-workspace/workflow statements are therefore `SUPERSEDED / ERRONEOUS_SWEEP_INTERPRETATION` and must not be reused as architecture evidence.

## Direct current evidence

### `dore-core/runtime/common-substrate.v1.json`

Defines the canonical storage/governance contract:

- SQLite + WAL, stdlib dependency floor;
- stable shared artifact truth;
- immutable revisions and optimistic `expected_revision` mutation gate;
- provenance and typed links;
- rebuildable full-text/semantic/product-view projections;
- deterministic retrieval first, optional semantic projection only after measured gain;
- protected human artifacts may not be silently rewritten by learning/retrieval;
- one shared Core truth, with products acting as projections/adapters rather than private memory stores.

### `dore-core/substrate.py`

Provides real runtime implementation rather than architecture prose:

- `SharedArtifactStore` creates/updates artifacts in SQLite;
- WAL and foreign-key enforcement are configured;
- immutable revision rows are persisted;
- stale revision writes raise `stale_revision`;
- provenance edges and typed links are persisted;
- FTS5 is a disposable projection with deterministic text fallback;
- the search projection can be rebuilt from canonical artifacts.

### `dore-core/runtime/common_substrate_acceptance.py`

Provides executable bounded acceptance over the actual substrate. Its checks cover:

- one SQLite truth;
- WAL;
- protected USER authority default;
- revision advancement + stale-write refusal;
- immutable history;
- provenance and typed-link preservation;
- retrieval and safe projection rebuild;
- Scripture Workspace using the same SQLite substrate rather than parallel JSON note truth;
- fuzzy Scripture-note retrieval preservation;
- Library source promotion into canonical artifacts.

The script emits schema `dore.common-substrate-acceptance.v2`.

## Classification

- Common shared artifact substrate implementation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION` under Core/Runtime evolution.
- Scripture Workspace → common substrate facade migration: implementation is explicit in the acceptance contract; terminal current PASS receipt is still evidence-gated.
- Product-wide adoption beyond the tested Scripture facade: `UNKNOWN_NEEDS_EVIDENCE`.
- Earlier four-workspace description and nonexistent workflow citation: `SUPERSEDED / ERRONEOUS_SWEEP_INTERPRETATION`.

## Missing proof

This corrected batch does not locate a durable fresh execution receipt proving the current `dore.common-substrate-acceptance.v2` script against the repository state now on `main`. The smallest useful proof is therefore:

1. execute the current acceptance script in a dependency-valid environment;
2. persist the exact JSON result;
3. preserve it as a regression gate;
4. separately prove additional product facades only as they actually migrate to the shared substrate.

Do **not** require fictitious per-workspace `scripture/design/video/code` results; that requirement belonged to the erroneous earlier interpretation.

## Durable lesson

Sweep summaries must be checked against source text before becoming architectural truth. A plausible system label is not evidence of the file's actual contract, and a referenced workflow must be verified to exist before it is cited as acceptance infrastructure.

## P01 boundary

No P01 code, ordering, deployment, audio/transcription environment, credentials or blocker state is modified by this correction.