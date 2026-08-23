#!/usr/bin/env python3
"""One-shot Biblical World graduation gate (BW-1..BW-6 + cross-domain blind exam)."""
from __future__ import annotations
import json,sys
from pathlib import Path
from dore_core.world.foundation_registry import registry_checks,MACRO_PERIODS,EMPIRE_SEQUENCE,INSTITUTIONS
from dore_core.world.evidence_reflex import EvidenceDecision,can_say_scripture_says
from dore_core.world.chronology_reflex import bounded_date
from dore_core.world.polity_reflex import contextualize,validate_time_bound
from dore_core.world.institution_reflex import explain_institution,valid_context
from dore_core.world.geography_reflex import distance_claim_allowed

REPORT=Path('reports/DORÉ-BIBLICAL-WORLD-GRADUATION.json')
BW1=Path('reports/DORÉ-BW1-ENTITY-GRADUATION.json')
GEO=Path('reports/DORÉ-BIBLICAL-GEOGRAPHY.json')

def load(path):
    return json.loads(path.read_text(encoding='utf-8')) if path.exists() else {}

def main():
    bw1=load(BW1);geo=load(GEO);reg=registry_checks();checks={}
    checks['bw1_entity_complete']=bw1.get('status')=='PASS'
    checks['bw2_geography_complete']=geo.get('status')=='PASS'
    checks['bw3_chronology_registry']=reg['macro_periods']
    checks['bw4_polity_registry']=reg['empire_sequence']
    checks['bw5_institutions_registry']=reg['institutions'] and reg['institution_period_integrity']
    checks['bw6_evidence_registry']=reg['evidence_classes_present']

    # Cross-domain blind exam: unseen combinations, not user-known live examples.
    # A route estimate from Scripture-linked places must remain reconstruction.
    checks['blind_geo_evidence_boundary']=distance_claim_allowed(source_is_scripture=True,reconstructed=True)=='SCHOLARLY_RECONSTRUCTION'
    # A historical absolute range cannot be promoted to a Scripture-explicit exact year.
    c=bounded_date('blind historical event',reconstructed_range=(722,721),era='BCE')
    checks['blind_chronology_boundary']=c.evidence_class=='SCHOLARLY_RECONSTRUCTION' and not c.precise
    # Polity must be time bound.
    p=contextualize('Assyria','Neo-Assyrian period',biblical_designation='Assyria',modern_label='Neo-Assyrian Empire')
    checks['blind_polity_context']=validate_time_bound(p)
    # Social institution explanation requires period and preserves reconstruction source.
    i=explain_institution('weights_measures','divided monarchies',comparative_source='historical metrology synthesis')
    checks['blind_institution_context']=valid_context(i) and i.evidence_class=='SCHOLARLY_RECONSTRUCTION'
    # Only Scripture-explicit evidence can support wording equivalent to "Scripture says".
    d=EvidenceDecision('blind inference','SCHOLARLY_RECONSTRUCTION','foundation synthesis',confidence=.6)
    checks['blind_evidence_wording']=not can_say_scripture_says(d)

    # Canon-spanning coverage proxy: all macro periods and major imperial contexts are represented.
    checks['canon_spanning_period_coverage']=len(MACRO_PERIODS)>=9
    checks['canon_spanning_polity_coverage']=len(EMPIRE_SEQUENCE)>=6
    checks['social_world_domain_coverage']=len({x['domain'] for x in INSTITUTIONS})>=5

    passed=all(checks.values())
    report={
      'status':'PASS' if passed else 'FAIL',
      'milestone':'BIBLICAL_WORLD_COMPLETE' if passed else None,
      'stage':'Doré Foundation — Biblical World',
      'sections':{'BW-1':'PASS' if checks['bw1_entity_complete'] else 'FAIL','BW-2':'PASS' if checks['bw2_geography_complete'] else 'FAIL','BW-3':'PASS' if checks['bw3_chronology_registry'] else 'FAIL','BW-4':'PASS' if checks['bw4_polity_registry'] else 'FAIL','BW-5':'PASS' if checks['bw5_institutions_registry'] else 'FAIL','BW-6':'PASS' if checks['bw6_evidence_registry'] else 'FAIL'},
      'checks':checks,
      'foundation_counts':{'macro_periods':len(MACRO_PERIODS),'imperial_contexts':len(EMPIRE_SEQUENCE),'institutions':len(INSTITUTIONS)},
      'note':'Foundation completion is not researcher graduation; later historical/textual/theological research education may refine scholarly reconstructions.'
    }
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not passed:sys.exit(1)
if __name__=='__main__':main()
