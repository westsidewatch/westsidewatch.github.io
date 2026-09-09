from dore_core.bible.query_planner import plan_bible_query


def test_reference_first_without_model():
    plan = plan_bible_query("馬太福音 6:33 先求他的國和義")
    assert plan.intent == "reference"
    assert plan.lanes[:2] == ("reference", "biblical_world")
    assert plan.semantic_allowed is False
    assert plan.large_model_required is False
    assert plan.model_invoked is False
    assert plan.execution_level == "L1-retrieval"


def test_geography_uses_world_before_documents():
    plan = plan_bible_query("基列的雅比城在哪裡？")
    assert plan.intent == "geography"
    assert plan.lanes[:2] == ("geography", "biblical_world")
    assert plan.lanes.index("biblical_world") < plan.lanes.index("document")


def test_entity_count_uses_entity_reflex():
    plan = plan_bible_query("聖經中一共有幾位馬利亞？")
    assert plan.intent == "entity"
    assert plan.lanes[0] == "entity"
    assert plan.model_invoked is False


def test_interpretive_query_marks_reasoning_without_invoking_model():
    plan = plan_bible_query("為什麼馬太把這段放在這裡？")
    assert plan.reasoning_allowed is True
    assert plan.execution_level == "L3-reasoning"
    assert plan.model_invoked is False


def test_deep_escalation_is_explicit_and_observable():
    plan = plan_bible_query("嗎哪和約翰福音六章有什麼關係？", deep=True)
    assert plan.semantic_allowed is True
    assert plan.reasoning_allowed is True
    assert plan.lanes[-2:] == ("semantic", "reasoning")
    assert plan.escalation_policy == "lowest-sufficient-capability"
