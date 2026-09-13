# DORÉ CONVERSATION ALPHA STATE-REPLAY DRIFT EVIDENCE LEDGER

Status: ACTIVE / SWEEP-01 EVIDENCE
Date: 2026-09-13
Related work: `CONVERSATION`, `CW-004`, `P01-PREFLIGHT`, `MEM-SWEEP-01`

## Bounded evidence reviewed

- `dore-core/runtime/conversation-alpha-verification.json`
- `dore-core/runtime/build_conversation_context.py`
- `dore-core/runtime/meetings/P01-PREFLIGHT-SUBTITLE/latest.json`
- `dore-core/runtime/project-execution-state.json`
- `dore-core/tests/test_conversation_context.py`
- `dore-core/tests/test_conversation_contribution.py`
- `dore-core/tests/test_conversation_meeting_close.py`

## Historical completion remains valid

The original Internal Alpha milestone remains a legitimate historical `VERIFIED_COMPLETE` result for its bounded 2026-08-25 contract. `conversation-alpha-verification.json` records five passing gates, internal-only authority, fresh-session replay, persisted meeting close and no public/consequential authority. Nothing in this sweep batch erases that historical evidence.

## Current regression / drift finding

The replayed durable meeting state is now stale relative to the canonical runtime.

Current canonical runtime:

- `project-execution-state.json` records `P01-PREFLIGHT-SUBTITLE` as `ENVIRONMENT_BLOCKED`;
- attempt is `39`;
- the terminal blocker is `CAPTION_SOURCE_UNAVAILABLE_AND_AUDIO_TRANSCRIPTION_RUNTIME_NOT_CONFIGURED`;
- the runtime's smallest human action is provisioning one approved production audio-acquisition/transcription path and exposing the required binding/credential.

Replayed meeting memory:

- `runtime/meetings/P01-PREFLIGHT-SUBTITLE/latest.json` still records `project_state_at_close: RUNNABLE`;
- its next action says `Keep P01 RUNNABLE`;
- its durable risk says production verification was still incomplete before the later live v5/D1 execution and environment-blocked terminal state.

`build_conversation_context.py` correctly loads the *current* canonical runtime into `packet.project`, but it also replays the old meeting record into `packet.meeting_memory` without a freshness/supersession check against the canonical runtime checkpoint. This can therefore present a fresh current project state and an obsolete remembered state in the same context packet.

## Test-boundary finding

The current Conversation Alpha tests prove the original bounded mechanics, but they do not detect this chronology contradiction:

- `test_conversation_context.py` requires the prior meeting record to be replayed and checks the historical `production-verified` risk string, but does not compare `meeting_memory.project_state_at_close` with the current runtime state/checkpoint;
- `test_conversation_contribution.py` uses example content that still says P01 is `RUNNABLE`; because contribution content is fixture text, the test does not fail when runtime truth changes;
- `test_conversation_meeting_close.py` likewise uses `RUNNABLE` fixture text and proves persistence filtering/round-trip behavior rather than current-state reconciliation.

Therefore the historical Internal Alpha completion is not falsified, but its regression surface is now incomplete.

## Classification

- Historical Conversation Runtime Internal Alpha milestone: `VERIFIED_COMPLETE` for the original bounded contract.
- Current Conversation workstream quality: `COMPLETED_REVISIT_CANDIDATE` until state-replay supersession/freshness behavior is repaired and regression-tested.
- Public Conversation: remains `PARKED` / unauthorized.
- Conversation Memory v1: remains a separate `ACTIVE_PARALLEL / IMPLEMENTING` workstream.

## Smallest repair

Do not rewrite or delete the historical meeting record. Preserve it as provenance.

Instead:

1. add a replay-freshness/supersession check comparing prior meeting close state/checkpoint with current canonical runtime;
2. when the current runtime is newer, mark the replayed meeting state as historical/superseded rather than current guidance;
3. prevent stale `next_actions` such as `Keep P01 RUNNABLE` from being presented as governing next action;
4. add a regression fixture in which the prior meeting says `RUNNABLE` while current runtime says `ENVIRONMENT_BLOCKED`, and require the packet to preserve both chronology and current canonical authority without ambiguity;
5. update example test text so fixture prose is not itself mistaken for current P01 truth.

## Disposition

This is a maintenance/revisit defect in Conversation continuity, not a P01 blocker and not a reason to reopen public Conversation. P01 ordering and the existing environment blocker remain unchanged.