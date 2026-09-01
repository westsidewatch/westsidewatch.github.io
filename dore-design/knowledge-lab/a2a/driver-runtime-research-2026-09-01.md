# Doré A2A — Autonomous Driver Runtime Research

Date: 2026-09-01
Status: research-to-adoption

## Problem proven by the silent road test

A2A transport, worker execution, skills and a Driver script are insufficient if nothing owns the next turn after the human/chat window disappears. The missing capability is a resident autonomous orchestration/runtime layer.

## Mature evidence

### Microsoft Agent Framework — Autonomous Handoff
Source: https://github.com/microsoft/agent-framework
Docs/sample: `HandoffBuilder.with_autonomous_mode()`.

Key reusable idea: interactive handoff normally returns control to the user when an agent responds without handing off. Autonomous mode instead supplies a continuation turn and invokes the agent again until handoff, termination, or turn limit. This is almost exactly Doré's current control-flow gap.

Adopt the control principle, not Azure/Foundry dependency: **no user response becomes a continuation event owned by the runtime**.

### A2A Protocol 1.x — stateful async Tasks
Source: https://a2a-protocol.org/latest/

Reusable ideas: Task is stateful and independent of a particular client connection; processing may continue asynchronously; clients can observe via polling, SSE, or push notifications/webhooks. Task lifecycle is independent of an individual stream lifecycle.

Adopt as interoperability/observation semantics. A2A is not itself the scheduler/driver.

### LangGraph — persistence/checkpoint/resume
Source: https://github.com/langchain-ai/langgraph
License: MIT.

Reusable idea: persist graph state/checkpoints so long-running work can resume after interruption instead of depending on a chat turn or process memory.

Adopt first as architecture/pattern. Do not require LangGraph package merely to solve the first local loop if stdlib persistence is sufficient.

### OpenHands — agent runtime/event architecture and skills
Sources: https://github.com/OpenHands/OpenHands and https://github.com/OpenHands/software-agent-sdk
License: MIT for the open-source project components reviewed.

Reusable ideas: agent server/event stream, conversation state, reconnectable observation, reusable skills. Useful reference for separating execution events from UI observation.

### Temporal — durable workflow runtime
Source: https://github.com/temporalio/temporal

Reusable ideas: durable timers, task queues, retries and crash recovery. Strong future candidate when Doré needs multi-process/distributed durability. Too heavy for the first local resident loop; defer installation.

## Architectural conclusion

Do not search for one mythical `driver` package and replace Doré with it. Mature systems separate four responsibilities:

1. **Resident runtime** — owns wakeup/next-turn scheduling.
2. **Durable state machine** — owns parent goal, checkpoint, attempt, next action.
3. **Agent orchestration policy** — chooses Doré/research/skill/verify/human gate.
4. **A2A observation/interop** — carries Task/status/artifact events without requiring the chat UI to remain connected.

Doré should compose these proven patterns around the capabilities it already has.

## Doré Driver v0.2 target

State machine:
`GOAL -> PLAN -> ACT -> OBSERVE -> DECIDE -> NEXT_ACTION -> ACT ...`
Failure branch:
`OBSERVE -> STALL/FAIL -> DIAGNOSE -> KNOWN_SKILL or RESEARCH -> EXPERIMENT -> VERIFY -> PROMOTE -> RESUME`
Only genuine external authorization becomes `HUMAN_GATE`.

Resident wakeup sources:
- inbox/event arrival
- child-process result
- task-state transition
- retry timer
- heartbeat/stall timeout
- research result

The runtime MUST create its own continuation event when none of the above arrives before the stall deadline. Human silence is not a stop condition.

## Free-first adoption decision

- Adopt A2A protocol semantics and official OSS SDK compatibility incrementally.
- Adopt Microsoft Agent Framework autonomous-mode **continuation policy** as a design pattern, but avoid Foundry/Azure paid dependency.
- Adopt LangGraph checkpoint/resume concepts; evaluate package only where it removes code rather than adds complexity.
- Adopt OpenHands event/skills patterns selectively.
- Defer Temporal until scale/durability justifies a resident server dependency.
- Keep first Driver runtime local, stdlib-first, launchd-compatible on macOS, with no paid model/API requirement.

## First acceptance

A resident process must remain alive independently of ChatGPT and:
1. preserve the New Westside parent goal;
2. notice the current Storybook stall;
3. choose and execute another action without a user message;
4. persist each state/evidence transition;
5. continue for a silent observation window;
6. stop only on PASS or genuine HUMAN_GATE.

The chat window is telemetry/command UI, never the clock or accelerator.