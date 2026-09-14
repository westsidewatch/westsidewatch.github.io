# Doré Tests Source-Family Reconciliation — 2026-09-14

Status: BOUNDED_RECONCILIATION
Sweep: DORÉ MEMORY CONSOLIDATION SWEEP 01

## Scope

Current `dore-core/tests/` family:

- `memory-layer-contract.mjs`
- `search-browser-negative-relevance.mjs`
- `search-cognition-understanding-gate.md`
- `test_conversation_context.py`
- `test_conversation_contribution.py`
- `test_conversation_meeting_close.py`
- `test_cross_witness_alignment.py`
- `test_original_language_reader.py`
- `test_wake_runtime.py`

This ledger reconciles the family as evidence infrastructure. It does not rerun or alter the active P01 subtitle path.

## Family-level judgment

Classification: `CORE/CONTINUOUS / EVIDENCE INFRASTRUCTURE` with mixed maturity per test.

The folder is not a single test suite with one global PASS state. It contains three different evidence classes:

1. runnable executable regression/acceptance tests;
2. static contract/source assertions;
3. documentary gates/specifications that intentionally remain unpassed.

A filename under `tests/` therefore must never be treated as proof that the represented capability passed.

## Reconciled components

### Wake runtime

`test_wake_runtime.py` is executable regression evidence for bounded wake-runtime primitives: idempotent enqueue, successful/failed probe state, verifier-gated file promotion with backup, refusal to promote on failed verification, and expired-lease recovery.

Disposition: retain as regression evidence supporting the already-bounded Runtime/Evolution component claims. It does not prove the whole autonomous gap→research→equip→resume→blind-transfer chain.

### Conversation Internal Alpha

`test_conversation_context.py`, `test_conversation_contribution.py`, and `test_conversation_meeting_close.py` encode real authority/evidence/persistence safeguards: internal-only mode, human/church authority, bounded source roles, rejection of unknown evidence references, persistence exclusion for speculative contributions, project mismatch rejection, and durable meeting-record round trip.

Disposition: retain as regression evidence for the already closed bounded Conversation Internal Alpha component.

Maintenance finding: two test fixtures still use historical prose asserting that P01 “remains RUNNABLE.” Current canonical P01 state is `BLOCKED / ENVIRONMENT_BLOCKED`. These strings are test payloads rather than current register assertions, and the tests do not appear to assert the literal runtime status, but they are semantically stale and could mislead future evidence interpretation. They should be replaced with status-neutral grounded fixture text at the next Conversation-test maintenance pass. This is maintenance debt, not a P01 action and not a blocker.

### Conversation Memory Layer contract

`memory-layer-contract.mjs` is a static source/SQL/architecture contract test. It verifies required D1 tables/indexes, scoped retrieval clauses, archive/vector hooks, content-hash dedupe and documentary tenant/scope rules by reading source files.

Disposition: useful regression guard, but classify as source-contract evidence rather than production D1/Vectorize runtime proof. It cannot by itself promote Full Memory Phase 1 beyond the existing live-diagnostic evidence boundaries.

### Search

`search-browser-negative-relevance.mjs` remains a bounded executable browser regression for known negative-relevance examples. `search-cognition-understanding-gate.md` explicitly remains `TAUGHT` and forbids `CONCEPT_PASS`, `PRODUCT_PASS` or an “understands” claim without unseen classification/reasoning plus live route execution.

Disposition: current Search `MAINTENANCE + DISCOVERY` classification remains correct. The tests support bounded regression and preserve the missing-evidence gate; they do not establish general Search cognition.

### Scripture / original-language reader

`test_cross_witness_alignment.py` is executable architecture evidence for witness separation, missing-witness review behavior and unaligned-unit reporting. `test_original_language_reader.py` has already been reconciled as a non-runnable acceptance specification pending package/import wiring.

Disposition: retain current Scripture Canon / Language-Core evidence boundary. Test existence is not reader acceptance completion.

## Durable lessons

- A `tests/` directory is an evidence inventory, not a global PASS token.
- Static source-contract tests, executable behavior tests and documentary acceptance gates must be labeled separately.
- Historical fixture prose can become semantically stale even when the assertion mechanics still pass; evidence fixtures should avoid embedding obsolete project-state claims unless the state itself is what is under test.
- Regression tests should preserve bounded component claims and resist capability inflation.

## Revisit / maintenance queue

Low-priority maintenance candidate:

- replace historical `P01 remains RUNNABLE` fixture wording in Conversation tests with status-neutral evidence text, while preserving authority/evidence/persistence behavior;
- do not touch P01 runtime or subtitle logic as part of that edit.

No new top-level workstream, human decision or environment dependency is created by this source-family reconciliation.
