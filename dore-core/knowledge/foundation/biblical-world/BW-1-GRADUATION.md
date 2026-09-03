# Doré Biblical World — BW-1 Graduation

Status: **COMPLETE — PASS**
Completed: 2026-08-22
Section: **BW-1 Entity identity and aliases**
Major milestone: **NO** — `BIBLICAL_WORLD_COMPLETE` remains reserved for BW-1 through BW-6 plus the canon-spanning blind exam.

## What graduated

Doré now has an evidence-bearing entity layer rather than a proper-name string list.

The graduated route is:

`mention/question → scope (ONE chapter or global canon) → exact entity/alias candidates → type separation → context ranking → canonical attestations → ambiguity/aggregation → bounded result`

Capabilities included in the gate:

- full-source entity ingestion from pinned STEPBible TIPNR;
- TIPNR format/documentation lines are rejected rather than admitted as entities;
- stable individualised identities and canonical attestations;
- person/place type separation;
- equal-looking names remain distinct unless evidence resolves them;
- cross-language source aliases;
- conservative Chinese translation aliases derived from CUV + TIPNR canonical co-attestation;
- ONE chapter scope may rank an entity without erasing global candidates;
- canon-wide same-name aggregation;
- translated names can resolve to a source-name identity cluster without merging those individual identities;
- natural-language entity-count intent such as `聖經有幾位馬利亞？`;
- browser Doré Search connection to the entity corpus;
- exact entity routing prevents substring identity pollution such as `馬利亞` being treated as `撒馬利亞`.

## Real-corpus gate evidence

The final end-to-end report `reports/DORÉ-BW1-ENTITY-GRADUATION.json` records PASS with:

- **4,293** cleaned derived entities;
- **2,876** conservative Chinese aligned aliases;
- Mary person resolution PASS;
- Samaria place resolution PASS;
- Mary/Samaria identity separation PASS;
- translated-name → source-name cluster expansion PASS;
- person-only count aggregation PASS;
- natural-language count intent PASS;
- unseen count-intent transfer PASS;
- public entity runtime connection PASS.

For the diagnostic Mary stimulus, only two individualised records carried a direct inferred Chinese alias `馬利亞`, but the evidence route correctly resolves that translated name to the source-name cluster of **six individualised Mary person records**. This is source-identity aggregation, not a theological assertion that all later identity questions are settled.

The browser corpus is persisted as `static/dore/entity-index.json`; raw TIPNR is not redistributed.

## Evidence boundary

A Chinese aligned alias is a routing aid produced from repeated canonical co-attestation. It is not independent proof that two identities are identical. Source identity and canonical attestations remain primary.

A canon-wide count is a count of source-individualised identity candidates. If later research/tradition disputes whether candidates should be merged, Doré must expose that dispute rather than silently force one number.

ONE editorial material may provide passage scope and user-intent stimuli, but is not automatically identity evidence.

## Live work tests

Primary known live checks:

- `馬利亞` — entity route must not be polluted by `撒馬利亞`.
- `聖經有幾位馬利亞？` — must trigger canon-wide person aggregation, not raw substring search.

These examples are diagnostic stimuli, not hard-coded answer keys. Transfer behavior is required for other names.

## Next education section

Proceed to **BW-2 Geography**, carrying the same dual-learning rule:

**Knowledge + Reflex**, with Doré Search and ONE continuing as work/learning nodes.

## Sweep 01 reconciliation — 2026-09-02

The earlier prose count of **3,592** Chinese aligned aliases conflicted with the persisted machine graduation report, whose `counts.chinese_aliases` value is **2,876**. The machine report is the stronger milestone evidence, so this graduation record has been corrected to 2,876. This numerical correction does **not** invalidate the bounded BW-1 PASS because every named boolean graduation check remains true in the persisted report. It does, however, establish a durable rule for completed-work review: when narrative milestone prose and its machine report disagree on a measured count, the machine report governs until a newer reproducible report proves otherwise.
