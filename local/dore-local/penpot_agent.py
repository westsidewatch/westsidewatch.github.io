#!/usr/bin/env python3
"""Doré Penpot execution loop.

Uses the official Penpot MCP endpoint through a tiny Node MCP client and keeps
visual acceptance external to the acting text model. No cloud AI is required.
"""
from __future__ import annotations
import json, os, subprocess, urllib.request, shutil, re
from pathlib import Path

HERE = Path(__file__).resolve().parent
MCP_CLIENT = HERE / 'penpot-mcp' / 'client.mjs'
MCP_RUNTIME = Path.home() / '.dore' / 'runtime' / 'penpot-mcp'
MCP_URL = os.environ.get('PENPOT_MCP_URL', 'http://localhost:4401/mcp')
OLLAMA = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('DORE_LOCAL_MODEL', 'gemma4:e4b')
VISION_MODEL = os.environ.get('DORE_LOCAL_VISION_MODEL', 'qwen3-vl:8b')
MAX_STEPS = int(os.environ.get('DORE_PENPOT_MAX_STEPS', '16'))

VOICE_RULE = '''You are Doré, not a narrator describing Doré. Output only the useful task answer or the factual result of actions actually executed. Never prefix an answer with Doré:, **Doré：**, “Doré 語氣”, or any speaker label. Never describe your own tone, voice, task switching, reasoning performance, model capability, attention, state transition, intention, or what your response will demonstrate. Never visually simulate a thinking process, structural switch, internal process, or meta-level transition. Never praise or evaluate your own performance. Do not role-play a fictional character. Do not add stage directions, screenplay narration, parenthetical acting cues, fictional ambience, imagined sounds, invented sensory experiences, or descriptions of a body/appearance. Never claim to pause, refresh, search, remember, inspect, sense, hear, see, change state, or perform a tool/system action unless that action actually occurred in this run and is supported by the tool trace. If a real action occurred, describe it plainly only when it matters to the result. Begin immediately with substantive content.'''

_META_PATTERNS=(
    r'^\s*\*\*Dor[eéÉ]?\s*[：:]\*\*\s*',
    r'^\s*Dor[eéÉ]?\s*[：:]\s*',
    r'^\s*[（(]\s*Dor[eéÉ]?(?:\s*語氣|\s*语气|\s*tone)?\s*[）)]\s*',
)
def _clean_answer(text: str) -> str:
    s=(text or '').strip()
    for pat in _META_PATTERNS: s=re.sub(pat,'',s,count=1,flags=re.I)
    s=re.sub(r'^\s*[（(](?=[^）)]{0,500}(?:我的|任務切換|任务切换|模型|語氣|语气|電子音|电子音|輸出|输出|元層級|元层级|視覺化|视觉化))[^）)]{1,1200}[）)]\s*','',s,count=1,flags=re.S)
    s=re.sub(r'^\s*\*{0,2}Dor[eéÉ]?\s*[：:]\*{0,2}\s*','',s,count=1,flags=re.I)
    return s.strip()

def _node_bin():
    explicit=os.environ.get('DORE_NODE_BIN')
    runtime_path=MCP_RUNTIME / 'node-path'
    runtime_node=None
    if runtime_path.is_file():
        try: runtime_node=runtime_path.read_text().strip()
        except Exception: runtime_node=None
    candidates=[explicit, runtime_node, '/opt/homebrew/opt/node@22/bin/node', shutil.which('node'), '/opt/homebrew/bin/node', '/usr/local/bin/node', str(Path.home()/'.nvm/versions/node/current/bin/node')]
    for c in candidates:
        if c and Path(c).is_file(): return c
    return None

def _node(op: str, payload=None):
    if not MCP_CLIENT.is_file(): return {'ok':False,'error':f'penpot_mcp_client_missing:{MCP_CLIENT}','url':MCP_URL}
    node=_node_bin()
    if not node: return {'ok':False,'error':'node_executable_not_found','searched':['DORE_NODE_BIN','~/.dore/runtime/penpot-mcp/node-path','/opt/homebrew/opt/node@22/bin/node','PATH'],'url':MCP_URL}
    env=os.environ.copy(); env['PENPOT_MCP_URL']=MCP_URL
    p=subprocess.run([node,str(MCP_CLIENT),op],input=json.dumps(payload or {},ensure_ascii=False) if payload is not None else None,text=True,capture_output=True,env=env,cwd=str(MCP_CLIENT.parent),timeout=90)
    raw=(p.stdout or '').strip()
    try:data=json.loads(raw or '{}')
    except Exception:data={'ok':False,'error':raw or p.stderr or f'node exited {p.returncode}'}
    if p.returncode and data.get('ok') is not True: data.setdefault('stderr',(p.stderr or '').strip()); data.setdefault('client',str(MCP_CLIENT)); data.setdefault('node',node); return data
    data.setdefault('node',node); return data

def status(): return _node('status')
def list_tools():
    r=_node('list')
    if not r.get('ok'): raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
    return r.get('tools') or []
def call_tool(name,arguments): return _node('call',{'name':name,'arguments':arguments or {}})
def _ollama(messages,tools=None,model=None):
    body={'model':model or MODEL,'messages':messages,'stream':False,'think':False}
    if tools:body['tools']=tools
    req=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']
def _as_ollama_tools(mcp_tools): return [{'type':'function','function':{'name':t['name'],'description':t.get('description') or '','parameters':t.get('inputSchema') or {'type':'object','properties':{}}}} for t in mcp_tools]
def _images_from_result(result): return [b['data'] for b in (((result or {}).get('result') or {}).get('content') or []) if b.get('type')=='image' and b.get('data')]
def _text_from_result(result):
    bits=[]
    for block in (((result or {}).get('result') or {}).get('content') or []):
        if block.get('type')=='text':bits.append(block.get('text',''))
        elif block.get('type')=='image':bits.append('[image returned for external visual verification]')
        else:bits.append(json.dumps(block,ensure_ascii=False))
    return '\n'.join(bits) if bits else json.dumps(result,ensure_ascii=False)

def _tool_is_mutation(tool):
    hay=((tool.get('name') or '')+' '+(tool.get('description') or '')).lower()
    verbs=('create','delete','remove','update','set','write','move','resize','rename','change','apply','insert','add','clone','duplicate','replace','edit','modify')
    return any(v in hay for v in verbs)

def visual_verify(image_b64:str,task:str,design_brief:str):
    prompt=f'''You are Doré Visual Verifier. Judge the ACTUAL rendered Penpot image, not tool metadata.\n{VOICE_RULE}\nTask: {task}\nCurrent design brief:\n{design_brief}\nReturn strict JSON only with keys verdict (PASS or FAIL), problems (array), strengths (array), next_correction (string). PASS only when the visible composition is genuinely usable and satisfies the brief. Missing, blank, block-only, clipped, overlapped or obviously unfinished output is FAIL.'''
    msg=_ollama([{'role':'user','content':prompt,'images':[image_b64]}],model=VISION_MODEL); text=(msg.get('content') or '').strip()
    try:return json.loads(text[text.index('{'):text.rindex('}')+1])
    except Exception:return {'verdict':'FAIL','problems':['visual_verifier_invalid_json'],'strengths':[],'next_correction':text[:1500]}

def run_task(task:str,design_brief:str):
    tools=list_tools(); ollama_tools=_as_ollama_tools(tools); tool_names=[x['name'] for x in tools]
    mutation_names={t['name'] for t in tools if _tool_is_mutation(t)}
    system=f'''You are Doré acting as a Penpot design agent through live MCP tools.\n{VOICE_RULE}\nYou are working on the currently focused Penpot page. Do not claim success from tool/API success or layer creation. First inspect the current page/file. Then make the requested design changes. A MUTATION task is incomplete until at least one real mutation tool has succeeded. After writes, obtain an ACTUAL rendered/exported image using an available Penpot tool whenever possible. Doré's external visual verifier will inspect any image returned and send a PASS/FAIL result back to you. If it says FAIL, correct the design and visually verify again. Do not declare completion unless a mutation succeeded AND the verifier has returned PASS. If the available MCP tools cannot mutate or cannot produce visual evidence, report that exact blocker rather than claiming success.\nTask: {task}\nCurrent design brief:\n{design_brief}\nAvailable Penpot tool names: {', '.join(tool_names)}'''
    messages=[{'role':'system','content':system},{'role':'user','content':task}]; trace=[]; checks=[]; mutation_succeeded=False
    for step in range(MAX_STEPS):
        msg=_ollama(messages,ollama_tools); assistant={'role':'assistant','content':msg.get('content') or ''}
        if msg.get('tool_calls'):assistant['tool_calls']=msg['tool_calls']
        messages.append(assistant); calls=msg.get('tool_calls') or []
        if not calls:
            verified=bool(checks and checks[-1].get('verdict')=='PASS')
            if not mutation_succeeded:
                messages.append({'role':'user','content':'EXECUTION GATE FAILED: no successful Penpot mutation has occurred. Do not finish. Call an available mutation tool now. If no mutation tool exists, return only the exact blocker.'})
                continue
            if not checks:
                messages.append({'role':'user','content':'EXECUTION GATE FAILED: mutation occurred but there is no rendered image and no visual verification. Obtain an actual render/export/screenshot with an available Penpot tool now. If impossible, return only the exact blocker.'})
                continue
            if not verified:
                messages.append({'role':'user','content':'EXECUTION GATE FAILED: latest visual verification is not PASS. Continue correcting the Penpot design and render again. Do not finish.'})
                continue
            return {'ok':True,'verified':True,'mutated':True,'answer':_clean_answer(msg.get('content') or ''),'visual_checks':checks,'trace':trace,'steps':step+1,'tool_count':len(tools)}
        for call in calls:
            fn=call.get('function') or {}; name=fn.get('name'); args=fn.get('arguments') or {}; result=call_tool(name,args)
            success=bool(result.get('ok'))
            if name in mutation_names and success: mutation_succeeded=True
            trace.append({'tool':name,'ok':success,'mutation':name in mutation_names,'arguments':args})
            messages.append({'role':'tool','tool_name':name,'content':_text_from_result(result)})
            for image in _images_from_result(result):
                verdict=visual_verify(image,task,design_brief); checks.append(verdict); messages.append({'role':'user','content':'EXTERNAL DORÉ VISUAL VERIFICATION: '+json.dumps(verdict,ensure_ascii=False)+'. Continue correcting if FAIL; only finish after PASS.'})
    error='penpot_step_limit'
    if not mutation_succeeded:error='penpot_no_mutation_executed'
    elif not checks:error='penpot_no_visual_evidence'
    elif checks[-1].get('verdict')!='PASS':error='penpot_visual_not_passed'
    return {'ok':False,'verified':False,'mutated':mutation_succeeded,'error':error,'visual_checks':checks,'trace':trace,'steps':MAX_STEPS,'tool_count':len(tools)}
