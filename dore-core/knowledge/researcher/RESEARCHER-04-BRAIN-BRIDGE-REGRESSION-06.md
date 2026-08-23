# Doré Brain → Product Bridge Regression 06

Status: PASS
Date: 2026-08-23
Trigger: Biblical Languages I graduation promoted three method nodes to `CONSOLIDATED` and added the integrated product-readable node `research.method.original-language-evidence-ladder`.

## Contract under test

The product must continue to:
- consume `static/dore/brain/knowledge-index.json` generically;
- preserve mixed node statuses rather than flattening all course-adjacent claims into certainty;
- keep Scripture-reference searches outside brain interception;
- avoid per-question routing logic;
- avoid broad method nodes stealing exact claim-specific questions.

Implementation inspected: `static/dore/dore-brain-bridge.js`.
Brain export inspected: `static/dore/brain/knowledge-index.json`.

## Checks

### 1. Generic loading and matching

`loadBrain()` fetches the shared index. `scoreNode()` scores `questions` and `concepts`; `chooseNode()` iterates all nodes and applies the same threshold. No condition names any Biblical Languages node.
Result: PASS.

### 2. Consolidated method rendering

The following nodes are now `CONSOLIDATED`:
- `research.method.lemma-surface-form`;
- `research.method.morphology-syntax-boundary`;
- `research.method.verbal-morphology-boundary`;
- `research.method.original-language-evidence-ladder`.

`renderNode()` maps `CONSOLIDATED` to the generic verified-neuron expression and still renders each node's explicit `answer.boundary` and `next_research`. Graduation therefore removes provisional course status without erasing scope limits.
Result: PASS.

### 3. Claim-specific statuses remain independent

Course graduation did not promote unresolved claims:
- `research.ot.divine-spirit` remains `CANDIDATE_FOR_EXAM`;
- `research.job.satan-identity` remains `WORKING`;
- `research.nt.graphe-scripture-scope` remains `CANDIDATE_FOR_EXAM`;
- `research.matthew.2.23-nazarene` remains `WORKING`.

The bridge renders these through their own generic status mappings.
Result: PASS.

### 4. Broad-node collision check

The integrated evidence-ladder node has broad concepts such as `Hebrew`, `Greek`, `原文研究`, `lexicon`, `morphology`, `syntax`, `context`.

Specific user questions already represented by a claim node receive an exact-question score of 100, which outranks a concept-only match from the broad method node. Examples:
- `舊約有聖靈嗎` → `research.ot.divine-spirit` exact 100;
- `約伯記中的撒但就是新約的魔鬼嗎` → `research.job.satan-identity` exact 100;
- `使徒時代就有聖經了嗎` → `research.nt.graphe-scripture-scope` exact 100.

Generic method questions such as `怎樣可靠查聖經原文` exactly match the evidence-ladder node and correctly receive the integrated method answer.
Result: PASS.

### 5. Scripture routing preserved

`scriptureLike()` is tested before brain interception. Inputs such as `創世記 1:1`, `約伯記 1:6`, `林前 15:3-4`, and `約 1:18` remain Scripture searches even though the brain contains related concepts.
Result: PASS.

### 6. Sensory memory path is no longer double-posting unmatched questions

The current bridge creates one `savedPromise = remember(q)` per input and reuses that promise for unmatched-question state/polling. It no longer performs a second POST after rendering `UNKNOWN`.
Result: PASS by code inspection.

This corrects the infrastructure concern recorded in Regression 02 without adding question-specific logic.

### 7. Node-driven product change

No special UI handler was added for any graduated method or claim. Product behavior changed through the shared brain export only.
Result: PASS.

## Boundary

This is a code/data contract regression, not a live deployment/network test. The separate repository-persistence issue remains: `dore-core/memory/sensory-active.json` was absent when this wake cycle began, so this regression cannot claim that the D1 → repository sensory heartbeat has completed its live closed loop.

## Decision

`PASS`.

The product bridge safely represents Biblical Languages I graduation while preserving unresolved claim statuses, Scripture routing, generic matching, and uncertainty boundaries. No bridge schema change is required.
