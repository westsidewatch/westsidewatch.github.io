#!/usr/bin/env python3
"""Doré Design 0.2 — local structured design engine, history, CRUD, SVG export and browser workbench."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from html import escape
import json,os,datetime,shutil
DATA=Path(os.environ.get('DORE_DESIGN_DATA',Path.home()/'.dore/design'));DATA.mkdir(parents=True,exist_ok=True);HIST=DATA/'history';HIST.mkdir(exist_ok=True)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pf(i):return DATA/(i+'.json')
def default_doc():
 return {'schema':'dore.design.v1','id':'westside-watch','name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'canvas':{'w':1200,'h':930},'tokens':{'paper':'#FAF9F5','ink':'#252525','night':'#102A43','gold':'#A2872A','morning':'#D2BC69'},'nodes':[{'id':'masthead','type':'text','role':'masthead','text':'WESTSIDE WATCH','x':72,'y':64,'w':760,'size':58},{'id':'zh','type':'text','role':'subtitle','text':'西區守望','x':76,'y':132,'w':360,'size':22},{'id':'rule','type':'rule','x':72,'y':180,'w':1056,'h':1},{'id':'hero','type':'text','role':'hero','text':'WATCH FOR\nTHE DAWN','x':72,'y':250,'w':650,'size':92},{'id':'feature','type':'block','role':'feature','x':790,'y':250,'w':338,'h':540,'eyebrow':'本月專題 · FEATURE','title':'守望，\n一座光明的城','body':'在黑夜仍未完全退去以前，守望者先看見黎明。'},{'id':'footer','type':'text','role':'footer','text':'A CITY OF LIGHT  ·  WATCH NIGHT / MORNING GOLD','x':72,'y':860,'w':900,'size':15}]}
def load(i):
 p=pf(i)
 if not p.exists():p.write_text(json.dumps(default_doc(),ensure_ascii=False,indent=2))
 return json.loads(p.read_text())
def save(d):
 old=pf(d['id']);rev=int(d.get('revision',0));
 if old.exists():shutil.copy2(old,HIST/f"{d['id']}.r{rev:04d}.json")
 d['revision']=rev+1;d['updated_at']=now();old.write_text(json.dumps(d,ensure_ascii=False,indent=2));return d
def svg(d):
 t=d['tokens'];w=d.get('canvas',{}).get('w',1200);h=d.get('canvas',{}).get('h',930);out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="{t["paper"]}"/>']
 for n in d['nodes']:
  if n['type']=='rule':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n.get("h",1)}" fill="{t["gold"]}"/>');continue
  if n['type']=='block':
   out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="8" fill="{t["gold"]}"/>');texts=[(n.get('eyebrow',''),13,t['gold'],32),(n.get('title',''),52,t['ink'],100),(n.get('body',''),18,t['ink'],260)]
  else:texts=[(n.get('text',''),n.get('size',18),t['night'] if n.get('role')=='hero' else t['ink'],0)]
  for text,size,color,dy in texts:
   for j,line in enumerate(text.split('\n')):out.append(f'<text x="{n["x"]}" y="{n["y"]+dy+(j+1)*size}" font-family="Georgia,serif" font-size="{size}" fill="{color}">{escape(line)}</text>')
 out.append('</svg>');return ''.join(out)
def mutate(d,p):
 op=p.get('op');nid=p.get('id');node=next((x for x in d['nodes'] if x['id']==nid),None) if nid else None
 if op=='set':
  if not node:raise ValueError('node_not_found')
  node.update(p.get('patch') or {})
 elif op=='add':
  n=p.get('node') or {}
  if not n.get('id') or any(x['id']==n['id'] for x in d['nodes']):raise ValueError('invalid_or_duplicate_node_id')
  d['nodes'].append(n)
 elif op=='delete':
  if not node:raise ValueError('node_not_found')
  d['nodes']=[x for x in d['nodes'] if x['id']!=nid]
 elif op=='token':
  key=p.get('key');value=p.get('value')
  if key not in d['tokens'] or not isinstance(value,str):raise ValueError('invalid_token')
  d['tokens'][key]=value
 else:raise ValueError('unsupported_op')
 return save(d)
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Doré Design</title><style>html,body{margin:0;height:100%;background:#d7d7d7;font-family:system-ui}#bar{height:48px;background:#171717;color:#eee;display:flex;align-items:center;padding:0 18px;gap:16px;font-size:13px;position:sticky;top:0;z-index:3}button,a{background:#333;color:white;border:1px solid #555;padding:6px 10px;text-decoration:none}#stage{padding:32px;display:flex;justify-content:center}.page{position:relative;width:1200px;height:930px;background:var(--paper);color:var(--ink);box-shadow:0 8px 35px #0003;overflow:hidden}.node{position:absolute;box-sizing:border-box}.text{white-space:pre-line;font-family:Georgia,serif;line-height:.92;letter-spacing:.02em}.subtitle{letter-spacing:.28em}.rule{background:var(--gold)}.block{border-top:8px solid var(--gold);padding-top:22px}.block .eye{font-size:13px;letter-spacing:.18em;color:var(--gold);margin-bottom:30px}.block h2{font:54px/1.05 Georgia,serif;white-space:pre-line;margin:0 0 30px}.block p{font:18px/1.8 Georgia,serif}.hero{color:var(--night)}.footer{letter-spacing:.16em}</style></head><body><div id="bar"><b>DORÉ DESIGN 0.2</b><span id="status">loading</span><button onclick="refine()">Refine same document</button><a href="/api/document/westside-watch/export.svg" target="_blank">SVG export</a><span>structured · editable · versioned · local</span></div><div id="stage"></div><script>let doc;async function get(){doc=await(await fetch('/api/document/westside-watch')).json();render()}function render(){let p=document.createElement('div');p.className='page';Object.entries(doc.tokens).forEach(([k,v])=>p.style.setProperty('--'+k,v));doc.nodes.forEach(n=>{let e=document.createElement('div');e.className='node '+n.type+' '+(n.role||'');e.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}`;if(n.type==='block')e.innerHTML=`<div class="eye">${n.eyebrow}</div><h2>${n.title}</h2><p>${n.body}</p>`;else e.textContent=n.text||'';p.appendChild(e)});stage.innerHTML='';stage.appendChild(p);status.textContent=`${doc.name} · r${doc.revision}`}async function refine(){await fetch('/api/document/westside-watch/mutate',{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify({op:'set',id:'hero',patch:{size:86,x:76}})});get()}get()</script></body></html>'''
class H(BaseHTTPRequestHandler):
 def send(self,c,b,t='application/json; charset=utf-8'):b=b.encode();self.send_response(c);self.send_header('Content-Type',t);self.send_header('Content-Length',len(b));self.end_headers();self.wfile.write(b)
 def do_GET(self):
  p=urlparse(self.path).path
  if p=='/':return self.send(200,HTML,'text/html; charset=utf-8')
  if p.endswith('/export.svg') and p.startswith('/api/document/'):return self.send(200,svg(load(p.split('/')[-2])),'image/svg+xml; charset=utf-8')
  if p.startswith('/api/document/'):return self.send(200,json.dumps(load(p.split('/')[-1]),ensure_ascii=False))
  return self.send(404,json.dumps({'ok':False}))
 def do_POST(self):
  parts=urlparse(self.path).path.strip('/').split('/');n=int(self.headers.get('content-length','0'))
  try:p=json.loads(self.rfile.read(n) or b'{}')
  except:return self.send(400,json.dumps({'ok':False,'error':'bad_json'}))
  if len(parts)==4 and parts[:2]==['api','document'] and parts[3]=='mutate':
   try:d=mutate(load(parts[2]),p);return self.send(200,json.dumps({'ok':True,'revision':d['revision'],'document':d},ensure_ascii=False))
   except ValueError as e:return self.send(400,json.dumps({'ok':False,'error':str(e)}))
  return self.send(404,json.dumps({'ok':False}))
if __name__=='__main__':
 host=os.environ.get('DORE_DESIGN_HOST','127.0.0.1');port=int(os.environ.get('DORE_DESIGN_PORT','4310'));print(f'Doré Design http://{host}:{port}',flush=True);ThreadingHTTPServer((host,port),H).serve_forever()
