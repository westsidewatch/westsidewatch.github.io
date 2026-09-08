# DORE MEMORY SWEEP 01 — CHECKPOINT 44

Date: 2026-09-08
Status: ACTIVE_PARALLEL
P01 impact: NONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence ledger: `DORÉ-WESTSIDE-CONTEXT-ADAPTER-EVIDENCE-LEDGER-2026-09-08.md`

## Bounded evidence reviewed

- `dore-core/context/README.md`;
- merged PR #409 (`DORÉ: minimal Westside Context adapter`);
- the Context implementation family under `dore_core/context/`;
- Context capability registration in `dore-core/runtime/capability-registry.v1.json`;
- Context benchmark/test family, especially `tests/benchmark_westside_context.py`;
- merged PR #412 (`fix: make CJK Westside Context questions retrievable`);
- available deployment/workflow evidence associated with those changes.

## Reconciliation findings

1. Westside Context is a real internal Doré capability, not a public main-site feature and not a replacement for Knowledge/Memory/Graph. Its governing source of truth remains `docs/MASTER_SITE_ARCHITECTURE.md`.
2. The bounded minimal implementation milestone is historically complete: the Markdown hierarchy compiler, SQLite/FTS5 projection, provenance-bearing ancestor-aware Context Packet, read-only adapter boundary and capability-registry entry were merged in PR #409.
3. The implementation follows the desired `能力越大、負擔越小` rule: no external API, third-party memory framework, vector DB or graph DB was added without measured need.
4. The first concrete retrieval defect was evidence-led rather than architecture-led. Question-form Chinese such as `多雷探索是什么意思？` exposed a real CJK recall gap; PR #412 repaired it with deterministic CJK n-grams plus a focused regression and also corrected section-content hierarchy boundaries.
5. The correct current classification is `COMPLETED_REVISIT_CANDIDATE / MAINTENANCE`: keep the minimal adapter, reopen only when measured misses/precision/scale/cross-source needs exceed it.
6. A stronger global acceptance claim is not justified. The repository contains benchmark/tests, but this batch did not find a dedicated persisted current post-PR-412 acceptance artifact proving the full benchmark against the current canonical architecture. The available earlier Foundation workflow had relevant test steps succeed but failed later on broader Foundation enforcement, so it is not clean Context completion evidence.
7. No Master Register workstream status requires promotion/demotion from this batch. The useful change is evidence accounting: `dore-core/context/` is now explicitly reconciled as a bounded completed foundation with an open acceptance-evidence boundary.
8. No P01 subtitle ordering, deployment, credentials, audio, transcription, runtime or blocker condition was touched.

## Missing evidence carried forward

- one persisted post-PR-412 Context benchmark/acceptance result against the current `MASTER_SITE_ARCHITECTURE.md`;
- unseen Chinese natural-language query coverage;
- precision-negative cases and false-positive tracking;
- measured retrieval/latency/index-size evidence before any heavier retrieval architecture is considered;
- evidence for multi-source Context assembly if that capability is later needed.

## Durable update

Created `DORÉ-WESTSIDE-CONTEXT-ADAPTER-EVIDENCE-LEDGER-2026-09-08.md` to preserve the historical completion judgment, current quality/debt, revisit triggers, missing-evidence boundary and retained reusable capability.

## Smallest next proof

Run and persist the current Westside Context benchmark after PR #412 against the current canonical architecture, adding a small unseen Chinese question set plus precision-negative cases. If it passes, retain the adapter without expansion. If it fails, repair the measured gap first; consider heavier semantic/vector/graph machinery only if repeated evidence shows the minimal local mechanism is insufficient.

Sweep status remains `ACTIVE_PARALLEL`; this checkpoint does not justify `VERIFIED_COMPLETE` and does not create a human/environment blocker.
