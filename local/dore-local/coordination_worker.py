#!/usr/bin/env python3
"""Resident Doré coordination worker: drain durable ChatGPT envelopes and execute bounded local repair tasks."""
from __future__ import annotations
import json,os,subprocess,traceback
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,flush_outbox
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); STATE=HOME/'coordination'/'worker-state.json'; REPO_INBOX=ROOT/'local/dore-local/coordination-inbox'; MAX_PER_RUN=int(os.environ.get('DORE_COORDINATION_MAX_PER_RUN','20'))
ALLOWED_LOCAL_EXE={'python3','python','git','node','npm','npx','launchctl','ps','pgrep','pkill','cat','ls','pwd','test','mkdir','touch','cp','mv','chmod','bash'}
def load_state():
 try:return json.loads(STATE.read_text()) if STATE.exists() else {}
 except:return {}
def save(s):STATE.parent.mkdir(parents=True,exist_ok=True);STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def pending(prev):
 done=set(prev.get('repo_inbox_processed') or []);out=[]
 if REPO_INBOX.exists():
  for p in sorted(REPO_INBOX.glob('*.json')):
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except:continue
   if m.get('message_id') and m['message_id'] not in done:out.append(m)
 return done,out
def reply(msg,result,evidence):
 send_to_chatgpt('Doré execution: '+str(msg.get('subject') or '')[:100],json.dumps(result,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'dore-coordination'),evidence_refs=evidence+['source-message:'+str(msg.get('message_id') or '')],thread_id=msg.get('thread_id'));flush_outbox()
def _safe_cwd(raw):
 p=Path(raw or ROOT).expanduser().resolve(); roots=(ROOT.resolve(),HOME.resolve(),Path.home().resolve())
 if not any(p==r or r in p.parents for r in roots):raise RuntimeError('local_exec_cwd_outside_allowed_roots:'+str(p))
 return p
def local_exec(msg):
 if msg.get('sender')!='chatgpt':raise RuntimeError('local_exec_sender_not_authorized')
 commands=msg.get('commands') or []
 if not isinstance(commands,list) or not commands:raise RuntimeError('local_exec_commands_required')
 results=[]
 for i,item in enumerate(commands,1):
  if isinstance(item,list): argv=item; cwd=ROOT; timeout=120
  elif isinstance(item,dict): argv=item.get('argv') or []; cwd=_safe_cwd(item.get('cwd')); timeout=min(int(item.get('timeout') or 120),900)
  else:raise RuntimeError('local_exec_invalid_command')
  if not argv or not all(isinstance(x,str) for x in argv):raise RuntimeError('local_exec_invalid_argv')
  exe=Path(argv[0]).name
  if exe not in ALLOWED_LOCAL_EXE:raise RuntimeError('local_exec_executable_not_allowed:'+exe)
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
  results.append({'index':i,'argv':argv,'cwd':str(cwd),'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]})
  if cp.returncode!=0:return {'ok':False,'results':results,'failed_index':i}
 return {'ok':True,'results':results}
def ai_kit_adopt(msg):
 target=HOME/'runtime'/'penpot-ai-kit';src='https://github.com/penpot/penpot-ai-kit.git';steps=[]
 try:
  if (target/'.git').exists():cp=subprocess.run(['git','-C',str(target),'pull','--ff-only'],text=True,capture_output=True,timeout=300)
  else:target.parent.mkdir(parents=True,exist_ok=True);cp=subprocess.run(['git','clone','--depth','1',src,str(target)],text=True,capture_output=True,timeout=300)
  steps.append({'step':'sync','ok':cp.returncode==0,'stdout':(cp.stdout or '')[-3000:],'stderr':(cp.stderr or '')[-3000:]})
  if cp.returncode:return {'ok':False,'target':str(target),'steps':steps}
  cp=subprocess.run(['node','scripts/install/detect-client.mjs'],cwd=target,text=True,capture_output=True,timeout=120);steps.append({'step':'preflight','ok':cp.returncode==0,'stdout':(cp.stdout or '')[-5000:],'stderr':(cp.stderr or '')[-3000:]})
  if cp.returncode:return {'ok':False,'target':str(target),'steps':steps}
  cp=subprocess.run(['node','scripts/install/install.mjs','--client','generic','--mode','none'],cwd=target,text=True,capture_output=True,timeout=600);steps.append({'step':'install','ok':cp.returncode==0,'stdout':(cp.stdout or '')[-8000:],'stderr':(cp.stderr or '')[-5000:]})
  if cp.returncode:return {'ok':False,'target':str(target),'steps':steps}
  manifest=Path.home()/'.penpot-ai-kit'/'install-manifest.json';steps.append({'step':'manifest','ok':manifest.exists(),'path':str(manifest)})
  overview=call_tool('high_level_overview',{});steps.append({'step':'mcp-overview','ok':bool(overview.get('ok'))})
  structure=call_tool('execute_code',{'code':'return penpotUtils.shapeStructure(penpot.currentPage.root, 1);'});steps.append({'step':'live-structure','ok':bool(structure.get('ok'))})
  return {'ok':all(x.get('ok') for x in steps),'target':str(target),'seed':str(Path.home()/'.penpot-ai-kit'),'steps':steps}
 except Exception as e:return {'ok':False,'target':str(target),'steps':steps,'exception':type(e).__name__+': '+str(e)}
def dispatch(msg):
 kind=msg.get('kind');task=str(msg.get('body') or msg.get('task') or '').strip()
 if kind=='local_exec':
  result=local_exec(msg);reply(msg,result,['dore-local-exec','local-self-repair']);
  if not result.get('ok'):raise RuntimeError('local_exec_failed')
  return
 if kind=='complete_recall':reply(msg,complete_recall(str(msg.get('query') or task)),['complete-recall']);return
 if kind in ('penpot_ai_kit_adoption','penpot_ai_kit_install'):
  result=ai_kit_adopt(msg);reply(msg,result,['penpot-ai-kit','official-upstream','live-mcp-verification']);
  if not result.get('ok'):raise RuntimeError('penpot_ai_kit_adoption_failed')
  return
 if kind=='penpot_execute':
  brief=str(msg.get('design_brief') or msg.get('brief') or msg.get('task') or task).strip();result=run_task(task,brief);reply(msg,result,['penpot-live-mutation-execution','penpot-visual-verification']);
  if not result.get('ok'):raise RuntimeError('penpot_execute_failed:'+str(result.get('error') or 'unknown'))
  return
 if kind=='penpot_work':reply(msg,execute_readonly(task),['penpot-live-tool-execution']);return
 if kind=='penpot_export_probe':reply(msg,call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'}),['penpot-export-probe']);return
 if kind=='penpot_mcp_reprovision':
  cp=subprocess.run(['bash',str(ROOT/'local/dore-local/setup-penpot-mcp.sh')],cwd=ROOT,text=True,capture_output=True,timeout=1800);reply(msg,{'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]},['penpot-mcp-reprovision']);return
 raise RuntimeError('unsupported_kind:'+str(kind))
def main():
 flush_outbox();state=load_state();done,queue=pending(state);failures=0
 for msg in queue[:MAX_PER_RUN]:
  mid=msg['message_id'];attempts=(state.get('attempts') or {}).get(mid,0)+1;state.setdefault('attempts',{})[mid]=attempts;state['active_message_id']=mid;save(state)
  try:
   dispatch(msg);done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.pop('last_error',None);state.pop('active_message_id',None);state['last_success_message_id']=mid;state['checked_at']=datetime.now(timezone.utc).isoformat();save(state)
  except Exception as e:
   failures+=1;state['last_error']={'message_id':mid,'attempt':attempts,'type':type(e).__name__,'error':str(e)[:1000],'traceback':traceback.format_exc()[-5000:]};state.pop('active_message_id',None);save(state)
   try:reply(msg,{'ok':False,'error':'coordination_dispatch_failed','message_id':mid,'attempt':attempts,'exception':type(e).__name__+': '+str(e)},['coordination-worker-error'])
   except:pass
   continue
 return 1 if failures else 0
if __name__=='__main__':raise SystemExit(main())
