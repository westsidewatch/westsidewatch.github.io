#!/usr/bin/env python3
"""Canonical A2A execution receipt and result-delivery status.

Execution truth and delivery truth stay separate:
- an execution receipt proves what happened;
- mailbox delivery proves whether that receipt/result reached the peer.
A failed publish must never erase or mutate completed execution evidence.
"""
from __future__ import annotations
import hashlib,json,os
from datetime import datetime,timezone
from pathlib import Path

SCHEMA='dore.execution-receipt.v2'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=HOME/'a2a-results';RECEIPTS=ROOT/'execution-receipts.jsonl'

def now():return datetime.now(timezone.utc).isoformat()
def _canon(obj):return json.dumps(obj,ensure_ascii=False,sort_keys=True,separators=(',',':'))
def _sha(obj):return hashlib.sha256(_canon(obj).encode()).hexdigest()
def _read():
 if not RECEIPTS.exists():return []
 out=[]
 for line in RECEIPTS.read_text(encoding='utf-8').splitlines():
  try:out.append(json.loads(line))
  except Exception:pass
 return out

def build(source_message_id,task_status,result,execution_proof,*,attempt=1,terminal=False,evidence_refs=None,result_message_id=None):
 mid=str(source_message_id or '')
 if not mid:raise ValueError('source_message_id_required')
 proof=execution_proof if isinstance(execution_proof,dict) else {}
 task=proof.get('task') if isinstance(proof.get('task'),dict) else {}
 execution_state=str(task.get('status') or task_status or 'UNKNOWN')
 completion=bool(proof.get('completion_evidence'))
 if str(task_status)=='PASS' and not (execution_state=='PASS' and completion):raise ValueError('pass_requires_verified_completion_evidence')
 artifact=task.get('artifact') if isinstance(task.get('artifact'),dict) else None
 verification=task.get('verification') if isinstance(task.get('verification'),dict) else None
 result_obj=result if isinstance(result,dict) else {'value':result}
 receipt={'schema':SCHEMA,'source_message_id':mid,'result_message_id':result_message_id or 'result-'+mid,'task_status':str(task_status),'execution_state':execution_state,'completion_evidence':completion,'attempt':int(attempt),'terminal':bool(terminal),'result_sha256':_sha(result_obj),'artifact_sha256':(artifact or {}).get('sha256'),'verification_ok':bool((verification or {}).get('ok')),'evidence_refs':list(evidence_refs or []),'issued_at':now()}
 stable={k:v for k,v in receipt.items() if k not in {'issued_at','receipt_sha256'}};receipt['receipt_sha256']=_sha(stable)
 return receipt

def record(receipt):
 if not isinstance(receipt,dict) or receipt.get('schema')!=SCHEMA:raise ValueError('invalid_execution_receipt')
 mid=str(receipt.get('source_message_id') or '');digest=str(receipt.get('receipt_sha256') or '')
 if not mid or not digest:raise ValueError('execution_receipt_identity_required')
 key=(mid,int(receipt.get('attempt') or 0),str(receipt.get('task_status') or ''))
 for old in _read():
  oldkey=(str(old.get('source_message_id') or ''),int(old.get('attempt') or 0),str(old.get('task_status') or ''))
  if oldkey!=key:continue
  if old.get('receipt_sha256')==digest:return {'ok':True,'code':'EXECUTION_RECEIPT_REPLAY','receipt':old}
  raise ValueError('execution_receipt_identity_conflict:'+mid+':'+str(key[1])+':'+key[2])
 RECEIPTS.parent.mkdir(parents=True,exist_ok=True)
 with RECEIPTS.open('a',encoding='utf-8') as f:f.write(json.dumps(receipt,ensure_ascii=False,sort_keys=True)+'\n')
 return {'ok':True,'code':'EXECUTION_RECEIPT_RECORDED','receipt':receipt}

def latest(source_message_id):
 rows=[r for r in _read() if r.get('source_message_id')==source_message_id]
 return rows[-1] if rows else None

def delivery_status(source_message_id,mailbox):
 receipt=latest(source_message_id)
 if not receipt:return {'ok':False,'code':'EXECUTION_RECEIPT_NOT_FOUND','source_message_id':source_message_id}
 result_mid=receipt['result_message_id'];outbound=mailbox.outbound_status(result_mid)
 return {'ok':True,'schema':'dore.result-delivery-status.v1','source_message_id':source_message_id,'result_message_id':result_mid,'execution_receipt':receipt,'execution_complete':bool(receipt.get('completion_evidence')),'delivery':outbound,'delivered':bool(outbound.get('published'))}
