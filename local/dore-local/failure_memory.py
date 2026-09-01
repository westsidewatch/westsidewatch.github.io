#!/usr/bin/env python3
"""Durable failure-memory store for Doré autonomous recovery."""
from __future__ import annotations
import hashlib,json,os,re
from datetime import datetime,timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();STORE=HOME/'coordination'/'failure-memory.jsonl'
def now():return datetime.now(timezone.utc).isoformat()
def normalize(text):return re.sub(r'\s+',' ',str(text or '')).strip()[-6000:]
def fingerprint(text):return hashlib.sha256(normalize(text).encode()).hexdigest()
def append(record):
    STORE.parent.mkdir(parents=True,exist_ok=True);row={'schema':'dore.failure-memory.v1','recorded_at':now(),**record};row.setdefault('failure_fingerprint',fingerprint(row.get('failure') or row.get('evidence')))
    with STORE.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return row
def read_all():
    if not STORE.exists():return []
    out=[]
    for line in STORE.read_text(encoding='utf-8',errors='replace').splitlines():
        try:out.append(json.loads(line))
        except Exception:pass
    return out
def find(query,limit=10):
    terms=[x.lower() for x in re.findall(r'[A-Za-z0-9@._:+/-]{3,}',str(query))][:12];hits=[]
    for row in read_all():
        hay=json.dumps(row,ensure_ascii=False).lower();score=sum(1 for t in terms if t in hay)
        if score:hits.append((score,row))
    return [r for _,r in sorted(hits,key=lambda x:-x[0])[:limit]]
def remember_failure(parent_goal,failure,evidence=None,hypothesis=None,resolution=None,verified=False):
    return append({'parent_goal':parent_goal,'failure':normalize(failure),'evidence':evidence,'hypothesis':hypothesis,'resolution':resolution,'verified':bool(verified),'status':'VERIFIED_RESOLUTION' if verified else 'OPEN'})
if __name__=='__main__':print(json.dumps({'ok':True,'records':len(read_all()),'path':str(STORE)},ensure_ascii=False))
