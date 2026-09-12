#!/usr/bin/env python3
"""Acceptance for Doré A2A Execution Plane.

PASS proves delivery acceptance is not promoted to completion: a task must be
claimed, run, produce an artifact, verify that artifact, and only then PASS.
"""
from __future__ import annotations
import json,os,tempfile
from datetime import datetime,timezone,timedelta
from pathlib import Path

with tempfile.TemporaryDirectory(prefix='dore-a2a-exec-') as td:
 os.environ['DORE_LOCAL_HOME']=td
 import a2a_execution_plane as ep

 msg={'schema':'dore.mail.v2','message_id':'acceptance-task-1','sender':'chatgpt','recipient':'dore','kind':'local_exec','body':'acceptance'}
 task=ep.register(msg,{'content_sha256':'a'*64,'source_commit':'b'*40,'source_ref':'main','accepted_at':ep.now()})
 assert task['status']=='ACCEPTED'
 # Re-register is replay-safe and does not advance or reset lifecycle.
 assert ep.register(msg)['status']=='ACCEPTED'

 c1=ep.claim(msg['message_id'],'worker-A',60);assert c1['ok'] and c1['task']['status']=='CLAIMED'
 c2=ep.claim(msg['message_id'],'worker-B',60);assert not c2['ok'] and c2['code']=='TASK_LEASED'
 r=ep.transition(msg['message_id'],'RUNNING',consumer='worker-A');assert r['ok'] and r['task']['status']=='RUNNING'
 early=ep.complete(msg['message_id'],consumer='worker-A');assert not early['ok'] and early['code']=='VERIFIED_ARTIFACT_REQUIRED'
 art=ep.record_artifact(msg['message_id'],{'type':'acceptance','result_digest':'deadbeef'},consumer='worker-A');assert art['ok'] and art['task']['status']=='ARTIFACT_PRODUCED'
 early2=ep.complete(msg['message_id'],consumer='worker-A');assert not early2['ok'] and early2['code']=='VERIFIED_ARTIFACT_REQUIRED'
 ver=ep.verify(msg['message_id'],{'ok':True,'method':'acceptance'},consumer='worker-A');assert ver['ok'] and ver['task']['status']=='VERIFIED'
 done=ep.complete(msg['message_id'],{'ok':True},consumer='worker-A');assert done['ok'] and done['task']['status']=='PASS'
 status=ep.status(msg['message_id']);assert status['completion_evidence'] is True

 # Verification failure is terminal FAIL.
 msg2={**msg,'message_id':'acceptance-task-verify-fail'}
 ep.register(msg2);ep.claim(msg2['message_id'],'worker-A',60);ep.transition(msg2['message_id'],'RUNNING',consumer='worker-A');ep.record_artifact(msg2['message_id'],{'type':'acceptance'},consumer='worker-A')
 bad=ep.verify(msg2['message_id'],{'ok':False,'reason':'negative-case'},consumer='worker-A');assert not bad['ok'] and bad['task']['status']=='FAIL'
 assert ep.status(msg2['message_id'])['completion_evidence'] is False

 # Expired lease can be reclaimed by another worker.
 msg3={**msg,'message_id':'acceptance-task-expired-lease'}
 ep.register(msg3);ep.claim(msg3['message_id'],'worker-A',60)
 p=ep._task_path(msg3['message_id']);t=json.loads(p.read_text());t['lease']['expires_at']=(datetime.now(timezone.utc)-timedelta(seconds=1)).isoformat();ep._atomic(p,t)
 reclaimed=ep.claim(msg3['message_id'],'worker-B',60);assert reclaimed['ok'] and reclaimed['task']['lease']['owner']=='worker-B'

 print(json.dumps({'ok':True,'code':'DORE_A2A_EXECUTION_PLANE_PASS','checks':['replay_safe','exclusive_live_lease','running_requires_lease','no_pass_without_artifact','no_pass_without_verification','verified_artifact_pass','verification_failure_terminal','expired_lease_reclaim']},sort_keys=True))
