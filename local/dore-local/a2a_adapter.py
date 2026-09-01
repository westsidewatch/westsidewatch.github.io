#!/usr/bin/env python3
"""Doré <-> A2A compatibility adapter v0.1.

Keeps dore.mail as the proven transport while giving Doré canonical A2A-shaped
Task/Message/Artifact/status objects. This is deliberately transport-neutral;
an HTTP server can be added later without rewriting Doré task semantics.
"""
from __future__ import annotations
import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
AGENT_CARD=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'agent-card.json'
STATE_MAP={
 'RECEIVED':'submitted','RUNNING':'working','LEARNING':'working','GAP_DETECTED':'working',
 'RESEARCH_REQUIRED':'working','RESEARCH_QUEUED':'working','RESEARCHING':'working',
 'PEER_RESEARCH_QUEUED':'working','KNOWLEDGE_RETURNED':'working','EXPERIMENTING':'working',
 'VERIFYING':'working','VERIFIED':'working','PROMOTED':'working','RESUME_PARENT':'working',
 'PASS':'completed','FAIL':'failed','HUMAN_GATE':'input-required','CANCELED':'canceled'
}

def now():return datetime.now(timezone.utc).isoformat()
def agent_card():return json.loads(AGENT_CARD.read_text(encoding='utf-8'))
def task_id(source_message_id):return 'task-'+str(source_message_id)
def context_id(parent_goal,parent_message_id):return 'ctx-'+str(parent_message_id or abs(hash(parent_goal)))
def status(state,message=None):
    return {'state':STATE_MAP.get(str(state),'working'),'timestamp':now(),**({'message':message} if message else {})}
def message(role,text,*,message_id=None,metadata=None):
    return {'kind':'message','messageId':message_id or str(uuid.uuid4()),'role':role,'parts':[{'kind':'text','text':str(text)}],'metadata':metadata or {}}
def artifact(name,data,*,artifact_id=None,metadata=None):
    return {'artifactId':artifact_id or str(uuid.uuid4()),'name':name,'parts':[{'kind':'data','data':data}],'metadata':metadata or {}}
def dore_to_a2a_task(*,source_message_id,parent_goal,state,body=None,artifacts=None,metadata=None):
    tid=task_id(source_message_id);ctx=context_id(parent_goal,source_message_id)
    history=[status(state)]
    return {'kind':'task','id':tid,'contextId':ctx,'status':history[-1],'history':history,'artifacts':list(artifacts or []),'metadata':{'doreSourceMessageId':source_message_id,'parentGoal':parent_goal,**(metadata or {})},**({'messages':[message('agent',body,metadata={'source':'dore'})]} if body else {})}
def append_transition(task,state,detail=None):
    h=list(task.get('history') or []);s=status(state,message=message('agent',detail,metadata={'doreState':state}) if detail else None);h.append(s);task={**task,'status':s,'history':h};return task
def knowledge_artifact_to_a2a(knowledge):
    return artifact('Doré Knowledge Artifact',knowledge,artifact_id=str(knowledge.get('knowledge_id') or uuid.uuid4()),metadata={'type':'dore.knowledge-artifact','verified':bool(knowledge.get('verified'))})
def validate_task(task):
    required={'kind','id','contextId','status'};missing=sorted(required-set(task));return {'ok':not missing,'missing':missing,'kind_ok':task.get('kind')=='task','state':(task.get('status') or {}).get('state')}

if __name__=='__main__':
    sample=dore_to_a2a_task(source_message_id='self-test',parent_goal='A2A compatibility',state='RESEARCH_QUEUED',body='Find missing capability')
    print(json.dumps({'ok':validate_task(sample)['ok'],'agent_card':agent_card(),'task':sample},ensure_ascii=False))
