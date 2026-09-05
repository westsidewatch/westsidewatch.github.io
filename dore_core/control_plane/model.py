from __future__ import annotations

from dataclasses import dataclass, field
from typing import Any, Mapping


@dataclass(frozen=True)
class ConsumerDescriptor:
    id: str
    capability_ids: tuple[str, ...]
    authority: str = "A1"
    version: str = "1"


@dataclass(frozen=True)
class ControlRequest:
    request_id: str
    conversation_id: str
    session_id: str
    consumer_id: str
    capability_id: str
    payload: Mapping[str, Any] = field(default_factory=dict)


@dataclass(frozen=True)
class ControlResult:
    request_id: str
    conversation_id: str
    session_id: str
    consumer_id: str
    capability_id: str
    status: str
    result: Mapping[str, Any] = field(default_factory=dict)
    error: str | None = None
    replayed: bool = False
