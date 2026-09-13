# DORÉ SOURCE PROBE + A2A RELIABILITY EVIDENCE LEDGER

Date: 2026-09-13
Status: BOUNDED RECONCILIATION
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
Canonical register: `DORÉ-MASTER-WORK-REGISTER.md`
P01 impact: NONE

## Evidence reviewed

### Universal Source Probe v0

- merged PR #725 / merge commit `a5ff067dd708ae340dbbd1107a082586c1edbacc`;
- `local/dore-local/source_probe_capability.py`;
- `local/dore-local/source_probe_acceptance.py`;
- `.github/workflows/dore-universal-source-probe-v0.yml`;
- `dore-core/runtime/capability-registry.v1.json` registration for `source.probe`.

### A2A Reliability Atlas v1 foundation

- merged PR #727 / merge commit `3aa5c884922cba2e76994010419e6e71afd0424d`;
- superseded PR #723;
- `docs/a2a-reliability-atlas-v1.md`;
- `docs/a2a-reliability-1b-existing-primitives.md`;
- `.github/workflows/a2a-reliability-authority.yml`;
- canonical capability authority, public `dore.call` normalization, durable execution, runtime generation, lease recovery, failure taxonomy / poison-isolation acceptance implementations;
- canonical registry/binding/bus/native-host/Unix-RPC integration touched by the merged foundation.

## Findings

### 1. Universal Source Probe v0 is a real reusable capability component

The merged implementation is not a provider-specific scraper. Its contract is standard-first, provider-neutral and request-scoped: it reads source policy and standard metadata surfaces, extracts media/poster/embed/caption/manifest capabilities, preserves the external source as authority, does not make the probe authority, and does not create a persistent Reflex/source substrate.

The acceptance specification proves the intended local contract against a provider-neutral fixture, including Open Graph / JSON-LD / oEmbed / HTML video-track discovery, HLS manifest recognition, non-rehost rights posture and the explicit Wikisource ban. The live GOOD TV path is deliberately allowed to return a bounded `partial` result requiring a runtime-browser probe when static acquisition is blocked, rather than fabricating a static success.

Classification:

- `source.probe` implementation: `VERIFIED_COMPLETE / COMPONENT` for the merged standard-first/provider-neutral contract;
- cross-site production coverage: `CORE/CONTINUOUS / UNKNOWN_NEEDS_EVIDENCE` beyond the bounded acceptance and one live GOOD TV boundary;
- provider-specific adapters: remain fallback-last, not a competing authority.

Durable principle: **unknown source ≠ unknown architecture**. Doré should first project an unfamiliar resource into capabilities/provenance/rights with a generic source-intelligence layer, escalate to runtime/browser observation when static evidence is insufficient, and use provider adapters only when a real source-specific gap remains.

### 2. A2A Reliability Atlas v1 changes the architecture interpretation materially

The merged foundation confirms the archaeology finding that Doré already had strong reliability primitives but distributed authority across multiple paths. The key defect was not absence of reliability logic; it was the absence of one compulsory public route through canonical capability identity, normalized request shape and durable execution truth.

PR #727 consolidates the first major reliability slices around:

- one canonical capability descriptor authority;
- public `dore.call` normalization into the typed internal envelope;
- compulsory durable task execution rather than route-local completion truth;
- runtime/capability generation identity;
- lease heartbeat + crash recovery semantics;
- explicit failure vocabulary and poison-message quarantine/isolation;
- preservation of the existing substrate bus contract.

The merge itself is strong implementation evidence. The workflow definition encodes the intended acceptance gate, but this bounded sweep did not independently recover a persisted workflow-run artifact/status set for the PR head. Therefore the engineering foundation is real and merged, while any claim that every acceptance slice was independently revalidated by Sweep 01 remains evidence-bounded.

Classification:

- A2A Reliability Atlas architecture + merged 1C foundation through poison isolation: `ACTIVE_PARALLEL / IMPLEMENTED_FOUNDATION`;
- the individual merged reliability slices: bounded `VERIFIED_COMPLETE / COMPONENT` where their deterministic acceptance programs are part of the merged path, but not a whole-system A2A completion claim;
- Universal A2A reliability as a system: remains `ACTIVE_PARALLEL` until compulsory routing, real long-task renewal/recovery, durable result delivery and transport-independent end-to-end execution are proven on materially real workloads.

### 3. Existing reliability primitives should be promoted, not rewritten

The 1B inventory correctly preserves mature pieces: durable delivery identity/dedupe/quarantine, durable execution records and leases, outbox semantics, information-gain retry, stall supervision, optional-module fault isolation, and the canonical JSON capability registry. The work should consolidate these into one path rather than replace them with another reliability stack.

### 4. Several older authority patterns are now superseded as current design truth

The following should no longer be treated as preferred architecture even where compatibility code remains:

- direct-module registration as a normal capability authority;
- Production Bus hard-coded capability identity as an independent semantic source;
- Python visual registry as a second capability-identity authority;
- route-specific handler/RPC/workflow response as completion truth.

These are `SUPERSEDED / COMPATIBILITY-ONLY` directions, subject to staged removal only after the canonical path proves equivalent or stronger behavior.

### 5. No P01 change and no new human/environment blocker

This batch did not change P01 subtitle code, job state, production bindings, credentials, source order, deployment, blocker condition or resume policy. The already-known production audio-acquisition/transcription environment dependency remains unchanged.

## Revisit / missing-evidence implications

1. Revisit the Source Probe only when real heterogeneous-source traffic exposes a capability/provenance/rights class that cannot be represented by v0 without source-specific leakage.
2. For A2A, require one persisted end-to-end real workload proof that enters through ordinary public `dore.call`, normalizes once, resolves canonical registry identity, executes durably with lease renewal, survives one induced worker/process failure, records artifact + verification before PASS, and publishes the caller-visible result from durable outbox state.
3. Persist workflow/run evidence for the merged A2A reliability acceptance gate so merged deterministic acceptance code is accompanied by independently inspectable execution evidence.
4. Keep the recovery/bootstrap escape hatch tiny; do not let exception routes regrow into a second normal control plane.

## Current disposition

- Universal Source Probe v0: retain as shared source-intelligence capability; enrich from demonstrated source classes only.
- A2A Reliability Atlas v1: retain and continue consolidation; do not reopen solved primitives for aesthetic rewrite.
- superseded duplicate authority routes: compatibility-only until safely removable.
- Sweep 01: remains `ACTIVE_PARALLEL`.
