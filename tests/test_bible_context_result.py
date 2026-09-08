from dore_core.bible.context_policy import SearchContextPolicy
from dore_core.bible.reference import BibleReference
from dore_core.bible.result import augment_context_result, apply_bible_context_result_policy


def test_augment_context_result_preserves_legacy_fields():
    legacy = {
        "id": "r1",
        "title": "Matthew 6",
        "snippet": "seek first the kingdom",
        "kind": "document",
        "score": 0.9,
        "provenance": [],
    }
    ref = BibleReference(book="Matt", chapter=6, verse_start=33, verse_end=34)
    out = augment_context_result(
        legacy,
        source_kind="one",
        bible_reference=ref,
        evidence_status="canonical",
    )
    assert out["id"] == "r1"
    assert out["score"] == 0.9
    assert out["source_kind"] == "one"
    assert out["canonical_reference"]["key"] == "Matt.6.33-34"
    assert out["evidence_status"] == "canonical"
    assert out["actions"] == ["keep", "flow", "present"]


def test_embedded_one_policy_suppresses_one_result_after_augmentation():
    results = [
        {"id": "one", "kind": "one", "title": "ONE"},
        {"id": "note", "kind": "note", "title": "Personal note"},
    ]
    policy = SearchContextPolicy(host="one", mode="prepare", embedded=True)
    out = apply_bible_context_result_policy(results, policy)
    assert [item["id"] for item in out] == ["note"]


def test_present_policy_blocks_all_context_results():
    policy = SearchContextPolicy(host="multiwrite", mode="present")
    out = apply_bible_context_result_policy(
        [{"id": "note", "kind": "note", "title": "Personal note"}], policy
    )
    assert out == []
