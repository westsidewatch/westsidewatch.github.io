from dore_core.world.geography import AncientPlace,ModernCandidate
from dore_core.world.geography_reflex import explain_place,distance_claim_allowed

def candidate(i,confidence,lat=31.0,lon=35.0):
    return ModernCandidate(i,i,confidence,lon,lat,'Point',int(confidence*1000))

def test_scripture_attestation_is_separate_from_modern_candidate():
    p=AncientPlace('adam','Adam','adam',('settlement',),('bible.ref.JOS.3.16',),None,(candidate('modern.adam',.91),))
    a=explain_place(p)
    assert a.scripture_explicit==('bible.ref.JOS.3.16:place_attested',)
    assert 'modern.adam' in a.reconstruction[0]
    assert a.resolved_modern_id=='modern.adam'

def test_multiple_strong_identifications_remain_unresolved():
    p=AncientPlace('x','X','x',('settlement',),('bible.ref.GEN.1.1',),None,(candidate('site.a',.9),candidate('site.b',.85)))
    assert explain_place(p).resolved_modern_id is None

def test_low_confidence_candidate_is_not_promoted_to_identity():
    p=AncientPlace('x','X','x',('settlement',),(),None,(candidate('site.a',.45),))
    assert explain_place(p).resolved_modern_id is None

def test_route_distance_reconstruction_never_becomes_scripture_fact():
    assert distance_claim_allowed(source_is_scripture=True,reconstructed=True)=='SCHOLARLY_RECONSTRUCTION'
    assert distance_claim_allowed(source_is_scripture=True,reconstructed=False)=='SCRIPTURE_EXPLICIT'
    assert distance_claim_allowed(source_is_scripture=False,reconstructed=False)=='GEOSPATIAL_OBSERVATION'
