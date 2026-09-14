from dimensional_writing_judge import judge_batch
from dimensional_writing_loop import DimensionalWritingLoop
from editorial_decision_ledger import EditorialDecision


def test_author_authority_and_return_gate():
    def infer(req):
        assert req["may_rewrite_thesis"] is False
        return {
            "proposals": [
                {
                    "id": "p1",
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
            ]
        }

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
