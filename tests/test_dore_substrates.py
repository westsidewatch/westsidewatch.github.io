from __future__ import annotations

import json
import subprocess
import unittest
from pathlib import Path

from dore_core.substrates.longmemory import LongMemoryConfig, project_context, recall
from dore_core.substrates.qmd import QMDConfig, search


def completed(argv, payload, code=0, err=""):
    return subprocess.CompletedProcess(argv, code, stdout=json.dumps(payload, ensure_ascii=False), stderr=err)


class SubstrateGateTests(unittest.TestCase):
    def test_longmemory_strict_recall_is_non_authoritative(self):
        seen = {}
        def runner(argv):
            seen["argv"] = argv
            return completed(argv, {"memories": [{"text": "current structure has no Antioch"}]})
        out = recall("current main site structure", LongMemoryConfig(Path("/tmp/dore.db"), "westside"), runner=runner)
        self.assertTrue(out["ok"])
        self.assertFalse(out["authority"])
        self.assertEqual(out["mode"], "strict")
        self.assertEqual(seen["argv"][:2], ["longmemory", "recall"])
        self.assertIn("--json", seen["argv"])

    def test_longmemory_historical_mode_is_explicit(self):
        def runner(argv):
            return completed(argv, {"memories": [{"text": "old structure contained Antioch"}]})
        out = recall("old structure", LongMemoryConfig(Path("/tmp/dore.db"), "westside"), mode="historical", runner=runner)
        self.assertEqual(out["mode"], "historical")
        self.assertFalse(out["authority"])

    def test_longmemory_project_context_stays_evidence(self):
        def runner(argv):
            return completed(argv, {"context": "bounded project context"})
        out = project_context("continue engineering", LongMemoryConfig(Path("/tmp/dore.db"), "dore"), runner=runner)
        self.assertTrue(out["ok"])
        self.assertFalse(out["authority"])

    def test_qmd_defaults_to_bm25_without_model(self):
        seen = {}
        def runner(argv):
            seen["argv"] = argv
            return completed(argv, [{"file": "qmd://notes/a.md", "score": 0.8}])
        out = search("嗎哪 曠野", QMDConfig("notes"), runner=runner)
        self.assertEqual(out["lane"], "bm25")
        self.assertEqual(seen["argv"][1], "search")
        self.assertNotIn("--no-rerank", seen["argv"])
        self.assertFalse(out["authority"])

    def test_qmd_semantic_uses_hybrid_without_rerank(self):
        seen = {}
        def runner(argv):
            seen["argv"] = argv
            return completed(argv, [])
        out = search("這句讓我想到曠野裡的嗎哪", semantic=True, runner=runner)
        self.assertEqual(out["lane"], "hybrid-no-rerank")
        self.assertEqual(seen["argv"][1], "query")
        self.assertIn("--no-rerank", seen["argv"])

    def test_qmd_deep_is_only_explicit_rerank_lane(self):
        seen = {}
        def runner(argv):
            seen["argv"] = argv
            return completed(argv, [])
        out = search("ambiguous research question", semantic=True, deep=True, runner=runner)
        self.assertEqual(out["lane"], "hybrid-rerank")
        self.assertNotIn("--no-rerank", seen["argv"])

    def test_substrate_failure_does_not_redefine_dore_state(self):
        def bad(argv):
            return subprocess.CompletedProcess(argv, 2, stdout="", stderr="offline")
        lm = recall("x", LongMemoryConfig(Path("/tmp/dore.db"), "dore"), runner=bad)
        qmd = search("x", runner=bad)
        self.assertFalse(lm["ok"])
        self.assertFalse(qmd["ok"])
        self.assertFalse(lm["authority"])
        self.assertFalse(qmd["authority"])


if __name__ == "__main__":
    unittest.main()
