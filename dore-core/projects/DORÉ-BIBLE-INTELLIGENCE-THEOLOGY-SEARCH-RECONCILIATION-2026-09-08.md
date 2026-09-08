# DORÉ Bible Intelligence / Search / Theology Boundary Reconciliation

Date: 2026-09-08
Status: EVIDENCE_LEDGER / SWEEP_01
P01 impact: NONE

## Bounded evidence

- commit `6d8c61d659fff6998daa60af9d93877016e65931` — BI-1 domain contracts and engineering baseline;
- commit `50bf068cf42a779009abb7bd9e96b37aae319a38` — production corpus index + bounded local action;
- commit `311f51e935f23e4757b08c6508cb74bf4564a344` — Christian ministry theological boundary implementation;
- commits `f7b9ab38fb284e7fd99f2ea0097f2a77e344cbef`, `3c8204b2a777c4e8d0e33b734b22017f12bb419f`, `790409d0d5ac629d7300d098173399be90c373c2`, `27d84113dfb81db520ef1cc14c9eae603a20981a`, `29fa404dd978e408751f0f89ecc2436682ba4c94`, `46ef68176fefab3d3546a97060988b2e1928a3d9` — bounded real-Mac theology acceptance/control-plane wiring and canonical gate reuse;
- commit `37661d22d6fad89c0cee70f3bb5fcd72c238d652` — post-checkpoint prayer-delivery refinement: prayer-specific instruction now requires the prayer itself without explanatory framing, and the canonical close validator accepts presentation-only punctuation/Markdown/quotation wrappers after final Amen while still rejecting lexical/devotional material after Amen;
- commit `0735a79e5b4643c18be81f2ebdff4f7c942b794c` — isolated theology-alignment MLX micro-POC, quarantine contract, readiness probe, tests and hard execution order;
- commit `e8cd4f17789d6f30e1ffcef84488be8ecdf18bd1` — bounded `theology.training.readiness` A2A capability and local-routing-host test alignment;
- commit `cc253d12300b06ff6c49fb5b9c9e7112feffaef3` — correction separating runtime model identity from the dedicated MLX training-model identity.

## Reconciliation

1. **BI-1 is implementation progress, not Bible Intelligence completion.** Provider-neutral `BibleReference`, Study Document/Flow and contextual search-policy contracts are real code. Their own implementation notes explicitly say UI and provider wiring are not yet complete. Current classification: `ACTIVE / FOUNDATION` under the existing Bible/Search/ONE/Multiwrite architecture; no global Bible Intelligence completion token is justified.

2. **The Search production corpus index is a real new substrate boundary.** Repository-authored `.md`/`.txt` under governed source families are copied into a local QMD production collection with SHA-256 manifest provenance and `authority:false`. QMD remains retrieval substrate, not Knowledge Authority. This is meaningful `ACTIVE / IMPLEMENTED_NEEDS_RUNTIME_PROOF` Search infrastructure, not proof of production retrieval quality by itself.

3. **The Christian ministry theological boundary is a legitimate authority-layer implementation milestone.** The production local dialogue path now has a Doré-owned pre-inference Christian ministry instruction plus deterministic post-generation admission, bounded regeneration and fail-closed delivery for ministry tasks. Comparative-religion research is explicitly separated from devotional authority. The Core deliberately avoids storing contamination watchword lists.

4. **Acceptance wiring is materially stronger than unit-only evidence.** A bounded real-Mac `theology.live.acceptance` capability was added to the local control plane, wired to the active A2A checkout, and later changed to validate live prayer output through the same canonical `christian_ministry_gate` rather than duplicating acceptance logic. This is the correct single-authority direction.

5. **The prayer boundary received one useful post-checkpoint refinement, but this is not new completion evidence.** Commit `37661d22d6fad89c0cee70f3bb5fcd72c238d652` makes prayer delivery stricter at instruction time while making deterministic validation tolerant of presentation-only wrappers after the terminal Amen. Classification: `ACTIVE / IMPLEMENTATION_REFINEMENT`. It supersedes the narrower final-Amen punctuation matcher as implementation detail, but does not supersede the canonical theology gate or change the evidence threshold for completion.

6. **Do not overclaim VERIFIED_COMPLETE yet.** The inspected commits prove implementation and acceptance-harness wiring, but this bounded batch did not recover a persisted terminal acceptance artifact showing all required live checks passing across Chinese/English prayer, comparative-research exception, multi-turn drift, worship/blessing/devotional/sermon/Bible teaching, provider/model changes and rejected-candidate non-disclosure. Current theological-boundary classification remains `ACTIVE / PARTIALLY_VERIFIED`; missing evidence is the persisted full regression result.

7. **Architecture convergence improved.** BI-1 and the theology boundary both reinforce the same durable rule already present elsewhere: models/substrates propose; Doré owns evidence, ranking, policy and admission. This should be retained as a cross-product authority principle under CORE/NERVOUS-SYSTEM rather than duplicated per product.

8. **The theology-alignment training POC is a real engineering workstream but is not training completion.** Commit `0735a79e...` adds an isolated MLX-LM adapter orchestrator, read-only readiness probe, quarantine enforcement excluding Doré runtime/core data locations, minimum-sufficient 0→32→64→128→256 learning stages, test coverage and an explicit order requiring live Theology Rails acceptance before any training execution. Its own status text says `TRAINING NOT YET EXECUTED`. Classification: `ACTIVE_PARALLEL / ENGINEERING_POC`, with completion evidence still absent.

9. **The quarantine boundary is a durable capability/safety principle.** Adversarial/devotional training fixtures must remain outside Doré Knowledge, Memory, Search, Bible World and canonical stores. Only abstract policy/evaluation results and, after gates, the adapter artifact may be admitted. This prevents foreign devotional material from silently becoming Doré authority while still allowing bounded behavioral alignment experiments.

10. **A2A readiness exposure is bounded and correctly non-mutating.** Commit `e8cd4f17...` exposes only fixed `theology.training.readiness` through the local routing host; it accepts no arbitrary shell command, performs no package/model installation, no canonical ingest and no training execution. This is an `ACTIVE / READINESS_CONTROL_PLANE` milestone, not evidence that the Mac is actually training-ready.

11. **The original POC model-identity assumption was corrected before execution.** Commit `cc253d12...` supersedes the earlier use of `DORE_LOCAL_MODEL` as the MLX trainer identity. Runtime inference and MLX training now have separate identities, with training requiring explicit `DORE_THEOLOGY_MLX_MODEL` or `--model`. This correction is important because an Ollama runtime model name is not automatically a valid MLX-LM training model. The pre-correction single-model assumption is `SUPERSEDED` as an implementation detail.

12. **No new human/environment blocker is established by repository code alone.** The readiness path can report whether arm64, `mlx-lm`, and a dedicated training model are present, but this bounded sweep did not recover a persisted real-Mac readiness result. Therefore missing configuration/dependency must remain `UNKNOWN_NEEDS_EVIDENCE`, not be promoted to `ENVIRONMENT_BLOCKED` until the actual probe is persisted.

13. **No P01 action or state changed.** The production subtitle audio/transcription environment dependency remains isolated and untouched.

## Current dispositions

- BI-1 domain contracts: `ACTIVE / FOUNDATION`.
- Search production QMD corpus index: `ACTIVE / IMPLEMENTED_NEEDS_RUNTIME_PROOF`.
- Christian ministry theological boundary: `ACTIVE / PARTIALLY_VERIFIED`.
- Prayer-delivery/presentation-wrapper refinement: `ACTIVE / IMPLEMENTATION_REFINEMENT`; retain under the canonical theology gate.
- Narrower pre-refinement terminal-Amen matcher: `SUPERSEDED` as implementation detail by commit `37661d22d6fad89c0cee70f3bb5fcd72c238d652`.
- Theology-alignment MLX micro-POC: `ACTIVE_PARALLEL / ENGINEERING_POC`; training not yet executed.
- Theology training readiness A2A action: `ACTIVE / READINESS_CONTROL_PLANE`.
- Pre-correction assumption that `DORE_LOCAL_MODEL` is also the MLX training model: `SUPERSEDED` by dedicated `DORE_THEOLOGY_MLX_MODEL` identity.
- Real-Mac MLX readiness: `UNKNOWN_NEEDS_EVIDENCE` until a persisted probe result exists.
- Canonical admission reuse in live acceptance: retain; duplicate acceptance logic is superseded.
- Bible Intelligence global completion: not justified.

## Smallest next proofs

1. Persist one production `search.production.index` execution artifact with document count, manifest path, QMD update success and at least one provenance-bearing retrieval readback.
2. Persist one terminal `theology.live.acceptance` artifact proving Chinese + English prayer admission, comparative-research exception and rejected-candidate non-disclosure from the guarded local endpoint.
3. Extend theology regression to worship, blessing, devotional, sermon, Bible teaching, multi-turn drift and provider/model replacement before any `VERIFIED_COMPLETE` claim.
4. Persist one read-only `theology.training.readiness` result from the real Mac proving exact runtime model, dedicated MLX training model identity, arm64 state and `mlx-lm` availability; only after live Theology Rails acceptance may the 32-example quarantined adapter run begin.
5. For the first 32-example run, persist peak unified-memory use, wall-clock time, adapter size, blind bilingual base-vs-adapter delta, no canonical ingest/no paid API, and an adapter-load fingerprint. Continue to 64/128/256 only on material improvement.
6. Continue BI-2 only behind the provider-neutral Doré contract; do not expose QMD/provider names to ONE or Multiwrite UI.
