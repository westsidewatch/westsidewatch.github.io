from __future__ import annotations

import json
from dataclasses import dataclass
from typing import Callable
from urllib.request import Request, urlopen


@dataclass(frozen=True)
class ProviderDescriptor:
    id: str
    transport: str
    endpoint: str
    cost_class: str = "local_free"
    authority: str = "A1"


@dataclass(frozen=True)
class ProviderHealth:
    provider_id: str
    ok: bool
    detail: str
    metadata: dict[str, object]


class ProviderRegistry:
    def __init__(self) -> None:
        self._descriptors: dict[str, ProviderDescriptor] = {}
        self._factories: dict[str, Callable[[ProviderDescriptor], object]] = {}

    def register(self, descriptor: ProviderDescriptor, factory: Callable[[ProviderDescriptor], object]) -> None:
        if descriptor.id in self._descriptors:
            raise ValueError(f"duplicate provider id: {descriptor.id}")
        self._descriptors[descriptor.id] = descriptor
        self._factories[descriptor.id] = factory

    def descriptor(self, provider_id: str) -> ProviderDescriptor:
        return self._descriptors[provider_id]

    def load(self, provider_id: str) -> object:
        return self._factories[provider_id](self._descriptors[provider_id])


def probe_json_http_provider(descriptor: ProviderDescriptor, *, path: str = "/system_stats", timeout: float = 1.5) -> ProviderHealth:
    """Probe a local JSON provider without importing its SDK or starting it."""
    url = descriptor.endpoint.rstrip("/") + "/" + path.lstrip("/")
    try:
        req = Request(url, headers={"Accept": "application/json", "User-Agent": "Dore/1"})
        with urlopen(req, timeout=timeout) as response:  # nosec B310: endpoint is explicit local/provider config
            raw = response.read(262144)
        payload = json.loads(raw.decode("utf-8")) if raw else {}
        if not isinstance(payload, dict):
            payload = {"response": payload}
        return ProviderHealth(descriptor.id, True, "reachable", payload)
    except Exception as exc:
        return ProviderHealth(descriptor.id, False, f"{type(exc).__name__}: {exc}", {})


def default_local_image_provider() -> ProviderDescriptor:
    return ProviderDescriptor(
        id="local-image-renderer",
        transport="http-json",
        endpoint="http://127.0.0.1:8188",
        cost_class="local_free",
    )
