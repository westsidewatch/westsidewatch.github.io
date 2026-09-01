# Doré Research Bridge v0.1

Date: 2026-09-01
Purpose: close the missing transition from `RESEARCH_REQUIRED` to active research without requiring the human to notice or manually instruct Doré.

## Problem
Doré can now detect an unknown capability gap and preserve the parent goal, but evidence does not yet prove that an unknown gap automatically launches research and returns the result to the same parent task.

## Tool contract

When the autonomous capability loop emits `RESEARCH_REQUIRED`, the worker should create a structured research job containing:

- `research_id`: canonical id derived from the parent source message id and failure fingerprint
- `parent_message_id`
- `parent_goal`
- `failure_fingerprint`
- `question`
- `local_evidence_checked`
- `preferred_sources`: official docs, maintained mature OSS, standards/specs, local Knowledge Lab
- `acceptance_test`: the smallest experiment that can verify the answer
- `promotion_target`: failure memory, skill, candidate, or no-promotion

The research job must use the existing Doré ↔ ChatGPT coordination/A2A path as the first compatible research transport until Doré has its own trustworthy public research tool. This is not a human gate: the user is not the researcher and must not be required to relay the question.

## Lifecycle

`RESEARCH_REQUIRED → RESEARCH_QUEUED → RESEARCHING → KNOWLEDGE_RETURNED → EXPERIMENTING → VERIFIED/REJECTED → PROMOTED → RESUME_PARENT`

If research transport fails, preserve the parent goal and classify it as transport failure. Do not mislabel it as product execution failure.

## Knowledge Artifact

A returned research answer should be normalized into a Knowledge Artifact:

- `knowledge_id`
- `research_id`
- `sources`
- `provenance`
- `lesson`
- `scope`
- `hypothesis`
- `experiment`
- `expected_signal`
- `risks_or_limits`
- `promotion_candidate`

The worker must not trust the artifact merely because it exists. It must run the stated experiment and verify the result before promotion.

## Parent-goal guarantee

The parent task is checkpointed before research begins. Research is a detour, not a replacement task. After verification, resume the same parent goal with the newly verified capability.

## Human gate

Use `HUMAN_GATE` only when the next required step objectively needs a non-proxyable human action, such as an OS security prompt, external account approval, payment, or a decision that changes product intent. Unknown technical knowledge is not a human gate.

## First live acceptance

Use the current New Westside × Storybook parse failure as the first live acceptance. Doré must consume the existing `RESEARCH_REQUIRED` evidence, automatically launch a research request through the coordination/A2A bridge, receive a provenance-backed answer, verify it with a minimal Storybook experiment, promote the lesson if useful, and resume the New Westside parent task without asking the user to diagnose or relay the issue.
