# DORÉ MEMORY SWEEP — CHECKPOINT 22

Date: 2026-08-27
Status: RECONCILED / SWEEP CONTINUES
Parent sweep: `dore-core/projects/DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical index: `dore-core/projects/DORÉ-MASTER-WORK-REGISTER.md`

## Bounded evidence reviewed

- `dore-core/README.md`;
- current `dore-core/` repository tree;
- direct existence checks for README-named literal paths including `dore-core/core/`, `dore-core/research/` and `dore-core/providers/`;
- current Master Work Register architecture/evidence posture.

## Findings

1. The README previously presented `core/`, `research/`, `providers/`, `roles/`, `adapters/` and `tools/` as if they were literal current `dore-core/` directories. Direct repository checks show at least `dore-core/core/`, `dore-core/research/` and `dore-core/providers/` do not exist at the current main-branch tree.
2. This is documentation/implementation-contract drift, not proof that the corresponding capabilities are absent. Doré implementation is split across the hyphenated durable-source tree, the `dore_core/` Python package, Cloudflare/runtime code and product-specific boundaries.
3. The correct interpretation is therefore: those names describe architectural responsibilities/faculties, while implementation claims must be established by repository/runtime/test evidence rather than inferred from an architecture folder list.
4. The README has been corrected to list the durable source families that actually exist and to label Core/Research/Providers/Roles/Product adapters/Tools as architecture namespaces rather than current literal directories.
5. No Master Work Register status change is justified by this batch. The finding reinforces the existing evidence rule already used by `NERVOUS-SYSTEM`, `CONV-MEM-V1`, Search and other workstreams: architecture text is not implementation evidence.
6. No P01 state, subtitle runtime, production job or blocker was modified.

## Classification

- `dore-core/README.md` architecture map drift: `SUPERSEDED` wording, corrected in place.
- Doré architecture responsibilities: retain as `CORE/CONTINUOUS` doctrine/organization language.
- Implementation completion of any named architecture layer: evidence-gated by its own workstream; no new completion claim.

## Durable learning

A repository front-door document must distinguish three things explicitly:

`architecture responsibility != literal folder topology != verified implementation`

This prevents future memory sweeps and project planning from creating false missing-component alarms or false completion claims from directory names alone.

## Persisted correction

Commit `980ef441d61362623d3fc41262cfdd9fe64f566a` reconciles `dore-core/README.md` with the current implementation topology and evidence boundary.

Sweep 01 remains `ACTIVE_PARALLEL`. This bounded batch does not justify `VERIFIED_COMPLETE` and creates no new human or environment blocker.