# Doré Local Intelligence Fabric — Compatibility Map

Status: Phase 1 engineering contract

## Product Interface Freeze

Existing products continue to address Doré capabilities, never LongMemory, QMD, oMLX, mlx-serve, macMLX, wake, or a physical model directly.

```text
Design / Image / 多寫 / ONE / Doré Search / Main Site / A2A
                         ↓
                 Doré Capability Bus
                         ↓
          Context / Reflex / Virtual Capability
                         ↓
             replaceable local substrates
```

A substrate integration that requires product surfaces to learn a new provider/model endpoint is rejected by default.

## Existing verified seams

- `dore-core/runtime/capability-registry.v1.json`: semantic discovery; products request capability names.
- `local/dore-local/capability_bus.py`: Core-owned execution/provider boundary; `image.generate` already demonstrates provider hiding.
- `local/dore-local/native_host.py`: A2A enters Core through capability resolution.
- `dore_core/context/*`: local SQLite/FTS5 context projection with provenance and read-only packets.
- launchd Unix-domain-socket control plane: existing browser-independent activation path.
- wake activation work exists and must be preserved/verified rather than rebuilt.

## Migration rules

1. Doré sovereignty: external projects are substrates, not Doré identity or authority.
2. Product Interface Freeze: preserve capability IDs and typed artifact contracts.
3. Minimum Capability Gate: deterministic → tiny-hot → resident specialist → cold specialist → optional escalation.
4. Residency Gate: capability availability does not imply model RAM residency.
5. Free Gate: local core rejects paid/required-cloud providers.
6. Exploration Preservation Gate: LongMemory/QMD/wake/Osaurus/OpenJarvis/Semantic Router/oMLX/mlx-serve/macMLX findings remain active until explicitly superseded by evidence.
7. No duplicate core: adapters must converge on the existing Capability Bus/Context boundary.

## Substrate placement

- LongMemory: candidate Knowledge/temporal/provenance/project-context substrate below Doré authority.
- QMD: fuzzy/hybrid document retrieval below Doré Search/Context.
- mnemos/localmem patterns: citation/recovery and deterministic recall, not competing authority stores.
- wake: durable execution/recovery.
- Osaurus: Mac-native runtime/sandbox source comparison.
- Semantic Router: routing recipes/signals/evaluation patterns, not full vLLM deployment.
- oMLX/mlx-serve/macMLX: residency/inference candidates below Virtual Capability Registry.

## Compatibility acceptance

Before promoting any substrate:

- existing capability IDs remain callable;
- `image.generate` keeps its typed artifact/product contract;
- Westside Context remains read-only and provenance-preserving;
- A2A still enters through Doré Core, not a substrate;
- no product gains a direct physical-model/provider dependency;
- offline/no-commercial-key core path remains valid;
- regression tests pass before merge.
