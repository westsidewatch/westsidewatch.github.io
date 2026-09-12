#!/usr/bin/env python3
"""Integration acceptance for coordination_worker -> A2A Execution Plane.

This test exercises the real worker execution adapter without running the
resident loop. It proves handler success is provisional until a verifiable
artifact receipt exists.
"""
from __future__ import annotations
import os,tempfile

with tempfile.TemporaryDirectory(prefix='dore-worker-exec-') as td:
 os.environ['DORE_LOCAL_HOME']=td
 os.environ['DORE_A2A_WORKER_ID']='acceptance-worker'
 import coordination_worker as worker
 import a2a_execution_plane as ep

 def message(mid,kind='local_exec'):
  return {'schema':'dore.mail.v2','message_id':mid,'sender':'chatgpt','recipient':'dore','kind':kind,'body':'acceptance'}

 # 1. Legacy behavior is forbidden: {ok:true} alone is not completion evidence.
 bare=message('worker-gate-no-artifact','acceptance_no_artifact')
 try:
  worker.execute_with_plane(bare,dispatcher=lambda _:{'ok':True})
  raise AssertionError('handler_success_without_artifact_must_not_pass')
 except worker.TaskResultError as e:
  assert e.result.get('code')=='EXECUTION_ARTIFACT_REQUIRED',e.result
 no_art=ep.status(bare['message_id'])
 assert no_art['task']['status']=='RUNNING',no_art
 assert no_art['completion_evidence'] is False,no_art

 # 2. A concrete local-exec receipt is normalized into an artifact, verified,
 # and only then promoted to PASS.
 good=message('worker-gate-verified')
 result=worker.execute_with_plane(good,dispatcher=lambda _:{
  'ok':True,
  'results':[{'index':1,'argv':['python3','-c','print(1)'],'cwd':'/tmp','returncode':0,'stdout':'1\n','stderr':''}],
 })
 assert result['ok'] is True,result
 assert result['execution_plane']['status']=='PASS',result
 assert result['execution_plane']['completion_evidence'] is True,result
 proof=ep.status(good['message_id'])
 assert proof['task']['artifact']['type']=='local_exec_receipt',proof
 assert proof['task']['verification']['ok'] is True,proof
 assert proof['completion_evidence'] is True,proof

 # 3. A failed handler cannot manufacture PASS and can be terminalized as FAIL.
 bad=message('worker-gate-fail')
 try:
  worker.execute_with_plane(bad,dispatcher=lambda _:{'ok':False,'error':'expected_failure'})
  raise AssertionError('failed_handler_must_raise')
 except worker.TaskResultError:
  failed=worker._mark_execution_fail(bad['message_id'],{'ok':False,'error':'expected_failure'})
 assert failed['status']=='FAIL',failed
 assert ep.status(bad['message_id'])['completion_evidence'] is False

 # 4. The legacy finish helper itself is guarded; callers cannot bypass the
 # plane by writing worker-state PASS directly.
 bypass=message('worker-gate-bypass','acceptance_no_artifact')
 ep.register(bypass)
 state={};done=set()
 try:
  worker._finish_pass(state,done,bypass,{'ok':True},1,[])
  raise AssertionError('legacy_finish_pass_bypass_must_be_blocked')
 except worker.TaskResultError as e:
  assert e.result.get('code')=='EXECUTION_PASS_WITHOUT_EVIDENCE',e.result
 assert bypass['message_id'] not in done

 print('PASS coordination_worker_execution_acceptance: no_artifact_blocked verified_artifact_pass failure_terminalized legacy_pass_blocked')
