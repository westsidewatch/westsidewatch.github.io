from dore_core.retrieval.living import plan, retrieve


def test_compact_term_stays_bm25():
    p = plan("嗎哪")
    assert p.lexical is True
    assert p.semantic is False
    assert p.deep is False
    assert p.recall_memory is False


def test_cjk_natural_phrase_uses_hybrid_without_rerank():
    p = plan("這句讓我想到曠野裡的嗎哪")
    assert p.lexical is True
    assert p.semantic is True
    assert p.deep is False
    assert p.recall_memory is False


def test_bible_relation_language_is_fuzzy_signal():
    for text in ("這段和出埃及記有什麼呼應", "這是不是一個預表", "找相關串珠"):
        p = plan(text)
        assert p.semantic is True
        assert p.deep is False


def test_explicit_search_can_recall_current_memory_without_heavy_model():
    calls = {"qmd": 0, "memory": 0}

    def qmd_search(text, *, semantic, deep, limit):
        calls["qmd"] += 1
        return {"ok": True, "lane": "hybrid-no-rerank" if semantic else "bm25", "results": [{"title": "嗎哪與曠野"}]}

    def memory_recall(text, *, mode):
        calls["memory"] += 1
        assert mode == "strict"
        return {"ok": True, "results": [{"id": "current-1"}]}

    result = retrieve(
        "這句讓我想到曠野裡的嗎哪",
        qmd_search=qmd_search,
        memory_recall=memory_recall,
        explicit_search=True,
    )
    assert calls == {"qmd": 1, "memory": 1}
    assert result["large_model_invoked"] is False
    assert result["authority"] is False


def test_passive_fuzzy_search_does_not_wake_memory():
    calls = {"memory": 0}

    def qmd_search(text, *, semantic, deep, limit):
        return {"ok": True, "lane": "hybrid-no-rerank", "results": [{"title": "嗎哪與曠野"}]}

    def memory_recall(text, *, mode):
        calls["memory"] += 1
        return {"ok": True}

    result = retrieve(
        "這句讓我想到曠野裡的嗎哪",
        qmd_search=qmd_search,
        memory_recall=memory_recall,
        explicit_search=False,
    )
    assert calls["memory"] == 0
    assert result["large_model_invoked"] is False
    assert result["qmd"]["results"][0]["title"] == "嗎哪與曠野"
