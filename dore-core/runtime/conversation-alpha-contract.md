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
A1 is now IMPLEMENTED_AND_CI_VERIFIED for the persisted active project path.

Evidence:
- `dore-core/runtime/build_conversation_context.py` builds a bounded packet from the canonical Master Register, persistent project runtime state, Constitution, this Alpha contract, and the active project brief.
- The packet explicitly carries human/church final authority, forbids public-conversation authorization, exposes missing required evidence, and refuses to silently substitute a non-active project for the persisted runtime context.
- `dore-core/tests/test_conversation_context.py` verifies the P01 packet and the project-substitution guard.
- `.github/workflows/dore-conversation-alpha.yml` executes the tests and builds the packet in CI.
- GitHub Actions run `32817415345` completed successfully on commit `eb17215f493ddf36297b124d807d458162415e56`.

This does not mark the Internal Alpha complete. A1 currently loads the canonical persistent project context, but project-specific memory/knowledge enrichment remains evidence-driven rather than fabricated when no explicit binding exists.

Next bounded step: implement the A2 grounded-contribution envelope so every Doré meeting contribution carries a type, evidence references, uncertainty, authority level, and persistence eligibility; exercise it against the P01 context packet before beginning A3 meeting-close persistence.
