#!/usr/bin/env python3
"""Doré Design product entrypoint: editable workspace + live HTML preview/export."""
import os
from html import escape
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse, parse_qs
import app_workspace as base
import multiwrite_integration as multiwrite

# Extend the established DORÉ DESIGN workspace in place. Multiwrite is a page
# family inside this product, never a parallel editor.
multiwrite.install_workspace(base)


def page_html(w, pid):
    p = next((x for x in w.get('pages', []) if x.get('id') == pid), None)
    if not p:
        raise ValueError('page_not_found')
    t = w.get('tokens', {})
    cw = float((p.get('canvas') or {}).get('w') or 1440)
    ch = float((p.get('canvas') or {}).get('h') or 1000)
    def style(n):
        parts = [
            'position:absolute', f'left:{float(n.get("x",0))}px', f'top:{float(n.get("y",0))}px',
            f'width:{float(n.get("w",0))}px', 'white-space:pre-line', 'box-sizing:border-box'
        ]
        if n.get('h') is not None: parts.append(f'height:{float(n.get("h",0))}px')
        if n.get('size') is not None: parts.append(f'font-size:{float(n.get("size",18))}px')
        if n.get('role') == 'hero': parts.append('color:var(--night)')
        return ';'.join(parts)
    nodes=[]
    for n in p.get('nodes', []):
        typ=n.get('type')
        if typ=='rule':
            nodes.append(f'<div class="node rule" style="{style(n)}"></div>')
        elif typ=='block':
            nodes.append('<section class="node block" style="%s"><div class="eyebrow">%s</div><h2>%s</h2><p>%s</p></section>' % (
                style(n), escape(str(n.get('eyebrow',''))), escape(str(n.get('title',''))).replace('\n','<br>'), escape(str(n.get('body','')))
            ))
        else:
            nodes.append(f'<div class="node text" style="{style(n)}">{escape(str(n.get("text",""))).replace(chr(10),"<br>")}</div>')
    vars_css=';'.join(f'--{k}:{v}' for k,v in t.items())
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>{escape(p.get('name','Doré Preview'))}</title><style>
html,body{{margin:0;background:#111;color:var(--ink);font-family:Georgia,"Times New Roman",serif}}body{{min-height:100vh;display:grid;place-items:start center;padding:24px;box-sizing:border-box}}.viewport{{width:min({cw}px,100%);overflow:auto}}.canvas{{position:relative;width:{cw}px;height:{ch}px;background:var(--paper);transform-origin:top left;box-shadow:0 20px 60px #0006}}.node{{line-height:1.05}}.rule{{background:var(--gold)}}.block{{border-top:8px solid var(--gold);padding-top:20px}}.block h2{{font:52px/1.05 Georgia,serif;margin:16px 0}}.block p{{font-size:18px;line-height:1.45}}.eyebrow{{font-size:13px;color:var(--gold);letter-spacing:.12em}}@media(max-width:{int(cw)}px){{.canvas{{transform:scale(calc((100vw - 32px)/{cw}));margin-bottom:calc(({ch}px * ((100vw - 32px)/{cw})) - {ch}px)}}body{{padding:16px}}}}@media(prefers-reduced-motion:reduce){{*{{animation:none!important;transition:none!important}}}}
</style></head><body style="{vars_css}"><main class="viewport"><div class="canvas">{''.join(nodes)}</div></main></body></html>'''

html=base.HTML
required=["DORÉ DESIGN 0.8","let w,active='cover',selected=null;","e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)"]
for marker in required:
    if marker not in html: raise RuntimeError('ui_contract_marker_missing:'+marker[:40])
html=html.replace('DORÉ DESIGN 0.8','DORÉ DESIGN 1.0')
html=html.replace('.node{position:absolute;font-family:Georgia,serif;white-space:pre-line;line-height:1.05}', '.node{position:absolute;font-family:Georgia,serif;white-space:pre-line;line-height:1.05;cursor:move;touch-action:none}')
html=html.replace('.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer}', '.pitem{border:1px solid #bbb;background:#fff;padding:9px;cursor:pointer;opacity:1!important;pointer-events:auto!important;user-select:none}.pitem:hover{border-color:#555;background:#fafafa}.pitem.on{background:#fff;color:#111}')
html=html.replace("let w,active='cover',selected=null;", "let w,active='cover',selected=null,drag=null;")
html=html.replace("pages.innerHTML=w.pages.map(x=>`<div class=\"pitem ${x.id===active?'on':''}\" onclick=\"active='${x.id}';selected=null;render()\"><b>${esc(x.name)}</b><div class=\"small\">${x.nodes.length} layers · ${esc(x.id)}</div></div>`).join('');", "pages.innerHTML=w.pages.map(x=>`<div class=\"pitem ${x.id===active?'on':''}\" data-page-id=\"${esc(x.id)}\"><b>${esc(x.name)}</b><div class=\"small\">${x.nodes.length} layers · ${esc(x.id)}</div></div>`).join('');")
html=html.replace("e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};s.appendChild(e)", "e.onclick=ev=>{ev.stopPropagation();selected=n.id;render()};e.onpointerdown=ev=>startDrag(ev,e,n);s.appendChild(e)")
html=html.replace('<a id="exportLink" class="btn" target="_blank">SVG Export</a>', '<a id="previewLink" class="btn" target="_blank">HTML Preview</a><a id="exportHtmlLink" class="btn" target="_blank">HTML Export</a><a id="exportLink" class="btn" target="_blank">SVG Export</a>')
html=html.replace("exportLink.href='/api/export.svg?page='+encodeURIComponent(active);", "previewLink.href='/preview/'+encodeURIComponent(active);exportHtmlLink.href='/api/export.html?page='+encodeURIComponent(active);exportLink.href='/api/export.svg?page='+encodeURIComponent(active);")
inject="""function activatePage(id){if(!id||!w?.pages?.some(p=>p.id===id))return;active=id;selected=null;render()}pages.addEventListener('click',ev=>{let item=ev.target.closest('.pitem');if(item)activatePage(item.dataset.pageId)});pages.addEventListener('keydown',ev=>{if(ev.key==='Enter'||ev.key===' '){let item=ev.target.closest('.pitem');if(item){ev.preventDefault();activatePage(item.dataset.pageId)}}});function startDrag(ev,e,n){if(ev.button!==0)return;ev.preventDefault();ev.stopPropagation();selected=n.id;drag={el:e,id:n.id,sx:ev.clientX,sy:ev.clientY,x:n.x,y:n.y,nx:n.x,ny:n.y};e.setPointerCapture?.(ev.pointerId);renderInspectorOnly(n)}function renderInspectorOnly(n){let x=document.getElementById('ix'),y=document.getElementById('iy');if(x)x.value=n.x;if(y)y.value=n.y}window.addEventListener('pointermove',ev=>{if(!drag)return;drag.nx=Math.round(drag.x+ev.clientX-drag.sx);drag.ny=Math.round(drag.y+ev.clientY-drag.sy);drag.el.style.left=drag.nx+'px';drag.el.style.top=drag.ny+'px'});window.addEventListener('pointerup',async ev=>{if(!drag)return;let d=drag;drag=null;w=await api('/api/workspace',{op:'set_node',page_id:active,id:d.id,patch:{x:d.nx,y:d.ny}});selected=d.id;render()});"""
html=html.replace("async function mut(x){w=await api('/api/workspace',x);render()}",inject+"async function mut(x){w=await api('/api/workspace',x);render()}")
html=multiwrite.augment_html(html)
base.HTML=html

class H(base.H):
    def do_GET(self):
        u=urlparse(self.path); p=u.path
        if p=='/api/health':
            return self.out(200,{'ok':True,'service':'dore-design','version':'1.0','workspace':'multi-page','direct_manipulation':True,'page_activation_fix':True,'html_preview':True,'html_export':True,'multiwrite_semantic_design':True})
        if p=='/api/export.html':
            pid=(parse_qs(u.query).get('page') or ['cover'])[0]
            return self.out(200,page_html(base.workspace(),pid),'text/html')
        if p.startswith('/preview/'):
            pid=p[len('/preview/'):]
            return self.out(200,page_html(base.workspace(),pid),'text/html')
        return super().do_GET()

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),H).serve_forever()
