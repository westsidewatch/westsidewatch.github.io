# Researcher 06 — Post-graduation capability diagnosis

Date: 2026-08-23
Status: DIAGNOSIS COMPLETE — COURSE NOT OPENED

## Sensory-first check

`dore-core/memory/sensory-active.json` is absent on `main`; no live user question was fabricated.

Infrastructure evidence now sharpens the blocker: `sensory-seed-diagnostic.json` records HTTP 500 / Cloudflare error 1101 when POSTing a test question to `/api/dore/sensory`, while the subsequent authenticated claim step completes but returns no signal. This is an ingestion-runtime failure, not evidence of a researcher knowledge gap.

## Capability-gap diagnosis

Graduated capabilities already cover:
- Biblical Languages I: bounded Hebrew/Greek research reading and lexical/morphological controls;
- Autonomous Learning I: gap detection, source selection, curriculum formation, examination and transfer;
- Biblical Concept Development I: diachronic/canonical concept tracing with corpus separation, counter-evidence and anti-retrojection controls.

No repeated evidence-backed *research-method* blocker currently justifies inventing a new Researcher 06 course.

The strongest unmet product/work prerequisite is instead the previously declared subtitle-proofreader path: robust Scripture quotation/allusion recognition under noisy Chinese/English input, names/transliteration variants, ASR confusions, context-sensitive ranking, and safe evidence-backed correction suggestions. This is a real external-work prerequisite and should be tested before deciding whether it requires a new course.

## Decision

Do **not** open Researcher 06 merely to maintain educational motion.

Next authorized learning action:

`SUBTITLE_PROOFREADER_PREREQUISITE_DIAGNOSTIC_01`

Run a bounded transfer benchmark against the existing Bible Search work node using noisy/partial Scripture quotations, biblical names, transliteration/ASR variants and uncertainty handling. Classify each failure as one of:
1. existing capability implementation defect;
2. missing corpus/index data;
3. missing reusable linguistic/retrieval skill;
4. higher-order research judgment already covered by graduated methods.

Open a new course only if category 3 failures repeat across independent cases and cannot be repaired by applying existing graduated methods.

## Separate infrastructure dependency

Sensory ingestion remains independently blocked at the Cloudflare POST runtime. Do not confuse that 500/1101 failure with Doré's educational readiness and do not claim PRODUCT → BRAIN closed-loop acceptance until a POST is durably written and later claimed into `sensory-active.json`.
