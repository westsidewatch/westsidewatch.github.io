# Researcher 06 — Unit 08 Fresh Final

Status: **V2 FROZEN / ONE-SHOT FINAL DISPATCHED / RESULT PENDING**
Date: 2026-08-24

## Preemption check
`dore-core/memory/sensory-active.json` was inspected first. No `RESEARCHING` signal without a `brain_node` exists; the Mary signal remains `CONSOLIDATED`. No sensory research preempted this unit.

## Development evidence
The durable v2 development gate is present and passing:
- deterministic dev partition: `sha256(entity-id\0surface) mod 10 in {0,1}`;
- inspected rows: 601;
- Han occurrences: 3,123;
- unknown Han: 0;
- empty encoding keys: 0;
- `pass: true`.

Evidence: `evidence/researcher06-unit08-v2-dev-gate.json`, persisted in commit `f2787822ce52ebce850ceca78953848db16ae932`.

## Architecture freeze
The fresh-final harness was committed before the final was opened, then a freeze record was persisted.

Frozen boundaries:
- Mandarin encoder: `mandarin-pinyin-pro-v2-research`;
- dependency: `pinyin-pro@3.29.3`;
- tone-free pinyin, `ü -> v`, explicit unknown-Han token policy;
- candidate budget: 20;
- ranking: stable corpus order among exact v2 phonetic-key matches, deduped by entity ID;
- fresh partition: `sha256(entity-id\0surface) mod 10 in {8,9}`;
- positive perturbation: deterministic single-Han substitution by another corpus Han with the same v2 tone-free pinyin syllable;
- negative controls: five fixed ordinary Mandarin utterances must abstain;
- pass gate: at least 40 positives, zero gold misses, all negatives abstain, zero unknown Han.

Harness commit: `2bb3ae463a9da4acc3b4a99c0d4f836590f479d3`.
Freeze record commit: `5d7de730b5444ee5df5a02c6efc6a7cfab328cfe`.

The exposed Unit 06 held-out suite remains retired from unseen evidence. No case-specific patching, product wiring or brain promotion was added.

## One-shot execution
Workflow `.github/workflows/dore-researcher06-v2-fresh-final.yml` was committed as `877b0ffff68e15961f8a7c95deb0dcdb226b40d7` to execute the frozen harness with the pinned dependency and persist a passing result to:

`evidence/researcher06-unit08-v2-fresh-final.json`

At the end of this heartbeat the result file is not yet durably visible on `main`. Therefore Unit 08 is **not yet passed or failed**. The absence is treated as an execution dependency, not as evidence about retrieval quality.

## Examination boundary
No score may be inferred until the durable final JSON exists. Once it exists, its first result is authoritative as the one-shot unseen gate. Any code or parameter change after opening it invalidates that result for unseen claims.

## Next authorized action
`RESEARCHER_06_UNIT_08_INSPECT_ONE_SHOT_FINAL_RESULT`.

If the durable final is passing, record the Unit 08 examination and determine whether Researcher 06 has enough transfer evidence for graduation or needs an additional integration/retention gate. If it fails, preserve the failure and diagnose only at architecture/corpus/perturbation-family level; do not patch exposed final identities.
