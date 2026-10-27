#!/usr/bin/env python3
"""Universal GitHub entry adapter for Doré A2A.

All GitHub-originated requests normalize to one public dore.call shape and then
enter the existing Unix-socket Universal A2A Core. This adapter does not restart
or refresh the control plane.
"""
from __future__ import annotations
import json, os, re, urllib.request
from pathlib import Path
import sys
HERE=Path(__file__).resolve().parent
if str(HERE) not in sys.path: sys.path.insert(0,str(HERE))
from unix_rpc_client import call

PROTOCOL='dore.a2a/1'
CAP_RE=re.compile(r'^[A-Za-z0-9_.-]{1,128}$')
MAX_COMMENT_BYTES=60000
LONG_CAPABILITIES={'design.production.rollout','search.local.repair','wake.runtime.install'}
CAPABILITY_TIMEOUTS={
 'context.fuzzy-search':45.0,'image.local.repair':3900.0,'theology.live.acceptance':900.0,
 'design.intelligence.live.acceptance':1500.0,'theology.training.prepare':2100.0,
 'theology.training.prefetch_model':3600.0,'theology.training.stage32':60.0,
 'theology.training.micro32':7200.0,'theology.training.eval32':3600.0,
 'theology.training.stage64':60.0,'theology.training.micro64':7200.0,
 'theology.training.eval64':3600.0,'theology.shadow.acceptance64':1200.0,
}

def fail(message):return {'ok':False,'protocol':PROTOCOL,'status':'failed','error':message}
def parse_command():
 raw=(os.environ.get('DORE_COMMAND_JSON') or '').strip()
 if raw:
  command=json.loads(raw)
  if not isinstance(command,dict):raise ValueError('command_must_be_object')
 else:
  args=json.loads(os.environ.get('DORE_ARGS_JSON') or '{}')
  command={'protocol':PROTOCOL,'request_id':os.environ.get('DORE_REQUEST_ID'),'capability':os.environ.get('DORE_CAPABILITY'),'args':args}
 if command.get('protocol')!=PROTOCOL:raise ValueError('invalid_protocol')
 request_id=str(command.get('request_id') or '').strip();capability=str(command.get('capability') or '').strip();args=command.get('args',{})
 if not request_id or len(request_id)>128:raise ValueError('invalid_request_id')
 if not CAP_RE.fullmatch(capability):raise ValueError('invalid_capability')
 if not isinstance(args,dict):raise ValueError('args_must_be_object')
 return request_id,capability,args

def execute_canonical_mail(args):
 # Owner-only issue transport reuses the already existing durable coordination
 # execution plane; it does not execute an arbitrary issue-body shell command.
 mid=str(args.get('message_id') or '').strip()
 if not re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',mid):raise ValueError('invalid_coordination_message_id')
 path=HERE.parents[1]/'coordination-inbox'/f'{mid}.json'
 if not path.is_file():raise FileNotFoundError('canonical_coordination_message_not_found:'+mid)
 msg=json.loads(path.read_text(encoding='utf-8'))
 if (msg.get('message_id')!=mid or msg.get('schema')!='dore.mail.v2' or
     msg.get('sender')!='chatgpt' or msg.get('recipient')!='dore' or msg.get('kind')!='local_exec'):
  raise ValueError('untrusted_or_unsupported_coordination_message')
 from a2a_delivery_plane import accept
 import a2a_execution_plane as plane
 import a2a_result_delivery as results
 from coordination_worker import execute_with_plane,evidence_for
 source_commit=os.environ.get('GITHUB_SHA') or 'github-issue-dispatch'
 delivery=accept(msg,source_ref='github-owner-issue',source_commit=source_commit,source_path='coordination-inbox/'+mid+'.json')
 if (delivery.get('status') or '').startswith('REJECTED'):raise RuntimeError('durable_inbox_rejected:'+str(delivery.get('status')))
 try:
  result=execute_with_plane(msg)
 except Exception as exc:
  detail=getattr(exc,'result',None)
  failure=detail if isinstance(detail,dict) else {'error':type(exc).__name__+':'+str(exc)}
  try:
   from coordination_worker import _mark_execution_fail
   _mark_execution_fail(mid,failure)
  except Exception:
   pass
  safe={k:(str(v)[-3200:] if isinstance(v,str) else v) for k,v in failure.items() if k in
        {'ok','code','error','failed_index','failed_command','failed_returncode','failed_stdout','failed_stderr'}}
  return {'ok':False,'status':'failed','message_id':mid,'failure':safe,'completion_evidence':False}
 proof=plane.status(mid)
 if not result.get('ok') or not proof.get('completion_evidence'):
  return {'ok':False,'status':'failed','message_id':mid,'execution':proof.get('task',{}).get('status'),'completion_evidence':False,'result':str(result)[:3500]}
 old=results.latest(mid)
 receipt=old if (result.get('replayed') and old and old.get('task_status')=='PASS') else results.build(mid,'PASS',result,proof,attempt=1,terminal=True,evidence_refs=evidence_for(msg))
 if not (result.get('replayed') and old and old.get('task_status')=='PASS'):results.record(receipt)
 rows=result.get('results') or []
 return {'ok':True,'status':'completed','message_id':mid,'delivery_status':delivery.get('delivery_status') or delivery.get('status'),
         'execution':(proof.get('task') or {}).get('status'),'completion_evidence':bool(proof.get('completion_evidence')),
         'receipt_sha256':receipt.get('receipt_sha256'),'replayed':bool(result.get('replayed')),
         'commands':[{'index':x.get('index'),'returncode':x.get('returncode'),'stdout_tail':str(x.get('stdout') or '')[-3000:],'stderr_tail':str(x.get('stderr') or '')[-1500:]} for x in rows]}

def inspect_canonical_mail(args):
 # Read-only diagnostics for one known, immutable coordination message.
 mid=str(args.get('message_id') or '').strip()
 if not re.fullmatch(r'[A-Za-z0-9_.-]{1,120}',mid):raise ValueError('invalid_coordination_message_id')
 path=HERE.parents[1]/'coordination-inbox'/f'{mid}.json'
 if not path.is_file():raise FileNotFoundError('canonical_coordination_message_not_found:'+mid)
 from a2a_execution_plane import status as execution_status
 from pathlib import Path
 import shutil
 proof=Path.home()/'.dore'/'egm-p2-review-a0747bba9580'/'.dev'/'egm'/'p2-4fa21ce51444'
 def tail(path,limit=1800):
  try:return path.read_text(encoding='utf-8',errors='replace')[-limit:] if path.is_file() else None
  except OSError as exc:return type(exc).__name__
 p=execution_status(mid)
 task=p.get('task') or {}
 return {'ok':True,'status':'inspected','message_id':mid,
         'execution':{'status':task.get('status'),'attempts':task.get('attempts'),'completion_evidence':p.get('completion_evidence'),'failure':task.get('failure')},
         'runner':{'codex_path':shutil.which('codex'),'proof_present':proof.is_dir(),
                   'files':[x.name for x in proof.iterdir()] if proof.is_dir() else [],
                   'exit_code':tail(proof/'codex-exitcode.txt',120),
                   'plugin_list':tail(proof/'plugin-list.txt',1600),
                   'stderr_tail':tail(proof/'codex-stderr.log',2000)},
         'source_path':'coordination-inbox/'+mid+'.json'}

def post_issue_comment(payload):
 repo=os.environ.get('GITHUB_REPOSITORY','');number=(os.environ.get('DORE_REPLY_ISSUE_NUMBER') or '').strip();token=os.environ.get('GITHUB_TOKEN','')
 if not (repo and number and token):return None
 marker='[DORÉ_LOCAL_RESULT '+json.dumps(payload,ensure_ascii=False,separators=(',',':'))+']';raw=json.dumps({'body':marker},ensure_ascii=False).encode()
 if len(raw)>MAX_COMMENT_BYTES:raw=json.dumps({'body':'[DORÉ_LOCAL_RESULT '+json.dumps(fail('result_too_large'),separators=(',',':'))+']'}).encode()
 req=urllib.request.Request(f'https://api.github.com/repos/{repo}/issues/{number}/comments',data=raw,method='POST',headers={'Authorization':f'Bearer {token}','Accept':'application/vnd.github+json','X-GitHub-Api-Version':'2022-11-28','Content-Type':'application/json','User-Agent':'dore-a2a-github-entry'})
 with urllib.request.urlopen(req,timeout=20) as r:
  if r.status not in (200,201):raise RuntimeError(f'comment_http_{r.status}')
 return {'posted':True,'issue_number':number}

def main():
 try:
  request_id,capability,args=parse_command();timeout=CAPABILITY_TIMEOUTS.get(capability,360.0 if capability in LONG_CAPABILITIES else 15.0)
  if capability in {'coordination.mail-execute','coordination.mail-status'}:
   if not os.environ.get('DORE_REPLY_ISSUE_NUMBER'):raise PermissionError('owner_issue_required_for_canonical_mail')
   payload=execute_canonical_mail(args) if capability=='coordination.mail-execute' else inspect_canonical_mail(args)
   result={'ok':bool(payload.get('ok')),'protocol':PROTOCOL,'request_id':request_id,'capability':capability,'execution':payload}
  else:
   rpc=call('dore.call',{'capability':capability,'args':args,'request_id':request_id,'caller_product':'github-a2a','transport':'github'},timeout=timeout)
   semantic=rpc.get('result') if isinstance(rpc,dict) else None
   result={'ok':bool(isinstance(semantic,dict) and semantic.get('ok')),'protocol':PROTOCOL,'request_id':request_id,'capability':capability,'rpc':rpc}
 except Exception as exc:
  result=fail(f'{type(exc).__name__}:{exc}')
  detail=getattr(exc,'result',None)
  if isinstance(detail,dict):
   result['task_detail']={k:(str(v)[-3500:] if k in {'failed_stderr','failed_stdout','error'} else v) for k,v in detail.items() if k in {'failed_index','failed_returncode','failed_stderr','failed_stdout','error','code'}}
 print(json.dumps(result,ensure_ascii=False,indent=2));post_issue_comment(result);return 0 if result.get('ok') else 1
if __name__=='__main__':raise SystemExit(main())
