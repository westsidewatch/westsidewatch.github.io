#!/usr/bin/env python3
"""Bind ChatGPT peer-research replies to Doré durable research jobs.

A queued peer request is not knowledge. This bridge scans the existing durable
ChatGPT->Doré mailbox for a provenance-bearing dore.knowledge-artifact.v1 tied
to research_id, validates it, then and only then advances the matching job to
KNOWLEDGE_RETURNED. The user is never the message relay.
"""
from __future__ import annotations
import json, os, sys
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path(__file__).resolve().parents[2])).expanduser();RESEARCH=HOME/'coordination'/'research';INBOX=HOME/'coordination'/'chatgpt-to-dore.jsonl'
def now():return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:return default
def atomic_json(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def messages():
    if not INBOX.exists():return []
    out=[]
    for line in INBOX.read_text(encoding='utf-8',errors='replace').splitlines():
        try:out.append(json.loads(line))
        except Exception:pass
    return out
def body_payload(msg):
    body=msg.get('body')
    if isinstance(body,dict):return body
    if isinstance(body,str):
        try:return json.loads(body)
        except Exception:return None
    return None
def validate_artifact(a,research_id):
    if not isinstance(a,dict):return False,'artifact_not_object'
    if a.get('schema')!='dore.knowledge-artifact.v1':return False,'wrong_schema'
    if str(a.get('research_id'))!=str(research_id):return False,'research_id_mismatch'
    if not a.get('sources'):return False,'sources_required'
    if not a.get('provenance_preserved'):return False,'provenance_required'
    return True,None
def consume(job_path):
    p=Path(job_path);job=read_json(p,{}) or {};rid=job.get('research_id')
    if not rid:return {'ok':False,'error':'research_id_missing'}
    if job.get('state')!='PEER_RESEARCH_QUEUED':return {'ok':True,'changed':False,'state':job.get('state')}
    matches=[]
    for msg in messages():
        meta=msg.get('metadata') or {};payload=body_payload(msg)
        if str(meta.get('research_id') or (payload or {}).get('research_id') or '')!=str(rid):continue
        artifact=(payload or {}).get('knowledge_artifact') if isinstance(payload,dict) else None
        if artifact is None and isinstance(payload,dict) and payload.get('schema')=='dore.knowledge-artifact.v1':artifact=payload
        valid,error=validate_artifact(artifact,rid);matches.append({'message_id':msg.get('message_id'),'valid':valid,'error':error,'artifact':artifact})
    valid=next((x for x in reversed(matches) if x['valid']),None)
    if not valid:return {'ok':True,'changed':False,'state':'PEER_RESEARCH_QUEUED','research_id':rid,'observed_replies':len(matches),'invalid_replies':[{'message_id':x['message_id'],'error':x['error']} for x in matches if not x['valid']]}
    history=list(job.get('history') or []);history.append({'at':now(),'state':'KNOWLEDGE_RETURNED','source':'peer_research','message_id':valid['message_id']})
    job={**job,'state':'KNOWLEDGE_RETURNED','updated_at':now(),'knowledge_artifact':valid['artifact'],'peer_reply_message_id':valid['message_id'],'history':history};atomic_json(p,job)
    return {'ok':True,'changed':True,'state':'KNOWLEDGE_RETURNED','research_id':rid,'message_id':valid['message_id']}
if __name__=='__main__':
    if len(sys.argv)!=2:print(json.dumps({'ok':False,'error':'usage: peer_research_bridge.py JOB.json'}));raise SystemExit(2)
    out=consume(sys.argv[1]);print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 3)
