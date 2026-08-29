#!/usr/bin/env python3
"""Run one Penpot mutation task with durable progress events."""
from __future__ import annotations
import json, os, sys, time, traceback
from coordination_mailbox import send_to_chatgpt
import penpot_agent

MESSAGE_ID=os.environ.get('DORE_SOURCE_MESSAGE_ID','unknown')
THREAD_ID=os.environ.get('DORE_THREAD_ID') or 'penpot-progress'
GOAL=os.environ.get('DORE_RELATED_GOAL') or 'figma-to-penpot-migration-01'
_started=time.time()
_seq=0

def emit(stage, **data):
    global _seq
    _seq += 1
    payload={
        'source_message_id':MESSAGE_ID,
        'stage':stage,
        'sequence':_seq,
        'elapsed_seconds':round(time.time()-_started,3),
        **data,
    }
    try:
        send_to_chatgpt(
            f'Penpot progress: {MESSAGE_ID} — {stage}',
            json.dumps(payload,ensure_ascii=False),
            requires_reply=False,
            priority='high',
            related_goal=GOAL,
            evidence_refs=['penpot-live-progress','source-message:'+MESSAGE_ID],
            thread_id=THREAD_ID,
        )
    except Exception:
        pass

# Wrap the existing agent without changing its execution semantics.
_orig_ollama=penpot_agent._ollama
_orig_call_tool=penpot_agent.call_tool
_orig_visual_verify=penpot_agent.visual_verify

def observed_ollama(messages, tools=None, model=None):
    model_name=model or penpot_agent.MODEL
    emit('model_start', model=model_name, message_count=len(messages), tool_count=len(tools or []))
    try:
        out=_orig_ollama(messages,tools,model)
        emit('model_done', model=model_name, has_tool_calls=bool(out.get('tool_calls')))
        return out
    except Exception as e:
        emit('model_error', model=model_name, error=type(e).__name__+':'+str(e)[:500])
        raise

def observed_call_tool(name, arguments):
    emit('tool_start', tool=name, arguments=arguments or {})
    try:
        out=_orig_call_tool(name,arguments)
        content=((out or {}).get('result') or {}).get('content') or []
        image_count=sum(1 for b in content if isinstance(b,dict) and b.get('type')=='image' and b.get('data'))
        emit('tool_done', tool=name, ok=bool((out or {}).get('ok')), image_count=image_count)
        return out
    except Exception as e:
        emit('tool_error', tool=name, error=type(e).__name__+':'+str(e)[:500])
        raise

def observed_visual_verify(image_b64, task, design_brief):
    emit('visual_verify_start', image_bytes_estimate=(len(image_b64 or '')*3)//4, model=penpot_agent.VISION_MODEL)
    try:
        out=_orig_visual_verify(image_b64,task,design_brief)
        emit('visual_verify_done', verdict=out.get('verdict'), problems=out.get('problems') or [])
        return out
    except Exception as e:
        emit('visual_verify_error', error=type(e).__name__+':'+str(e)[:500])
        raise

penpot_agent._ollama=observed_ollama
penpot_agent.call_tool=observed_call_tool
penpot_agent.visual_verify=observed_visual_verify

def main():
    raw=sys.stdin.read()
    envelope=json.loads(raw or '{}')
    task=str(envelope.get('task') or '').strip()
    brief=str(envelope.get('design_brief') or task).strip()
    emit('runner_started', pid=os.getpid())
    try:
        result=penpot_agent.run_task(task,brief)
        emit('runner_finished', ok=bool(result.get('ok')), verified=bool(result.get('verified')), error=result.get('error'))
        print(json.dumps(result,ensure_ascii=False))
        return 0
    except Exception as e:
        emit('runner_crashed', error=type(e).__name__+':'+str(e)[:800])
        result={'ok':False,'verified':False,'error':'penpot_runner_exception:'+type(e).__name__+':'+str(e),'traceback':traceback.format_exc()[-4000:]}
        print(json.dumps(result,ensure_ascii=False))
        return 1

if __name__=='__main__':
    raise SystemExit(main())
