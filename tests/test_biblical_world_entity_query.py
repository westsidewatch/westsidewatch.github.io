from dore_core.world.entity_query import parse_entity_question

def test_entity_count_intent_is_generic():
    q=parse_entity_question('聖經有幾位馬利亞？')
    assert q and q.kind=='entity_count' and q.mention=='馬利亞' and q.entity_type=='person'
    q=parse_entity_question('圣经中有多少个犹大?')
    assert q and q.mention=='犹大'

def test_non_count_question_is_not_forced_into_entity_count():
    assert parse_entity_question('馬利亞') is None
    assert parse_entity_question('馬太福音第三章') is None
