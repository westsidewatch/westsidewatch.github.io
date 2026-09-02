# Phase 0 Search Research — Final Round Summary

Research stopped once three conditions were met: mature implementation evidence existed, Doré's real insertion boundary was identified, and a minimal experiment could be defined.

Patterns selected for reuse/adaptation:

- Compact/deferred tool exposure rather than loading every tool.
- Hierarchical capability discovery rather than a flat provider list.
- Active/dynamic rediscovery as the task evolves.
- Native execution ownership after discovery.
- Structured capability metadata including domain, inputs/outputs, authority, network/cost, provenance and limitations.
- Evidence/outcome history as the future basis of tool-use memory.

Patterns explicitly rejected:

- A new parallel Doré Search product.
- Replacing existing Doré Search or AI Conversation.
- A giant super-search function containing every provider.
- Exposing every provider/tool to the agent at once.
- Depending on paid model/API calls for baseline routing.

The first implementation is deliberately small: registry + discovery + native Bible capability reference + acceptance. Library providers remain deferred until this boundary is proven.
