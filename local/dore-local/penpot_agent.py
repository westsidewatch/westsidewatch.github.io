#!/usr/bin/env python3
"""Doré Penpot execution loop with hard visual verification."""
from __future__ import annotations
import base64, json, os, re, shutil, subprocess, tempfile, urllib.request, uuid
from pathlib import Path

HERE = Path(__file__).resolve().parent
MCP_CLIENT = HERE / 'penpot-mcp' / 'client.mjs'
MCP_RUNTIME = Path.home() / '.dore' / 'runtime' / 'penpot-mcp'
MCP_URL = os.environ.get('PENPOT_MCP_URL', 'http://localhost:4401/mcp')
OLLAMA = os.environ.get('OLLAMA_BASE_URL', 'http://127.0.0.1:11434')
MODEL = os.environ.get('DORE_LOCAL_MODEL', 'gemma4:e4b')
VISION_MODEL = MODEL
MAX_STEPS = int(os.environ.get('DORE_PENPOT_MAX_STEPS', '16'))
EXPORT_DIR = MCP_RUNTIME / 'exports'

VOICE_RULE = '''You are Doré, not a narrator describing Doré. Output only useful task answers or factual results of actions actually executed. Never claim a tool/system action unless it actually occurred and is supported by the tool trace. Never role-play, narrate internal state, or claim success without evidence.'''
_META_PATTERNS=(r'^\s*\*\*Dor[eéÉ]?\s*[：:]\*\*\s*',r'^\s*Dor[eéÉ]?\s*[：:]\s*',r'^\s*[（(]\s*Dor[eéÉ]?(?:\s*語氣|\s*语气|\s*tone)?\s*[）)]\s*')

def _clean_answer(text:str)->str:
    s=(text or '').strip()
    for pat in _META_PATTERNS:s=re.sub(pat,'',s,count=1,flags=re.I)
    s=re.sub(r'^\s*\*{0,2}Dor[eéÉ]?\s*[：:]\*{0,2}\s*','',s,count=1,flags=re.I)
    return s.strip()

def _node_bin():
    explicit=os.environ.get('DORE_NODE_BIN'); runtime_path=MCP_RUNTIME/'node-path'; runtime_node=None
    if runtime_path.is_file():
        try: runtime_node=runtime_path.read_text().strip()
        except Exception: runtime_node=None
    for c in [explicit,runtime_node,'/opt/homebrew/opt/node@22/bin/node',shutil.which('node'),'/opt/homebrew/bin/node','/usr/local/bin/node',str(Path.home()/'.nvm/versions/node/current/bin/node')]:
        if c and Path(c).is_file(): return c
    return None

def _node(op:str,payload=None):
    if not MCP_CLIENT.is_file(): return {'ok':False,'error':f'penpot_mcp_client_missing:{MCP_CLIENT}','url':MCP_URL}
    node=_node_bin()
    if not node:return {'ok':False,'error':'node_executable_not_found','url':MCP_URL}
    env=os.environ.copy(); env['PENPOT_MCP_URL']=MCP_URL
    p=subprocess.run([node,str(MCP_CLIENT),op],input=json.dumps(payload or {},ensure_ascii=False) if payload is not None else None,text=True,capture_output=True,env=env,cwd=str(MCP_CLIENT.parent),timeout=90)
    raw=(p.stdout or '').strip()
    try:data=json.loads(raw or '{}')
    except Exception:data={'ok':False,'error':raw or p.stderr or f'node exited {p.returncode}'}
    if p.returncode and data.get('ok') is not True:
        data.setdefault('stderr',(p.stderr or '').strip()); data.setdefault('client',str(MCP_CLIENT)); data.setdefault('node',node); return data
    data.setdefault('node',node); return data

def _valid_png_b64(value:str)->bool:
    if not isinstance(value,str) or len(value)<16:return False
    try:return base64.b64decode(value,validate=True).startswith(b'\x89PNG\r\n\x1a\n')
    except Exception:return False

def _walk_images(value):
    out=[]
    if isinstance(value,dict):
        data=value.get('data')
        if value.get('type')=='image' and isinstance(data,str) and data:out.append(data)
        elif value.get('__type')=='base64' and isinstance(data,str) and _valid_png_b64(data):out.append(data)
        elif isinstance(data,str) and _valid_png_b64(data):out.append(data)
        for v in value.values():out.extend(_walk_images(v))
    elif isinstance(value,list):
        for v in value:out.extend(_walk_images(v))
    elif isinstance(value,str):
        s=value.strip()
        if s.startswith('data:image/') and ';base64,' in s:
            candidate=s.split(';base64,',1)[1]
            if _valid_png_b64(candidate):out.append(candidate)
        elif _valid_png_b64(s):out.append(s)
        elif s.startswith('{') or s.startswith('['):
            try:out.extend(_walk_images(json.loads(s)))
            except Exception:pass
    return out

def _images_from_result(result):
    seen=set(); out=[]
    for image in _walk_images(result or {}):
        if image not in seen:seen.add(image);out.append(image)
    return out

def _inject_png(result,data_b64,source,diagnostics=None):
    result=dict(result or {}); inner=result.get('result')
    if not isinstance(inner,dict):inner={}
    content=inner.get('content')
    if not isinstance(content,list):content=[]
    content.append({'type':'image','data':data_b64,'mimeType':'image/png'}); inner['content']=content
    result['result']=inner; result['visual_source']=source; result['ok']=True
    if diagnostics is not None:result['visual_diagnostics']=diagnostics
    return result

def _result_summary(result):
    try:
        inner=(result or {}).get('result') or {}; content=inner.get('content') or []
        return {'ok':bool((result or {}).get('ok')),'isError':inner.get('isError'),'content_types':[x.get('type') for x in content if isinstance(x,dict)],'text':[(x.get('text') or '')[:500] for x in content if isinstance(x,dict) and x.get('type')=='text'][:3]}
    except Exception as e:return {'summary_error':repr(e)}

def _export_file_fallback(arguments):
    EXPORT_DIR.mkdir(parents=True,exist_ok=True)
    attempts=[]
    candidates=[EXPORT_DIR/f'penpot-{uuid.uuid4().hex}.png',Path(tempfile.gettempdir())/f'dore-penpot-{uuid.uuid4().hex}.png']
    last=None
    for path in candidates:
        retry_args=dict(arguments or {}); retry_args['format']='png'; retry_args.setdefault('mode','shape'); retry_args['filePath']=str(path)
        retry=_node('call',{'name':'export_shape','arguments':retry_args}); last=retry
        exists=path.is_file(); size=path.stat().st_size if exists else 0
        diag={'path':str(path),'parent_exists':path.parent.exists(),'parent_writable':os.access(path.parent,os.W_OK),'exists':exists,'size':size,'mcp':_result_summary(retry)}
        attempts.append(diag)
        try:
            if retry.get('ok') and exists and size>0:
                raw=path.read_bytes()
                if raw.startswith(b'\x89PNG\r\n\x1a\n'):
                    return _inject_png(retry,base64.b64encode(raw).decode('ascii'),'filePath-fallback',attempts)
                diag['file_error']='not_png_magic'
            leaked=_images_from_result(retry)
            if leaked:return _inject_png(retry,leaked[0],'fallback-response-base64',attempts)
        finally:
            try:path.unlink(missing_ok=True)
            except Exception:pass
    last=dict(last or {'ok':False}); last['visual_fallback_error']='export_file_missing_empty_or_invalid'; last['visual_diagnostics']=attempts; return last

def status():return _node('status')
def list_tools():
    r=_node('list')
    if not r.get('ok'):raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
    return r.get('tools') or []

def call_tool(name,arguments):
    result=_node('call',{'name':name,'arguments':arguments or {}})
    if name=='export_shape' and bool(result.get('ok')) and not _images_from_result(result):return _export_file_fallback(arguments or {})
    return result

def _ollama(messages,tools=None,model=None):
    body={'model':model or MODEL,'messages':messages,'stream':False,'think':False}
    if tools:body['tools']=tools
    req=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']

def _as_ollama_tools(mcp_tools):return [{'type':'function','function':{'name':t['name'],'description':t.get('description') or '','parameters':t.get('inputSchema') or {'type':'object','properties':{}}}} for t in mcp_tools]
def _text_from_result(result):
    blocks=(((result or {}).get('result') or {}).get('content') or []); bits=[]
    for block in blocks:
        if block.get('type')=='text':bits.append(block.get('text',''))
        elif block.get('type')=='image':bits.append('[image returned for external visual verification]')
        else:bits.append(json.dumps(block,ensure_ascii=False))
    if result.get('visual_source'):bits.append('[visual source: '+str(result['visual_source'])+']')
    if result.get('visual_diagnostics'):bits.append('[visual diagnostics: '+json.dumps(result['visual_diagnostics'],ensure_ascii=False)+']')
    return '\n'.join(bits) if bits else json.dumps(result,ensure_ascii=False)

def visual_verify(image_b64:str,task:str,design_brief:str):
    prompt=f'''You are Doré Visual Verifier. Judge the ACTUAL rendered Penpot image, not tool metadata.\n{VOICE_RULE}\nTask: {task}\nCurrent design brief:\n{design_brief}\nReturn strict JSON only with keys verdict (PASS or FAIL), problems (array), strengths (array), next_correction (string). PASS only when the visible composition is genuinely usable and satisfies the brief. Missing, blank, block-only, clipped, overlapped or obviously unfinished output is FAIL.'''
    try:msg=_ollama([{'role':'user','content':prompt,'images':[image_b64]}],model=VISION_MODEL)
    except Exception as e:return {'verdict':'FAIL','problems':['visual_engine_error:'+type(e).__name__+':'+str(e)[:500]],'strengths':[],'next_correction':'Verify that the active Doré engine supports image input.','vision_model':VISION_MODEL}
    text=(msg.get('content') or '').strip()
    try:
        verdict=json.loads(text[text.index('{'):text.rindex('}')+1]); verdict.setdefault('vision_model',VISION_MODEL); return verdict
    except Exception:return {'verdict':'FAIL','problems':['visual_verifier_invalid_json'],'strengths':[],'next_correction':text[:1500],'vision_model':VISION_MODEL}

def _grounding_packet(tool_names):
    packet=[]
    if 'high_level_overview' in tool_names:
        r=call_tool('high_level_overview',{})
        packet.append({'tool':'high_level_overview','ok':bool(r.get('ok')),'text':_text_from_result(r)[:12000]})
    if 'penpot_api_info' in tool_names:
        for api_type in ('Penpot','Board','Rectangle','Text'):
            r=call_tool('penpot_api_info',{'type':api_type})
            packet.append({'tool':'penpot_api_info','type':api_type,'ok':bool(r.get('ok')),'text':_text_from_result(r)[:8000]})
    return packet

def _construction_code():
    return """
const page = penpot.currentPage;
const board = penpot.createBoard();
board.name = '02 — Westside Watch Homepage v0.1 — API Grounded';
board.x = 0; board.y = 0; board.resize(1440,1200);
board.fills = [{fillColor:'#FAF9F5', fillOpacity:1}];
page.appendChild(board);
const mast = penpot.createText('WESTSIDE WATCH');
mast.name='Masthead'; mast.x=96; mast.y=72; mast.fontSize='36'; mast.fills=[{fillColor:'#252525',fillOpacity:1}]; board.appendChild(mast);
const rule = penpot.createRectangle(); rule.name='First Light Rule'; rule.x=96; rule.y=140; rule.resize(1248,1); rule.fills=[{fillColor:'#A2872A',fillOpacity:1}]; board.appendChild(rule);
const title = penpot.createText('Watch for the Dawn');
title.name='Hero Title'; title.x=96; title.y=220; title.fontSize='88'; title.fills=[{fillColor:'#252525',fillOpacity:1}]; board.appendChild(title);
const sub = penpot.createText('A quiet editorial field for Scripture, witness, and watchfulness.');
sub.name='Hero Deck'; sub.x=100; sub.y=350; sub.fontSize='24'; sub.fills=[{fillColor:'#252525',fillOpacity:1}]; board.appendChild(sub);
const visual = penpot.createRectangle(); visual.name='5:8 Visual Field'; visual.x=900; visual.y=220; visual.resize(320,512); visual.fills=[{fillColor:'#102A43',fillOpacity:1}]; board.appendChild(visual);
const gold = penpot.createRectangle(); gold.name='Morning Accent'; gold.x=900; gold.y=748; gold.resize(320,20); gold.fills=[{fillColor:'#D2BC69',fillOpacity:1}]; board.appendChild(gold);
const body = penpot.createText('FEATURE / JOURNAL / PRAYER / BIBLE STUDY');
body.name='Editorial Passage'; body.x=96; body.y=880; body.fontSize='22'; body.fills=[{fillColor:'#252525',fillOpacity:1}]; board.appendChild(body);
penpot.save();
return {boardId: board.id, boardName: board.name};
"""

def _extract_board_id(result):
    text=_text_from_result(result)
    m=re.search(r'"boardId"\s*:\s*"([^"]+)"',text)
    if not m:m=re.search(r'boardId\s*[:=]\s*([0-9a-fA-F-]{16,})',text)
    return m.group(1) if m else None

def run_task(task:str,design_brief:str):
    tools=list_tools(); tool_names=[x['name'] for x in tools]
    grounding=_grounding_packet(tool_names)
    trace=[]; checks=[]
    for item in grounding:
        trace.append({'tool':item.get('tool'),'ok':item.get('ok',False),'mutation':False,'arguments':({'type':item.get('type')} if item.get('type') else {}),'image_count':0,'preflight':True})
    if 'execute_code' not in tool_names:
        return {'ok':False,'verified':False,'mutated':False,'error':'penpot_execute_code_missing','visual_checks':checks,'trace':trace,'steps':0,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}
    create=call_tool('execute_code',{'code':_construction_code()})
    create_ok=bool(create.get('ok'))
    board_id=_extract_board_id(create)
    trace.append({'tool':'execute_code','ok':create_ok,'mutation':True,'arguments':{'code':'[deterministic homepage construction]'},'image_count':len(_images_from_result(create)),'visual_source':create.get('visual_source'),'visual_diagnostics':create.get('visual_diagnostics'),'visual_fallback_error':create.get('visual_fallback_error'),'board_id':board_id})
    if not create_ok:
        return {'ok':False,'verified':False,'mutated':False,'error':'penpot_construction_failed','visual_checks':checks,'trace':trace,'steps':1,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}
    if not board_id:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_board_id_missing','visual_checks':checks,'trace':trace,'steps':1,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}
    if 'export_shape' not in tool_names:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_export_shape_missing','board_id':board_id,'visual_checks':checks,'trace':trace,'steps':1,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}
    exported=call_tool('export_shape',{'format':'png','mode':'shape','shapeId':board_id})
    images=_images_from_result(exported)
    trace.append({'tool':'export_shape','ok':bool(exported.get('ok')),'mutation':False,'arguments':{'format':'png','mode':'shape','shapeId':board_id},'image_count':len(images),'visual_source':exported.get('visual_source'),'visual_diagnostics':exported.get('visual_diagnostics'),'visual_fallback_error':exported.get('visual_fallback_error')})
    if not images:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_no_visual_evidence','board_id':board_id,'visual_checks':checks,'trace':trace,'steps':2,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}
    verdict=visual_verify(images[0],task,design_brief); checks.append(verdict)
    return {'ok':verdict.get('verdict')=='PASS','verified':verdict.get('verdict')=='PASS','mutated':True,'board_id':board_id,'answer':'Created and exported the API-grounded Westside Watch homepage board.' if verdict.get('verdict')=='PASS' else 'Created board but visual verification failed.','error':None if verdict.get('verdict')=='PASS' else 'penpot_visual_verification_failed','visual_checks':checks,'trace':trace,'steps':2,'tool_count':len(tools),'model':MODEL,'vision_model':VISION_MODEL}

if __name__=='__main__':
    print(json.dumps({'status':status(),'tools':[x['name'] for x in list_tools()]},ensure_ascii=False,indent=2))
