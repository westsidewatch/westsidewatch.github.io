from dore_core.world.geography import AncientPlace,ModernCandidate
from dore_core.world.geography_reflex import explain_place,distance_claim_allowed
from dore_core.world.chronology_reflex import bounded_date,compare_sequence
from dore_core.world.polity_reflex import contextualize,validate_time_bound,naming_boundary
from dore_core.world.institution_reflex import explain_institution,valid_context
from dore_core.world.evidence_reflex import EvidenceDecision,can_say_scripture_says,permitted_wording


def candidate(i,c):return ModernCandidate(i,i,c,35.0,31.0,'Point',int(c*1000))

def test_bw2_multiple_geography_candidates_stay_open():
    p=AncientPlace('x','X','x',('settlement',),('bible.ref.JOS.3.16',),None,(candidate('a',.91),candidate('b',.86)))
    assert explain_place(p).resolved_modern_id is None
    assert distance_claim_allowed(source_is_scripture=True,reconstructed=True)=='SCHOLARLY_RECONSTRUCTION'

def test_bw3_reconstruction_is_range_not_fake_scripture_year():
    c=bounded_date('event',reconstructed_range=(586,587),era='BCE')
    assert c.evidence_class=='SCHOLARLY_RECONSTRUCTION' and not c.precise
    assert compare_sequence('exodus','monarchy','before')['relation']=='before'

def test_bw4_polity_identity_is_time_bound_and_naming_is_separated():
    c=contextualize('Judah','Iron Age',biblical_designation='Judah',modern_label='Kingdom of Judah')
    assert validate_time_bound(c)
    assert naming_boundary(c)['same_label_asserted'] is False

def test_bw5_institution_requires_period_and_marks_comparative_reconstruction():
    c=explain_institution('synagogue','Second Temple',comparative_source='historical synthesis')
    assert valid_context(c) and c.evidence_class=='SCHOLARLY_RECONSTRUCTION'

def test_bw6_only_explicit_claim_can_be_worded_as_scripture_says():
    explicit=EvidenceDecision('x','SCRIPTURE_EXPLICIT','bible.ref.MAT.1.1')
    inferred=EvidenceDecision('x','SCRIPTURE_INFERRED','canonical synthesis',confidence=.7)
    assert can_say_scripture_says(explicit)
    assert not can_say_scripture_says(inferred)
    assert permitted_wording(inferred).startswith('The textual evidence suggests')

def test_bw6_contested_reconstruction_carries_contestation():
    d=EvidenceDecision('site','SCHOLARLY_RECONSTRUCTION','gazetteer','Iron Age',.55,'multiple identifications')
    assert 'contested' in permitted_wording(d)
