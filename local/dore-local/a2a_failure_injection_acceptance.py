#!/usr/bin/env python3
"""1E reliability acceptance with synthetic failure conditions."""
from __future__ import annotations
import importlib,os,tempfile
from datetime import datetime,timezone,timedelta
from pathlib import Path

HERE=Path(__file__).resolve().parent
import sys
if str(HERE) not in sys.path:sys.path.insert(0,str(HERE))


def envelope(request_id):
 return {'protocol':'dore.a2a/1','action':'dispatch','request_id':request_id,'conversation_id':'failure-injection','session_id':'s1','consumer_id':'acceptance','capability_id':'context.fuzzy-search','payload':{'q':'x'}}


def main():
 with tempfile.TemporaryDirectory(prefix='dore-a2a-fi-') as td:
  os.environ['DORE_LOCAL_HOME']=td
  import a2a_execution_plane as plane
  import a2a_executor as executor
  import a2a_failure_policy as policy
  import a2a_generation as generation
  import a2a_delivery_plane as delivery
  import coordination_mailbox as mailbox
  import a2a_result_delivery as result_delivery
  plane=importlib.reload(plane);policy=importlib.reload(policy);mailbox=importlib.reload(mailbox);result_delivery=importlib.reload(result_delivery)
  checks={}

  msg={'message_id':'fi-worker','kind':'capability.call'}
  plane.register(msg);plane.claim(msg['message_id'],'worker-a');plane.transition(msg['message_id'],'RUNNING',consumer='worker-a')
  task=plane.read(msg['message_id']);task['lease']['expires_at']=(datetime.now(timezone.utc)-timedelta(seconds=2)).isoformat();plane._atomic(plane._task_path(msg['message_id']),task)
  rec=plane.recoverability(msg['message_id']);reclaim=plane.claim(msg['message_id'],'worker-b')
  checks['worker_reclaim']=rec['state']=='RECLAIMABLE' and reclaim['ok'] and reclaim['reclaimed']

  same={'message_id':'fi-duplicate','kind':'capability.call','payload':{'x':1}}
  one=plane.register(same);two=plane.register(same);conflict=False
  try:plane.register({**same,'payload':{'x':2}})
  except ValueError as exc:conflict='identity_conflict' in str(exc)
  checks['duplicate_hash_identity']=one['content_sha256']==two['content_sha256'] and conflict

  droot=Path(td)/'delivery'
  bad={'schema':'bad','message_id':'unsafe/id','sender':'chatgpt','recipient':'dore','body':'bad'}
  good={'schema':'dore.mail.v2','message_id':'fi-good','sender':'chatgpt','recipient':'dore','body':'good'}
  bad_result=delivery.accept(bad,source_ref='test',source_commit='a'*40,source_path='bad',delivery_root=droot)
  good_result=delivery.accept(good,source_ref='test',source_commit='a'*40,source_path='good',delivery_root=droot)
  checks['poison_isolation']=bad_result['status']=='REJECTED_INVALID' and good_result['delivery_status']=='DURABLE_ACCEPTED'

  def provider_timeout():raise TimeoutError('synthetic timeout')
  timeout_result=executor.execute(envelope('fi-timeout'),{'retry_safe':True},{'kind':'native','retry_safe':True},provider_timeout,plane=plane)
  checks['provider_timeout']=timeout_result.get('failure_state')=='RETRYABLE' and timeout_result.get('completion_evidence') is False

  transport_loss=policy.classify({'code':'connection_reset'},descriptor={'retry_safe':True})
  checks['transport_loss']=transport_loss['state']=='RETRYABLE'

  original=generation.checkout_state
  try:
   generation.checkout_state=lambda:{'commit':'different-head','ref':'main','registry_sha256':generation.ACTIVE_REGISTRY_SHA256}
   stale=generation.identity()
  finally:generation.checkout_state=original
  checks['stale_resident']=stale['restart_required'] is True

  proof={'ok':True,'task':{'status':'PASS','artifact':{'sha256':'b'*64},'verification':{'ok':True}},'completion_evidence':True}
  receipt=result_delivery.build('fi-result','PASS',{'ok':True},proof,terminal=True);result_delivery.record(receipt)
  mailbox.ROOT=Path(td)/'missing-repo';out=mailbox.send_to_chatgpt('fi','result',message_id='result-fi-result')
  failed=mailbox.outbound_status(out['message_id']);before=result_delivery.latest('fi-result')['receipt_sha256']
  original_publish=mailbox._git_publish
  try:
   mailbox._git_publish=lambda m:{'published':True,'path':'synthetic/'+m['message_id']}
   mailbox.flush_outbox()
  finally:mailbox._git_publish=original_publish
  recovered=mailbox.outbound_status(out['message_id']);after=result_delivery.latest('fi-result')['receipt_sha256']
  checks['result_delivery_recovery']=failed['published'] is False and recovered['published'] is True and before==after

  assert all(checks.values()),checks
  print({'ok':True,'code':'A2A_FAILURE_INJECTION_ACCEPTANCE_PASS','checks':checks})

if __name__=='__main__':main()
