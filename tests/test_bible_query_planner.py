from dore_core.bible.query_planner import plan_bible_query


def test_reference_first_without_model():
    p=plan_bible_query('馬太福音 6:33 為什麼說先求他的國和義？')
    assert p.intent=='reference'
    assert p.lanes[:2]==('reference','biblical_world')
    assert p.semantic_allowed is False
    assert p.large_model_required is False


def test_geography_uses_world_before_documents():
    p=plan_bible_query('基列的雅比城在哪裡？')
    assert p.intent=='geography'
    assert p.lanes[:2]==('geography','biblical_world')
    assert p.lanes.index('biblical_world') < p.lanes.index('document')


def test_entity_count_uses_entity_reflex():
    p=plan_bible_query('聖經中一共有幾位馬利亞？')
    assert p.intent=='entity'
    assert p.lanes[0]=='entity'


def test_deep_escalates_only_when_requested():
    p=plan_bible_query('嗎哪和約翰福音六章有什麼關係？',deep=True)
    assert p.semantic_allowed is True
    assert p.reasoning_allowed is True
    assert p.lanes[-2:]==('semantic','reasoning')
