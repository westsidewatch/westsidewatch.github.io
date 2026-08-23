from dore_core.world.model import Alias,Attestation,WorldEntity
from dore_core.world.entity_reflex import resolve_entity

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
    assert 'canonical_attestation' in r.candidates[0].reasons

def test_alias_routes_to_identity_without_replacing_evidence():
    entity=WorldEntity('peter','person','Peter',(
        Alias('彼得','zh-Hant','test','translation'),Alias('Πέτρος','grc','test','source_form'),
    ),(Attestation('test','bible.ref.MAT.16.18','SCRIPTURE_EXPLICIT'),))
    assert resolve_entity('彼得',[entity]).resolved_entity_id=='peter'
    assert resolve_entity('Πέτρος',[entity]).resolved_entity_id=='peter'

def test_type_context_can_keep_place_and_person_apart():
    person=e('adam.person','亞當','bible.ref.GEN.3.17','亚当')
    place=e('adam.place','亞當','bible.ref.JOS.3.16','亚当',typ='place')
    assert resolve_entity('亚当',[person,place]).ambiguous
    assert resolve_entity('亚当',[person,place],entity_type='place').resolved_entity_id=='adam.place'

def test_unseen_alias_transfer():
    entity=WorldEntity('jesus','person','Jesus',(
        Alias('耶穌','zh-Hant','test','translation'),Alias('Ἰησοῦς','grc','test','source_form'),
    ),(Attestation('test','bible.ref.MAT.1.21','SCRIPTURE_EXPLICIT'),))
    assert resolve_entity('耶穌',[entity]).resolved_entity_id=='jesus'
