# Doré Brain → Product Bridge Regression 03

Status: PASS
Date: 2026-08-23
Trigger: Biblical Languages I Unit 4 materially changed product-readable verbal-morphology method knowledge.
Exported node: `research.method.verbal-morphology-boundary`

## Checks

1. Generic loading: `static/dore/dore-brain-bridge.js` fetches the shared knowledge index and iterates nodes generically. PASS.
2. Generic matching: no branch was added for aorist, Hebrew Perfect, Piel, or this node id. Exact question variants score 100; multi-concept variants can qualify via the common concept matcher. PASS.
3. Status boundary: node is `CANDIDATE_FOR_EXAM`; the bridge renders provisional state, boundary, and next-research items. PASS.
4. Scripture routing: `scriptureLike()` remains checked before brain interception; reference searches are not swallowed by the new method node. PASS.
5. Node-driven behavior: the answer became product-readable through `static/dore/brain/knowledge-index.json` only; no per-question UI logic was added. PASS.

## Test examples

- `aorist 是不是 once for all` → exact question variant → new verbal-morphology node.
- `希伯來文 perfect 是不是過去式` → exact question variant → new node.
- `Piel 是不是一定表示加強語氣` → exact question variant → new node.
- `羅馬書 6:10` → Scripture-like routing remains responsible.

## Boundary

This is a code/data contract regression, not a live deployment/network test. It verifies that Unit 4 knowledge can alter product behavior generically while preserving provisional status and Scripture routing.

No bridge schema change is required.
