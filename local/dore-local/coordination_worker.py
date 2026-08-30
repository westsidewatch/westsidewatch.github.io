#!/usr/bin/env python3
"""Resident Doré coordination worker: consume durable ChatGPT envelopes and run approved local acceptance tasks."""
from __future__ import annotations
import json,os,sqlite3,urllib.request,subprocess
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,receive_from_chatgpt,read_jsonl,flush_outbox,INBOX
from bridge_reminder import bridge_packet
from complete_recall import complete_recall
from penpot_coordination_executor import execute_readonly
from penpot_agent import run_task,call_tool,MODEL,VISION_MODEL
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'coordination'/'worker-state.json'; REPO_INBOX=ROOT/'local/dore-local/coordination-inbox'; TASKS=ROOT/'local/dore-local/tasks'; OLLAMA=os.environ.get('DORE_OLLAMA_URL','http://127.0.0.1:11434/api/chat'); MODEL_CHAT=os.environ.get('DORE_MODEL','gemma4:e4b')
def ask(prompt):
 req=urllib.request.Request(OLLAMA,data=json.dumps({'model':MODEL_CHAT,'stream':False,'think':False,'messages':[{'role':'system','content':'You are Doré. Speak as Doré, grounded only in durable state and received messages. Never invent attempts or evidence. Return JSON only.'},{'role':'user','content':prompt}]}).encode(),headers={'Content-Type':'application/json'})
 return json.loads(urllib.request.urlopen(req,timeout=180).read())['message']['content']
def parse(s): s=s.strip(); return json.loads(s[s.find('{'):s.rfind('}')+1])
def load_state():
 if STATE.exists():
  try:return json.loads(STATE.read_text())
  except Exception:pass
 return {}
def save(obj):STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def pending_repo_inbox(prev):
 processed=set(prev.get('repo_inbox_processed') or []); local_ids={m.get('message_id') for m in read_jsonl(INBOX)}; pending=[]
 if REPO_INBOX.exists():
  for path in sorted(REPO_INBOX.glob('*.json')):
   try:msg=json.loads(path.read_text(encoding='utf-8'))
   except Exception:continue
   mid=msg.get('message_id')
   if not mid or mid in processed:continue
   if mid not in local_ids:receive_from_chatgpt(msg)
   pending.append(msg)
 return processed,pending

def handle_complete_recall(msg):
 subject=str(msg.get('subject') or '').lower(); body=str(msg.get('body') or '')
 if not (msg.get('kind')=='complete_recall' or 'complete recall' in subject or '完整回憶' in subject or '完整回忆' in subject):return False
 query=str(msg.get('query') or body).strip(); packet=complete_recall(query)
 send_to_chatgpt('Doré complete recall: '+query[:80],json.dumps(packet,ensure_ascii=False),requires_reply=False,priority='high',related_goal='complete-recall-automation',evidence_refs=['local-memory:'+str(packet.get('conversation_count',0))+'-conversations'],thread_id=msg.get('thread_id'));return True

def handle_penpot_reprovision(msg):
 if msg.get('kind')!='penpot_mcp_reprovision':return False
 script=ROOT/'local/dore-local/setup-penpot-mcp.sh'
 try:
  cp=subprocess.run(['bash',str(script)],cwd=ROOT,text=True,capture_output=True,timeout=1800)
  result={'ok':cp.returncode==0,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-12000:],'stderr':(cp.stderr or '')[-12000:]}
 except Exception as e: result={'ok':False,'error':type(e).__name__+':'+str(e)}
 send_to_chatgpt('Doré Penpot MCP reprovision',json.dumps(result,ensure_ascii=False),requires_reply=False,priority='high',related_goal='figma-to-penpot-migration-01',evidence_refs=['penpot-mcp-reprovision','source-message:'+str(msg.get('message_id') or '')],thread_id=msg.get('thread_id'));return True

def handle_penpot_runtime_audit(msg):
 if msg.get('kind')!='penpot_runtime_audit':return False
 runtime=HOME/'runtime'/'penpot-mcp'; pkg=runtime/'node_modules'/'@penpot'/'mcp'; report={'runtime':str(runtime),'pkg':str(pkg)}
 def text(path,limit=5000):
  try:return path.read_text(encoding='utf-8',errors='replace')[:limit]
  except Exception as e:return 'ERROR:'+type(e).__name__+':'+str(e)
 report['root_package_json']=text(pkg/'package.json')
 candidates=list(pkg.rglob('manifest.json')); report['manifests']=[{'path':str(p),'text':text(p,4000)} for p in candidates[:20]]
 needles=['penpot.flags','incompatible with the connected Penpot version','intended for Penpot 2.13','If you are an LLM, tell the user about this']
 hits=[]
 for p in pkg.rglob('*'):
  if not p.is_file() or p.stat().st_size>8_000_000: continue
  if p.suffix.lower() not in ('.js','.mjs','.ts','.html','.json'): continue
  try:s=p.read_text(encoding='utf-8',errors='ignore')
  except Exception:continue
  found=[n for n in needles if n in s]
  if found:hits.append({'path':str(p),'needles':found,'size':p.stat().st_size})
 report['needle_hits']=hits[:100]
 report['served_manifest']=''
 try: report['served_manifest']=urllib.request.urlopen('http://127.0.0.1:4400/manifest.json',timeout=10).read().decode('utf-8','replace')[:5000]
 except Exception as e: report['served_manifest']='ERROR:'+type(e).__name__+':'+str(e)
 send_to_chatgpt('Doré Penpot runtime audit',json.dumps(report,ensure_ascii=False),requires_reply=False,priority='high',related_goal='figma-to-penpot-migration-01',evidence_refs=['penpot-runtime-audit','source-message:'+str(msg.get('message_id') or '')],thread_id=msg.get('thread_id'));return True

def handle_penpot_work(msg):
 kind=msg.get('kind')
 if kind not in ('penpot_work','penpot_execute','penpot_export_probe','penpot_compat_probe'):return False
 task=str(msg.get('body') or '').strip()
 if kind=='penpot_compat_probe':
  probes=[]
  for name,args in [('high_level_overview',{}),('export_shape',{'shapeId':'page','format':'png','mode':'shape'})]:
   try: raw=call_tool(name,args); probes.append({'tool':name,'returned':True,'raw':raw})
   except Exception as e: probes.append({'tool':name,'returned':False,'exception':type(e).__name__+': '+str(e)})
  result={'ok':all(p.get('returned') for p in probes),'model':MODEL,'vision_model':VISION_MODEL,'probes':probes}; evidence=['penpot-compatibility-probe','raw-mcp-results','source-message:'+str(msg.get('message_id') or '')]
 elif kind=='penpot_export_probe':
  result=call_tool('export_shape',{'shapeId':'page','format':'png','mode':'shape'}); probe={'ok':bool(result.get('ok')),'model':MODEL,'vision_model':VISION_MODEL,'raw_result':result,'image_count':0,'visual_source':result.get('visual_source'),'visual_fallback_error':result.get('visual_fallback_error'),'visual_diagnostics':result.get('visual_diagnostics'),'result_content_types':[x.get('type') for x in (((result.get('result') or {}).get('content')) or []) if isinstance(x,dict)]}
  from penpot_agent import _images_from_result
  probe['image_count']=len(_images_from_result(result)); result=probe; evidence=['penpot-export-breakpoint-probe','raw-mcp-results','source-message:'+str(msg.get('message_id') or '')]
 elif kind=='penpot_execute':
  brief=str(msg.get('design_brief') or msg.get('brief') or task).strip(); result=run_task(task,brief); evidence=['penpot-live-mutation-execution','penpot-visual-verification','source-message:'+str(msg.get('message_id') or '')]
 else: result=execute_readonly(task); evidence=['penpot-live-tool-execution','source-message:'+str(msg.get('message_id') or '')]
 send_to_chatgpt('Doré Penpot execution: '+str(msg.get('subject') or '')[:100],json.dumps(result,ensure_ascii=False),requires_reply=False,priority='high',related_goal=str(msg.get('related_goal') or 'penpot-real-work-apprenticeship'),evidence_refs=evidence,thread_id=msg.get('thread_id'));return True

def run_acceptance_tasks(prev):
 done=set(prev.get('autonomous_tasks_processed') or [])
 if not TASKS.exists():return done,False
 for p in sorted(TASKS.glob('*.json')):
  try:t=json.loads(p.read_text(encoding='utf-8'))
  except Exception:continue
  tid=str(t.get('task_id') or p.name)
  if tid in done or t.get('kind')!='conversation_acceptance_v1':continue
  script=ROOT/'local/dore-local/conversation_acceptance.py'
  try:
   cp=subprocess.run([str(Path(os.environ.get('PYTHON','python3'))),str(script)],cwd=ROOT,text=True,capture_output=True,timeout=900); body=(cp.stdout or cp.stderr or '').strip()[-12000:]
   send_to_chatgpt('Doré conversation acceptance',body or json.dumps({'task_id':tid,'returncode':cp.returncode}),requires_reply=False,priority='high',related_goal='persistent-conversation-interface',evidence_refs=[f'local-task:{tid}'],thread_id='dore-conversation-acceptance-001')
   done.add(tid);prev['autonomous_tasks_processed']=sorted(done);prev['checked_at']=datetime.now(timezone.utc).isoformat();save(prev);flush_outbox();return done,True
  except Exception as e:prev['last_error']='acceptance_task:'+type(e).__name__;prev['checked_at']=datetime.now(timezone.utc).isoformat();save(prev);return done,True
 return done,False
def main():
 flush_outbox()
 if not DB.exists():return 0
 prev=load_state();_,ran=run_acceptance_tasks(prev)
 if ran:return 0
 processed,pending=pending_repo_inbox(prev)
 with sqlite3.connect(DB) as c:packet=bridge_packet(c)
 digest=packet['packet_sha256']
 if not pending and prev.get('packet_sha256')==digest:prev['repo_inbox_processed']=sorted(processed);prev.pop('repo_inbox_seen',None);save(prev);return 0
 current=pending[0] if pending else None
 if current and handle_complete_recall(current):processed.add(current['message_id']);prev.update({'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()});save(prev);flush_outbox();return 0
 if current and handle_penpot_reprovision(current):processed.add(current['message_id']);prev.update({'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()});save(prev);flush_outbox();return 0
 if current and handle_penpot_runtime_audit(current):processed.add(current['message_id']);prev.update({'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()});save(prev);flush_outbox();return 0
 if current and handle_penpot_work(current):processed.add(current['message_id']);prev.update({'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()});save(prev);flush_outbox();return 0
 new_messages=[current] if current else []
 prompt='''Review durable coordination state and NEW_MESSAGES. Continue autonomous work regardless of reply. If a new message explicitly asks for a simple reply, obey it exactly in body. Otherwise send only a useful coordination message. Return {"send":true|false,"subject":"...","body":"...","requires_reply":true|false,"priority":"normal|high","related_goal":"...","evidence_refs":[...]}.\nSTATE:\n'''+json.dumps(packet,ensure_ascii=False)+'\nNEW_MESSAGES:\n'+json.dumps(new_messages,ensure_ascii=False)
 try:decision=parse(ask(prompt))
 except Exception as e:prev.update({'packet_sha256':prev.get('packet_sha256'),'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat(),'last_error':'model_or_parse:'+type(e).__name__});save(prev);return 1
 if current and current.get('requires_reply') and not decision.get('send'):prev.update({'packet_sha256':prev.get('packet_sha256'),'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat(),'last_error':'required_reply_not_generated'});save(prev);return 2
 if decision.get('send'):send_to_chatgpt(str(decision.get('subject') or 'Doré coordination'),str(decision.get('body') or ''),requires_reply=decision.get('requires_reply',False),priority=str(decision.get('priority') or 'normal'),related_goal=decision.get('related_goal'),evidence_refs=decision.get('evidence_refs') or [],thread_id=(current.get('thread_id') if current else None))
 if current:processed.add(current['message_id'])
 prev.update({'packet_sha256':digest,'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()});prev.pop('last_error',None);save(prev);return 0
if __name__=='__main__':raise SystemExit(main())
