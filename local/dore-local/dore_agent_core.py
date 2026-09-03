#!/usr/bin/env python3
"""Doré Agent Core v0.3 — autonomous reasoning/research/learning controller.

ChatGPT is an asynchronous conversation-activated peer. A pending peer request is
never a global stop condition: Doré checkpoints the handoff, keeps doing useful
local/free/OSS work, polls for a matching research_id reply on later wakes, and
only HUMAN_GATE may stop for a non-proxyable human decision/permission.

Storybook browser evidence is a first-class learning signal. Infrastructure PASS
may coexist with design-gate failures; those failures are checkpointed and fed
back into the next materially different local design hypothesis.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();CONTROL_ROOT=Path(os.environ.get('DORE_CONTROL_ROOT',ROOT)).expanduser();LOCAL=CONTROL_ROOT/'local'/'dore-local';LEARNING=HOME/'coordination'/'learning';RESEARCH=HOME/'coordination'/'research';A2A=CONTROL_ROOT/'dore-design'/'knowledge-lab'/'a2a';PROJECT_STATE=A2A/'project-state.json';DRIVER=LOCAL/'autonomous_driver.py';RESEARCH_EXECUTOR=LOCAL/'research_executor.py';PEER_BRIDGE=LOCAL/'peer_research_bridge.py'
sys.path.insert(0,str(LOCAL))
VERSION='dore.agent-core.v0.6'
ALT_RESEARCH_HINTS=[
 'Search a different local Knowledge Lab/skill/failure-memory path before repeating execution.',
 'Search a different maintained OSS or official-documentation source family and extract an executable pattern.',
 'Compare at least two alternatives and run the smallest falsifiable Storybook experiment.',
 'Inspect current Storybook evidence and choose a materially different hypothesis rather than repeating the same build.',
]
def now():return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except Exception:return default
def atomic_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def fingerprint(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def default_goal():
 try:rel=(json.loads(PROJECT_STATE.read_text(encoding='utf-8')).get('active_relationship') or {})
 except Exception:rel={}
 return {'goal_id':os.environ.get('DORE_RUNTIME_PARENT_ID',str(rel.get('current_parent_message_id') or 'new-westside-storybook-real-loop-2')),'goal':os.environ.get('DORE_RUNTIME_PARENT_GOAL',str(rel.get('parent_product_goal') or 'New Westside visual construction')),'project_loop':str(rel.get('loop') or 'A2A <-> Storybook')}
def context():
 d=default_goal()
 try:
  from goal_queue import ensure_default,current
  ensure_default(d['goal_id'],d['goal'],project_loop=d['project_loop']);row=current() or {};meta=dict(row.get('metadata') or {});return {'goal_id':str(row.get('goal_id') or d['goal_id']),'goal':str(row.get('goal') or d['goal']),'project_loop':str(meta.get('project_loop') or d['project_loop']),'metadata':meta}
 except Exception:return d
def latest_learning(goal_id):
 p=LEARNING/f'{goal_id}.json'
 if p.exists():
  d=read_json(p)
  if isinstance(d,dict):return p,d
 if LEARNING.exists():
  for p in sorted(LEARNING.glob('*.json'),key=lambda x:x.stat().st_mtime,reverse=True):
   d=read_json(p)
   if isinstance(d,dict) and d.get('state')=='RESEARCH_REQUIRED' and str(d.get('parent_source_message_id') or goal_id)==goal_id:return p,d
 return None,None
def synthetic_gap(ctx,result,question=None):
 LEARNING.mkdir(parents=True,exist_ok=True);p=LEARNING/f"{ctx['goal_id']}.json";diag={'returncode':result.get('returncode'),'stdout':(result.get('stdout') or '')[-5000:],'stderr':(result.get('stderr') or '')[-5000:],'result':result.get('result')};data={'schema':'dore.learning-evidence.v2','state':'RESEARCH_REQUIRED','created_at':now(),'parent_source_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'failure_fingerprint':fingerprint(diag),'question':question or 'Research the capability or knowledge gap exposed by this failed real-work attempt. Find new evidence before another experiment.','diagnostic':diag,'retry_parent':False};atomic_json(p,data);return p,data
def transition(p,job,state,**extra):
 h=list(job.get('history') or []);h.append({'at':now(),'state':state});job={**job,'state':state,'updated_at':now(),'history':h,**extra};atomic_json(p,job);return job
def ensure_job(ctx,learning):
 RESEARCH.mkdir(parents=True,exist_ok=True);failure=(learning or {}).get('failure_fingerprint') or fingerprint(learning or {'goal':ctx['goal_id']});rid=f"research-{ctx['goal_id']}-{fingerprint(failure)[:16]}";p=RESEARCH/f'{rid}.json';old=read_json(p,{}) or {}
 acceptance={'minimum_qualified_references':int((ctx.get('metadata') or {}).get('minimum_qualified_references') or 0),'minimum_source_families':int((ctx.get('metadata') or {}).get('minimum_source_families') or 0),'continuous':bool((ctx.get('metadata') or {}).get('continuous'))}
 if old:
  old['acceptance']=acceptance;atomic_json(p,old);return p,old
 q=((learning or {}).get('knowledge_request') or {}).get('question') or (learning or {}).get('question') or 'Find a mature evidence-backed repair, verify it in isolation, promote it, then resume this exact parent goal.';job={'schema':'dore.research-job.v0.4','research_id':rid,'state':'RESEARCH_QUEUED','created_at':now(),'updated_at':now(),'iteration':1,'parent_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'project_loop':ctx['project_loop'],'parent_goal_preserved':True,'failure_fingerprint':failure,'question':q,'preferred_sources':['local Knowledge Lab','verified skills/failure memory','official docs','maintained mature OSS','standards/specs'],'acceptance_test':'smallest falsifiable parent-specific experiment','promotion_target':'verified skill/failure-memory/shared-learning','human_gate':False,'peer_policy':'conversation-activated-nonblocking','acceptance':acceptance,'history':[{'at':now(),'state':'RESEARCH_QUEUED'}]};atomic_json(p,job);return p,job
def exec_json(script,args=(),timeout=600,input_text=None):
 if not script.exists():return {'ok':False,'error':'component_missing:'+str(script)}
 cp=subprocess.run([sys.executable,str(script),*map(str,args)],cwd=str(ROOT),text=True,capture_output=True,timeout=timeout,input=input_text);parsed=None
 try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:pass
 return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def drive(ctx,lp,learning,jp=None,job=None,reason='NO_USER_INPUT_CONTINUE'):
 msg={'schema':'dore.agent-core.v0.3','message_id':f'agent-{int(time.time())}','kind':'autonomous_driver','sender':'dore-agent-core','recipient':'dore','related_goal':ctx['goal'],'task':{'parent_source_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'project_loop':ctx['project_loop'],'trigger':reason,'learning_evidence':str(lp) if lp else None,'failure_fingerprint':(learning or {}).get('failure_fingerprint'),'research_job':str(jp) if jp else None,'knowledge_artifact':(job or {}).get('knowledge_artifact')}};return exec_json(DRIVER,timeout=1200,input_text=json.dumps(msg,ensure_ascii=False))
def remember(ctx,result,verified=False,resolution=None):
 try:
  from failure_memory import remember_failure
  return remember_failure(ctx['goal'],((result.get('stderr') or '')+'\n'+(result.get('stdout') or ''))[-6000:],evidence=result.get('result'),resolution=resolution,verified=verified)
 except Exception as e:return {'error':repr(e)}
def share(ctx,job,status,verification=None):
 try:
  from shared_learning import record
  a=(job or {}).get('knowledge_artifact') or {};return record(a,learned_by='dore',status=status,verification=verification,parent_goal=ctx['goal']) if a else None
 except Exception as e:return {'ok':False,'error':repr(e)}
def reject(ctx,jp,job,result):
 diag={'returncode':result.get('returncode'),'stdout':(result.get('stdout') or '')[-2500:],'stderr':(result.get('stderr') or '')[-2500:],'parsed':result.get('result')};job=transition(jp,{**job,'experiments':list(job.get('experiments') or [])+[{'at':now(),'status':'REJECTED','diagnostic':diag}],'failure_memory':remember(ctx,result)},'REJECTED');job={**job,'iteration':int(job.get('iteration') or 1)+1,'knowledge_artifact':None,'question':str(job.get('question') or '')+' New rejected-experiment evidence: '+json.dumps(diag,ensure_ascii=False)[-3000:]};return transition(jp,job,'RESEARCH_QUEUED')
def verified(ctx,jp,job,result):
 v={'at':now(),'signal':'parent-specific experiment passed','driver_result':result.get('result')};job=transition(jp,job,'VERIFIED',verification=v);s=share(ctx,job,'VERIFIED',v);parsed=result.get('result') if isinstance(result.get('result'),dict) else {};promotion=parsed.get('promoted_skills') or parsed.get('promoted_skill') or 'verified evidence retained';job=transition(jp,{**job,'shared_learning':s,'failure_memory':remember(ctx,result,True,promotion)},'PROMOTED',promotion=promotion);return transition(jp,job,'RESUME_PARENT',resumed=True)
def _source_count(result):
 best=0
 def walk(v):
  nonlocal best
  if isinstance(v,dict):
   if isinstance(v.get('source_count'),int):best=max(best,v['source_count'])
   for x in v.values():walk(x)
  elif isinstance(v,list):
   for x in v:walk(x)
 walk(result);return best
def _storybook_observation(result):
 parsed=result.get('result') if isinstance(result,dict) else None
 if not isinstance(parsed,dict):return None
 evidence=parsed.get('browser_evidence') or {}
 observation=evidence.get('observation') if isinstance(evidence,dict) else None
 if isinstance(observation,dict):return observation
 driver=parsed.get('driver') or {}
 for state in reversed(driver.get('states') or []):
  if isinstance(state,dict) and isinstance(state.get('observation'),dict):return state.get('observation')
 return None
def _failed_design_gates(observation):
 if not isinstance(observation,dict):return []
 gates=observation.get('gates') or {};design=['VISUAL_STABLE','RESPONSIVE_PASS','DESIGN_DISTINCT','WESTSIDE_FIT']
 return [name for name in design if gates.get(name) is False or gates.get(name)=='INSUFFICIENT_CANDIDATES']
def complete_goal(ctx,result):
 try:
  from goal_queue import set_status
  meta=ctx.get('metadata') or {};minimum=int(meta.get('minimum_qualified_references') or 0);prior=int(meta.get('current_qualified_references') or 0);count=max(prior,_source_count(result));observation=_storybook_observation(result);failed_design=_failed_design_gates(observation)
  if meta.get('continuous') and (count<minimum or failed_design):
   set_status(ctx['goal_id'],'ACTIVE',current_qualified_references=count,minimum_qualified_references=minimum,acceptance_met=False,last_activity_result=result.get('result'),last_design_observation=observation,failed_design_gates=failed_design)
   parts=[]
   if count<minimum:parts.append(f'qualified references remain {count}/{minimum}; expand qualified source families without discarding prior count')
   if failed_design:parts.append('Storybook design observation failed '+', '.join(failed_design)+'; choose a materially different design hypothesis and verify it with the next browser-evidence run')
   question='; '.join(parts)+'. Use local Knowledge Lab, verified skills and free/OSS references first. Do not wait for ChatGPT; keep any peer handoff non-blocking.'
   synthetic_gap(ctx,{'returncode':0,'stdout':question,'stderr':'','result':{'acceptance_met':False,'current_qualified_references':count,'minimum_qualified_references':minimum,'design_observation':observation,'failed_design_gates':failed_design}},question=question);return False
  set_status(ctx['goal_id'],'PASS',result=result.get('result'),acceptance_met=True,current_qualified_references=count,last_design_observation=observation,failed_design_gates=[]);return True
 except Exception:return False
def mark_active(ctx,result,**extra):
 try:
  from goal_queue import set_status
  return set_status(ctx['goal_id'],'ACTIVE',last_activity_result=result.get('result'),**extra)
 except Exception:return None
def a2a_task(ctx,state_name,**metadata):
 try:
  from a2a_adapter import dore_to_a2a_task
  return dore_to_a2a_task(source_message_id=ctx['goal_id'],parent_goal=ctx['goal'],state=state_name,metadata={'projectLoop':ctx['project_loop'],'agentCore':VERSION,'chatgptMode':'conversation-activated-peer',**metadata})
 except Exception as e:return {'error':repr(e)}
def semantic_driver_bound(ctx,result):
 if (ctx.get('metadata') or {}).get('execution_kind')!='coordination_message':return True
 parsed=result.get('result') if isinstance(result.get('result'),dict) else {};dispatched=((parsed.get('coordination_goal') or {}).get('result') or {})
 return bool(dispatched.get('ok')) and dispatched.get('reviewed_message_id')==ctx.get('goal_id') and dispatched.get('terminal_eligible') is not False
def record_nonblocking_attempt(jp,job,result):
 diag={'returncode':result.get('returncode'),'ok':bool(result.get('ok')),'stdout':(result.get('stdout') or '')[-1800:],'stderr':(result.get('stderr') or '')[-1800:],'result':result.get('result')};fp=fingerprint(diag);attempts=list(job.get('nonblocking_attempts') or []);previous=attempts[-1].get('fingerprint') if attempts else None;attempts.append({'at':now(),'fingerprint':fp,'driver_ok':bool(result.get('ok'))});attempts=attempts[-12:];same=fp==previous;iteration=int(job.get('autonomous_iteration') or 0)+1;job={**job,'nonblocking_attempts':attempts,'autonomous_iteration':iteration,'peer_request_pending':True,'peer_blocking':False,'last_autonomous_result':diag,'updated_at':now()}
 if same:
  hint=ALT_RESEARCH_HINTS[(iteration-1)%len(ALT_RESEARCH_HINTS)];job['question']=str(job.get('question') or '')+f'\nAutonomous information-gain iteration {iteration}: {hint}';job['history']=list(job.get('history') or [])+[{'at':now(),'state':'INFORMATION_GAIN_ROTATION','hint':hint}]
 atomic_json(jp,job);return job,same
def step():
 ctx=context();lp,learning=latest_learning(ctx['goal_id']);jp=job=None;events=[];peer_pending=False;rr=None;peer=None;agency_pre=None
 def emit(name,**extra):events.append({'at':now(),'event':name,**extra})
 try:
  from multi_loop_control_plane import agent_cycle
  control_plane=agent_cycle(ctx);emit('CONTROL_PLANE',**control_plane)
 except Exception as e:control_plane={'ok':False,'error':repr(e)};emit('CONTROL_PLANE_ERROR',error=repr(e))
 if control_plane.get('goal_pass'):
  emit('PASS',reason='incremental enrichment satisfied reference and source-family gates')
  return {'ok':True,'agent_core':VERSION,'state':'PASS','parent':ctx,'events':events,'continue':False,'peer_pending':False,'peer_blocking':False,'control_plane':control_plane,'a2a_task':a2a_task(ctx,'PASS',controlPlane='dore.multi-loop-control-plane.v1.0')}
 if learning and learning.get('state')=='RESEARCH_REQUIRED':
  jp,job=ensure_job(ctx,learning)
  if job.get('state') in {'RESEARCH_QUEUED','RESEARCHING','RESEARCH_BLOCKED'}:
   emit('RESEARCHING',research_id=job.get('research_id'));rr=exec_json(RESEARCH_EXECUTOR,[jp]);job=read_json(jp,job) or job;emit(job.get('state') or 'RESEARCHING',research_id=job.get('research_id'))
   if job.get('state') not in {'KNOWLEDGE_RETURNED','PEER_RESEARCH_QUEUED'}:return {'ok':True,'agent_core':VERSION,'state':job.get('state'),'parent':ctx,'research_job':job,'events':events,'continue':True,'research_diagnostic':rr,'a2a_task':a2a_task(ctx,job.get('state'))}
  if job.get('state')=='PEER_RESEARCH_QUEUED':
   from multi_loop_agency import checkpoint,peer_poll_due
   prior={'result':(ctx.get('metadata') or {}).get('last_activity_result')};agency_pre=checkpoint(ctx,prior,job)
   if peer_poll_due(agency_pre):peer=exec_json(PEER_BRIDGE,[jp],timeout=60);job=read_json(jp,job) or job;emit(job.get('state') or 'PEER_RESEARCH_QUEUED',research_id=job.get('research_id'))
   else:emit('PEER_WAIT_SLEEP',research_id=job.get('research_id'),until=agency_pre.get('peer_cooldown_until'))
   if job.get('state')!='KNOWLEDGE_RETURNED':
    peer_pending=True;job=transition(jp,job,'PEER_RESEARCH_QUEUED',peer_request_pending=True,peer_blocking=False,peer_mode='conversation-activated');emit('PENDING_PEER_NONBLOCKING',research_id=job.get('research_id'));reason=(agency_pre.get('decision') or {}).get('route') or 'PEER_PENDING_CONTINUE_AUTONOMOUS'
  if job.get('state')=='KNOWLEDGE_RETURNED':job=transition(jp,job,'EXPERIMENTING',peer_request_pending=False,peer_blocking=False);reason='KNOWLEDGE_RETURNED_EXPERIMENT';emit('EXPERIMENTING',research_id=job.get('research_id'))
  elif job.get('state')=='RESUME_PARENT':reason='RESUME_PARENT'
  elif not peer_pending:return {'ok':True,'agent_core':VERSION,'state':job.get('state'),'parent':ctx,'events':events,'continue':True}
 else:reason='NO_USER_INPUT_CONTINUE'
 emit('ACT',reason=reason)
 result=drive(ctx,lp,learning,None if peer_pending else jp,None if peer_pending else job,reason);emit('OBSERVE',driver_ok=bool(result.get('ok')),returncode=result.get('returncode'))
 if peer_pending and jp and job:
  from multi_loop_agency import checkpoint
  agency=checkpoint(ctx,result,job);job,same=record_nonblocking_attempt(jp,job,result);mark_active(ctx,result,pending_peer_research_id=job.get('research_id'),peer_blocking=False,autonomous_iteration=job.get('autonomous_iteration'),agency=agency);emit('MATERIAL_PROGRESS' if agency['assessment']['progress'] else 'REPEATED_ACTIVITY_NOT_PROGRESS',research_id=job.get('research_id'),iteration=job.get('autonomous_iteration'),agency=agency)
  if same and not agency['decision']['yield_peer']:
   emit('RESEARCHING_ALTERNATIVE',research_id=job.get('research_id'));rr2=exec_json(RESEARCH_EXECUTOR,[jp]);job=read_json(jp,job) or job;emit(job.get('state') or 'RESEARCHING',research_id=job.get('research_id'))
   if job.get('state')=='KNOWLEDGE_RETURNED':emit('KNOWLEDGE_RETURNED',research_id=job.get('research_id'))
  state='PENDING_PEER_NONBLOCKING' if job.get('state')!='KNOWLEDGE_RETURNED' else 'KNOWLEDGE_RETURNED'
  return {'ok':True,'agent_core':VERSION,'state':state,'parent':ctx,'driver_result':result,'research_job':job,'events':events,'continue':True,'peer_pending':True,'peer_blocking':False,'peer_diagnostic':peer,'research_diagnostic':rr,'a2a_task':a2a_task(ctx,state,peerBlocking=False,researchId=job.get('research_id'))}
 if jp and job:
  if result.get('ok'):
   if not semantic_driver_bound(ctx,result):
    result={**result,'ok':False,'error':'semantic_completion_binding_failed'};job=reject(ctx,jp,job,result);mark_active(ctx,result,acceptance_met=False,semantic_completion_rejected=True);state='RESEARCH_QUEUED';emit('SEMANTIC_COMPLETION_REJECTED');emit('RESEARCH_QUEUED')
    return {'ok':True,'agent_core':VERSION,'state':state,'parent':ctx,'driver_result':result,'research_job':job,'events':events,'continue':True,'peer_pending':False,'peer_blocking':False,'a2a_task':a2a_task(ctx,state)}
   done=complete_goal(ctx,result)
   if done:
    job=verified(ctx,jp,job,result);state='RESUME_PARENT';emit('VERIFIED');emit('PROMOTED');emit('RESUME_PARENT')
    if (ctx.get('metadata') or {}).get('execution_kind')=='coordination_message':
     try:
      from coordination_completion import complete
      completion=complete(ctx,job,result);emit('CANONICAL_COMPLETION_RECEIPT',**completion)
      if not completion.get('ok'):
       from goal_queue import set_status
       set_status(ctx['goal_id'],'ACTIVE',acceptance_met=False,completion_error=completion);job=transition(jp,job,'RESEARCH_QUEUED',completion_error=completion);state='RESEARCH_REQUIRED'
     except Exception as e:completion={'ok':False,'error':repr(e)};emit('COMPLETION_RECEIPT_FAILED',error=repr(e))
   else:job=transition(jp,{**job,'acceptance_unmet':True},'RESEARCH_QUEUED');state='RESEARCH_REQUIRED';emit('ACCEPTANCE_UNMET');emit('RESEARCH_QUEUED')
  else:job=reject(ctx,jp,job,result);state='RESEARCH_QUEUED';emit('REJECTED');emit('RESEARCH_QUEUED')
 elif result.get('ok'):
  done=complete_goal(ctx,result);state='PASS' if done else 'RESEARCH_REQUIRED';emit('PASS' if done else 'ACCEPTANCE_UNMET')
 else:
  lp,learning=synthetic_gap(ctx,result);state='RESEARCH_REQUIRED';emit('GAP_DETECTED',failure_fingerprint=learning.get('failure_fingerprint'));emit('RESEARCH_REQUIRED')
 return {'ok':True,'agent_core':VERSION,'state':state,'parent':ctx,'driver_result':result,'research_job':job,'events':events,'continue':state!='PASS','peer_pending':False,'peer_blocking':False,'a2a_task':a2a_task(ctx,state)}
if __name__=='__main__':
 try:out=step()
 except Exception as e:out={'ok':False,'agent_core':VERSION,'state':'AGENT_ERROR','error':repr(e),'continue':True}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
