#!/usr/bin/env python3
from pathlib import Path

p=Path('dore-design/app_workspace.py')
s=p.read_text(encoding='utf-8')

def once(old,new):
 global s
 if new in s:return
 if old not in s:raise SystemExit('anchor not found: '+old[:80])
 s=s.replace(old,new,1)

once("DATA=core.DATA;WS=DATA/'westside-watch.workspace.json';HIST=DATA/'workspace-history';HIST.mkdir(exist_ok=True);EXPORTS=DATA/'exports';EXPORTS.mkdir(exist_ok=True)","DATA=core.DATA;WS=DATA/'westside-watch.workspace.json';HIST=DATA/'workspace-history';HIST.mkdir(exist_ok=True);EXPORTS=DATA/'exports';EXPORTS.mkdir(exist_ok=True);ASSETS=DATA/'assets';ASSETS.mkdir(exist_ok=True)")
once("return {'schema':'dore.design.workspace.v1','id':'westside-watch','name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'tokens':d['tokens'],'pages':", "return {'schema':'dore.design.workspace.v1','id':'westside-watch','name':'Westside Watch — Doré Design','revision':1,'updated_at':now(),'tokens':d['tokens'],'assets':{},'pages':")
once("if n.get('type') not in {'text','rule','block'}:e.append(f'node_type:{pid}:{nid}')", "if n.get('type') not in {'text','rule','block','image'}:e.append(f'node_type:{pid}:{nid}')\n   if n.get('type')=='image' and (not n.get('asset_id') or n.get('asset_id') not in w.get('assets',{})):e.append(f'image_asset:{pid}:{nid}')")
once("elif op=='set_node':", "elif op=='place_image':\n  if not pg:raise ValueError('page_not_found')\n  a=copy.deepcopy(p.get('asset') or {});n=copy.deepcopy(p.get('shape') or {})\n  aid=a.get('id');nid=n.get('id')\n  if not aid or a.get('kind')!='image' or not isinstance(a.get('uri'),str):raise ValueError('invalid_image_asset')\n  if not nid or n.get('type')!='image' or n.get('asset_id')!=aid:raise ValueError('invalid_image_shape')\n  for k in ('x','y','w','h'):\n   if not isinstance(n.get(k),(int,float)):raise ValueError('invalid_image_geometry')\n  if n['w']<=0 or n['h']<=0 or n.get('fit','cover') not in {'cover','contain','fill'}:raise ValueError('invalid_image_geometry')\n  w.setdefault('assets',{})[aid]=a\n  old=next((x for x in pg['nodes'] if x.get('id')==nid),None)\n  if old:old.update(n)\n  else:pg['nodes'].append(n)\n elif op=='set_node':")
once("if n['type']=='rule':out.append", "if n['type']=='image':\n   a=w.get('assets',{}).get(n.get('asset_id'),{});href=escape(str(a.get('uri','')),quote=True);fit=n.get('fit','cover');par='none' if fit=='fill' else ('xMidYMid meet' if fit=='contain' else 'xMidYMid slice');rot=float(n.get('rotation',0) or 0);cx=n['x']+n['w']/2;cy=n['y']+n.get('h',0)/2;tr=f' rotate({rot} {cx} {cy})' if rot else '';out.append(f'<image x=\"{n[\"x\"]}\" y=\"{n[\"y\"]}\" width=\"{n[\"w\"]}\" height=\"{n.get(\"h\",0)}\" href=\"{href}\" preserveAspectRatio=\"{par}\" transform=\"{tr.strip()}\"/>');continue\n  if n['type']=='rule':out.append")
once(".block{border-top:8px solid var(--gold);padding-top:20px}", ".block{border-top:8px solid var(--gold);padding-top:20px}.image{overflow:hidden}.image img{width:100%;height:100%;display:block}")
once("if(n.type==='rule')e.innerHTML='';else if(n.type==='block')", "if(n.type==='image'){let a=w.assets?.[n.asset_id];let im=document.createElement('img');im.src=a?.uri||'';im.alt=n.role||'Design image';im.style.objectFit=n.fit||'cover';im.draggable=false;e.appendChild(im)}else if(n.type==='rule')e.innerHTML='';else if(n.type==='block')")
once("if(n.type==='block')patch.title=itext.value;else patch.text=itext.value", "if(n.type==='block')patch.title=itext.value;else if(n.type!=='image')patch.text=itext.value")
once("if p=='/api/workspace':return self.out(200,workspace())", "if p=='/api/workspace':return self.out(200,workspace())\n   if p=='/api/assets':return self.out(200,workspace().get('assets',{}))")

p.write_text(s,encoding='utf-8')
print('patched',p)
# migration-v1
