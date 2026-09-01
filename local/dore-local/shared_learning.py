#!/usr/bin/env python3
"""Doré shared-learning gate: synchronize verified knowledge, not raw memory."""
from __future__ import annotations
import json,os,re
from datetime import datetime,timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();STORE=HOME/'coordination'/'shared-learning.jsonl'
def now():return datetime.now(timezone.utc).isoformat()
def relevant(artifact,goal):
    terms=[x.lower() for x in re.findall(r'[A-Za-z0-9@._:+/-]{3,}',str(goal))]
    hay=json.dumps(artifact,ensure_ascii=False).lower();return sum(1 for t in terms if t in hay)>0
def validate(artifact):
    required=['knowledge_id','sources','provenance_preserved'];missing=[x for x in required if x not in artifact]
    return {'ok':not missing and bool(artifact.get('provenance_preserved')),'missing':missing,'experiment_required':bool(artifact.get('experiment_required',True))}
def record(artifact,*,learned_by='dore',status='CANDIDATE',verification=None,parent_goal=None):
    gate=validate(artifact)
    if not gate['ok']:return {'ok':False,'error':'invalid_knowledge_artifact','validation':gate}
    if status in {'VERIFIED','PROMOTED'} and not verification:return {'ok':False,'error':'verification_required_before_promotion'}
    row={'schema':'dore.shared-learning.v1','at':now(),'knowledge_id':artifact['knowledge_id'],'discovered_by':artifact.get('discovered_by') or 'research_executor','learned_by':learned_by,'parent_goal':parent_goal,'relevant':relevant(artifact,parent_goal or ''),'status':status,'verification':verification,'artifact':artifact}
    STORE.parent.mkdir(parents=True,exist_ok=True)
    with STORE.open('a',encoding='utf-8') as f:f.write(json.dumps(row,ensure_ascii=False)+'\n')
    return {'ok':True,'record':row,'path':str(STORE)}
def records():
    if not STORE.exists():return []
    out=[]
    for line in STORE.read_text(encoding='utf-8',errors='replace').splitlines():
        try:out.append(json.loads(line))
        except Exception:pass
    return out
if __name__=='__main__':print(json.dumps({'ok':True,'records':len(records()),'path':str(STORE)},ensure_ascii=False))
