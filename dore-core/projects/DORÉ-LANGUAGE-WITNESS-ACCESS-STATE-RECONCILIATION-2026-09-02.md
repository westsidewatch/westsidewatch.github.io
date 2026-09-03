# DORÉ LANGUAGE WITNESS ACCESS STATE RECONCILIATION — 2026-09-02

Status: SWEEP_01_BOUNDED_RECONCILIATION
Sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01`
Related canonical work: `SCRIPTURE-CANON`, `CORE`, `ME-011`

## Bounded evidence reviewed

- `dore-core/knowledge/foundation/language-text/BASELINE-ACCESS-SURVEY-01.md`
- `dore-core/knowledge/foundation/language-text/CHINESE-ENGLISH-WITNESS-REGISTRY.yaml`
- `dore-core/knowledge/foundation/language-text/WITNESS-ACCESS-ARCHITECTURE.md`
- canonical `DORÉ-MISSING-EVIDENCE-REGISTER.md` entry `ME-011`
- canonical `DORÉ-MASTER-WORK-REGISTER.md` Scripture/Foundation interpretation

## Finding 1 — the access survey is discovery evidence, not current execution authority

`BASELINE-ACCESS-SURVEY-01.md` records candidate Tier-1 routes, including KJV/ASV and an exact eBible New-Punctuation CUV witness candidate. It explicitly says these are candidates pending pinned-snapshot / package / rights verification and warns that similarly named editions can carry different rights.

The later/current machine-readable `CHINESE-ENGLISH-WITNESS-REGISTRY.yaml` is more conservative:

- CUV is the only Chinese baseline witness marked `local_corpus / ingested`;
- New-Punctuation CUV is `human_only / source_verified_access_pending`;
- RCUV, TCV and Lü Zhenzhong are also `human_only / source_verified_access_pending`;
- CNV, Recovery Version, NCB and Studium Biblicum remain `access_survey_required`;
- WEBU is the only English baseline witness marked `local_corpus / ingested`;
- KJV and ASV remain `local_corpus_candidate / source_and_license_survey_required`;
- the remaining named English baselines remain `human_only / licensed_access_survey_required`.

Current governing interpretation: **candidate discovery does not equal authorization or ingestion state**. The registry's restrictive state governs execution until an exact witness/provider/snapshot is verified and deliberately promoted.

## Finding 2 — apparent New-Punctuation CUV conflict is resolved by exact-witness identity

The access survey notes an eBible traditional-script New-Punctuation CUV candidate whose provider page appeared to label that exact downloadable witness public domain, while separately warning that other similarly named editions/renderings carry UBS/HKBS copyright claims. The current registry instead records the baseline `cunp` entry as HKBS, `human_only`, `source_verified_access_pending`.

This is not evidence that either record is simply false. It is evidence that the registry currently collapses a **version family label** (`新標點和合本`) into one baseline entry while the survey had identified a potentially different exact digital witness/provider package.

Therefore the safe canonical rule is:

1. do not generalize rights from the eBible candidate to the whole New-Punctuation CUV family;
2. do not generalize the HKBS human-only baseline policy to a separately verified exact public-domain/permissive digital witness without evaluating identity and provenance;
3. if the eBible candidate is reconsidered later, give it its own exact `witness_id + edition + provider + snapshot + rights` identity before any Tier-1 promotion.

Until then, the current registry's restrictive state remains correct for production behavior.

## Finding 3 — ME-011 remains evidence-correct and is more specific than a generic “corpus missing” claim

The witness family is not empty: CUV and WEBU are already ingested, and original-language substrate milestones have separate bounded PASS evidence elsewhere. But the named `BIBLICAL_CORPUS_READING_COMPLETE` gate is much broader: every baseline witness requires a sourced dossier and verified lawful access policy, local corpora need canonical coverage validation, authorized non-local witnesses need tested canonical-reference routing, and comparison benchmarks must span Chinese, English and original-language evidence.

The current registry itself shows many baseline witnesses still in survey/pending states. No evidence in this batch justifies promoting `ME-011` or issuing `BIBLICAL_CORPUS_READING_COMPLETE`.

Classification remains:

- Language/Text witness-access doctrine: `CORE/CONTINUOUS`;
- current baseline witness expansion: `ACTIVE / FOUNDATION`;
- global biblical corpus-reading completion: `UNKNOWN_NEEDS_EVIDENCE` under `ME-011`;
- no `VERIFIED_COMPLETE`, `COMPLETED_REVISIT_CANDIDATE`, `RETIRED`, or broad migration claim is warranted.

## Durable supersession rule

Where a discovery memo says `candidate`, `Tier 1 candidate`, `ingest after verification`, or similar, and the current witness registry still says `human_only`, `access_pending`, or `source_and_license_survey_required`, the **registry state governs execution**. The older candidate statement remains provenance for a future access investigation but must not silently reactivate ingestion.

This is a narrow historical-supersession rule, not retirement of the survey document.

## Smallest useful future evidence

For one pending witness at a time:

1. establish exact edition/provider/package identity;
2. pin authoritative license/terms evidence and snapshot;
3. assign an explicit access tier under `WITNESS-ACCESS-ARCHITECTURE.md`;
4. if local corpus is authorized, ingest and run canonical coverage/provenance validation;
5. if only API/external-reader access is authorized, persist a tested canonical-reference route with caching/quotation constraints;
6. update the machine-readable witness registry only after those gates pass.

Do not chase this work merely to manufacture sweep progress; it remains subordinate to P01.

## P01 protection

No P01 subtitle code, runtime state, deployment, binding, credential, ordering, or blocker state was changed by this reconciliation. The existing production audio-acquisition/transcription environment dependency remains untouched.

## Sweep accounting

This bounded pass explicitly accounts for the current Chinese/English witness-access state and resolves the survey-vs-registry chronology without inventing permission. Sweep 01 remains `ACTIVE_PARALLEL`; this batch does not justify `VERIFIED_COMPLETE`.