#!/usr/bin/env python3
"""Execute one preserved coordination message as a resident-runtime goal.

This lets the autonomous goal queue resume the exact original task after a
research detour instead of replacing it with a Storybook-specific action.
"""
from __future__ import annotations
import json, sys
from coordination_worker import dispatch

def execute(payload):
 msg=payload.get('message') if isinstance(payload,dict) else None
 if not isinstance(msg,dict) or not msg.get('message_id'):return {'ok':False,'error':'coordination_message_required'}
 try:
  result=dispatch(msg);ok=not isinstance(result,dict) or result.get('ok',True)
  return {'ok':bool(ok),'source_message_id':msg['message_id'],'result':result,'resumed_parent_goal':True}
 except Exception as e:return {'ok':False,'source_message_id':msg['message_id'],'error':type(e).__name__+': '+str(e),'resumed_parent_goal':True}
if __name__=='__main__':
 try:payload=json.loads(sys.stdin.read() or '{}');out=execute(payload)
 except Exception as e:out={'ok':False,'error':'executor_uncaught:'+repr(e)}
 print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 2)
