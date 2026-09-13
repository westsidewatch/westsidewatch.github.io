#!/usr/bin/env python3
"""Doré <-> A2A compatibility adapter v0.6.

Canonical capabilities now enter one durable execution plane after normalization.
The older typed Design control-plane lane remains available as a compatibility lane
until it is consolidated separately.
"""
from __future__ import annotations
import importlib.util,json,os,uuid
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
HERE=Path(__file__).resolve().parent
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

def _load_sibling(name):
 p=HERE/(name+'.py');s=importlib.util.spec_from_file_location('dore_adapter_'+name,p)
 if s is None or s.loader is None:raise RuntimeError('cannot load '+str(p))
 m=importlib.util.module_from_spec(s);s.loader.exec_module(m);return m

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
 for capability_id,handler in resident_design_handlers().items():executor.register_handler(capability_id,handler)
 return build_design_control_plane(registry,executor)

def control_plane():
 global _CONTROL_PLANE
 if _CONTROL_PLANE is None:_CONTROL_PLANE=_build_control_plane()
 return _CONTROL_PLANE

def handle_control_envelope(envelope):
 from dore_core.control_plane.transport import handle_envelope
 return handle_envelope(control_plane(),envelope)

def _required_text(envelope,key):
 value=envelope.get(key)
 if not isinstance(value,str) or not value.strip():raise ValueError('missing_or_invalid_'+key)
 return value.strip()

def canonical_capability(capability_id):
 registry=_load_sibling('capability_registry')
 return registry.get(str(capability_id),include_planned=True)

def handle_universal_envelope(envelope):
 """Execute one canonical capability through durable execution truth."""
 if not isinstance(envelope,dict) or envelope.get('protocol')!='dore.a2a/1':raise ValueError('unsupported_protocol')
 if envelope.get('action','dispatch')!='dispatch':return None
 request_id=_required_text(envelope,'request_id');conversation_id=_required_text(envelope,'conversation_id');session_id=_required_text(envelope,'session_id');consumer_id=_required_text(envelope,'consumer_id');capability_id=_required_text(envelope,'capability_id')
 payload=envelope.get('payload',{})
 if not isinstance(payload,dict):raise ValueError('payload_must_be_object')
 descriptor=canonical_capability(capability_id)
 if descriptor is None:return None
 bindings=_load_sibling('capability_bindings');binding=bindings.get(capability_id)
 route={'ingress':'normalized','identity_authority':'dore-core/runtime/capability-registry.v1.json','binding_authority':'capability_bindings','execution_authority':'a2a_execution_plane'}
 if binding is None:
  return {'protocol':'dore.a2a/1','request_id':request_id,'conversation_id':conversation_id,'session_id':session_id,'consumer_id':consumer_id,'capability_id':capability_id,'status':'failed','error':{'code':'capability_not_callable','message':'canonical capability has no execution binding'},'core_route':route}
 route['execution_binding']=binding.get('kind')
 bus=_load_sibling('capability_bus');production=_load_sibling('production_actions');executor=_load_sibling('a2a_executor');plane=_load_sibling('a2a_execution_plane')
 execution=executor.execute(envelope,descriptor,binding,lambda:bus.call(capability_id,payload,production,caller_product=consumer_id),plane=plane)
 succeeded=bool(execution.get('ok') and execution.get('completion_evidence') and execution.get('execution_status')=='PASS')
 out={'protocol':'dore.a2a/1','request_id':request_id,'conversation_id':conversation_id,'session_id':session_id,'consumer_id':consumer_id,'capability_id':capability_id,'status':'succeeded' if succeeded else 'failed','execution':execution,'result':execution.get('result'),'core_route':route}
 if execution.get('error'):out['error']=execution['error']
 return out

def handle_companion_payload(payload):
 if not isinstance(payload,dict) or payload.get('protocol')!='dore.a2a/1':return None
 capability_id=str(payload.get('capability_id') or '')
 if capability_id and canonical_capability(capability_id) is not None:
  return handle_universal_envelope(payload)
 return handle_control_envelope(payload)

if __name__=='__main__':
 sample=dore_to_a2a_task(source_message_id='self-test',parent_goal='A2A compatibility',state='RESEARCH_QUEUED',body='Find missing capability');print(json.dumps({'ok':validate_task(sample)['ok'],'agent_card':agent_card(),'task':sample},ensure_ascii=False))
