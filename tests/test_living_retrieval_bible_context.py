from dore_core.retrieval.living import retrieve


def _qmd_with_one_and_note(calls):
    def search(query, *, semantic=False, deep=False, limit=6):
        calls.append({"query": query, "semantic": semantic, "deep": deep, "limit": limit})
        return {
            "ok": True,
            "lane": "lexical",
            "results": [
                {
                    "title": "ONE · Matthew 6",
                    "snippet": "Matthew 6 study preview",
                    "uri": "one://Matt/6",
                    "source_kind": "one",
                    "source_ref": "Matt.6",
                    "score": 0.95,
                },
                {
                    "title": "My manna note",
                    "snippet": "Daily provision and Exodus 16",
                    "uri": "note://manna",
                    "source_kind": "note",
                    "score": 0.9,
                },
            ],
        }
    return search


def test_standalone_multiwrite_keeps_one_as_a_context_source():
    calls = []
    out = retrieve(
        "曠野中的嗎哪",
        qmd_search=_qmd_with_one_and_note(calls),
        host="multiwrite",
        mode="prepare",
        embedded=False,
    )
    assert len(calls) == 1
    assert [item["source_kind"] for item in out["results"]] == ["one", "note"]
    assert out["results"][0]["source_ref"] == "Matt.6"
    assert out["results"][0]["actions"] == ["keep", "flow", "present"]
    assert out["context_policy"]["ambient_enabled"] is True


def test_embedded_multiwrite_in_one_suppresses_one_self_result_only():
    calls = []
    out = retrieve(
        "曠野中的嗎哪",
        qmd_search=_qmd_with_one_and_note(calls),
        host="one",
        mode="prepare",
        embedded=True,
    )
    assert len(calls) == 1
    assert [item["source_kind"] for item in out["results"]] == ["note"]
    assert out["context_policy"]["suppressed_source_kinds"] == ["one"]


def test_live_mode_does_not_run_ambient_retrieval():
    calls = []
    out = retrieve(
        "嗎哪",
        qmd_search=_qmd_with_one_and_note(calls),
        host="one",
        mode="live",
        embedded=True,
    )
    assert calls == []
    assert out["results"] == []
    assert out["plan"].reason.startswith("live mode")


def test_live_mode_still_allows_explicit_search():
    calls = []
    out = retrieve(
        "嗎哪",
        qmd_search=_qmd_with_one_and_note(calls),
        host="one",
        mode="live",
        embedded=True,
        explicit_search=True,
    )
    assert len(calls) == 1
    assert [item["source_kind"] for item in out["results"]] == ["note"]


def test_present_mode_performs_zero_retrieval():
    calls = []
    out = retrieve(
        "馬太福音六章",
        qmd_search=_qmd_with_one_and_note(calls),
        host="multiwrite",
        mode="present",
    )
    assert calls == []
    assert out["results"] == []
    assert out["context_policy"]["search_enabled"] is False
