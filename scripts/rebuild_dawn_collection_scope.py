#!/usr/bin/env python3
"""Rebuild existing Dawn public collection through the locked scope gate.

Reads the current canonical index, removes out-of-scope religious works, keeps
Jewish research, then prunes public JSON surfaces by Work ID. This is the
one-shot migration companion to the permanent ingestion/canonical gates.
"""
from __future__ import annotations
from pathlib import Path
import json
from dawn_collection_scope import classify

ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'static/dawn-library/canonical-index.json'
AUDIT=ROOT/'data/dawn-collection-scope-audit.json'
PUBLIC_ROOTS=(ROOT/'static/dawn-library/cover-preview',ROOT/'static/dawn-library/cover-authority',ROOT/'static/dawn-library/surfaces')

def clean(obj,banned:set[str]):
    if isinstance(obj,list):
        return [clean(x,banned) for x in obj if not (isinstance(x,dict) and str(x.get('workId') or x.get('id') or '') in banned)]
    if isinstance(obj,dict):
        return {k:clean(v,banned) for k,v in obj.items() if k not in banned and not (isinstance(v,dict) and str(v.get('workId') or v.get('id') or '') in banned)}
    return obj

def main():
    index=json.loads(INDEX.read_text(encoding='utf-8'));works=index.get('works') or {};kept={};removed=[];scopes={}
    for wid,work in works.items():
        row=dict(work);row['workId']=wid;verdict=classify(row);scopes[verdict['scope']]=scopes.get(verdict['scope'],0)+1
        if verdict['admit']:
            row['collectionScope']=verdict['scope'];kept[wid]=row
        else:
            removed.append({'workId':wid,'title':work.get('title'),'authors':work.get('authors') or [],'reason':verdict['reason']})
    banned={x['workId'] for x in removed};index['schema']='dawn.library.canonical-index.v2';index['collectionPolicy']='Christian/Biblical religious holdings; Jewish research admitted; other religions excluded.';index['excludedByCollectionScope']=len(removed);index['works']=dict(sorted(kept.items()));index['workCount']=len(kept);INDEX.write_text(json.dumps(index,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8')
    touched=[]
    for root in PUBLIC_ROOTS:
        if not root.exists():continue
        for path in root.rglob('*.json'):
            try:old=json.loads(path.read_text(encoding='utf-8'))
            except Exception:continue
            new=clean(old,banned)
            if new!=old:
                path.write_text(json.dumps(new,ensure_ascii=False,separators=(',',':'))+'\n',encoding='utf-8');touched.append(str(path.relative_to(ROOT)))
    audit={'schema':'dawn.library.collection-scope-audit.v2','scanned':len(works),'kept':len(kept),'removed':len(removed),'scopeCounts':scopes,'publicFilesChanged':len(touched),'changedFiles':touched,'remove':removed};AUDIT.write_text(json.dumps(audit,ensure_ascii=False,indent=2)+'\n',encoding='utf-8')
    print(json.dumps({k:audit[k] for k in ('scanned','kept','removed','scopeCounts','publicFilesChanged')},ensure_ascii=False))
if __name__=='__main__':main()
