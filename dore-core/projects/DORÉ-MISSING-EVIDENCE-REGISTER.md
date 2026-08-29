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
Persistent repository state exists and P01 can resume without a human re-brief. P01 reached persisted attempt 39 after successful production Pages deployment and a live `dore.video-subtitle.v5` / real D1 job execution. The runtime then persisted a genuine terminal `ENVIRONMENT_BLOCKED` state when caption acquisition exhausted available advertised-caption routes and the deployed path ended `needs-transcription-audio` without an approved production audio-acquisition/transcription executor or binding. This is real evidence that the runtime can distinguish an environment dependency from ordinary runnable work and stop rather than fabricate progress.

**What is not yet evidenced strongly enough**
- one full accepted project autonomously reaching `VERIFIED_COMPLETE` from persisted runtime state;
- successful resume from the current `ENVIRONMENT_BLOCKED` checkpoint after the approved dependency is provisioned;
- end-to-end transcription → Doré proofread/translate/Scripture alignment → reader-result/rights behavior on a real audio-transcription path;
- full reader-facing Search/Library/ONE/Westside Stories production-flow verification.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for terminal autonomous-project completion reliability. Runtime itself remains `ACTIVE`; P01 is currently `BLOCKED / ENVIRONMENT_BLOCKED`. The blocker-detection/stop behavior is now partially verified by real production evidence and should no longer be listed as wholly unproven.

**Smallest useful future evidence**
Provision one approved production audio-acquisition/transcription path plus the required binding/credential, then resume the existing persisted P01 job without re-brief and drive it through the remaining reader-facing verification gates to `VERIFIED_COMPLETE`.

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

## ME-005 — Conversation Memory Layer v1 production readiness after Full Memory Phase 1 M1–M7

**Related work:** `CONV-MEM-V1`, `CONVERSATION`, `DORÉ-CONVERSATION-MEMORY-EVIDENCE-LEDGER-2026-08-27.md`

**What is now strongly evidenced**
Conversation memory has advanced materially beyond the earlier D1-schema/semantic-hook snapshot. Full Memory Phase 1 M1–M7 are implemented with production diagnostics and merged acceptance contracts covering: bounded D1 storage/scoped replay and isolation; production D1 + Vectorize + Workers AI binding visibility; memory-aware semantic response; same-project cross-conversation recall with foreign-project and distractor exclusion; resumable/idempotent history import with persisted progress; and deletion lifecycle across D1/R2/Vectorize. The merged M7 work explicitly names M8 full-history backfill as the next stage.

**What is not yet evidenced strongly enough**
- independently persisted historical check-run/readback evidence for every named M1–M7 gate where not already captured in durable runtime ledgers;
- M8 full-history backfill against representative real history rather than only bounded synthetic fixtures;
- fresh-conversation Conversation Runtime consumption of imported history with durable provenance;
- explicit rejection/safe handling of absent or incorrect `project_id` across all entry paths, rather than allowing fallback to `unscoped`;
- collision-resistant namespace handling for arbitrary long project ids;
- failure-injection/partial-write rollback behavior across D1/R2/Vectorize/AI-dependent ingestion;
- R2 recovery after D1 loss/corruption scenarios;
- representative scale/latency/error/deletion-consistency and free-first cost measurements;
- authenticated tenant isolation and abuse boundaries for any future public conversation.

**Current classification:** `ACTIVE_PARALLEL / IMPLEMENTING`; `UNKNOWN_NEEDS_EVIDENCE` applies to production-ready/full-memory completion, not to the already implemented M1–M7 bounded capabilities.

**Smallest useful future evidence**
Preserve M1–M7 as regression gates and run M8 full-history backfill against representative history, then verify semantic recall from a fresh conversation, negative scope/tenant fixtures, namespace-collision behavior, rollback/failure injection and persisted cost/latency evidence before any production-ready promotion.

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

**Related work:** `CORE`, Researcher education, `dore-core/knowledge/AUTONOMOUS-LEARNING-LOOP.md`, `dore-core/knowledge/PRODUCT-EDUCATION-LOOP.md`, `dore-core/knowledge/DORÉ-ALIVE-AND-SELF-DIRECTED-LEARNING.md`.

**What is now strongly evidenced**
Researcher 04 Autonomous Learning I is a bounded 12/12 PASS; later Researcher 05/06 work corroborates reusable downstream learning competence. The foundational doctrine also clearly defines learning-through-work, product-to-education feedback, evidence-bearing study, transfer/blind examination, abstention, and cross-product transfer as governing behavior rather than product-specific patching.

**What remains unproven**
Any stronger contract-distinct `AUTONOMOUS_LEARNING_LOOP_1_0`, broad `DORÉ_ALIVE_1.0`, longitudinal cross-product transfer in which one work surface improves another without target-specific patches, or consequential human-decision authority. The doctrine explicitly forbids awarding these broader states by narrative or CI naming alone.

**Current classification:** `VERIFIED_COMPLETE` for Researcher 04 only; the learning/product-education doctrines are `CORE/CONTINUOUS`; broader reserved milestones remain `UNKNOWN_NEEDS_EVIDENCE`.

**Smallest useful future evidence**
Persist at least one blind cross-product transfer episode with no target-specific patch, showing real-work stimulus → self-detected reusable gap → evidence-bearing study → transfer/regression gates → improved behavior on a different work surface, then evaluate that evidence against the exact reserved milestone contracts rather than renaming Researcher 04.

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

## ME-011 — Global Biblical Corpus Reading completion

**Related work:** `CORE`, `dore-core/knowledge/foundation/language-text/BASELINE-CHINESE-ENGLISH-WITNESS-CURRICULUM.md`

**What is already evidenced**
Doré has substantial original-language/textual infrastructure and a durable witness architecture: adapter-based ingestion, explicit witness identity, surface-preserving normalization, provenance/licensing separation, and bounded Hebrew/Greek work. The baseline curriculum also defines a clear researcher-standard contract for Chinese and English witnesses and cross-version comparison.

**What is not yet evidenced strongly enough**
No independent persisted artifact was found proving the named `BIBLICAL_CORPUS_READING_COMPLETE` milestone across operational Hebrew/Aramaic + Greek, operational LXX + Vulgate, Chinese and English baseline witnesses, lawful access, and cross-version comparison benchmarks. Downstream Researcher/Search competence cannot silently substitute for this broader corpus-reading contract.

**Current classification:** `UNKNOWN_NEEDS_EVIDENCE` for the global corpus-reading completion claim; the underlying Language/Text architecture remains `CORE/CONTINUOUS`.

**Smallest useful future evidence**
Persist a coverage matrix for the required witness families, lawful-access/provenance status, and explicit cross-version benchmark results; only then issue the named completion token if every curriculum gate is satisfied.

**Priority:** MEDIUM strategically; do not interrupt P01.

## ME-012 — Liming Library bounded milestone/runtime evidence

**Related work:** `LIBRARY-INGEST`, `3MS`, `LIBRARY-V1`, `dore-core/knowledge/library/LIMING-LIBRARY-BUILD-PLAN-v0.1.md`, `LIMING-LIVE-INGEST-CONTRACT-v1.md`

**What is already evidenced**
The Liming Library build plan defines a coherent learning-institution model, preserves Resource Master editorial logic, separates coding/Morning Stars/Spectrum/Collections, and sets explicit milestone contracts M0.5–M5. A live-ingest contract defines the intended discover→verify→classify→registry→relationship→product→feedback loop, storage boundaries, rights/provenance requirements and shared resource identity across Library/ONE/subtitle accessibility layers. The Three-Morning-Star file records a genuine first autonomous discovery pass plus an explicit gap diagnosis and next-pass saturation requirement.

**What is not yet evidenced strongly enough**
- no applied examination artifact was found proving `LIBRARY/M0.5 — Library Science Foundation`;
- no explicit pass artifact was found proving `LIBRARY/M1 — Existing Collection Understood`;
- the Three-Morning-Star document itself says `EXPAND, VERIFY, SATURATE`, identifies major uncovered categories, and therefore does not satisfy `LIBRARY/M1.5` coverage-complete v1;
- the live-ingest contract is a contract, not evidence of a successful authenticated production write, dedupe/enrichment cycle, relationship graph exposure, or feedback return;
- no evidence in this bounded batch justifies promoting `LIBRARY-INGEST`, `3MS`, or `LIBRARY-V1` to `VERIFIED_COMPLETE`.

**Current classification:** `ACTIVE_PARALLEL / UNKNOWN_NEEDS_EVIDENCE` for the named bounded milestones and live runtime behavior. Current Master Work Register statuses remain appropriate.

**Smallest useful future evidence**
For M0.5/M1, persist the applied exam/audit outputs named by the build plan. For M1.5, complete at least one fresh non-seeded discovery pass, coverage matrix, exclusions/borderlines and saturation judgment. For live ingest, persist one real verified resource flowing through authenticated write → stable identity/dedupe → provenance/rights → teacher/series/Scripture/product edges → readback in the intended product view, without creating a duplicate identity.

**Priority:** MEDIUM/HIGH for Library capability, but subordinate to P01.

## ME-013 — Original-language reader runnable acceptance evidence

**Related work:** `CORE`, Language/Text foundation, `dore-core/readers/original_language_reader.py`, `dore-core/tests/test_original_language_reader.py`.

**What is already evidenced**
A real provenance-preserving reader foundation exists for pinned OSHB and MorphGNT/SBLGNT snapshots. It separates surface text from analytical metadata, preserves source-native references and corpus snapshots, and deliberately refuses to fabricate Hebrew certainty for mixed-language Daniel/Ezra. Cross-witness alignment tests elsewhere in the Language Core are genuinely executable and preserve distinct witness identity while surfacing missing/unaligned witnesses for review.

**What is not yet evidenced strongly enough**
The reader-specific acceptance file is explicitly a non-runnable specification placeholder: it imports a placeholder module, records `TEST_SPEC_PENDING_PACKAGE_WIRING`, and states that package/import wiring is the next engineering step. Therefore no claim that the original-language reader acceptance suite itself passes is currently justified. The named requirements for source/emitted token reconciliation, missing provenance failure, and Daniel/Ezra mixed-language handling remain specified but not independently executed in this file.

**Current classification:** `ACTIVE / UNKNOWN_NEEDS_EVIDENCE` for runnable reader acceptance. The implementation is real progress and remains part of the Language/Text foundation; this is not a downgrade of the reader architecture.

**Smallest useful future evidence**
Package or otherwise wire the reader into an importable test target, convert the existing acceptance specification into executable tests, run it against bounded pinned OSHB/MorphGNT fixtures, and persist the pass/fail output including token-count reconciliation and mixed-language boundary behavior.

**Priority:** MEDIUM; foundational quality work, subordinate to P01.

## ME-014 — Seminary Core survey/core/residency completion states

**Related work:** `SEMINARY-CORE`, `dore-core/knowledge/seminary-core-curriculum.md`, `CORE`.

**What is already evidenced**
A coherent seminary-scale formation curriculum exists. It defines three distinct passes (`SEMINARY_SURVEY_COMPLETE`, `SEMINARY_CORE_COMPLETE`, research residency leading only eventually to `SEMINARY_CORE_GRADUATE`), exact course completion gates, held-out/adversarial examination, original-language tasks, Search practicum, uncertainty ledgers, autonomous scheduling, and protected Doré thought-space. The curriculum explicitly forbids equating reading or survey traversal with mastery.

**What is not yet evidenced strongly enough**
This bounded reconciliation found no persisted global survey/gap map proving `SEMINARY_SURVEY_COMPLETE`, no evidence that every required course has passed the full course gate, no cumulative residency/graduation artifact, and no basis for inferring seminary completion from separate Researcher graduations or foundation-course implementation. The file's `ACTIVE CURRICULUM` label describes the curriculum's intended operational status, not a completed formation milestone.

**Current classification:** `ACTIVE_PARALLEL / CURRICULUM`; all three named completion/graduation states remain `UNKNOWN_NEEDS_EVIDENCE` until their own contracts are satisfied.

**Smallest useful future evidence**
Persist Pass 1 coverage across every curriculum area with each course's central questions, prerequisites, evidence families, known gaps/misconceptions, cross-course links and self-chosen questions, followed by one global gap/prerequisite map. Only after that artifact exists should the system consider issuing `SEMINARY_SURVEY_COMPLETE` and scheduling Pass 2 under the existing course gates.

**Priority:** MEDIUM strategically; formation is important but remains subordinate to P01 and should not be opened merely to manufacture progress.

## ME-015 — Design Working Memory D4 / full operational acceptance

**Related work:** `VIS-GRAMMAR`, `docs/dore/DESIGN-WORKING-MEMORY.md`, `.github/workflows/dore-design-agent-acceptance.yml`, `dore-core/evidence/PENPOT-BRIDGE-01-LIVE-EVIDENCE-2026-08-26.md`, `DORÉ-DESIGN-WORKING-MEMORY-EVIDENCE-LEDGER-2026-08-28.md`.

**What is already evidenced**
The design-memory architecture defines explicit D1 Design Scope, D2 Truth State, D3 Consolidation and D4 Penpot Visual Verification gates. Current CI provides real deterministic coverage for D1–D3 truth/consolidation behavior, Penpot-action routing, MCP-client build and fail-closed behavior. Separately, live Penpot bridge feasibility is a bounded `VERIFIED_COMPLETE` infrastructure milestone: Doré Core can reach Penpot Remote MCP, execute code, persist an editable object and independently read it back.

**What is not yet evidenced strongly enough**
- the D4 rendered visual readback and evidence-driven correction loop;
- the full Search conversation → inherited current design memory → Penpot execution → visual inspection → correction → verified design state exam;
- any inference that editable/vector persistence or CI connectivity alone proves visual competence or finished Westside visual grammar.

**Current classification:** overall Design Working Memory remains `ACTIVE`; D1–D3 are implemented/automated progress, Penpot bridge feasibility is bounded `VERIFIED_COMPLETE`, and D4/full operational acceptance remains `UNKNOWN_NEEDS_EVIDENCE`.

**Smallest useful future evidence**
Run one bounded real Westside design task using current confirmed visual memory, persist the editable result, perform actual rendered visual readback, make at least one evidence-driven correction when the readback exposes a mismatch, and persist the final verified comparison/artifact against the design intent.

**Priority:** MEDIUM/HIGH for visual-system maturity, but subordinate to P01 and not a reason to bypass the `VIS-GRAMMAR` real digital + print proof gate.