# Doré A2A Reliability 1B — Existing Primitives Inventory

Status: verified inventory for consolidation. Purpose: identify which existing components should be promoted, adapted, or retired before Universal A2A Core work begins.

## Decision rule

Do not rewrite mature reliability behavior merely to make architecture look cleaner. Reuse proven primitives where their semantics are already correct; adapt only the interface/state vocabulary around them; retire only duplicate authority or route-specific glue.

## Promote directly into Universal A2A Core

### 1. Durable inbound delivery — `local/dore-local/a2a_delivery_plane.py`

Promote as the canonical ingress persistence layer.

Keep:
- checkout-independent source reading from exact ref/commit;
- canonical content hash;
- `message_id` identity;
- durable local inbox;
- dedupe for identical replay;
- quarantine for invalid messages and identity conflicts;
- delivery ACK separated from execution status;
- canonical delivery reply explicitly stating that delivery/consumer receipt is not completion evidence.

Do not duplicate this behavior in Issue relay, Unix RPC, workflow dispatch, or repository dispatch.

### 2. Durable execution truth — `local/dore-local/a2a_execution_plane.py`

Promote as the sole normal execution lifecycle authority.

Keep:
- persistent task record;
- append-only event ledger;
- claim ownership;
- expiring lease;
- heartbeat renewal API;
- artifact-before-verification ordering;
- verification-before-PASS gate;
- completion evidence derived from persisted task state.

Required adaptation before universal use:
- add runtime generation / capability generation evidence;
- make long-running handlers renew leases automatically;
- expand failure vocabulary beyond undifferentiated FAIL;
- preserve source commit/ref and normalized capability identity on every task.

### 3. Durable outbound result delivery — `local/dore-local/coordination_mailbox.py`

Promote the outbox semantics, not necessarily its current ChatGPT-specific naming.

Keep:
- durable outbox before publication attempt;
- message hash/version identity;
- retry across process restarts;
- ordered delivery;
- exact-remote idempotency check;
- isolated worktree publication;
- bounded push-race retry.

Generalize from `send_to_chatgpt()` into a transport-neutral result-delivery interface. Issue comments, workflow results, repository dispatch acknowledgements, and other caller-visible responses must become sinks of this durable result record rather than independent completion mechanisms.

### 4. Information-gain retry policy — `local/dore-local/retry_policy.py`

Promote as the default retry decision primitive.

Keep:
- failure fingerprint comparison;
- identical retry blocking;
- bounded retry budget;
- exponential backoff + jitter;
- `RESEARCH_OR_STOP` when budget is exhausted.

Adapt its actions into the unified execution lifecycle vocabulary.

### 5. Stall supervision — `local/dore-local/a2a_supervisor.py`

Promote its observation semantics into Core supervision.

Keep:
- unchanged-cycle detection;
- explicit distinction between human gate, peer pending, project pass and autonomous-recovery need;
- non-blocking peer absence;
- mandatory intervention instead of silent observation.

Adapt:
- source its state from canonical execution/recovery records rather than parallel worker-specific state;
- emit standard lifecycle transitions instead of a separate A2A state vocabulary.

## Promote as canonical identity authority, but extend before use

### 6. JSON capability registry — `dore-core/runtime/capability-registry.v1.json`

This is the strongest existing candidate for the single capability identity source because it already declares:

- owner: `dore-core`;
- purpose: canonical semantic capability discovery for every Doré product surface;
- product surfaces request capabilities by name rather than owning provider addresses;
- deferred / replaceable adapters;
- evidence-before-learning.

`local/dore-local/capability_registry.py` already enforces schema ownership by `dore-core`.

Promote this registry to the one descriptor authority, but extend the descriptor schema to include at least:
- callable status derived from registered handler binding rather than a second list;
- execution class (`normal`, `production-mutation`, `acceptance-job`, `training-job`, `recovery-plane`);
- timeout profile;
- lease profile / heartbeat interval;
- artifact contract;
- verification contract;
- recovery policy;
- runtime generation compatibility;
- handler binding / adapter binding;
- side-effect classification;
- release/graduation metadata.

Do not maintain a second Python capability registry with overlapping identity.

## Adapt, do not promote as independent authority

### 7. Typed Core transport / control-plane envelope

Keep the typed `dore.a2a/1` semantics as the normalized internal contract.

Do not require every external transport to construct that full shape itself. Build one normalization boundary that accepts public `dore.call` and produces the canonical envelope.

The public shape and internal shape can differ; what is forbidden is an unbridged discontinuity.

### 8. `native_host` lazy optional-module loading

Keep the fault-isolation behavior: one broken optional module must not take down unrelated A2A capabilities.

Do not keep `native_host` as an independent capability authority.

Adapt lazy cache to a generation contract:
- active control-plane commit;
- active runtime generation;
- registry hash;
- loaded capability generations;
- restart-required flag.

## Demote / retire after consolidation

### 9. Direct-module capability registration

Retire as a normal registration mechanism.

Allowed survivor:
- minimal recovery/bootstrap escape hatch such as `system.self-maintain`.

Demote Design live acceptance, Theology acceptance/training, and similar routes into canonical job/test profiles.

### 10. Production Bus hard-coded native capability identity

Retire duplicate identity ownership. It may survive temporarily as a compatibility adapter that binds canonical registry descriptors to handlers, but it must not independently decide what capabilities exist.

### 11. Python visual registry as a second semantic authority

Retire overlapping capability identity. Its handler/provider logic may remain, but descriptor identity must come from the canonical registry.

### 12. Route-specific completion truth

Retire any convention where handler return, RPC response, workflow success, or Issue comment is treated as task completion by itself.

Completion truth must come only from the durable execution record with verified artifact evidence.

## Consolidation map

```text
External transports
Issue / workflow_dispatch / repository_dispatch / Unix caller
                         |
                         v
                Normalization Boundary
                         |
                  dore.a2a/1 envelope
                         |
              Canonical Capability Registry
                         |
                 Handler Binding Layer
                         |
                Durable Execution Plane
             / claim / lease / heartbeat \
                         |
                  Capability Handler
                         |
                 Artifact + Verification
                         |
                  Canonical Completion
                         |
                 Durable Result Outbox
                         |
                  Caller-visible sink
```

## 1B conclusion

Universal A2A Core does not need a new reliability stack. The proven stack already exists in fragments.

The components that should become the common substrate are:

1. `a2a_delivery_plane.py` — inbound durability and identity;
2. canonical JSON capability registry — capability identity;
3. typed `dore.a2a/1` envelope — normalized internal request contract;
4. `a2a_execution_plane.py` — execution truth;
5. `retry_policy.py` + supervisor semantics — recovery decisions;
6. durable outbox semantics from `coordination_mailbox.py` — result delivery.

The main engineering work for 1C is therefore consolidation and compulsory routing, not reinvention.

## 1C entry criteria

Begin consolidation only with these invariants fixed:

- one capability identity source;
- one normal execution authority;
- one normalized internal envelope;
- transports may differ, execution truth may not;
- every long task has lease renewal;
- every terminal PASS has verified completion evidence;
- every caller-visible result is recoverable from durable state after transport loss;
- adding a Doré project adds a capability only, never another A2A route.
