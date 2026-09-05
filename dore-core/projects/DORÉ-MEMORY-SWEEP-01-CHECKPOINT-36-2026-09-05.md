# DORÉ MEMORY SWEEP 01 — CHECKPOINT 36 — 2026-09-05

Status: BOUNDED_PASS_COMPLETE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Bounded batch

This pass reconciled the newest Firefox Companion 1.0 browser-shell evidence introduced at commit `2e2db37df4b30ad6b2ae5be499c54c8da34e5885` against the existing A2A/control-plane/Native Messaging canonical interpretation.

Reviewed:

- introducing commit diff and files;
- Companion manifest/background/content-script implementation;
- extended Companion Native contract tests;
- combined commit-status surface;
- commit-associated workflow-run surface;
- existing sparse-capability-runtime addendum and A2A/Companion Native evidence.

## Findings

1. Companion 1.0 is a real `VERIFIED_COMPLETE_SUBMILESTONE` at repository implementation level: an installable Firefox shell now binds ChatGPT `/dore` capture, health/status UI, background routing and native-first `dore.a2a/1` dispatch.
2. This closes the earlier product-shell gap but does not prove live Firefox/ChatGPT/Native Messaging acceptance.
3. Both GitHub receipt surfaces returned no persisted status/run receipt for the introducing head. This remains `UNKNOWN_NEEDS_EVIDENCE`, not a test failure or blocker.
4. The present fixed status badge is retained as first operational UX and marked `COMPLETED_REVISIT_CANDIDATE` only after functional acceptance; redesign should not outrun proof.
5. The Native Messaging direction remains governing; `localhost:4312` remains compatibility/debug fallback.
6. No human decision or environment blocker was created by this batch.
7. P01 was not modified, interrupted or reprioritized.

## Durable updates

- added `DORÉ-COMPANION-1-EXTENSION-SHELL-EVIDENCE-LEDGER-2026-09-05.md`;
- extended `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md` with the Companion 1.0 submilestone and acceptance boundary.

## Sweep disposition

Sweep 01 remains `ACTIVE_PARALLEL` and is not yet `VERIFIED_COMPLETE`.
