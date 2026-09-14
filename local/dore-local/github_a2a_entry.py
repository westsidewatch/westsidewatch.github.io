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
  rpc=call('dore.call',{'capability':capability,'args':args,'request_id':request_id,'caller_product':'github-a2a','transport':'github'},timeout=timeout)
  result={'ok':'result' in rpc,'protocol':PROTOCOL,'request_id':request_id,'capability':capability,'rpc':rpc}
 except Exception as exc:result=fail(f'{type(exc).__name__}:{exc}')
 print(json.dumps(result,ensure_ascii=False,indent=2));post_issue_comment(result);return 0 if result.get('ok') else 1
if __name__=='__main__':raise SystemExit(main())
