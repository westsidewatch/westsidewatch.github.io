# Doré Conversation Runtime — Internal Alpha Contract

Status: INTERNAL_ALPHA / NOT_PUBLIC

## Purpose
Provide a bounded internal meeting mode in which Doré can load relevant project context, contribute grounded judgments, questions, and suggestions, use available repository/knowledge/tool evidence, and persist durable decisions and learning after discussion.

## Authority boundary
Doré is advisory and evidentiary. Human/church authority remains final. The runtime must not impersonate pastoral, doctrinal, editorial, operational, or publication authority; it must distinguish evidence, inference, recommendation, and unresolved questions. No public conversational-agent surface is authorized by this contract.

## A1 — Context loading
For a named project or meeting topic, load the smallest relevant evidence set from persistent project runtime, project brief, memory, knowledge, constitution/authority constraints, and current repository evidence. Prefer canonical persisted evidence over conversational recollection. Record missing evidence rather than inventing it.

## A2 — Grounded contribution
Each substantive Doré contribution should be classifiable as one or more of: evidence, judgment, question, suggestion, risk, or decision candidate. Claims that depend on project facts must be traceable to loaded evidence. Uncertainty and conflicting evidence must remain visible.

## A3 — Meeting close / durable persistence
At discussion close, separate transient dialogue from durable outputs. Persist only durable decisions, changed constraints, verified learning, unresolved blockers, and next executable actions into the appropriate project/memory/knowledge evidence surface. Do not persist speculation as fact.

## Alpha readiness gates
1. Context can be loaded from persistent evidence without a human re-brief.
2. Contributions can cite or identify their evidence basis and uncertainty.
3. Human/church authority boundaries are explicit and preserved.
4. A meeting can end with a compact durable record that survives a new session.
5. No public conversational UI/API is exposed before a separate publication/readiness decision.

## Current checkpoint
A1, A2, and the bounded A3 persistence primitive are IMPLEMENTED_AND_CI_VERIFIED for the persisted active-project path.

A1 evidence:
- `dore-core/runtime/build_conversation_context.py` builds a bounded packet from the canonical Master Register, persistent project runtime state, Constitution, this Alpha contract, and the active project brief.
- The packet explicitly carries human/church final authority, forbids public-conversation authorization, exposes missing required evidence, and refuses to silently substitute a non-active project for the persisted runtime context.
- `dore-core/tests/test_conversation_context.py` verifies the P01 packet and the project-substitution guard.

A2 evidence:
- `dore-core/runtime/conversation_contribution.py` validates a typed internal contribution envelope with evidence references, explicit uncertainty, authority level, and persistence eligibility.
- Evidence/judgment/risk/decision-candidate contributions are rejected when they lack an evidence basis; unknown evidence references are rejected.
- Speculative/unverified/unknown contributions cannot be marked persistence-allowed; grounded evidence can be marked eligible while human/church final authority and the public-conversation prohibition remain carried in the envelope.
- `dore-core/tests/test_conversation_contribution.py` exercises grounded judgment, missing-evidence rejection, unknown-reference rejection, speculative persistence rejection, and grounded persistence eligibility.

A3 evidence:
- `dore-core/runtime/conversation_meeting_close.py` builds a compact internal meeting-close record from the ready context and validated contributions.
- Only contributions already marked persistence-allowed can enter the durable contribution set; project-mismatched, transient, speculative, or authority-unsafe items are rejected into an explicit non-durable list.
- Every persisted meeting record keeps human/church authority final, public conversation unauthorized, and consequential action unauthorized by the record itself.
- `persist_meeting_record()` writes a replayable JSON record whose round trip is tested to survive a fresh process/session boundary.
- `dore-core/tests/test_conversation_meeting_close.py` verifies filtering, project mismatch rejection, authority preservation, and round-trip durability.
- `.github/workflows/dore-conversation-alpha.yml` verifies A1+A2+A3 together.
- GitHub Actions run `32822094490` completed the Conversation Alpha job successfully on commit `db0e39d93a296cc5e695aa4dc3cacf63aec592fe`.

This does not yet mark the Internal Alpha VERIFIED_COMPLETE. The primitives are now present and CI-verified, but the readiness gate still requires a real internal meeting exercise that loads persisted P01 context, produces at least one grounded contribution and one rejected transient/speculative contribution, persists the meeting-close record into a durable repository evidence path, then demonstrates that a fresh context load can discover/replay that record without a human re-brief. Project-specific memory/knowledge enrichment also remains evidence-driven rather than fabricated where no explicit binding exists.

Next bounded step: execute and persist that full internal P01 meeting rehearsal end-to-end, then perform a fresh-session replay check. If successful, evaluate whether Internal Alpha meets VERIFIED_COMPLETE without changing P01 priority or authorizing any public conversation surface.
