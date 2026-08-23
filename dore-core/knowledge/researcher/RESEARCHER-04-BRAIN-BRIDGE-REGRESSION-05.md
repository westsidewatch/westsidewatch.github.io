# Doré Brain → Product Bridge Regression 05

Status: PASS
Date: 2026-08-23
Trigger: Unit 9 created a product-readable Greek/Scripture-scope node.
Exported node: `research.nt.graphe-scripture-scope`

## Checks

1. Generic loading: the existing bridge fetches `static/dore/brain/knowledge-index.json` and iterates nodes generically. PASS.
2. Exact variants: `使徒時代就有聖經了嗎` and `林前15章照聖經所說是什麼聖經` resolve by the common question matcher. PASS.
3. Concept variants: combinations such as `林前15 + 聖經`, `γραφή + canon`, or `使徒時代 + Scripture` are handled by the generic concept scorer; no special handler was added. PASS.
4. Status boundary: node is `CANDIDATE_FOR_EXAM`; the renderer shows the provisional boundary and next research rather than presenting canon-history claims as fully consolidated. PASS.
5. Scripture routing: direct references such as `林前 15:3-4` and `彼後 3:16` remain Scripture-like and are handled before brain interception. PASS.
6. Node-driven behavior: Search behavior changed through the shared brain export only; `static/dore/dore-brain-bridge.js` was not edited. PASS.

## Boundary

This is a code/data regression, not a live network/deployment check. The separate sensory persistence issue remains tracked independently.

## Decision

The existing generic bridge contract is sufficient for the Unit 9 answer. No schema or per-question UI change is justified.
