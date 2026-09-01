# Autonomous Capability Loop — Maturity Curriculum

Date: 2026-09-01
Parent goal: New Westside visual construction

## Why now

Doré Autonomous Capability Loop v0.1 has a verified closed-loop acceptance: failure → capability-gap match → executable skill → repair → resume parent goal → PASS. The next step is not to invent a large framework. It is to absorb mature patterns and extend the smallest working loop while New Westside/Storybook remains the real task.

## Mature patterns to absorb

### Voyager — automatic curriculum + executable skill library
Source: MineDojo/Voyager (MIT).
Adopt the pattern, not the Minecraft implementation:
- generate/choose the next useful learning objective from current environment and capability gaps;
- store successful behavior as executable, retrievable skills;
- incorporate execution errors and environment feedback;
- self-verify before promoting a skill;
- compose prior skills for harder tasks.

Doré adaptation: the curriculum must be subordinate to the parent real-world goal. New Westside is the environment/task source; Storybook is the controlled experiment surface; Knowledge Lab is the growing skill/evidence library.

### Reflexion — failure memory
Source: Shinn et al., Reflexion (2023).
Adopt:
- turn task feedback/errors into compact reusable reflection;
- persist the reflection with the failure fingerprint and later outcome;
- retrieve relevant prior failures before repeating an approach.

Doré adaptation: a retry without new evidence, knowledge, tool, or hypothesis is not progress.

### LangGraph — durable state/checkpoint semantics
Source: official LangGraph persistence/interrupt docs.
Adopt semantics before dependency:
- checkpoint state at meaningful lifecycle boundaries;
- preserve parent task identity and state through learning detours;
- resume from the last valid checkpoint;
- make side effects idempotent/replay-safe;
- reserve explicit interrupt for genuine human gates.

Do not add LangGraph as a dependency merely for fashion. Doré already has a working worker/state mechanism; first reproduce the useful semantics in the existing architecture and evaluate dependency adoption only when it provides measurable value.

### OpenHands Skills — progressive reusable skill packaging
Source: OpenHands skills/extensions docs and repository.
Adopt:
- separate shareable/general skills from repository-specific skills;
- concise trigger/description metadata;
- progressive disclosure: enough metadata to decide relevance, detailed references/scripts only when activated;
- skills may include executable scripts/hooks;
- monitor skill performance and revise weak skills.

Doré adaptation: evolve registry.json toward skill directories with SKILL.md + optional scripts/references/evidence, while preserving compatibility with the current registry during migration.

## Maturity loop v0.2 target

GOAL
→ ATTEMPT
→ OBSERVE
→ GAP_DETECTED
→ RETRIEVE_SKILL_OR_FAILURE_MEMORY
→ if known: LEARN/APPLY
→ if unknown: RESEARCH_REQUIRED
→ EXPERIMENT
→ VERIFY
→ PROMOTE_SKILL_OR_REFLECTION
→ CHECKPOINT
→ RESUME_PARENT
→ PASS / new observation

## Critical missing capability

v0.1 can recover when an appropriate skill is already registered. v0.2 must make an unknown gap a first-class state rather than terminal failure.

For the first increment, implement an evidence-producing `RESEARCH_REQUIRED` path that:
1. fingerprints the unknown failure;
2. records parent goal/checkpoint;
3. searches local Knowledge Lab/skills/failure memory first;
4. creates a structured research request/artifact when local knowledge is insufficient;
5. does not blindly retry;
6. preserves enough state for the new knowledge/skill to be installed and the same parent task resumed.

A later increment can connect this request to external research automatically. Do not fake external research from the local worker if it has no trustworthy research capability yet.

## Storybook/New Westside coupling

Do not create artificial curriculum exercises after this acceptance. Use actual New Westside visual construction as the curriculum generator.

When Doré encounters an unfamiliar layout, animation, responsive behavior, asset treatment, accessibility issue, Storybook behavior, build/tooling issue, or visual-test requirement:
- first retrieve known skills/evidence;
- if insufficient, enter RESEARCH_REQUIRED;
- research mature references/tools/implementations;
- create the smallest Storybook specimen that answers the question;
- verify;
- promote reusable knowledge;
- return to the real New Westside surface.

Locked approved homepage #262 remains a control/reference and must not be modified without explicit direction.

## Acceptance criteria for v0.2

PASS requires evidence that:
- an unknown capability gap does not immediately become blind RETRYING;
- a structured RESEARCH_REQUIRED artifact is produced automatically;
- parent goal and failure fingerprint survive;
- prior failure/skill knowledge is checked before escalation;
- the architecture has a resumable handoff point for newly acquired knowledge;
- existing v0.1 Storybook recovery still works.
