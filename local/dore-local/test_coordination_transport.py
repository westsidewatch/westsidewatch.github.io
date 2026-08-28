#!/usr/bin/env python3
"""Offline contract tests for the free Doré<->ChatGPT transport."""
import json,os,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as td:
 os.environ['DORE_LOCAL_HOME']=td
 import coordination_mailbox as m
 msg={'schema':'dore.mail.v1','message_id':'m1','thread_id':'t1','sender':'chatgpt','recipient':'dore','body':'hello','requires_reply':True}
 r1=m.receive_from_chatgpt(msg); r2=m.receive_from_chatgpt(msg)
 assert r1['message_id']=='m1' and not r1.get('duplicate')
 assert r2.get('duplicate') is True
 assert len(m.read_jsonl(m.INBOX))==1
 out=m.send_to_chatgpt('reply','hello world',thread_id='t1')
 assert out['sender']=='dore' and out['recipient']=='chatgpt' and out['body']=='hello world' and out['thread_id']=='t1'
 assert out['message_sha256']
 assert len(m.read_jsonl(m.OUTBOX))==1
 print('DORE_COORDINATION_TRANSPORT_CONTRACT_PASS')
