# ADR-0003 — Universal Source Contract Freeze

Status: Accepted

The source path is frozen as:

`source.probe → source.capability-envelope → source.dispatch → consumer admission`

`source.dispatch` is the only access-routing authority. Product surfaces may consume its decision but may not reinterpret probe needs, envelope access modes, or runtimeBoundary to derive a competing route.

The dispatcher remains a pure in-process primitive. It is not source authority, canonical identity authority, rights authority, or editorial authority, and it persists no source media or admission state.

Cinema consumes `dispatch.requiresRuntime`; Dawn consumes `dispatch.materializationReady`; Multiwrite consumes dispatch first and then applies its independent rights/editorial publication admission.

The v1 error reasons and schema names are contract-frozen and protected by `source_contract_acceptance.py` in source CI.
