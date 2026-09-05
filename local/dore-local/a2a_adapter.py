#!/usr/bin/env python3
"""Doré <-> A2A compatibility adapter v0.4.

The typed ``dore.a2a/1`` control plane is the production seam used by the
browser Companion. Synthetic visual handlers remain available for non-resident
capabilities, while Design is promoted to the resident Doré Design service.
"""
from __future__ import annotations
import json, os, uuid
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
AGENT_CARD=ROOT/'dore-design'/'knowledge-lab'/'a2a'/'agent-card.json'
STATE_MAP={'RECEIVED':'submitted','RUNNING':'working','LEARNING':'working','GAP_DETECTED':'working','RESEARCH_REQUIRED':'working','RESEARCH_QUEUED':'working','RESEARCHING':'working','PEER_RESEARCH_QUEUED':'working','KNOWLEDGE_RETURNED':'working','EXPERIMENTING':'working','VERIFYING':'working','VERIFIED':'working','PROMOTED':'working','RESUME_PARENT':'working','PASS':'completed','FAIL':'failed','HUMAN_GATE':'input-required','CANCELED':'canceled'}
def now():return datetime.now(timezone.utc).isoformat()
def agent_card():return json.loads(AGENT_CARD.read_text(encoding='utf-8'))
def task_id(source_message_id):return 'task-'+str(source_message_id)
def context_id(parent_goal,parent_message_id):return 'ctx-'+str(parent_message_id or abs(hash(parent_goal)))
def status(state,message=None):return {'state':STATE_MAP.get(str(state),'working'),'timestamp':now(),**({'message':message} if message else {})}
def message(role,text,*,message_id=None,metadata=None):return {'kind':'message','messageId':message_id or str(uuid.uuid4()),'role':role,'parts':[{'kind':'text','text':str(text)}],'metadata':metadata or {}}
def artifact(name,data,*,artifact_id=None,metadata=None):return {'artifactId':artifact_id or str(uuid.uuid4()),'name':name,'parts':[{'kind':'data','data':data}],'metadata':metadata or {}}
def dore_to_a2a_task(*,source_message_id,parent_goal,state,body=None,artifacts=None,metadata=None):
 tid=task_id(source_message_id);ctx=context_id(parent_goal,source_message_id);s=status(state)
 return {'kind':'task','id':tid,'contextId':ctx,'status':s,'history':[s],'artifacts':list(artifacts or []),'metadata':{'doreSourceMessageId':source_message_id,'parentGoal':parent_goal,**(metadata or {})},**({'messages':[message('agent',body,metadata={'source':'dore'})]} if body else {})}
def append_transition(task,state,detail=None):
 h=list(task.get('history') or []);s=status(state,message=message('agent',detail,metadata={'doreState':state}) if detail else None);h.append(s);return {**task,'status':s,'history':h}
def knowledge_artifact_to_a2a(knowledge):return artifact('Doré Knowledge Artifact',knowledge,artifact_id=str(knowledge.get('knowledge_id') or uuid.uuid4()),metadata={'type':'dore.knowledge-artifact','verified':bool(knowledge.get('verified'))})
def validate_task(task):
 missing=sorted({'kind','id','contextId','status'}-set(task));return {'ok':not missing and task.get('kind')=='task','missing':missing,'kind_ok':task.get('kind')=='task','state':(task.get('status') or {}).get('state')}

_CONTROL_PLANE=None

def _build_control_plane():
 from dore_core.capabilities.executor import CapabilityExecutor
 from dore_core.capabilities.registry import default_registry
 from dore_core.capabilities.runtime import LazyCapabilityRuntime
 from dore_core.capabilities.synthetic_visual import synthetic_visual_handlers
 from dore_core.capabilities.resident_design import resident_design_handlers
 from dore_core.control_plane.runtime import build_design_control_plane
 registry=default_registry();runtime=LazyCapabilityRuntime(registry,root=str(ROOT));executor=CapabilityExecutor(registry,runtime)
 for capability_id,handler in synthetic_visual_handlers().items():executor.register_handler(capability_id,handler)
 # Resident handlers intentionally override the synthetic Design test doubles.
 for capability_id,handler in resident_design_handlers().items():executor.register_handler(capability_id,handler)
 return build_design_control_plane(registry,executor)

def control_plane():
 global _CONTROL_PLANE
 if _CONTROL_PLANE is None:_CONTROL_PLANE=_build_control_plane()
 return _CONTROL_PLANE

def handle_control_envelope(envelope):
 from dore_core.control_plane.transport import handle_envelope
 return handle_envelope(control_plane(),envelope)

def handle_companion_payload(payload):
 if isinstance(payload,dict) and payload.get('protocol')=='dore.a2a/1':return handle_control_envelope(payload)
 return None

if __name__=='__main__':
 sample=dore_to_a2a_task(source_message_id='self-test',parent_goal='A2A compatibility',state='RESEARCH_QUEUED',body='Find missing capability');print(json.dumps({'ok':validate_task(sample)['ok'],'agent_card':agent_card(),'task':sample},ensure_ascii=False))
