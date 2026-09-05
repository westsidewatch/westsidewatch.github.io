#!/usr/bin/env python3
"""Doré coordination ingress with autonomous-loop handoff."""
from __future__ import annotations
import fcntl,json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,flush_outbox,receive_from_chatgpt
from a2a_delivery_plane import DELIVERY as DELIVERY_ROOT,durable_messages,sync as sync_delivery
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool
from autonomous_capability_loop import attempt_learning_recovery
from goal_queue import enqueue
from peer_collaboration import respond as peer_respond
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve();STATE=HOME/'coordination'/'worker-state.json';LOCK=HOME/'coordination'/'worker.lock';REPO_INBOX=ROOT/'local/dore-local/coordination-inbox';MAX_PER_RUN=max(1,int(os.environ.get('DORE_COORDINATION_MAX_PER_RUN','20')));MAX_ATTEMPTS=max(1,int(os.environ.get('DORE_COORDINATION_MAX_ATTEMPTS','3')))
ALLOWED_LOCAL_EXE={'python3','python','git','node','npm','npx','launchctl','ps','pgrep','pkill','cat','ls','pwd','test','mkdir','touch','cp','mv','chmod','bash'};PRIORITY={'critical':0,'high':1,'normal':2,'low':3}
class TaskResultError(RuntimeError):
 def __init__(self,result):self.result=result if isinstance(result,dict) else {'ok':False,'error':str(result)};super().__init__(str(self.result.get('cause') or self.result.get('error') or 'task_failed'))
def now():return datetime.now(timezone.utc).isoformat()
def load_state():
 try:return json.loads(STATE.read_text()) if STATE.exists() else {}
 except Exception:return {}
def save(s):STATE.parent.mkdir(parents=True,exist_ok=True);tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(s,ensure_ascii=False,indent=2));tmp.replace(STATE)
def set_task(state,mid,status,**extra):
 record=state.setdefault('tasks',{}).setdefault(mid,{});record.update({'status':status,'updated_at':now(),**extra});state['last_task_id']=mid;state['last_task_status']=status;save(state);return record
def pending(prev):
 done=set(prev.get('repo_inbox_processed') or []);out=[]
 for m in durable_messages(DELIVERY_ROOT):
  if m.get('message_id') and m['message_id'] not in done:out.append(m)
 durable_ids={m.get('message_id') for m in out}
 if REPO_INBOX.exists():
  for p in REPO_INBOX.glob('*.json'):
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except Exception:continue
   if m.get('message_id') and m['message_id'] not in done and m['message_id'] not in durable_ids:m['_source_name']=p.name;out.append(m)
 out.sort(key=lambda m:(PRIORITY.get(str(m.get('priority','normal')).lower(),2),0 if str(m.get('related_goal','')).startswith('dore-design') else 1,str(m.get('_source_name',''))))
 for m in out:m.pop('_source_name',None)
 return done,out
def run_script(name,timeout=1800):
 cp=subprocess.run(['python3',str(ROOT/'local/dore-local'/name)] if (ROOT/'local/dore-local'/name).exists() else ['python3',str(ROOT/'dore-design'/name)],cwd=ROOT,text=True,capture_output=True,timeout=timeout);result={'ok':cp.returncode==0,'returncode':cp.returncode,'stderr':(cp.stderr or '')[-12000:]}
 try:result.update(json.loads((cp.stdout or '').strip().splitlines()[-1]))
 except Exception:result['stdout']=(cp.stdout or '')[-20000:]
 return result
def product_monitor():
 try:return run_script('product_monitor.py',30)
 except Exception as e:return {'ok':False,'product_monitor':'UNKNOWN','error':type(e).__name__+': '+str(e)}
def reply(msg,result,evidence,status,attempt,terminal=False):
 mid=str(msg.get('message_id') or 'unknown');monitor=product_monitor();payload={'source_message_id':mid,'task_status':status,'attempt':attempt,'terminal':terminal,'transport':'PASS','execution':'PASS' if result.get('ok') else 'FAIL','product_monitor':monitor,'result':result};return send_to_chatgpt('Doré execution: '+str(msg.get('subject') or '')[:100],json.dumps(payload,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'dore-coordination'),evidence_refs=evidence+['source-message:'+mid],thread_id=msg.get('thread_id'),message_id='result-'+mid,metadata={'source_message_id':mid,'task_status':status,'attempt':attempt,'terminal':terminal,'product_monitor':monitor.get('product_monitor')})
def _safe_cwd(raw):
 p=Path(raw or ROOT).expanduser().resolve();roots=(ROOT.resolve(),HOME.resolve(),Path.home().resolve())
 if not any(p==r or r in p.parents for r in roots):raise RuntimeError('local_exec_cwd_outside_allowed_roots:'+str(p))
 return p
def local_exec(msg):
 if msg.get('sender')!='chatgpt':raise RuntimeError('local_exec_sender_not_authorized')
 commands=msg.get('commands') or []
 if not isinstance(commands,list) or not commands:raise RuntimeError('local_exec_commands_required')
 results=[]
 for i,item in enumerate(commands,1):
  if isinstance(item,list):argv=item;cwd=ROOT;timeout=120
  elif isinstance(item,dict):argv=item.get('argv') or [];cwd=_safe_cwd(item.get('cwd'));timeout=min(int(item.get('timeout') or 120),900)
  else:raise RuntimeError('local_exec_invalid_command')
  if not argv or not all(isinstance(x,str) for x in argv):raise RuntimeError('local_exec_invalid_argv')
  exe=Path(argv[0]).name
  if exe not in ALLOWED_LOCAL_EXE:raise RuntimeError('local_exec_executable_not_allowed:'+exe)
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout);row={'index':i,'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]};results.append(row)
  if cp.returncode!=0:return {'ok':False,'results':results,'failed_index':i,'failed_command':argv,'failed_returncode':cp.returncode,'failed_stdout':row['stdout'],'failed_stderr':row['stderr']}
 return {'ok':True,'results':results}
def peer_research_result(msg):
 receipt=receive_from_chatgpt(msg);rid=str((msg.get('metadata') or {}).get('research_id') or '');bridged=None
 if rid:
  research=HOME/'coordination'/'research';matches=list(research.glob(rid+'.json')) if research.exists() else []
  if matches:
   cp=subprocess.run(['python3',str(ROOT/'local/dore-local/peer_research_bridge.py'),str(matches[0])],cwd=ROOT,text=True,capture_output=True,timeout=60)
   try:bridged=json.loads((cp.stdout or '').strip().splitlines()[-1])
   except Exception:bridged={'ok':False,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-4000:],'stderr':(cp.stderr or '')[-4000:]}
 return {'ok':True,'receipt':receipt,'research_id':rid or None,'bridge':bridged}
def dispatch(msg):
 kind=msg.get('kind');task=str(msg.get('body') or msg.get('task') or '').strip()
 if isinstance(kind,str) and kind.startswith('peer_') and kind!='peer_research_result':return peer_respond(msg,ROOT)
 if kind=='maintenance.update':return run_script('maintenance_update.py',300)
 if kind=='dore_design_bakeoff':return run_script('dore_design_bakeoff.py')
 if kind=='dore_design_elimination':return run_script('dore_design_elimination.py',3600)
 if kind=='dore_design_framesmith_mcp_trial':return run_script('dore_design_framesmith_mcp_trial.py',1800)
 if kind=='dore_design_openpencil_trial':return run_script('dore_design_openpencil_trial.py')
 if kind=='local_exec':return local_exec(msg)
 if kind=='peer_research_result':return peer_research_result(msg)
 if kind=='complete_recall':return {'ok':True,'recall':complete_recall(str(msg.get('query') or task))}
 if kind in ('penpot_ai_kit_adoption','penpot_ai_kit_install'):raise RuntimeError('legacy_handler_not_loaded_in_goal_worker')
 if kind=='penpot_execute':return run_task(task,str(msg.get('design_brief') or msg.get('brief') or msg.get('task') or task).strip())
 if kind=='penpot_work':
  result=execute_readonly(task);return {'ok':bool(result.get('ok')),'penpot':result}
 if kind=='penpot_export_probe':
  result=call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'});return {'ok':bool(result.get('ok')),'penpot':result}
 raise RuntimeError('unsupported_kind:'+str(kind))
def evidence_for(msg):
 base=['coordination-hardening-v1','product-invariant-monitor','autonomous-capability-loop','resident-goal-queue','research-bridge-executable']
 if msg.get('kind')=='local_exec':base+=['dore-local-exec','local-self-repair']
 if msg.get('kind')=='maintenance.update':base+=['guarded-maintenance-update','fast-forward-only','dirty-worktree-refusal']
 return base
def _finish_pass(state,done,msg,result,attempt,evidence):
 mid=msg['message_id'];done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.pop('active_message_id',None);state.pop('last_error',None);state['last_success_message_id']=mid;state['last_result']=result;set_task(state,mid,'PASS',attempt=attempt,completed_at=now(),result=result);reply(msg,result,evidence,'PASS',attempt,True)
def handoff_research(state,done,msg,attempt,learning,failure_result):
 mid=msg['message_id'];goal=str(msg.get('related_goal') or mid);row=enqueue(mid,goal,priority=str(msg.get('priority') or 'normal').lower(),source='coordination_worker',metadata={'execution_kind':'coordination_message','message':msg,'project_loop':'A2A <-> coordination real work','requires_reply':bool(msg.get('requires_reply',True))});handoff={'ok':False,'state':'RESEARCH_QUEUED','learning':learning,'goal_queue':{'goal_id':row.get('goal_id'),'status':row.get('status')},'original_failure':failure_result,'parent_goal_preserved':True,'handoff_to_resident_runtime':True};done.add(mid);state['repo_inbox_processed']=sorted(done);state.setdefault('research_handoffs',{})[mid]={'at':now(),'goal':goal,'status':'RESEARCH_QUEUED'};state.get('attempts',{}).pop(mid,None);state.pop('active_message_id',None);set_task(state,mid,'RESEARCH_QUEUED',attempt=attempt,terminal=False,result=handoff);reply(msg,handoff,evidence_for(msg)+['research-required','goal-queue-handoff'],'LEARNING',attempt,False);return handoff
def main():
 LOCK.parent.mkdir(parents=True,exist_ok=True);lock=LOCK.open('w')
 try:fcntl.flock(lock.fileno(),fcntl.LOCK_EX|fcntl.LOCK_NB)
 except BlockingIOError:return 0
 flush_outbox();state=load_state();delivery=sync_delivery(skip_message_ids=set(state.get('repo_inbox_processed') or []));state['last_delivery_sync']={k:v for k,v in delivery.items() if k!='results'};done,queue=pending(state);state['queue_depth']=len(queue);state['checked_at']=now();save(state);failures=0
 for msg in queue[:MAX_PER_RUN]:
  mid=msg['message_id'];goal=str(msg.get('related_goal') or mid);attempt=(state.get('attempts') or {}).get(mid,0)+1;state.setdefault('attempts',{})[mid]=attempt;state['active_goal']=goal;state['active_message_id']=mid;set_task(state,mid,'RECEIVED',attempt=attempt,goal=goal,kind=msg.get('kind'));set_task(state,mid,'RUNNING',attempt=attempt,started_at=now())
  try:
   result=dispatch(msg);ok=not isinstance(result,dict) or result.get('ok',True)
   if ok:_finish_pass(state,done,msg,result,attempt,evidence_for(msg));continue
   raise TaskResultError(result)
  except Exception as e:
   err=type(e).__name__+': '+str(e);failure_result=e.result if isinstance(e,TaskResultError) else {'ok':False,'error':err};failure_result={**failure_result,'error':err,'parent_goal_preserved':True};learning=attempt_learning_recovery(msg,failure_result);failure_result['learning']=learning
   if learning.get('retry_parent'):
    set_task(state,mid,'LEARNING',attempt=attempt,learning=learning)
    try:
     resumed=dispatch(msg);resumed_ok=not isinstance(resumed,dict) or resumed.get('ok',True)
     if resumed_ok:
      resumed={**(resumed if isinstance(resumed,dict) else {'ok':True,'result':resumed}),'autonomous_recovery':learning,'resumed_parent_goal':True};_finish_pass(state,done,msg,resumed,attempt,evidence_for(msg)+['learning-skill:'+str(learning.get('selected_skill')),'parent-goal-resumed']);continue
     failure_result={'ok':False,'error':'parent_retry_after_learning_failed','result':resumed,'learning':learning,'parent_goal_preserved':True}
    except Exception as x:failure_result={'ok':False,'error':type(x).__name__+': '+str(x),'learning':learning,'parent_goal_preserved':True}
   if learning.get('state')=='RESEARCH_REQUIRED':handoff_research(state,done,msg,attempt,learning,failure_result);continue
   failures+=1;terminal=attempt>=MAX_ATTEMPTS;failure_result['recovery_required']=terminal;state['last_error']={'message_id':mid,'attempt':attempt,'error':failure_result.get('error','task_failed')[:1000]};state['last_result']=failure_result;status='FAIL' if terminal else 'RETRYING';set_task(state,mid,status,attempt=attempt,terminal=terminal,error=failure_result.get('error','task_failed')[:1000],completed_at=now() if terminal else None,result=failure_result)
   if terminal:
    done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.setdefault('terminal_failures',{})[mid]={'failed_at':now(),'attempts':attempt,'kind':msg.get('kind'),'error':failure_result.get('error','task_failed')[:1000],'result':failure_result};state.pop('active_message_id',None)
   reply(msg,failure_result,evidence_for(msg)+['coordination-worker-error'],'FAIL' if terminal else 'RETRYING',attempt,terminal)
 state['queue_depth']=max(0,len(queue)-min(len(queue),MAX_PER_RUN));state['checked_at']=now();save(state);return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
