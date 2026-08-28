#!/usr/bin/env python3
"""Durable asynchronous Doré <-> ChatGPT mailbox with free git-backed transport."""
from __future__ import annotations
import hashlib,json,os,subprocess,uuid
from datetime import datetime,timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
BOX=HOME/'coordination'; OUTBOX=BOX/'dore-to-chatgpt.jsonl'; INBOX=BOX/'chatgpt-to-dore.jsonl'; RECEIPTS=BOX/'receipts.jsonl'; REPO_OUTBOX=ROOT/'local/dore-local/coordination-outbox'
def now(): return datetime.now(timezone.utc).isoformat()
def _append(path:Path,obj:dict):
 path.parent.mkdir(parents=True,exist_ok=True); raw=json.dumps(obj,ensure_ascii=False,sort_keys=True)
 with path.open('a',encoding='utf-8') as f:f.write(raw+'\n')
 return hashlib.sha256(raw.encode()).hexdigest()
def _git_publish(msg):
 """Best-effort free transport. Never blocks Doré if git credentials/network are unavailable."""
 if not (ROOT/'.git').exists(): return {'published':False,'reason':'repo_missing'}
 try:
  dirty=subprocess.run(['git','status','--porcelain'],cwd=ROOT,text=True,capture_output=True,timeout=15)
  if dirty.returncode or dirty.stdout.strip(): return {'published':False,'reason':'dirty_worktree'}
  REPO_OUTBOX.mkdir(parents=True,exist_ok=True); path=REPO_OUTBOX/(msg['message_id']+'.json'); path.write_text(json.dumps(msg,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8')
  rel=str(path.relative_to(ROOT)); subprocess.run(['git','add','--',rel],cwd=ROOT,check=True,capture_output=True,text=True,timeout=15)
  c=subprocess.run(['git','commit','-m','dore: publish coordination message '+msg['message_id']],cwd=ROOT,capture_output=True,text=True,timeout=30)
  if c.returncode: subprocess.run(['git','reset','HEAD','--',rel],cwd=ROOT,capture_output=True); path.unlink(missing_ok=True); return {'published':False,'reason':'commit_failed'}
  p=subprocess.run(['git','push','origin','HEAD:main'],cwd=ROOT,capture_output=True,text=True,timeout=60)
  if p.returncode: return {'published':False,'reason':'push_failed','committed':True}
  return {'published':True,'path':rel}
 except Exception as e:return {'published':False,'reason':type(e).__name__}
def send_to_chatgpt(subject:str,body:str,*,requires_reply=False,priority='normal',related_goal=None,evidence_refs=None,thread_id=None):
 msg={'schema':'dore.mail.v1','message_id':str(uuid.uuid4()),'thread_id':thread_id or str(uuid.uuid4()),'sender':'dore','recipient':'chatgpt','created_at':now(),'subject':subject,'body':body,'requires_reply':bool(requires_reply),'priority':priority,'related_goal':related_goal,'evidence_refs':list(evidence_refs or [])}
 msg['message_sha256']=hashlib.sha256(json.dumps(msg,ensure_ascii=False,sort_keys=True).encode()).hexdigest(); _append(OUTBOX,msg); msg['transport_result']=_git_publish(msg); return msg
def receive_from_chatgpt(message:dict):
 required={'message_id','sender','recipient','body'}
 if not required.issubset(message) or message.get('sender')!='chatgpt' or message.get('recipient')!='dore': raise ValueError('invalid ChatGPT->Doré message')
 existing={m.get('message_id') for m in read_jsonl(INBOX)}
 if message['message_id'] in existing:return {'schema':'dore.mail-receipt.v1','message_id':message['message_id'],'duplicate':True}
 sha=_append(INBOX,message); receipt={'schema':'dore.mail-receipt.v1','message_id':message['message_id'],'received_at':now(),'sha256':sha}; _append(RECEIPTS,receipt); return receipt
def read_jsonl(path:Path):
 if not path.exists(): return []
 out=[]
 for line in path.read_text(encoding='utf-8').splitlines():
  try:out.append(json.loads(line))
  except Exception:pass
 return out
def status():return {'ok':True,'inbox':len(read_jsonl(INBOX)),'outbox':len(read_jsonl(OUTBOX)),'receipts':len(read_jsonl(RECEIPTS)),'paths':{'inbox':str(INBOX),'outbox':str(OUTBOX),'repo_outbox':str(REPO_OUTBOX)}}
