#!/usr/bin/env python3
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse
import json,os,datetime
import app as core
DATA=core.DATA
WS=DATA/'westside-watch.workspace.json'
def now(): return datetime.datetime.now(datetime.timezone.utc).isoformat()
def atomic(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def workspace():
 if WS.exists(): return json.loads(WS.read_text(encoding='utf-8'))
 d=core.load('westside-watch')
 w={'schema':'dore.design.workspace.v1','id':'westside-watch','name':d['name'],'revision':1,'updated_at':now(),'tokens':d['tokens'],'pages':[{'id':'cover','name':'Cover','canvas':d['canvas'],'nodes':d['nodes']},{'id':'page-02','name':'Page 02','canvas':{'w':1200,'h':930},'nodes':[]},{'id':'page-03','name':'Page 03','canvas':{'w':1200,'h':930},'nodes':[]}]}
 atomic(WS,w);return w
def save(w):
 w['revision']=int(w.get('revision',0))+1;w['updated_at']=now();atomic(WS,w);return w
def mutate(w,p):
 op=p.get('op');pid=p.get('page_id');page=next((x for x in w['pages'] if x['id']==pid),None) if pid else None
 if op=='add_page':
  n=len(w['pages'])+1;w['pages'].append({'id':p.get('id') or f'page-{n:02d}','name':p.get('name') or f'Page {n:02d}','canvas':{'w':1200,'h':930},'nodes':[]})
 elif op=='delete_page':
  if len(w['pages'])<=1: raise ValueError('cannot_delete_last_page')
  if not page: raise ValueError('page_not_found')
  w['pages']=[x for x in w['pages'] if x['id']!=pid]
 elif op=='rename_page':
  if not page: raise ValueError('page_not_found')
  page['name']=str(p.get('name') or page['name'])[:80]
 elif op=='add_text':
  if not page: raise ValueError('page_not_found')
  n=len(page['nodes'])+1;page['nodes'].append({'id':p.get('id') or f'text-{n:02d}','type':'text','text':p.get('text') or 'New text','x':80,'y':100+n*35,'w':700,'size':34})
 elif op=='set_node':
  if not page: raise ValueError('page_not_found')
  node=next((x for x in page['nodes'] if x['id']==p.get('id')),None)
  if not node: raise ValueError('node_not_found')
  node.update(p.get('patch') or {})
 else: raise ValueError('unsupported_op')
 return save(w)
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Doré Design</title><style>*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:system-ui;background:#cfcfcf;color:#202020}#top{height:50px;background:#171717;color:#eee;display:flex;align-items:center;gap:14px;padding:0 16px}button{border:1px solid #777;background:#fff;padding:7px 10px}#top button{background:#333;color:#fff}.app{height:calc(100% - 50px);display:grid;grid-template-columns:250px 1fr 280px}.side{background:#f2f1ed;overflow:auto;padding:14px;border-right:1px solid #aaa}.right{border-right:0;border-left:1px solid #aaa}.pages{display:grid;gap:8px}.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer}.pitem.on{border:2px solid #252525}.thumb{height:72px;background:#faf9f5;border:1px solid #ddd;margin-bottom:6px}.stagewrap{overflow:auto;padding:34px}.stage{position:relative;margin:auto;background:#faf9f5;box-shadow:0 10px 35px #0003;overflow:hidden}.node{position:absolute;font-family:Georgia,serif;white-space:pre-line}.node.sel{outline:2px solid #777;outline-offset:3px}.rule{background:#a2872a}.block{border-top:8px solid #a2872a;padding-top:22px}.block h2{font:52px/1.05 Georgia,serif;white-space:pre-line}.small{font-size:11px;color:#666}h3{font-size:11px;letter-spacing:.14em;text-transform:uppercase}.layer{padding:6px 4px;border-bottom:1px solid #ddd;cursor:pointer}input,textarea{width:100%;margin:4px 0;padding:6px}textarea{height:110px}</style></head><body><div id="top"><b>DORÉ DESIGN 0.6</b><span id="status">multi-page workspace</span><button onclick="addPage()">+ Page</button><button onclick="addText()">+ Text</button><button onclick="saveNode()">Save selected</button></div><div class="app"><aside class="side"><h3>Pages</h3><div id="pages" class="pages"></div><h3>Layers</h3><div id="layers"></div></aside><main class="stagewrap"><div id="stage"></div></main><aside class="side right"><h3>Page</h3><input id="pname" onchange="renamePage(this.value)"><h3>Inspector</h3><div id="inspector" class="small">Select a layer.</div><h3>Document</h3><pre id="meta" class="small"></pre></aside></div><script>let w,active='cover',selected=null;const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));async function api(body){let r=await fetch('/api/workspace',body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});let j=await r.json();if(!r.ok)throw Error(j.error);return j}async function load(){w=await api();if(!w.pages.some(p=>p.id===active))active=w.pages[0].id;render()}function page(){return w.pages.find(p=>p.id===active)}function render(){let p=page();pages.innerHTML=w.pages.map(x=>`<div class="pitem ${x.id===active?'on':''}" onclick="active='${x.id}';selected=null;render()"><div class="thumb"></div><b>${esc(x.name)}</b><div class="small">${x.nodes.length} layers</div></div>`).join('');layers.innerHTML=p.nodes.map(n=>`<div class="layer" onclick="selected='${n.id}';render()">${esc(n.id)} · ${esc(n.type)}</div>`).join('');pname.value=p.name;let s=document.createElement('div');s.className='stage';s.style.width=p.canvas.w+'px';s.style.height=p.canvas.h+'px';for(const n of p.nodes){let e=document.createElement('div');e.className='node '+n.type+(n.id===selected?' sel':'');e.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}`;if(n.type==='rule')e.innerHTML='';else if(n.type==='block')e.innerHTML=`<div>${esc(n.eyebrow||'')}</div><h2>${esc(n.title||'').replaceAll('\\n','<br>')}</h2><p>${esc(n.body||'')}</p>`;else e.innerHTML=esc(n.text||'').replaceAll('\\n','<br>');e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)}stage.innerHTML='';stage.appendChild(s);let n=p.nodes.find(x=>x.id===selected);inspector.innerHTML=n?`<b>${esc(n.id)}</b><input id="ix" value="${n.x}"><input id="iy" value="${n.y}"><input id="iw" value="${n.w}"><input id="isize" value="${n.size||18}"><textarea id="itext">${esc(n.text||n.title||'')}</textarea>`:'Select a layer.';meta.textContent=`${w.schema}\nr${w.revision}\n${w.pages.length} pages`;status.textContent=`${w.name} · r${w.revision} · ${w.pages.length} pages`}async function addPage(){w=await api({op:'add_page'});active=w.pages.at(-1).id;render()}async function renamePage(name){w=await api({op:'rename_page',page_id:active,name});render()}async function addText(){w=await api({op:'add_text',page_id:active,text:'New editorial text'});selected=page().nodes.at(-1)?.id;render()}async function saveNode(){if(!selected)return;let patch={x:+ix.value,y:+iy.value,w:+iw.value,size:+isize.value,text:itext.value};w=await api({op:'set_node',page_id:active,id:selected,patch});render()}load()</script></body></html>'''
class H(BaseHTTPRequestHandler):
 def out(self,status,body,ctype='application/json'):
  raw=body.encode() if isinstance(body,str) else json.dumps(body,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type',ctype+'; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  p=urlparse(self.path).path
  if p=='/': return self.out(200,HTML,'text/html')
  if p=='/api/health': return self.out(200,{'ok':True,'service':'dore-design','version':'0.6','workspace':'multi-page'})
  if p=='/api/workspace': return self.out(200,workspace())
  return self.out(404,{'ok':False,'error':'not_found'})
 def do_POST(self):
  try:
   n=int(self.headers.get('Content-Length','0'));payload=json.loads(self.rfile.read(n) or b'{}')
   if urlparse(self.path).path!='/api/workspace': return self.out(404,{'ok':False,'error':'not_found'})
   return self.out(200,mutate(workspace(),payload))
  except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
 def log_message(self,*a): pass
if __name__=='__main__':
 port=int(os.environ.get('DORE_DESIGN_PORT','4310'));ThreadingHTTPServer(('127.0.0.1',port),H).serve_forever()
