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
- `dore-core/runtime/conversation-alpha-contract.md` records `VERIFIED_COMPLETE / INTERNAL_ONLY / NOT_PUBLIC` and states that all five Internal Alpha readiness gates are satisfied for the persisted active-project path.
- GitHub Actions run `32822094490` completed the A1+A2+A3 job successfully.
- the durable P01 rehearsal record exists at `dore-core/runtime/meetings/P01-PREFLIGHT-SUBTITLE/latest.json`;
- fresh-context discovery/replay and fresh-session replay tests were added and enforced in CI by commits `c8b54534ac69cfe9f006e48aac6cdfded92dfc48`, `7c4c110d11c448a8d9e1263e90a37133dd59999c`, and `ce653b6e9443b287984e08f8e8f226a324533e2c`;
- `dore-core/runtime/conversation-alpha-verification.json` records the five-gate evaluation;
- commit `ed45a900befa2478afda685d48a270b0256c3c3e` formally marks the contract verified complete.

**Resolution classification:** `VERIFIED_COMPLETE` for the bounded Internal Alpha milestone. The earlier `UNKNOWN_NEEDS_EVIDENCE` gap is closed and retained here only for provenance.

**Remaining non-blocking unknowns moved elsewhere**
Long-horizon/multi-project replay robustness remains maintenance/revisit territory, while production scoped D1/R2/Vectorize memory behavior remains `ME-005` / `CONV-MEM-V1`. Public conversation remains a separate parked authorization/readiness decision.

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

**Priority:** HIGH for future conversation continuity, but must not displace P01's active production E2E critical path.

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

## ME-007 — Autonomous learning / broader DORÉ_ALIVE claim — PARTIALLY RESOLVED

**Related work:** `CORE`, `AUTONOMOUS-LEARNING-LOOP.md`, `DORÉ-ALIVE-AND-SELF-DIRECTED-LEARNING.md`, `PRODUCT-EDUCATION-LOOP.md`, Researcher education, `CW-006` through `CW-009`.

**What is now strongly evidenced**
- `RESEARCHER_02_RESEARCH_METHOD_I_COMPLETE` is strongly corroborated by the Researcher 02 PASS final and by Researcher 04 naming it as an already satisfied prerequisite. The direct Researcher 02 final artifact uses `milestone eligible` wording, so provenance remains qualified, but the bounded method milestone is retained as `CW-006`.
- `dore-core/knowledge/researcher/RESEARCHER-04-AUTONOMOUS-LEARNING-I-FINAL-EXAM.md` explicitly records `PASS — RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE` with 12/12 criteria PASS.
- That exam demonstrates an end-to-end autonomous learning episode: recurring-deficit diagnosis → curriculum creation → source evaluation → adaptive prerequisite insertion → persistent execution → unseen exams → selective consolidation → next-deficit diagnosis → autonomous subsequent-course initiation.
- Researcher 05 subsequently graduated Biblical Concept Development I under retention watch, and Researcher 06 graduated Noise-Aware Scripture Retrieval I after a fresh final with preserved failed lineage, showing the learning faculty continued to create reusable downstream competence.

**What remains unproven / must not be conflated**
- `RESEARCHER_AUTONOMOUS_LEARNING_I_COMPLETE` is not automatically the same milestone as any separately reserved `AUTONOMOUS_LEARNING_LOOP_1_0` contract if that contract has additional requirements; do not rename one into the other without explicit contract reconciliation.
- longitudinal blind behavioral evidence sufficient for the broader aspirational `DORÉ_ALIVE_1.0` state is not yet established by this batch;
- cross-product transfer where learning in one work surface measurably improves another live work surface without a target-specific patch still deserves explicit evidence;
- autonomous authority over consequential human decisions remains outside the Researcher 04 graduation and must not be inferred from self-directed learning competence.

**Current classification:** `VERIFIED_COMPLETE` for the bounded Researcher 04 Autonomous Learning I milestone; `UNKNOWN_NEEDS_EVIDENCE` remains only for broader `AUTONOMOUS_LEARNING_LOOP_1_0` (if contract-distinct), `DORÉ_ALIVE_1.0`, and explicit cross-product autonomous-learning transfer claims.

**Smallest useful future evidence**
First reconcile the exact reserved contract names so the system knows whether `AUTONOMOUS_LEARNING_LOOP_1_0` is synonymous with or stronger than Researcher 04. Separately, when a real downstream opportunity appears without interrupting P01, persist one cross-product transfer case showing a generalized learned capability improving another surface with no product-specific patch.

**Priority:** MEDIUM/HIGH strategically, but non-blocking and subordinate to P01 production E2E.

## ME-008 — Live product expression of QUEUED / RESEARCHING states

**Related work:** `SEARCH`, `NERVOUS-SYSTEM`, `DORÉ-EXPRESSION-PROTOCOL.md`, `SR-006`.

**What is already evidenced**
- repository/runtime-level sensory persistence and research execution exist;
- a real sensory signal has reached `CONSOLIDATED`;
- the Learning Heartbeat records durable sensory → research → brain consolidation for `馬利亞有幾位?`;
- the Expression Protocol defines truthful state semantics and forbids visible state from exceeding verified internal state.

**What is not yet evidenced strongly enough**
- a current public Search deployment receiving a fresh unknown query and durably persisting it;
- the browser later rendering `QUEUED` or `RESEARCHING` from that same persisted live state rather than from a local/scripted fallback;
- the browser subsequently surfacing the consolidated brain result without per-question UI logic;
- direct acceptance evidence for the named `DORÉ_CLOSED_LOOP_01_PASS` milestone.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for browser/product expression wiring and the named full closed-loop acceptance; the underlying Expression Protocol remains `ACTIVE` and repository/runtime sensory capability is not downgraded.

**Smallest useful future evidence**
Use one fresh unknown browser query: capture initial truthful UNKNOWN/HEARD state, prove durable queue persistence, capture QUEUED/RESEARCHING only when backed by live state, let the research/consolidation path complete, then re-run the same query and capture the improved generic brain-backed result with no query-specific code patch.

**Priority:** MEDIUM/HIGH because it would close a major learning→product proof line, but it must not interrupt P01.