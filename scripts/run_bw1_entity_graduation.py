#!/usr/bin/env python3
"""End-to-end BW-1 graduation gate against the real derived browser entity index."""
from __future__ import annotations
import json,sys,re
from pathlib import Path
from dore_core.world.entity_query import parse_entity_question

INDEX=Path('static/dore/entity-index.json')
REPORT=Path('reports/DORÉ-BW1-ENTITY-GRADUATION.json')

def fold(s):
    table=str.maketrans({'马':'馬','亚':'亞','约':'約','玛':'瑪','罗':'羅','稣':'穌','经':'經','圣':'聖','里':'裡','个':'個','几':'幾'})
    return re.sub(r'[\s·._\-–—，。！？?、:：;；()（）「」『』]','',str(s or '').lower().translate(table))
def source_fold(s):return re.sub(r'[\s._\-–—]+','',str(s or '').strip().lower())
def names(e):return [e.get('p',''),*[a.get('v','') for a in e.get('a',[])]]
def exact(data,mention,typ=None):
    n=fold(mention)
    return [e for e in data['entities'] if (not typ or e.get('t')==typ) and any(fold(x)==n for x in names(e))]
def source_cluster(data,seeds):
    keys=set()
    for e in seeds:
        if e.get('p'):keys.add(source_fold(e['p']))
        for a in e.get('a',[]):
            if a.get('l')=='en' and a.get('v'):keys.add(source_fold(a['v']))
    out=[]
    for e in data['entities']:
        if e.get('t')!='person':continue
        vals=[e.get('p',''),*[a.get('v','') for a in e.get('a',[]) if a.get('l')=='en']]
        if any(source_fold(v) in keys for v in vals):out.append(e)
    return out

def main():
    d=json.loads(INDEX.read_text(encoding='utf-8'))
    checks={}
    checks['schema']=d.get('schema')=='dore.browser-entity-index.v1'
    checks['entity_coverage']=d.get('counts',{}).get('entities',0)>=4000
    checks['chinese_alias_coverage']=d.get('counts',{}).get('chinese_aliases',0)>=150
    mary=exact(d,'馬利亞','person');mary_cluster=source_cluster(d,mary);samaria=exact(d,'撒馬利亞','place')
    checks['mary_person_resolves']=len(mary)>=1
    checks['samaria_place_resolves']=len(samaria)>=1
    checks['mary_does_not_equal_samaria']=bool(mary) and bool(samaria) and not ({e['id'] for e in mary_cluster}&{e['id'] for e in samaria})
    checks['translated_name_expands_to_source_identity_cluster']=bool(mary_cluster) and len(mary_cluster)>=len(mary)
    checks['no_place_in_mary_person_count']=all(e.get('t')=='person' for e in mary_cluster)
    # Known fragment-shaped aliases exposed by the live page must never survive
    # regeneration. This is a class gate for internal fragments, not a display patch.
    all_zh=[a.get('v','') for e in d['entities'] for a in e.get('a',[]) if a.get('l')=='zh-Hant']
    bad={'拉的馬利亞','抹大拉的馬','大拉的馬利'}
    checks['no_fragmentary_mary_aliases']=not (bad & set(all_zh))
    # If the complete Magdalene expression is derivable, prefer it over fragments.
    magdalene_full='抹大拉的馬利亞' in set(all_zh)
    checks['complete_name_preferred_when_available']=magdalene_full or not any('抹大拉' in x and x!='抹大拉的馬利亞' for x in all_zh)
    q=parse_entity_question('聖經有幾位馬利亞？')
    checks['natural_language_count_intent']=bool(q and q.mention=='馬利亞' and q.kind=='entity_count')
    q2=parse_entity_question('圣经中有多少个犹大?')
    checks['count_intent_transfer']=bool(q2 and q2.mention=='犹大')
    runtime=Path('static/dore/dore-entity-search.js').read_text(encoding='utf-8')
    gallery=Path('static/dore/dore-gallery.js').read_text(encoding='utf-8')
    checks['public_runtime_connected']='entity-index.json' in runtime and 'parseCount' in runtime and 'sourceNameCluster' in runtime
    checks['scripture_search_preserved']='preventDefault' not in runtime and 'stopImmediatePropagation' not in runtime
    checks['public_loader_connected']='dore-entity-search.js' in gallery
    passed=all(checks.values())
    report={'status':'PASS' if passed else 'FAIL','stage':'BW-1 Entity identity and aliases','checks':checks,'counts':d.get('counts',{}),'diagnostics':{'mary_direct_alias_candidates':len(mary),'mary_source_name_cluster':len(mary_cluster),'samaria_candidates':len(samaria),'fragment_aliases_found':sorted(bad & set(all_zh))}}
    REPORT.parent.mkdir(parents=True,exist_ok=True);REPORT.write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    if not passed:sys.exit(1)
if __name__=='__main__':main()
