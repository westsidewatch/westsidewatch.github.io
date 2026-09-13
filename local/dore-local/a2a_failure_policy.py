#!/usr/bin/env python3
"""Canonical failure taxonomy for the Universal Doré A2A Core.

This module gives delivery, execution and recovery one vocabulary. A failure is not
silently collapsed into FAIL: callers can distinguish retryable work, uncertain
side effects, poison input, research handoff and terminal failure.
"""
from __future__ import annotations
import json, os
from datetime import datetime, timezone
from pathlib import Path
from typing import Any

HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=HOME/'a2a-execution'
QUARANTINE=ROOT/'quarantine'
FAILURES=ROOT/'failure-events.jsonl'
VOCABULARY=('RETRYABLE','UNKNOWN','QUARANTINED','RESEARCH_REQUIRED','TERMINAL_FAIL')
TRANSIENT_CODES={'timeout','timed_out','temporarily_unavailable','connection_reset','connection_refused','rate_limited','lease_expired','worker_lost'}
POISON_CODES={'invalid_schema','invalid_payload','identity_conflict','unsafe_message_id','unsupported_schema','malformed_message','poison_message'}
RESEARCH_CODES={'retry_budget_exhausted','no_information_gain','capability_gap','research_required'}
TERMINAL_CODES={'policy_violation','authority_rejected','verification_failed','forbidden','not_authorized'}

def now():return datetime.now(timezone.utc).isoformat()
def _atomic(path,value):
 path.parent.mkdir(parents=True,exist_ok=True);tmp=path.with_suffix(path.suffix+'.tmp');tmp.write_text(json.dumps(value,ensure_ascii=False,sort_keys=True,indent=2)+'\n',encoding='utf-8');tmp.replace(path)
def _append(path,value):
 path.parent.mkdir(parents=True,exist_ok=True)
 with path.open('a',encoding='utf-8') as f:f.write(json.dumps(value,ensure_ascii=False,sort_keys=True)+'\n')
def _code(failure):
 if isinstance(failure,BaseException):return type(failure).__name__.lower()
 if isinstance(failure,dict):
  err=failure.get('error')
  if isinstance(err,dict) and err.get('code'):return str(err.get('code')).lower()
  return str(failure.get('code') or failure.get('status') or '').lower()
 return str(failure or '').lower()

def classify(failure:Any,*,descriptor:dict[str,Any]|None=None,binding:dict[str,Any]|None=None,attempt:int=1,max_attempts:int=3)->dict[str,Any]:
 descriptor=descriptor or {};binding=binding or {};code=_code(failure)
 side_effect=bool(descriptor.get('requires_verified_execution') or descriptor.get('side_effecting') or binding.get('kind')=='production-action')
 retry_safe=bool(descriptor.get('retry_safe',not side_effect))
 if code in POISON_CODES or any(x in code for x in ('schema','malformed','identity_conflict','unsafe_message')):
  state='QUARANTINED';reason='poison_or_invalid_input'
 elif code in RESEARCH_CODES or attempt>=max_attempts:
  state='RESEARCH_REQUIRED';reason='retry_budget_or_information_exhausted'
 elif code in TERMINAL_CODES:
  state='TERMINAL_FAIL';reason='non_retryable_policy_failure'
 elif side_effect and not retry_safe:
  state='UNKNOWN';reason='side_effect_outcome_not_safe_to_replay'
 elif code in TRANSIENT_CODES or any(x in code for x in ('timeout','temporar','connection','lease','worker_lost')):
  state='RETRYABLE';reason='transient_failure'
 else:
  state='TERMINAL_FAIL';reason='unclassified_non_retryable_failure'
 return {'state':state,'reason':reason,'code':code or 'unknown','retry_safe':retry_safe,'side_effecting':side_effect,'attempt':attempt,'max_attempts':max_attempts}

def record(task_id:str,failure:Any,classification:dict[str,Any],*,context:dict[str,Any]|None=None)->dict[str,Any]:
 if classification.get('state') not in VOCABULARY:raise ValueError('unknown_failure_state:'+str(classification.get('state')))
 row={'schema':'dore.a2a-failure-event.v1','at':now(),'task_id':str(task_id),'classification':dict(classification),'failure':failure if isinstance(failure,(dict,list,str,int,float,bool,type(None))) else {'type':type(failure).__name__,'message':str(failure)},'context':dict(context or {})}
 _append(FAILURES,row)
 if classification.get('state')=='QUARANTINED':_atomic(QUARANTINE/(str(task_id)+'.json'),row)
 return row

def decision(task_id:str,failure:Any,*,descriptor:dict[str,Any]|None=None,binding:dict[str,Any]|None=None,attempt:int=1,max_attempts:int=3,context:dict[str,Any]|None=None)->dict[str,Any]:
 c=classify(failure,descriptor=descriptor,binding=binding,attempt=attempt,max_attempts=max_attempts);event=record(task_id,failure,c,context=context);return {**c,'event':event}
