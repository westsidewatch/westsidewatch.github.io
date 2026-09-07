"""Minimal local capability discovery and invocation for Doré Runtime.

The registry is declarative. This module adds only the missing read-only dispatch
step: discover a named capability, resolve its Python entrypoint, and invoke it.
It does not grant write access or introduce a provider/runtime framework.
"""
from __future__ import annotations

import importlib
import json
from pathlib import Path
from typing import Any, Callable

ROOT = Path(__file__).resolve().parents[2]
REGISTRY = ROOT / "dore-core/runtime/capability-registry.v1.json"


class CapabilityError(RuntimeError):
    """Raised when a capability cannot be safely discovered or invoked."""


def _load_registry(path: Path = REGISTRY) -> dict[str, Any]:
    raw = json.loads(path.read_text(encoding="utf-8"))
    if not isinstance(raw, dict) or raw.get("schema") != "dore.capability-registry.v1":
        raise CapabilityError("unsupported capability registry")
    return raw


def discover_capability(capability_id: str, path: Path = REGISTRY) -> dict[str, Any]:
    """Return the declarative capability record by semantic id."""
    for capability in _load_registry(path).get("capabilities", []):
        if capability.get("id") == capability_id:
            return dict(capability)
    raise CapabilityError(f"unknown capability: {capability_id}")


def resolve_entrypoint(capability: dict[str, Any]) -> Callable[..., Any]:
    """Resolve a Python ``module:function`` entrypoint from a capability record."""
    entrypoint = capability.get("entrypoint")
    if capability.get("execution") != "adapter" or not isinstance(entrypoint, str) or ":" not in entrypoint:
        raise CapabilityError(f"capability has no supported adapter entrypoint: {capability.get('id')}")
    module_name, function_name = entrypoint.split(":", 1)
    try:
        module = importlib.import_module(module_name)
        function = getattr(module, function_name)
    except (ImportError, AttributeError) as exc:
        raise CapabilityError(f"cannot resolve capability entrypoint: {entrypoint}") from exc
    if not callable(function):
        raise CapabilityError(f"capability entrypoint is not callable: {entrypoint}")
    return function


def invoke_capability(
    capability_id: str,
    query: str,
    *,
    db: Any,
    limit: int = 4,
    registry_path: Path = REGISTRY,
) -> list[dict[str, Any]]:
    """Discover and invoke one local read-only capability.

    The dispatcher deliberately accepts the existing SQLite connection supplied by
    the caller; it creates no network client, provider, or mutation path.
    """
    capability = discover_capability(capability_id, registry_path)
    if capability.get("network") is True:
        raise CapabilityError(f"network capability is not permitted by local dispatcher: {capability_id}")
    if capability.get("write_access") is not False:
        raise CapabilityError(f"capability is not explicitly read-only: {capability_id}")
    function = resolve_entrypoint(capability)
    return function(query, db, limit=limit)
