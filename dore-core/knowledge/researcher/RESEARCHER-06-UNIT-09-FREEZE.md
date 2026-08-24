# Researcher 06 — Unit 09 Integration Freeze

Status: FROZEN — FRESH FINAL NOT YET OPENED
Date: 2026-08-24

## Frozen contract
- Mandarin encoder: `mandarin-pinyin-pro-v2-research` (Unit 08 frozen architecture).
- English phonetic channel: existing Researcher 06 encoder contract; no identity-specific patching.
- Normalization: Unicode/punctuation/case normalization only; observed transcript is retained verbatim in output.
- Candidate budget: bounded candidate generation; no exhaustive product-specific answer routing.
- Decision surface: `suggest | review | abstain`.
- Required evidence object: `observed`, `candidate`, `source/canonical_anchor`, `evidence_channels`, `score_boundary`, `decision`.
- Search adapter: may display a suggestion/recovered anchor but consumes the generic result unchanged.
- Subtitle adapter: may propose a correction/review but MUST retain observed text and MUST NOT silently overwrite it.
- Ambiguity rule: competing plausible identities/verses without sufficient separation => `review` or `abstain`, never forced certainty.
- Theological-attractor rule: doctrinal familiarity alone is not retrieval evidence.

## Development partition
`fixtures/noise-retrieval-unit09-dev.json` is development-only and permanently exposed. It may be used to debug the generic contract but can never count as fresh final evidence.

## Fresh-final protocol
The fresh final must be authored/sealed separately after this freeze and must cover all seven required evidence families. Once opened, the first result is authoritative. A failure is preserved; no exposed identity may be patched and re-scored as unseen evidence.

## Graduation threshold
PASS requires: zero gold misses within the frozen budget on positive fixtures; all ordinary negatives abstain; ambiguous fixtures do not become unjustified certainty; provenance survives both adapters; both adapters consume the same generic retrieval object; no per-question logic.

## Next action
`RESEARCHER_06_UNIT_09_IMPLEMENT_GENERIC_OFFLINE_TRANSFER_HARNESS_AND_RUN_DEV_GATE`.
