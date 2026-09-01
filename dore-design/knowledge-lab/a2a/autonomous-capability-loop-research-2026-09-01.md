# Autonomous Capability Loop — Prior Art Map

Date: 2026-09-01
Purpose: turn the Doré/ChatGPT/New Westside recursive learning idea into an evidence-backed architecture by reusing mature research and tools.

## Our loop

GOAL → ATTEMPT → OBSERVE → GAP → RESEARCH → LEARN → EXPERIMENT → VERIFY → PROMOTE → RESUME

Meta-loop: observe the loop itself → identify manual/friction points → research prior art → improve the loop → verify on the same parent goal.

## Strong prior art

### Voyager — lifelong learning + automatic curriculum + executable skill library
Source: MineDojo/Voyager, MIT.
Key reusable ideas:
- automatic curriculum selects useful next challenges;
- ever-growing executable skill library stores successful behaviors;
- environment feedback + execution errors + self-verification improve programs iteratively;
- learned skills are retrieved and composed for new tasks.
Doré mapping: real Westside tasks become curriculum; Knowledge Lab/Westside Core becomes skill library; failures generate learning tasks; successful Storybook/design/search procedures become reusable capabilities.

### Reflexion — learn from failure without weight updates
Source: Shinn et al., arXiv 2303.11366.
Key reusable idea: convert task feedback into linguistic reflection, keep it in episodic memory, and use it to improve later trials.
Doré mapping: a FAIL should produce a structured lesson/failure memory, not merely a retry count.

### Self-Refine — feedback → refinement loop
Source: Madaan et al., arXiv 2303.17651.
Key reusable idea: generate, critique, refine repeatedly without requiring model fine-tuning.
Doré mapping: Storybook specimens and search/design outputs can be iteratively critiqued against explicit acceptance criteria before promotion.

### LangGraph — durable stateful execution
Source: official LangGraph docs.
Key reusable ideas:
- durable execution;
- checkpoints/persistence;
- resumable interrupts;
- streaming;
- long-term stores across threads.
Doré mapping: the parent goal must survive learning detours, transport failures, restarts, and human-only gates. A learning excursion should be a resumable state transition, not abandonment of the original task.

### OpenHands Skills — reusable and repository-specific capabilities
Source: OpenHands/OpenHands and OpenHands/extensions.
Key reusable ideas:
- shareable skills for general expertise;
- repository-specific skills automatically loaded for project conventions;
- trigger/context-based loading;
- versioned reusable knowledge;
- skills can include executable plugins/hooks/scripts.
Doré mapping: split durable knowledge into general capabilities and Westside-specific capabilities; retrieve only relevant skills when needed rather than flooding context.

### DSPy — optimize programs against metrics rather than hand-tune prompts
Source: official DSPy project, MIT.
Key reusable idea: express AI behavior as structured programs/signatures that can be optimized and evaluated against examples/metrics.
Doré mapping: later candidate for optimizing repeatable research/search/evaluation modules once Doré has reliable datasets and acceptance metrics. Do not adopt prematurely.

## Architectural synthesis

Do not clone any one framework. Reuse concepts by layer:
- A2A: inter-agent communication and capability exchange.
- Durable runtime pattern (LangGraph-like): parent-goal state, checkpoints, resume.
- Voyager-like curriculum + skill library: turn real work into progressive capability acquisition.
- Reflexion-like failure memory: every meaningful failure produces reusable evidence/lesson.
- Self-Refine-like critique loop: iterate artifacts until acceptance or information-gain exhaustion.
- OpenHands-like skills: general + repository-specific knowledge with selective activation.
- Storybook/Knowledge Lab: executable visual/design laboratory and verification environment.

## Proposed Doré states

GOAL
ATTEMPTING
OBSERVING
GAP_DETECTED
RESEARCHING
LEARNING
EXPERIMENTING
VERIFYING
PROMOTING
RESUMING
PASS
HUMAN_GATE

Failure is not automatically terminal. It is an observation that may transition to GAP_DETECTED. Terminal failure should mean no safe next step or no information-gain path remains.

## Promotion rule

A lesson becomes a reusable capability only when it has:
1. provenance/source;
2. a concrete problem it solves;
3. an executable or inspectable procedure;
4. verification evidence from real work or a controlled experiment;
5. scope/limitations;
6. retrieval trigger or capability metadata.

## Immediate experiment

Use New Westside visual construction as the live curriculum. The next unfamiliar design/Storybook implementation problem should be allowed to trigger GAP_DETECTED. Doré should then inspect existing Knowledge Lab skills; if insufficient, research authoritative docs/mature OSS; create a minimal specimen/experiment; verify it; promote the lesson if reusable; and resume the original Westside visual task.

Success criterion: the parent visual goal advances and the new reusable capability is evidenced. Stronger milestone: Doré initiates this learning detour without ChatGPT explicitly prescribing the missing technical lesson.

## Principle

Automation is not only automatic execution of known steps. The target capability is increasingly automatic acquisition, verification, storage, retrieval, and reuse of the knowledge needed to complete previously unknown work.
