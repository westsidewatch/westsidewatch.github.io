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
A1/A2 contract persisted. Next bounded step: implement or identify the internal context-packet builder against the existing project runtime and project brief, then exercise it on P01 without changing P01 priority or terminal-state rules.
