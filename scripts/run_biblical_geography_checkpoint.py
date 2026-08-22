#!/usr/bin/env python3
"""Biblical Geography educational checkpoint against pinned OpenBible data."""
from __future__ import annotations
import json,os
from pathlib import Path
from dore_core.world.geography import iter_ancient_places
SNAPSHOT='7eb18a5ee62f27b9b93bd6689ea272d76dd23b8f'
DEFAULT=Path('.cache/openbible/ancient.jsonl');OUT=Path('reports/DORÉ-BIBLICAL-GEOGRAPHY.json')
def main():
    path=Path(os.environ.get('DORE_OPENBIBLE_ANCIENT',str(DEFAULT)))
    places=list(iter_ancient_places(path.read_text(encoding='utf-8')))
    candidate_places=[p for p in places if p.candidates]
    multi=[p for p in places if len(p.candidates)>1]
    geocoded=[c for p in places for c in p.candidates if c.lon is not None and c.lat is not None]
    refs=sum(len(p.canonical_refs) for p in places)
    linked=sum(1 for p in places if p.tipnr_source_id)
    failures=[]
    if len(places)<1000:failures.append(f'too_few_ancient_places:{len(places)}')
    if len(candidate_places)<500:failures.append(f'too_few_identified_places:{len(candidate_places)}')
    if len(geocoded)<500:failures.append(f'too_few_geocoded_candidates:{len(geocoded)}')
    if refs<2000:failures.append(f'too_few_scripture_attestations:{refs}')
    if linked<500:failures.append(f'too_few_tipnr_crosswalks:{linked}')
    bad_coord=[c for c in geocoded if not (-180<=c.lon<=180 and -90<=c.lat<=90)]
    if bad_coord:failures.append(f'invalid_coordinates:{len(bad_coord)}')
    bad_conf=[c for p in places for c in p.candidates if not (0<=c.confidence<=1)]
    if bad_conf:failures.append(f'invalid_confidence:{len(bad_conf)}')
    # Ambiguity must remain represented rather than being silently reduced to one site.
    if not multi:failures.append('no_competing_identifications_preserved')
    sample=[]
    for name in ['Jerusalem','Bethlehem','Abana','Abarim']:
        rows=[p for p in places if p.friendly_id.casefold()==name.casefold()]
        if rows:
            p=rows[0];sample.append({'ancient_id':p.source_id,'name':p.friendly_id,'canonical_ref_count':len(p.canonical_refs),'tipnr_source_id':p.tipnr_source_id,'types':list(p.types),'modern_candidates':[{'modern_id':c.modern_id,'description':c.description,'confidence':c.confidence,'lon':c.lon,'lat':c.lat,'type':c.geometry_type} for c in p.candidates[:4]]})
    result={'schema':'dore.biblical-geography-checkpoint.v0.1','status':'PASS' if not failures else 'FAIL','checkpoint':'BIBLICAL_GEOGRAPHY_FOUNDATION','milestone':False,'source':{'id':'openbibleinfo/Bible-Geocoding-Data','snapshot':SNAPSHOT,'license':'CC BY 4.0','raw_source_redistributed':False},'counts':{'ancient_places':len(places),'places_with_modern_candidates':len(candidate_places),'competing_identification_places':len(multi),'geocoded_candidates':len(geocoded),'scripture_attestations':refs,'tipnr_crosswalks':linked},'evidence_separation':{'ancient_place_attestation':'SCRIPTURE_EXPLICIT','ancient_to_modern_identification':'SCHOLARLY_RECONSTRUCTION','modern_coordinate':'GEOSPATIAL_OBSERVATION'},'failures':failures,'samples':sample,'boundary':'Coordinates describe modern candidate locations; they are never promoted to biblical-location certainty. Competing identifications remain visible.','product_relevance':{'bible_search':'place search and candidate geography foundation','subtitle_proofreader':'place-name identity and contextual disambiguation foundation'}}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
