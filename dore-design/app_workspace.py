#!/usr/bin/env python3
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from html import escape
import json,os,datetime,re,copy,hashlib
import app as core
DATA=core.DATA;WS=DATA/'westside-watch.workspace.json';HIST=DATA/'workspace-history';HIST.mkdir(exist_ok=True);EXPORTS=DATA/'exports';EXPORTS.mkdir(exist_ok=True);ASSETS=DATA/'assets';ASSETS.mkdir(exist_ok=True)
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def atomic_obj(p,obj):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(obj,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def atomic_text(p,text):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(text,encoding='utf-8');t.replace(p)
def page(w,pid):return next((x for x in w.get('pages',[]) if x.get('id')==pid),None)
def unique(base,used):
 v=base;i=1
 while v in used:i+=1;v=f'{base}-{i}'
 return v
def obsolete_node(n):
 text=' '.join(str(n.get(k,'')) for k in ('text','title','eyebrow','body')).strip()
 return n.get('id')=='section-10' or bool(re.fullmatch(r'(?:\d+\s*[·.-]\s*)?(?:安提阿|antioch)',text,re.I))
def clean_obsolete(w):
 changed=False
 for p in w.get('pages',[]):
  old=len(p.get('nodes',[]));p['nodes']=[n for n in p.get('nodes',[]) if not obsolete_node(n)];changed|=old!=len(p['nodes'])
 return changed
def default_workspace():
 d=core.default_doc();d['canvas']={'w':1200,'h':930};d['nodes']=[n for n in d['nodes'] if not obsolete_node(n)]
 return {'schema':'dore.design.workspace.v1','id':'westside-watch','name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'tokens':d['tokens'],'assets':{},'pages':[{'id':'cover','name':'Cover','canvas':d['canvas'],'nodes':d['nodes']},{'id':'contents','name':'Contents / Editorial Wall','canvas':{'w':1200,'h':930},'nodes':[{'id':'contents-title','type':'text','role':'hero','text':'CONTENTS','x':72,'y':72,'w':600,'size':74},{'id':'contents-rule','type':'rule','x':72,'y':172,'w':1056,'h':1},{'id':'contents-note','type':'text','text':'Editorial wall · information as brick, weight as battlement, time as flow','x':72,'y':220,'w':900,'size':22}]},{'id':'feature-story','name':'Feature / Story','canvas':{'w':1200,'h':930},'nodes':[{'id':'story-kicker','type':'text','text':'FEATURE','x':72,'y':72,'w':300,'size':18},{'id':'story-title','type':'text','role':'hero','text':'WATCH FOR\nTHE DAWN','x':72,'y':140,'w':760,'size':78},{'id':'story-rule','type':'rule','x':72,'y':350,'w':1056,'h':1},{'id':'story-body','type':'text','text':'A structured story page ready for real editorial content.','x':72,'y':410,'w':760,'size':24}]}]}
def validate(w):
 e=[]
 if w.get('schema')!='dore.design.workspace.v1':e.append('schema')
 pages=w.get('pages');
 if not isinstance(pages,list) or not pages:e.append('pages');return e
 pids=[]
 for p in pages:
  pid=p.get('id');pids.append(pid)
  if not core.valid_id(pid):e.append(f'page_id:{pid}')
  c=p.get('canvas') or {}
  if not isinstance(c.get('w'),(int,float)) or not isinstance(c.get('h'),(int,float)) or c.get('w',0)<=0 or c.get('h',0)<=0:e.append(f'canvas:{pid}')
  ids=[]
  for n in p.get('nodes',[]):
   nid=n.get('id');ids.append(nid)
   if not core.valid_id(nid):e.append(f'node_id:{pid}:{nid}')
   if n.get('type') not in {'text','rule','block','image'}:e.append(f'node_type:{pid}:{nid}')
   if n.get('type')=='image' and (not n.get('asset_id') or n.get('asset_id') not in w.get('assets',{})):e.append(f'image_asset:{pid}:{nid}')
   for k in ('x','y','w'):
    if not isinstance(n.get(k),(int,float)):e.append(f'{pid}:{nid}:{k}')
  if len(ids)!=len(set(ids)):e.append(f'duplicate_nodes:{pid}')
 if len(pids)!=len(set(pids)):e.append('duplicate_pages')
 return e
def snapshot(w):
 p=HIST/f"westside-watch.r{int(w.get('revision',0)):05d}.json"
 if not p.exists():atomic_obj(p,w)
def save(w,snapshot_before=True):
 errs=validate(w)
 if errs:raise ValueError('invalid_workspace:'+','.join(errs))
 if snapshot_before and WS.exists():snapshot(json.loads(WS.read_text(encoding='utf-8')))
 w['revision']=int(w.get('revision',0))+1;w['updated_at']=now();atomic_obj(WS,w);return w
def workspace():
 if not WS.exists():atomic_obj(WS,default_workspace())
 w=json.loads(WS.read_text(encoding='utf-8'))
 if clean_obsolete(w):save(w)
 errs=validate(w)
 if errs:raise ValueError('invalid_workspace:'+','.join(errs))
 return w
def history():
 rows=[]
 for p in sorted(HIST.glob('westside-watch.r*.json')):
  try:d=json.loads(p.read_text(encoding='utf-8'));rows.append({'revision':d.get('revision'),'updated_at':d.get('updated_at'),'path':p.name})
  except Exception:pass
 w=workspace();rows.append({'revision':w['revision'],'updated_at':w.get('updated_at'),'current':True});return rows
def undo():
 rows=[r for r in history() if not r.get('current')]
 if not rows:raise ValueError('no_history')
 src=HIST/rows[-1]['path'];target=json.loads(src.read_text(encoding='utf-8'));cur=workspace();snapshot(cur);target['revision']=cur['revision']+1;target['updated_at']=now();atomic_obj(WS,target);return target
def mutate(w,p):
 op=p.get('op');pid=p.get('page_id');pg=page(w,pid) if pid else None
 if op=='add_page':
  pid=unique(p.get('id') or 'page',{x['id'] for x in w['pages']});w['pages'].append({'id':pid,'name':p.get('name') or 'Untitled Page','canvas':{'w':1200,'h':930},'nodes':[]})
 elif op=='duplicate_page':
  if not pg:raise ValueError('page_not_found')
  q=copy.deepcopy(pg);q['id']=unique(pg['id']+'-copy',{x['id'] for x in w['pages']});q['name']=pg['name']+' Copy';w['pages'].append(q)
 elif op=='delete_page':
  if not pg:raise ValueError('page_not_found')
  if len(w['pages'])<=1:raise ValueError('cannot_delete_last_page')
  w['pages']=[x for x in w['pages'] if x['id']!=pid]
 elif op=='rename_page':
  if not pg:raise ValueError('page_not_found')
  pg['name']=str(p.get('name') or pg['name'])[:80]
 elif op=='set_canvas':
  if not pg:raise ValueError('page_not_found')
  patch=p.get('patch') or {}
  for k in ('w','h'):
   if k in patch:
    v=patch[k]
    if not isinstance(v,(int,float)) or v<=0:raise ValueError('invalid_canvas')
    pg['canvas'][k]=v
 elif op=='token':
  k=p.get('key');v=p.get('value')
  if k not in w.get('tokens',{}) or not isinstance(v,str):raise ValueError('invalid_token')
  w['tokens'][k]=v
 elif op=='add_text':
  if not pg:raise ValueError('page_not_found')
  nid=unique(p.get('id') or 'text',{x['id'] for x in pg['nodes']});pg['nodes'].append({'id':nid,'type':'text','text':p.get('text') or 'New text','x':80,'y':100+len(pg['nodes'])*28,'w':700,'size':34})
 elif op=='add_rule':
  if not pg:raise ValueError('page_not_found')
  nid=unique(p.get('id') or 'rule',{x['id'] for x in pg['nodes']});pg['nodes'].append({'id':nid,'type':'rule','x':80,'y':160+len(pg['nodes'])*20,'w':600,'h':1})
 elif op=='place_image':
  if not pg:raise ValueError('page_not_found')
  a=copy.deepcopy(p.get('asset') or {});n=copy.deepcopy(p.get('shape') or {})
  aid=a.get('id');nid=n.get('id')
  if not aid or a.get('kind')!='image' or not isinstance(a.get('uri'),str):raise ValueError('invalid_image_asset')
  if not nid or n.get('type')!='image' or n.get('asset_id')!=aid:raise ValueError('invalid_image_shape')
  for k in ('x','y','w','h'):
   if not isinstance(n.get(k),(int,float)):raise ValueError('invalid_image_geometry')
  if n['w']<=0 or n['h']<=0 or n.get('fit','cover') not in {'cover','contain','fill'}:raise ValueError('invalid_image_geometry')
  w.setdefault('assets',{})[aid]=a
  old=next((x for x in pg['nodes'] if x.get('id')==nid),None)
  if old:old.update(n)
  else:pg['nodes'].append(n)
 elif op=='set_node':
  if not pg:raise ValueError('page_not_found')
  n=next((x for x in pg['nodes'] if x['id']==p.get('id')),None)
  if not n:raise ValueError('node_not_found')
  patch=copy.deepcopy(p.get('patch') or {});patch.pop('id',None);n.update(patch)
 elif op=='delete_node':
  if not pg:raise ValueError('page_not_found')
  before=len(pg['nodes']);pg['nodes']=[x for x in pg['nodes'] if x['id']!=p.get('id')]
  if len(pg['nodes'])==before:raise ValueError('node_not_found')
 elif op=='duplicate_node':
  if not pg:raise ValueError('page_not_found')
  n=next((x for x in pg['nodes'] if x['id']==p.get('id')),None)
  if not n:raise ValueError('node_not_found')
  q=copy.deepcopy(n);q['id']=unique(n['id']+'-copy',{x['id'] for x in pg['nodes']});q['x']=q.get('x',0)+24;q['y']=q.get('y',0)+24;pg['nodes'].append(q)
 elif op=='undo':return undo()
 else:raise ValueError('unsupported_op')
 clean_obsolete(w);return save(w)
def page_svg(w,pid):
 p=page(w,pid)
 if not p:raise ValueError('page_not_found')
 t=w['tokens'];cw=p['canvas']['w'];ch=p['canvas']['h'];out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}"><rect width="100%" height="100%" fill="{escape(t["paper"])}"/>']
 for n in p['nodes']:
  if n['type']=='image':
   a=w.get('assets',{}).get(n.get('asset_id'),{});href=escape(str(a.get('uri','')),quote=True);fit=n.get('fit','cover');par='none' if fit=='fill' else ('xMidYMid meet' if fit=='contain' else 'xMidYMid slice');rot=float(n.get('rotation',0) or 0);cx=n['x']+n['w']/2;cy=n['y']+n.get('h',0)/2;tr=f' rotate({rot} {cx} {cy})' if rot else '';out.append(f'<image x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n.get("h",0)}" href="{href}" preserveAspectRatio="{par}" transform="{tr.strip()}"/>');continue
  if n['type']=='rule':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n.get("h",1)}" fill="{escape(t["gold"])}"/>');continue
  texts=[(n.get('text',''),n.get('size',18),t['night'] if n.get('role')=='hero' else t['ink'],0)] if n['type']=='text' else [(n.get('eyebrow',''),13,t['gold'],20),(n.get('title',''),52,t['ink'],80),(n.get('body',''),18,t['ink'],250)]
  if n['type']=='block':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="8" fill="{escape(t["gold"])}"/>')
  for text,size,color,dy in texts:
   for j,line in enumerate(str(text).split('\n')):out.append(f'<text x="{n["x"]}" y="{n["y"]+dy+(j+1)*size}" font-family="Georgia,serif" font-size="{size}" fill="{escape(color)}">{escape(line)}</text>')
 out.append('</svg>');return ''.join(out)
def verify(w=None):
 w=w or workspace();errs=validate(w);hashes={};render=True
 for p in w.get('pages',[]):
  s=page_svg(w,p['id']);hashes[p['id']]=hashlib.sha256(s.encode()).hexdigest();render=render and len(s)>100
 checks={'schema_valid':not errs,'multi_page':len(w.get('pages',[]))>=2,'unique_page_ids':len({p['id'] for p in w['pages']})==len(w['pages']),'node_structure_valid':not any('node_' in e or 'duplicate_nodes' in e for e in errs),'render_all_pages':render,'history_available':len(history())>=1,'obsolete_structure_removed':not any(obsolete_node(n) for p in w['pages'] for n in p.get('nodes',[]))}
 return {'ok':all(checks.values()),'document_id':w['id'],'revision':w['revision'],'page_count':len(w['pages']),'node_count':sum(len(p['nodes']) for p in w['pages']),'checks':checks,'errors':errs,'page_render_sha256':hashes}
HTML='''<!doctype html><html><head><meta charset="utf-8"><title>Doré Design</title><style>*{box-sizing:border-box}html,body{margin:0;height:100%;font-family:system-ui;background:#c9c9c7;color:#202020}#top{height:52px;background:#171717;color:#eee;display:flex;align-items:center;gap:8px;padding:0 14px;position:relative;z-index:2}button,a.btn{border:1px solid #777;background:#fff;color:#222;padding:7px 9px;cursor:pointer;text-decoration:none;font-size:12px}#top button,#top a.btn{background:#303030;color:#fff;border-color:#555}.app{height:calc(100% - 52px);display:grid;grid-template-columns:270px 1fr 300px}.side{background:#f2f1ed;overflow:auto;padding:14px;border-right:1px solid #aaa}.right{border-right:0;border-left:1px solid #aaa}.pages{display:grid;gap:7px}.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer}.pitem.on{border:2px solid #252525}.stagewrap{overflow:auto;padding:34px}.stage{position:relative;margin:auto;background:var(--paper);box-shadow:0 10px 35px #0003;overflow:hidden}.node{position:absolute;font-family:Georgia,serif;white-space:pre-line;line-height:1.05}.node.sel{outline:2px solid #777;outline-offset:3px}.rule{background:var(--gold)}.block{border-top:8px solid var(--gold);padding-top:20px}.image{overflow:hidden}.image img{width:100%;height:100%;display:block}.block h2{font:52px/1.05 Georgia,serif;white-space:pre-line}.small{font-size:11px;color:#666}h3{font-size:11px;letter-spacing:.14em;text-transform:uppercase}.layer{padding:7px 4px;border-bottom:1px solid #ddd;cursor:pointer}.layer.on{font-weight:700;background:#e3e0d7}input,textarea{width:100%;margin:4px 0;padding:6px}textarea{height:110px}.danger{border-color:#9b4b4b}.actions{display:flex;gap:6px;flex-wrap:wrap;margin:8px 0}.token{display:grid;grid-template-columns:1fr 80px;gap:6px;margin:5px 0}</style></head><body><div id="top"><b>DORÉ DESIGN 0.8</b><span id="status">workspace</span><button onclick="undo()">Undo</button><button onclick="addPage()">+ Page</button><button onclick="addText()">+ Text</button><button onclick="addRule()">+ Rule</button><button onclick="duplicateNode()">Duplicate Layer</button><button class="danger" onclick="deleteNode()">Delete Layer</button><button onclick="verifyNow()">Verify</button><a id="exportLink" class="btn" target="_blank">SVG Export</a></div><div class="app"><aside class="side"><h3>Pages</h3><div id="pages" class="pages"></div><div class="actions"><button onclick="duplicatePage()">Duplicate Page</button><button class="danger" onclick="deletePage()">Delete Page</button></div><h3>Layers</h3><div id="layers"></div><h3>Tokens</h3><div id="tokens"></div></aside><main class="stagewrap"><div id="stage"></div></main><aside class="side right"><h3>Page</h3><input id="pname" onchange="renamePage(this.value)"><div class="actions"><input id="cw" style="width:90px"><input id="ch" style="width:90px"><button onclick="saveCanvas()">Canvas</button></div><h3>Inspector</h3><div id="inspector" class="small">Select a layer.</div><h3>Verification</h3><pre id="verification" class="small"></pre><h3>Document</h3><pre id="meta" class="small"></pre></aside></div><script>let w,active='cover',selected=null;const esc=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));async function api(path='/api/workspace',body){let r=await fetch(path,body?{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify(body)}:{});let j=await r.json();if(!r.ok)throw Error(j.error);return j}async function load(){w=await api();if(!w.pages.some(p=>p.id===active))active=w.pages[0].id;render()}function pg(){return w.pages.find(p=>p.id===active)}function render(){let p=pg();pages.innerHTML=w.pages.map(x=>`<div class="pitem ${x.id===active?'on':''}" onclick="active='${x.id}';selected=null;render()"><b>${esc(x.name)}</b><div class="small">${x.nodes.length} layers · ${esc(x.id)}</div></div>`).join('');layers.innerHTML=p.nodes.map(n=>`<div class="layer ${n.id===selected?'on':''}" onclick="selected='${n.id}';render()">${esc(n.id)} · ${esc(n.type)}</div>`).join('');tokens.innerHTML=Object.entries(w.tokens).map(([k,v])=>`<div class="token"><span>${esc(k)}</span><input value="${esc(v)}" onchange="setToken('${k}',this.value)"></div>`).join('');pname.value=p.name;cw.value=p.canvas.w;ch.value=p.canvas.h;exportLink.href='/api/export.svg?page='+encodeURIComponent(active);let s=document.createElement('div');s.className='stage';s.style.width=p.canvas.w+'px';s.style.height=p.canvas.h+'px';Object.entries(w.tokens).forEach(([k,v])=>s.style.setProperty('--'+k,v));for(const n of p.nodes){let e=document.createElement('div');e.className='node '+n.type+(n.id===selected?' sel':'');e.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}${n.role==='hero'?'color:var(--night);':''}`;if(n.type==='image'){let a=w.assets?.[n.asset_id];let im=document.createElement('img');im.src=a?.uri||'';im.alt=n.role||'Design image';im.style.objectFit=n.fit||'cover';im.draggable=false;e.appendChild(im)}else if(n.type==='rule')e.innerHTML='';else if(n.type==='block')e.innerHTML=`<div>${esc(n.eyebrow||'')}</div><h2>${esc(n.title||'').replaceAll('\\n','<br>')}</h2><p>${esc(n.body||'')}</p>`;else e.innerHTML=esc(n.text||'').replaceAll('\\n','<br>');e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)}stage.innerHTML='';stage.appendChild(s);let n=p.nodes.find(x=>x.id===selected);inspector.innerHTML=n?`<b>${esc(n.id)}</b><input id="ix" value="${n.x}"><input id="iy" value="${n.y}"><input id="iw" value="${n.w}"><input id="isize" value="${n.size||18}"><textarea id="itext">${esc(n.text||n.title||'')}</textarea><div class="actions"><button onclick="saveNode()">Save</button><button onclick="duplicateNode()">Duplicate</button><button class="danger" onclick="deleteNode()">Delete</button></div>`:'Select a layer.';meta.textContent=`${w.schema}\nr${w.revision}\n${w.pages.length} pages`;status.textContent=`${w.name} · r${w.revision} · ${w.pages.length} pages`}async function mut(x){w=await api('/api/workspace',x);render()}async function addPage(){await mut({op:'add_page'});active=w.pages.at(-1).id;selected=null;render()}async function renamePage(name){await mut({op:'rename_page',page_id:active,name})}async function addText(){await mut({op:'add_text',page_id:active,text:'New editorial text'});selected=pg().nodes.at(-1)?.id;render()}async function addRule(){await mut({op:'add_rule',page_id:active});selected=pg().nodes.at(-1)?.id;render()}async function saveNode(){if(!selected)return;let n=pg().nodes.find(x=>x.id===selected),patch={x:+ix.value,y:+iy.value,w:+iw.value,size:+isize.value};if(n.type==='block')patch.title=itext.value;else if(n.type!=='image')patch.text=itext.value;await mut({op:'set_node',page_id:active,id:selected,patch})}async function deleteNode(){if(!selected)return;await mut({op:'delete_node',page_id:active,id:selected});selected=null;render()}async function duplicateNode(){if(!selected)return;await mut({op:'duplicate_node',page_id:active,id:selected});selected=pg().nodes.at(-1)?.id;render()}async function deletePage(){if(w.pages.length<=1)return;await mut({op:'delete_page',page_id:active});active=w.pages[0].id;selected=null;render()}async function duplicatePage(){await mut({op:'duplicate_page',page_id:active});active=w.pages.at(-1).id;selected=null;render()}async function setToken(key,value){await mut({op:'token',key,value})}async function saveCanvas(){await mut({op:'set_canvas',page_id:active,patch:{w:+cw.value,h:+ch.value}})}async function undo(){w=await api('/api/workspace',{op:'undo'});if(!w.pages.some(p=>p.id===active))active=w.pages[0].id;selected=null;render()}async function verifyNow(){verification.textContent=JSON.stringify(await api('/api/verify'),null,2)}document.addEventListener('keydown',e=>{if((e.key==='Delete'||e.key==='Backspace')&&selected&&!['INPUT','TEXTAREA'].includes(document.activeElement.tagName)){e.preventDefault();deleteNode()}if((e.metaKey||e.ctrlKey)&&e.key.toLowerCase()==='z'){e.preventDefault();undo()}});load()</script></body></html>'''
class H(BaseHTTPRequestHandler):
 def out(self,status,body,ctype='application/json'):
  raw=body.encode() if isinstance(body,str) else json.dumps(body,ensure_ascii=False).encode();self.send_response(status);self.send_header('Content-Type',ctype+'; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  u=urlparse(self.path);p=u.path
  try:
   if p=='/':return self.out(200,HTML,'text/html')
   if p=='/api/health':return self.out(200,{'ok':True,'service':'dore-design','version':'0.8','workspace':'multi-page'})
   if p=='/api/workspace':return self.out(200,workspace())
   if p=='/api/assets':return self.out(200,workspace().get('assets',{}))
   if p=='/api/history':return self.out(200,history())
   if p=='/api/verify':return self.out(200,verify())
   if p=='/api/export.svg':
    pid=(parse_qs(u.query).get('page') or ['cover'])[0];return self.out(200,page_svg(workspace(),pid),'image/svg+xml')
   return self.out(404,{'ok':False,'error':'not_found'})
  except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
 def do_POST(self):
  try:
   if urlparse(self.path).path!='/api/workspace':return self.out(404,{'ok':False,'error':'not_found'})
   n=int(self.headers.get('Content-Length','0'));payload=json.loads(self.rfile.read(n) or b'{}');return self.out(200,mutate(workspace(),payload))
  except Exception as e:return self.out(400,{'ok':False,'error':type(e).__name__+': '+str(e)})
 def log_message(self,*a):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
