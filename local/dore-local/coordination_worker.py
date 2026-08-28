#!/usr/bin/env python3
"""Give resident Doré a non-blocking chance to initiate dialogue with ChatGPT.

This worker never waits for ChatGPT. It asks the local Doré model whether current
open work contains a genuinely useful coordination message, and if so writes that
message to the durable outbox. Rate/dedup state prevents repetitive chatter.
"""
from __future__ import annotations
import hashlib,json,os,sqlite3,urllib.request
from datetime import datetime,timezone
from pathlib import Path
from coordination_mailbox import send_to_chatgpt
from bridge_reminder import bridge_packet
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser(); DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'coordination'/'worker-state.json'; OLLAMA=os.environ.get('DORE_OLLAMA_URL','http://127.0.0.1:11434/api/chat'); MODEL=os.environ.get('DORE_MODEL','qwen3:8b')
def ask(prompt):
 req=urllib.request.Request(OLLAMA,data=json.dumps({'model':MODEL,'stream':False,'messages':[{'role':'system','content':'You are Doré. Decide and speak as Doré, grounded only in supplied durable state. Never invent attempts or evidence. Return JSON only.'},{'role':'user','content':prompt}]}).encode(),headers={'Content-Type':'application/json'})
 return json.loads(urllib.request.urlopen(req,timeout=180).read())['message']['content']
def parse(s):
 s=s.strip(); a=s.find('{'); b=s.rfind('}'); return json.loads(s[a:b+1])
def main():
 if not DB.exists(): return 0
 with sqlite3.connect(DB) as c: packet=bridge_packet(c)
 digest=packet['packet_sha256']; prev={}
 if STATE.exists():
  try: prev=json.loads(STATE.read_text())
  except: pass
 # Speak when durable coordination state changed; never block autonomous work waiting for ChatGPT.
 if prev.get('packet_sha256')==digest: return 0
 prompt='''Review your durable coordination state below. Decide whether you have a useful message for ChatGPT now. This is asynchronous: continue autonomous work regardless of reply. Especially surface a real failure, uncertainty, contradiction, request for critique, or material progress. Do not merely restate policy. Return {"send":true|false,"subject":"...","body":"...","requires_reply":true|false,"priority":"normal|high","related_goal":"...","evidence_refs":[...]}.\nSTATE:\n'''+json.dumps(packet,ensure_ascii=False)
 try: decision=parse(ask(prompt))
 except Exception: return 1
 if decision.get('send'):
  send_to_chatgpt(str(decision.get('subject') or 'Doré coordination'),str(decision.get('body') or ''),requires_reply=decision.get('requires_reply',False),priority=str(decision.get('priority') or 'normal'),related_goal=decision.get('related_goal'),evidence_refs=decision.get('evidence_refs') or [])
 STATE.parent.mkdir(parents=True,exist_ok=True); STATE.write_text(json.dumps({'packet_sha256':digest,'checked_at':datetime.now(timezone.utc).isoformat()},indent=2)); return 0
if __name__=='__main__': raise SystemExit(main())
