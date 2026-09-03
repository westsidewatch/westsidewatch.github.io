#!/usr/bin/env python3
"""Checkout-independent inbound delivery for ChatGPT -> Doré A2A mail."""
from __future__ import annotations
import hashlib,json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path

VERSION='dore.a2a-delivery-plane.v1.1'
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve()
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
DELIVERY=HOME/'a2a-delivery';REMOTE_REF=os.environ.get('DORE_A2A_REMOTE_REF','origin/main')
INBOX_PREFIXES=('coordination-inbox','local/dore-local/coordination-inbox')
MAIN_REFSPEC='+refs/heads/main:refs/remotes/origin/main'
def now():return datetime.now(timezone.utc).isoformat()
def canonical_hash(message):
 payload={k:v for k,v in message.items() if not str(k).startswith('_delivery')};raw=json.dumps(payload,ensure_ascii=False,sort_keys=True,separators=(',',':'));return hashlib.sha256(raw.encode()).hexdigest()
def _run(args,timeout=60):return subprocess.run(args,cwd=ROOT,text=True,capture_output=True,timeout=timeout)
def _append(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('a',encoding='utf-8') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True)+'\n')
def _atomic(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8');tmp.replace(path)
def validate(message):
 missing=sorted({'schema','message_id','sender','recipient','body'}-set(message));errors=[]
 if missing:errors.append('missing:'+','.join(missing))
 if message.get('sender')!='chatgpt':errors.append('sender_not_chatgpt')
 if message.get('recipient')!='dore':errors.append('recipient_not_dore')
 if not str(message.get('schema') or '').startswith('dore.mail.v'):errors.append('unsupported_schema')
 if '/' in str(message.get('message_id') or '') or '..' in str(message.get('message_id') or ''):errors.append('unsafe_message_id')
 return {'ok':not errors,'errors':errors}
def remote_commit(ref=REMOTE_REF):
 cp=_run(['git','rev-parse',ref],15)
 if cp.returncode:raise RuntimeError('remote_ref_unavailable:'+cp.stderr[-300:])
 return cp.stdout.strip()
def remote_paths(ref=REMOTE_REF):
 found=[]
 for prefix in INBOX_PREFIXES:
  cp=_run(['git','ls-tree','-r','--name-only',ref,'--',prefix],30)
  if cp.returncode:raise RuntimeError('remote_tree_unavailable:'+cp.stderr[-300:])
  found.extend(x for x in cp.stdout.splitlines() if x.endswith('.json'))
 return sorted(set(found))
def remote_message(path,ref=REMOTE_REF):
 cp=_run(['git','show',f'{ref}:{path}'],20)
 if cp.returncode:raise RuntimeError('remote_message_unavailable:'+path)
 return json.loads(cp.stdout)
def accept(message,*,source_ref,source_commit,source_path,delivery_root=DELIVERY):
 root=Path(delivery_root);inbox=root/'inbox';quarantine=root/'quarantine';acks=root/'delivery-acks.jsonl';events=root/'events.jsonl';check=validate(message);mid=str(message.get('message_id') or 'invalid');digest=canonical_hash(message)
 base={'schema':'dore.a2a-delivery-event.v1','at':now(),'message_id':mid,'content_sha256':digest,'source_ref':source_ref,'source_commit':source_commit,'source_path':source_path}
 if not check['ok']:
  row={**base,'status':'REJECTED_INVALID','validation':check};_atomic(quarantine/(digest+'.json'),{'event':row,'message':message});_append(events,row);return row
 target=inbox/(mid+'.json')
 if target.exists():
  old=json.loads(target.read_text(encoding='utf-8'));oldhash=str((old.get('_delivery') or {}).get('content_sha256') or canonical_hash(old))
  if oldhash==digest:
   row={**base,'status':'REPLAY_DEDUPLICATED'};_append(events,row);return row
  row={**base,'status':'REJECTED_IDENTITY_CONFLICT','accepted_sha256':oldhash};_atomic(quarantine/(mid+'-'+digest+'.json'),{'event':row,'message':message});_append(events,row);return row
 envelope=dict(message);envelope['_delivery']={'plane':VERSION,'status':'DURABLE_ACCEPTED','accepted_at':now(),'content_sha256':digest,'source_ref':source_ref,'source_commit':source_commit,'source_path':source_path,'execution_status':'NOT_STARTED'};_atomic(target,envelope)
 ack={'schema':'dore.mail-delivery-ack.v1','message_id':mid,'content_sha256':digest,'delivery_status':'DURABLE_ACCEPTED','execution_status':'NOT_STARTED','accepted_at':envelope['_delivery']['accepted_at'],'source_ref':source_ref,'source_commit':source_commit,'source_path':source_path};_append(acks,ack);_append(events,{**base,'status':'DURABLE_ACCEPTED'});return ack
def sync(*,fetch=True,ref=REMOTE_REF,delivery_root=DELIVERY,only_message_ids=None,skip_message_ids=None):
 if fetch:
  cp=_run(['git','fetch','origin',MAIN_REFSPEC],120)
  if cp.returncode:return {'ok':False,'code':'A2A_REMOTE_FETCH_FAILED','error':cp.stderr[-500:],'delivery_plane':VERSION}
 commit=remote_commit(ref);results=[];only=set(only_message_ids or []);skip=set(skip_message_ids or [])
 for path in remote_paths(ref):
  if only and Path(path).stem not in only:continue
  try:
   msg=remote_message(path,ref)
   mid=msg.get('message_id')
   if mid in skip or (only and mid not in only):continue
   if msg.get('sender')=='chatgpt' and msg.get('recipient')=='dore':results.append(accept(msg,source_ref=ref,source_commit=commit,source_path=path,delivery_root=delivery_root))
  except (ValueError,RuntimeError) as e:results.append({'status':'SOURCE_READ_FAILED','source_path':path,'error':type(e).__name__+': '+str(e)})
 accepted=[x for x in results if x.get('delivery_status')=='DURABLE_ACCEPTED']
 return {'ok':not any(x.get('status')=='SOURCE_READ_FAILED' for x in results),'code':'A2A_DELIVERY_SYNC_PASS','delivery_plane':VERSION,'source_ref':ref,'source_commit':commit,'accepted':accepted,'accepted_count':len(accepted),'deduplicated_count':sum(x.get('status')=='REPLAY_DEDUPLICATED' for x in results),'identity_conflicts':sum(x.get('status')=='REJECTED_IDENTITY_CONFLICT' for x in results),'results':results}
def durable_messages(delivery_root=DELIVERY):
 inbox=Path(delivery_root)/'inbox';out=[]
 for path in sorted(inbox.glob('*.json')) if inbox.exists() else []:
  try:out.append(json.loads(path.read_text(encoding='utf-8')))
  except ValueError:pass
 return out
def claim(message_id,*,consumer='dore-coordination-worker',delivery_root=DELIVERY):
 root=Path(delivery_root);target=root/'inbox'/(str(message_id)+'.json')
 if not target.exists():raise FileNotFoundError('durable_message_missing:'+str(message_id))
 message=json.loads(target.read_text(encoding='utf-8'));delivery=dict(message.get('_delivery') or {})
 if delivery.get('execution_status') in {'RECEIVED','RUNNING','PASS','FAIL'}:
  return {'schema':'dore.mail-consumer-receipt.v1','message_id':message_id,'content_sha256':delivery.get('content_sha256'),'consumer':delivery.get('consumer') or consumer,'delivery_status':'DURABLE_ACCEPTED','execution_status':delivery.get('execution_status'),'duplicate_claim':True}
 delivery.update({'execution_status':'RECEIVED','consumer':consumer,'consumer_received_at':now()});message['_delivery']=delivery;_atomic(target,message)
 receipt={'schema':'dore.mail-consumer-receipt.v1','message_id':message_id,'content_sha256':delivery.get('content_sha256'),'consumer':consumer,'delivery_status':'DURABLE_ACCEPTED','execution_status':'RECEIVED','consumer_received_at':delivery['consumer_received_at'],'duplicate_claim':False};_append(root/'consumer-receipts.jsonl',receipt);return receipt
def canonical_delivery_reply(message_id,*,delivery_root=DELIVERY):
 target=Path(delivery_root)/'inbox'/(str(message_id)+'.json');message=json.loads(target.read_text(encoding='utf-8'));d=message.get('_delivery') or {}
 return {'schema':'dore.a2a-canonical-delivery-reply.v1','source_message_id':message_id,'transport':'PASS','delivery':'PASS' if d.get('status')=='DURABLE_ACCEPTED' else 'FAIL','consumer':'PASS' if d.get('execution_status') in {'RECEIVED','RUNNING','PASS','FAIL'} else 'PENDING','execution':d.get('execution_status') or 'NOT_STARTED','content_sha256':d.get('content_sha256'),'source_commit':d.get('source_commit'),'claim':'delivery/consumer receipt only; not task-completion evidence'}
if __name__=='__main__':
 import argparse
 parser=argparse.ArgumentParser();parser.add_argument('--ref',default=REMOTE_REF);parser.add_argument('--message-id',action='append',default=[]);parser.add_argument('--no-fetch',action='store_true');parser.add_argument('--claim');args=parser.parse_args()
 if args.claim:
  receipt=claim(args.claim);result={'ok':True,'code':'A2A_DURABLE_CONSUMER_RECEIPT_PASS','consumer_receipt':receipt,'canonical_reply':canonical_delivery_reply(args.claim)}
 else:result=sync(fetch=not args.no_fetch,ref=args.ref,only_message_ids=set(args.message_id))
 print(json.dumps(result,ensure_ascii=False));raise SystemExit(0 if result.get('ok') else 2)
