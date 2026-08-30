#!/usr/bin/env python3
"""Doré Penpot execution loop with task-aware mutation and visual verification."""
from __future__ import annotations
import base64,json,os,re,shutil,subprocess,urllib.request
from pathlib import Path
HERE=Path(__file__).resolve().parent; MCP_CLIENT=HERE/'penpot-mcp'/'client.mjs'; MCP_RUNTIME=Path.home()/'.dore'/'runtime'/'penpot-mcp'; MCP_URL=os.environ.get('PENPOT_MCP_URL','http://localhost:4401/mcp'); OLLAMA=os.environ.get('OLLAMA_BASE_URL','http://127.0.0.1:11434'); MODEL=os.environ.get('DORE_LOCAL_MODEL','gemma4:e4b'); VISION_MODEL=MODEL

def _node_bin():
 p=MCP_RUNTIME/'node-path'; vals=[os.environ.get('DORE_NODE_BIN'),p.read_text().strip() if p.is_file() else None,'/opt/homebrew/opt/node@22/bin/node',shutil.which('node'),'/opt/homebrew/bin/node','/usr/local/bin/node']; return next((x for x in vals if x and Path(x).is_file()),None)
def _node(op,payload=None):
 n=_node_bin()
 if not MCP_CLIENT.is_file(): return {'ok':False,'error':'penpot_mcp_client_missing'}
 if not n:return {'ok':False,'error':'node_executable_not_found'}
 e=os.environ.copy();e['PENPOT_MCP_URL']=MCP_URL;p=subprocess.run([n,str(MCP_CLIENT),op],input=json.dumps(payload or {},ensure_ascii=False) if payload is not None else None,text=True,capture_output=True,env=e,cwd=str(MCP_CLIENT.parent),timeout=90)
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
 t=_text_from_result(r).lower()
 bad=('tool execution failed','error handling task','unexpected token','syntaxerror','referenceerror','typeerror:','execution failed')
 return not any(x in t for x in bad)
def status():return _node('status')
def list_tools():
 r=_node('list')
 if not r.get('ok'):raise RuntimeError(r.get('error') or 'penpot_mcp_unavailable')
 return r.get('tools') or []
def call_tool(name,args):return _node('call',{'name':name,'arguments':args or {}})
def _ollama(messages,model=None):
 q=urllib.request.Request(OLLAMA+'/api/chat',data=json.dumps({'model':model or MODEL,'messages':messages,'stream':False,'think':False}).encode(),headers={'Content-Type':'application/json'});return json.loads(urllib.request.urlopen(q,timeout=300).read())['message']
def visual_verify(img,task,brief):
 try:
  m=_ollama([{'role':'user','content':f'Judge the ACTUAL Penpot render. Task: {task}\nBrief: {brief}\nReturn strict JSON: verdict PASS/FAIL, problems, strengths, next_correction. Blank, duplicated, cluttered, unchanged-old-design, or test-looking output is FAIL.','images':[img]}],VISION_MODEL);s=m.get('content','');return json.loads(s[s.index('{'):s.rindex('}')+1])
 except Exception as e:return {'verdict':'FAIL','problems':['visual_engine_error:'+str(e)],'strengths':[],'next_correction':'inspect render'}
def _ground(names):
 out=[]
 if 'high_level_overview' in names:out.append(('high_level_overview',{},call_tool('high_level_overview',{})))
 if 'penpot_api_info' in names:
  for t in ('Penpot','Page','Board','Shape','Rectangle','Text'):out.append(('penpot_api_info',{'type':t},call_tool('penpot_api_info',{'type':t})))
 return out
def _board_id(task):
 m=re.search(r'\b[0-9a-fA-F]{8}(?:-[0-9a-fA-F]{4}){3}-[0-9a-fA-F]{12}\b',task or '');return m.group(0) if m else None
def _extract_board_id(r):
 m=re.search(r'DORE_BOARD_ID=([0-9a-fA-F-]{16,})',_text_from_result(r));return m.group(1) if m else None
def _agent_code(task,brief,bid,docs,clean=False,error_feedback=''):
 mode='''CLEAN-SLATE MODE. Create ONE fresh board named "00 — Westside Watch Homepage — CLEAN START" on penpot.root. Do not reuse or copy old homepage boards. The new board must be the only artifact you work on in this task. Build the first coherent editorial homepage composition from scratch. Do not create swatches, demos, test rectangles, or duplicate boards.''' if clean else f'''EXISTING-BOARD MODE. Locate and modify only existing board id {bid}. Never create a new board. If the task asks for CLEAN START, delete all existing children from that board first and rename that same board exactly as requested.'''
 retry=f'\nPREVIOUS EXECUTION ERROR TO FIX:\n{error_feedback[:3000]}' if error_feedback else ''
 prompt=f'''You are Doré's Penpot code author. Write ONLY executable JavaScript for official Penpot MCP execute_code, no markdown. {mode}
Use only official APIs evidenced below. Preserve native editable Penpot layers. Implement the design materially. Keep JavaScript simple and syntactically conservative: no TypeScript, no optional type syntax, no markdown, no prose outside code. At the end console.log('DORE_BOARD_ID='+board.id), console.log('DORE_CHILDREN='+board.children.length), and return a short success string. TASK:\n{task}\nBRIEF:\n{brief}\nOFFICIAL API GROUNDING:\n{docs[:16000]}{retry}'''
 m=_ollama([{'role':'user','content':prompt}],MODEL);code=(m.get('content') or '').strip();return re.sub(r'^```(?:javascript|js)?\s*|\s*```$','',code,flags=re.S)
def run_task(task,design_brief):
 tools=list_tools();names=[x['name'] for x in tools];trace=[];checks=[];ground=_ground(names)
 for n,a,r in ground:trace.append({'tool':n,'ok':bool(r.get('ok')),'mutation':False,'preflight':True,'arguments':a})
 if 'execute_code' not in names:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_execute_code_missing','trace':trace}
 clean=('CLEAN_START' in (task or '')) and not _board_id(task)
 bid=_board_id(task)
 if not clean and not bid:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_existing_board_id_required','trace':trace}
 docs='\n'.join(_text_from_result(r) for _,_,r in ground)
 actual=None;mut=None;feedback=''
 for attempt in range(1,4):
  try:code=_agent_code(task,design_brief,bid,docs,clean,feedback)
  except Exception as e:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_code_author_failed:'+str(e),'trace':trace}
  if not clean and 'createBoard' in code:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_agent_attempted_new_board','board_id':bid,'trace':trace}
  mut=call_tool('execute_code',{'code':code});actual=_extract_board_id(mut) or bid
  text=_text_from_result(mut)
  trace.append({'tool':'execute_code','ok':_semantic_ok(mut),'transport_ok':bool(mut.get('ok')),'mutation':True,'attempt':attempt,'phase':'clean-start-rebuild' if clean else 'task-aware-existing-board-mutation','board_id':actual,'text':text[:3500]})
  if _semantic_ok(mut) and actual:break
  feedback=text
 else:return {'ok':False,'verified':False,'mutated':False,'error':'penpot_task_mutation_failed','board_id':actual,'trace':trace}
 verify_code=f'''const board=penpot.currentPage.getShapeById("{actual}"); if (!board) throw new Error("board_not_found"); return JSON.stringify({{id:board.id,name:board.name,childCount:board.children.length}});'''
 vr=call_tool('execute_code',{'code':verify_code});vtxt=_text_from_result(vr);trace.append({'tool':'execute_code','ok':_semantic_ok(vr),'mutation':False,'phase':'post-mutation-structure-check','board_id':actual,'text':vtxt[:1200]})
 if not _semantic_ok(vr):return {'ok':False,'verified':False,'mutated':True,'error':'penpot_post_mutation_structure_check_failed','board_id':actual,'trace':trace}
 if 'export_shape' not in names:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_export_shape_missing','board_id':actual,'trace':trace}
 exp=call_tool('export_shape',{'format':'png','mode':'shape','shapeId':actual});imgs=_images_from_result(exp);trace.append({'tool':'export_shape','ok':bool(exp.get('ok')),'mutation':False,'shapeId':actual,'image_count':len(imgs),'text':_text_from_result(exp)[:700]})
 if not imgs:return {'ok':False,'verified':False,'mutated':True,'error':'penpot_no_visual_evidence','board_id':actual,'trace':trace}
 v=visual_verify(imgs[0],task,design_brief);checks.append(v);passed=v.get('verdict')=='PASS';return {'ok':passed,'verified':passed,'mutated':True,'board_id':actual,'error':None if passed else 'penpot_visual_verification_failed','visual_checks':checks,'trace':trace,'model':MODEL,'vision_model':VISION_MODEL}
if __name__=='__main__':print(json.dumps({'status':status(),'tools':[x['name'] for x in list_tools()]},ensure_ascii=False,indent=2))
