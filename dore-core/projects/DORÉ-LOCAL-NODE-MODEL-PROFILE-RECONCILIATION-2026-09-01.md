# DORÉ LOCAL NODE MODEL-PROFILE RECONCILIATION — 2026-09-01

Status: SWEEP-01 DURABLE RECONCILIATION
Classification: documentation drift corrected; no operational status promotion.
Canonical operational rows: `DORÉ-MASTER-WORK-REGISTER.md` → `EVOLUTION`, `VIS-GRAMMAR`, `MEM-SWEEP-01`.

## Bounded evidence reviewed

- `local/dore-local/README.md`;
- `local/dore-local/bootstrap-macos.sh`;
- the current local visual-engine single-source reconciliation already persisted in `DORÉ-LOCAL-VISUAL-ENGINE-SINGLE-SOURCE-EVIDENCE-LEDGER-2026-09-01.md` and the Master Work Register.

## Finding

The local-node README still presented retired historical model names as the current “First model profile”. Current executable bootstrap evidence instead defines one reasoning-model source, `DORE_LOCAL_MODEL`, defaulting to `gemma4:e4b`. Embeddings are independently optional and are provisioned only when `DORE_LOCAL_EMBED_MODEL` is explicitly supplied; no embedding model is auto-selected when that variable is absent.

This was a memory/documentation contradiction rather than a runtime failure. The README has now been corrected so historical model names cannot silently reassert current configuration authority.

## Classification

- retired historical README model-name claims: `SUPERSEDED` as current configuration guidance;
- current local reasoning-model source contract: `ACTIVE / MAINTENANCE`, governed by executable source/runtime evidence;
- embedding-model provisioning: optional configuration, not a required capability-completion claim;
- D1–D3 Design Working Memory: unchanged bounded implementation status;
- D4 rendered visual readback/correction: still unproven;
- global Doré single-runtime/model unification: not claimed.

## Durable lesson

When documentation and executable configuration disagree, current executable source/runtime evidence governs the operational interpretation. Historical names may remain as provenance but must be labeled retired/superseded rather than left in imperative or present-tense configuration sections.

## P01 impact

None. No subtitle runtime, deployment, source ordering, credential, binding, blocker, or recovery action was modified.

## Sweep disposition

This bounded batch closes one local-node documentation contradiction but does not make Sweep 01 `VERIFIED_COMPLETE`. No new human or environment blocker was discovered.