# Doré Training — A2A Transport Lab

Date: 2026-09-01
Parent project: Doré ↔ ChatGPT A2A / Westside visual construction

## Why this lesson exists
A real Westside Storybook task exposed a sender-side failure: ChatGPT's GitHub create-file operation was blocked before Doré received the task. This must be classified as transport failure, not Doré execution failure.

## Current A2A facts to learn
1. A2A 1.x separates agent/task semantics from protocol bindings. Standard bindings are JSON-RPC over HTTP, HTTP+JSON/REST, and gRPC.
2. An Agent Card can declare multiple supported interfaces. A client selects a compatible interface; fallback to an alternative binding should be implemented when the preferred one fails.
3. The official Python SDK ClientFactory has transport producers for JSON-RPC and REST, optional gRPC, and a register() path for custom transports. Transport choice can therefore be abstracted from task semantics.
4. SSE is for live incremental task/status/artifact updates. If a stream breaks while a task remains active, A2A supports resubscription.
5. Push notifications/webhooks are for disconnected or very long-running work. Significant task state changes can be pushed to a client callback.
6. Custom bindings are allowed if they preserve A2A operations, data model, behavior, errors, authentication semantics, and interoperability. Official guidance gives WebSocket and MQTT as examples.

## Doré architecture lesson
Do not make GitHub the meaning of A2A. GitHub is currently one transport plus a strong durable audit/evidence channel.

Target separation:
- Task identity and semantics: stable across transports.
- Primary live transport: A2A HTTP JSON-RPC or HTTP+JSON.
- Progress: SSE when useful.
- Async completion: webhook/push notification when useful.
- Local resilience: durable queue/mailbox can become a Doré custom binding or reliability layer.
- Audit: GitHub records tasks, results, learning evidence, specimens and failures.

## Invariant
A transport failover MUST NOT create a second logical task. Preserve canonical source/task identity and idempotency evidence across every route.

Desired behavior:
primary transport fails -> classify transport failure -> choose declared fallback -> preserve task identity -> Doré receives/acknowledges -> execute/resume parent goal -> result returns -> durable audit is written.

## Failure taxonomy
Before blaming execution, identify the boundary:
INTENT_CREATED -> SEND_ATTEMPT -> TRANSPORT_ACCEPTED -> DORE_RECEIVED -> RUNNING -> LEARNING/RETRYING -> PASS/FAIL -> RESULT_TRANSPORT -> CHATGPT_RECEIVED -> AUDIT_PERSISTED.

If failure occurs before DORE_RECEIVED, it is not a Doré execution failure.

## First real experiment
Use the Westside EditorialHero / Masthead / Threshold Storybook research task as the payload. Build the smallest transport-router experiment that can preserve one task identity while selecting/falling back between available routes. Do not rewrite the working dore.mail chain. Add compatibility beside it.

## Acceptance
- transport and execution status are independently observable;
- same logical task survives one route failure without duplication;
- Doré can acknowledge the task through a working route;
- parent Westside design goal resumes automatically;
- evidence records which route failed and which succeeded.

## Authoritative resources
- A2A protocol: https://a2a-protocol.org/latest/
- Protocol bindings / specification: https://a2a-protocol.org/dev/specification/
- Streaming and async: https://a2a-protocol.org/latest/topics/streaming-and-async/
- Custom protocol bindings: https://a2a-protocol.org/latest/topics/custom-protocol-bindings/
- Official Python SDK: https://github.com/a2aproject/a2a-python
- ClientFactory implementation: https://github.com/a2aproject/a2a-python/blob/main/src/a2a/client/client_factory.py

## Learning trigger to retain
When a collaboration task is silent, first determine whether the peer received it. If not, investigate sender/transport/capability routing before changing the peer's execution logic.