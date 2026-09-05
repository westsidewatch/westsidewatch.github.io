from __future__ import annotations

from dataclasses import dataclass, field
from hashlib import sha256
from json import dumps
from typing import Any, Mapping


def _stable_hash(value: Any) -> str:
    raw = dumps(value, sort_keys=True, ensure_ascii=False, separators=(",", ":"), default=str)
    return sha256(raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class CapabilityManifest:
    id: str
    faculty: str
    description: str
    triggers: tuple[str, ...] = ()
    inputs: tuple[str, ...] = ()
    outputs: tuple[str, ...] = ()
    requires: tuple[str, ...] = ()
    verification: tuple[str, ...] = ()
    cost_class: str = "local_free"
    latency_class: str = "fast"
    authority: str = "A1"
    instruction_ref: str | None = None
    provider_refs: tuple[str, ...] = ()

    @property
    def searchable_text(self) -> str:
        return " ".join((self.id, self.faculty, self.description, *self.triggers)).casefold()


@dataclass(frozen=True)
class ArtifactRef:
    id: str
    schema: str
    payload: Mapping[str, Any]
    provenance: tuple[str, ...] = ()
    content_hash: str = ""

    def __post_init__(self) -> None:
        if not self.content_hash:
            object.__setattr__(self, "content_hash", _stable_hash({
                "schema": self.schema,
                "payload": dict(self.payload),
                "provenance": self.provenance,
            }))


@dataclass(frozen=True)
class RouteDecision:
    intent: str
    capability_ids: tuple[str, ...]
    level: str
    confidence: float
    reason: str


@dataclass
class TaskState:
    task_id: str
    artifacts: dict[str, ArtifactRef] = field(default_factory=dict)
    active_capabilities: list[str] = field(default_factory=list)
    route_history: list[RouteDecision] = field(default_factory=list)
    telemetry: dict[str, Any] = field(default_factory=lambda: {
        "capability_activations": 0,
        "provider_activations": 0,
        "lazy_loads": 0,
    })

    def add_artifact(self, artifact: ArtifactRef) -> None:
        self.artifacts[artifact.id] = artifact

    def activate(self, capability_id: str) -> None:
        if capability_id not in self.active_capabilities:
            self.active_capabilities.append(capability_id)
            self.telemetry["capability_activations"] += 1

    def record_route(self, decision: RouteDecision) -> None:
        self.route_history.append(decision)
