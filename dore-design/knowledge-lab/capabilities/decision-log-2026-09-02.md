# Doré Search Capability Upgrade — Research → Engineering Decision

## Why this exists

The project initially risked creating a second `Doré Search`. That direction was rejected because Doré already owns Search and AI Conversation. The enhancement must preserve those capabilities and add discovery around them.

## Phase 0 research lessons promoted into engineering

1. Large tool collections should not all be exposed at once. Use compact/deferred discovery.
2. Capability selection should be hierarchical (type/service/tool) rather than one flat tool list.
3. Discovery should be dynamic: execution may reveal that a different capability is needed next.
4. Registry descriptions should be objective structured metadata rather than provider marketing prose.
5. Tool-use outcomes should later become experience memory, but only after evidence.
6. Registry/discovery is not the execution owner. Native tools keep their protocols and implementations.
7. Free/local-first is a hard baseline for Doré; paid API dependencies are not accepted.

## First engineering hypothesis

A thin registry can describe existing Doré Bible capabilities without changing `/dore/dore-search.js`. If acceptance proves that boundary, new `library.books` adapters can be added behind deferred discovery without rebuilding Search.

## Learning record for Doré

This change records the project method itself:

`need → inspect existing capability → research mature patterns → reject conflicting architecture → define minimal hypothesis → isolate branch → acceptance before promotion → only then add new capability`

This is intended to become part of Doré's future engineering judgement, not merely implementation documentation.
