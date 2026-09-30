#!/usr/bin/env python3
"""Audit existing Dawn canonical holdings and emit a removal manifest."""
from pathlib import Path
import json
from dawn_collection_scope import classify
ROOT=Path(__file__).resolve().parents[1]
INDEX=ROOT/'static/dawn-library/canonical-index.json'
OUT=ROOT/'data/dawn-collection-scope-audit.json'

def main():
 data=json.loads(INDEX.read_text(encoding='utf-8'));works=data.get('works') or {};keep=[];remove=[];scopes={}
 for wid,work in works.items():
  row=dict(work);row['workId']=wid;v=classify(row);scopes[v['scope']]=scopes.get(v['scope'],0)+1
  target={'workId':wid,'title':work.get('title'),'authors':work.get('authors') or [],'scope':v['scope'],'reason':v['reason']}
  (keep if v['admit'] else remove).append(target)
 payload={'schema':'dawn.library.collection-scope-audit.v1','rule':'Christian/Biblical religious holdings; Jewish research admitted; other religions excluded.','scanned':len(works),'kept':len(keep),'removeCount':len(remove),'scopeCounts':scopes,'remove':remove}
 OUT.write_text(json.dumps(payload,ensure_ascii=False,indent=2)+'\n',encoding='utf-8');print(json.dumps({k:payload[k] for k in ('scanned','kept','removeCount','scopeCounts')},ensure_ascii=False))
if __name__=='__main__':main()
