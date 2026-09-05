from __future__ import annotations

import json
from pathlib import Path

from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.model import ArtifactRef, TaskState
from dore_core.capabilities.registry import default_registry
from dore_core.capabilities.runtime import LazyCapabilityRuntime
from dore_core.capabilities.synthetic_visual import synthetic_visual_handlers


def main() -> int:
    root = Path(__file__).resolve().parents[1]
    registry = default_registry()
    provider_calls: list[str] = []

    def provider_loader(ref: str):
        provider_calls.append(ref)
        return {"provider": ref, "mode": "test-double"}

    runtime = LazyCapabilityRuntime(registry, root=root, provider_loader=provider_loader)
    executor = CapabilityExecutor(registry, runtime, synthetic_visual_handlers())
    state = TaskState("visual-pipeline-probe")
    state.add_artifact(ArtifactRef("request", "request", {"need": "Matthew 3 hero"}, ("probe",)))
    sequence = (
        "visual.direct",
        "visual.grammar",
        "image.generate",
        "image.critic",
        "design.compose",
        "design.verify",
    )
    results = executor.execute_sequence(sequence, state)
    schemas = [artifact.schema for artifact in state.artifacts.values()]
    ok = len(results) == len(sequence) and all(result.ok for result in results)
    report = {
        "status": "PASS" if ok else "FAIL",
        "mode": "synthetic-zero-cost-contract-probe",
        "claim_boundary": "This proves typed routing/execution/state flow only; it does not claim a real image was rendered or visually approved.",
        "sequence": sequence,
        "results": [
            {"capability_id": r.capability_id, "ok": r.ok, "error": r.error, "elapsed_ms": r.elapsed_ms}
            for r in results
        ],
        "artifact_schemas": schemas,
        "active_capabilities": state.active_capabilities,
        "provider_calls": provider_calls,
        "telemetry": state.telemetry,
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True, default=str))
    return 0 if ok else 1


if __name__ == "__main__":
    raise SystemExit(main())
