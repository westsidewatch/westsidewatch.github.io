# DORÉ MISSING EVIDENCE REGISTER

Status: ACTIVE / SWEEP-01 OUTPUT
Established: 2026-08-25
Primary index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

This register records claims that are plausible or partially evidenced but should not be promoted to stronger completion/quality claims without additional proof.

## ME-001 — Sensory-loop broad robustness beyond repair milestone

**Related work:** `CW-001 — Sensory-loop consolidation / D1 reconciliation milestone`

**What is already evidenced**
A real sensory signal reached `CONSOLIDATED`; deployed seed/heartbeat diagnostics show HTTP success, deduplication and schema reconciliation; Actions probing succeeded.

**What is not yet evidenced strongly enough**
- sustained operation across many signals;
- multiple heterogeneous signal/query classes;
- quantitative duplicate/drop/error rates;
- claim/retry behavior under failure;
- long-horizon persistence across schema/runtime changes;
- systematic quality evaluation of the research answer linked to a sensory signal.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` only for these broader robustness claims, not for the already verified repair milestone.

**Smallest useful future evidence**
A bounded benchmark using a representative batch of real or fixture signals with explicit expected outcomes, plus persisted counts for claimed/consolidated/deduplicated/failed/retried and a sampled quality check of resulting brain nodes.

**Priority:** LOW until traffic, regression risk or schema evolution makes the benchmark high leverage.

## ME-002 — Autonomous Project Runtime terminal completion

**Related work:** `RUNTIME`, `P01-PREFLIGHT`

**What is already evidenced**
Persistent repository state exists; P01 can resume without a human re-brief; the current state is `RUNNABLE` with attempt history, checkpoint evidence and no blocker. Multiple engineering cycles have persisted concrete progress, including CI-verified rights-aware result behavior.

**What is not yet evidenced strongly enough**
- one full accepted project autonomously reaching `VERIFIED_COMPLETE` from persisted runtime state;
- production verification of the current P01 schema-v5/result endpoint on live D1/Pages;
- full reader-facing Search/Library/ONE/Westside Stories flow verification;
- evidence that the runtime reliably distinguishes and stops at `HUMAN_DECISION_BLOCKED` / `ENVIRONMENT_BLOCKED` when those states occur in a real project.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for terminal autonomous-project reliability; Runtime itself remains `ACTIVE`.

**Smallest useful future evidence**
Drive P01 through production E2E verification to a persisted terminal state, with checkpoint history showing resume continuity and final verification evidence.

**Priority:** CRITICAL because this is one of the three convergence proof lines.

## ME-003 — Conversation Internal Alpha end-to-end continuity

**Related work:** `CONVERSATION`

**What is already evidenced**
- A1 context loading, A2 grounded contribution validation and bounded A3 meeting-close persistence primitives are implemented and CI-verified in the previously reviewed state.
- `dore-core/runtime/meetings/P01-PREFLIGHT-SUBTITLE/latest.json` now records a real persisted internal P01 rehearsal close with one grounded durable risk, one rejected speculative/transient suggestion, authority boundaries, no unresolved blocker and a fresh-session replay next action.
- `dore-core/tests/test_conversation_context.py` now requires the active P01 context packet to discover and replay the prior meeting record, preserve project identity and authority, and expose the durable contribution/verified learning without a human re-brief.
- commit `ce653b6e9443b287984e08f8e8f226a324533e2c` updates the Conversation Alpha workflow to require a prior meeting record and print `meeting-replay-ready` after the replay assertions.

**What is not yet evidenced strongly enough**
- an independently observed successful GitHub Actions run for the new rehearsal-replay assertions in this sweep batch; the commit/workflow/test definitions are present, but the commit-status endpoint exposes no completed status context and the available connector run lookup does not return push-triggered runs;
- evidence that the replay loop survives ordinary project-state changes over time rather than one current rehearsal fixture;
- a separate decision that the Internal Alpha as a whole meets every contract readiness gate and should be marked `VERIFIED_COMPLETE`.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for Internal Alpha `VERIFIED_COMPLETE`; the rehearsal/replay implementation gate is materially advanced and implementation remains `ACTIVE_PARALLEL` until execution evidence is closed.

**Smallest useful future evidence**
Persist or directly inspect one successful Conversation Alpha workflow run executing the current replay assertions, then evaluate the Alpha contract gates. Do not expose a public conversation surface as part of this verification.

**Priority:** HIGH because this is one of the three convergence proof lines, but it must not displace P01's production E2E critical path.

## ME-004 — R2 cost assumptions as current external fact

**Related work:** Cloudflare/R2 asset architecture, Cost Frontier

**What is already evidenced**
The architecture intentionally records free-first storage assumptions, safety thresholds and safe cleanup/preservation rules as design-time operating parameters.

**What is not yet evidenced strongly enough**
That the recorded provider free-tier allowances remain current at any future decision point. Provider billing limits are external facts and may change independently of repository architecture.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` only when using those numeric allowances for a present-day financial decision; the architectural policy itself remains current.

**Smallest useful future evidence**
Re-verify current provider pricing/allowances from authoritative provider documentation when Cost Frontier first approaches a real storage/operation threshold or before recommending paid capacity.

**Priority:** LOW now; automatically rises near the first capacity warning threshold.

## ME-005 — Conversation Memory Layer v1 production isolation and semantic recall

**Related work:** `CONV-MEM-V1`, `CONVERSATION`

**What is already evidenced**
- `cloudflare/d1/002_dore_conversation_memory.sql` defines conversation, message and memory-chunk structures with project/conversation scope;
- `functions/api/dore/memory.js` implements scoped record/retrieve behavior, conversation-local deduplication and optional R2/Vectorize binding awareness;
- `dore-core/tests/memory-layer-contract.mjs` explicitly requires scope, anti-global-vector rules, project/conversation boundaries and public tenant/authentication caution;
- `DORÉ-CONVERSATION-MEMORY-LAYER-V1.md` separates raw history, selected memory and consolidated knowledge and defines staged M1–M4 gates.

**What is not yet evidenced strongly enough**
- a real production D1 write through `/api/dore/memory`;
- exact replay of that message under the intended conversation+project scope;
- proof that a different conversation cannot retrieve the message;
- R2 archive write/recovery on a bound production archive;
- any real embedding generation or Vectorize retrieval;
- metadata-filtered vector retrieval that resists cross-conversation contamination;
- Conversation Alpha consuming the scoped memory interface;
- authenticated tenant isolation for any future public multi-user use.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for production-ready conversational memory; implementation remains `ACTIVE_PARALLEL / IMPLEMENTING`.

**Smallest useful future evidence**
Run one production-safe two-conversation fixture in the same project: write distinct sentinel messages, replay each exact scope, assert zero cross-retrieval, then persist the diagnostic. Only after this passes should R2 recovery and scoped Vectorize recall be activated and evaluated.

**Priority:** HIGH for Conversation Alpha continuity, but must not displace P01's active production E2E critical path.

## ME-006 — Search cognition understanding/product gate

**Related work:** `SEARCH`, `dore-core/knowledge/search-cognition-protocol.md`

**What is already evidenced**
- `dore-core/tests/search-cognition-understanding-gate.md` defines taught contrasts, eight unseen transfer cases, explanation requirements and product-routing requirements.
- The gate explicitly distinguishes `TAUGHT`, `CONCEPT_PASS` and `PRODUCT_PASS` and forbids claiming that Doré "understands" the protocol before the corresponding evidence exists.
- Its current recorded state is `TAUGHT`.
- `dore-core/tests/search-browser-negative-relevance.mjs` separately protects an important production-quality boundary: unrelated English phrases such as `Mortal Shell II` and `Grand Theft Auto` must not fabricate Scripture results, while explicit Scripture references and single-term fuzzy tolerance must continue to work.

**What is not yet evidenced strongly enough**
- recorded unseen-case reasoning sufficient for `CONCEPT_PASS`;
- live route execution proving SEARCH, scoped SEARCH, QUESTION and HYBRID behaviors sufficient for `PRODUCT_PASS`;
- evidence that fuzzy tolerance and negative relevance remain stable across the broader multilingual query distribution, not only the current regression fixtures.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for any claim that Search cognition is understood/product-complete; Search itself remains `MAINTENANCE + DISCOVERY`.

**Smallest useful future evidence**
Run and persist the Stage B/C transfer evaluation, then execute one bounded live-product routing fixture covering SEARCH, scoped SEARCH, QUESTION and HYBRID. Preserve the existing negative-relevance regression as a non-regression gate.

**Priority:** MEDIUM. Search is public and reader-facing, but this cognition graduation work should not interrupt the active P01 subtitle critical path.