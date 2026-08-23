#!/usr/bin/env python3
"""End-to-end BW-1 graduation gate against the real derived browser entity index."""
from __future__ import annotations
import json,sys
from pathlib import Path
from dore_core.world.entity_query import parse_entity_question

INDEX=Path('static/dore/entity-index.json')
REPORT=Path('reports/DORÉ-BW1-ENTITY-GRADUATION.json')

def fold(s):
    table=str.maketrans({'马':'馬','亚':'亞','约':'約','玛':'瑪','罗':'羅','稣':'穌','经':'經','圣':'聖','里':'裡','个':'個','几':'幾'})
    return ''.join(str(s or '').lower().translate(table).split())

def names(e):return [e.get('p',''),*[a.get('v','') for a in e.get('a',[])]]
def exact(data,mention,typ=None):
    n=fold(mention)
    return [e for e in data['entities'] if (not typ or e.get('t')==typ) and any(fold(x)==n for x in names(e))]

def main():
    d=json.loads(INDEX.read_text(encoding='utf-8'))
    checks={}
    checks['schema']=d.get('schema')=='dore.browser-entity-index.v1'
    checks['entity_coverage']=d.get('counts',{}).get('entities',0)>=4000
    checks['chinese_alias_coverage']=d.get('counts',{}).get('chinese_aliases',0)>=150
    mary=exact(d,'馬利亞','person');samaria=exact(d,'撒馬利亞','place')
    checks['mary_person_resolves']=len(mary)>=2
    checks['samaria_place_resolves']=len(samaria)>=1
    checks['mary_does_not_equal_samaria']=bool(mary) and bool(samaria) and not ({e['id'] for e in mary}&{e['id'] for e in samaria})
    checks['no_place_in_mary_person_count']=all(e.get('t')=='person' for e in mary)
    q=parse_entity_question('聖經有幾位馬利亞？')
    checks['natural_language_count_intent']=bool(q and q.mention=='馬利亞' and q.kind=='entity_count')
    # Blind transfer: the same intent parser must work for a different same-name question.
    q2=parse_entity_question('圣经中有多少个犹大?')
    checks['count_intent_transfer']=bool(q2 and q2.mention=='犹大')
    runtime=Path('static/dore/dore-entity-search.js').read_text(encoding='utf-8')
    gallery=Path('static/dore/dore-gallery.js').read_text(encoding='utf-8')
    checks['public_runtime_connected']='entity-index.json' in runtime and 'parseCount' in runtime
    checks['public_loader_connected']='dore-entity-search.js' in gallery
    passed=all(checks.values())
    report={'status':'PASS' if passed else 'FAIL','stage':'BW-1 Entity identity and aliases','checks':checks,'counts':d.get('counts',{}),'diagnostics':{'mary_candidates':len(mary),'samaria_candidates':len(samaria)}}
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not passed:sys.exit(1)
if __name__=='__main__':main()
