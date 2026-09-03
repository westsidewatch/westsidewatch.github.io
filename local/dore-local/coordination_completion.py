#!/usr/bin/env python3
"""Emit an evidence-bound terminal receipt after resident learning recovery."""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt

HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();STATE=HOME/'coordination'/'worker-state.json'
def now():return datetime.now(timezone.utc).isoformat()
def atomic_json(p,v):
 p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix('.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def complete(ctx,job,driver_result):
 meta=ctx.get('metadata') or {};msg=meta.get('message') or {};mid=str(msg.get('message_id') or '')
 if not mid or mid!=str(ctx.get('goal_id')):return {'ok':False,'error':'source_message_binding_failed'}
 dispatched=((driver_result.get('result') or {}).get('coordination_goal') or {}).get('result')
 if not isinstance(dispatched,dict) or not dispatched.get('ok') or dispatched.get('reviewed_message_id')!=mid:return {'ok':False,'error':'semantic_completion_binding_failed','source_message_id':mid,'dispatch_result':dispatched}
 chain=['RESEARCH_QUEUED','RESEARCHING','KNOWLEDGE_RETURNED','EXPERIMENTING','VERIFIED','PROMOTED','RESUME_PARENT']
 history=[x.get('state') for x in (job.get('history') or [])];missing=[x for x in chain if x not in history]
 if missing:return {'ok':False,'error':'learning_chain_incomplete','missing':missing,'history':history}
 payload={'source_message_id':mid,'task_status':'PASS','terminal':True,'transport':'PASS','execution':'PASS','result':{**dispatched,'state':'PASS','autonomous_learning_activation':{'research_id':job.get('research_id'),'states':history,'parent_goal_preserved':True,'original_message_redispatched':True},'canonical_completion':True}}
 send_to_chatgpt('Doré autonomous completion: '+str(msg.get('subject') or '')[:100],json.dumps(payload,ensure_ascii=False),requires_reply=False,priority='high',related_goal=ctx.get('goal'),evidence_refs=['learning-activation-bridge-v1','semantic-result-binding','research-job:'+str(job.get('research_id')),'source-message:'+mid],thread_id=msg.get('thread_id'),message_id='result-'+mid,metadata={'source_message_id':mid,'task_status':'PASS','terminal':True,'semantic_bound':True})
 try:state=json.loads(STATE.read_text(encoding='utf-8'))
 except Exception:state={}
 task=state.setdefault('tasks',{}).setdefault(mid,{});task.update({'status':'PASS','terminal':True,'completed_at':now(),'updated_at':now(),'result':payload['result']});state['last_task_id']=mid;state['last_task_status']='PASS';state['last_success_message_id']=mid;atomic_json(STATE,state)
 return {'ok':True,'source_message_id':mid,'research_id':job.get('research_id'),'terminal':True}
