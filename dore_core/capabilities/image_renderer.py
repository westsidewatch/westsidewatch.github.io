from __future__ import annotations

import hashlib
import json
import time
from dataclasses import dataclass
from typing import Any
from urllib.parse import urlencode
from urllib.request import Request, urlopen

from .providers import ProviderDescriptor, probe_json_http_provider


@dataclass(frozen=True)
class RenderRequest:
    workflow: dict[str, Any]
    seed: int | None = None
    model: str | None = None
    workflow_id: str | None = None


@dataclass(frozen=True)
class RenderArtifact:
    prompt_id: str
    images: tuple[dict[str, str], ...]
    provenance: dict[str, Any]


class ComfyUIRenderer:
    """Minimal stdlib ComfyUI adapter. It never starts or installs a provider."""

    def __init__(self, descriptor: ProviderDescriptor, *, timeout: float = 10.0) -> None:
        if descriptor.cost_class != "local_free":
            raise ValueError("Doré resident renderer must be local_free")
        self.descriptor = descriptor
        self.timeout = timeout

    def health(self):
        return probe_json_http_provider(self.descriptor, timeout=min(self.timeout, 2.0))

    def _json(self, path: str, *, method: str = "GET", body: dict[str, Any] | None = None) -> dict[str, Any]:
        url = self.descriptor.endpoint.rstrip("/") + "/" + path.lstrip("/")
        data = json.dumps(body).encode("utf-8") if body is not None else None
        req = Request(url, data=data, method=method, headers={"Accept": "application/json", "Content-Type": "application/json", "User-Agent": "Dore/1"})
        with urlopen(req, timeout=self.timeout) as response:  # nosec B310: configured resident provider
            raw = response.read(2 * 1024 * 1024)
        value = json.loads(raw.decode("utf-8")) if raw else {}
        if not isinstance(value, dict):
            raise RuntimeError("renderer returned non-object JSON")
        return value

    def submit(self, request: RenderRequest) -> str:
        if not self.health().ok:
            raise RuntimeError("resident image renderer is not reachable")
        response = self._json("/prompt", method="POST", body={"prompt": request.workflow})
        prompt_id = response.get("prompt_id")
        if not isinstance(prompt_id, str) or not prompt_id:
            raise RuntimeError("renderer did not return prompt_id")
        return prompt_id

    def await_result(self, prompt_id: str, *, poll_seconds: float = 0.5, max_wait_seconds: float = 180.0) -> dict[str, Any]:
        deadline = time.monotonic() + max_wait_seconds
        while time.monotonic() < deadline:
            history = self._json(f"/history/{prompt_id}")
            item = history.get(prompt_id)
            if isinstance(item, dict) and item.get("outputs"):
                return item
            time.sleep(poll_seconds)
        raise TimeoutError(f"renderer job {prompt_id} did not finish")

    @staticmethod
    def image_refs(history_item: dict[str, Any]) -> tuple[dict[str, str], ...]:
        refs: list[dict[str, str]] = []
        outputs = history_item.get("outputs", {})
        if isinstance(outputs, dict):
            for output in outputs.values():
                if not isinstance(output, dict):
                    continue
                for image in output.get("images", []):
                    if isinstance(image, dict) and isinstance(image.get("filename"), str):
                        refs.append({k: str(image.get(k, "")) for k in ("filename", "subfolder", "type")})
        return tuple(refs)

    def render(self, request: RenderRequest) -> RenderArtifact:
        prompt_id = self.submit(request)
        history = self.await_result(prompt_id)
        refs = self.image_refs(history)
        if not refs:
            raise RuntimeError("renderer completed without image output")
        workflow_hash = hashlib.sha256(json.dumps(request.workflow, sort_keys=True, separators=(",", ":")).encode()).hexdigest()
        provenance = {
            "engine": "comfyui",
            "provider": self.descriptor.id,
            "cost_class": self.descriptor.cost_class,
            "model": request.model,
            "workflow_id": request.workflow_id,
            "workflow_sha256": workflow_hash,
            "seed": request.seed,
            "prompt_id": prompt_id,
        }
        return RenderArtifact(prompt_id, refs, provenance)

    def image_url(self, ref: dict[str, str]) -> str:
        query = urlencode({k: ref.get(k, "") for k in ("filename", "subfolder", "type")})
        return self.descriptor.endpoint.rstrip("/") + "/view?" + query
