from __future__ import annotations

from dataclasses import dataclass
from time import perf_counter
from typing import Callable, Mapping, Any

from .model import ArtifactRef, TaskState
from .registry import CapabilityRegistry
from .runtime import LazyCapabilityRuntime, LoadedCapability
from .visual import require_visual_inputs, visual_artifact


CapabilityHandler = Callable[[LoadedCapability, Mapping[str, ArtifactRef], TaskState], Mapping[str, Any]]


@dataclass(frozen=True)
class ExecutionResult:
    capability_id: str
    ok: bool
    output_artifacts: tuple[ArtifactRef, ...]
    error: str | None = None
    elapsed_ms: float = 0.0


class CapabilityExecutor:
    """Execute selected Doré capabilities against one shared typed TaskState.

    Handlers receive only the typed artifacts declared by the capability
    manifest. They do not receive another capability's chat history or hidden
    reasoning. Outputs are written back as typed artifacts with provenance.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        runtime: LazyCapabilityRuntime,
        handlers: Mapping[str, CapabilityHandler] | None = None,
    ) -> None:
        self.registry = registry
        self.runtime = runtime
        self.handlers: dict[str, CapabilityHandler] = dict(handlers or {})

    def register_handler(self, capability_id: str, handler: CapabilityHandler) -> None:
        self.registry.get(capability_id)
        self.handlers[capability_id] = handler

    def execute(self, capability_id: str, state: TaskState) -> ExecutionResult:
        started = perf_counter()
        manifest = self.registry.get(capability_id)
        handler = self.handlers.get(capability_id)
        if handler is None:
            return self._failure(capability_id, state, started, "no handler registered")

        try:
            inputs = require_visual_inputs(state, manifest.inputs) if manifest.faculty == "visual" else {}
            loaded = self.runtime.activate(capability_id, state)
            payloads = handler(loaded, inputs, state)
            if set(payloads) != set(manifest.outputs):
                expected = ",".join(manifest.outputs) or "<none>"
                actual = ",".join(sorted(payloads)) or "<none>"
                raise ValueError(f"output schema mismatch: expected {expected}; got {actual}")

            input_hashes = tuple(artifact.content_hash for artifact in inputs.values())
            outputs: list[ArtifactRef] = []
            for schema in manifest.outputs:
                payload = payloads[schema]
                if not isinstance(payload, Mapping):
                    raise TypeError(f"handler output for {schema} must be a mapping")
                artifact = visual_artifact(
                    state,
                    schema,
                    payload,
                    provenance=(capability_id, *input_hashes),
                )
                outputs.append(artifact)

            elapsed_ms = (perf_counter() - started) * 1000
            state.telemetry["capability_executions"] = state.telemetry.get("capability_executions", 0) + 1
            state.telemetry["execution_latency_ms"] = state.telemetry.get("execution_latency_ms", 0.0) + elapsed_ms
            return ExecutionResult(capability_id, True, tuple(outputs), elapsed_ms=elapsed_ms)
        except Exception as exc:
            return self._failure(capability_id, state, started, f"{type(exc).__name__}: {exc}")

    def execute_sequence(self, capability_ids: tuple[str, ...], state: TaskState) -> tuple[ExecutionResult, ...]:
        results: list[ExecutionResult] = []
        for capability_id in capability_ids:
            result = self.execute(capability_id, state)
            results.append(result)
            if not result.ok:
                break
        return tuple(results)

    @staticmethod
    def _failure(capability_id: str, state: TaskState, started: float, error: str) -> ExecutionResult:
        elapsed_ms = (perf_counter() - started) * 1000
        state.telemetry["capability_failures"] = state.telemetry.get("capability_failures", 0) + 1
        state.telemetry["last_failure"] = {"capability_id": capability_id, "error": error}
        return ExecutionResult(capability_id, False, (), error=error, elapsed_ms=elapsed_ms)
