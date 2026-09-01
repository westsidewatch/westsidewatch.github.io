# Doré ↔ ChatGPT Shared Learning Loop

Date: 2026-09-01
Status: working doctrine / experiment rule

## Discovery

The collaboration itself can be a source of research questions.

Observed sequence:

1. One collaborator learns something useful during real work.
2. Share the useful knowledge increment with the other collaborator.
3. Notice the pattern itself: "when I learn, you should be able to learn too."
4. Treat that pattern as a research question rather than only a local habit.
5. Search external standards, research, mature tools, and open-source implementations for prior work on the pattern.
6. Evaluate and reuse what is mature instead of rebuilding blindly.
7. Convert the improved method into a shared capability.
8. Apply it immediately to the parent real-world task.
9. Preserve evidence so the next occurrence begins from a higher baseline.

Compact form:

REAL WORK → NEW KNOWLEDGE → SHARE → META-QUESTION → EXTERNAL RESEARCH → REUSE/ADAPT → JOINT EXPERIMENT → VERIFIED CAPABILITY → RESUME REAL WORK

This loop is recursive. Any improvement to the learning loop can itself become new shared knowledge and trigger another research/evaluation cycle.

## Core rule

Do not merely share answers. Share relevant, provenance-backed, testable knowledge increments that can improve the other agent's capability on a common goal.

Do not merely invent collaboration mechanisms. When a useful collaboration pattern is discovered, search for existing standards, papers, SDKs, protocols, tools, and open-source implementations; compare them; borrow mature parts; then adapt only what is distinctive to Doré/Westside.

## Shared-baseline principle

The target is not full internal-memory synchronization. Agents may remain opaque and independent.

The target is a synchronized working knowledge baseline for shared goals:
- what was learned;
- why it matters;
- source/provenance;
- affected capability;
- what the receiver already knows;
- what must be learned or tested;
- verification evidence;
- whether the lesson is reusable.

## Suggested knowledge-increment lifecycle

DISCOVERED → SHARED → RECEIVED → GAP_CHECKED → LEARNING/ALREADY_KNOWN/NOT_APPLICABLE → EXPERIMENTING → VERIFIED/REJECTED → PROMOTED → REUSED

A knowledge artifact should eventually carry fields such as:
`knowledge_id`, `discovered_by`, `sources`, `provenance`, `relevance`, `capability`, `lesson`, `experiment`, `verification`, `learned_by`, `status`.

## Meta-learning trigger

When ChatGPT or Doré notices a recurring useful behavior, ask:

> Is this only our improvised habit, or has the agent/research/open-source ecosystem already studied it?

If the answer is unknown, research before building deeply.

This applies to transport, shared learning, capability discovery, durable execution, failure recovery, relationship memory, design research, Storybook workflows, and future unknown domains.

## Westside testbed

New Westside is the parent real-world project. Storybook/Knowledge Lab is the executable design research laboratory. A2A is the collaboration/learning/recovery layer.

Therefore each real design obstacle can simultaneously:
1. advance Westside;
2. expose a capability gap;
3. trigger shared/external learning;
4. improve A2A;
5. return to Westside with a stronger joint capability.

The parent goal must survive the learning detour.

## First evidence

The Storybook runtime recovery is the first strong teacher-assisted example:
- real task failed;
- evidence exposed a knowledge gap;
- official migration knowledge was researched;
- a targeted lesson was shared with Doré;
- Doré applied the lesson;
- the original build resumed and passed.

Next maturity step: either agent should increasingly detect the gap, research/share the relevant knowledge, verify it, and resume the parent task without requiring the user to invent the recovery procedure.
