#!/usr/bin/env python3
"""Doré Design 0.5 — local-first structured design workbench."""
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
from html import escape
import json,os,datetime,re,hashlib
DATA=Path(os.environ.get("DORE_DESIGN_DATA",Path.home()/".dore/design")).expanduser();DATA.mkdir(parents=True,exist_ok=True)
HIST=DATA/"history";HIST.mkdir(exist_ok=True);EXPORTS=DATA/"exports";EXPORTS.mkdir(exist_ok=True)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def pf(i):return DATA/f"{i}.json"
def hp(i,r):return HIST/f"{i}.r{int(r):04d}.json"
def valid_id(v):return bool(re.fullmatch(r"[A-Za-z0-9._-]{1,80}",str(v or "")))
def atomic_write(p,text):
 t=p.with_suffix(p.suffix+".tmp");t.write_text(text,encoding="utf-8");t.replace(p)
def default_doc():
 return {"schema":"dore.design.v1","id":"westside-watch","name":"Westside Watch — Doré Design","revision":1,"updated_at":now(),"canvas":{"w":1200,"h":930},"tokens":{"paper":"#FAF9F5","ink":"#252525","night":"#102A43","gold":"#A2872A","morning":"#D2BC69"},"nodes":[{"id":"masthead","type":"text","role":"masthead","text":"WESTSIDE WATCH","x":72,"y":64,"w":760,"size":58},{"id":"zh","type":"text","role":"subtitle","text":"西區守望","x":76,"y":132,"w":360,"size":22},{"id":"rule","type":"rule","x":72,"y":180,"w":1056,"h":1},{"id":"hero","type":"text","role":"hero","text":"WATCH FOR\nTHE DAWN","x":72,"y":250,"w":650,"size":92},{"id":"feature","type":"block","role":"feature","x":790,"y":250,"w":338,"h":540,"eyebrow":"本月專題 · FEATURE","title":"守望，\n一座光明的城","body":"在黑夜仍未完全退去以前，守望者先看見黎明。"},{"id":"footer","type":"text","role":"footer","text":"A CITY OF LIGHT  ·  WATCH NIGHT / MORNING GOLD","x":72,"y":860,"w":900,"size":15}]}
def validate(d):
 e=[]
 if d.get("schema")!="dore.design.v1":e.append("schema")
 if not valid_id(d.get("id")):e.append("document_id")
 c=d.get("canvas") or {}
 if not isinstance(c.get("w"),(int,float)) or not isinstance(c.get("h"),(int,float)):e.append("canvas")
 seen=set()
 for n in d.get("nodes",[]):
  nid=n.get("id")
  if not valid_id(nid) or nid in seen:e.append(f"node_id:{nid}")
  seen.add(nid)
  if n.get("type") not in {"text","rule","block"}:e.append(f"node_type:{nid}")
  for k in ("x","y","w"):
   if not isinstance(n.get(k),(int,float)):e.append(f"{nid}.{k}")
 return e
def load(i):
 if not valid_id(i):raise ValueError("invalid_document_id")
 p=pf(i)
 if not p.exists():
  if i!="westside-watch":raise FileNotFoundError(i)
  atomic_write(p,json.dumps(default_doc(),ensure_ascii=False,indent=2))
 d=json.loads(p.read_text(encoding="utf-8"));errs=validate(d)
 if errs:raise ValueError("invalid_document:"+",".join(errs))
 return d
def snapshot(d):
 p=hp(d["id"],d["revision"])
 if not p.exists():atomic_write(p,json.dumps(d,ensure_ascii=False,indent=2))
def save(d):
 errs=validate(d)
 if errs:raise ValueError("invalid_document:"+",".join(errs))
 if pf(d["id"]).exists():snapshot(load(d["id"]))
 d["revision"]=int(d.get("revision",0))+1;d["updated_at"]=now();atomic_write(pf(d["id"]),json.dumps(d,ensure_ascii=False,indent=2));return d
def history(i):
 rows=[]
 for p in sorted(HIST.glob(f"{i}.r*.json")):
  try:
   d=json.loads(p.read_text(encoding="utf-8"));rows.append({"revision":d["revision"],"updated_at":d.get("updated_at"),"path":p.name})
  except:pass
 cur=load(i);rows.append({"revision":cur["revision"],"updated_at":cur.get("updated_at"),"current":True});return rows
def restore(i,rev):
 src=hp(i,rev)
 if not src.exists():raise ValueError("revision_not_found")
 target=json.loads(src.read_text(encoding="utf-8"));cur=load(i);snapshot(cur);target["revision"]=cur["revision"]+1;target["updated_at"]=now();atomic_write(pf(i),json.dumps(target,ensure_ascii=False,indent=2));return target
def mutate(d,p):
 op=p.get("op");nid=p.get("id");node=next((x for x in d["nodes"] if x["id"]==nid),None) if nid else None
 if op=="set":
  if not node:raise ValueError("node_not_found")
  patch=p.get("patch") or {}
  if "id" in patch and patch["id"]!=nid:raise ValueError("node_id_immutable")
  node.update(patch)
 elif op=="add":
  n=p.get("node") or {}
  if not valid_id(n.get("id")) or any(x["id"]==n["id"] for x in d["nodes"]):raise ValueError("invalid_or_duplicate_node_id")
  d["nodes"].append(n)
 elif op=="delete":
  if not node:raise ValueError("node_not_found")
  d["nodes"]=[x for x in d["nodes"] if x["id"]!=nid]
 elif op=="token":
  key=p.get("key");value=p.get("value")
  if key not in d["tokens"] or not isinstance(value,str):raise ValueError("invalid_token")
  d["tokens"][key]=value
 elif op=="canvas":
  patch=p.get("patch") or {}
  for k in ("w","h"):
   if k in patch and (not isinstance(patch[k],(int,float)) or patch[k]<=0):raise ValueError("invalid_canvas")
  d["canvas"].update(patch)
 else:raise ValueError("unsupported_op")
 return save(d)
def batch(d,ops):
 if not isinstance(ops,list) or not ops or len(ops)>100:raise ValueError("invalid_batch")
 for op in ops:
  kind=op.get("op");nid=op.get("id");node=next((x for x in d["nodes"] if x["id"]==nid),None) if nid else None
  if kind=="set":
   if not node:raise ValueError("node_not_found")
   patch=op.get("patch") or {}
   if "id" in patch and patch["id"]!=nid:raise ValueError("node_id_immutable")
   node.update(patch)
  elif kind=="token":
   if op.get("key") not in d["tokens"]:raise ValueError("invalid_token")
   d["tokens"][op["key"]]=op.get("value")
  elif kind=="add":
   n=op.get("node") or {}
   if not valid_id(n.get("id")) or any(x["id"]==n["id"] for x in d["nodes"]):raise ValueError("invalid_or_duplicate_node_id")
   d["nodes"].append(n)
  elif kind=="delete":
   if not node:raise ValueError("node_not_found")
   d["nodes"]=[x for x in d["nodes"] if x["id"]!=nid]
  else:raise ValueError("unsupported_batch_op")
 return save(d)
def svg(d):
 t=d["tokens"];w=d["canvas"]["w"];h=d["canvas"]["h"];out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{w}" height="{h}" viewBox="0 0 {w} {h}"><rect width="100%" height="100%" fill="{escape(t["paper"])}"/>']
 for n in d["nodes"]:
  if n["type"]=="rule":out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n.get("h",1)}" fill="{escape(t["gold"])}"/>');continue
  if n["type"]=="block":out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="8" fill="{escape(t["gold"])}"/>');texts=[(n.get("eyebrow",""),13,t["gold"],32),(n.get("title",""),52,t["ink"],100),(n.get("body",""),18,t["ink"],260)]
  else:texts=[(n.get("text",""),n.get("size",18),t["night"] if n.get("role")=="hero" else t["ink"],0)]
  for text,size,color,dy in texts:
   for j,line in enumerate(str(text).split("\n")):out.append(f'<text x="{n["x"]}" y="{n["y"]+dy+(j+1)*size}" font-family="Georgia,serif" font-size="{size}" fill="{escape(color)}">{escape(line)}</text>')
 out.append("</svg>");return "".join(out)
def verify(d):
 errs=validate(d);rendered=svg(d);ids=[n["id"] for n in d["nodes"]];checks={"schema_valid":not errs,"stable_unique_node_ids":len(ids)==len(set(ids)),"render_nonempty":len(rendered)>200 and "<svg" in rendered,"required_visual_roles":all(x in ids for x in ("masthead","hero","feature")),"history_available":len(history(d["id"]))>=1}
 return {"ok":all(checks.values()),"document_id":d["id"],"revision":d["revision"],"checks":checks,"errors":errs,"render_sha256":hashlib.sha256(rendered.encode()).hexdigest(),"node_count":len(ids)}
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Doré Design</title><style>*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:system-ui;background:#d2d2d2;color:#171717}#top{height:48px;background:#171717;color:#eee;display:flex;align-items:center;padding:0 16px;gap:14px;position:fixed;inset:0 0 auto;z-index:10;font-size:13px}#top button,#top a{background:#303030;color:#fff;border:1px solid #555;padding:6px 10px;text-decoration:none}#app{display:grid;grid-template-columns:220px 1fr 280px;height:100%;padding-top:48px}.panel{background:#f3f3f1;border-right:1px solid #bbb;overflow:auto;padding:14px}.right{border-right:0;border-left:1px solid #bbb}#stageWrap{overflow:auto;padding:32px}.page{position:relative;margin:auto;background:var(--paper);color:var(--ink);box-shadow:0 8px 35px #0003;overflow:hidden}.node{position:absolute;box-sizing:border-box}.node.sel{outline:2px solid #6d6d6d;outline-offset:4px}.text{white-space:pre-line;font-family:Georgia,serif;line-height:.92;letter-spacing:.02em}.subtitle{letter-spacing:.28em}.rule{background:var(--gold)}.block{border-top:8px solid var(--gold);padding-top:22px}.block .eye{font-size:13px;letter-spacing:.18em;color:var(--gold);margin-bottom:30px}.block h2{font:54px/1.05 Georgia,serif;white-space:pre-line;margin:0 0 30px}.block p{font:18px/1.8 Georgia,serif}.hero{color:var(--night)}.footer{letter-spacing:.16em}h3{font-size:12px;text-transform:uppercase;letter-spacing:.12em;margin:8px 0}.row{display:flex;gap:6px;margin:6px 0}.row>*{min-width:0}input,textarea{width:100%;padding:6px;border:1px solid #aaa;background:#fff}textarea{height:90px}.layer{padding:6px;border-bottom:1px solid #ddd;cursor:pointer;font-size:12px}.layer.active{font-weight:700;background:#e4e1d8}.token{display:grid;grid-template-columns:1fr 72px;gap:6px;margin:6px 0}.small{font-size:11px;color:#666}.ok{color:#396b39}.bad{color:#933}</style></head><body><div id="top"><b>DORÉ DESIGN 0.5</b><span id="status">loading</span><button onclick="undo()">Undo</button><button onclick="verifyNow()">Verify</button><a href="/api/document/westside-watch/export.svg" target="_blank">SVG Export</a><span>local · structured · editable · versioned</span></div><div id="app"><aside class="panel"><h3>Layers</h3><div id="layers"></div><h3>Tokens</h3><div id="tokens"></div></aside><main id="stageWrap"><div id="stage"></div></main><aside class="panel right"><h3>Inspector</h3><div id="inspector" class="small">Select a layer.</div><h3>Verification</h3><pre id="verification" class="small"></pre></aside></div><script>const ID='westside-watch';let doc,selected=null,hist=[];async function api(url,opt){let r=await fetch(url,opt);let j=await r.json();if(!r.ok)throw Error(j.error||r.status);return j}async function reload(){doc=await api('/api/document/'+ID);hist=await api('/api/document/'+ID+'/history');render()}function esc(s){return String(s).replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]))}function nodeHTML(n){if(n.type==='block')return `<div class="eye">${esc(n.eyebrow||'')}</div><h2>${esc(n.title||'').replaceAll('\\n','<br>')}</h2><p>${esc(n.body||'')}</p>`;return esc(n.text||'').replaceAll('\\n','<br>')}function render(){let p=document.createElement('div');p.className='page';p.style.width=doc.canvas.w+'px';p.style.height=doc.canvas.h+'px';Object.entries(doc.tokens).forEach(([k,v])=>p.style.setProperty('--'+k,v));doc.nodes.forEach(n=>{let e=document.createElement('div');e.className='node '+n.type+' '+(n.role||'')+(n.id===selected?' sel':'');e.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}`;e.innerHTML=nodeHTML(n);e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};p.appendChild(e)});p.onclick=()=>{selected=null;render()};stage.innerHTML='';stage.appendChild(p);layers.innerHTML=doc.nodes.map(n=>`<div class="layer ${n.id===selected?'active':''}" onclick="selected='${n.id}';render()">${esc(n.id)} · ${esc(n.type)}</div>`).join('');tokens.innerHTML=Object.entries(doc.tokens).map(([k,v])=>`<div class="token"><span>${k}</span><input value="${esc(v)}" onchange="setToken('${k}',this.value)"></div>`).join('');status.textContent=`${doc.name} · r${doc.revision}`;renderInspector()}function renderInspector(){let n=doc.nodes.find(x=>x.id===selected);if(!n){inspector.innerHTML='Select a layer.';return}let fields=['x','y','w','h','size'];inspector.innerHTML=`<b>${esc(n.id)}</b><div class="small">${esc(n.type)} · ${esc(n.role||'')}</div>`+fields.filter(k=>n[k]!=null).map(k=>`<label>${k}<input type="number" value="${n[k]}" onchange="patch('${k}',Number(this.value))"></label>`).join('')+(n.text!=null?`<label>text<textarea onchange="patch('text',this.value)">${esc(n.text)}</textarea></label>`:'')+(n.title!=null?`<label>title<textarea onchange="patch('title',this.value)">${esc(n.title)}</textarea></label><label>body<textarea onchange="patch('body',this.value)">${esc(n.body||'')}</textarea></label>`:'')+`<div class="row"><button onclick="duplicate()">Duplicate</button><button onclick="delNode()">Delete</button></div>`}async function post(payload,path='mutate'){await api(`/api/document/${ID}/${path}`,{method:'POST',headers:{'content-type':'application/json'},body:JSON.stringify(payload)});await reload()}async function patch(k,v){await post({op:'set',id:selected,patch:{[k]:v}})}async function setToken(k,v){await post({op:'token',key:k,value:v})}async function duplicate(){let n=JSON.parse(JSON.stringify(doc.nodes.find(x=>x.id===selected)));n.id=n.id+'-copy';n.x+=24;n.y+=24;await post({op:'add',node:n});selected=n.id}async function delNode(){if(selected)await post({op:'delete',id:selected});selected=null}async function undo(){let prev=[...hist].filter(x=>!x.current&&x.revision<doc.revision).pop();if(!prev)return;await post({revision:prev.revision},'restore')}async function verifyNow(){let v=await api(`/api/document/${ID}/verify`);verification.textContent=JSON.stringify(v,null,2);verification.className='small '+(v.ok?'ok':'bad')}reload();verifyNow()</script></body></html>'''
class H(BaseHTTPRequestHandler):
 def log_message(self,*a):pass
 def send(self,c,b,t="application/json; charset=utf-8"):
  b=b.encode();self.send_response(c);self.send_header("Content-Type",t);self.send_header("Cache-Control","no-store");self.send_header("Content-Length",str(len(b)));self.end_headers();self.wfile.write(b)
 def json(self,c,o):self.send(c,json.dumps(o,ensure_ascii=False))
 def body(self):n=int(self.headers.get("content-length","0"));return json.loads(self.rfile.read(n) or b"{}")
 def do_GET(self):
  p=urlparse(self.path).path
  try:
   if p=="/":return self.send(200,HTML,"text/html; charset=utf-8")
   if p=="/api/health":return self.json(200,{"ok":True,"service":"dore-design","version":"0.5","data":str(DATA)})
   parts=p.strip("/").split("/")
   if len(parts)>=3 and parts[:2]==["api","document"]:
    i=parts[2]
    if len(parts)==3:return self.json(200,load(i))
    if len(parts)==4 and parts[3]=="history":return self.json(200,history(i))
    if len(parts)==4 and parts[3]=="verify":return self.json(200,verify(load(i)))
    if len(parts)==4 and parts[3]=="export.svg":
     s=svg(load(i));atomic_write(EXPORTS/f"{i}.svg",s);return self.send(200,s,"image/svg+xml; charset=utf-8")
   return self.json(404,{"ok":False,"error":"not_found"})
  except FileNotFoundError:return self.json(404,{"ok":False,"error":"document_not_found"})
  except ValueError as e:return self.json(400,{"ok":False,"error":str(e)})
 def do_POST(self):
  parts=urlparse(self.path).path.strip("/").split("/")
  try:p=self.body()
  except:return self.json(400,{"ok":False,"error":"bad_json"})
  try:
   if len(parts)==4 and parts[:2]==["api","document"]:
    i=parts[2];a=parts[3]
    if a=="mutate":d=mutate(load(i),p);return self.json(200,{"ok":True,"revision":d["revision"],"document":d})
    if a=="batch":d=batch(load(i),p.get("ops"));return self.json(200,{"ok":True,"revision":d["revision"],"document":d})
    if a=="restore":d=restore(i,p.get("revision"));return self.json(200,{"ok":True,"revision":d["revision"],"document":d})
   return self.json(404,{"ok":False,"error":"not_found"})
  except (ValueError,TypeError) as e:return self.json(400,{"ok":False,"error":str(e)})
if __name__=="__main__":
 host=os.environ.get("DORE_DESIGN_HOST","127.0.0.1");port=int(os.environ.get("DORE_DESIGN_PORT","4310"));print(f"Doré Design 0.5 http://{host}:{port}",flush=True);ThreadingHTTPServer((host,port),H).serve_forever()
