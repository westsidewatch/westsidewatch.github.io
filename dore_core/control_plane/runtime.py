from __future__ import annotations

from dataclasses import replace
from threading import RLock
from typing import Mapping

from dore_core.capabilities.executor import CapabilityExecutor
from dore_core.capabilities.model import ArtifactRef, TaskState
from dore_core.capabilities.registry import CapabilityRegistry

from .model import ConsumerDescriptor, ControlRequest, ControlResult


DESIGN_CONSUMER = ConsumerDescriptor(
    id="design",
    capability_ids=("design.compose", "design.verify"),
    authority="A1",
    version="1",
)


class ControlPlane:
    """Small in-process A2A control plane for resident Doré consumers.

    The Companion/4312 transport supplies typed requests. This layer binds a
    conversation to a session, exposes consumer discovery, enforces consumer
    capability boundaries, and makes request_id execution idempotent.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        executor: CapabilityExecutor,
        consumers: tuple[ConsumerDescriptor, ...],
    ) -> None:
        self.registry = registry
        self.executor = executor
        self._consumers = {consumer.id: consumer for consumer in consumers}
        self._sessions: dict[str, str] = {}
        self._results: dict[str, ControlResult] = {}
        self._lock = RLock()

    def discover(self) -> tuple[ConsumerDescriptor, ...]:
        return tuple(self._consumers[key] for key in sorted(self._consumers))

    def dispatch(self, request: ControlRequest) -> ControlResult:
        with self._lock:
            cached = self._results.get(request.request_id)
            if cached is not None:
                return replace(cached, replayed=True)

            consumer = self._consumers.get(request.consumer_id)
            if consumer is None:
                return self._store_failure(request, "unknown consumer")
            if request.capability_id not in consumer.capability_ids:
                return self._store_failure(request, "capability not exposed by consumer")
            try:
                self.registry.get(request.capability_id)
            except KeyError:
                return self._store_failure(request, "capability not registered")

            bound = self._sessions.get(request.conversation_id)
            if bound is None:
                self._sessions[request.conversation_id] = request.session_id
            elif bound != request.session_id:
                return self._store_failure(request, "conversation already bound to another session")

            state = TaskState(task_id=request.request_id)
            for schema, payload in request.payload.items():
                if not isinstance(payload, Mapping):
                    return self._store_failure(request, f"input {schema} must be an object")
                state.add_artifact(ArtifactRef(
                    id=f"{request.request_id}:{schema}",
                    schema=schema,
                    payload=dict(payload),
                    provenance=("a2a", request.conversation_id, request.session_id),
                ))

            execution = self.executor.execute(request.capability_id, state)
            if not execution.ok:
                return self._store_failure(request, execution.error or "execution failed")

            result_payload = {
                artifact.schema: {
                    "id": artifact.id,
                    "payload": dict(artifact.payload),
                    "content_hash": artifact.content_hash,
                    "provenance": artifact.provenance,
                }
                for artifact in execution.output_artifacts
            }
            result = ControlResult(
                request_id=request.request_id,
                conversation_id=request.conversation_id,
                session_id=request.session_id,
                consumer_id=request.consumer_id,
                capability_id=request.capability_id,
                status="succeeded",
                result=result_payload,
            )
            self._results[request.request_id] = result
            return result

    def status(self, request_id: str) -> ControlResult | None:
        with self._lock:
            return self._results.get(request_id)

    def _store_failure(self, request: ControlRequest, error: str) -> ControlResult:
        result = ControlResult(
            request_id=request.request_id,
            conversation_id=request.conversation_id,
            session_id=request.session_id,
            consumer_id=request.consumer_id,
            capability_id=request.capability_id,
            status="failed",
            error=error,
        )
        self._results[request.request_id] = result
        return result


def build_design_control_plane(
    registry: CapabilityRegistry,
    executor: CapabilityExecutor,
) -> ControlPlane:
    return ControlPlane(registry, executor, (DESIGN_CONSUMER,))
