# BI-1 Implementation Notes

This slice establishes domain contracts only. It intentionally does not wire UI or substrate-specific search providers yet.

Implemented:
- `BibleReference`
- `StudyBlock`, `StudyFlowItem`, `StudyDocument`
- `SearchContextPolicy`
- Prepare / Live / Present policy semantics
- ONE self-suppression when Multiwrite is embedded in ONE
- default Keep / Flow / Present actions on contextual results

Next code slice:
- extend current normalized Context Result with `source_kind`, `canonical_reference`, `evidence_status`, and `actions` while preserving legacy fields
- thread `host`, `mode`, `embedded` context through `context.fuzzy-search`
- apply policy after provider-neutral result normalization
- add regression coverage proving standalone Multiwrite may recommend ONE while embedded Multiwrite in ONE cannot self-recommend ONE
