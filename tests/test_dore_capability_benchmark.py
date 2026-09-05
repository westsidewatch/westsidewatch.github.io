import unittest

from dore_core.capabilities.benchmark import benchmark_router, expanded_registry
from dore_core.capabilities.registry import default_registry


class CapabilityBenchmarkTests(unittest.TestCase):
    def test_working_set_stays_bounded_with_1000_dormant_capabilities(self):
        base = default_registry()
        large = expanded_registry(base, dormant_count=1000)
        result = benchmark_router(
            large,
            (
                "generate image hero art",
                "critique image candidate",
                "verify design responsive export",
                "Matthew six Greek original language",
            ),
            iterations=10,
            max_active=3,
        )
        self.assertEqual(result.registry_size, len(base) + 1000)
        self.assertLessEqual(result.max_active_capabilities, 3)
        self.assertLessEqual(result.median_active_capabilities, 3)
        self.assertGreaterEqual(result.l2_required, 10)

    def test_benchmark_is_free_first_and_deterministic_contract(self):
        result = benchmark_router(
            default_registry(),
            ("generate image", "verify design"),
            iterations=3,
            max_active=2,
        )
        self.assertEqual(result.iterations, 6)
        self.assertLessEqual(result.max_active_capabilities, 2)
        self.assertGreaterEqual(result.median_route_ms, 0.0)


if __name__ == "__main__":
    unittest.main()
