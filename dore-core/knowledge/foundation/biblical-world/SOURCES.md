# Biblical World — Source Register

Status: active Foundation source registry

## 1. OpenBible.info Bible Geocoding Data

Repository: `openbibleinfo/Bible-Geocoding-Data`
Pinned snapshot: `7eb18a5ee62f27b9b93bd6689ea272d76dd23b8f`
License: CC BY 4.0 (with separate ODbL considerations for OpenStreetMap-derived material)
Role: geographic candidate evidence, biblical-place attestations, modern-location candidates, resolution paths, and scholarly identification confidence.

Doré treatment:
- ancient biblical place identity is not the same object as a modern site;
- a coordinate is never treated as Scripture fact merely because a dataset supplies it;
- competing identifications remain competing identifications;
- dataset confidence is retained as source evidence, not converted into certainty;
- raw source attribution must remain visible in derived claims.

## 2. STEPBible TIPNR

Repository family: `STEPBible/STEPBible-Data`
Dataset: Translators Individualised Proper Names with all References (TIPNR)
License: CC BY 4.0
Role: disambiguated biblical proper nouns, Hebrew/Greek forms, translation forms, entity identity and exhaustive canonical references.

Doré treatment:
- TIPNR identifiers are source identifiers, not automatically Doré canonical entity IDs;
- names and transliterations are aliases with provenance;
- two people with the same surface name remain distinct entities;
- ambiguous names must not be auto-merged;
- AI-generated descriptive prose in upstream resources is not admitted as factual evidence without independent provenance.

## Evidence policy

These datasets are instructional witnesses, not authorities that replace Scripture or scholarship. Doré must retain source-specific identifiers and map them into its own evidence-first entity model.

For future additions, every source must record: snapshot/version, license, domain role, evidence class, known limitations, and whether redistribution into Core is permitted.
