#!/usr/bin/env python3
"""Doré Penpot execution loop.

Uses the official Penpot MCP endpoint through a tiny Node MCP client and keeps
visual acceptance external to the acting text model. No cloud AI is required.
"""
from __future__ import annotations
import base64, json, os, subprocess, urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
MCP_CLIENT = HERE / 'penpot-mcp' / 'client.mjs'
MCP_URL = os.environ.get('PENPOT_MCP_URL', 'http://127.0.0.1:4401/mcp')
OLLAMA = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('DORE_LOCAL_MODEL', 'qwen3:8b')
VISION_MODEL = os.environ.get('DORE_LOCAL_VISION_MODEL', 'qwen3-vl:8b')
MAX_STEPS = int(os.environ.get('DORE_PENPOT_MAX_STEPS', '16'))


def _node(op: str, payload=None):
    env = os.environ.copy(); env['PENPOT_MCP_URL'] = MCP_URL
    p = subprocess.run(
        ['node', str(MCP_CLIENT), op],
        input=json.dumps(payload or {}, ensure_ascii=False) if payload is not None else None,
        text=True, capture_output=True, env=env, timeout=90,
    )
    raw = (p.stdout or '').strip()
    try: data = json.loads(raw or '{}')
    except Exception: data = {'ok': False, 'error': raw or p.stderr or f'node exited {p.returncode}'}
    if p.returncode and data.get('ok') is not True: return data
    return data


def status():
    return _node('status')


def list_tools():
    r = _node('list')
    if not r.get('ok'): raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
    return r.get('tools') or []


def call_tool(name, arguments):
    return _node('call', {'name': name, 'arguments': arguments or {}})


def _ollama(messages, tools=None, model=None):
    body = {'model': model or MODEL, 'messages': messages, 'stream': False}
    if tools: body['tools'] = tools
    req = urllib.request.Request(OLLAMA + '/api/chat', data=json.dumps(body).encode(), headers={'Content-Type': 'application/json'})
    return json.loads(urllib.request.urlopen(req, timeout=300).read())['message']


def _as_ollama_tools(mcp_tools):
    out=[]
    for t in mcp_tools:
        schema=t.get('inputSchema') or {'type':'object','properties':{}}
        out.append({'type':'function','function':{'name':t['name'],'description':t.get('description') or '', 'parameters':schema}})
    return out


def _images_from_result(result):
    images=[]
    content=((result or {}).get('result') or {}).get('content') or []
    for block in content:
        if block.get('type') == 'image' and block.get('data'):
            images.append(block['data'])
    return images


def _text_from_result(result):
    content=((result or {}).get('result') or {}).get('content') or []
    bits=[]
    for block in content:
        if block.get('type') == 'text': bits.append(block.get('text',''))
        elif block.get('type') == 'image': bits.append('[image returned for external visual verification]')
        else: bits.append(json.dumps(block, ensure_ascii=False))
    return '\n'.join(bits) if bits else json.dumps(result, ensure_ascii=False)


def visual_verify(image_b64: str, task: str, design_brief: str):
    prompt = f'''You are Doré Visual Verifier. Judge the ACTUAL rendered Penpot image, not tool metadata.
Task: {task}
Current design brief:\n{design_brief}
Return strict JSON only with keys verdict (PASS or FAIL), problems (array), strengths (array), next_correction (string). PASS only when the visible composition is genuinely usable and satisfies the brief. Missing, blank, block-only, clipped, overlapped or obviously unfinished output is FAIL.'''
    msg=_ollama([{'role':'user','content':prompt,'images':[image_b64]}], model=VISION_MODEL)
    text=(msg.get('content') or '').strip()
    try:
        start=text.index('{'); end=text.rindex('}')+1; return json.loads(text[start:end])
    except Exception:
        return {'verdict':'FAIL','problems':['visual_verifier_invalid_json'],'strengths':[],'next_correction':text[:1500]}


def run_task(task: str, design_brief: str):
    tools=list_tools(); ollama_tools=_as_ollama_tools(tools)
    tool_names=[x['name'] for x in tools]
    system=f'''You are Doré acting as a Penpot design agent through live MCP tools.
You are working on the currently focused Penpot page. Do not claim success from tool/API success or layer creation.
First inspect the current page/file. Then make the requested design changes. After writes, obtain an ACTUAL rendered/exported image using an available Penpot tool whenever possible. Doré's external visual verifier will inspect any image returned and send a PASS/FAIL result back to you. If it says FAIL, correct the design and visually verify again. Do not declare completion unless the verifier has returned PASS. If the available MCP tools cannot produce visual evidence, report that as a blocker rather than claiming success.
Task: {task}
Current design brief:\n{design_brief}
Available Penpot tool names: {', '.join(tool_names)}'''
    messages=[{'role':'system','content':system},{'role':'user','content':task}]
    trace=[]; checks=[]
    for step in range(MAX_STEPS):
        msg=_ollama(messages, ollama_tools)
        assistant={'role':'assistant','content':msg.get('content') or ''}
        if msg.get('tool_calls'): assistant['tool_calls']=msg['tool_calls']
        messages.append(assistant)
        calls=msg.get('tool_calls') or []
        if not calls:
            verified=bool(checks and checks[-1].get('verdict')=='PASS')
            return {'ok':True,'verified':verified,'answer':msg.get('content') or '', 'visual_checks':checks,'trace':trace,'steps':step+1,'tool_count':len(tools)}
        for call in calls:
            fn=(call.get('function') or {}); name=fn.get('name'); args=fn.get('arguments') or {}
            result=call_tool(name,args); trace.append({'tool':name,'ok':bool(result.get('ok')),'arguments':args})
            tool_text=_text_from_result(result)
            messages.append({'role':'tool','tool_name':name,'content':tool_text})
            for image in _images_from_result(result):
                verdict=visual_verify(image,task,design_brief); checks.append(verdict)
                messages.append({'role':'user','content':'EXTERNAL DORÉ VISUAL VERIFICATION: '+json.dumps(verdict,ensure_ascii=False)+'. Continue correcting if FAIL; only finish after PASS.'})
    return {'ok':False,'verified':False,'error':'penpot_step_limit','visual_checks':checks,'trace':trace,'steps':MAX_STEPS,'tool_count':len(tools)}
