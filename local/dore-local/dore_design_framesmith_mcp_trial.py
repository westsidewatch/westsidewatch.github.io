#!/usr/bin/env python3
"""Bounded Framesmith MCP real-work trial using standard stdio MCP JSON-RPC.
Goal: real Westside Watch canvas -> screenshot -> same-canvas edit -> screenshot.
No model/API dependency; Doré drives Framesmith's native MCP tools directly.
"""
from __future__ import annotations
import json, os, subprocess, threading, queue, time, base64
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
REPO=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
P=HOME/'runtime/design-providers/framesmith'
E=HOME/'evolution/design-bakeoff/framesmith-mcp'; E.mkdir(parents=True,exist_ok=True)

class MCP:
 def __init__(self):
  self.p=subprocess.Popen(['node',str(P/'dist/index.js')],cwd=REPO,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1)
  self.q=queue.Queue(); self.n=0
  threading.Thread(target=self._read,daemon=True).start()
 def _read(self):
  for line in self.p.stdout:
   try:self.q.put(json.loads(line))
   except:pass
 def req(self,method,params=None,timeout=90):
  self.n+=1; i=self.n; msg={'jsonrpc':'2.0','id':i,'method':method}
  if params is not None:msg['params']=params
  self.p.stdin.write(json.dumps(msg)+'\n');self.p.stdin.flush(); end=time.time()+timeout
  while time.time()<end:
   try:r=self.q.get(timeout=1)
   except queue.Empty:continue
   if r.get('id')==i:
    if 'error' in r: raise RuntimeError(method+': '+json.dumps(r['error']))
    return r.get('result')
  raise TimeoutError(method)
 def notify(self,method,params=None):
  m={'jsonrpc':'2.0','method':method};
  if params is not None:m['params']=params
  self.p.stdin.write(json.dumps(m)+'\n');self.p.stdin.flush()
 def tool(self,name,args,timeout=120): return self.req('tools/call',{'name':name,'arguments':args},timeout)
 def close(self):
  try:self.p.terminate();self.p.wait(timeout=3)
  except: self.p.kill()

def unwrap(r):
 if isinstance(r,dict) and r.get('structuredContent') is not None:return r['structuredContent']
 if isinstance(r,dict):
  for x in r.get('content') or []:
   if x.get('type')=='text':
    try:return json.loads(x.get('text',''))
    except:return {'text':x.get('text','')}
 return r

def main():
 m=None; trace=[]
 try:
  m=MCP(); init=m.req('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'dore','version':'0.1'}},30);m.notify('notifications/initialized')
  tools=m.req('tools/list',{},30); names=[x['name'] for x in tools.get('tools',[])]
  required=['init','canvas_create','generate_design_system','list_structures','apply_structure','batch_design','canvas_screenshot','canvas_evaluate']
  missing=[x for x in required if x not in names]
  if missing: raise RuntimeError('missing_tools:'+','.join(missing))
  state=unwrap(m.tool('init',{'dir':str(REPO),'workspaceName':'Doré Design','projects':['Foundations','Westside Watch']}));trace.append(['init',state])
  # Resolve project from init, otherwise project_list.
  plist=unwrap(m.tool('project_list',{}));trace.append(['projects',plist])
  projects=(plist.get('projects') if isinstance(plist,dict) else None) or []
  target=next((x for x in projects if str(x.get('name','')).lower()=='westside watch'),projects[-1] if projects else None)
  if not target: raise RuntimeError('westside_project_not_found')
  pid=target.get('id') or target.get('projectId')
  c=unwrap(m.tool('canvas_create',{'name':'Westside Watch — Homepage 0.1','projectId':pid}));trace.append(['create',c])
  cid=c.get('id') or c.get('canvasId') or (c.get('canvas') or {}).get('id')
  if not cid: raise RuntimeError('canvas_id_missing:'+json.dumps(c))
  ds=unwrap(m.tool('generate_design_system',{'canvasId':cid,'seed':'#A2872A','personality':'editorial'}));trace.append(['design_system',ds])
  structs=unwrap(m.tool('list_structures',{}));trace.append(['structures',structs])
  # Use Framesmith's vetted editorial page scaffold.
  ap=unwrap(m.tool('apply_structure',{'canvasId':cid,'structure':'editorial-longform'}));trace.append(['structure',ap])
  # Find visible text nodes, then perform brand/content edits using native query/update tools when available.
  if 'find_nodes' in names and 'replace_matching_properties' in names:
   found=unwrap(m.tool('find_nodes',{'canvasId':cid,'property':'type','value':'text'}));trace.append(['find_text',found])
  # First render is real evidence even if content refinement must use batch ops later.
  shot1=unwrap(m.tool('canvas_screenshot',{'canvasId':cid,'width':1440,'height':1000}));trace.append(['shot1',shot1])
  # Same-artifact second edit: add a branded editorial hero block with native batch_design ops.
  ops=[
   {'op':'add','parentId':'root','node':{'type':'frame','name':'Doré Brand Revision','layout':'vertical','gap':16,'padding':[40,64],'fill':'#FAF9F5','children':[
    {'type':'text','name':'Masthead','text':'WESTSIDE WATCH','fontSize':56,'fontWeight':600,'fill':'#252525'},
    {'type':'text','name':'Chinese Masthead','text':'西區守望','fontSize':30,'fontWeight':400,'fill':'#252525'},
    {'type':'text','name':'Dawn Line','text':'WATCH FOR THE DAWN','fontSize':15,'letterSpacing':3,'fill':'#A2872A'},
    {'type':'text','name':'Feature','text':'守望，一座光明的城','fontSize':42,'fontWeight':600,'fill':'#102A43'},
    {'type':'text','name':'Feature Label','text':'本月專題 · FEATURE','fontSize':14,'letterSpacing':2,'fill':'#A2872A'}
   ]}}
  ]
  edit=unwrap(m.tool('batch_design',{'canvasId':cid,'operations':ops}));trace.append(['edit',edit])
  shot2=unwrap(m.tool('canvas_screenshot',{'canvasId':cid,'width':1440,'height':1000}));trace.append(['shot2',shot2])
  ev=unwrap(m.tool('canvas_evaluate',{'canvasId':cid,'mode':'fast'}));trace.append(['evaluate',ev])
  out={'ok':True,'provider':'framesmith','artifact':cid,'structured_editable':True,'visible':True,'render':shot1,'second_edit':True,'second_render':shot2,'evaluation':ev,'viewer_hint':'run framesmith-viewer against persisted canvas','trace':trace}
  (E/'latest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));return 0
 except Exception as e:
  out={'ok':False,'provider':'framesmith','cause':type(e).__name__+': '+str(e),'trace':trace}
  (E/'latest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));return 1
 finally:
  if m:m.close()
if __name__=='__main__':raise SystemExit(main())
