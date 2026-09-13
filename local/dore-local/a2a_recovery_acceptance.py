#!/usr/bin/env python3
"""Acceptance for Universal A2A lease heartbeat and crash recovery policy."""
from __future__ import annotations
import importlib.util,json,os,tempfile,time
from datetime import datetime,timezone,timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent

def load(name):
 spec=importlib.util.spec_from_file_location('recovery_'+name,HERE/(name+'.py'));mod=importlib.util.module_from_spec(spec);spec.loader.exec_module(mod);return mod

def expire(plane,task_id):
 task=plane.read(task_id);task['lease']['expires_at']=(datetime.now(timezone.utc)-timedelta(seconds=2)).isoformat();plane._atomic(plane._task_path(task_id),task)

def base_envelope(request_id):
 return {'protocol':'dore.a2a/1','action':'dispatch','request_id':request_id,'conversation_id':'recovery-acceptance','session_id':'session-1','consumer_id':'acceptance','capability_id':'knowledge.recall','payload':{'q':'lease'}}

def main():
 with tempfile.TemporaryDirectory(prefix='dore-a2a-recovery-') as td:
  os.environ['DORE_LOCAL_HOME']=td
  plane=load('a2a_execution_plane');executor=load('a2a_executor')

  # 1. Expired RUNNING work is explicitly reclaimable, not terminal FAIL.
  env=base_envelope('reclaim-running');tid=executor._task_id(env);plane.register(executor._message(env,tid));plane.claim(tid,consumer='worker-a');plane.transition(tid,'RUNNING',consumer='worker-a');expire(plane,tid)
  rec=plane.recoverability(tid);assert rec['state']=='RECLAIMABLE' and rec['resume_from']=='RUNNING'
  claimed=plane.claim(tid,consumer='worker-b');assert claimed['ok'] and claimed['reclaimed'] and claimed['code']=='TASK_RECLAIMED'

  # 2. Universal executor renews leases while provider work is still running.
  env2=base_envelope('heartbeat-live');calls={'n':0}
  def slow_provider():calls['n']+=1;time.sleep(0.14);return {'ok':True,'status':'completed','value':'heartbeat'}
  out=executor.execute(env2,{}, {'kind':'native','heartbeat_interval_seconds':0.03,'retry_safe':True},slow_provider,plane=plane)
  assert out['ok'] and out['completion_evidence'] and calls['n']==1
  events=plane.EVENTS.read_text(encoding='utf-8');assert 'LEASE_HEARTBEAT' in events

  # 3. Expired retry-safe RUNNING work is reclaimed and can finish.
  env3=base_envelope('safe-retry');tid3=executor._task_id(env3);plane.register(executor._message(env3,tid3));plane.claim(tid3,consumer='dead-worker');plane.transition(tid3,'RUNNING',consumer='dead-worker');expire(plane,tid3);count={'n':0}
  def safe_provider():count['n']+=1;return {'ok':True,'status':'completed','value':'recovered'}
  recovered=executor.execute(env3,{}, {'kind':'native','retry_safe':True},safe_provider,plane=plane)
  assert recovered['ok'] and recovered['reclaimed'] and recovered['completion_evidence'] and count['n']==1

  # 4. Expired side-effecting RUNNING work is UNKNOWN, never blindly replayed.
  env4=base_envelope('unsafe-side-effect');tid4=executor._task_id(env4);plane.register(executor._message(env4,tid4));plane.claim(tid4,consumer='dead-side-effect');plane.transition(tid4,'RUNNING',consumer='dead-side-effect');expire(plane,tid4);unsafe_calls={'n':0}
  def unsafe_provider():unsafe_calls['n']+=1;return {'ok':True}
  blocked=executor.execute(env4,{'requires_verified_execution':True,'verification_contract':'external-proof-v1'},{'kind':'production-action','retry_safe':False},unsafe_provider,plane=plane)
  assert not blocked['ok'] and blocked['execution_status']=='UNKNOWN' and blocked['error']['code']=='unsafe_replay_blocked' and unsafe_calls['n']==0

  # 5. Crash after durable artifact resumes verification/completion without provider replay.
  env5=base_envelope('artifact-resume');tid5=executor._task_id(env5);plane.register(executor._message(env5,tid5));plane.claim(tid5,consumer='artifact-worker');plane.transition(tid5,'RUNNING',consumer='artifact-worker');result={'ok':True,'status':'completed','value':'already-produced'};artifact={'schema':'dore.a2a-capability-result-artifact.v1','capability_id':'knowledge.recall','request_id':'artifact-resume','result_sha256':executor._digest(result),'result':result};plane.record_artifact(tid5,artifact,consumer='artifact-worker');expire(plane,tid5);resume_calls={'n':0}
  def must_not_run():resume_calls['n']+=1;return {'ok':True}
  resumed=executor.execute(env5,{}, {'kind':'native','retry_safe':True},must_not_run,plane=plane)
  assert resumed['ok'] and resumed['completion_evidence'] and resumed['reclaimed'] and resumed['provider_reexecuted'] is False and resume_calls['n']==0

  print(json.dumps({'ok':True,'acceptance':'dore.a2a-recovery.v1','lease_expiry':'RECLAIMABLE','heartbeat':True,'safe_retry_reclaimed':True,'unsafe_side_effect_replay':'BLOCKED_UNKNOWN','artifact_resume_without_reexecution':True},sort_keys=True))

if __name__=='__main__':main()
