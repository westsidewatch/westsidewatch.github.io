from __future__ import annotations

import unittest

from dore_core.retrieval.living import plan, retrieve


class LivingRetrievalTests(unittest.TestCase):
    def test_short_note_stays_bm25_only(self):
        p = plan("嗎哪 曠野")
        self.assertTrue(p.lexical)
        self.assertFalse(p.semantic)
        self.assertFalse(p.deep)
        self.assertFalse(p.recall_memory)

    def test_note_fragment_uses_hybrid_without_rerank(self):
        p = plan("這句讓我想到曠野裡的嗎哪")
        self.assertTrue(p.lexical)
        self.assertTrue(p.semantic)
        self.assertFalse(p.deep)
        self.assertFalse(p.recall_memory)

    def test_memory_is_not_woken_for_passive_presearch(self):
        calls = []
        def qmd(text, **kwargs):
            calls.append(("qmd", kwargs))
            return {"ok": True, "results": ["x"], "authority": False}
        def memory(text, **kwargs):
            calls.append(("memory", kwargs))
            return {"ok": True, "payload": ["m"], "authority": False}
        out = retrieve("這句讓我想到曠野裡的嗎哪", qmd_search=qmd, memory_recall=memory)
        self.assertEqual([c[0] for c in calls], ["qmd"])
        self.assertFalse(out["authority"])

    def test_explicit_search_can_add_strict_memory_evidence(self):
        calls = []
        def qmd(text, **kwargs):
            calls.append(("qmd", kwargs))
            return {"ok": True, "results": [], "authority": False}
        def memory(text, **kwargs):
            calls.append(("memory", kwargs))
            return {"ok": True, "payload": {"current": True}, "authority": False}
        out = retrieve("主站現在的欄目結構是什麼", qmd_search=qmd, memory_recall=memory, explicit_search=True)
        self.assertEqual([c[0] for c in calls], ["qmd", "memory"])
        self.assertEqual(calls[1][1]["mode"], "strict")
        self.assertFalse(out["authority"])

    def test_deep_request_is_only_path_to_rerank_lane(self):
        seen = {}
        def qmd(text, **kwargs):
            seen.update(kwargs)
            return {"ok": True, "results": [], "authority": False}
        retrieve("需要深入比較這些互文與背景來源", qmd_search=qmd, deep_requested=True)
        self.assertTrue(seen["semantic"])
        self.assertTrue(seen["deep"])


if __name__ == "__main__":
    unittest.main()
