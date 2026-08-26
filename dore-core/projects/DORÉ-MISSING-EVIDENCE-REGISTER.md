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

## ME-003 — Conversation Internal Alpha end-to-end continuity — RESOLVED

**Related work:** `CONVERSATION`, `CW-004 — Conversation Runtime Internal Alpha`

**Resolution evidence**
The bounded Internal Alpha milestone is recorded `VERIFIED_COMPLETE / INTERNAL_ONLY / NOT_PUBLIC`, with persisted P01 rehearsal, fresh-context replay, CI verification and a formal verification artifact. The earlier evidence gap is closed; production scoped memory remains separately tracked under `ME-005`.

## ME-004 — R2 cost assumptions as current external fact

**Related work:** Cloudflare/R2 asset architecture, Cost Frontier

**What is already evidenced**
The architecture records free-first storage assumptions, safety thresholds and safe cleanup/preservation rules as design-time operating parameters.

**What is not yet evidenced strongly enough**
That recorded provider free-tier allowances remain current at a future decision point.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` only when numeric allowances are used for a present-day financial decision.

**Smallest useful future evidence**
Re-verify current provider pricing/allowances from authoritative documentation near a real threshold or before recommending paid capacity.

**Priority:** LOW now.

## ME-005 — Conversation Memory Layer v1 production isolation and semantic recall

**Related work:** `CONV-MEM-V1`, `CONVERSATION`

**What is already evidenced**
D1 conversation/message/chunk structures, scoped memory API, dedupe, optional R2/Vectorize hooks and anti-cross-talk contract tests exist.

**What is not yet evidenced strongly enough**
Production D1 write/replay/isolation, R2 recovery, real embeddings/Vectorize retrieval, metadata-filtered vector isolation, Conversation Alpha consumption, and future public tenant isolation.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for production-ready conversational memory; implementation remains `ACTIVE_PARALLEL / IMPLEMENTING`.

**Smallest useful future evidence**
Run a production-safe two-conversation fixture in one project, replay exact scopes, assert zero cross-retrieval, then persist the diagnostic before activating R2/Vectorize stages.

**Priority:** HIGH, subordinate to P01.

## ME-006 — Search cognition understanding/product gate

**Related work:** `SEARCH`, `dore-core/knowledge/search-cognition-protocol.md`

**What is already evidenced**
A taught understanding gate and negative-relevance regression exist; current cognition state remains `TAUGHT`.

**What is not yet evidenced strongly enough**
Recorded unseen-case reasoning for `CONCEPT_PASS`, live SEARCH/scoped SEARCH/QUESTION/HYBRID routing for `PRODUCT_PASS`, and broader multilingual stability.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for cognition understanding/product-complete claims.

**Smallest useful future evidence**
Persist Stage B/C transfer evaluation and one bounded live routing fixture while preserving negative-relevance regression.

**Priority:** MEDIUM, subordinate to P01.

## ME-007 — Autonomous learning / broader DORÉ_ALIVE claim — PARTIALLY RESOLVED

**Related work:** `CORE`, Researcher education.

**What is now strongly evidenced**
Researcher 04 Autonomous Learning I is a bounded 12/12 PASS; later Researcher 05/06 work corroborates reusable downstream learning competence.

**What remains unproven**
Any stronger contract-distinct `AUTONOMOUS_LEARNING_LOOP_1_0`, broad `DORÉ_ALIVE_1.0`, explicit cross-product transfer without target patches, or consequential human-decision authority.

**Current classification:** `VERIFIED_COMPLETE` for Researcher 04 only; broader claims remain `UNKNOWN_NEEDS_EVIDENCE`.

**Priority:** MEDIUM/HIGH strategically, subordinate to P01.

## ME-008 — Live product expression of QUEUED / RESEARCHING states

**Related work:** `SEARCH`, `NERVOUS-SYSTEM`, Expression Protocol, closed-loop experiment.

**What is already evidenced**
Repository/runtime sensory persistence and research execution exist, including a consolidated real sensory signal; the experiment defines a ten-step acceptance contract.

**What is not yet evidenced strongly enough**
Fresh public unknown-query persistence, browser QUEUED/RESEARCHING from live state, autonomous learning under experiment gates, material generic brain update, improved re-query without a per-question patch, and explicit `DORÉ_CLOSED_LOOP_01_PASS` evidence.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for browser/product expression wiring and named full closed-loop acceptance.

**Priority:** MEDIUM/HIGH, subordinate to P01.

## ME-009 — Foundation Scripture Canon course completion

**Related work:** `dore-core/knowledge/foundation/scripture-canon/COURSE-01-SCRIPTURE-CANON.md`

**What is already evidenced**
The Scripture Canon foundation has substantial durable infrastructure: canon/book schemas, corpus ingestion/reader contracts, entity-graph schema, pinned OSHB and MorphGNT/SBLGNT snapshots, first-reading artifacts, and explicit provenance/licensing discipline. The current pinned corpus snapshot separates OSHB analytical CC BY 4.0 metadata from WLC public-domain base-text metadata and pins both Hebrew/Aramaic and Greek upstream commits for reproducibility.

**What is not yet evidenced strongly enough**
- the course source itself still records `Status: IN PROGRESS`;
- its graduation rule requires machine-readable registry/schema plus passing first exercises;
- the corpus-reader acceptance contract requires zero critical failures and names `LESSON_03_CORPUS_FOUNDATION_COMPLETE` only on pass;
- this bounded sweep found no independent passing artifact for that named Lesson 03 completion token;
- no evidence in this batch warrants promoting the whole Scripture Canon course to `VERIFIED_COMPLETE`.

**Current classification:** `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` for completion. Existing infrastructure is retained as real progress, not downgraded.

**Smallest useful future evidence**
Run/persist the canonical-reference exercises and Lesson 03 corpus provenance suite against the pinned snapshot, with explicit critical-gate results and a course-status update only after all required gates pass.

**Priority:** MEDIUM. Important foundation work, but it must not interrupt P01.

## ME-010 — Scripture Search Input Literacy 1.0 graduation

**Related work:** `dore-core/knowledge/foundation/search-input/SCRIPTURE-SEARCH-INPUT-LITERACY-1.0.md`, `SEARCH`

**What is already evidenced**
The micro-unit clearly specifies stable real-world Chinese Scripture-reference forms, punctuation/range variants, multi-reference parsing, deduplication, and a transfer-based graduation standard. Separate Search production work already protects some explicit-reference and fuzzy/negative-relevance behavior.

**What is not yet evidenced strongly enough**
The micro-unit requires unseen transfer across different books and formatting variants, including two- and three-reference inputs and mixed single/range references. This bounded sweep found no dedicated graduation/pass artifact demonstrating that exact contract, and existing Search regressions must not be silently treated as equivalent evidence.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for the micro-unit graduation claim; the curriculum artifact remains valid foundation doctrine.

**Smallest useful future evidence**
Execute a bounded unseen fixture set satisfying the micro-unit's exact graduation paragraph, persist pass/fail results, and only then record a bounded completion milestone.

**Priority:** LOW/MEDIUM; useful for Search quality, subordinate to P01.
