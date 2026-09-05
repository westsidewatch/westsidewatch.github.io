from __future__ import annotations

from dataclasses import dataclass
from statistics import median
from time import perf_counter

from .model import CapabilityManifest, TaskState
from .registry import CapabilityRegistry
from .router import SparseCapabilityRouter


@dataclass(frozen=True)
class BenchmarkResult:
    registry_size: int
    iterations: int
    median_route_ms: float
    median_active_capabilities: float
    max_active_capabilities: int
    l2_required: int


def benchmark_router(
    registry: CapabilityRegistry,
    queries: tuple[str, ...],
    *,
    iterations: int = 50,
    max_active: int = 3,
) -> BenchmarkResult:
    if not queries:
        raise ValueError("queries required")
    router = SparseCapabilityRouter(registry, max_active=max_active)
    route_times: list[float] = []
    active_counts: list[int] = []
    l2_required = 0
    for i in range(iterations):
        for query in queries:
            state = TaskState(f"bench-{i}")
            started = perf_counter()
            decision = router.route(query, state=state)
            route_times.append((perf_counter() - started) * 1000)
            active_counts.append(len(state.active_capabilities))
            if decision.level == "L2_REQUIRED":
                l2_required += 1
    return BenchmarkResult(
        registry_size=len(registry),
        iterations=iterations * len(queries),
        median_route_ms=median(route_times),
        median_active_capabilities=median(active_counts),
        max_active_capabilities=max(active_counts),
        l2_required=l2_required,
    )


def expanded_registry(base: CapabilityRegistry, *, dormant_count: int) -> CapabilityRegistry:
    registry = CapabilityRegistry(base.all())
    for i in range(dormant_count):
        registry.register(CapabilityManifest(
            id=f"dormant.synthetic.{i:05d}",
            faculty="synthetic",
            description=f"Dormant synthetic capability {i}",
            triggers=(f"synthetic-trigger-{i}",),
        ))
    return registry
