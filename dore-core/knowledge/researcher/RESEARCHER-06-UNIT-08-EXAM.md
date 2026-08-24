# Researcher 06 — Unit 08 Examination

Status: PASS
Date: 2026-08-24

The first durable one-shot result in `evidence/researcher06-unit08-v2-fresh-final.json` is accepted as authoritative unseen evidence for the frozen v2 architecture.

Result:
- 80 positives;
- 5 negatives;
- recall-at-budget 1.0;
- 0 gold misses;
- mean candidate set 2.4941;
- negative abstention 5/5;
- unknown Han rate 0;
- perturbation family `single-han-same-pinyin` x80;
- pass true.

Examination gate: 8/8 PASS.
1. Architecture frozen before final exposure.
2. Fresh partition independent of the retired Unit 06 final.
3. At least 40 unseen positives.
4. Zero gold misses inside budget 20.
5. All ordinary Mandarin negatives abstained.
6. Zero unknown Han on evaluated positives.
7. No identity-specific patching or product wiring.
8. Durable evidence and boundary preserved.

Interpretation: Unit 08 proves the corpus-wide Mandarin v2 encoder repairs the v1 coverage failure for unseen biblical-entity surfaces under same-pinyin single-Han corruption while preserving conservative abstention. It does not alone prove the full course goal across mixed transcript noise and multiple product consumers.

Next authorized action: `RESEARCHER_06_UNIT_09_OFFLINE_INTEGRATION_TRANSFER_GATE`.

Unit 09 must remain non-production and product-neutral. It should combine previously learned components, test multiple noise families across Search-like recovery and subtitle-proofreader candidate suggestion, preserve `observed -> candidate -> source -> confidence`, require abstention under ambiguity/nonquotation, freeze the integration contract before fresh evaluation, and avoid per-question or per-product hard-coded routing.
