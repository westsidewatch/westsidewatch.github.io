# Researcher 06 — Unit 09 Offline Integration Transfer Gate

Status: ACTIVE — DESIGN / FREEZE REQUIRED
Date: 2026-08-24

## Authorization basis
Unit 08 passed its frozen one-shot unseen final, but that final covered one important perturbation family: same-pinyin single-Han corruption over biblical-entity surfaces. Researcher 06 has a broader course goal: recover Scripture and biblical entities from noisy/partial transcript evidence while preserving evidence boundaries and abstention. Therefore graduation requires one product-neutral integration transfer gate rather than immediate production promotion.

## Required consumers
The same generic retrieval contract must be exercised by at least two simulated consumers without consumer-specific answer logic:
1. Search-like query recovery.
2. Subtitle-proofreader candidate suggestion.

## Required evidence families
Use only previously authorized/researched families and fresh fixtures:
- exact/partial Scripture evidence;
- Mandarin homophone corruption;
- biblical entity corruption;
- deletion/insertion noise;
- transliteration/alias variation when fixtures and corpus support it;
- ambiguous competing candidates;
- ordinary nonquotation negatives.

## Required output contract
Every positive suggestion must keep separate fields for:
- observed input;
- candidate;
- source/canonical anchor;
- evidence channel(s);
- confidence or score boundary;
- abstain/review decision.

A candidate may not overwrite what was heard. Theological familiarity alone may not force a correction.

## Freeze protocol
Before opening any fresh final:
- define deterministic fresh fixture partition or separately authored sealed fixture set;
- freeze encoder IDs, normalization, candidate budget, ranking/abstention policy and consumer adapters;
- commit the harness and freeze record;
- then execute once and persist the first result.

## Pass policy
The final gate must demonstrate, at minimum:
- no gold miss in fresh positive fixtures within frozen candidate budget;
- all ordinary nonquotation negatives abstain;
- ambiguous fixtures do not collapse to unjustified certainty;
- both consumer adapters use the same generic retrieval result rather than separate hard-coded rules;
- provenance/evidence fields survive the full offline path;
- no exposed identity is patched after final opening.

## Promotion boundary
Even a PASS authorizes course graduation/retention-watch consideration, not automatic production deployment. Production Search/subtitle wiring remains a separate integration and human-impact boundary with regression requirements.

## Next action
`RESEARCHER_06_UNIT_09_BUILD_AND_FREEZE_OFFLINE_TRANSFER_HARNESS`.
