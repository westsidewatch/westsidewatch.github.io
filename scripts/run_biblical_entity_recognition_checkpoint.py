#!/usr/bin/env python3
"""Run Doré's first Biblical World educational checkpoint against pinned TIPNR."""
from __future__ import annotations
import json,os
from collections import Counter,defaultdict
from pathlib import Path
from dore_core.world.model import validate_entity
from dore_core.world.tipnr import iter_tipnr_records,to_world_entity

SNAPSHOT='efe428a0047bf7b9c3ce2624f60c252c6e435945'
DEFAULT=Path('.cache/stepbible/Proper Nouns/TIPNR - Translators Individualised Proper Names with all References - STEPBible.org CC BY.txt')
OUT=Path('reports/DORÉ-BIBLICAL-ENTITY-RECOGNITION.json')

def main():
    path=Path(os.environ.get('DORE_TIPNR_FILE',str(DEFAULT)))
    text=path.read_text(encoding='utf-8-sig')
    records=list(iter_tipnr_records(text))
    entities=[to_world_entity(r,SNAPSHOT) for r in records if r.category in {'PERSON','PLACE'}]
    category_counts=Counter(r.category for r in records)
    label_entities=defaultdict(list)
    for e in entities:label_entities[e.preferred_label.casefold()].append(e.entity_id)
    ambiguous_labels={k:v for k,v in label_entities.items() if len(v)>1}
    validation=[]
    for e in entities:validation.extend(validate_entity(e).errors)
    ids=[e.entity_id for e in entities]
    alias_count=sum(len(e.aliases) for e in entities)
    ref_attestations=sum(sum(1 for a in e.attestations if a.locator.startswith('bible.ref.')) for e in entities)

    def find(label,category=None):
        return [r for r in records if r.label.casefold()==label.casefold() and (category is None or r.category==category)]
    moses=find('Moses','PERSON');aaron=find('Aaron','PERSON');akeldama=find('Akeldama','PLACE')
    moses_alias_langs=sorted({a.language for r in moses for a in r.aliases})
    failures=[]
    if len(entities)<1000:failures.append(f'too_few_entities:{len(entities)}')
    if category_counts['PERSON']<500:failures.append(f'too_few_people:{category_counts["PERSON"]}')
    if category_counts['PLACE']<300:failures.append(f'too_few_places:{category_counts["PLACE"]}')
    if len(ids)!=len(set(ids)):failures.append('unstable_or_duplicate_entity_ids')
    if validation:failures.append(f'entity_validation_errors:{len(validation)}')
    if not ambiguous_labels:failures.append('same_surface_disambiguation_not_observed')
    if not moses or not {'he','grc'} <= set(moses_alias_langs):failures.append('moses_cross_language_aliases_missing')
    if not aaron or max((len(r.canonical_refs) for r in aaron),default=0)<100:failures.append('aaron_reference_coverage_too_low')
    if not akeldama:failures.append('akeldama_place_identity_missing')
    if '@Article=' not in text:failures.append('source_fixture_missing_editorial_prose')
    # Reader never emits prose summaries as aliases or attestations.
    if any(a.value.startswith('@') for e in entities for a in e.aliases):failures.append('editorial_prose_leaked_into_aliases')

    samples=[]
    for label,cat in [('Moses','PERSON'),('Aaron','PERSON'),('Akeldama','PLACE')]:
        rows=find(label,cat)
        if rows:
            r=rows[0];samples.append({'label':r.label,'category':r.category,'source_unique_name':r.source_unique_name,'aliases':[{'value':a.value,'language':a.language,'kind':a.kind} for a in r.aliases[:8]],'canonical_ref_count':len(r.canonical_refs),'canonical_ref_sample':list(r.canonical_refs[:8])})
    result={
      'schema':'dore.biblical-entity-recognition-checkpoint.v0.1',
      'status':'PASS' if not failures else 'FAIL',
      'checkpoint':'BIBLICAL_ENTITY_RECOGNITION',
      'milestone':False,
      'source':{'id':'STEPBible/TIPNR','snapshot':SNAPSHOT,'license':'CC BY 4.0','raw_source_redistributed':False},
      'counts':{'records':len(records),'entities':len(entities),'people':category_counts['PERSON'],'places':category_counts['PLACE'],'other':category_counts['OTHER'],'aliases':alias_count,'scripture_attestations':ref_attestations,'ambiguous_surface_labels':len(ambiguous_labels)},
      'capabilities_demonstrated':['individualised_same-name_entities','english_aliases','hebrew_aliases','greek_aliases','canonical_attestations','source_provenance','editorial_ai_prose_exclusion'],
      'validation_errors':validation[:100],
      'failures':failures,
      'samples':samples,
      'product_relevance':{'bible_search':'entity/person/place query foundation','subtitle_proofreader':'proper-name and transliteration disambiguation foundation'},
      'boundary':'This checkpoint recognises evidence-bearing biblical proper-name identities. It does not yet graduate geography, chronology, historical reconstruction, or Biblical World as a whole.'}
    OUT.parent.mkdir(parents=True,exist_ok=True);OUT.write_text(json.dumps(result,ensure_ascii=False,indent=2,sort_keys=True)+'\n',encoding='utf-8');print(json.dumps(result,ensure_ascii=False,indent=2))
    if result['status']!='PASS':raise SystemExit(1)
if __name__=='__main__':main()
