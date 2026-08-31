#!/usr/bin/env python3
"""Resident Doré coordination worker: execute bounded local tasks while preserving the active parent goal."""
from __future__ import annotations
import json,os,subprocess,traceback
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,flush_outbox
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();STATE=HOME/'coordination'/'worker-state.json';REPO_INBOX=ROOT/'local/dore-local/coordination-inbox';MAX_PER_RUN=max(1,int(os.environ.get('DORE_COORDINATION_MAX_PER_RUN','20')));MAX_ATTEMPTS=max(1,int(os.environ.get('DORE_COORDINATION_MAX_ATTEMPTS','3')))
ALLOWED_LOCAL_EXE={'python3','python','git','node','npm','npx','launchctl','ps','pgrep','pkill','cat','ls','pwd','test','mkdir','touch','cp','mv','chmod','bash'}
PRIORITY={'critical':0,'high':1,'normal':2,'low':3}
def load_state():
 try:return json.loads(STATE.read_text()) if STATE.exists() else {}
 except:return {}
def save(s):STATE.parent.mkdir(parents=True,exist_ok=True);STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def pending(prev):
 done=set(prev.get('repo_inbox_processed') or []);out=[]
 if REPO_INBOX.exists():
  for p in REPO_INBOX.glob('*.json'):
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except:continue
   if m.get('message_id') and m['message_id'] not in done:
    m['_source_name']=p.name;out.append(m)
 # Current critical work must not wait behind historical experiment files. Among equal
 # priority, newer numeric product tasks sort ahead of older lexical backlog.
 out.sort(key=lambda m:(PRIORITY.get(str(m.get('priority','normal')).lower(),2),0 if m.get('related_goal')=='dore-design-product' else 1,str(m.get('_source_name',''))))
 for m in out:m.pop('_source_name',None)
 return done,out
def reply(msg,result,evidence):
 send_to_chatgpt('Doré execution: '+str(msg.get('subject') or '')[:100],json.dumps(result,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'dore-coordination'),evidence_refs=evidence+['source-message:'+str(msg.get('message_id') or '')],thread_id=msg.get('thread_id'));flush_outbox()
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
def run_script(name,timeout=1800):
 cp=subprocess.run(['python3',str(ROOT/'local/dore-local'/name)],cwd=ROOT,text=True,capture_output=True,timeout=timeout);result={'ok':cp.returncode==0,'returncode':cp.returncode,'stderr':(cp.stderr or '')[-12000:]}
 try:result.update(json.loads((cp.stdout or '').strip().splitlines()[-1]))
 except:result['stdout']=(cp.stdout or '')[-20000:]
 return result
def dispatch(msg):
 kind=msg.get('kind');task=str(msg.get('body') or msg.get('task') or '').strip()
 if kind=='dore_design_bakeoff':result=run_script('dore_design_bakeoff.py');reply(msg,result,['design-equipment-discovery']);return result
 if kind=='dore_design_elimination':result=run_script('dore_design_elimination.py',3600);reply(msg,result,['dore-design-real-work-elimination']);return result
 if kind=='dore_design_framesmith_mcp_trial':result=run_script('dore_design_framesmith_mcp_trial.py',1800);reply(msg,result,['framesmith-mcp-real-work','westside-watch-artifact','render-edit-rerender']);return result
 if kind=='dore_design_openpencil_trial':result=run_script('dore_design_openpencil_trial.py');reply(msg,result,['openpencil-real-work']);return result
 if kind=='local_exec':result=local_exec(msg);reply(msg,result,['dore-local-exec','local-self-repair']);return result
 if kind=='complete_recall':result=complete_recall(str(msg.get('query') or task));reply(msg,result,['complete-recall']);return {'ok':True}
 if kind in ('penpot_ai_kit_adoption','penpot_ai_kit_install'):raise RuntimeError('legacy_handler_not_loaded_in_goal_worker')
 if kind=='penpot_execute':brief=str(msg.get('design_brief') or msg.get('brief') or msg.get('task') or task).strip();result=run_task(task,brief);reply(msg,result,['penpot-live-mutation-execution']);return result
 if kind=='penpot_work':reply(msg,execute_readonly(task),['penpot-live-tool-execution']);return {'ok':True}
 if kind=='penpot_export_probe':reply(msg,call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'}),['penpot-export-probe']);return {'ok':True}
 raise RuntimeError('unsupported_kind:'+str(kind))
def main():
 flush_outbox();state=load_state();done,queue=pending(state);failures=0
 for msg in queue[:MAX_PER_RUN]:
  mid=msg['message_id'];goal=str(msg.get('related_goal') or mid);state['active_goal']=goal;state['active_goal_status']='RUNNING';attempts=(state.get('attempts') or {}).get(mid,0)+1;state.setdefault('attempts',{})[mid]=attempts;state['active_message_id']=mid;save(state)
  try:
   result=dispatch(msg)
   if isinstance(result,dict) and not result.get('ok',True):raise RuntimeError(str(result.get('cause') or result.get('error') or 'task_failed'))
   done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.pop('last_error',None);state.pop('active_message_id',None);state['last_success_message_id']=mid;state['active_goal_status']='RUNNING_UNTIL_ACCEPTANCE';state['checked_at']=datetime.now(timezone.utc).isoformat();save(state)
  except Exception as e:
   failures+=1;terminal=attempts>=MAX_ATTEMPTS;state['last_error']={'message_id':mid,'attempt':attempts,'error':str(e)[:1000]};state.pop('active_message_id',None)
   if terminal:
    done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.setdefault('terminal_failures',{})[mid]={'failed_at':datetime.now(timezone.utc).isoformat(),'attempts':attempts,'kind':msg.get('kind'),'error':str(e)[:1000]};state['active_goal_status']='RECOVERY_REQUIRED';state['recovery_reason']='terminal_child_failed';state['recovery_goal']=goal
   save(state)
   try:reply(msg,{'ok':False,'message_id':mid,'attempt':attempts,'terminal':terminal,'parent_goal_preserved':True,'recovery_required':terminal,'exception':type(e).__name__+': '+str(e)},['coordination-worker-error','parent-goal-preserved'])
   except:pass
 return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
