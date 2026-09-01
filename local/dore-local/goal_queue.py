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
def current():
 data=load()
 active=next((x for x in data.get('goals',[]) if x.get('status')=='ACTIVE'),None)
 if active:return active
 pending=next((x for x in data.get('goals',[]) if x.get('status')=='PENDING'),None)
 if pending:
  pending['status']='ACTIVE';pending['updated_at']=now();pending.setdefault('history',[]).append({'at':now(),'status':'ACTIVE'});save(data);return pending
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
