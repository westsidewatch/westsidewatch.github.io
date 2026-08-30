#!/usr/bin/env python3
"""Resident Doré coordination worker: reliably drain durable ChatGPT envelopes."""
from __future__ import annotations
import json,os,sqlite3,urllib.request,subprocess,time,traceback
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,receive_from_chatgpt,read_jsonl,flush_outbox,INBOX
from bridge_reminder import bridge_packet
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool,MODEL,VISION_MODEL
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'coordination'/'worker-state.json'; REPO_INBOX=ROOT/'local/dore-local/coordination-inbox'; OLLAMA=os.environ.get('DORE_OLLAMA_URL','http://127.0.0.1:11434/api/chat'); MODEL_CHAT=os.environ.get('DORE_MODEL','gemma4:e4b'); MAX_PER_RUN=int(os.environ.get('DORE_COORDINATION_MAX_PER_RUN','20'))
def load_state():
 try:return json.loads(STATE.read_text()) if STATE.exists() else {}
 except:return {}
def save(s):STATE.parent.mkdir(parents=True,exist_ok=True);STATE.write_text(json.dumps(s,ensure_ascii=False,indent=2))
def pending(prev):
 done=set(prev.get('repo_inbox_processed') or []); out=[]
 if REPO_INBOX.exists():
  for p in sorted(REPO_INBOX.glob('*.json')):
   try:m=json.loads(p.read_text(encoding='utf-8'))
   except:continue
   if m.get('message_id') and m['message_id'] not in done:out.append(m)
 return done,out
def reply(msg,result,evidence):
 send_to_chatgpt('Doré execution: '+str(msg.get('subject') or '')[:100],json.dumps(result,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'dore-coordination'),evidence_refs=evidence+['source-message:'+str(msg.get('message_id') or '')],thread_id=msg.get('thread_id'));flush_outbox()
def dispatch(msg):
 kind=msg.get('kind'); task=str(msg.get('body') or msg.get('task') or '').strip()
 if kind=='complete_recall':
  q=str(msg.get('query') or task); reply(msg,complete_recall(q),['complete-recall']); return
 if kind=='penpot_execute':
  brief=str(msg.get('design_brief') or msg.get('brief') or msg.get('task') or task).strip(); reply(msg,run_task(task,brief),['penpot-live-mutation-execution','penpot-visual-verification']); return
 if kind=='penpot_work':reply(msg,execute_readonly(task),['penpot-live-tool-execution']);return
 if kind=='penpot_export_probe':reply(msg,call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'}),['penpot-export-probe']);return
 if kind=='penpot_mcp_reprovision':
  cp=subprocess.run(['bash',str(ROOT/'local/dore-local/setup-penpot-mcp.sh')],cwd=ROOT,text=True,capture_output=True,timeout=1800);reply(msg,{'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]},['penpot-mcp-reprovision']);return
 raise RuntimeError('unsupported_kind:'+str(kind))
def main():
 flush_outbox()
 if not DB.exists():return 0
 state=load_state();done,queue=pending(state); processed_now=0
 for msg in queue[:MAX_PER_RUN]:
  mid=msg['message_id']; attempts=(state.get('attempts') or {}).get(mid,0)+1;state.setdefault('attempts',{})[mid]=attempts;state['active_message_id']=mid;state['checked_at']=datetime.now(timezone.utc).isoformat();save(state)
  try:
   dispatch(msg);done.add(mid);state['repo_inbox_processed']=sorted(done);state.get('attempts',{}).pop(mid,None);state.pop('last_error',None);state.pop('active_message_id',None);state['last_success_message_id']=mid;state['checked_at']=datetime.now(timezone.utc).isoformat();save(state);processed_now+=1
  except Exception as e:
   state['last_error']={'message_id':mid,'attempt':attempts,'type':type(e).__name__,'error':str(e)[:1000],'traceback':traceback.format_exc()[-5000:]};state.pop('active_message_id',None);state['checked_at']=datetime.now(timezone.utc).isoformat();save(state)
   try:reply(msg,{'ok':False,'error':'coordination_dispatch_failed','message_id':mid,'attempt':attempts,'exception':type(e).__name__+': '+str(e)},['coordination-worker-error'])
   except:pass
   return 1
 return 0
if __name__=='__main__':raise SystemExit(main())