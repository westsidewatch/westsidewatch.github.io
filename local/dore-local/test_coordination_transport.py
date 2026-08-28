#!/usr/bin/env python3
"""Offline contract tests for the free Doré<->ChatGPT transport."""
import os,tempfile
with tempfile.TemporaryDirectory() as td:
 os.environ['DORE_LOCAL_HOME']=td
 import coordination_mailbox as m
 msg={'schema':'dore.mail.v1','message_id':'m1','thread_id':'t1','sender':'chatgpt','recipient':'dore','body':'hello','requires_reply':True}
 r1=m.receive_from_chatgpt(msg); r2=m.receive_from_chatgpt(msg)
 assert r1['message_id']=='m1' and not r1.get('duplicate'); assert r2.get('duplicate') is True; assert len(m.read_jsonl(m.INBOX))==1
 # Isolate contract from real git. A failed transport must never erase the spoken message.
 m.ROOT=m.Path(td)/'no-repo'
 out=m.send_to_chatgpt('reply','hello world',thread_id='t1')
 assert out['sender']=='dore' and out['body']=='hello world' and out['thread_id']=='t1' and out['message_sha256']; assert len(m.read_jsonl(m.OUTBOX))==1
 attempts=m.read_jsonl(m.DELIVERY); assert attempts and attempts[-1]['published'] is False
 before=len(attempts); m.flush_outbox(); after=m.read_jsonl(m.DELIVERY); assert len(after)==before+1 and after[-1]['message_id']==out['message_id']
 # A delivered message is not retried again.
 m._append(m.DELIVERY,{'schema':'dore.mail-delivery.v1','message_id':out['message_id'],'attempted_at':m.now(),'published':True})
 before=len(m.read_jsonl(m.DELIVERY)); assert m.flush_outbox()==[]; assert len(m.read_jsonl(m.DELIVERY))==before
 print('DORE_COORDINATION_TRANSPORT_CONTRACT_PASS')
