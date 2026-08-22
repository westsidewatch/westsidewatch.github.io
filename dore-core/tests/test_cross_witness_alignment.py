from dore_core.language.alignment import audit_alignment, build_alignment_clusters
from dore_core.language.base import LanguageUnit, TextWitness


def witness(wid: str, lang: str, edition: str) -> TextWitness:
    return TextWitness(wid, lang, edition, f"source:{wid}", "test-snapshot")


def unit(wid: str, lang: str, ref: str | None, text: str, order: int = 1) -> LanguageUnit:
    return LanguageUnit(wid, ref, order, text, text, lang, provenance=(f"source:{wid}",))


def test_alignment_preserves_distinct_witness_identity():
    witnesses = {
        "heb": witness("heb", "he", "OSHB"),
        "lxx": witness("lxx", "grc", "LXX"),
        "cuv": witness("cuv", "zh-Hant", "CUV Traditional"),
        "kjv": witness("kjv", "en", "KJV"),
    }
    units = {
        "heb": [unit("heb", "he", "GEN.1.1", "בראשית")],
        "lxx": [unit("lxx", "grc", "GEN.1.1", "Ἐν ἀρχῇ")],
        "cuv": [unit("cuv", "zh-Hant", "GEN.1.1", "起初")],
        "kjv": [unit("kjv", "en", "GEN.1.1", "In the beginning")],
    }
    clusters = build_alignment_clusters(units, witnesses)
    assert len(clusters) == 1
    assert clusters[0].canonical_ref_id == "GEN.1.1"
    assert set(clusters[0].witness_ids) == {"heb", "lxx", "cuv", "kjv"}
    assert len({item.surface for item in clusters[0].witnesses}) == 4


def test_audit_queues_missing_witness_instead_of_synthesizing():
    witnesses = {
        "heb": witness("heb", "he", "OSHB"),
        "lxx": witness("lxx", "grc", "LXX"),
    }
    units = {
        "heb": [unit("heb", "he", "GEN.1.1", "בראשית")],
        "lxx": [],
    }
    report = audit_alignment(units, witnesses, expected_witnesses=("heb", "lxx"))
    assert report.status == "REVIEW"
    assert report.incomplete_refs == 1
    assert any(
        e.code == "MISSING_WITNESS_AT_REF" and e.witness_id == "lxx"
        for e in report.exceptions
    )


def test_audit_flags_unaligned_units():
    witnesses = {"cuv": witness("cuv", "zh-Hant", "CUV Traditional")}
    units = {"cuv": [unit("cuv", "zh-Hant", None, "未對齊")]} 
    report = audit_alignment(units, witnesses)
    assert any(e.code == "UNALIGNED_UNIT" for e in report.exceptions)
