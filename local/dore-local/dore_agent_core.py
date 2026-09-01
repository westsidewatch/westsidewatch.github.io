#!/usr/bin/env python3
"""Doré Agent Core v0.1 — owns reasoning, research, learning and next-action choice.

Runtime is deliberately not the agent. The Agent Core owns the stochastic/control
loop: observe -> detect gap -> research -> experiment -> verify -> promote ->
resume parent. The resident runtime only wakes this process, persists mechanical
state, supervises execution and publishes telemetry.
"""
from __future__ import annotations
import hashlib, json, os, subprocess, sys, time
from datetime import datetime, timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();LOCAL=ROOT/'local'/'dore-local';LEARNING=HOME/'coordination'/'learning';RESEARCH=HOME/'coordination'/'research';A2A=ROOT/'dore-design'/'knowledge-lab'/'a2a';PROJECT_STATE=A2A/'project-state.json';DRIVER=LOCAL/'autonomous_driver.py';RESEARCH_EXECUTOR=LOCAL/'research_executor.py';PEER_BRIDGE=LOCAL/'peer_research_bridge.py'
sys.path.insert(0,str(LOCAL))
VERSION='dore.agent-core.v0.1'
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
  ensure_default(d['goal_id'],d['goal'],project_loop=d['project_loop']);row=current() or {};return {'goal_id':str(row.get('goal_id') or d['goal_id']),'goal':str(row.get('goal') or d['goal']),'project_loop':str((row.get('metadata') or {}).get('project_loop') or d['project_loop'])}
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
def synthetic_gap(ctx,result):
 LEARNING.mkdir(parents=True,exist_ok=True);p=LEARNING/f"{ctx['goal_id']}.json";diag={'returncode':result.get('returncode'),'stdout':(result.get('stdout') or '')[-5000:],'stderr':(result.get('stderr') or '')[-5000:],'result':result.get('result')};data={'schema':'dore.learning-evidence.v2','state':'RESEARCH_REQUIRED','created_at':now(),'parent_source_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'failure_fingerprint':fingerprint(diag),'question':'Research the capability or knowledge gap exposed by this failed real-work attempt. Find new evidence before another experiment.','diagnostic':diag,'retry_parent':False};atomic_json(p,data);return p,data
def transition(p,job,state,**extra):
 h=list(job.get('history') or []);h.append({'at':now(),'state':state});job={**job,'state':state,'updated_at':now(),'history':h,**extra};atomic_json(p,job);return job
def ensure_job(ctx,learning):
 RESEARCH.mkdir(parents=True,exist_ok=True);failure=(learning or {}).get('failure_fingerprint') or fingerprint(learning or {'goal':ctx['goal_id']});rid=f"research-{ctx['goal_id']}-{fingerprint(failure)[:16]}";p=RESEARCH/f'{rid}.json';old=read_json(p,{}) or {}
 if old:return p,old
 q=((learning or {}).get('knowledge_request') or {}).get('question') or (learning or {}).get('question') or 'Find a mature evidence-backed repair, verify it in isolation, promote it, then resume this exact parent goal.';job={'schema':'dore.research-job.v0.3','research_id':rid,'state':'RESEARCH_QUEUED','created_at':now(),'updated_at':now(),'iteration':1,'parent_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'project_loop':ctx['project_loop'],'parent_goal_preserved':True,'failure_fingerprint':failure,'question':q,'preferred_sources':['local Knowledge Lab','verified skills/failure memory','official docs','maintained mature OSS','standards/specs'],'acceptance_test':'smallest falsifiable parent-specific experiment','promotion_target':'verified skill/failure-memory/shared-learning','human_gate':False,'history':[{'at':now(),'state':'RESEARCH_QUEUED'}]};atomic_json(p,job);return p,job
def exec_json(script,args=(),timeout=600,input_text=None):
 if not script.exists():return {'ok':False,'error':'component_missing:'+str(script)}
 cp=subprocess.run([sys.executable,str(script),*map(str,args)],cwd=str(ROOT),text=True,capture_output=True,timeout=timeout,input=input_text);parsed=None
 try:parsed=json.loads((cp.stdout or '').strip().splitlines()[-1])
 except Exception:pass
 return {'ok':cp.returncode==0 and isinstance(parsed,dict) and bool(parsed.get('ok')),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:],'result':parsed}
def drive(ctx,lp,learning,jp=None,job=None,reason='NO_USER_INPUT_CONTINUE'):
 msg={'schema':'dore.agent-core.v0.1','message_id':f'agent-{int(time.time())}','kind':'autonomous_driver','sender':'dore-agent-core','recipient':'dore','related_goal':ctx['goal'],'task':{'parent_source_message_id':ctx['goal_id'],'parent_goal':ctx['goal'],'project_loop':ctx['project_loop'],'trigger':reason,'learning_evidence':str(lp) if lp else None,'failure_fingerprint':(learning or {}).get('failure_fingerprint'),'research_job':str(jp) if jp else None,'knowledge_artifact':(job or {}).get('knowledge_artifact')}};return exec_json(DRIVER,timeout=1200,input_text=json.dumps(msg,ensure_ascii=False))
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
def complete_goal(ctx,result):
 try:
  from goal_queue import set_status
  set_status(ctx['goal_id'],'PASS',result=result.get('result'))
 except Exception:pass
def a2a_task(ctx,state_name):
 try:
  from a2a_adapter import dore_to_a2a_task
  return dore_to_a2a_task(source_message_id=ctx['goal_id'],parent_goal=ctx['goal'],state=state_name,metadata={'projectLoop':ctx['project_loop'],'agentCore':VERSION})
 except Exception as e:return {'error':repr(e)}
def step():
 ctx=context();lp,learning=latest_learning(ctx['goal_id']);jp=job=None;events=[]
 def emit(name,**extra):events.append({'at':now(),'event':name,**extra})
 if learning and learning.get('state')=='RESEARCH_REQUIRED':
  jp,job=ensure_job(ctx,learning)
  if job.get('state') in {'RESEARCH_QUEUED','RESEARCHING','RESEARCH_BLOCKED'}:
   emit('RESEARCHING',research_id=job.get('research_id'));rr=exec_json(RESEARCH_EXECUTOR,[jp]);job=read_json(jp,job) or job;emit(job.get('state') or 'RESEARCHING',research_id=job.get('research_id'))
   if job.get('state') not in {'KNOWLEDGE_RETURNED','PEER_RESEARCH_QUEUED'}:return {'ok':True,'agent_core':VERSION,'state':job.get('state'),'parent':ctx,'research_job':job,'events':events,'continue':True,'research_diagnostic':rr,'a2a_task':a2a_task(ctx,job.get('state'))}
  if job.get('state')=='PEER_RESEARCH_QUEUED':
   peer=exec_json(PEER_BRIDGE,[jp],timeout=60);job=read_json(jp,job) or job;emit(job.get('state') or 'PEER_RESEARCH_QUEUED',research_id=job.get('research_id'))
   if job.get('state')!='KNOWLEDGE_RETURNED':return {'ok':True,'agent_core':VERSION,'state':job.get('state'),'parent':ctx,'research_job':job,'events':events,'continue':True,'peer_diagnostic':peer,'a2a_task':a2a_task(ctx,job.get('state'))}
  if job.get('state')=='KNOWLEDGE_RETURNED':job=transition(jp,job,'EXPERIMENTING');reason='KNOWLEDGE_RETURNED_EXPERIMENT';emit('EXPERIMENTING',research_id=job.get('research_id'))
  elif job.get('state')=='RESUME_PARENT':reason='RESUME_PARENT'
  else:return {'ok':True,'agent_core':VERSION,'state':job.get('state'),'parent':ctx,'events':events,'continue':True}
 else:reason='NO_USER_INPUT_CONTINUE'
 emit('ACT',reason=reason);result=drive(ctx,lp,learning,jp,job,reason);emit('OBSERVE',driver_ok=bool(result.get('ok')),returncode=result.get('returncode'))
 if jp and job:
  if result.get('ok'):job=verified(ctx,jp,job,result);complete_goal(ctx,result);state='RESUME_PARENT';emit('VERIFIED');emit('PROMOTED');emit('RESUME_PARENT')
  else:job=reject(ctx,jp,job,result);state='RESEARCH_QUEUED';emit('REJECTED');emit('RESEARCH_QUEUED')
 elif result.get('ok'):complete_goal(ctx,result);state='PASS';emit('PASS')
 else:
  lp,learning=synthetic_gap(ctx,result);state='RESEARCH_REQUIRED';emit('GAP_DETECTED',failure_fingerprint=learning.get('failure_fingerprint'));emit('RESEARCH_REQUIRED')
 return {'ok':True,'agent_core':VERSION,'state':state,'parent':ctx,'driver_result':result,'research_job':job,'events':events,'continue':state!='PASS','a2a_task':a2a_task(ctx,state)}
if __name__=='__main__':
 try:out=step()
 except Exception as e:out={'ok':False,'agent_core':VERSION,'state':'AGENT_ERROR','error':repr(e),'continue':True}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
