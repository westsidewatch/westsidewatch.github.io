#!/usr/bin/env python3
from __future__ import annotations
import base64,json,os,re,shutil,subprocess,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent
MCP_CLIENT=HERE/'penpot-mcp'/'client.mjs'
MCP_RUNTIME=Path.home()/'.dore'/'runtime'/'penpot-mcp'
MCP_URL=os.environ.get('PENPOT_MCP_URL','http://localhost:4401/mcp')
OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434')
MODEL=os.environ.get('DORE_LOCAL_MODEL','gemma4:e4b'); VISION_MODEL=MODEL

def _node_bin():
 p=MCP_RUNTIME/'node-path'; vals=[os.environ.get('DORE_NODE_BIN'),p.read_text().strip() if p.is_file() else None,'/opt/homebrew/opt/node@22/bin/node',shutil.which('node'),'/opt/homebrew/bin/node','/usr/local/bin/node']; return next((x for x in vals if x and Path(x).is_file()),None)
def _node(op,payload=None):
 n=_node_bin()
 if not MCP_CLIENT.is_file(): return {'ok':False,'error':'penpot_mcp_client_missing'}
 if not n:return {'ok':False,'error':'node_executable_not_found'}
 e=os.environ.copy();e['PENPOT_MCP_URL']=MCP_URL
 try:p=subprocess.run([n,str(MCP_CLIENT),op],input=json.dumps(payload or {},ensure_ascii=False) if payload is not None else None,text=True,capture_output=True,env=e,cwd=str(MCP_CLIENT.parent),timeout=45)
 except subprocess.TimeoutExpired:return {'ok':False,'error':'penpot_mcp_timeout_45s'}
 try:return json.loads((p.stdout or '').strip() or '{}')
 except:return {'ok':False,'error':(p.stdout or p.stderr or '').strip()}
def _valid_png_b64(v):
 try:return isinstance(v,str) and base64.b64decode(v,validate=True).startswith(b'\x89PNG\r\n\x1a\n')
 except:return False
def _walk_images(v):
 o=[]
 if isinstance(v,dict):
  if v.get('type')=='image' and isinstance(v.get('data'),str):o.append(v['data'])
  for x in v.values():o+=_walk_images(x)
 elif isinstance(v,list):
  for x in v:o+=_walk_images(x)
 elif isinstance(v,str) and _valid_png_b64(v):o.append(v)
 return o
def _images_from_result(r):return list(dict.fromkeys(_walk_images(r or {})))
def _text_from_result(r):
 b=(((r or {}).get('result') or {}).get('content') or []);t=[x.get('text','') for x in b if isinstance(x,dict) and x.get('type')=='text'];return '\n'.join(t) if t else json.dumps(r or {},ensure_ascii=False)
def _semantic_ok(r):
 if not (r or {}).get('ok'):return False
 t=_text_from_result(r).lower(); bad=('tool execution failed','error handling task','unexpected token','syntaxerror','referenceerror','typeerror:','execution failed','timeout')
 return not any(x in t for x in bad)
def status():return _node('status')
def list_tools():
 r=_node('list')
 if not r.get('ok'):raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
 return r.get('tools') or []
def call_tool(name,args):return _node('call',{'name':name,'arguments':args or {}})
def _ollama(messages,model=None):
 q=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps({'model':model or MODEL,'messages':messages,'stream':False,'think':False}).encode(),headers={'Content-Type':'application/json'});return json.loads(urllib.request.urlopen(q,timeout=75).read())['message']
def visual_verify(img,task,brief):
 try:
  m=_ollama([{'role':'user','content':f'Judge the ACTUAL Penpot render. Task: {task}\nBrief: {brief}\nReturn strict JSON: verdict PASS/FAIL, problems, strengths, next_correction. Blank, duplicated, cluttered, unchanged-old-design, or test-looking output is FAIL.','images':[img]}]);s=m.get('content','');return json.loads(s[s.index('{'):s.rindex('}')+1])
 except Exception as e:return {'verdict':'FAIL','problems':['visual_engine_error:'+str(e)],'strengths':[],'next_correction':'inspect render'}
def _board_id(task):
 m=re.search(r'\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b',task or '');return m.group(0) if m else None
def _extract_board_id(r):
 m=re.search(r'DORE_BOARD_ID=([0-9a-fA-F-]{16,})',_text_from_result(r));return m.group(1) if m else None
def _westside_code(bid):
 return f'''const board=penpotUtils.findShapeById("{bid}");
if(!board) throw new Error("board_not_found");
for(const child of Array.from(board.children||[])) child.remove();
board.name="00 — Westside Watch Homepage — CLEAN START";
board.resize(1440,1200); board.fills=[{{fillColor:"#FAF9F5",fillOpacity:1}}];
const bx=board.x, by=board.y;
function R(n,x,y,w,h,c){{const s=penpot.createRectangle();s.name=n;s.resize(w,h);s.fills=[{{fillColor:c,fillOpacity:1}}];board.insertChild(board.children.length,s);s.x=bx+x;s.y=by+y;return s;}}
function T(n,v,x,y,z,c,w){{const s=penpot.createText(v);s.name=n;board.insertChild(board.children.length,s);s.x=bx+x;s.y=by+y;s.fontSize=z;if(w)s.fontWeight=w;s.fills=[{{fillColor:c,fillOpacity:1}}];return s;}}
R("Living Paper",0,0,1440,1200,"#FAF9F5");
R("First Light Top Rule",72,54,1296,3,"#A2872A");
T("Masthead","WESTSIDE WATCH",72,82,24,"#252525",600);
T("Chinese Masthead","西區守望",72,118,18,"#252525",400);
T("Navigation","JOURNAL   ARCHIVE   TOPICS   AUTHORS   SEARCH",850,92,13,"#252525",400);
R("Header Rule",72,156,1296,1,"#A2872A");
T("Hero Kicker","WATCH FOR THE DAWN",72,220,14,"#A2872A",600);
T("Hero Title","A CITY OF LIGHT",72,260,68,"#252525",400);
T("Hero Deck","Scripture, witness, prayer, and the life of the church — held together in the first light.",72,352,20,"#252525",400);
R("Watch Night Field",870,220,390,520,"#102A43");
R("Morning Gold Accent",870,726,390,14,"#D2BC69");
R("Editorial Gold Block",72,470,520,220,"#D2BC69");
T("Feature Number","01",104,500,14,"#252525",400);
T("Feature Chinese","守望，一座光明的城",104,548,30,"#252525",400);
T("Feature Note","本月專題 · FEATURE",104,620,13,"#252525",400);
R("Lower Rule",72,810,1296,1,"#A2872A");
T("Editorial Passage","在城市仍黑暗的時候，守望不是焦躁地尋找答案，而是在黎明以前仍站在城牆上。",72,862,22,"#252525",400);
T("Section Index","FEATURE    JOURNAL    PRAYER    BIBLE STUDY    WITNESS",72,1045,13,"#252525",400);
return "DORE_BOARD_ID="+board.id+";DORE_CHILDREN="+board.children.length;'''
def run_task(task,design_brief):
 tools=list_tools();names=[x['name'] for x in tools];trace=[];checks=[]
 if 'execute_code' not in names:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_execute_code_missing','trace':trace}
 bid=_board_id(task)
 if not bid:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_existing_board_id_required','trace':trace}
 if 'Westside Watch' not in task or 'CLEAN START' not in task.upper():return {'ok':False,'verified':False,'mutated':False,'error':'unsupported_task_for_safe_executor','board_id':bid,'trace':trace}
 mut=call_tool('execute_code',{'code':_westside_code(bid)});txt=_text_from_result(mut);actual=_extract_board_id(mut) or bid
 trace.append({'tool':'execute_code','ok':_semantic_ok(mut),'transport_ok':bool(mut.get('ok')),'mutation':True,'phase':'deterministic-westside-clean-rebuild','board_id':actual,'text':txt[:3500]})
 if not _semantic_ok(mut):return {'ok':False,'verified':False,'mutated':False,'error':'penpot_task_mutation_failed','board_id':actual,'trace':trace}
 verify=f'''const board=penpotUtils.findShapeById("{actual}");if(!board)throw new Error("board_not_found");return "DORE_VERIFY_NAME="+board.name+";DORE_VERIFY_CHILDREN="+board.children.length;'''
 vr=call_tool('execute_code',{'code':verify});vtxt=_text_from_result(vr);trace.append({'tool':'execute_code','ok':_semantic_ok(vr),'mutation':False,'phase':'post-mutation-structure-check','board_id':actual,'text':vtxt[:1200]})
 if not _semantic_ok(vr) or 'DORE_VERIFY_CHILDREN=0' in vtxt:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_post_mutation_structure_check_failed','board_id':actual,'trace':trace}
 if 'export_shape' not in names:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_export_shape_missing','board_id':actual,'trace':trace}
 exp=call_tool('export_shape',{'format':'png','mode':'shape','shapeId':actual});imgs=_images_from_result(exp);trace.append({'tool':'export_shape','ok':bool(exp.get('ok')),'mutation':False,'shapeId':actual,'image_count':len(imgs),'text':_text_from_result(exp)[:700]})
 if not imgs:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_no_visual_evidence','board_id':actual,'trace':trace}
 v=visual_verify(imgs[0],task,design_brief);checks.append(v);passed=v.get('verdict')=='PASS';return {'ok':passed,'verified':passed,'mutated':True,'board_id':actual,'error':None if passed else 'penpot_visual_verification_failed','visual_checks':checks,'trace':trace,'model':MODEL,'vision_model':VISION_MODEL}
if __name__=='__main__':print(json.dumps({'status':status(),'tools':[x['name'] for x in list_tools()]},ensure_ascii=False,indent=2))
