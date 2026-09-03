#!/usr/bin/env python3
"""Doré Design product entrypoint: accepted workspace engine plus direct canvas manipulation."""
import os
from http.server import ThreadingHTTPServer
import app_workspace as base
html=base.HTML
required=["DORÉ DESIGN 0.8","let w,active='cover',selected=null;","e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)"]
for marker in required:
 if marker not in html: raise RuntimeError('ui_contract_marker_missing:'+marker[:40])
html=html.replace('DORÉ DESIGN 0.8','DORÉ DESIGN 0.9')
html=html.replace('.node{position:absolute;font-family:Georgia,serif;white-space:pre-line;line-height:1.05}', '.node{position:absolute;font-family:Georgia,serif;white-space:pre-line;line-height:1.05;cursor:move;touch-action:none}')
html=html.replace('.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer}', '.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer;opacity:1!important;pointer-events:auto!important;user-select:none}.pitem:hover{border-color:#555;background:#fafafa}')
html=html.replace("let w,active='cover',selected=null;", "let w,active='cover',selected=null,drag=null;")
html=html.replace("e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)", "e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};e.onpointerdown=ev=>startDrag(ev,e,n);s.appendChild(e)")
inject="""function startDrag(ev,e,n){if(ev.button!==0)return;ev.preventDefault();ev.stopPropagation();selected=n.id;drag={el:e,id:n.id,sx:ev.clientX,sy:ev.clientY,x:n.x,y:n.y,nx:n.x,ny:n.y};e.setPointerCapture?.(ev.pointerId);renderInspectorOnly(n)}function renderInspectorOnly(n){let x=document.getElementById('ix'),y=document.getElementById('iy');if(x)x.value=n.x;if(y)y.value=n.y}window.addEventListener('pointermove',ev=>{if(!drag)return;drag.nx=Math.round(drag.x+ev.clientX-drag.sx);drag.ny=Math.round(drag.y+ev.clientY-drag.sy);drag.el.style.left=drag.nx+'px';drag.el.style.top=drag.ny+'px'});window.addEventListener('pointerup',async ev=>{if(!drag)return;let d=drag;drag=null;w=await api('/api/workspace',{op:'set_node',page_id:active,id:d.id,patch:{x:d.nx,y:d.ny}});selected=d.id;render()});document.addEventListener('click',ev=>{let item=ev.target.closest?.('.pitem');if(!item)return;let label=item.querySelector('.small')?.textContent||'';let id=(label.split('·').pop()||'').trim();if(!id||!w?.pages?.some(p=>p.id===id))return;active=id;selected=null;render()},true);"""
html=html.replace("async function mut(x){w=await api('/api/workspace',x);render()}",inject+"async function mut(x){w=await api('/api/workspace',x);render()}")
base.HTML=html
class H(base.H):
 def do_GET(self):
  if self.path.split('?',1)[0]=='/api/health':return self.out(200,{'ok':True,'service':'dore-design','version':'0.9','workspace':'multi-page','direct_manipulation':True,'page_activation_fix':True})
  return super().do_GET()
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
