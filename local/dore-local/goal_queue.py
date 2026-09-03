#!/usr/bin/env python3
"""Durable goal queue for the resident Doré driver.

Humans set destination/product intent; the runtime owns continuation. Every goal
keeps canonical identity, parent goal, priority and lifecycle so a repair detour
never replaces the work that caused it.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();STORE=HOME/'runtime'/'goals.json'
def now():return datetime.now(timezone.utc).isoformat()
def load():
 try:return json.loads(STORE.read_text(encoding='utf-8'))
 except Exception:return {'schema':'dore.goal-queue.v1','updated_at':now(),'goals':[]}
def save(data):
 STORE.parent.mkdir(parents=True,exist_ok=True);data['updated_at']=now();t=STORE.with_suffix('.json.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(STORE);return data
def enqueue(goal_id,goal,*,priority='normal',source='runtime',metadata=None):
 data=load();goals=data.setdefault('goals',[])
 for row in goals:
  if row.get('goal_id')==goal_id:
   if row.get('status') in {'PASS','CANCELED'}:return row
   row.update({'goal':goal,'priority':priority,'metadata':{**(row.get('metadata') or {}),**(metadata or {})},'updated_at':now()});save(data);return row
 rank={'high':0,'normal':1,'low':2};row={'goal_id':goal_id,'goal':goal,'priority':priority,'source':source,'status':'PENDING','created_at':now(),'updated_at':now(),'metadata':metadata or {},'history':[{'at':now(),'status':'PENDING'}]};goals.append(row);goals.sort(key=lambda x:(rank.get(x.get('priority'),1),x.get('created_at','')));save(data);return row
def _learning_evidence(row):
 p=HOME/'coordination'/'learning'/(str(row.get('goal_id'))+'.json')
 try:
  evidence=json.loads(p.read_text(encoding='utf-8'))
  return evidence if evidence.get('state')=='RESEARCH_REQUIRED' else None
 except Exception:return None
def _activation_candidate(goals):
 """Return the newest durable peer learning request that has executable evidence.

 A stale ACTIVE product loop must not make a newly-created capability gap
 invisible forever. Only coordination messages with an actual persisted
 RESEARCH_REQUIRED record qualify; this is not a general priority bypass.
 """
 candidates=[]
 for row in goals:
  meta=row.get('metadata') or {}
  if row.get('status')!='PENDING' or meta.get('execution_kind')!='coordination_message':continue
  if not meta.get('requires_reply'):continue
  evidence=_learning_evidence(row)
  if evidence:candidates.append((str(evidence.get('observed_at') or row.get('updated_at') or ''),row,evidence))
 return max(candidates,key=lambda x:x[0]) if candidates else None
def get(goal_id):
 return next((x for x in load().get('goals',[]) if str(x.get('goal_id'))==str(goal_id)),None)
def current():
 data=load()
 goals=data.get('goals',[]);active=next((x for x in goals if x.get('status')=='ACTIVE'),None);activation=_activation_candidate(goals)
 if active and (active.get('metadata') or {}).get('activation_reason')=='DURABLE_RESEARCH_REQUIRED':return active
 if activation and (not active or activation[1].get('goal_id')!=active.get('goal_id')):
  _,candidate,evidence=activation
  if active:
   active['status']='PAUSED';active['updated_at']=now();active.setdefault('history',[]).append({'at':now(),'status':'PAUSED','reason':'LEARNING_ACTIVATION_PREEMPT','preempted_by':candidate.get('goal_id')})
  candidate['status']='ACTIVE';candidate['updated_at']=now();candidate['metadata']={**(candidate.get('metadata') or {}),'activation_reason':'DURABLE_RESEARCH_REQUIRED','learning_evidence_path':str(HOME/'coordination'/'learning'/(str(candidate.get('goal_id'))+'.json'))};candidate.setdefault('history',[]).append({'at':now(),'status':'ACTIVE','reason':'LEARNING_QUEUE_WAKE','research_state':evidence.get('state')});save(data);return candidate
 if active:return active
 pending=next((x for x in data.get('goals',[]) if x.get('status')=='PENDING'),None)
 if pending:
  pending['status']='ACTIVE';pending['updated_at']=now();pending.setdefault('history',[]).append({'at':now(),'status':'ACTIVE'});save(data);return pending
 paused=[x for x in goals if x.get('status')=='PAUSED']
 if paused:
  resumed=max(paused,key=lambda x:str(x.get('updated_at') or ''));resumed['status']='ACTIVE';resumed['updated_at']=now();resumed.setdefault('history',[]).append({'at':now(),'status':'ACTIVE','reason':'RESUME_AFTER_LEARNING'});save(data);return resumed
 return None
def set_status(goal_id,status,**metadata):
 data=load()
 for row in data.get('goals',[]):
  if row.get('goal_id')==goal_id:
   row['status']=status;row['updated_at']=now();row['metadata']={**(row.get('metadata') or {}),**metadata};row.setdefault('history',[]).append({'at':now(),'status':status});save(data);return row
 return None
def ensure_default(goal_id,goal,**metadata):
 row=next((x for x in load().get('goals',[]) if x.get('goal_id')==goal_id),None);return row or enqueue(goal_id,goal,metadata=metadata)
if __name__=='__main__':print(json.dumps({'ok':True,'current':current(),'queue':load()},ensure_ascii=False))
