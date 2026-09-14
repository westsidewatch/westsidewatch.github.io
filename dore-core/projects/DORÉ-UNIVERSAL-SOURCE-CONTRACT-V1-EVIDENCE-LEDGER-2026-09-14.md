# DORÉ UNIVERSAL SOURCE CONTRACT V1 — EVIDENCE LEDGER

Date: 2026-09-14
Status: VERIFIED_COMPLETE / BOUNDED CONTRACT FREEZE
Parent sweep: `DORÉ-MEMORY-CONSOLIDATION-SWEEP-01.md`
P01 impact: NONE

## Original objective

Converge source access behind one provider-neutral execution contract so product surfaces do not independently reinterpret probe results, runtime requirements, access modes, rights, identity, or persistence.

Canonical chain:

`source.probe → source.capability-envelope → source.dispatch → consumer-admission`

## Completion evidence

- PR #757, **Freeze Universal Source Contract v1**, is merged into `main` at merge commit `82e27a3ea3565513543376ebe36b58196e46105a`.
- The merged PR formally registers `source.dispatch` in `dore-core/runtime/capability-registry.v1.json` and binds it to `dore-core/runtime/source-capability-contract.v1.json`.
- `source-capability-contract.v1.json` records `status: frozen-v1`, the four-stage canonical pipeline, stable dispatch statuses/error reasons, provider-neutral boundaries, request-scoped/no-persistence behavior, and explicit separation from canonical identity, rights, and editorial authority.
- `local/dore-local/source_contract_acceptance.py` verifies the frozen contract, dispatcher behavior, capability-registry membership, and product-consumer conformance.
- Source CI now includes the frozen contract and conformance acceptance in its watched/required source family.
- Cinema, Dawn, and Multiwrite are explicitly required to consume the dispatcher boundary rather than derive competing routes. PR #755 had already removed Cinema's final independent runtime/access interpretation before the freeze.

## Current classification

- Universal Source Contract v1 freeze: `VERIFIED_COMPLETE / CONTRACT MILESTONE`.
- `source.probe`, `source.capability-envelope`, and `source.dispatch`: reusable `CORE/CONTINUOUS` source-intelligence capabilities after the freeze.
- Consumer-specific independent access-routing logic: `SUPERSEDED` where it competes with `source.dispatch`.
- Rights/editorial/canonical-identity admission: remains outside dispatcher authority and must not be inferred from technical access capability.

## Current quality judgment

Strong for the declared contract milestone. The work is no longer merely a probe prototype: the dispatcher is formally registered, the schema/boundary is frozen, consumer conformance is machine-checked, and at least Cinema/Dawn/Multiwrite have explicit consumption semantics.

The evidence should not be inflated into a claim that every source/provider/media type is successfully retrievable in production. Contract convergence and provider-neutral routing are complete at v1; source coverage, runtime availability, rights decisions, and downstream consumer quality remain separate evidence questions.

## Durable learning / retained capability

1. Product surfaces should consume one shared access-routing decision instead of reconstructing source logic locally.
2. Technical capability must remain distinct from source authority, canonical identity, rights, editorial authority, and persistence authority.
3. Browser/runtime fallback is an execution route, not a provider-specific product exception.
4. Contract freezes should include machine-readable schema, stable failure reasons, capability registration, and cross-consumer conformance tests.
5. Provider-specific adapters remain last-mile implementation details and must not become competing architectural control planes.

## Weaknesses / debt

- No successful workflow-run record was returned for the merge commit by the bounded GitHub workflow-status query in this sweep pass; therefore this ledger relies on the merged code/contract/acceptance harness and PR evidence rather than claiming a persisted post-merge CI run for `82e27a3e...`.
- The frozen v1 contract proves routing semantics, not universal extraction success or production runtime availability for every provider.
- Consumer conformance explicitly covers Cinema, Dawn and Multiwrite in the freeze; ONE/Design/Search are registered consumers but still need real downstream episodes before cross-product behavioral maturity can be claimed.
- The dispatcher intentionally cannot resolve rights/editorial/publishing decisions; downstream products must preserve those independent gates.

## Revisit trigger

Reopen the v1 contract only if one of the following becomes materially true:

- a real source class cannot be represented without breaking frozen semantics;
- multiple consumers again begin inferring access independently;
- stable error reasons become insufficient for operational diagnosis;
- a new execution environment requires a contract-level change rather than an adapter;
- production evidence shows that the current authority separation is being violated.

Ordinary addition of providers, probe strategies, or consumer adapters should not reopen the contract.

## Disposition

Keep the v1 contract freeze closed as a bounded completed milestone. Continue source intelligence as `CORE/CONTINUOUS`, enforce the single-dispatcher boundary as regression protection, and gather downstream real-use evidence without turning the dispatcher into rights/editorial/identity authority.

No P01 subtitle runtime state, ordering, deployment, credential, binding, blocker, or resume condition was modified by this reconciliation.
