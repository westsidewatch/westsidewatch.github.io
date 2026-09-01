#!/usr/bin/env python3
"""Resident Doré coordination worker with canonical task lifecycle and result reporting."""
from __future__ import annotations
import json,os,subprocess
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,flush_outbox
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();STATE=HOME/'coordination'/'worker-state.json';REPO_INBOX=ROOT/'local/dore-local/coordination-inbox';MAX_PER_RUN=max(1,int(os.environ.get('DORE_COORDINATION_MAX_PER_RUN','20')));MAX_ATTEMPTS=max(1,int(os.environ.get('DORE_COORDINATION_MAX_ATTEMPTS','3')))
ALLOWED_LOCAL_EXE={'python3','python','git','node','npm','npx','launchctl','ps','pgrep','pkill','cat','ls','pwd','test','mkdir','touch','cp','mv','chmod','bash'};PRIORITY={'critical':0,'high':1,'normal':2,'low':3}
def now():return datetime.now(timezone.utc).isoformat()
def load_state():
 try:return json.loads(STATE.read_text()) if STATE.exists() else {}
 except:return {}
def save(s):STATE.parent.mkdir(parents=True,exist_ok=True);tmp=STATE.with_suffix('.tmp');tmp.write_text(json.dumps(s,ensure_ascii=False,indent=2));tmp.replace(STATE)
def set_task(state,mid,status,**extra):
 tasks=state.setdefault('tasks',{});record=tasks.setdefault(mid,{});record.update({'status':status,'updated_at':now(),**extra});state['last_task_id']=mid;state['last_task_status']=status;save(state);return record
def pending(prev):
 done=set(prev.get('repo_inbox_processed') or []);out=[]
 if REPO_INBOX.exists():
  for p in REPO_INBOX.glob('*.json'):
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except:continue
   if m.get('message_id') and m['message_id'] not in done:m['_source_name']=p.name;out.append(m)
 out.sort(key=lambda m:(PRIORITY.get(str(m.get('priority','normal')).lower(),2),0 if str(m.get('related_goal','')).startswith('dore-design') else 1,str(m.get('_source_name',''))))
 for m in out:m.pop('_source_name',None)
 return done,out
def run_script(name,timeout=1800):
 cp=subprocess.run(['python3',str(ROOT/'local/dore-local'/name)] if (ROOT/'local/dore-local'/name).exists() else ['python3',str(ROOT/'dore-design'/name)],cwd=ROOT,text=True,capture_output=True,timeout=timeout);result={'ok':cp.returncode==0,'returncode':cp.returncode,'stderr':(cp.stderr or '')[-12000:]}
 try:result.update(json.loads((cp.stdout or '').strip().splitlines()[-1]))
 except:result['stdout']=(cp.stdout or '')[-20000:]
 return result
def product_monitor():
 try:return run_script('product_monitor.py',30)
 except Exception as e:return {'ok':False,'product_monitor':'UNKNOWN','error':type(e).__name__+': '+str(e)}
def reply(msg,result,evidence,status,attempt,terminal=False):
 mid=str(msg.get('message_id') or 'unknown');monitor=product_monitor();payload={'source_message_id':mid,'task_status':status,'attempt':attempt,'terminal':terminal,'transport':'PASS','execution':'PASS' if result.get('ok') else 'FAIL','product_monitor':monitor,'result':result}
 return send_to_chatgpt('Doré execution: '+str(msg.get('subject') or '')[:100],json.dumps(payload,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'dore-coordination'),evidence_refs=evidence+['source-message:'+mid],thread_id=msg.get('thread_id'),message_id='result-'+mid,metadata={'source_message_id':mid,'task_status':status,'attempt':attempt,'terminal':terminal,'product_monitor':monitor.get('product_monitor')})
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
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout);results.append({'index':i,'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]})
  if cp.returncode!=0:return {'ok':False,'results':results,'failed_index':i}
 return {'ok':True,'results':results}
def dispatch(msg):
 kind=msg.get('kind');task=str(msg.get('body') or msg.get('task') or '').strip()
 if kind=='dore_design_bakeoff':return run_script('dore_design_bakeoff.py')
 if kind=='dore_design_elimination':return run_script('dore_design_elimination.py',3600)
 if kind=='dore_design_framesmith_mcp_trial':return run_script('dore_design_framesmith_mcp_trial.py',1800)
 if kind=='dore_design_openpencil_trial':return run_script('dore_design_openpencil_trial.py')
 if kind=='local_exec':return local_exec(msg)
 if kind=='complete_recall':return {'ok':True,'recall':complete_recall(str(msg.get('query') or task))}
 if kind in ('penpot_ai_kit_adoption','penpot_ai_kit_install'):raise RuntimeError('legacy_handler_not_loaded_in_goal_worker')
 if kind=='penpot_execute':return run_task(task,str(msg.get('design_brief') or msg.get('brief') or msg.get('task') or task).strip())
 if kind=='penpot_work':return {'ok':True,'penpot':execute_readonly(task)}
 if kind=='penpot_export_probe':return {'ok':True,'penpot':call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'})}
 raise RuntimeError('unsupported_kind:'+str(kind))
def evidence_for(msg):
 kind=msg.get('kind');base=['coordination-hardening-v1','product-invariant-monitor']
 if kind=='local_exec':base+=['dore-local-exec','local-self-repair']
 return base
def main():
 flush_outbox();state=load_state();done,queue=pending(state);state['queue_depth']=len(queue);state['checked_at']=now();save(state);failures=0
 for msg in queue[:MAX_PER_RUN]:
  mid=msg['message_id'];goal=str(msg.get('related_goal') or mid);attempt=(state.get('attempts') or {}).get(mid,0)+1;state.setdefault('attempts',{})[mid]=attempt;state['active_goal']=goal;state['active_message_id']=mid;set_task(state,mid,'RECEIVED',attempt=attempt,goal=goal,kind=msg.get('kind'));set_task(state,mid,'RUNNING',attempt=attempt,started_at=now())
  try:
   result=dispatch(msg);ok=not isinstance(result,dict) or result.get('ok',True)
   if ok:
    done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.pop('active_message_id',None);state.pop('last_error',None);state['last_success_message_id']=mid;state['last_result']=result;set_task(state,mid,'PASS',attempt=attempt,completed_at=now(),result=result);reply(msg,result,evidence_for(msg),'PASS',attempt,True)
   else:raise RuntimeError(str(result.get('cause') or result.get('error') or 'task_failed'))
  except Exception as e:
   failures+=1;terminal=attempt>=MAX_ATTEMPTS;err=type(e).__name__+': '+str(e);state['last_error']={'message_id':mid,'attempt':attempt,'error':err[:1000]};state['last_result']={'ok':False,'error':err};status='FAIL' if terminal else 'RETRYING';set_task(state,mid,status,attempt=attempt,terminal=terminal,error=err[:1000],completed_at=now() if terminal else None)
   if terminal:
    done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.setdefault('terminal_failures',{})[mid]={'failed_at':now(),'attempts':attempt,'kind':msg.get('kind'),'error':err[:1000]};state.pop('active_message_id',None)
   reply(msg,{'ok':False,'error':err,'parent_goal_preserved':True,'recovery_required':terminal},evidence_for(msg)+['coordination-worker-error'],'FAIL' if terminal else 'RETRYING',attempt,terminal)
 state['queue_depth']=max(0,len(queue)-min(len(queue),MAX_PER_RUN));state['checked_at']=now();save(state);return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
