#!/usr/bin/env python3
"""Acceptance for 1C/6 stage 2 consumer recovery unification."""
from __future__ import annotations
import importlib,os,tempfile,time
from pathlib import Path

HERE=Path(__file__).resolve().parent
import sys
if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))


def fresh_plane(home):
 os.environ['DORE_LOCAL_HOME']=str(home)
 import a2a_execution_plane
 return importlib.reload(a2a_execution_plane)


def envelope(request_id):
 return {'request_id':request_id,'conversation_id':'acceptance','session_id':'s1','consumer_id':'test','capability_id':'context.fuzzy-search','payload':{'q':'x'}}


def main():
 import a2a_executor
 with tempfile.TemporaryDirectory() as td:
  plane=fresh_plane(Path(td))
  safe_descriptor={'id':'context.fuzzy-search','retry_safe':True,'lease_seconds':30}
  safe_binding={'kind':'native','retry_safe':True,'lease_seconds':30,'heartbeat_interval_seconds':0.01}

  def transient():raise TimeoutError('simulated timeout')
  r=a2a_executor.execute(envelope('retryable'),safe_descriptor,safe_binding,transient,plane=plane)
  assert r['failure_state']=='RETRYABLE',r
  assert r['execution_status']=='UNKNOWN',r
  assert not r['completion_evidence'],r
  st=plane.status(r['task_id'])
  assert st['task']['status']=='RUNNING',st

  side_descriptor={'id':'design.production.rollout','requires_verified_execution':True,'verification_contract':'external','retry_safe':False}
  side_binding={'kind':'production-action','retry_safe':False}
  task_id=a2a_executor._task_id(envelope('side-effect'))
  plane.register(a2a_executor._message(envelope('side-effect'),task_id))
  claimed=plane.claim(task_id,consumer='old-worker',lease_seconds=30);assert claimed['ok']
  running=plane.transition(task_id,'RUNNING',consumer='old-worker');assert running['ok']
  task=plane.read(task_id);task['lease']['expires_at']='2000-01-01T00:00:00+00:00';plane._atomic(plane._task_path(task_id),task)
  r2=a2a_executor.execute(envelope('side-effect'),side_descriptor,side_binding,lambda:{'ok':True},plane=plane)
  assert r2['failure_state']=='UNKNOWN',r2
  assert r2['error']['code']=='unsafe_replay_blocked',r2

  terminal_descriptor={'id':'context.fuzzy-search','retry_safe':True}
  terminal_binding={'kind':'native','retry_safe':True}
  def denied():raise RuntimeError('not authorized')
  # dict semantic failure exercises terminal policy deterministically.
  r3=a2a_executor.execute(envelope('terminal'),terminal_descriptor,terminal_binding,lambda:{'ok':False,'code':'not_authorized'},plane=plane)
  assert r3['failure_state']=='TERMINAL_FAIL',r3
  assert plane.status(r3['task_id'])['task']['status']=='FAIL'

 print({'ok':True,'code':'A2A_CONSUMER_RECOVERY_ACCEPTANCE_PASS','states':['RETRYABLE','UNKNOWN','TERMINAL_FAIL']})

if __name__=='__main__':main()
