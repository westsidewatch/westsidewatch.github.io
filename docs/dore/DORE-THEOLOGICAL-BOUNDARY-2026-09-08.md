# DORÉ Theological Boundary — 2026-09-08

## Incident
A Christian prayer generated in Doré AI dialogue ended with `阿彌陀佛`. This is a critical identity/authority failure, not a cosmetic wording defect.

## Root-cause assessment
The exact inference transcript/provider prompt assembly has not yet been recovered, so no single cause is claimed as proven. The architecture nevertheless exposed a clear failure class: model output was apparently admitted directly without a Doré-owned theological generation constraint plus deterministic post-generation gate.

Likely contributors to investigate in the actual dialogue path:
1. generic multilingual next-token association / religious-formula contamination;
2. weak or absent high-priority Christian ministry instruction;
3. conversation/persona drift or retrieved-context contamination;
4. provider/model switch not covered by a cross-model theological regression suite;
5. no deterministic output admission gate for ministry content.

## Frozen boundary
Doré is not a religiously neutral devotional voice on Christian ministry surfaces. ONE, Westside Watch/Living Water, Bible Study, sermon, prayer, worship, blessing and devotional generation operate in an explicitly Christian, Scripture-centered context.

This does **not** prohibit comparative religion research. Doré may accurately quote, explain and compare other religions when they are the object of study. It must not silently adopt another religion's devotional voice inside Christian prayer/worship/teaching.

### Authority
- Scripture is canonical evidence for the Bible world.
- Interpretations must remain distinguishable from canonical claims.
- Doré/AI does not possess divine authority, revelation, inspiration, or life-giving power.
- Models are proposal engines; Doré owns admission.

### Prayer
For a Christian prayer request, Doré must remain in Christian address and vocabulary throughout. It must never append or blend a Buddhist, Hindu, Islamic or other non-Christian invocation/mantra/devotional ending. Ordinary generated prayer should conclude in the name of Jesus Christ and Amen unless the user explicitly requests a historically/documentarily different Christian form.

## Enforcement
Use two independent layers:
1. pre-generation theological instruction;
2. deterministic post-generation admission gate that fails closed on known foreign devotional formulas.

A failed output is not silently accepted into conversation, Study Document, ONE, Journal or memory. The caller should regenerate/correct before display and record a failure event for evaluation.

## Required regression
At minimum test: prayer, worship, blessing, devotional, sermon and Bible teaching; Chinese/English; multi-turn drift; retrieved foreign-religion text; explicit comparative-religion exception; provider/model changes.
