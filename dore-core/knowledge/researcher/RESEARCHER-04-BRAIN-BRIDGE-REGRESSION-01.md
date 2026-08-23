# Doré Brain → Product Bridge Regression 01

Status: PASS
Date: 2026-08-23
Trigger: Biblical Languages I Unit 1 materially changed product-readable method knowledge.
Exported node: `research.method.lemma-surface-form`

## Contract under test

The product must consume the generic brain export, preserve status/confidence boundaries, avoid swallowing Scripture references, and require no per-question hard-coded answer handler.

Implementation inspected: `static/dore/dore-brain-bridge.js`.
Brain export inspected: `static/dore/brain/knowledge-index.json`.

## Checks

### 1. Generic loading

Bridge loads `/dore/brain/knowledge-index.json` with `fetch()` and iterates `brain.nodes` generically.
Result: PASS.

### 2. Generic matching, no per-question branch

`scoreNode()` evaluates normalized `node.questions` and `node.concepts`; `chooseNode()` selects the highest node with score >= 70. No handler names or conditionals are keyed to the new lemma/form question.
Result: PASS.

### 3. New node match

Test query: `lemma 和 surface form 有什麼不同`
Expected: exact question variant -> score 100 -> `research.method.lemma-surface-form`.
Result: PASS by direct algorithm evaluation.

Test query: `原文詞形和詞元差在哪裡`
Expected: multiple concept hits (`原文`, `詞形`, `詞元`) -> score 81 -> same node.
Result: PASS by direct algorithm evaluation.

### 4. Status boundary

New node status is `CANDIDATE_FOR_EXAM`. Bridge maps this to the provisional expression state and renders node `answer.boundary` plus `next_research`.
Result: PASS.

### 5. Scripture routing preserved

Test query: `創世記 1:2`.
The new node has no matching concepts sufficient for the 70 threshold, and `scriptureLike()` independently detects Scripture-like input before brain interception.
Expected: normal Scripture search remains responsible for the query.
Result: PASS by code inspection and algorithm evaluation.

### 6. Node-driven behavior

The new answer became product-readable solely by changing `knowledge-index.json`; `static/dore/dore-brain-bridge.js` was not edited for this question.
Result: PASS.

## Regression boundary

This is a code/data contract regression, not a browser end-to-end deployment test. It verifies the current matching/rendering logic against the new node and confirms absence of hard-coded per-question logic. Network/deployment failures would be a separate product/infrastructure concern.

## Next bridge action

No bridge schema change is required. Continue using the same generic contract for later Biblical Languages nodes. Reopen this bridge test if a later unit needs structured morphology/parsing payloads the current answer schema cannot express.
