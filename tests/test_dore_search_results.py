from __future__ import annotations

import unittest

from dore_core.retrieval.living import retrieve
from dore_core.retrieval.results import merge_results


class DoreSearchResultTests(unittest.TestCase):
    def test_merge_results_deduplicates_and_preserves_provenance(self):
        qmd = {
            "ok": True,
            "lane": "hybrid-no-rerank",
            "results": [
                {"title": "嗎哪與曠野", "snippet": "以色列人在曠野得嗎哪", "path": "notes/manna.md", "score": 0.91},
                {"title": "出埃及記十六章", "snippet": "嗎哪的供應", "path": "notes/ex16.md", "score": 0.72},
            ],
        }
        memory = {
            "ok": True,
            "mode": "strict",
            "payload": {
                "results": [
                    {"title": "嗎哪與曠野", "text": "以色列人在曠野得嗎哪", "path": "notes/manna.md", "score": 0.88},
                ]
            },
        }

        results = merge_results(qmd, memory)

        self.assertEqual(len(results), 2)
        self.assertEqual(results[0]["title"], "嗎哪與曠野")
        self.assertEqual(results[0]["score"], 0.91)
        self.assertEqual({p["kind"] for p in results[0]["provenance"]}, {"document", "memory"})
        self.assertNotIn("qmd", str(results[0]).lower())
        self.assertNotIn("longmemory", str(results[0]).lower())

    def test_passive_fuzzy_search_stays_light_and_returns_clean_results(self):
        calls = {"memory": 0}

        def qmd_search(text, *, semantic, deep, limit):
            self.assertEqual(text, "這句讓我想到曠野裡的嗎哪")
            self.assertTrue(semantic)
            self.assertFalse(deep)
            return {
                "ok": True,
                "lane": "hybrid-no-rerank",
                "results": [{"title": "嗎哪與曠野", "snippet": "曠野中的嗎哪", "path": "notes/manna.md"}],
            }

        def memory_recall(text, *, mode):
            calls["memory"] += 1
            return {"ok": True, "mode": mode, "payload": {"results": []}}

        result = retrieve(
            "這句讓我想到曠野裡的嗎哪",
            qmd_search=qmd_search,
            memory_recall=memory_recall,
            explicit_search=False,
        )

        self.assertEqual(calls["memory"], 0)
        self.assertFalse(result["large_model_invoked"])
        self.assertEqual(result["results"][0]["title"], "嗎哪與曠野")
        self.assertEqual(result["results"][0]["provenance"][0]["kind"], "document")

    def test_explicit_search_may_add_current_memory_and_merge_duplicate(self):
        calls = {"memory": 0}

        def qmd_search(text, *, semantic, deep, limit):
            return {
                "ok": True,
                "lane": "hybrid-no-rerank",
                "results": [{"title": "嗎哪與曠野", "snippet": "曠野中的嗎哪", "path": "notes/manna.md", "score": 0.8}],
            }

        def memory_recall(text, *, mode):
            calls["memory"] += 1
            self.assertEqual(mode, "strict")
            return {
                "ok": True,
                "mode": mode,
                "payload": {"results": [{"title": "嗎哪與曠野", "text": "曠野中的嗎哪", "path": "notes/manna.md", "score": 0.9}]},
            }

        result = retrieve(
            "這句讓我想到曠野裡的嗎哪",
            qmd_search=qmd_search,
            memory_recall=memory_recall,
            explicit_search=True,
        )

        self.assertEqual(calls["memory"], 1)
        self.assertEqual(len(result["results"]), 1)
        self.assertEqual(result["results"][0]["score"], 0.9)
        self.assertEqual({p["kind"] for p in result["results"][0]["provenance"]}, {"document", "memory"})


if __name__ == "__main__":
    unittest.main()
