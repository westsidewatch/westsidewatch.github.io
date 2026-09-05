#!/usr/bin/env python3
from http.server import ThreadingHTTPServer,BaseHTTPRequestHandler
from pathlib import Path
from urllib.parse import urlparse,parse_qs
from html import escape
import copy,datetime,hashlib,json,mimetypes,os,re
import app as core
DATA=core.DATA;WS=DATA/'westside-watch.workspace.json';HIST=DATA/'workspace-history';HIST.mkdir(exist_ok=True);ROOT=Path(__file__).resolve().parents[1]
IMG_EXT={'.png','.jpg','.jpeg','.webp'}
def now():return datetime.datetime.now(datetime.timezone.utc).isoformat()
def atomic(p,o):
 t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(o,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def page(w,pid):return next((x for x in w.get('pages',[]) if x.get('id')==pid),None)
def page_name(w,name):
 k=re.sub(r'\s+','',str(name or '')).casefold();return next((x for x in w.get('pages',[]) if re.sub(r'\s+','',str(x.get('name',''))).casefold()==k),None) if k else None
def target_page(w,p):return page_name(w,p.get('page_name')) or page(w,p.get('page_id'))
def unique(base,used):
 base=re.sub(r'[^A-Za-z0-9._-]+','-',str(base or 'node')).strip('-')[:64] or 'node';v=base;i=1
 while v in used:i+=1;v=f'{base}-{i}'
 return v
def obsolete(n):
 text=' '.join(str(n.get(k,'')) for k in ('text','title','eyebrow','body')).strip();return n.get('id')=='section-10' or bool(re.fullmatch(r'(?:\d+\s*[·.-]\s*)?(?:安提阿|antioch)',text,re.I))
def default_workspace():
 d=core.default_doc();d['canvas']={'w':1200,'h':930};d['nodes']=[n for n in d['nodes'] if not obsolete(n)]
 return {'schema':'dore.design.workspace.v1','id':'westside-watch','name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'tokens':d['tokens'],'pages':[{'id':'cover','name':'Cover','canvas':d['canvas'],'nodes':d['nodes']},{'id':'contents','name':'Contents / Editorial Wall','canvas':{'w':1200,'h':930},'nodes':[{'id':'contents-title','type':'text','role':'hero','text':'CONTENTS','x':72,'y':72,'w':600,'size':74}]},{'id':'feature-story','name':'Feature / Story','canvas':{'w':1200,'h':930},'nodes':[{'id':'story-title','type':'text','role':'hero','text':'WATCH FOR\nTHE DAWN','x':72,'y':140,'w':760,'size':78}]}]}
def valid_uri(uri):
 s=str(uri or '').strip();u=urlparse(s)
 if not s:return False
 if u.scheme in {'http','https'}:
  q=(parse_qs(u.query).get('name') or [''])[0];return u.hostname in {'127.0.0.1','localhost'} and (Path(u.path).suffix.lower() in IMG_EXT or Path(q).suffix.lower() in IMG_EXT)
 return Path(s).suffix.lower() in IMG_EXT
def validate(w):
 e=[]
 if w.get('schema')!='dore.design.workspace.v1':e.append('schema')
 ps=w.get('pages')
 if not isinstance(ps,list) or not ps:return e+['pages']
 pids=[]
 for p in ps:
  pid=p.get('id');pids.append(pid);c=p.get('canvas') or {}
  if not core.valid_id(pid):e.append(f'page_id:{pid}')
  if not all(isinstance(c.get(k),(int,float)) and c.get(k)>0 for k in ('w','h')):e.append(f'canvas:{pid}')
  ids=[]
  for n in p.get('nodes',[]):
   nid=n.get('id');ids.append(nid);typ=n.get('type')
   if not core.valid_id(nid):e.append(f'node_id:{pid}:{nid}')
   if typ not in {'text','rule','block','image'}:e.append(f'node_type:{pid}:{nid}')
   for k in ('x','y','w'):
    if not isinstance(n.get(k),(int,float)):e.append(f'{pid}:{nid}:{k}')
   if typ=='image':
    if not isinstance(n.get('h'),(int,float)) or n.get('h',0)<=0:e.append(f'{pid}:{nid}:h')
    if n.get('fit','cover') not in {'cover','contain','fill'}:e.append(f'{pid}:{nid}:fit')
    if not valid_uri(n.get('uri')):e.append(f'{pid}:{nid}:uri')
    if not re.fullmatch(r'[0-9a-fA-F]{64}',str(n.get('sha256',''))):e.append(f'{pid}:{nid}:sha256')
  if len(ids)!=len(set(ids)):e.append(f'duplicate_nodes:{pid}')
 if len(pids)!=len(set(pids)):e.append('duplicate_pages')
 return e
def snapshot(w):
 p=HIST/f"westside-watch.r{int(w.get('revision',0)):05d}.json"
 if not p.exists():atomic(p,w)
def save(w):
 e=validate(w)
 if e:raise ValueError('invalid_workspace:'+','.join(e))
 if WS.exists():snapshot(json.loads(WS.read_text(encoding='utf-8')))
 w['revision']=int(w.get('revision',0))+1;w['updated_at']=now();atomic(WS,w);return w
def workspace():
 if not WS.exists():atomic(WS,default_workspace())
 w=json.loads(WS.read_text(encoding='utf-8'));changed=False
 for p in w.get('pages',[]):
  old=len(p.get('nodes',[]));p['nodes']=[n for n in p.get('nodes',[]) if not obsolete(n)];changed|=old!=len(p['nodes'])
 if changed:save(w)
 e=validate(w)
 if e:raise ValueError('invalid_workspace:'+','.join(e))
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
 cur=workspace();snapshot(cur);w=json.loads((HIST/rows[-1]['path']).read_text(encoding='utf-8'));w['revision']=cur['revision']+1;w['updated_at']=now();atomic(WS,w);return w
def place_image(w,p):
 pg=target_page(w,p)
 if not pg:raise ValueError('page_not_found')
 a=copy.deepcopy(p.get('asset') or {});s=copy.deepcopy(p.get('shape') or {});pl=s.get('placement') or s;uri=str(a.get('uri') or '');sha=str(a.get('sha256') or '');fit=str(s.get('fit') or 'cover')
 if not valid_uri(uri) or not re.fullmatch(r'[0-9a-fA-F]{64}',sha):raise ValueError('invalid_image_asset')
 if fit not in {'cover','contain','fill'}:raise ValueError('invalid_image_fit')
 if not all(isinstance(pl.get(k),(int,float)) for k in ('x','y','w','h')) or pl['w']<=0 or pl['h']<=0:raise ValueError('invalid_image_placement')
 nid=unique(s.get('id') or 'image-'+sha[:16],{n['id'] for n in pg['nodes']});pg['nodes'].append({'id':nid,'type':'image','x':pl['x'],'y':pl['y'],'w':pl['w'],'h':pl['h'],'uri':uri,'sha256':sha,'fit':fit,'role':s.get('role') or 'editorial-image','asset_id':a.get('id') or sha[:16],'provenance':a.get('provenance') or {}})
def mutate(w,p):
 op=p.get('op');pg=target_page(w,p)
 if op=='add_page':
  pid=unique(p.get('id') or 'page',{x['id'] for x in w['pages']});w['pages'].append({'id':pid,'name':p.get('name') or 'Untitled Page','canvas':{'w':1200,'h':930},'nodes':[]})
 elif op=='duplicate_page':
  if not pg:raise ValueError('page_not_found')
  q=copy.deepcopy(pg);q['id']=unique(pg['id']+'-copy',{x['id'] for x in w['pages']});q['name']=pg['name']+' Copy';w['pages'].append(q)
 elif op=='delete_page':
  if not pg:raise ValueError('page_not_found')
  if len(w['pages'])<=1:raise ValueError('cannot_delete_last_page')
  w['pages']=[x for x in w['pages'] if x['id']!=pg['id']]
 elif op=='rename_page':
  if not pg:raise ValueError('page_not_found')
  pg['name']=str(p.get('name') or pg['name'])[:80]
 elif op=='set_canvas':
  if not pg:raise ValueError('page_not_found')
  for k,v in (p.get('patch') or {}).items():
   if k in {'w','h'}:
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
 elif op=='apply_image_patch':
  q=p.get('patch') or {}
  if q.get('schema')!='dore.design.image-patch.v1':raise ValueError('invalid_image_patch_schema')
  place_image(w,{'page_id':q.get('page_id'),'page_name':q.get('page_name'),'asset':{'id':q.get('asset_id'),'uri':q.get('uri'),'sha256':q.get('sha256'),'provenance':q.get('provenance') or {}},'shape':{'id':'image-'+str(q.get('sha256',''))[:16],'placement':q.get('placement') or {},'fit':q.get('fit') or 'cover','role':q.get('role') or 'editorial-image'}})
 elif op=='place_image':place_image(w,p)
 elif op=='set_node':
  if not pg:raise ValueError('page_not_found')
  n=next((x for x in pg['nodes'] if x['id']==p.get('id')),None)
  if not n:raise ValueError('node_not_found')
  q=copy.deepcopy(p.get('patch') or {});q.pop('id',None);q.pop('type',None);n.update(q)
 elif op=='delete_node':
  if not pg:raise ValueError('page_not_found')
  before=len(pg['nodes']);pg['nodes']=[x for x in pg['nodes'] if x['id']!=p.get('id')]
  if before==len(pg['nodes']):raise ValueError('node_not_found')
 elif op=='duplicate_node':
  if not pg:raise ValueError('page_not_found')
  n=next((x for x in pg['nodes'] if x['id']==p.get('id')),None)
  if not n:raise ValueError('node_not_found')
  q=copy.deepcopy(n);q['id']=unique(n['id']+'-copy',{x['id'] for x in pg['nodes']});q['x']+=24;q['y']+=24;pg['nodes'].append(q)
 elif op=='undo':return undo()
 else:raise ValueError('unsupported_op')
 return save(w)
def page_svg(w,pid):
 p=page(w,pid)
 if not p:raise ValueError('page_not_found')
 t=w['tokens'];cw=p['canvas']['w'];ch=p['canvas']['h'];out=[f'<svg xmlns="http://www.w3.org/2000/svg" width="{cw}" height="{ch}" viewBox="0 0 {cw} {ch}"><rect width="100%" height="100%" fill="{escape(t["paper"])}"/>']
 for n in p['nodes']:
  if n['type']=='rule':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n.get("h",1)}" fill="{escape(t["gold"])}"/>');continue
  if n['type']=='image':
   par={'cover':'xMidYMid slice','contain':'xMidYMid meet','fill':'none'}[n.get('fit','cover')];out.append(f'<image x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="{n["h"]}" href="/api/image?page={escape(pid)}&amp;node={escape(n["id"])}" preserveAspectRatio="{par}"/>');continue
  texts=[(n.get('text',''),n.get('size',18),t['night'] if n.get('role')=='hero' else t['ink'],0)] if n['type']=='text' else [(n.get('eyebrow',''),13,t['gold'],20),(n.get('title',''),52,t['ink'],80),(n.get('body',''),18,t['ink'],250)]
  if n['type']=='block':out.append(f'<rect x="{n["x"]}" y="{n["y"]}" width="{n["w"]}" height="8" fill="{escape(t["gold"])}"/>')
  for text,size,color,dy in texts:
   for j,line in enumerate(str(text).split('\n')):out.append(f'<text x="{n["x"]}" y="{n["y"]+dy+(j+1)*size}" font-family="Georgia,serif" font-size="{size}" fill="{escape(color)}">{escape(line)}</text>')
 out.append('</svg>');return ''.join(out)
def verify(w=None):
 w=w or workspace();e=validate(w);hashes={};render=True
 for p in w['pages']:
  s=page_svg(w,p['id']);hashes[p['id']]=hashlib.sha256(s.encode()).hexdigest();render&=len(s)>100
 checks={'schema_valid':not e,'multi_page':len(w['pages'])>=2,'unique_page_ids':len({p['id'] for p in w['pages']})==len(w['pages']),'node_structure_valid':not any('node_' in x or 'duplicate_nodes' in x for x in e),'render_all_pages':render,'history_available':len(history())>=1,'obsolete_structure_removed':not any(obsolete(n) for p in w['pages'] for n in p.get('nodes',[]))}
 return {'ok':all(checks.values()),'document_id':w['id'],'revision':w['revision'],'page_count':len(w['pages']),'node_count':sum(len(p['nodes']) for p in w['pages']),'checks':checks,'errors':e,'page_render_sha256':hashes}
HTML='''<!doctype html><meta charset="utf-8"><title>Doré Design</title><style>*{box-sizing:border-box}body{margin:0;font-family:system-ui;background:#c9c9c7}#top{height:52px;background:#171717;color:#eee;padding:14px}.app{display:grid;grid-template-columns:260px 1fr;height:calc(100vh - 52px)}aside{background:#f2f1ed;padding:14px;overflow:auto}.stagewrap{overflow:auto;padding:34px}.stage{position:relative;margin:auto;background:#faf9f5;box-shadow:0 10px 35px #0003;overflow:hidden}.node{position:absolute;font-family:Georgia,serif;white-space:pre-line}.node img{width:100%;height:100%;display:block}.p{padding:8px;background:white;border:1px solid #bbb;margin:5px 0;cursor:pointer}.on{border:2px solid #222}</style><div id="top"><b>DORÉ DESIGN 0.9</b> · native image workspace · <span id="status"></span></div><div class="app"><aside><b>Pages</b><div id="pages"></div><hr><b>Layers</b><div id="layers"></div></aside><main class="stagewrap"><div id="stage"></div></main></div><script>let w,active='cover';const e=s=>String(s??'').replace(/[&<>"']/g,c=>({'&':'&amp;','<':'&lt;','>':'&gt;','"':'&quot;',"'":'&#39;'}[c]));async function load(){w=await(await fetch('/api/workspace')).json();if(!w.pages.some(p=>p.id===active))active=w.pages[0].id;render()}function render(){let p=w.pages.find(x=>x.id===active);pages.innerHTML=w.pages.map(x=>`<div class="p ${x.id===active?'on':''}" onclick="active='${x.id}';render()"><b>${e(x.name)}</b><br><small>${e(x.id)}</small></div>`).join('');layers.innerHTML=p.nodes.map(n=>`<div>${e(n.id)} · ${e(n.type)}</div>`).join('');let s=document.createElement('div');s.className='stage';s.style.width=p.canvas.w+'px';s.style.height=p.canvas.h+'px';for(const n of p.nodes){let x=document.createElement('div');x.className='node';x.style.cssText=`left:${n.x}px;top:${n.y}px;width:${n.w}px;${n.h?'height:'+n.h+'px;':''}${n.size?'font-size:'+n.size+'px;':''}`;if(n.type==='image')x.innerHTML=`<img src="/api/image?page=${encodeURIComponent(active)}&node=${encodeURIComponent(n.id)}" style="object-fit:${n.fit==='fill'?'fill':n.fit}">`;else if(n.type==='rule')x.style.cssText+='background:#A2872A;height:'+(n.h||1)+'px';else x.textContent=n.text||n.title||'';s.appendChild(x)}stage.innerHTML='';stage.appendChild(s);status.textContent=w.name+' · r'+w.revision}load()</script>'''
def image_node(q):
 w=workspace();pid=(q.get('page') or [''])[0];nid=(q.get('node') or [''])[0];pg=page(w,pid) if pid else None;return next((n for n in (pg or {}).get('nodes',[]) if n.get('id')==nid and n.get('type')=='image'),None)
def read_local(uri):
 p=Path(str(uri)).expanduser().resolve()
 if p.suffix.lower() not in IMG_EXT or not p.is_file():raise FileNotFoundError('image_not_found')
 if ROOT not in p.parents and not (Path.home().resolve() in p.parents and '.dore' in p.parts):raise ValueError('image_path_not_allowed')
 return p,p.read_bytes()
class H(BaseHTTPRequestHandler):
 def out(self,s,b,ct='application/json'):
  raw=b.encode() if isinstance(b,str) else json.dumps(b,ensure_ascii=False).encode();self.send_response(s);self.send_header('Content-Type',ct+'; charset=utf-8');self.send_header('Content-Length',str(len(raw)));self.end_headers();self.wfile.write(raw)
 def do_GET(self):
  u=urlparse(self.path);p=u.path
  try:
   if p=='/':return self.out(200,HTML,'text/html')
   if p=='/api/health':return self.out(200,{'ok':True,'service':'dore-design','version':'0.9','workspace':'multi-page+image'})
   if p=='/api/workspace':return self.out(200,workspace())
   if p=='/api/history':return self.out(200,history())
   if p=='/api/verify':return self.out(200,verify())
   if p=='/api/export.svg':return self.out(200,page_svg(workspace(),(parse_qs(u.query).get('page') or ['cover'])[0]),'image/svg+xml')
   if p=='/api/image':
    n=image_node(parse_qs(u.query))
    if not n:raise FileNotFoundError('image_node_not_found')
    uri=str(n.get('uri'));pr=urlparse(uri)
    if pr.scheme in {'http','https'}:self.send_response(302);self.send_header('Location',uri);self.end_headers();return
    fp,data=read_local(uri);ct=mimetypes.guess_type(fp.name)[0] or 'application/octet-stream';self.send_response(200);self.send_header('Content-Type',ct);self.send_header('Content-Length',str(len(data)));self.end_headers();self.wfile.write(data);return
   return self.out(404,{'ok':False,'error':'not_found'})
  except Exception as ex:return self.out(400,{'ok':False,'error':type(ex).__name__+': '+str(ex)})
 def do_POST(self):
  try:
   if urlparse(self.path).path!='/api/workspace':return self.out(404,{'ok':False,'error':'not_found'})
   n=int(self.headers.get('Content-Length','0'))
   if n<=0 or n>262144:raise ValueError('invalid_request_size')
   return self.out(200,mutate(workspace(),json.loads(self.rfile.read(n) or b'{}')))
  except Exception as ex:return self.out(400,{'ok':False,'error':type(ex).__name__+': '+str(ex)})
 def log_message(self,*a):pass
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
