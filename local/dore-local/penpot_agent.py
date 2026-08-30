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
EXPORT_DIR = MCP_RUNTIME / 'exports'
VOICE_RULE = '''You are Doré, not a narrator describing Doré. Output only useful task answers or factual results of actions actually executed. Never claim a tool/system action unless it actually occurred and is supported by the tool trace.'''

def _node_bin():
    explicit=os.environ.get('DORE_NODE_BIN'); runtime_path=MCP_RUNTIME/'node-path'; runtime_node=None
    if runtime_path.is_file():
        try: runtime_node=runtime_path.read_text().strip()
        except Exception: runtime_node=None
    for c in [explicit,runtime_node,'/opt/homebrew/opt/node@22/bin/node',shutil.which('node'),'/opt/homebrew/bin/node','/usr/local/bin/node']:
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
    if p.returncode and data.get('ok') is not True:data.setdefault('stderr',(p.stderr or '').strip())
    return data

def _valid_png_b64(value:str)->bool:
    if not isinstance(value,str) or len(value)<16:return False
    try:return base64.b64decode(value,validate=True).startswith(b'\x89PNG\r\n\x1a\n')
    except Exception:return False

def _walk_images(value):
    out=[]
    if isinstance(value,dict):
        data=value.get('data')
        if value.get('type')=='image' and isinstance(data,str) and data:out.append(data)
        elif isinstance(data,str) and _valid_png_b64(data):out.append(data)
        for v in value.values():out.extend(_walk_images(v))
    elif isinstance(value,list):
        for v in value:out.extend(_walk_images(v))
    elif isinstance(value,str):
        s=value.strip()
        if s.startswith('data:image/') and ';base64,' in s:
            v=s.split(';base64,',1)[1]
            if _valid_png_b64(v):out.append(v)
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

def _text_from_result(result):
    blocks=(((result or {}).get('result') or {}).get('content') or []); bits=[]
    for block in blocks:
        if isinstance(block,dict) and block.get('type')=='text':bits.append(block.get('text',''))
    return '\n'.join(bits) if bits else json.dumps(result or {},ensure_ascii=False)

def _inject_png(result,data_b64,source,diagnostics=None):
    result=dict(result or {}); inner=result.get('result') if isinstance(result.get('result'),dict) else {}; content=inner.get('content') if isinstance(inner.get('content'),list) else []
    content.append({'type':'image','data':data_b64,'mimeType':'image/png'}); inner['content']=content; result['result']=inner; result['visual_source']=source; result['ok']=True
    if diagnostics is not None:result['visual_diagnostics']=diagnostics
    return result

def _export_file_fallback(arguments):
    EXPORT_DIR.mkdir(parents=True,exist_ok=True); attempts=[]; last=None
    for path in [EXPORT_DIR/f'penpot-{uuid.uuid4().hex}.png',Path(tempfile.gettempdir())/f'dore-penpot-{uuid.uuid4().hex}.png']:
        retry_args=dict(arguments or {}); retry_args['format']='png'; retry_args.setdefault('mode','shape'); retry_args['filePath']=str(path)
        retry=_node('call',{'name':'export_shape','arguments':retry_args}); last=retry
        exists=path.is_file(); size=path.stat().st_size if exists else 0; attempts.append({'path':str(path),'exists':exists,'size':size,'mcp_text':_text_from_result(retry)[:500]})
        try:
            if exists and size>0:
                raw=path.read_bytes()
                if raw.startswith(b'\x89PNG\r\n\x1a\n'):return _inject_png(retry,base64.b64encode(raw).decode('ascii'),'filePath-fallback',attempts)
            images=_images_from_result(retry)
            if images:return _inject_png(retry,images[0],'fallback-response-base64',attempts)
        finally:
            try:path.unlink(missing_ok=True)
            except Exception:pass
    last=dict(last or {'ok':False}); last['visual_diagnostics']=attempts; last['visual_fallback_error']='export_file_missing_empty_or_invalid'; return last

def status():return _node('status')
def list_tools():
    r=_node('list')
    if not r.get('ok'):raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
    return r.get('tools') or []
def call_tool(name,arguments):
    result=_node('call',{'name':name,'arguments':arguments or {}})
    if name=='export_shape' and bool(result.get('ok')) and not _images_from_result(result):return _export_file_fallback(arguments or {})
    return result

def _ollama(messages,model=None):
    body={'model':model or MODEL,'messages':messages,'stream':False,'think':False}
    req=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps(body).encode(),headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(req,timeout=300).read())['message']

def visual_verify(image_b64:str,task:str,design_brief:str):
    prompt=f'''You are Doré Visual Verifier. Judge the ACTUAL rendered Penpot image.\n{VOICE_RULE}\nTask: {task}\nBrief: {design_brief}\nReturn strict JSON with verdict PASS or FAIL, problems, strengths, next_correction. Blank or unfinished output is FAIL.'''
    try:msg=_ollama([{'role':'user','content':prompt,'images':[image_b64]}],model=VISION_MODEL); text=(msg.get('content') or '').strip(); return json.loads(text[text.index('{'):text.rindex('}')+1])
    except Exception as e:return {'verdict':'FAIL','problems':['visual_engine_error:'+str(e)[:400]],'strengths':[],'next_correction':'inspect rendered board'}

def _grounding_packet(tool_names):
    packet=[]
    if 'high_level_overview' in tool_names:
        r=call_tool('high_level_overview',{}); packet.append({'tool':'high_level_overview','ok':bool(r.get('ok'))})
    if 'penpot_api_info' in tool_names:
        for api_type in ('Penpot','Board','Rectangle','Text'):
            r=call_tool('penpot_api_info',{'type':api_type}); packet.append({'tool':'penpot_api_info','type':api_type,'ok':bool(r.get('ok'))})
    return packet

def _construction_code():
    return r"""
const root = penpot.root;
const board = penpot.createBoard();
board.name = '02 — Westside Watch Homepage v0.2 — VISIBLE';
board.resize(1440,1200);
board.fills = [{fillColor:'#FAF9F5',fillOpacity:1}];
root.insertChild(root.children.length, board);
board.x = 0; board.y = -1800;

function addRect(name,x,y,w,h,color){
  const s=penpot.createRectangle(); s.name=name; s.resize(w,h); s.fills=[{fillColor:color,fillOpacity:1}];
  board.insertChild(board.children.length,s); penpotUtils.setParentXY(s,x,y); s.bringToFront(); return s;
}
function addText(name,text,x,y,size,color){
  const s=penpot.createText(text); if(!s) throw new Error('createText failed: '+name);
  s.name=name; s.fontSize=String(size); s.growType='auto-width'; s.fills=[{fillColor:color,fillOpacity:1}];
  board.insertChild(board.children.length,s); penpotUtils.setParentXY(s,x,y); s.bringToFront(); return s;
}
addRect('Top Gold Bar',0,0,1440,12,'#A2872A');
addText('Masthead','WESTSIDE WATCH',96,58,38,'#252525');
addText('Navigation','JOURNAL     ONE     DAWN LIBRARY     JOIN',820,72,18,'#252525');
addRect('First Light Rule',96,142,1248,2,'#A2872A');
addText('Hero Kicker','WATCH FOR THE DAWN',96,216,18,'#A2872A');
addText('Hero Title','A CITY OF LIGHT',96,262,88,'#252525');
addText('Hero Deck','Scripture, witness, prayer, and the life of the church — held together in the first light.',100,390,25,'#252525');
addRect('Watch Night Field',880,208,360,576,'#102A43');
addRect('Morning Gold Accent',880,784,360,24,'#D2BC69');
addRect('Editorial Gold Block',96,560,560,210,'#D2BC69');
addText('Feature Number','01',124,590,24,'#252525');
addText('Feature Title','守望，一座光明的城',124,640,42,'#252525');
addRect('Lower Rule',96,900,1248,2,'#A2872A');
addText('Editorial Passage','FEATURE     JOURNAL     PRAYER     BIBLE STUDY     WITNESS',96,948,21,'#252525');
console.log('DORE_BOARD_ID='+board.id);
console.log('DORE_CHILDREN='+board.children.length);
return 'DORE_BOARD_ID='+board.id+' DORE_CHILDREN='+board.children.length;
"""

def _extract_board_id(result):
    text=_text_from_result(result)
    for pat in (r'DORE_BOARD_ID=([0-9a-fA-F-]{16,})',r'"boardId"\s*:\s*"([^"]+)"'):
        m=re.search(pat,text)
        if m:return m.group(1)
    return None

def _lookup_code():
    return r"""
const b=penpotUtils.findShape(s=>s.name==='02 — Westside Watch Homepage v0.2 — VISIBLE',penpot.root);
if(!b) throw new Error('homepage board not found after construction');
console.log('DORE_BOARD_ID='+b.id);
console.log('DORE_CHILDREN='+(b.children?b.children.length:-1));
return 'DORE_BOARD_ID='+b.id+' DORE_CHILDREN='+(b.children?b.children.length:-1);
"""

def run_task(task:str,design_brief:str):
    tools=list_tools(); tool_names=[x['name'] for x in tools]; trace=[]; checks=[]
    for item in _grounding_packet(tool_names):trace.append({'tool':item.get('tool'),'ok':item.get('ok'),'mutation':False,'preflight':True,'type':item.get('type')})
    if 'execute_code' not in tool_names:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_execute_code_missing','trace':trace,'visual_checks':checks}
    create=call_tool('execute_code',{'code':_construction_code()}); create_ok=bool(create.get('ok')); board_id=_extract_board_id(create)
    trace.append({'tool':'execute_code','ok':create_ok,'mutation':True,'phase':'construct-visible-v02','board_id':board_id,'text':_text_from_result(create)[:1000]})
    if not create_ok:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_construction_failed','trace':trace,'visual_checks':checks}
    if not board_id:
        lookup=call_tool('execute_code',{'code':_lookup_code()}); board_id=_extract_board_id(lookup)
        trace.append({'tool':'execute_code','ok':bool(lookup.get('ok')),'mutation':False,'phase':'lookup-board-id','board_id':board_id,'text':_text_from_result(lookup)[:1000]})
    if not board_id:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_board_id_missing_after_lookup','trace':trace,'visual_checks':checks}
    if 'export_shape' not in tool_names:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_export_shape_missing','board_id':board_id,'trace':trace,'visual_checks':checks}
    exported=call_tool('export_shape',{'format':'png','mode':'shape','shapeId':board_id}); images=_images_from_result(exported)
    trace.append({'tool':'export_shape','ok':bool(exported.get('ok')),'mutation':False,'shapeId':board_id,'image_count':len(images),'text':_text_from_result(exported)[:700],'visual_diagnostics':exported.get('visual_diagnostics')})
    if not images:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_no_visual_evidence','board_id':board_id,'trace':trace,'visual_checks':checks}
    verdict=visual_verify(images[0],task,design_brief); checks.append(verdict); passed=verdict.get('verdict')=='PASS'
    return {'ok':passed,'verified':passed,'mutated':True,'board_id':board_id,'error':None if passed else 'penpot_visual_verification_failed','visual_checks':checks,'trace':trace,'model':MODEL,'vision_model':VISION_MODEL}

if __name__=='__main__':print(json.dumps({'status':status(),'tools':[x['name'] for x in list_tools()]},ensure_ascii=False,indent=2))
