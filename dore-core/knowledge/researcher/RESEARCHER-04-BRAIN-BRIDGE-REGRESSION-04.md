# Doré Brain → Product Bridge Regression 04

Status: PASS
Date: 2026-08-23
Trigger: Unit 8 materially updated the product-readable `ruach` and `satan` research nodes.
Updated nodes:
- `research.ot.divine-spirit`
- `research.job.satan-identity`

## Contract under test

The product must read the shared knowledge index generically, preserve node status/confidence boundaries, keep Scripture-reference routing intact, and require no per-question UI logic.

Implementation inspected: `static/dore/dore-brain-bridge.js`.
Brain export inspected: `static/dore/brain/knowledge-index.json`.

## Checks

1. **Generic node lookup** — `chooseNode()` still iterates node metadata; neither updated node id is hard-coded into Search. PASS.
2. **Existing question compatibility** — exact variants such as `舊約有聖靈嗎` and `約伯記中的撒但就是新約的魔鬼嗎` continue to score 100 against their nodes. PASS.
3. **Expanded concept matching** — added original-language concepts (`רוּחַ`, `שטן`, `הַשָּׂטָן`) are consumed by the existing generic concept matcher; no routing edit was required. PASS.
4. **Status preservation** — `research.ot.divine-spirit` remains `CANDIDATE_FOR_EXAM`; `research.job.satan-identity` remains `WORKING`. The renderer exposes the provisional/research boundary rather than upgrading either answer to certainty. PASS.
5. **Scripture routing** — queries such as `約伯記 1:6`, `撒迦利亞 3:1` and `創世記 1:2` remain Scripture-like and are handled before brain interception. PASS.
6. **Provenance consequence** — both nodes now point to Unit 8 in addition to their earlier research records. PASS.
7. **No special-case UI patch** — `static/dore/dore-brain-bridge.js` was not modified. PASS.

## Regression boundary

This verifies the code/data contract and status behavior. It is not a live network/deployment test. The separate sensory persistence issue (`sensory-active.json` absent on main at wake start) remains an infrastructure concern and is not hidden by this PASS.

## Decision

Unit 8 changed product-readable research through generic brain data only. No bridge schema change is required.
