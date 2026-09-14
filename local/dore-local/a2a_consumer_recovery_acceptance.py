#!/usr/bin/env python3
"""Acceptance for 1C/6 stage 2 consumer recovery unification."""
from __future__ import annotations
import importlib,os,tempfile
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
 with tempfile.TemporaryDirectory() as td:
  plane=fresh_plane(Path(td))
  import a2a_executor
  safe_descriptor={'id':'context.fuzzy-search','retry_safe':True,'lease_seconds':30}
  safe_binding={'kind':'native','retry_safe':True,'lease_seconds':30,'heartbeat_interval_seconds':0.01}

  def transient():raise TimeoutError('simulated timeout')
  r=a2a_executor.execute(envelope('retryable'),safe_descriptor,safe_binding,transient,plane=plane)
  assert r['failure_state']=='RETRYABLE',r
  assert r['execution_status']=='UNKNOWN',r
  assert not r['completion_evidence'],r
  st=plane.status(r['task_id']);assert st['task']['status']=='RUNNING',st

  budget=[a2a_executor.execute(envelope('retry-budget'),safe_descriptor,safe_binding,transient,plane=plane) for _ in range(3)]
  assert [x['failure']['attempt'] for x in budget]==[1,2,3],budget
  assert budget[-1]['failure_state']=='RESEARCH_REQUIRED',budget[-1]
  assert plane.status(budget[-1]['task_id'])['task']['status']=='RESEARCH_REQUIRED'

  side_calls=[]
  def uncertain_side_effect():side_calls.append(True);raise TimeoutError('side effect outcome unknown')
  unknown_first=a2a_executor.execute(envelope('unknown-side-effect'),{'id':'design.production.rollout','requires_verified_execution':True,'verification_contract':'external','retry_safe':False}, {'kind':'production-action','retry_safe':False},uncertain_side_effect,plane=plane)
  unknown_second=a2a_executor.execute(envelope('unknown-side-effect'),{'id':'design.production.rollout','requires_verified_execution':True,'verification_contract':'external','retry_safe':False}, {'kind':'production-action','retry_safe':False},uncertain_side_effect,plane=plane)
  assert unknown_first['failure_state']=='UNKNOWN' and unknown_second['failure_state']=='UNKNOWN',(unknown_first,unknown_second)
  assert len(side_calls)==1,side_calls

  import capability_bus
  original_native=capability_bus._invoke_native
  try:
   capability_bus._invoke_native=lambda *args,**kwargs:(_ for _ in ()).throw(TimeoutError('bus timeout'))
   descriptor=capability_bus.resolve('design.intelligence');binding=capability_bus.BINDINGS.get('design.intelligence')
   bus_timeout=a2a_executor.execute(envelope('bus-timeout'),descriptor,binding,lambda:capability_bus.call('design.intelligence',{},None),plane=plane)
  finally:capability_bus._invoke_native=original_native
  assert bus_timeout['failure_state']=='RETRYABLE',bus_timeout

  side_descriptor={'id':'design.production.rollout','requires_verified_execution':True,'verification_contract':'external','retry_safe':False}
  side_binding={'kind':'production-action','retry_safe':False}
  task_id=a2a_executor._task_id(envelope('side-effect'));plane.register(a2a_executor._message(envelope('side-effect'),task_id))
  claimed=plane.claim(task_id,consumer='old-worker',lease_seconds=30);assert claimed['ok']
  running=plane.transition(task_id,'RUNNING',consumer='old-worker');assert running['ok']
  task=plane.read(task_id);task['lease']['expires_at']='2000-01-01T00:00:00+00:00';plane._atomic(plane._task_path(task_id),task)
  r2=a2a_executor.execute(envelope('side-effect'),side_descriptor,side_binding,lambda:{'ok':True},plane=plane)
  assert r2['failure_state']=='UNKNOWN',r2
  assert r2['error']['code']=='unsafe_replay_blocked',r2

  r3=a2a_executor.execute(envelope('terminal'),safe_descriptor,safe_binding,lambda:{'ok':False,'code':'not_authorized'},plane=plane)
  assert r3['failure_state']=='TERMINAL_FAIL',r3
  assert plane.status(r3['task_id'])['task']['status']=='FAIL'

  worker=(HERE/'coordination_worker.py').read_text(encoding='utf-8')
  required=['import a2a_failure_policy as failure_policy','def _canonical_failure(','def _finish_canonical_failure(','canonical-recovery:RETRYABLE','canonical-recovery:UNKNOWN','canonical-recovery:QUARANTINED','canonical-recovery:TERMINAL_FAIL']
  missing=[x for x in required if x not in worker];assert not missing,missing

  import a2a_failure_policy as policy
  safe=policy.classify({'code':'timeout'},descriptor={'retry_safe':True},binding={'kind':'coordination-worker'},attempt=1,max_attempts=3);assert safe['state']=='RETRYABLE',safe
  ambiguous=policy.classify({'code':'timeout'},descriptor={'retry_safe':False,'side_effecting':True},binding={'kind':'production-action'},attempt=1,max_attempts=3);assert ambiguous['state']=='UNKNOWN',ambiguous
  poison=policy.classify({'code':'malformed_message'},descriptor={'retry_safe':True},binding={'kind':'coordination-worker'},attempt=1,max_attempts=3);assert poison['state']=='QUARANTINED',poison
  research=policy.classify({'code':'timeout'},descriptor={'retry_safe':True},binding={'kind':'coordination-worker'},attempt=3,max_attempts=3);assert research['state']=='RESEARCH_REQUIRED',research

 print({'ok':True,'code':'A2A_CONSUMER_RECOVERY_ACCEPTANCE_PASS','states':['RETRYABLE','UNKNOWN','QUARANTINED','RESEARCH_REQUIRED','TERMINAL_FAIL'],'consumers':['universal-executor','coordination-worker']})

if __name__=='__main__':main()
