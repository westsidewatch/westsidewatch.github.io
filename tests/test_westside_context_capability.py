"""Contract test for exposing Westside Context through Doré capability discovery."""
from __future__ import annotations

import importlib
import json
from pathlib import Path
import unittest


ROOT = Path(__file__).resolve().parents[1]
REGISTRY = ROOT / "dore-core" / "runtime" / "capability-registry.v1.json"


class WestsideContextCapabilityTests(unittest.TestCase):
    def test_capability_is_local_read_only_and_resolvable(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        capability = next(item for item in registry["capabilities"] if item["id"] == "westside.context")

        self.assertEqual(capability["execution"], "adapter")
        self.assertEqual(capability["cost"], "local")
        self.assertFalse(capability["network"])
        self.assertFalse(capability["write_access"])
        self.assertEqual(capability["source_of_truth"], "docs/MASTER_SITE_ARCHITECTURE.md")

        module_name, function_name = capability["entrypoint"].split(":", 1)
        function = getattr(importlib.import_module(module_name), function_name)
        self.assertTrue(callable(function))

    def test_capability_does_not_register_a_new_knowledge_or_memory_store(self) -> None:
        registry = json.loads(REGISTRY.read_text(encoding="utf-8"))
        capability = next(item for item in registry["capabilities"] if item["id"] == "westside.context")
        self.assertEqual(capability["type"], "context")
        self.assertNotIn("provider", capability)
        self.assertNotIn("database", capability)
        self.assertNotIn("vector_store", capability)
        self.assertNotIn("graph_store", capability)


if __name__ == "__main__":
    unittest.main()
