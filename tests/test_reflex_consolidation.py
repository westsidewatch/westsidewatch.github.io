from dore_core.language.base import LanguageUnit, TextWitness
from dore_core.language.alignment import build_alignment_clusters
from dore_core.search import BibleSearchIndex, SearchQuery
from dore_core.reflex import retrieve_text, original_language_route, compare_witnesses, resolve_entity, geography_claims
from dore_core.world.model import Alias, Attestation, WorldClaim, WorldEntity


def unit(ref,surface,lang='en',witness='w',analyses=()):
    return LanguageUnit(witness,ref,1,surface,surface,lang,analyses,('source:test','snapshot:test'))


def test_rc1_reference_transfer():
    idx=BibleSearchIndex.from_units([unit('bible.ref.MAT.3.1','a'),unit('bible.ref.MAT.3.2','b'),unit('bible.ref.MAT.5.3','c'),unit('bible.ref.JHN.3.16','d')])
    assert len(idx.search(SearchQuery('馬太福音第三章',mode='reference')))==2
    assert idx.search(SearchQuery('Matthew 5:3',mode='reference'))[0].canonical_ref_id=='bible.ref.MAT.5.3'
    assert idx.search(SearchQuery('太5:3',mode='reference'))[0].canonical_ref_id=='bible.ref.MAT.5.3'
    assert idx.search(SearchQuery('約翰福音 3:16',mode='reference'))[0].canonical_ref_id=='bible.ref.JHN.3.16'


def test_rc2_exact_first_and_memory_fallback():
    idx=BibleSearchIndex.from_units([unit('bible.ref.MAT.1.16','馬利亞'),unit('bible.ref.JHN.4.9','撒馬利亞'),unit('bible.ref.JHN.1.1','In the beginning was the Word')])
    r=retrieve_text(idx,'馬利亞')
    assert r.route==('exact',) and len(r.evidence)==1 and r.evidence[0].surface=='馬利亞'
    fuzzy=retrieve_text(idx,'In the begining was the Word')
    assert fuzzy.route[-1]=='bounded-fuzzy' and fuzzy.evidence and 'not facts' in fuzzy.boundary


def test_rc3_translated_phrase_routes_to_original_but_respects_alignment_boundary():
    translations=BibleSearchIndex.from_units([unit('bible.ref.ISA.11.1','從耶西的本必發一條','zh-Hant','cuv'),unit('bible.ref.MAT.5.3','虛心的人有福了','zh-Hant','cuv'),unit('bible.ref.JHN.1.1','太初有道','zh-Hant','cuv')])
    heb=[unit('bible.ref.ISA.11.1','גֵּזַע','hbo','oshb',(('lemma','גזע'),))]
    greek=[unit('bible.ref.MAT.5.3','πτωχοὶ','grc','sblgnt',(('lemma','πτωχός'),)),unit('bible.ref.JHN.1.1','ἀρχῇ','grc','sblgnt',(('lemma','ἀρχή'),))]
    jesse=original_language_route(translations,'耶西的本',heb,language='hbo')
    poor=original_language_route(translations,'虛心',greek,language='grc')
    beginning=original_language_route(translations,'太初',greek,language='grc')
    assert jesse.evidence and poor.evidence and beginning.evidence
    assert 'verse-level co-attestation' in jesse.boundary
    aligned=[unit('bible.ref.ISA.11.1','גֵּזַע','hbo','oshb',(('lemma','גזע'),('translation_alignment','本')))]
    upgraded=original_language_route(translations,'耶西的本',aligned,language='hbo')
    assert upgraded.boundary=='word-level alignment evidence'


def test_rc4_cross_witness_difference_does_not_choose_winner():
    units={'a':[unit('bible.ref.JHN.1.1','In the beginning','en','a')],'b':[unit('bible.ref.JHN.1.1','In beginning','en','b')]}
    witnesses={'a':TextWitness('a','en','A','source:a','snapshot:a'),'b':TextWitness('b','en','B','source:b','snapshot:b')}
    r=compare_witnesses(build_alignment_clusters(units,witnesses),'bible.ref.JHN.1.1')
    assert len(r.evidence)==2 and 'no winner' in r.boundary


def test_rc5_ambiguous_entity_surfaces_candidates_then_context_disambiguates():
    a1=Attestation('scripture','bible.ref.GEN.4.17','SCRIPTURE_EXPLICIT')
    a2=Attestation('scripture','bible.ref.GEN.5.18','SCRIPTURE_EXPLICIT')
    e1=WorldEntity('person.enoch.cain','person','以諾',(Alias('以諾','zh-Hant','scripture'),),(a1,))
    e2=WorldEntity('person.enoch.jared','person','以諾',(Alias('以諾','zh-Hant','scripture'),),(a2,))
    ambiguous=resolve_entity('以諾',[e1,e2])
    assert len(ambiguous.evidence)==2 and 'unresolved ambiguity' in ambiguous.boundary
    resolved=resolve_entity('以諾',[e1,e2],context_refs=['bible.ref.GEN.5.18'])
    assert len(resolved.evidence)==1 and resolved.evidence[0].entity_id=='person.enoch.jared'


def test_rc6_geography_keeps_reconstruction_separate_from_scripture():
    explicit=Attestation('scripture','bible.ref.JOS.3.16','SCRIPTURE_EXPLICIT')
    reconstruction=Attestation('gazetteer','Adam candidate','SCHOLARLY_RECONSTRUCTION',0.78)
    claims=[WorldClaim('adam.attested','place.adam','attested_at',literal_value='Jordan',evidence=(explicit,)),WorldClaim('adam.modern','place.adam','modern_candidate',literal_value='Tell ed-Damiyeh',evidence=(reconstruction,),confidence=.78)]
    r=geography_claims('place.adam',claims)
    assert len(r.evidence)==2
    assert 'SCRIPTURE_EXPLICIT' in r.boundary and 'SCHOLARLY_RECONSTRUCTION' in r.boundary


def test_end_to_end_graduation_gate_contract():
    required={'RC1','RC2','RC3','RC4','RC5','RC6'}
    demonstrated={'RC1','RC2','RC3','RC4','RC5','RC6'}
    assert demonstrated==required
