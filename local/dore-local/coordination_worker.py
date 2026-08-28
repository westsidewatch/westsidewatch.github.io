#!/usr/bin/env python3
"""Resident Doré coordination worker: consume durable ChatGPT envelopes and speak asynchronously."""
from __future__ import annotations
import json,os,sqlite3,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt,receive_from_chatgpt,read_jsonl,flush_outbox,INBOX
from bridge_reminder import bridge_packet
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser(); DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'coordination'/'worker-state.json'; REPO_INBOX=ROOT/'local/dore-local/coordination-inbox'; OLLAMA=os.environ.get('DORE_OLLAMA_URL','http://127.0.0.1:11434/api/chat'); MODEL=os.environ.get('DORE_MODEL','qwen3:8b')
def ask(prompt):
 req=urllib.request.Request(OLLAMA,data=json.dumps({'model':MODEL,'stream':False,'messages':[{'role':'system','content':'You are Doré. Speak as Doré, grounded only in durable state and received messages. Never invent attempts or evidence. Return JSON only.'},{'role':'user','content':prompt}]}).encode(),headers={'Content-Type':'application/json'})
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
def main():
 flush_outbox()
 if not DB.exists():return 0
 prev=load_state(); processed,pending=pending_repo_inbox(prev)
 with sqlite3.connect(DB) as c:packet=bridge_packet(c)
 digest=packet['packet_sha256']
 if not pending and prev.get('packet_sha256')==digest:
  prev['repo_inbox_processed']=sorted(processed); prev.pop('repo_inbox_seen',None); save(prev); return 0
 # Process one durable letter/thread at a time. Discovery/receipt is NOT processing.
 current=pending[0] if pending else None
 new_messages=[current] if current else []
 prompt='''Review durable coordination state and NEW_MESSAGES. Continue autonomous work regardless of reply. If a new message explicitly asks for a simple reply, obey it exactly in body. Otherwise send only a useful coordination message. Return {"send":true|false,"subject":"...","body":"...","requires_reply":true|false,"priority":"normal|high","related_goal":"...","evidence_refs":[...]}.\nSTATE:\n'''+json.dumps(packet,ensure_ascii=False)+'\nNEW_MESSAGES:\n'+json.dumps(new_messages,ensure_ascii=False)
 try:decision=parse(ask(prompt))
 except Exception as e:
  save({'packet_sha256':prev.get('packet_sha256'),'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat(),'last_error':'model_or_parse:'+type(e).__name__}); return 1
 if current and current.get('requires_reply') and not decision.get('send'):
  save({'packet_sha256':prev.get('packet_sha256'),'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat(),'last_error':'required_reply_not_generated'}); return 2
 if decision.get('send'):
  send_to_chatgpt(str(decision.get('subject') or 'Doré coordination'),str(decision.get('body') or ''),requires_reply=decision.get('requires_reply',False),priority=str(decision.get('priority') or 'normal'),related_goal=decision.get('related_goal'),evidence_refs=decision.get('evidence_refs') or [],thread_id=(current.get('thread_id') if current else None))
 if current:processed.add(current['message_id'])
 save({'packet_sha256':digest,'repo_inbox_processed':sorted(processed),'checked_at':datetime.now(timezone.utc).isoformat()}); return 0
if __name__=='__main__':raise SystemExit(main())
