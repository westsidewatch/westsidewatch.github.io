# Baseline Witness Access Survey — Batch 01

Status: ACTIVE
Date: 2026-08-22

This batch begins execution of Doré's Chinese/English baseline witness curriculum. The purpose is to identify trustworthy lawful full-corpus sources first, then ingest by family rather than hand-feed verses.

## Confirmed Tier 1 candidates

### English — KJV
- role: baseline / historical-mainstream
- candidate corpus: midvash/bible-data `kjv` (1769)
- declared status: public domain
- alternative verification source: TheologyCommons/Bible.TEI.KJV (JSON/XML; repository describes KJV text as public domain)
- action: ingest after pinned-snapshot verification

### English — ASV
- role: baseline / research lineage
- candidate corpus: openbibleinfo/American-Standard-Version-Bible (1901)
- format: USX
- declared status: public domain
- independent verification: eBible.org identifies ASV 1901 as public domain and provides developer formats
- action: ingest after pinned-snapshot verification

### Chinese — CUV traditional
- role: baseline / mainstream
- current corpus already integrated through midvash/bible-data
- declared status there: public domain
- additional open-bibles source lists traditional CUV as public domain
- action: retain as baseline corpus and compare against New Punctuation witness

### Chinese — 新標點和合本 / Chinese Union Version with New Punctuation
- role: baseline / mainstream
- eBible.org witness id: cmn-cu89t
- eBible.org currently labels the traditional-script witness public domain and exposes USFM/USFX and other developer formats
- note: a separate Biblia/Logos rendering identifies a UBS 1988/1989 copyright for a simplified Shen edition. Therefore edition identity and rights must not be conflated. Doré must pin the exact eBible witness and preserve its rights declaration rather than generalize rights across all New Punctuation editions.
- action: candidate Tier 1 only for the exact eBible witness after source package/license metadata are pinned and checked

## Important access finding

A version title is not sufficient to determine rights. Script, edition, publisher, revision, Shen/Shangti edition, and digital source can have different rights declarations. Access policy therefore attaches to an exact `witness_id + edition + provider + snapshot`, never merely to labels such as `CUV` or `新標點和合本`.

## Batch execution order

1. Pin and ingest KJV 1769.
2. Pin and ingest ASV 1901.
3. Verify exact eBible 新標點和合本 package and rights metadata; ingest only if the exact downloadable witness permits it.
4. Continue official-access survey for RCU, 呂振中, TCV, CNV, Recovery Version, NCB, Studium Biblicum, NIV, ESV, NRSVue, NASB, NLT, NET, CSB, RSV.
5. For each non-Tier-1 witness, establish API/external-reader/human-only routing rather than copying full text.

## Guardrail

No corpus is promoted to `BIBLICAL_CORPUS_READING_COMPLETE` merely because a similarly named edition is public domain. Exact witness provenance and access rights must pass first.
