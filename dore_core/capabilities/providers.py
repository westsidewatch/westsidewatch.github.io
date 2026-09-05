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


_SAFE_SYSTEM_KEYS = {
    "os", "python_version", "comfyui_version", "pytorch_version",
    "embedded_python", "ram_total", "ram_free", "deploy_environment",
}
_SAFE_DEVICE_KEYS = {
    "name", "type", "index", "vram_total", "vram_free",
    "torch_vram_total", "torch_vram_free",
}


def sanitize_system_stats(payload: dict[str, object]) -> dict[str, object]:
    """Return only diagnostics Doré needs; never retain command lines or paths."""
    safe: dict[str, object] = {}
    system = payload.get("system")
    if isinstance(system, dict):
        safe["system"] = {key: system[key] for key in _SAFE_SYSTEM_KEYS if key in system}
    devices = payload.get("devices")
    if isinstance(devices, list):
        safe["devices"] = [
            {key: device[key] for key in _SAFE_DEVICE_KEYS if key in device}
            for device in devices if isinstance(device, dict)
        ]
    return safe


def probe_json_http_provider(descriptor: ProviderDescriptor, *, path: str = "/system_stats", timeout: float = 1.5) -> ProviderHealth:
    """Probe a local JSON provider without importing its SDK or starting it."""
    url = descriptor.endpoint.rstrip("/") + "/" + path.lstrip("/")
    try:
        req = Request(url, headers={"Accept": "application/json", "User-Agent": "Dore/1"})
        with urlopen(req, timeout=timeout) as response:  # nosec B310: endpoint is explicit provider config
            raw = response.read(262144)
        payload = json.loads(raw.decode("utf-8")) if raw else {}
        if not isinstance(payload, dict):
            payload = {}
        metadata = sanitize_system_stats(payload) if path.rstrip("/").endswith("system_stats") else {}
        return ProviderHealth(descriptor.id, True, "reachable", metadata)
    except Exception as exc:
        return ProviderHealth(descriptor.id, False, f"{type(exc).__name__}: {exc}", {})


def default_local_image_provider() -> ProviderDescriptor:
    return ProviderDescriptor(
        id="local-image-renderer",
        transport="http-json",
        endpoint="http://127.0.0.1:8188",
        cost_class="local_free",
    )
