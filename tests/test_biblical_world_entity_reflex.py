from dore_core.world.model import Alias,Attestation,WorldEntity
from dore_core.world.entity_reflex import resolve_entity,aggregate_entities

def e(i,label,ref,*aliases,typ='person'):
    return WorldEntity(i,typ,label,tuple(Alias(a,'zh-Hant','test','translation') for a in aliases),(Attestation('test',ref,'SCRIPTURE_EXPLICIT'),))

def test_same_name_stays_ambiguous_without_context():
    entities=[e('judas.iscariot','猶大','bible.ref.MAT.26.14','犹大'),e('judas.james','猶大','bible.ref.LUK.6.16','犹大')]
    r=resolve_entity('犹大',entities)
    assert r.ambiguous and r.resolved_entity_id is None and len(r.candidates)==2

def test_passage_context_disambiguates_same_name():
    entities=[e('judas.iscariot','猶大','bible.ref.MAT.26.14','犹大'),e('judas.james','猶大','bible.ref.LUK.6.16','犹大')]
    r=resolve_entity('猶大',entities,canonical_ref_id='bible.ref.MAT.26.14')
    assert not r.ambiguous and r.resolved_entity_id=='judas.iscariot'

def test_one_chapter_scope_ranks_local_entity_without_erasing_global_candidates():
    entities=[e('mary.jesus','馬利亞','bible.ref.MAT.1.16','玛利亚'),e('mary.magdalene','馬利亞','bible.ref.MAT.27.56','玛利亚')]
    r=resolve_entity('馬利亞',entities,canonical_scope='bible.ref.MAT.1')
    assert r.resolved_entity_id=='mary.jesus'
    assert len(r.candidates)==2 and 'canonical_scope' in r.candidates[0].reasons

def test_alias_routes_to_identity_without_replacing_evidence():
    entity=WorldEntity('peter','person','Peter',(Alias('彼得','zh-Hant','test','translation'),Alias('Πέτρος','grc','test','source_form')),(Attestation('test','bible.ref.MAT.16.18','SCRIPTURE_EXPLICIT'),))
    assert resolve_entity('彼得',[entity]).resolved_entity_id=='peter'
    assert resolve_entity('Πέτρος',[entity]).resolved_entity_id=='peter'

def test_type_context_can_keep_place_and_person_apart():
    person=e('adam.person','亞當','bible.ref.GEN.3.17','亚当')
    place=e('adam.place','亞當','bible.ref.JOS.3.16','亚当',typ='place')
    assert resolve_entity('亚当',[person,place]).ambiguous
    assert resolve_entity('亚当',[person,place],entity_type='place').resolved_entity_id=='adam.place'

def test_canon_wide_count_reports_range_when_identity_merge_is_disputed():
    entities=[e('mary.a','馬利亞','bible.ref.MAT.1.16','玛利亚'),e('mary.b','馬利亞','bible.ref.MAT.27.56','玛利亚'),e('mary.c','馬利亞','bible.ref.JHN.12.3','玛利亚')]
    a=aggregate_entities('玛利亚',entities,entity_type='person',disputed_identity_groups=[('mary.b','mary.c')])
    assert a.maximum_distinct==3 and a.minimum_distinct==2
    assert a.disputed_groups==( ('mary.b','mary.c'), )

def test_canon_aggregation_does_not_count_place_substrings_as_person_entities():
    entities=[e('mary.a','馬利亞','bible.ref.MAT.1.16','玛利亚'),e('samaria','撒馬利亞','bible.ref.JHN.4.4','撒玛利亚',typ='place')]
    a=aggregate_entities('馬利亞',entities,entity_type='person')
    assert a.maximum_distinct==1 and [c.entity.entity_id for c in a.candidates]==['mary.a']

def test_unseen_alias_transfer():
    entity=WorldEntity('jesus','person','Jesus',(Alias('耶穌','zh-Hant','test','translation'),Alias('Ἰησοῦς','grc','test','source_form')),(Attestation('test','bible.ref.MAT.1.21','SCRIPTURE_EXPLICIT'),))
    assert resolve_entity('耶穌',[entity]).resolved_entity_id=='jesus'
