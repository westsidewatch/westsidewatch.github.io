from dore_core.bible import (
    BibleReference,
    SearchContextPolicy,
    StudyBlock,
    StudyDocument,
    StudyFlowItem,
    apply_search_context_policy,
)


def test_bible_reference_contract_and_key():
    ref = BibleReference(book="Matt", chapter=6, verse_start=33, verse_end=34)
    payload = ref.to_dict()
    assert payload["schema"] == "dore.bible-reference.v1"
    assert payload["key"] == "Matt.6.33-34"
    assert BibleReference.from_dict(payload) == ref


def test_study_document_flow_duration_and_actions():
    ref = BibleReference(book="Matt", chapter=6, verse_start=33, verse_end=34)
    block = StudyBlock(
        id="b1",
        kind="bible-reference",
        bible_reference=ref,
        actions=["keep", "flow", "present"],
    )
    doc = StudyDocument(
        id="study-matt-6",
        title="Matthew 6",
        bible_context=ref,
        blocks=[block],
        flow=[StudyFlowItem(block_id="b1", order=0, duration_seconds=300, present=True)],
    )
    payload = doc.to_dict()
    assert payload["planned_duration_seconds"] == 300
    assert payload["blocks"][0]["bible_reference"]["key"] == "Matt.6.33-34"


def test_standalone_multiwrite_keeps_one_recommendations():
    results = [
        {"id": "n1", "source_kind": "note", "title": "My note"},
        {"id": "o1", "source_kind": "one", "title": "ONE · Matthew 6"},
    ]
    policy = SearchContextPolicy(host="multiwrite", mode="prepare", embedded=False)
    output = apply_search_context_policy(results, policy)
    assert [item["id"] for item in output] == ["n1", "o1"]
    assert output[0]["actions"] == ["keep", "flow", "present"]


def test_embedded_multiwrite_in_one_suppresses_one_only():
    results = [
        {"id": "n1", "source_kind": "note", "title": "My note"},
        {"id": "o1", "source_kind": "one", "title": "ONE · Matthew 6"},
        {"id": "j1", "source_kind": "journal", "title": "Journal"},
    ]
    policy = SearchContextPolicy(host="one", mode="prepare", embedded=True)
    output = apply_search_context_policy(results, policy)
    assert [item["id"] for item in output] == ["n1", "j1"]


def test_live_mode_disables_ambient_but_keeps_explicit_results():
    policy = SearchContextPolicy(host="multiwrite", mode="live")
    assert policy.ambient_enabled is False
    assert policy.search_enabled is True
    assert apply_search_context_policy([{"id": "x", "source_kind": "note"}], policy)


def test_present_mode_returns_no_search_results():
    policy = SearchContextPolicy(host="multiwrite", mode="present")
    assert policy.search_enabled is False
    assert apply_search_context_policy([{"id": "x", "source_kind": "note"}], policy) == []
