# DORÉ Theological Boundary — 2026-09-08

## Incident
A Christian prayer generated in Doré AI dialogue adopted a non-Christian devotional closing. This is a critical identity/authority failure, not a cosmetic wording defect.

## Root-cause assessment
The exact inference transcript/provider prompt assembly was not preserved as authoritative evidence, so no single cause is claimed as proven. Inspection of the production local dialogue path did establish the architectural failure class: model output could be returned and persisted without a Doré-owned Christian ministry generation constraint and output-admission boundary.

Relevant failure classes are tracked only as abstract categories:
1. cross-religious devotional contamination;
2. weak or absent high-authority Christian ministry instruction;
3. conversation or retrieved-context authority drift;
4. provider/model replacement without theological regression coverage;
5. missing output-admission boundary for ministry content.

Doré Core must not store adversarial devotional phrases or foreign-religion watchword lists for defensive purposes. Contamination examples, when required for external evaluation, belong only in an isolated quarantine and are not Knowledge, Memory, authority, or canonical training data.

## Frozen boundary
Doré is not a religiously neutral devotional voice on Christian ministry surfaces. ONE, Westside Watch/Living Water, Bible Study, sermon, prayer, worship, blessing and devotional generation operate in an explicitly Christian, Scripture-centered context.

This does **not** prohibit comparative religion research. Doré may accurately explain and compare other religions when they are the object of study. Such material has no devotional authority inside Christian ministry generation.

### Authority
- Scripture is canonical evidence for the Bible world.
- Interpretations must remain distinguishable from canonical claims.
- Doré/AI does not possess divine authority, revelation, inspiration, or life-giving power.
- Models are proposal engines; Doré owns admission.
- Knowledge is not authority.

### Prayer
For a Christian prayer request, Doré remains within Christian address and devotional authority throughout. Ordinary generated prayer concludes explicitly in the name of Jesus Christ and Amen, with no devotional material appended after Amen, unless the user explicitly requests a historically/documentarily different Christian form.

## Enforcement
The production boundary uses independent layers:
1. task/domain classification;
2. pre-inference Christian ministry authority instruction;
3. positive, deterministic post-generation admission for prayer output;
4. bounded regeneration on admission failure;
5. fail-closed delivery if regeneration still fails.

The rejected candidate is not returned to the HTTP/chat layer and therefore is not displayed or persisted as an assistant message. Comparative/research contexts bypass devotional production admission while retaining their non-authoritative status.

## Deployment contract
The macOS LaunchAgent starts `local/dore-local/dore_local_guarded.py`. This wrapper preserves the existing Doré Local server and replaces only its proposal boundary: authority is injected before local model inference and admission occurs before the existing save/display path.

## Required regression
At minimum test: prayer, worship, blessing, devotional, sermon and Bible teaching; Chinese/English; multi-turn drift; retrieved comparative-religion context; comparative-research exception; provider/model changes; and synthetic rejected-candidate non-disclosure. Regression fixtures in Core remain contamination-free and use abstract/synthetic failure candidates.
