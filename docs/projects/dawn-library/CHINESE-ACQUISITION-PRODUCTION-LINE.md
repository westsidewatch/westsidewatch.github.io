# Dawn Chinese Acquisition Production Line

Status: ACTIVE
Date: 2026-09-25

The Chinese acquisition mainline is now a production line, not a source-listing exercise.

## Flow

`trusted provider catalog / attachment`
→ `fetch / export`
→ `catalog normalizer`
→ `static/dawn-library/acquisition/chinese/*.json`
→ `materialize-chinese-acquisition-candidates.mjs`
→ `203,448 canonical Work reconciliation`
→ `MATCH_EXISTING | EDITION_OR_RESOURCE | NEW_WORK_CANDIDATE | RIGHTS_DEFERRED | POLICY_REJECTED`
→ `rights + relevance + authority admission`
→ `canonical Work / Edition / Resource admission`
→ `semantic + material projection`
→ `Chinese gap rescan`

## Hard boundaries

- Chinese discovery and promotion are prioritized, but admission standards are not lowered.
- Wikisource remains prohibited at discovery and canonical admission.
- Political / ethnic / war controversy material remains outside Dawn Library admission scope.
- Availability of a catalog, scan, PDF, image, video or attachment never implies rehost rights.
- Provider metadata may support discovery/reconciliation without becoming canonical identity authority.
- Periodical issues, scans, translations, reprints and manuscripts do not automatically become distinct Works.
- The production line extends the existing canonical pipeline; it does not create a parallel Chinese library.

## Attachment contract

The normalizer accepts UTF-8 CSV, TSV, JSON and JSONL. Provider XLS/XLSX/PDF catalogs should be fetched/exported once and converted into one of these normalized interchange formats. The normalized candidate output keeps provider identity and rights state separate from canonical admission.

## Success measure

A batch is not considered successful because a source was discovered or a workflow passed. It must report non-zero candidate rows and then report explicit reconciliation/admission counts. Canonical growth is counted only after admission.
