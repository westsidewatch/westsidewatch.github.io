# DORÉ COMPANION NATIVE MESSAGING — EVIDENCE LEDGER

Date: 2026-09-05
Status: SWEEP_RECONCILED / VERIFIED_COMPLETE_SUBMILESTONE
Parent: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register extension: `DORÉ-MASTER-WORK-REGISTER-ADDENDUM-SPARSE-CAPABILITY-RUNTIME-2026-09-05.md`
P01 impact: NONE

## Evidence reviewed

- commit `56b767c1fd4957f7597c231a64029902d012c985` (`DORÉ A2A: Firefox Native Messaging control-plane transport (#314)`);
- commit `5a47ff781ae876058561af2a08395512184ebbc3` (`DORÉ A2A: close Companion Native CI gate (#315)`);
- Firefox Native Messaging extension manifest/transport contract;
- macOS native-host installer and stdio host implementation;
- `tests/test_dore_companion_native_contract.py` and native-host tests;
- capability-runtime workflow trigger/test coverage changes;
- commit-associated workflow-run receipt surfaces for both introducing/follow-on commits.

## Findings

1. Companion→Doré now has a materially better production transport direction than the earlier resident HTTP bridge alone: Firefox Native Messaging is explicitly the native-first carrier into the existing `dore.a2a/1` adapter/control plane, while `localhost:4312` is retained as compatibility/debug fallback until live Mac acceptance.
2. The implementation preserves the existing typed control-plane seam rather than creating a second Doré intelligence or new runtime bus. The native host is a local stdio carrier, does not create a daemon/socket listener, and delegates into the mature adapter/control-plane path.
3. The contract is fail-bounded: native messages are length-bounded JSON objects, the extension pins the expected host and extension IDs, the macOS installer validates downloaded host code before switching the active snapshot, and the follow-on test asserts native-first ordering plus the fallback role.
4. Commit `5a47ff...` closes a previous CI *configuration* hole by adding extension/native contract paths and tests to `dore-capability-runtime.yml`. However, the commit-associated workflow-run surface returned no persisted run receipt for either `56b767...` or `5a47ff...`. Therefore latest-head CI PASS is still `UNKNOWN_NEEDS_EVIDENCE`; wiring the test into CI is not equivalent to a persisted passing run.
5. Live browser→Native Messaging→host→adapter→Design acceptance on the user's Mac is also not yet persisted. Until that proof exists, `4312` should not be retired. Native-first is the governing direction; 4312 is `MAINTENANCE / compatibility fallback`, not an independently evolving primary transport.
6. This does not remove the existing authority-hardening debt: typed/native transport improves carrier integrity and reduces exposed localhost surface area, but transport identity alone does not prove cryptographic authorization for consequential mutation. Existing authority-envelope rules remain governing.
7. No new `HUMAN_DECISION_BLOCKED` or `ENVIRONMENT_BLOCKED` condition is justified by this evidence. The missing live Mac acceptance/CI receipt is an evidence gap, not a proven blocked state.
8. No P01 subtitle state, ordering, deployment or audio/transcription dependency was changed.

## Current classification

- Native Messaging transport implementation + contract tests: `VERIFIED_COMPLETE_SUBMILESTONE`;
- latest-head CI receipt: `UNKNOWN_NEEDS_EVIDENCE`;
- live Mac Companion→native→adapter→Design acceptance: `UNKNOWN_NEEDS_EVIDENCE`;
- localhost:4312 primary-transport role: `SUPERSEDED` by native-first direction, retained as `MAINTENANCE` fallback pending live acceptance;
- human/environment blocker discovered by Sweep: NONE.
