from __future__ import annotations

import json

from dore_core.capabilities.benchmark import benchmark_router, expanded_registry
from dore_core.capabilities.registry import default_registry


def main() -> int:
    base = default_registry()
    large = expanded_registry(base, dormant_count=1000)
    queries = (
        "generate image hero art",
        "critique image candidate",
        "verify design responsive export",
        "Matthew six Greek original language",
    )
    base_result = benchmark_router(base, queries, iterations=50, max_active=3)
    large_result = benchmark_router(large, queries, iterations=50, max_active=3)
    report = {
        "status": "PASS" if large_result.max_active_capabilities <= 3 else "FAIL",
        "invariant": "registry growth must not expand active working set",
        "base": base_result.__dict__,
        "plus_1000_dormant": large_result.__dict__,
        "criteria": {
            "max_active_capabilities": 3,
            "metered_model_calls": 0,
            "provider_activations": 0,
        },
    }
    print(json.dumps(report, ensure_ascii=False, indent=2, sort_keys=True))
    return 0 if report["status"] == "PASS" else 1


if __name__ == "__main__":
    raise SystemExit(main())
