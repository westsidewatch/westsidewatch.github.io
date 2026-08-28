#!/usr/bin/env python3
"""Durable asynchronous Doré <-> ChatGPT mailbox.

Local Doré can write its own outbound messages without ChatGPT being online.
Messages are append-only JSONL evidence under ~/.dore/coordination. ChatGPT-facing
transport can mirror them later; this module does not pretend an inbound ChatGPT
callback exists.
"""
from __future__ import annotations
import hashlib, json, os, uuid
from datetime import datetime, timezone
from pathlib import Path

HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
BOX=HOME/'coordination'; OUTBOX=BOX/'dore-to-chatgpt.jsonl'; INBOX=BOX/'chatgpt-to-dore.jsonl'; RECEIPTS=BOX/'receipts.jsonl'

def now(): return datetime.now(timezone.utc).isoformat()
def _append(path:Path,obj:dict):
 path.parent.mkdir(parents=True,exist_ok=True)
 raw=json.dumps(obj,ensure_ascii=False,sort_keys=True)
 with path.open('a',encoding='utf-8') as f:f.write(raw+'\n')
 return hashlib.sha256(raw.encode()).hexdigest()

def send_to_chatgpt(subject:str,body:str,*,requires_reply=False,priority='normal',related_goal=None,evidence_refs=None,thread_id=None):
 msg={'schema':'dore.mail.v1','message_id':str(uuid.uuid4()),'thread_id':thread_id or str(uuid.uuid4()),'sender':'dore','recipient':'chatgpt','created_at':now(),'subject':subject,'body':body,'requires_reply':bool(requires_reply),'priority':priority,'related_goal':related_goal,'evidence_refs':list(evidence_refs or [])}
 msg['message_sha256']=hashlib.sha256(json.dumps(msg,ensure_ascii=False,sort_keys=True).encode()).hexdigest(); _append(OUTBOX,msg); return msg

def receive_from_chatgpt(message:dict):
 required={'message_id','sender','recipient','body'}
 if not required.issubset(message) or message.get('sender')!='chatgpt' or message.get('recipient')!='dore': raise ValueError('invalid ChatGPT->Doré message')
 sha=_append(INBOX,message); receipt={'schema':'dore.mail-receipt.v1','message_id':message['message_id'],'received_at':now(),'sha256':sha}; _append(RECEIPTS,receipt); return receipt

def read_jsonl(path:Path):
 if not path.exists(): return []
 out=[]
 for line in path.read_text(encoding='utf-8').splitlines():
  try: out.append(json.loads(line))
  except Exception: pass
 return out

def status(): return {'ok':True,'inbox':len(read_jsonl(INBOX)),'outbox':len(read_jsonl(OUTBOX)),'receipts':len(read_jsonl(RECEIPTS)),'paths':{'inbox':str(INBOX),'outbox':str(OUTBOX)}}
