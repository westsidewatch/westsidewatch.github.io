#!/usr/bin/env python3
"""Doré Design 0.1 — zero-dependency local structured design engine + browser workbench."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json,os,uuid,datetime
ROOT=Path(__file__).resolve().parent; DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design')); DATA.mkdir(parents=True,exist_ok=True)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def path_for(i):return DATA/(i+'.json')
def default_doc():
 i='westside-watch';return {'schema':'dore.design.v1','id':i,'name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'tokens':{'paper':'#FAF9F5','ink':'#252525','night':'#102A43','gold':'#A2872A','morning':'#D2BC69'},'nodes':[{'id':'masthead','type':'text','role':'masthead','text':'WESTSIDE WATCH','x':72,'y':64,'w':760,'size':58},{'id':'zh','type':'text','role':'subtitle','text':'西區守望','x':76,'y':132,'w':360,'size':22},{'id':'rule','type':'rule','x':72,'y':180,'w':1056,'h':1},{'id':'hero','type':'text','role':'hero','text':'WATCH FOR\nTHE DAWN','x':72,'y':250,'w':650,'size':92},{'id':'feature','type':'block','role':'feature','x':790,'y':250,'w':338,'h':540,'eyebrow':'本月專題 · FEATURE','title':'守望，\n一座光明的城','body':'在黑夜仍未完全退去以前，守望者先看見黎明。'},{'id':'footer','type':'text','role':'footer','text':'A CITY OF LIGHT  ·  WATCH NIGHT / MORNING GOLD','x':72,'y':860,'w':900,'size':15}]}
def load(i):
 p=path_for(i)
 if not p.exists():
  d=default_doc();p.write_text(json.dumps(d,ensure_ascii=False,indent=2))
 return json.loads(p.read_text())
def save(d):d['revision']=int(d.get('revision',0))+1;d['updated_at']=now();path_for(d['id']).write_text(json.dumps(d,ensure_ascii=False,indent=2));return d
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Doré Design</title><style>html,body{margin:0;height:100%;background:#ddd;font-family:system-ui}#bar{height:48px;background:#171717;color:#eee;display:flex;align-items:center;padding:0 18px;gap:18px;font-size:13px}button{background:#333;color:white;border:1px solid #555;padding:6px 12px}#stage{padding:32px;display:flex;justify-content:center}.page{position:relative;width:1200px;height:930px;background:var(--paper);color:var(--ink);box-shadow:0 8px 35px #0003;overflow:hidden}.node{position:absolute;box-sizing:border-box}.text{white-space:pre-line;font-family:Georgia,'Times New Roman',serif;line-height:.92;letter-spacing:.02em}.subtitle{letter-spacing:.28em}.rule{background:var(--gold)}.block{border-top:8px solid var(--gold);padding-top:22px}.block .eye{font-size:13px;letter-spacing:.18em;color:var(--gold);margin-bottom:30px}.block h2{font:54px/1.05 Georgia,serif;white-space:pre-line;margin:0 0 30px}.block p{font:18px/1.8 Georgia,serif}.hero{color:var(--night)}.footer{letter-spacing:.16em}</style></head><body><div id="bar"><b>DORÉ DESIGN 0.1</b><span id="status">loading</span><button onclick="mutate()">Refine same document</button><span>Structured JSON · live browser canvas · local</span></div><div id="stage"></div><script>let doc;async function get(){doc=await(await fetch('/api/document/westside-watch')).json();render()}function render(){let p=document.createElement('div');p.className='page';Object.entries(doc.tokens).forEach(([k,v])=>p.style.setProperty('--'+k,v));doc.nodes.forEach(n=>{let e=document.createElement('div');e.className='node '+n.type+' '+(n.role||'');e.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}`;if(n.type==='block')e.innerHTML=`<div class="eye">${n.eyebrow}</div><h2>${n.title}</h2><p>${n.body}</p>`;else e.textContent=n.text||'';p.appendChild(e)});stage.innerHTML='';stage.appendChild(p);status.textContent=`${doc.name} · revision ${doc.revision}`}async function mutate(){await fetch('/api/document/westside-watch/mutate',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({op:'set',id:'hero',patch:{size:86,x:76}})});await get()}get()</script></body></html>'''
class H(BaseHTTPRequestHandler):
 def send(self,code,body,typ='application/json; charset=utf-8'):
  b=body.encode();self.send_response(code);self.send_header('Content-Type',typ);self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  u=urlparse(self.path)
  if u.path=='/':return self.send(200,HTML,'text/html; charset=utf-8')
  if u.path.startswith('/api/document/'):
   i=u.path.split('/')[-1];return self.send(200,json.dumps(load(i),ensure_ascii=False))
  return self.send(404,json.dumps({'ok':False}))
 def do_POST(self):
  u=urlparse(self.path);parts=u.path.strip('/').split('/')
  try:n=int(self.headers.get('content-length','0'));payload=json.loads(self.rfile.read(n) or b'{}')
  except:return self.send(400,json.dumps({'ok':False,'error':'bad_json'}))
  if len(parts)==4 and parts[:2]==['api','document'] and parts[3]=='mutate':
   d=load(parts[2]);nid=payload.get('id');node=next((x for x in d['nodes'] if x['id']==nid),None)
   if not node:return self.send(404,json.dumps({'ok':False,'error':'node_not_found'}))
   if payload.get('op')=='set':node.update(payload.get('patch') or {})
   else:return self.send(400,json.dumps({'ok':False,'error':'unsupported_op'}))
   return self.send(200,json.dumps({'ok':True,'document':save(d)},ensure_ascii=False))
  return self.send(404,json.dumps({'ok':False}))
if __name__=='__main__':
 host=os.environ.get('DORE_DESIGN_HOST','127.0.0.1');port=int(os.environ.get('DORE_DESIGN_PORT','4310'));print(f'Doré Design http://{host}:{port}',flush=True);ThreadingHTTPServer((host,port),H).serve_forever()
