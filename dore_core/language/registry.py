"""Language adapter registry for Doré."""
from __future__ import annotations
from typing import Any

class LanguageRegistry:
    def __init__(self) -> None:
        self._adapters: dict[str, Any] = {}

    def register(self, adapter: Any) -> None:
        adapter_id = getattr(adapter, "adapter_id", None)
        if not adapter_id:
            raise ValueError("adapter must declare adapter_id")
        if adapter_id in self._adapters:
            raise ValueError(f"adapter already registered: {adapter_id}")
        self._adapters[adapter_id] = adapter

    def get(self, adapter_id: str) -> Any:
        try:
            return self._adapters[adapter_id]
        except KeyError as exc:
            raise KeyError(f"unknown language adapter: {adapter_id}") from exc

    def capabilities(self) -> dict[str, object]:
        return {key: adapter.capabilities for key, adapter in sorted(self._adapters.items())}

    def ids(self) -> tuple[str, ...]:
        return tuple(sorted(self._adapters))
