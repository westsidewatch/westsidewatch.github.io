#!/usr/bin/env python3
"""Doré Penpot execution loop with bounded calls, deterministic recovery and visual verification."""
from __future__ import annotations
import base64,json,os,re,shutil,subprocess,urllib.request
from pathlib import Path

HERE=Path(__file__).resolve().parent
MCP_CLIENT=HERE/'penpot-mcp'/'client.mjs'
MCP_RUNTIME=Path.home()/'.dore'/'runtime'/'penpot-mcp'
MCP_URL=os.environ.get('PENPOT_MCP_URL','http://localhost:4401/mcp')
OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')
MODEL=os.environ.get('DORE_LOCAL_MODEL','gemma4:e4b')
VISION_MODEL=MODEL
MCP_TIMEOUT=int(os.environ.get('DORE_PENPOT_MCP_TIMEOUT','45'))
OLLAMA_TIMEOUT=int(os.environ.get('DORE_OLLAMA_TIMEOUT','75'))


def _node_bin():
    p=MCP_RUNTIME/'node-path'
    vals=[os.environ.get('DORE_NODE_BIN'),p.read_text().strip() if p.is_file() else None,'/opt/homebrew/opt/node@22/bin/node',shutil.which('node'),'/opt/homebrew/bin/node','/usr/local/bin/node']
    return next((x for x in vals if x and Path(x).is_file()),None)


def _node(op,payload=None):
    n=_node_bin()
    if not MCP_CLIENT.is_file(): return {'ok':False,'error':'penpot_mcp_client_missing'}
    if not n: return {'ok':False,'error':'node_executable_not_found'}
    e=os.environ.copy(); e['PENPOT_MCP_URL']=MCP_URL
    try:
        p=subprocess.run([n,str(MCP_CLIENT),op],input=json.dumps(payload or {},ensure_ascii=False) if payload is not None else None,text=True,capture_output=True,env=e,cwd=str(MCP_CLIENT.parent),timeout=MCP_TIMEOUT)
    except subprocess.TimeoutExpired:
        return {'ok':False,'error':f'penpot_mcp_timeout_{MCP_TIMEOUT}s','operation':op}
    try: return json.loads((p.stdout or '').strip() or '{}')
    except: return {'ok':False,'error':(p.stdout or p.stderr or '').strip()}


def _valid_png_b64(v):
    try: return isinstance(v,str) and base64.b64decode(v,validate=True).startswith(b'\x89PNG\r\n\x1a\n')
    except: return False


def _walk_images(v):
    out=[]
    if isinstance(v,dict):
        if v.get('type')=='image' and isinstance(v.get('data'),str): out.append(v['data'])
        for x in v.values(): out += _walk_images(x)
    elif isinstance(v,list):
        for x in v: out += _walk_images(x)
    elif isinstance(v,str) and _valid_png_b64(v): out.append(v)
    return out


def _images_from_result(r): return list(dict.fromkeys(_walk_images(r or {})))


def _text_from_result(r):
    body=(((r or {}).get('result') or {}).get('content') or [])
    txt=[x.get('text','') for x in body if isinstance(x,dict) and x.get('type')=='text']
    return '\n'.join(txt) if txt else json.dumps(r or {},ensure_ascii=False)


def _semantic_ok(r):
    if not (r or {}).get('ok'): return False
    t=_text_from_result(r).lower()
    bad=('tool execution failed','error handling task','unexpected token','syntaxerror','referenceerror','typeerror:','execution failed','timed out','timeout')
    return not any(x in t for x in bad)


def status(): return _node('status')

def list_tools():
    r=_node('list')
    if not r.get('ok'): raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
    return r.get('tools') or []

def call_tool(name,args): return _node('call',{'name':name,'arguments':args or {}})


def _ollama(messages,model=None):
    q=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps({'model':model or MODEL,'messages':messages,'stream':False,'think':False}).encode(),headers={'Content-Type':'application/json'})
    return json.loads(urllib.request.urlopen(q,timeout=OLLAMA_TIMEOUT).read())['message']


def visual_verify(img,task,brief):
    try:
        m=_ollama([{'role':'user','content':f'Judge the ACTUAL Penpot render. Task: {task}\nBrief: {brief}\nReturn strict JSON: verdict PASS/FAIL, problems, strengths, next_correction. Blank, duplicated, cluttered, unchanged-old-design, or test-looking output is FAIL.','images':[img]}],VISION_MODEL)
        s=m.get('content','')
        return json.loads(s[s.index('{'):s.rindex('}')+1])
    except Exception as e:
        return {'verdict':'FAIL','problems':['visual_engine_error:'+str(e)],'strengths':[],'next_correction':'inspect render'}


def _board_id(task):
    m=re.search(r'\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b',task or '')
    return m.group(0) if m else None


def _extract_board_id(r):
    m=re.search(r'DORE_BOARD_ID=([0-9a-fA-F-]{16,})',_text_from_result(r))
    return m.group(1) if m else None


def _westside_clean_code(board_id):
    # Intentionally deterministic: this recovery path must not block on local LLM code generation.
    return f'''const board = penpotUtils.findShapeById("{board_id}");
if (!board) throw new Error("board_not_found");
const oldChildren = Array.from(board.children || []);
for (const child of oldChildren) child.remove();
board.name = "00 — Westside Watch Homepage — CLEAN START";
board.resize(1440, 1200);
board.fills = [{{fillColor:"#FAF9F5",fillOpacity:1}}];
const bx = board.x;
const by = board.y;
function rect(name,x,y,w,h,color) {{
  const s = penpot.createRectangle();
  s.name = name;
  s.resize(w,h);
  s.fills = [{{fillColor:color,fillOpacity:1}}];
  board.insertChild(board.children.length,s);
  s.x = bx + x; s.y = by + y;
  return s;
}}
function text(name,value,x,y,size,color,weight) {{
  const s = penpot.createText(value);
  s.name = name;
  board.insertChild(board.children.length,s);
  s.x = bx + x; s.y = by + y;
  s.fontSize = size;
  if (weight) s.fontWeight = weight;
  s.fills = [{{fillColor:color,fillOpacity:1}}];
  return s;
}}
rect("Living Paper",0,0,1440,1200,"#FAF9F5");
rect("First Light Top Rule",72,54,1296,3,"#A2872A");
text("Masthead","WESTSIDE WATCH",72,82,24,"#252525",600);
text("Chinese Masthead","西區守望",72,118,18,"#252525",500);
text("Navigation","JOURNAL   ARCHIVE   TOPICS   AUTHORS   SEARCH",850,92,13,"#252525",400);
rect("Header Rule",72,156,1296,1,"#A2872A");
text("Hero Kicker","WATCH FOR THE DAWN",72,220,14,"#A2872A",600);
text("Hero Title","A CITY OF LIGHT",72,260,68,"#252525",500);
text("Hero Deck","Scripture, witness, prayer, and the life of the church — held together in the first light.",72,352,20,"#252525",400);
rect("Watch Night Field",870,220,390,520,"#102A43");
rect("Morning Gold Accent",870,726,390,14,"#D2BC69");
rect("Editorial Gold Block",72,470,520,220,"#D2BC69");
text("Feature Number","01",104,500,14,"#252525",500);
text("Feature Chinese","守望，一座光明的城",104,548,30,"#252525",500);
text("Feature Note","本月專題 · FEATURE",104,620,13,"#252525",500);
rect("Lower Rule",72,810,1296,1,"#A2872A");
text("Editorial Passage","在城市仍黑暗的時候，守望不是焦躁地尋找答案，而是在黎明以前仍站在城牆上。",72,862,22,"#252525",400);
text("Section Index","FEATURE    JOURNAL    PRAYER    BIBLE STUDY    WITNESS",72,1045,13,"#252525",500);
console.log("DORE_BOARD_ID=" + board.id);
console.log("DORE_CHILDREN=" + board.children.length);
return "DORE_BOARD_ID=" + board.id + ";DORE_CHILDREN=" + board.children.length;'''


def _generic_agent_code(task,brief,bid,error_feedback=''):
    retry=f'\nPREVIOUS EXECUTION ERROR TO FIX:\n{error_feedback[:2000]}' if error_feedback else ''
    prompt=f'''Write ONLY conservative executable JavaScript for Penpot MCP execute_code. Modify existing board id {bid}; never create another board. Use penpotUtils.findShapeById, shape.remove(), penpot.createRectangle(), penpot.createText(), board.insertChild(), resize(), fills, x/y. No TypeScript. End by returning DORE_BOARD_ID and child count. TASK:\n{task}\nBRIEF:\n{brief}{retry}'''
    m=_ollama([{'role':'user','content':prompt}],MODEL)
    code=(m.get('content') or '').strip()
    return re.sub(r'^```(?:javascript|js)?\s*|\s*```$','',code,flags=re.S)


def run_task(task,design_brief):
    trace=[]; checks=[]
    tools=list_tools(); names=[x['name'] for x in tools]
    if 'execute_code' not in names:
        return {'ok':False,'verified':False,'mutated':False,'error':'penpot_execute_code_missing','trace':trace}
    bid=_board_id(task)
    if not bid:
        return {'ok':False,'verified':False,'mutated':False,'error':'penpot_existing_board_id_required','trace':trace}

    is_westside_clean=('Westside Watch' in (task or '') and 'CLEAN START' in (task or '').upper())
    if is_westside_clean:
        code=_westside_clean_code(bid)
        mut=call_tool('execute_code',{'code':code})
        text=_text_from_result(mut)
        actual=_extract_board_id(mut) or bid
        trace.append({'tool':'execute_code','ok':_semantic_ok(mut),'transport_ok':bool(mut.get('ok')),'mutation':True,'attempt':1,'phase':'deterministic-westside-clean-rebuild','board_id':actual,'text':text[:3500]})
        if not _semantic_ok(mut):
            return {'ok':False,'verified':False,'mutated':False,'error':'penpot_task_mutation_failed','board_id':actual,'trace':trace}
    else:
        feedback=''; actual=bid
        for attempt in range(1,3):
            try: code=_generic_agent_code(task,design_brief,bid,feedback)
            except Exception as e:
                return {'ok':False,'verified':False,'mutated':False,'error':'penpot_code_author_failed:'+str(e),'trace':trace}
            if 'createBoard' in code:
                return {'ok':False,'verified':False,'mutated':False,'error':'penpot_agent_attempted_new_board','board_id':bid,'trace':trace}
            mut=call_tool('execute_code',{'code':code}); text=_text_from_result(mut); actual=_extract_board_id(mut) or bid
            trace.append({'tool':'execute_code','ok':_semantic_ok(mut),'transport_ok':bool(mut.get('ok')),'mutation':True,'attempt':attempt,'phase':'task-aware-existing-board-mutation','board_id':actual,'text':text[:3500]})
            if _semantic_ok(mut): break
            feedback=text
        else:
            return {'ok':False,'verified':False,'mutated':False,'error':'penpot_task_mutation_failed','board_id':actual,'trace':trace}

    verify_code=f'''const board=penpotUtils.findShapeById("{actual}"); if (!board) throw new Error("board_not_found"); return "DORE_VERIFY_ID="+board.id+";DORE_VERIFY_NAME="+board.name+";DORE_VERIFY_CHILDREN="+board.children.length;'''
    vr=call_tool('execute_code',{'code':verify_code}); vtxt=_text_from_result(vr)
    trace.append({'tool':'execute_code','ok':_semantic_ok(vr),'mutation':False,'phase':'post-mutation-structure-check','board_id':actual,'text':vtxt[:1200]})
    if not _semantic_ok(vr) or 'DORE_VERIFY_CHILDREN=0' in vtxt:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_post_mutation_structure_check_failed','board_id':actual,'trace':trace}

    if 'export_shape' not in names:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_export_shape_missing','board_id':actual,'trace':trace}
    exp=call_tool('export_shape',{'format':'png','mode':'shape','shapeId':actual}); imgs=_images_from_result(exp)
    trace.append({'tool':'export_shape','ok':bool(exp.get('ok')),'mutation':False,'shapeId':actual,'image_count':len(imgs),'text':_text_from_result(exp)[:700]})
    if not imgs:
        return {'ok':False,'verified':False,'mutated':True,'error':'penpot_no_visual_evidence','board_id':actual,'trace':trace}

    v=visual_verify(imgs[0],task,design_brief); checks.append(v)
    passed=v.get('verdict')=='PASS'
    return {'ok':passed,'verified':passed,'mutated':True,'board_id':actual,'error':None if passed else 'penpot_visual_verification_failed','visual_checks':checks,'trace':trace,'model':MODEL,'vision_model':VISION_MODEL}


if __name__=='__main__':
    print(json.dumps({'status':status(),'tools':[x['name'] for x in list_tools()]},ensure_ascii=False,indent=2))
