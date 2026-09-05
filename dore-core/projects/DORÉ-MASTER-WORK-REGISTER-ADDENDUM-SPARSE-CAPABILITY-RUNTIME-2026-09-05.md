# DORÉ MASTER WORK REGISTER — ADDENDUM: SPARSE CAPABILITY RUNTIME

Date: 2026-09-05
Status: CANONICAL_ADDENDUM / SWEEP_RECONCILED
Parent register: `DORÉ-MASTER-WORK-REGISTER.md`
Evidence: `DORÉ-SPARSE-CAPABILITY-RUNTIME-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-A2A-CONTROL-PLANE-LOCAL-BRIDGE-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-CONSTITUTION-RECONCILIATION-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-IMAGE-ITERATION-DESIGN-HANDOFF-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-RESIDENT-IMAGE-PIPELINE-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-RESIDENT-IMAGE-AUTORUN-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-COMPANION-NATIVE-MESSAGING-EVIDENCE-LEDGER-2026-09-05.md`, `DORÉ-COMPANION-1-EXTENSION-SHELL-EVIDENCE-LEDGER-2026-09-05.md`
P01 impact: NONE

## Canonical interpretation

The following interpretation supplements the current `CORE`, `EVOLUTION`, `NERVOUS-SYSTEM`, `VIS-GRAMMAR` / Doré Visual and Memory Sweep entries until folded into the main register text.

### CAPABILITY-RUNTIME — Sparse capability embodiment

**Status:** `ACTIVE_PARALLEL / FOUNDATION`

Doré's runtime identity is one persistent intelligence with sparsely activated capabilities. Doré Image and Doré Design remain distinct engineering work packages where useful, but they are not separate intelligences and should not perform normal work through free-form agent-to-agent conversation. Shared typed state + capability routing is the governing runtime direction.

A bounded implementation milestone is now real: compact capability manifests, lazy activation, trigger-anchored routing, typed shared visual state, one-state execution, replaceable providers, focused probes/tests and an offline evidence-based consolidation ledger exist in repository code. This is `VERIFIED_COMPLETE_SUBMILESTONE`, not completion of the full sparse-embodiment architecture.

A second bounded convergence submilestone is now also real: the mature local A2A adapter v0.3 lazily constructs the shared capability runtime/executor and routes typed `dore.a2a/1` control envelopes into the Design control plane instead of creating a second local intelligence/server path. The same bounded commit sequence adds the canonical resident localhost `4312` / Companion path and Design as the first control-plane consumer, while capability-runtime CI configuration now includes the adapter bridge test. This is implementation evidence and a `VERIFIED_COMPLETE_SUBMILESTONE`; it is **not** yet latest-head CI/runtime acceptance.

A third bounded visual-runtime submilestone is now real: Doré Image has a bounded `generate → vision observations → critic → correction → regenerate` loop with explicit iteration limits/terminal reasons, and accepted image artifacts can cross into Doré Design through typed `dore.design.image-patch.v1` payloads preserving asset identity, checksum, geometry and provenance. Unit tests verify correction-then-accept behavior, identity preservation and invalid-geometry refusal. This is `VERIFIED_COMPLETE_SUBMILESTONE` implementation evidence only: the tested renderer and vision reader are synthetic, no commit-associated workflow run receipt is persisted for the introducing commit, and no real purpose-built Westside asset has yet been proven through live generation → real visual judgment → correction → real Design application.

A fourth bounded resident-image submilestone is now real: Doré can compile visual recipes into a provider workflow, request a resident render, fetch the returned image bytes into Doré-owned storage, enforce content-type/empty/size guards, hash and persist a content-addressable artifact record with provenance/recipe/brief, and emit critic input that explicitly refuses visual acceptance until actual vision observations exist. Correction direction can re-enter a later generation prompt. This is `VERIFIED_COMPLETE_SUBMILESTONE` implementation evidence, not a real-media acceptance result. The introducing commits have no associated GitHub workflow-run receipt, and the bounded tests use synthetic/fake provider bytes; real ComfyUI/model execution, real visual review and real product application remain `UNKNOWN_NEEDS_EVIDENCE`.

A fifth resident-runtime submilestone is now real: `scripts/dore_image_autorun.py` and `dore.image.resident.v1` add a bounded zero-terminal execution seam around the resident image pipeline. The runtime discovers local configuration, distinguishes `NOT_READY` / `IDLE` / `PASS`, rejects non-loopback renderer endpoints, health-checks the resident renderer, consumes a queued image job, persists `last-completed.json`, and removes the consumed job only after generation returns. This is `VERIFIED_COMPLETE_SUBMILESTONE` orchestration evidence, not proof of a real configured ComfyUI/model render. The introducing commit has no persisted workflow-run receipt; missing/unreachable resident configuration remains readiness evidence until an actual configured runtime attempt proves a blocker.

A sixth control-plane transport submilestone is now real: Firefox Native Messaging is the governing Companion→Doré production-carrier direction, preserving the existing `dore.a2a/1` adapter/control-plane seam while keeping `localhost:4312` as compatibility/debug fallback. The native host is a bounded local stdio carrier, the installer preflights downloaded host code before switching the current snapshot, and follow-on contract tests pin native-first ordering, host/extension identity and fallback role. This is `VERIFIED_COMPLETE_SUBMILESTONE` implementation/contract evidence. The associated commit-run surfaces currently contain no persisted workflow receipt and there is no persisted live Mac browser→native→host→adapter→Design acceptance, so latest-head CI and live-native acceptance remain `UNKNOWN_NEEDS_EVIDENCE`. The old idea of `4312` as the primary Companion production carrier is superseded; retain it under `MAINTENANCE` until live native acceptance is persisted.

A seventh Companion product-shell submilestone is now real at commit `2e2db37df4b30ad6b2ae5be499c54c8da34e5885`: a Firefox-installable Companion 1.0 manifest, ChatGPT content-script command capture, live health/status badge, background command bridge, and native-first `dore.a2a/1` dispatch wiring now exist as one coherent extension shell. Contract tests pin installable-manifest identity, `/dore` capture, health/status signaling and routing into the native transport module. This is `ACTIVE_PARALLEL / VERIFIED_COMPLETE_SUBMILESTONE` repository implementation evidence, not live browser acceptance. Both available GitHub receipt surfaces for the introducing head currently return no persisted statuses or workflow runs, so latest-head CI PASS, actual Firefox installation, ChatGPT DOM compatibility, live Native Messaging host connection and end-to-end command/result delivery remain `UNKNOWN_NEEDS_EVIDENCE`. This evidence closes the earlier gap between transport primitives and a usable Companion extension shell, but does not justify declaring A2A/Companion complete.

Sweep recheck on 2026-09-05 queried both the GitHub combined-status surface and commit-associated workflow-run surface for head `45f1373b342d12ddeb2e78f87ff7a278b13b9432`; both returned no persisted status/run receipts. Additional commit-associated workflow-run checks for image-substrate commits `80305920ce2012a445ae7f75b5b75576e12df900`, `7daf1c176d365ff65cbd9d8865534673f2407699`, resident-autorun commit `69c4a40a2e082749a7d03c54a68948305a24f3fa`, Native Messaging commit `56b767c1fd4957f7597c231a64029902d012c985`, native-contract follow-on `5a47ff781ae876058561af2a08395512184ebbc3`, and Companion 1.0 shell commit `2e2db37df4b30ad6b2ae5be499c54c8da34e5885` likewise returned no runs/status receipts. Therefore absence of a receipt remains an evidence gap, not a failure result, and no status promotion or demotion is justified.

The consolidation rule is canonical: repeated compatible success can nominate a capability candidate; matching failure blocks the candidate; no production/reflex promotion is automatic. Production promotion still requires regression evidence and existing authority/governance gates.

The constitutional authority envelope is also canonical here: `tool access != authority`, `suggestion != permission`, and human review continues to govern consequential promotion/action. Sparse capability activation, typed routing, A2A compatibility, local execution, Penpot access, Cloudflare access or future connectors may prove capability inside an already-authorized scope; none of them silently expand Doré's permission boundary.

Provider diagnostics now follow a minimum-necessary metadata rule: command lines, private filesystem paths, model paths, tokens and unknown provider fields are not retained in Doré evidence/CI logs. Preserve this as a regression invariant.

### Open acceptance evidence

Do not promote this workstream beyond foundation/submilestone status until evidence exists for:

- non-visual tasks keeping visual skill bodies/provider schemas dormant;
- bounded active-capability count and ordinary-run cost as registry size grows;
- real Image + Design flow over one typed task state without conversational handoff;
- one real purpose-built Westside asset (prefer Doré-derived light texture or Bethlehem-star grammar rather than an original Doré artwork) completing generation → real resident/provider render → fetched durable bytes + checksum/provenance → real vision observations → critic/correction if needed → accepted artifact → typed Design application with persisted identity/provenance and before/after acceptance evidence;
- latest-head capability-runtime CI PASS including the local A2A bridge, Companion Native contract, Companion 1.0 installable shell, Image iteration/handoff/resident-pipeline and resident-autorun coverage;
- live Mac Companion→Firefox Native Messaging→native host→mature adapter→Design dispatch with request/idempotency identity preserved;
- live Companion 1.0 ChatGPT `/dore` capture and result/status update without blocking or corrupting normal ChatGPT send behavior;
- keep `localhost:4312` only as compatibility/debug fallback until that live-native proof passes, then reconsider retirement;
- negative/unauthorized mutation behavior at the authority boundary;
- a repeated real workflow compiling downward to fewer deliberative/model calls;
- materially different-domain transfer;
- persisted telemetry and regression evidence across the runtime acceptance gates.

### Relation to EVOLUTION

This runtime gives `EVOLUTION` a concrete embodiment substrate, but does not prove broad self-equipping autonomy. `AUTONOMOUS_CAPABILITY_RECOVERY_01` remains the bounded recovery proof; sparse routing/runtime implementation is infrastructure that may support future transfer evidence.

### Relation to A2A / coordination

The current Design/control-plane direction supersedes the idea of adding another independent local control daemon for the same mature path. Legacy A2A compatibility remains valid, but typed capability routing should converge through the established adapter/runtime seam. Firefox Native Messaging now supersedes resident HTTP as the preferred Companion production carrier while leaving `4312` in place as bounded compatibility/debug fallback pending live Mac acceptance. Companion 1.0 now supplies the concrete browser shell that consumes that transport direction, but live installation/DOM/Native Messaging acceptance remains open. Typed/native envelopes improve protocol and carrier discipline; they do not by themselves prove authenticated mutation authority, so existing authority-hardening debt remains open.

### Relation to VISUAL work

Purpose-built Doré visual assets and future Doré Image generation should use the shared `visual` faculty/capability path rather than creating a second visual agent identity. Original Doré works remain curated content; purpose-built Doré-derived website assets remain a separate visual-grammar production problem.

For Doré Image quality work, one-shot generation as the default final-production model is superseded by the bounded correction-loop direction where visual acceptance matters. Provider-returned image references should likewise not remain ephemeral when an asset enters Doré's production/evaluation loop: the governing path is durable bytes + checksum/provenance + real review. Resident autorun now provides the bounded zero-terminal seam that can consume a queued visual job once local renderer configuration is present. Where Image hands an accepted asset to Design, free-form conversational transfer is likewise superseded by the typed image-patch contract. These are architectural directions, not claims that the real visual-production loop is already complete.

### Relation to P01

No change. P01 remains `BLOCKED / ENVIRONMENT_BLOCKED` on the approved production audio-acquisition/transcription path. This addendum must not be used to alter or replace that critical path.
