from __future__ import annotations

from dataclasses import dataclass
from pathlib import Path
from time import perf_counter
from typing import Callable

from .model import CapabilityManifest, TaskState
from .registry import CapabilityRegistry


@dataclass(frozen=True)
class LoadedCapability:
    manifest: CapabilityManifest
    instruction: str | None = None
    providers: tuple[object, ...] = ()


class LazyCapabilityRuntime:
    """Load capability bodies only after routing has selected them.

    The registry remains cheap metadata. Instructions and providers are resolved
    at activation time, cached per runtime, and never pulled for unrelated work.
    """

    def __init__(
        self,
        registry: CapabilityRegistry,
        *,
        root: str | Path = ".",
        provider_loader: Callable[[str], object] | None = None,
    ) -> None:
        self.registry = registry
        self.root = Path(root)
        self.provider_loader = provider_loader
        self._instruction_cache: dict[str, str] = {}
        self._provider_cache: dict[str, object] = {}

    def activate(self, capability_id: str, state: TaskState) -> LoadedCapability:
        started = perf_counter()
        manifest = self.registry.get(capability_id)
        instruction = self._load_instruction(manifest, state)
        providers = tuple(self._load_provider(ref, state) for ref in manifest.provider_refs)
        state.activate(capability_id)
        state.telemetry["activation_latency_ms"] = state.telemetry.get("activation_latency_ms", 0.0) + (perf_counter() - started) * 1000
        state.telemetry["instruction_bytes_loaded"] = state.telemetry.get("instruction_bytes_loaded", 0) + (
            len(instruction.encode("utf-8")) if instruction is not None else 0
        )
        return LoadedCapability(manifest=manifest, instruction=instruction, providers=providers)

    def activate_route(self, capability_ids: tuple[str, ...], state: TaskState) -> tuple[LoadedCapability, ...]:
        return tuple(self.activate(cid, state) for cid in capability_ids)

    def _load_instruction(self, manifest: CapabilityManifest, state: TaskState) -> str | None:
        ref = manifest.instruction_ref
        if ref is None:
            return None
        if ref in self._instruction_cache:
            state.telemetry["instruction_cache_hits"] = state.telemetry.get("instruction_cache_hits", 0) + 1
            return self._instruction_cache[ref]
        path = (self.root / ref).resolve()
        root = self.root.resolve()
        if root not in path.parents and path != root:
            raise ValueError(f"instruction ref escapes runtime root: {ref}")
        text = path.read_text(encoding="utf-8")
        self._instruction_cache[ref] = text
        state.telemetry["lazy_loads"] += 1
        return text

    def _load_provider(self, ref: str, state: TaskState) -> object:
        if ref in self._provider_cache:
            state.telemetry["provider_cache_hits"] = state.telemetry.get("provider_cache_hits", 0) + 1
            return self._provider_cache[ref]
        if self.provider_loader is None:
            raise RuntimeError(f"provider requested but no loader is configured: {ref}")
        provider = self.provider_loader(ref)
        self._provider_cache[ref] = provider
        state.telemetry["provider_activations"] += 1
        return provider
