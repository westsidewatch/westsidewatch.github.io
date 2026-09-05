# DORÉ MEMORY SWEEP 01 — CHECKPOINT 35

Date: 2026-09-05
Status: BOUNDED_RECONCILIATION_COMPLETE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
Canonical extension updated: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Bounded evidence reviewed

- commit `69c4a40a2e082749a7d03c54a68948305a24f3fa` (`Continue Doré Image: resident autorun bridge (#313)`);
- commit `56b767c1fd4957f7597c231a64029902d012c985` (`DORÉ A2A: Firefox Native Messaging control-plane transport (#314)`);
- commit `5a47ff781ae876058561af2a08395512184ebbc3` (`DORÉ A2A: close Companion Native CI gate (#315)`);
- resident-image runtime discovery/autorun implementation and tests;
- Companion Native Messaging manifest, transport, native host, installer and contract tests;
- capability-runtime CI trigger/test wiring for the native transport;
- commit-associated workflow-run receipt surfaces for all three commits;
- Checkpoint 34 resident-image substrate interpretation.

## Reconciliation findings

1. Doré Image now has a bounded resident **autorun** seam on top of the previously reconciled resident-byte pipeline. It can discover loopback-only renderer configuration, distinguish `NOT_READY` / `IDLE` / `PASS`, health-check the local renderer, consume a queued job, persist completion state and remove the job after generation returns. This is a `VERIFIED_COMPLETE_SUBMILESTONE` for orchestration architecture, not proof of real ComfyUI/model execution.
2. The resident autorun does not create a new human/environment blocker. Missing config or an unreachable renderer is a readiness state until a configured real runtime attempt demonstrates otherwise. The real acceptance chain remains one purpose-built Westside asset through resident render → durable bytes/provenance → real vision observations → correction/acceptance → typed Design application.
3. Companion→Doré transport has advanced from resident HTTP-first to **Firefox Native Messaging native-first** while preserving the mature `dore.a2a/1` adapter/control-plane seam. `localhost:4312` is now explicitly compatibility/debug fallback, not the preferred production carrier.
4. The Native Messaging implementation and contract tests are a `VERIFIED_COMPLETE_SUBMILESTONE`: the carrier is local stdio, message size/type is bounded, host/extension IDs are pinned, the installer preflights downloaded code, and CI configuration now includes the native contract paths/tests.
5. Latest-head CI acceptance is still not proved. The commit-associated workflow-run surfaces for `69c4a40...`, `56b767...` and `5a47ff...` returned no persisted runs. This is `UNKNOWN_NEEDS_EVIDENCE`, not a failure result.
6. Live Mac browser→Native Messaging→host→adapter→Design acceptance is likewise still `UNKNOWN_NEEDS_EVIDENCE`. Until that proof exists, retiring `4312` would be premature. Its primary-carrier role is `SUPERSEDED`; its fallback implementation remains `MAINTENANCE`.
7. Native transport reduces dependence on an exposed localhost browser HTTP carrier but does not close the separate mutation-authority problem. Existing constitutional authority-envelope / A3-A4 hardening debt remains governing.
8. No P01 state or action was modified. The approved production audio-acquisition/transcription environment dependency remains the same governing P01 blocker.

## Durable updates

- created `DORÉ-RESIDENT-IMAGE-AUTORUN-EVIDENCE-LEDGER-2026-09-05.md`;
- created `DORÉ-COMPANION-NATIVE-MESSAGING-EVIDENCE-LEDGER-2026-09-05.md`;
- extended the canonical sparse-capability runtime addendum with resident-autorun and native-first Companion transport classifications, supersession judgment and open acceptance evidence.

## Sweep disposition

Sweep 01 remains `ACTIVE_PARALLEL`. This bounded batch does not justify `VERIFIED_COMPLETE` and introduces no new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition.
