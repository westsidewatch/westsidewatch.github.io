#!/usr/bin/env python3
"""Framesmith real-work trial. Evidence-first: runtime schemas + init-returned IDs drive execution."""
from __future__ import annotations
import json,os,subprocess,threading,queue,time
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();REPO=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser();P=HOME/'runtime/design-providers/framesmith';E=HOME/'evolution/design-bakeoff/framesmith-mcp';E.mkdir(parents=True,exist_ok=True)
class MCP:
 def __init__(self):
  self.p=subprocess.Popen(['node',str(P/'dist/index.js')],cwd=REPO,stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE,text=True,bufsize=1);self.q=queue.Queue();self.n=0;threading.Thread(target=self._read,daemon=True).start()
 def _read(self):
  for l in self.p.stdout:
   try:self.q.put(json.loads(l))
   except:pass
 def req(self,m,p=None,t=90):
  self.n+=1;i=self.n;x={'jsonrpc':'2.0','id':i,'method':m};
  if p is not None:x['params']=p
  self.p.stdin.write(json.dumps(x)+'\n');self.p.stdin.flush();end=time.time()+t
  while time.time()<end:
   try:r=self.q.get(timeout=1)
   except queue.Empty:continue
   if r.get('id')==i:
    if 'error'in r:raise RuntimeError(m+': '+json.dumps(r['error']))
    return r.get('result')
  raise TimeoutError(m)
 def notify(self,m,p=None):
  x={'jsonrpc':'2.0','method':m};
  if p is not None:x['params']=p
  self.p.stdin.write(json.dumps(x)+'\n');self.p.stdin.flush()
 def tool(self,n,a,t=180):return self.req('tools/call',{'name':n,'arguments':a},t)
 def close(self):
  try:self.p.terminate();self.p.wait(timeout=3)
  except:self.p.kill()
def unwrap(r):
 if isinstance(r,dict) and r.get('structuredContent') is not None:return r['structuredContent']
 if isinstance(r,dict):
  for x in r.get('content') or []:
   if x.get('type')=='text':
    try:return json.loads(x.get('text',''))
    except:return {'text':x.get('text','')}
 return r
def main():
 m=None;tr=[]
 try:
  m=MCP();m.req('initialize',{'protocolVersion':'2025-03-26','capabilities':{},'clientInfo':{'name':'dore-supervised','version':'0.3'}},30);m.notify('notifications/initialized')
  listed=m.req('tools/list',{},30);tools={x['name']:x for x in listed.get('tools',[])};tr.append(['runtime_tools',{k:v.get('inputSchema') for k,v in tools.items()}])
  required=['init','canvas_create','generate_design_system','list_structures','apply_structure','batch_design','screenshot','canvas_evaluate'];missing=[x for x in required if x not in tools]
  if missing:raise RuntimeError('runtime_capability_missing:'+','.join(missing))
  state=unwrap(m.tool('init',{'dir':str(REPO),'workspaceName':'Doré Design','projects':['Foundations','Westside Watch']}));tr.append(['init',state])
  # Framesmith upstream initWorkspace explicitly ensures requested projects and RETURNS their re-keyed live IDs.
  projects=(state.get('projects') if isinstance(state,dict) else None) or []
  target=next((x for x in projects if str(x.get('name','')).casefold()=='westside watch'),None)
  if not target:raise RuntimeError('init_contract_violation_missing_requested_project:'+json.dumps(state,ensure_ascii=False))
  pid=target['id']
  c=unwrap(m.tool('canvas_create',{'name':'Westside Watch — Homepage 0.1','projectId':pid}));tr.append(['create',c]);cid=c.get('canvasId') or c.get('id') or (c.get('canvas') or {}).get('id')
  if not cid:raise RuntimeError('canvas_create_contract_missing_id:'+json.dumps(c))
  ds=unwrap(m.tool('generate_design_system',{'canvasId':cid,'seed':'#A2872A','personality':'editorial'}));tr.append(['design_system',ds])
  structs=unwrap(m.tool('list_structures',{}));tr.append(['structures',structs])
  ap=unwrap(m.tool('apply_structure',{'canvasId':cid,'structure':'editorial-longform'}));tr.append(['structure',ap])
  shot1=unwrap(m.tool('screenshot',{'canvasId':cid,'width':1440,'height':1000,'scale':1}));tr.append(['shot1',shot1])
  operations='''hero=I("document", { type: "frame", name: "Westside Watch Brand Hero", layout: "vertical", gap: 16, padding: 64, fill: "#FAF9F5", width: 1440 })\nI(hero, { type: "text", name: "Masthead", content: "WESTSIDE WATCH", fontSize: 56, fontWeight: 600, fill: "#252525" })\nI(hero, { type: "text", name: "Chinese Masthead", content: "西區守望", fontSize: 30, fill: "#252525" })\nI(hero, { type: "text", name: "Dawn Line", content: "WATCH FOR THE DAWN", fontSize: 15, letterSpacing: 3, fill: "#A2872A" })\nI(hero, { type: "text", name: "Feature", content: "守望，一座光明的城", fontSize: 42, fontWeight: 600, fill: "#102A43" })\nI(hero, { type: "text", name: "Feature Label", content: "本月專題 · FEATURE", fontSize: 14, letterSpacing: 2, fill: "#A2872A" })'''
  edit=unwrap(m.tool('batch_design',{'canvasId':cid,'operations':operations}));tr.append(['edit',edit])
  shot2=unwrap(m.tool('screenshot',{'canvasId':cid,'width':1440,'height':1000,'scale':1}));tr.append(['shot2',shot2])
  ev=unwrap(m.tool('canvas_evaluate',{'canvasId':cid,'mode':'fast'}));tr.append(['evaluate',ev])
  out={'ok':True,'provider':'framesmith','artifact':cid,'viewerUrl':c.get('viewerUrl') or state.get('viewerUrl'),'structured_editable':True,'visible':True,'render':shot1,'second_edit':True,'second_render':shot2,'evaluation':ev,'trace':tr}
  (E/'latest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));return 0
 except Exception as e:
  out={'ok':False,'provider':'framesmith','cause':type(e).__name__+': '+str(e),'trace':tr};(E/'latest.json').write_text(json.dumps(out,ensure_ascii=False,indent=2),encoding='utf-8');print(json.dumps(out,ensure_ascii=False));return 1
 finally:
  if m:m.close()
if __name__=='__main__':raise SystemExit(main())
