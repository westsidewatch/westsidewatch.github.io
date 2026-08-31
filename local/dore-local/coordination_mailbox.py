#!/usr/bin/env python3
"""Durable asynchronous Doré <-> ChatGPT mailbox with free git-backed transport."""
from __future__ import annotations
import hashlib,json,os,subprocess,uuid,tempfile,shutil
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
def _run(args,timeout=60,cwd=None):return subprocess.run(args,cwd=cwd or ROOT,text=True,capture_output=True,timeout=timeout)
def _remote_exact(rel,rendered):
 cp=_run(['git','fetch','origin','main'],60)
 if cp.returncode:return False
 r=_run(['git','show',f'origin/main:{rel}'],15)
 return r.returncode==0 and r.stdout==rendered
def _git_publish(msg):
 """Publish one mail path from an isolated worktree so heartbeat commits cannot race the resident checkout."""
 if not (ROOT/'.git').exists(): return {'published':False,'reason':'repo_missing'}
 rel=f"local/dore-local/coordination-outbox/{msg['message_id']}.json";rendered=json.dumps(msg,ensure_ascii=False,sort_keys=True,indent=2)+'\n'
 try:
  if _remote_exact(rel,rendered):return {'published':True,'path':rel,'already_remote':True}
  last=''
  for attempt in range(1,4):
   _run(['git','fetch','origin','main'],60)
   td=Path(tempfile.mkdtemp(prefix='dore-mail-'))
   try:
    add=_run(['git','worktree','add','--detach',str(td),'origin/main'],60)
    if add.returncode:
     last=add.stderr[-400:];continue
    path=td/rel;path.parent.mkdir(parents=True,exist_ok=True);path.write_text(rendered,encoding='utf-8')
    a=_run(['git','add','--',rel],15,td)
    if a.returncode:last=a.stderr[-400:];continue
    c=_run(['git','commit','-m','dore: publish coordination message '+msg['message_id'],'--',rel],30,td)
    if c.returncode:
     if _remote_exact(rel,rendered):return {'published':True,'path':rel,'already_remote':True}
     last=c.stderr[-400:];continue
    p=_run(['git','push','origin','HEAD:main'],60,td)
    if p.returncode==0:return {'published':True,'path':rel,'attempt':attempt,'isolated_worktree':True}
    last=p.stderr[-400:]
    if _remote_exact(rel,rendered):return {'published':True,'path':rel,'already_remote':True}
   finally:
    _run(['git','worktree','remove','--force',str(td)],30)
    shutil.rmtree(td,ignore_errors=True)
  return {'published':False,'reason':'push_race_exhausted','detail':last}
 except Exception as e:return {'published':False,'reason':type(e).__name__+': '+str(e)[:200]}
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
