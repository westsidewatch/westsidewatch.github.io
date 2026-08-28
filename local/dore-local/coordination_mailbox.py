#!/usr/bin/env python3
"""Durable asynchronous Doré <-> ChatGPT mailbox with free git-backed transport."""
from __future__ import annotations
import hashlib,json,os,subprocess,uuid
from datetime import datetime,timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
BOX=HOME/'coordination'; OUTBOX=BOX/'dore-to-chatgpt.jsonl'; INBOX=BOX/'chatgpt-to-dore.jsonl'; RECEIPTS=BOX/'receipts.jsonl'; DELIVERY=BOX/'delivery.jsonl'; REPO_OUTBOX=ROOT/'local/dore-local/coordination-outbox'
def now(): return datetime.now(timezone.utc).isoformat()
def _append(path:Path,obj:dict):
 path.parent.mkdir(parents=True,exist_ok=True); raw=json.dumps(obj,ensure_ascii=False,sort_keys=True)
 with path.open('a',encoding='utf-8') as f:f.write(raw+'\n')
 return hashlib.sha256(raw.encode()).hexdigest()
def read_jsonl(path:Path):
 if not path.exists(): return []
 out=[]
 for line in path.read_text(encoding='utf-8').splitlines():
  try:out.append(json.loads(line))
  except Exception:pass
 return out
def _delivered_ids(): return {x.get('message_id') for x in read_jsonl(DELIVERY) if x.get('published') is True}
def _run(args,timeout=60):return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
def _git_publish(msg):
 """Publish only this mail path; unrelated Doré work must not block communication."""
 if not (ROOT/'.git').exists(): return {'published':False,'reason':'repo_missing'}
 path=None
 try:
  # Reconcile remote first only when HEAD can fast-forward. Never stage/commit unrelated files.
  _run(['git','fetch','origin','main'])
  rel=f"local/dore-local/coordination-outbox/{msg['message_id']}.json"; path=ROOT/rel; path.parent.mkdir(parents=True,exist_ok=True)
  # If the exact path is already in origin/main, delivery already succeeded earlier.
  remote=_run(['git','show',f'origin/main:{rel}'],15)
  rendered=json.dumps(msg,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
  if remote.returncode==0 and remote.stdout==rendered:return {'published':True,'path':rel,'already_remote':True}
  # Pull remote changes only if this checkout is behind with no local divergence.
  ff=_run(['git','merge-base','--is-ancestor','HEAD','origin/main'],15)
  if ff.returncode==0:_run(['git','merge','--ff-only','origin/main'],30)
  path.write_text(rendered,encoding='utf-8')
  _run(['git','add','--',rel],15)
  # --only + pathspec isolates the mail commit from unrelated staged/unstaged autonomous work.
  c=_run(['git','commit','--only','-m','dore: publish coordination message '+msg['message_id'],'--',rel],30)
  if c.returncode:
   remote=_run(['git','show',f'origin/main:{rel}'],15)
   if remote.returncode==0 and remote.stdout==rendered:return {'published':True,'path':rel,'already_remote':True}
   return {'published':False,'reason':'commit_failed','detail':c.stderr[-300:]}
  p=_run(['git','push','origin','HEAD:main'],60)
  if p.returncode:return {'published':False,'reason':'push_failed','committed':True,'detail':p.stderr[-300:]}
  return {'published':True,'path':rel}
 except Exception as e:return {'published':False,'reason':type(e).__name__}
def flush_outbox():
 delivered=_delivered_ids(); results=[]
 for msg in read_jsonl(OUTBOX):
  mid=msg.get('message_id')
  if not mid or mid in delivered:continue
  result=_git_publish(msg); rec={'schema':'dore.mail-delivery.v1','message_id':mid,'attempted_at':now(),**result}; _append(DELIVERY,rec); results.append(rec)
  if result.get('published'):delivered.add(mid)
  else:break
 return results
def send_to_chatgpt(subject:str,body:str,*,requires_reply=False,priority='normal',related_goal=None,evidence_refs=None,thread_id=None):
 msg={'schema':'dore.mail.v1','message_id':str(uuid.uuid4()),'thread_id':thread_id or str(uuid.uuid4()),'sender':'dore','recipient':'chatgpt','created_at':now(),'subject':subject,'body':body,'requires_reply':bool(requires_reply),'priority':priority,'related_goal':related_goal,'evidence_refs':list(evidence_refs or [])}
 msg['message_sha256']=hashlib.sha256(json.dumps(msg,ensure_ascii=False,sort_keys=True).encode()).hexdigest(); _append(OUTBOX,msg); flush_outbox(); return msg
def receive_from_chatgpt(message:dict):
 required={'message_id','sender','recipient','body'}
 if not required.issubset(message) or message.get('sender')!='chatgpt' or message.get('recipient')!='dore':raise ValueError('invalid ChatGPT->Doré message')
 existing={m.get('message_id') for m in read_jsonl(INBOX)}
 if message['message_id'] in existing:return {'schema':'dore.mail-receipt.v1','message_id':message['message_id'],'duplicate':True}
 sha=_append(INBOX,message); receipt={'schema':'dore.mail-receipt.v1','message_id':message['message_id'],'received_at':now(),'sha256':sha}; _append(RECEIPTS,receipt); return receipt
def status():return {'ok':True,'inbox':len(read_jsonl(INBOX)),'outbox':len(read_jsonl(OUTBOX)),'receipts':len(read_jsonl(RECEIPTS)),'delivered':len(_delivered_ids()),'paths':{'inbox':str(INBOX),'outbox':str(OUTBOX),'repo_outbox':str(REPO_OUTBOX)}}
