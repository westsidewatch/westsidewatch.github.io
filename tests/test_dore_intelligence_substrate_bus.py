from __future__ import annotations

import importlib.util
import sys
import unittest
from pathlib import Path
from unittest.mock import patch

ROOT = Path(__file__).resolve().parents[1]
LOCAL = ROOT / "local" / "dore-local"
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

spec = importlib.util.spec_from_file_location("dore_capability_bus_test", LOCAL / "capability_bus.py")
BUS = importlib.util.module_from_spec(spec)
assert spec and spec.loader
spec.loader.exec_module(BUS)

class ProductionStub:
    CAPABILITIES = set()


class SubstrateBusTests(unittest.TestCase):
    def test_virtual_substrates_are_core_owned_capabilities(self):
        found = {x["id"]: x for x in BUS.discover(ProductionStub())}
        self.assertTrue(found["context.fuzzy-search"]["callable"])
        self.assertEqual(found["context.fuzzy-search"]["provider"], "dore-search")
        self.assertEqual(found["context.fuzzy-search"]["result"], "dore-search-results")
        self.assertFalse(found["context.fuzzy-search"]["authority"])
        self.assertTrue(found["knowledge.recall"]["callable"])
        self.assertEqual(found["knowledge.recall"]["provider"], "longmemory-local")
        self.assertFalse(found["knowledge.recall"]["authority"])

    def test_qmd_absence_fails_closed_without_rewriting_product_contract(self):
        with patch.object(BUS, "qmd_available", return_value=False):
            out = BUS.call("context.fuzzy-search", {"query": "嗎哪"}, ProductionStub(), caller_product="multiwrite")
        self.assertFalse(out["ok"])
        self.assertEqual(out["status"], "not_ready")
        self.assertFalse(out["authority"])
        self.assertEqual(out["core_route"]["capability"], "context.fuzzy-search")
        self.assertEqual(out["core_route"]["caller_product"], "multiwrite")
        self.assertEqual(out["core_route"]["provider"], "dore-search")

    def test_fuzzy_search_public_result_hides_substrate_names(self):
        fake_qmd = {
            "ok": True,
            "lane": "hybrid-no-rerank",
            "results": [{"title": "嗎哪與曠野", "snippet": "曠野中的嗎哪", "path": "notes/manna.md"}],
        }
        with patch.object(BUS, "qmd_available", return_value=True), \
             patch.object(BUS, "qmd_search", return_value=fake_qmd), \
             patch.object(BUS, "longmemory_available", return_value=False):
            out = BUS.call(
                "context.fuzzy-search",
                {"query": "這句讓我想到曠野裡的嗎哪"},
                ProductionStub(),
                caller_product="multiwrite",
            )
        self.assertTrue(out["ok"])
        self.assertEqual(out["results"][0]["title"], "嗎哪與曠野")
        self.assertFalse(out["retrieval"]["memory_recall"])
        self.assertFalse(out["large_model_invoked"])
        serialized = str(out).lower()
        self.assertNotIn("qmd-local", serialized)
        self.assertNotIn("longmemory-local", serialized)

    def test_longmemory_absence_fails_closed_without_becoming_authority(self):
        with patch.object(BUS, "longmemory_available", return_value=False):
            out = BUS.call("knowledge.recall", {"query": "主站現在結構"}, ProductionStub(), caller_product="dore-search")
        self.assertFalse(out["ok"])
        self.assertEqual(out["status"], "not_ready")
        self.assertFalse(out["authority"])
        self.assertEqual(out["core_route"]["provider"], "longmemory-local")


if __name__ == "__main__":
    unittest.main()
