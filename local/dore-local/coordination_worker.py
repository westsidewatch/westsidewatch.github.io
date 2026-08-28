#!/usr/bin/env python3
"""Resident Doré coordination worker: consume durable ChatGPT envelopes and speak asynchronously."""
from __future__ import annotations
import json,os,sqlite3,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,receive_from_chatgpt,read_jsonl,INBOX
from bridge_reminder import bridge_packet
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'coordination'/'worker-state.json'; REPO_INBOX=ROOT/'local/dore-local/coordination-inbox'; OLLAMA=os.environ.get('DORE_OLLAMA_URL','http://127.0.0.1:11434/api/chat'); MODEL=os.environ.get('DORE_MODEL','qwen3:8b')
def ask(prompt):
 req=urllib.request.Request(OLLAMA,data=json.dumps({'model':MODEL,'stream':False,'messages':[{'role':'system','content':'You are Doré. Speak as Doré, grounded only in durable state and received messages. Never invent attempts or evidence. Return JSON only.'},{'role':'user','content':prompt}]}).encode(),headers={'Content-Type':'application/json'})
 return json.loads(urllib.request.urlopen(req,timeout=180).read())['message']['content']
def parse(s):
 s=s.strip(); a=s.find('{'); b=s.rfind('}'); return json.loads(s[a:b+1])
def load_state():
 if STATE.exists():
  try:return json.loads(STATE.read_text())
  except Exception:pass
 return {}
def save(obj): STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps(obj,ensure_ascii=False,indent=2))
def consume_repo_inbox(prev):
 seen=set(prev.get('repo_inbox_seen') or []); local_ids={m.get('message_id') for m in read_jsonl(INBOX)}; pending=[]
 if REPO_INBOX.exists():
  for path in sorted(REPO_INBOX.glob('*.json')):
   try: msg=json.loads(path.read_text(encoding='utf-8'))
   except Exception: continue
   mid=msg.get('message_id')
   if not mid or mid in seen: continue
   if mid not in local_ids: receive_from_chatgpt(msg)
   seen.add(mid); pending.append(msg)
 return seen,pending
def main():
 if not DB.exists(): return 0
 prev=load_state(); seen,pending=consume_repo_inbox(prev)
 with sqlite3.connect(DB) as c: packet=bridge_packet(c)
 digest=packet['packet_sha256']
 if not pending and prev.get('packet_sha256')==digest:
  prev['repo_inbox_seen']=sorted(seen); save(prev); return 0
 prompt='''Review durable coordination state and NEW_MESSAGES. Continue autonomous work regardless of reply. If a new message explicitly asks for a simple reply, obey it exactly in body. Otherwise send only a useful coordination message. Return {"send":true|false,"subject":"...","body":"...","requires_reply":true|false,"priority":"normal|high","related_goal":"...","evidence_refs":[...]}.\nSTATE:\n'''+json.dumps(packet,ensure_ascii=False)+'\nNEW_MESSAGES:\n'+json.dumps(pending,ensure_ascii=False)
 try: decision=parse(ask(prompt))
 except Exception:
  save({'packet_sha256':prev.get('packet_sha256'),'repo_inbox_seen':sorted(seen),'checked_at':datetime.now(timezone.utc).isoformat(),'last_error':'model_or_parse'}); return 1
 if decision.get('send'):
  send_to_chatgpt(str(decision.get('subject') or 'Doré coordination'),str(decision.get('body') or ''),requires_reply=decision.get('requires_reply',False),priority=str(decision.get('priority') or 'normal'),related_goal=decision.get('related_goal'),evidence_refs=decision.get('evidence_refs') or [],thread_id=(pending[0].get('thread_id') if pending else None))
 save({'packet_sha256':digest,'repo_inbox_seen':sorted(seen),'checked_at':datetime.now(timezone.utc).isoformat()}); return 0
if __name__=='__main__': raise SystemExit(main())
