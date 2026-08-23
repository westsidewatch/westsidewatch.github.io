# Doré Brain → Product Bridge Regression 02

Status: PASS_WITH_INFRASTRUCTURE_NOTE
Date: 2026-08-23
Trigger: Biblical Languages I Units 2–3 materially changed product-readable method knowledge.
Exported node: `research.method.morphology-syntax-boundary`

## Contract under test

The product must consume the generic brain export, preserve status/confidence boundaries, avoid swallowing Scripture references, and require no per-question hard-coded answer handler.

Implementation inspected: `static/dore/dore-brain-bridge.js`.
Brain export inspected: `static/dore/brain/knowledge-index.json`.

## Checks

### 1. Generic loading

The bridge fetches `/dore/brain/knowledge-index.json` and iterates `brain.nodes` generically.
Result: PASS.

### 2. Generic matching

`scoreNode()` checks normalized `questions` and `concepts`; `chooseNode()` selects the highest-scoring node above the generic threshold. There is no branch keyed to morphology, Greek case, Hebrew construct state, or this new node id.
Result: PASS.

### 3. Exact question variants

Queries represented directly in the exported node, including `原文形態標籤可以直接告訴我意思嗎`, `希臘文 case 是不是等於固定翻譯`, and `希伯來文 construct state 是不是就是所有格`, receive an exact-question score and resolve to the new node.
Result: PASS by direct algorithm inspection.

### 4. Concept-driven variants

Queries containing multiple node concepts such as `Greek genitive case 固定翻譯嗎` or `Hebrew construct state 所有格` have enough concept overlap to be eligible for the same generic matcher without any UI edit.
Result: PASS by algorithm inspection; natural-language coverage should continue to be expanded from real failures rather than guessed exhaustively.

### 5. Status boundary

The node is `CANDIDATE_FOR_EXAM`. `renderNode()` maps that state to the provisional expression and renders the answer boundary and `next_research` items.
Result: PASS.

### 6. Scripture routing

`scriptureLike()` is checked before brain interception. Scripture-reference inputs such as `創世記 1:1` remain under Scripture search rather than being consumed by the method node.
Result: PASS.

### 7. Node-driven behavior

No change to `static/dore/dore-brain-bridge.js` was needed to expose the new knowledge. Product-readable behavior changed only through the generic brain export.
Result: PASS.

## Infrastructure note discovered before this regression

`dore-core/memory/sensory-active.json` was absent when this wake cycle began. Therefore no repository-persisted `RESEARCHING` sensory signal could be inspected or responsibly reconstructed. This is treated as an ingestion/heartbeat persistence gap, not evidence that no live signal exists in D1. No sensory question was fabricated from memory or guessed into the file.

A separate code observation: the current Search bridge calls `remember(q)` once for every input and a second time for an unmatched question after rendering `UNKNOWN`. If the ingestion endpoint increments `heard_count` per POST, a single unmatched question may be heard twice. This is a product/infrastructure issue to verify separately; it does not invalidate this node regression.

## Decision

The generic brain contract remains sufficient for Units 2–3. No schema or per-question routing change is justified.

Next bridge action: reopen only if Unit 4 or later learning requires structured grammatical payloads that cannot be expressed by the current generic answer schema, or if real Search failures demonstrate matcher inadequacy.
