# Doré A2A Reliability Atlas v1

Status: archaeology baseline. This document records verified reliability history and classifies root causes before consolidation into Universal A2A Core.

## Core finding

Doré already contains many mature reliability primitives, but they are distributed across transports, direct modules, capability registries, execution paths, recovery loops and result delivery. The primary systemic failure is not absence of reliability logic; it is absence of one compulsory public path that every capability must traverse.

The current public Unix invocation path does **not** naturally enter the typed Core control plane. `dore.call` uses `capability/args`, while the typed Core requires a `dore.a2a/1` envelope with `consumer_id`, `capability_id`, `payload`, `request_id`, `conversation_id`, and `session_id`. The adapter only accepts payloads that already contain `protocol: dore.a2a/1`. Therefore the ordinary Unix path reaches direct modules or the Production Bus, but the typed adapter is normally unreachable.

## Reliability layers

1. Entry transport
2. Durable delivery
3. Capability identity / discovery authority
4. Routing / normalization
5. Runtime generation / resident version
6. Durable execution
7. Lease / retry / recovery
8. Artifact verification / completion evidence
9. Durable result delivery

A pass in one layer never substitutes for a pass in the next layer.

## Root-cause classes

### R1 — Capability identity split

There is no single capability authority. At least these authorities coexist:

- canonical JSON capability registry;
- Python visual registry;
- Production Bus hard-coded native capabilities;
- `native_host` direct-module capability sets.

Consequence: discovery success, callability and actual execution can disagree.

### R2 — Public-path schema discontinuity

Ordinary Unix `dore.call` produces a payload shaped around `capability/args`; the typed Core transport expects the full `dore.a2a/1` dispatch envelope. No normalization bridge currently converts the former into the latter.

Consequence: adapter presence is mistaken for adapter reachability. Capabilities that appear connected to Core may actually be running through side routes.

### R3 — Parallel execution authorities

`native_host` can execute through:

- direct local modules;
- Production Bus;
- typed adapter / Python Core when an already-typed envelope is supplied.

Some specialized subsystems, such as Design Intelligence, then create their own durable execution task after entering their local bridge.

Consequence: capability execution truth depends on route.

### R4 — Runtime generation drift

Repository HEAD is not active-runtime identity. `native_host` lazily caches modules. Updating GitHub code does not update a resident launchd process until its generation is replaced.

Historical attempts to refresh the control plane inside or immediately before active RPCs caused response loss and relay instability.

Consequence: code may be merged while the machine still executes an older routing generation.

### R5 — Response orchestration gap

Historical A2A response stall proved that durable delivery and resident heartbeat can both succeed while no substantive response is emitted. The first missing transition was `RECEIVED -> TASK_REGISTERED`.

Consequence: heartbeat is not response evidence; delivery ACK is not execution completion.

### R6 — Recovery vocabulary split

Lease reclaim, retry policy, stall supervision, research handoff and worker state exist, but use different state vocabularies.

Consequence: retryable failure, terminal failure, quarantine, research-required and worker-loss are not yet represented as one execution lifecycle.

### R7 — Long-task lease gap

The durable execution plane provides lease heartbeat renewal, but long-running consumers do not universally renew leases. Existing task profiles can run far longer than the default lease.

Consequence: correct long-running work may finish after its lease expires and then fail to record artifact / verification / completion evidence.

## Verified mature primitives already present

- durable delivery independent of execution checkout;
- exact source ref / source commit evidence;
- content hash and message-id idempotency identity;
- dedupe / conflict quarantine concepts;
- durable execution task records;
- claim ownership and expiring leases;
- artifact recording before completion;
- verification gate before PASS;
- completion evidence;
- durable outbound outbox;
- retryable result publication;
- isolated Git worktree publication;
- information-gain retry policy;
- stall detection and autonomous-recovery signal;
- resident supervision of coordination worker;
- capability-specific timeout history;
- optional-module degradation isolation;
- explicit same-UID Unix-socket peer validation.

## Direct-module classification

### Recovery / bootstrap escape hatch

- `system.self-maintain`

May remain a very small recovery-plane capability because it can be needed to repair the control plane itself.

### Acceptance / training harnesses

Examples:

- `design.intelligence.live.acceptance`
- `theology.live.acceptance`
- theology training readiness / micro / eval / recovery actions

These should become canonical test/job profiles, not permanent parallel capability registries.

### Production mutation

- `dawn.library.publish`

This must become a canonical capability and must be forced through durable execution + verified completion because it mutates repository state and pushes production changes.

## Failure Atlas rules

1. Transport does not own execution truth.
2. Active execution must never update or restart the control plane carrying that execution.
3. Control-plane upgrade and capability execution must be separated.
4. Timeout is a capability profile, not a global constant.
5. Delivery and execution checkout must be decoupled.
6. Exact source ref/commit must be preserved and validated.
7. launchd/self-hosted runner environment must be explicit.
8. Outbound result delivery must be durable, retryable and non-lossy.
9. Delivery ACK != execution receipt != verified completion.
10. `message_id + canonical content hash` is idempotency identity; conflicts quarantine.
11. Capability routing requires one authoritative registry/resolve path.
12. All normal capability execution must be forced through one durable execution truth.
13. Bootstrap escape hatches must not become general capability-registration mechanisms.
14. Acceptance success is not infrastructure graduation.
15. Production side-effect capabilities require durable execution and verified evidence.
16. Repository HEAD != active runtime generation.
17. Control plane must never restart inside active RPC.
18. Lazy module cache must be bound to generation/version identity.
19. Transport lifetime and capability generation must be independently managed.
20. Heartbeat is not response evidence.
21. `RECEIVED` is not `RUNNING`; deferment must be explicit.
22. Completion must produce canonical execution evidence.
23. Result delivery must be durable, idempotent and retryable.
24. Resident liveness must cover the actual response worker.
25. Lease existence is not lease safety; long jobs require heartbeat renewal.
26. Retry requires information gain; identical retry loops are forbidden.
27. Worker crash recovery should use lease reclaim, not manual state clearing.
28. Poison messages must be isolated from the rest of the queue.
29. Execution failure must distinguish retryable / terminal / quarantined / research-required states.
30. Supervisor, retry policy, execution plane and goal queue must converge on one lifecycle vocabulary.
31. Public transport and typed Core currently have a schema discontinuity.
32. `dore.call` and typed Core use incompatible invocation schemas without a normalization bridge.
33. Adapter presence != adapter reachability.
34. Direct-capability success is not proof that Universal Core is connected.

## Root problems vs symptoms

### Root problems

- split capability identity;
- public-path schema discontinuity;
- parallel execution authorities;
- runtime-generation drift;
- recovery-state fragmentation.

### Symptoms

- new capability needs another direct module;
- capability visible in one discovery path but not callable from another;
- merged code not visible on the Mac;
- successful delivery with no substantive reply;
- request timeout although work may still be executing;
- repeated per-project timeout/refresh patches;
- successful subsystem acceptance without infrastructure graduation.

## Consolidation target

The target architecture is:

```text
Issue / workflow_dispatch / repository_dispatch / local caller
                    |
                    v
          Universal A2A Ingress
                    |
          normalize one envelope
                    |
          canonical capability authority
                    |
          durable execution plane
                    |
       capability handler / worker
                    |
          artifact + verification
                    |
          canonical completion receipt
                    |
          durable result delivery
```

Adding a Doré project must add only a Capability. It must not add another A2A transport, registry, execution authority or result-delivery mechanism.

## 1B / 1C work queue

1. Define one canonical capability descriptor source.
2. Add a normalization boundary from public `dore.call` into the typed Core envelope.
3. Make durable execution a compulsory wrapper for normal capability execution.
4. Add runtime-generation identity to health/discovery.
5. Add lease-heartbeat support for long-running jobs.
6. Unify retry/recovery/quarantine/research states.
7. Demote acceptance/training direct modules to job/test profiles.
8. Keep only a minimal recovery-plane escape hatch.
9. Move production mutation capabilities, including Dawn publication, behind the canonical execution path.
10. Run failure-injection acceptance before Living Water becomes the first real consumer.

## Acceptance principle

Universal A2A is not considered connected because a capability can be made to run. It is connected only when a newly registered capability, with no bespoke route, can be discovered, invoked, durably executed, verified, recovered after injected failure, and have its result durably returned through the same common path.
