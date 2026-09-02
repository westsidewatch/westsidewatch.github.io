#!/usr/bin/env python3
"""A2A Supervisor v0.2 — observes asynchronous Doré↔ChatGPT collaboration.

ChatGPT is conversation-activated. Its absence is normal and never freezes Doré.
The supervisor reports pending peer work as durable non-blocking state, while true
human gates remain explicit and project stalls trigger autonomous-recovery signals.
"""
from __future__ import annotations
import hashlib, json, os, sys
from datetime import datetime, timezone
from pathlib import Path
VERSION='dore.a2a-supervisor.v0.2'
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();BASE=HOME/'a2a-supervisor';STATE=BASE/'state.json';STALL_CYCLES=max(2,int(os.environ.get('DORE_A2A_STALL_CYCLES','3')))
def now():return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except Exception:return default
def atomic_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def fp(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def nested(d,*path):
 cur=d
 for key in path:
  if not isinstance(cur,dict):return None
  cur=cur.get(key)
 return cur
def observe(agent_envelope):
 parsed=(agent_envelope.get('result') or {}) if isinstance(agent_envelope,dict) else {};state=str(parsed.get('state') or 'UNKNOWN');parent=parsed.get('parent') or {};job=parsed.get('research_job') or {};driver=parsed.get('driver_result') or {};driver_result=driver.get('result') or {}
 peer_pending=bool(parsed.get('peer_pending')) or state in {'PEER_RESEARCH_QUEUED','PENDING_PEER_NONBLOCKING'} or bool(job.get('peer_request_pending'))
 human_gate=state=='HUMAN_GATE' or bool(job.get('human_gate'))
 diagnostic={'agent_state':state,'parent_goal_id':parent.get('goal_id'),'research_id':job.get('research_id'),'research_state':job.get('state'),'peer_pending':peer_pending,'peer_blocking':False if peer_pending else bool(parsed.get('peer_blocking')),'failure_fingerprint':job.get('failure_fingerprint'),'autonomous_iteration':job.get('autonomous_iteration'),'driver_error':driver_result.get('error') if isinstance(driver_result,dict) else None,'driver_returncode':driver.get('returncode'),'stderr_tail':str(driver.get('stderr') or nested(driver_result,'build','stderr') or '')[-1200:]}
 signature=fp(diagnostic);old=read_json(STATE,{}) or {};unchanged=(int(old.get('unchanged_cycles') or 0)+1) if old.get('signature')==signature else 1;continuing=bool(parsed.get('continue',True)) and state!='PASS';stalled=continuing and unchanged>=STALL_CYCLES and not peer_pending
 if state=='PASS':a2a_state='PROJECT_PASS';action='NONE';peer_required=False
 elif human_gate:a2a_state='A2A_HUMAN_GATE';action='HUMAN_DECISION_REQUIRED';peer_required=False
 elif peer_pending:a2a_state='A2A_PEER_PENDING_NONBLOCKING';action='CONTINUE_AUTONOMOUS_WORK';peer_required=True
 elif stalled:a2a_state='A2A_INTERVENE';action='AUTONOMOUS_RECOVERY_REQUIRED';peer_required=False
 elif unchanged>=max(2,STALL_CYCLES-1) and continuing:a2a_state='A2A_ATTENTION';action='WATCH_INFORMATION_GAIN';peer_required=False
 else:a2a_state='A2A_HEALTHY';action='NONE';peer_required=False
 out={'schema':'dore.a2a-supervision.v0.2','supervisor':VERSION,'at':now(),'authority':{'higher_loop':'Doré <-> ChatGPT asynchronous A2A','supervised_loop':str(parent.get('project_loop') or 'project continuation loop'),'rule':'Doré continues autonomous project work while ChatGPT is absent; A2A peer handoffs are durable and non-blocking.'},'a2a_state':a2a_state,'action_required':action,'peer_required':peer_required,'peer_blocking':False if peer_pending else None,'chatgpt_presence_required':False,'must_not_silently_observe':True,'unchanged_cycles':unchanged,'stall_threshold_cycles':STALL_CYCLES,'signature':signature,'diagnostic':diagnostic,'previous_a2a_state':old.get('a2a_state'),'user_gate':human_gate}
 atomic_json(STATE,out);return out
def main():
 raw=sys.stdin.read().strip();env=json.loads(raw) if raw else {};print(json.dumps({'ok':True,**observe(env)},ensure_ascii=False));return 0
if __name__=='__main__':raise SystemExit(main())
