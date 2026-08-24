# Doré Learning Heartbeat

Status: ACTIVE
Established: 2026-08-23
Updated: 2026-08-24

## Rule
Doré learning does not wait for a human to say `continue`, `execute`, `next`, or approve each course. On wake, read current state, execute `AUTONOMOUS_ALLOWED` work, self-check, persist evidence/failures/state/next action, and continue while evidence and authority remain clear. Course completion requires exam gates. Retention/transfer failures reopen learning.

Human approval is reserved for irreversible/destructive external actions, paid obligations, official outward doctrinal/editorial publication, brand/governance changes, new private credentials/access, material legal/security/privacy consequences, or genuine unresolved value conflicts.

## Major completed milestones
- Biblical Languages I: `PASS / GRADUATED`.
- Researcher 04 — Autonomous Learning I: `COMPLETE → RETENTION_WATCH`, final 12/12 PASS.
- Researcher 05 — Biblical Concept Development I: `PASS / GRADUATED → RETENTION_WATCH`, independent resurrection transfer 6/6 PASS.
- First durable sensory → research → brain consolidation: `馬利亞有幾位?` consolidated to `research.nt.mary-count` after independent research and 7/7 examination.
- Generic Brain → Product repository regression established without per-question answer logic.

## Sensory state checked this heartbeat
`dore-core/memory/sensory-active.json` contains no `RESEARCHING` signal without a `brain_node`. Existing Mary signal remains `CONSOLIDATED`; therefore no live sensory research preempted the course loop.

## Researcher 06 — Noise-Aware Scripture Retrieval I
Status: ACTIVE — UNITS 01–08 PASS; UNIT 09 ACTIVE / EXECUTABLE DEV GATE IMPLEMENTED.

### Unit 06 honest failure
After dev calibration reached recall-at-budget 1.0 with zero gold misses, the frozen one-time held-out final failed at recall 0.5 because the deliberately small Mandarin mapping covered only a small fraction of the biblical entity corpus. V1 remains frozen and that exposed final is permanently retired as unseen evidence.

### Unit 07 corpus-wide repair
Corpus audit showed 2,876 Chinese entity surfaces / 14,953 Han occurrences but only 30.78% occurrence coverage under v1. A pinned research-only `pinyin-pro@3.29.3` reference covered the corpus, leading to `mandarin-pinyin-pro-v2-research` without identity-specific patches. Unit 07 examination: 8/8 PASS.

### Unit 08 authoritative fresh final
The first durable result at `evidence/researcher06-unit08-v2-fresh-final.json` is authoritative for the frozen v2 architecture: 80/80 positives, recall-at-budget 1.0, zero gold misses, 5/5 negative abstention, unknown Han rate 0, mean candidate set 2.4941. Unit 08 examination: 8/8 PASS. This does not alone prove mixed transcript-noise correction, subtitle editing safety, calibrated ambiguity handling, or production readiness.

### Unit 09 — Offline Integration Transfer Gate
The integration contract remains frozen in `RESEARCHER-06-UNIT-09-FREEZE.md`.

This heartbeat completed the next authorized implementation action:
- added `scripts/dore/researcher06-unit09-transfer-gate.mjs`;
- the harness emits one product-neutral evidence object containing observed transcript, candidate, canonical source/anchor, evidence channels, non-probabilistic score boundary, and decision;
- Search-like and subtitle-proofreader adapters consume that same generic object rather than separate product-specific retrieval logic;
- subtitle output explicitly preserves observed text and forbids silent overwrite;
- ambiguity and ordinary-negative safety invariants are checked;
- added `.github/workflows/dore-researcher06-unit09-dev-gate.yml` to execute the exposed development partition with pinned `pinyin-pro@3.29.3` and persist the resulting evidence JSON.

No Unit 09 PASS is claimed yet. The development fixture is exposed and cannot count as fresh-final evidence. The workflow/evidence result must exist before a fresh final may be authored or opened.

## Current next action
`RESEARCHER_06_UNIT_09_INSPECT_PERSISTED_DEV_GATE_RESULT`.

When `dore-core/knowledge/researcher/evidence/researcher06-unit09-dev-gate.json` is present, inspect it. If the dev gate passes all shared-object, provenance, negative-abstention, ambiguity and subtitle-no-silent-overwrite invariants, author and seal a separate fresh-final partition covering all seven required evidence families, then run it once under the frozen contract. If the dev gate fails, preserve the failure and repair only generic architecture using the exposed dev partition.

## Brain/Product status
This heartbeat changed no product-readable knowledge node, so no Brain → Product regression was required. Researcher 06 remains research-only and is not production-promoted.

## Closed-loop remaining acceptance
Repository-level durable sensory → research → brain and generic Brain → Product regression are evidenced. Browser-level acceptance remains: a current Search deployment must itself POST a fresh unknown query into sensory memory and later surface the consolidated live brain result without per-question UI logic.
