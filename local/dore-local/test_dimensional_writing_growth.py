from dimensional_living_corpus import corpus_context, default_corpus
from dimensional_publishing_capability import DimensionalPublishingCapability
from dimensional_writing_judge import judge_batch
from dimensional_writing_loop import DimensionalWritingLoop
from editorial_decision_ledger import EditorialDecision


def _passing_proposal(proposal_id="p1"):
    return {
        "id": proposal_id,
        "text": "Let the reader hear the Hebrew poem.",
        "checks": {
            "thesis_preserved": True,
            "author_voice_preserved": True,
            "dimension_earns_return": True,
            "evidence_supports_claim": True,
            "media_participates_in_argument": True,
            "reader_burden_not_increased": True,
        },
    }


def test_author_authority_and_return_gate():
    def infer(req):
        if "may_rewrite_thesis" in req:
            assert req["may_rewrite_thesis"] is False
            return {"proposals": [_passing_proposal()]}
        return {}

    result = DimensionalWritingLoop(infer=infer, judge=judge_batch).run(
        title="The Shadow of the Cross",
        manuscript="draft",
        thesis="Christ is the center",
    )
    assert result["accepted_candidates"][0]["id"] == "p1"
    assert result["thesis"] == "Christ is the center"


def test_bad_excursion_fails_closed():
    result = judge_batch({"proposals": [{"id": "p2", "text": "interesting tangent", "checks": {}}]})
    assert result["accepted"] == []
    assert result["rejected"][0]["judgment"]["admit"] is False


def test_editorial_decision_becomes_growth_data():
    record = EditorialDecision(
        work_id="westside:vol01",
        original="original",
        proposal="proposal",
        decision="revise",
        reason="Return line is weak",
        author_revision="final",
        thesis_relation="preserves",
    ).record()
    assert record["schema"] == "dore.editorial-decision.v0"
    assert record["decision_id"].startswith("ed-")
    assert record["capability"] == "publishing.dimensional-writing"


def test_dual_line_corpus_is_parallel_and_temporally_ordered():
    corpus = default_corpus()
    works = {work["work_id"]: work for work in corpus["works"]}
    assert corpus["growth_mode"] == "parallel-real-writing"
    assert corpus["do_not_wait_for_completion"] is True
    assert works["westside:vol00"]["temporal_order"] < works["westside:vol01"]["temporal_order"]
    assert corpus_context("westside:vol00")["parallel_peers"][0]["work_id"] == "westside:vol01"
    assert corpus_context("westside:vol01")["parallel_peers"][0]["work_id"] == "westside:vol00"


def test_compile_carries_peer_baseline_into_growth_loop():
    seen_contexts = []

    def infer(req):
        seen_contexts.append(req.get("context", {}))
        if "may_rewrite_thesis" in req:
            return {"proposals": [_passing_proposal("dual-p1")]}
        return {"deep_dive": [], "return_lines": []}

    result = DimensionalPublishingCapability(infer=infer).compile(
        title="The Shadow of the Cross",
        manuscript="draft",
        thesis="Christ is the center",
        context={"work_id": "westside:vol01"},
    )
    assert result["publication"]["growth_mode"] == "parallel-real-writing"
    assert result["corpus"]["current_work"]["work_id"] == "westside:vol01"
    assert result["corpus"]["parallel_peers"][0]["work_id"] == "westside:vol00"
    assert result["growth"]["accepted_candidates"][0]["id"] == "dual-p1"
    assert any(ctx.get("current_work", {}).get("work_id") == "westside:vol01" for ctx in seen_contexts)
