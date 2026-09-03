# DORÉ NEWSROOM / REAL SIGNAL LOOP EVIDENCE LEDGER — 2026-09-03

Status: ACTIVE_EVIDENCE / MEMORY-SWEEP-01
Scope: bounded reconciliation of the new Newsroom control-plane + Real Signal Loop family
P01 impact: NONE — this ledger does not modify, resume, reprioritize, or reinterpret the active P01 subtitle critical path.

## Evidence inspected

- commit `7520d3d594950bf10d6148410bb133d42821c7b1` — `feat(dore): package newsroom control plane v1`
- commit `121dbf3d578037a535fe2078a22f7ca1375fb8d770` is NOT evidence for this family and is excluded; the governing implementation commit is `121dbf3d578037a535fe2078a22f4c4e4977ab84` — `feat(dore): connect newsroom real signal loop`
- coordination result commit `1f7cb763158e0db999cf40d43a1ac21bb4d7b13f` — attempted peer-engineering execution for Newsroom isolated packaging / real signal work
- repository commit-status query for `121dbf3d578037a535fe2078a22f4c4e4977ab84` returned no persisted status checks in the bounded inspection

## What is real implementation

The Newsroom family is no longer only product doctrine. The implementation commit adds an event-driven `dore.newsroom-control-plane.v1.0` with explicit signal validation, bounded Editorial Gravity, priority/pre-emption behavior, reuse of provenance-preserving Dawn assets, delta-only enrichment for named gaps, review-only prayer/report draft generation, and resume of displaced lower-priority work.

The follow-on Real Signal Loop adds a free-only HTTPS official-feed connector, canonical event identity, content hashes, replay dedupe, correction/retraction revisions, PREPARED→COMMITTED operation state, recoverable uncommitted operations, and a hard publication boundary (`publishable=false`, `requires_human_editor=true`, `published=false`). The source contract explicitly says observation is not publication authority.

These are meaningful implementation milestones and should be retained as `ACTIVE_IMPLEMENTATION`, not dismissed as architecture-only notes.

## Evidence boundary / classification

**Current classification:** `ACTIVE_PARALLEL / IMPLEMENTED_BUT_NOT_VERIFIED_COMPLETE`.

The bounded evidence does **not** justify a Newsroom completion token. The repository contains unit/acceptance programs, but this Sweep pass did not find persisted CI/status evidence proving that the packaged Newsroom control plane and live official-feed acceptance completed successfully at the inspected commit. The later coordination result is explicitly non-terminal: `task_status=LEARNING`, `terminal=false`, `execution=FAIL`, state `RESEARCH_QUEUED`, caused by `UNSUPPORTED_PEER_SEMANTICS` / `peer_kind_requires_research:peer_engineering`, while preserving the parent goal and handing it to resident runtime.

Therefore:

- implementation existence: **EVIDENCED**;
- human editorial/publication gate: **EVIDENCED IN CONTRACT/CODE**;
- live signal path design: **EVIDENCED IN IMPLEMENTATION**;
- persisted end-to-end live acceptance: **MISSING_EVIDENCE in this bounded pass**;
- Newsroom completion: **NOT ESTABLISHED**;
- blocker requiring human intervention: **NO** — the observed coordination failure is a resident capability-research handoff, not a demonstrated human/environment blocker;
- superseded/retired state: **NONE**.

## Revisit candidate

This family is a high-value revisit once terminal evidence exists because it touches real-world information, editorial interruption/pre-emption, provenance, and publication authority. Revisit only from persisted evidence, not from commit names or the existence of an acceptance script.

Minimum verification package:

1. unit suite PASS for Newsroom and Real Signal Loop;
2. one persisted live no-publish official-feed acceptance receipt;
3. replay dedupe proof;
4. correction/retraction revision proof;
5. PREPARED-operation recovery proof;
6. proof that a displaced lower-priority loop resumes;
7. proof that output remains editorial-review-only and cannot publish autonomously;
8. if a capability-recovery episode is claimed, a terminal resident-runtime receipt showing research/repair/verification and parent-goal resume.

## Canonical disposition

Treat Newsroom / Real Signal Loop as a newly discovered active product/runtime family that was absent from the canonical active-map wording inspected by Sweep 01. It belongs under the broader Doré distribution/editorial/runtime architecture, but must remain separately evidence-gated because `DORE-DISTRIBUTION` discovery status does not itself describe this implemented event-driven control plane.

Recommended active-map row when the canonical register is next safely rewritten in full:

`NEWSROOM | Verified-world-signal → editorial-review response loop | ACTIVE_PARALLEL / IMPLEMENTED_BUT_NOT_VERIFIED_COMPLETE | Event-driven control plane + free official-feed signal/revision store implemented; publication remains human-gated; terminal live acceptance not yet persisted in bounded evidence | Persist end-to-end no-publish live acceptance + dedupe/revision/recovery/resume receipts; then evaluate bounded completion`

Do not promote this family to `VERIFIED_COMPLETE` unless the verification package above is present. Do not treat the non-terminal peer-semantics failure as a P01 blocker or as a reason for user notification.
