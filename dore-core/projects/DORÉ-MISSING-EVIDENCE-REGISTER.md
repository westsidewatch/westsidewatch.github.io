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
A1 context loading, A2 grounded contribution validation and bounded A3 meeting-close persistence primitives are implemented and CI-verified. Authority boundaries and no-public-conversation constraints are explicitly carried by the runtime contract.

**What is not yet evidenced strongly enough**
- one real internal P01 meeting rehearsal using persisted context;
- at least one grounded durable contribution plus one rejected transient/speculative contribution in the same exercise;
- a durable meeting-close record persisted into repository evidence;
- fresh-session discovery/replay of that record without a human re-brief;
- proof that this loop survives ordinary project-state changes rather than only fixtures.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for Internal Alpha `VERIFIED_COMPLETE`; implementation remains `ACTIVE_PARALLEL`.

**Smallest useful future evidence**
Execute the contract's defined P01 rehearsal and fresh-session replay check, persist the evidence, then evaluate the Alpha against all readiness gates.

**Priority:** HIGH because this is one of the three convergence proof lines.

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