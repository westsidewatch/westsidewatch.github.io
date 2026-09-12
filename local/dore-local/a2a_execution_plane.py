#!/usr/bin/env python3
"""Durable A2A execution lifecycle for Doré local workers.

This module is intentionally independent from transport. Delivery proves that a
message arrived; this plane proves that work was claimed, executed, produced an
artifact, verified, and only then completed.
"""
from __future__ import annotations
import hashlib,json,os,socket
from datetime import datetime,timezone,timedelta
from pathlib import Path

VERSION='dore.a2a-execution-plane.v1'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=HOME/'a2a-execution'
TASKS=ROOT/'tasks';EVENTS=ROOT/'events.jsonl'
DEFAULT_LEASE_SECONDS=max(30,int(os.environ.get('DORE_A2A_LEASE_SECONDS','300')))
TERMINAL={'PASS','FAIL','REJECTED'}
ORDER=('SUBMITTED','ACCEPTED','CLAIMED','RUNNING','ARTIFACT_PRODUCED','VERIFIED','PASS')

def now():return datetime.now(timezone.utc).isoformat()
def _parse(s):return datetime.fromisoformat(str(s).replace('Z','+00:00'))
def _atomic(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8');tmp.replace(path)
def _append(value):
 EVENTS.parent.mkdir(parents=True,exist_ok=True)
 with EVENTS.open('a',encoding='utf-8') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True)+'\n')
def _task_path(task_id):return TASKS/(str(task_id)+'.json')
def _digest(obj):return hashlib.sha256(json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode()).hexdigest()
def worker_id():return os.environ.get('DORE_A2A_WORKER_ID') or f'{socket.gethostname()}:{os.getpid()}'

def read(task_id):
 p=_task_path(task_id)
 return json.loads(p.read_text(encoding='utf-8')) if p.exists() else None

def register(message,delivery=None):
 task_id=str(message.get('message_id') or '')
 if not task_id:raise ValueError('task_id_required')
 existing=read(task_id)
 if existing:return existing
 d=delivery or message.get('_delivery') or {}
 t={
  'schema':'dore.a2a-task.v1','execution_plane':VERSION,'task_id':task_id,
  'message_id':task_id,'kind':message.get('kind'),'related_goal':message.get('related_goal'),
  'content_sha256':d.get('content_sha256') or _digest({k:v for k,v in message.items() if k!='_delivery'}),
  'source_commit':d.get('source_commit'),'source_ref':d.get('source_ref'),
  'status':'ACCEPTED','submitted_at':d.get('accepted_at') or now(),'accepted_at':now(),
  'lease':None,'artifact':None,'verification':None,'result':None,
 }
 _atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':'SUBMITTED','to':'ACCEPTED'})
 return t

def _lease_live(lease):
 if not lease:return False
 try:return _parse(lease.get('expires_at'))>datetime.now(timezone.utc)
 except Exception:return False

def claim(task_id,consumer=None,lease_seconds=DEFAULT_LEASE_SECONDS):
 t=read(task_id)
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 if t['status'] in TERMINAL:return {'ok':False,'code':'TASK_TERMINAL','task':t}
 owner=consumer or worker_id();lease=t.get('lease')
 if _lease_live(lease) and lease.get('owner')!=owner:
  return {'ok':False,'code':'TASK_LEASED','owner':lease.get('owner'),'expires_at':lease.get('expires_at'),'task':t}
 expires=datetime.now(timezone.utc)+timedelta(seconds=max(30,int(lease_seconds)))
 previous=t['status'];t['lease']={'owner':owner,'claimed_at':now(),'expires_at':expires.isoformat()};t['status']='CLAIMED';t['claimed_at']=now();_atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':previous,'to':'CLAIMED','owner':owner,'expires_at':t['lease']['expires_at']});return {'ok':True,'code':'TASK_CLAIMED','task':t}

def heartbeat(task_id,consumer=None,lease_seconds=DEFAULT_LEASE_SECONDS):
 t=read(task_id);owner=consumer or worker_id()
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 lease=t.get('lease') or {}
 if lease.get('owner')!=owner:return {'ok':False,'code':'LEASE_OWNER_MISMATCH','task':t}
 lease['expires_at']=(datetime.now(timezone.utc)+timedelta(seconds=max(30,int(lease_seconds)))).isoformat();lease['heartbeat_at']=now();t['lease']=lease;_atomic(_task_path(task_id),t);return {'ok':True,'code':'LEASE_RENEWED','task':t}

def transition(task_id,status,*,consumer=None,result=None):
 if status not in {'RUNNING','FAIL'}:raise ValueError('unsupported_transition:'+status)
 t=read(task_id);owner=consumer or worker_id()
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 lease=t.get('lease') or {}
 if lease.get('owner')!=owner or not _lease_live(lease):return {'ok':False,'code':'LEASE_REQUIRED','task':t}
 previous=t['status'];t['status']=status;t['updated_at']=now()
 if status=='RUNNING':t['started_at']=t.get('started_at') or now()
 if status=='FAIL':t['failed_at']=now();t['result']=result;t['lease']=None
 _atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':previous,'to':status,'owner':owner});return {'ok':True,'task':t}

def record_artifact(task_id,artifact,*,consumer=None):
 t=read(task_id);owner=consumer or worker_id()
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 lease=t.get('lease') or {}
 if lease.get('owner')!=owner or not _lease_live(lease):return {'ok':False,'code':'LEASE_REQUIRED','task':t}
 if t['status'] not in {'RUNNING','CLAIMED'}:return {'ok':False,'code':'TASK_NOT_RUNNING','task':t}
 a=dict(artifact or {});a.setdefault('recorded_at',now());a.setdefault('sha256',_digest(a));previous=t['status'];t['artifact']=a;t['status']='ARTIFACT_PRODUCED';_atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':previous,'to':'ARTIFACT_PRODUCED','artifact_sha256':a['sha256']});return {'ok':True,'task':t}

def verify(task_id,verification,*,consumer=None):
 t=read(task_id);owner=consumer or worker_id()
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 lease=t.get('lease') or {}
 if lease.get('owner')!=owner or not _lease_live(lease):return {'ok':False,'code':'LEASE_REQUIRED','task':t}
 if t['status']!='ARTIFACT_PRODUCED' or not t.get('artifact'):return {'ok':False,'code':'ARTIFACT_REQUIRED','task':t}
 v=dict(verification or {});v['verified_at']=now();passed=bool(v.get('ok'));t['verification']=v;previous=t['status'];t['status']='VERIFIED' if passed else 'FAIL'
 if not passed:t['failed_at']=now();t['lease']=None
 _atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':previous,'to':t['status'],'verification_ok':passed});return {'ok':passed,'task':t}

def complete(task_id,result=None,*,consumer=None):
 t=read(task_id);owner=consumer or worker_id()
 if not t:raise FileNotFoundError('execution_task_missing:'+str(task_id))
 lease=t.get('lease') or {}
 if lease.get('owner')!=owner or not _lease_live(lease):return {'ok':False,'code':'LEASE_REQUIRED','task':t}
 if t['status']!='VERIFIED' or not (t.get('verification') or {}).get('ok') or not t.get('artifact'):
  return {'ok':False,'code':'VERIFIED_ARTIFACT_REQUIRED','task':t}
 previous=t['status'];t['status']='PASS';t['completed_at']=now();t['result']=result;t['lease']=None;_atomic(_task_path(task_id),t);_append({'at':now(),'task_id':task_id,'from':previous,'to':'PASS'});return {'ok':True,'code':'TASK_COMPLETED','task':t}

def status(task_id):
 t=read(task_id)
 if not t:return {'ok':False,'code':'TASK_NOT_FOUND','task_id':task_id}
 return {'ok':True,'task':t,'completion_evidence':bool(t.get('status')=='PASS' and t.get('artifact') and (t.get('verification') or {}).get('ok'))}

if __name__=='__main__':
 import argparse
 p=argparse.ArgumentParser();p.add_argument('task_id');args=p.parse_args();print(json.dumps(status(args.task_id),ensure_ascii=False))
