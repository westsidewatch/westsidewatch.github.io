#!/usr/bin/env python3
"""First-class Multiwrite surface inside DORÉ DESIGN's existing WYSIWYG editor."""
from html import escape
import app_workspace as base

PAGE_ID='multiwrite-home'
COLORS={'paper':'#F5EEDB','first-light':'#CEBD74','watch-night':'#26241F','olive':'#7A7B57'}
TITLE={'quiet':32,'equal':42,'display':62}
REC={'color':'paper','hierarchy':'quiet','axis':'center','density':'1','lines':'1'}


def _page():
    w=base.workspace()
    p=next((x for x in w.get('pages',[]) if x.get('id')==PAGE_ID),None)
    if not p: raise FileNotFoundError('multiwrite_home_not_mounted')
    return w,p


def _node_style(n,d):
    parts=[f'left:{n.get("x",0)}px',f'top:{n.get("y",0)}px',f'width:{n.get("w",0)}px']
    if n.get('h') is not None: parts.append(f'height:{n.get("h")}px')
    size=n.get('size',18)
    if n.get('id')=='mw-story-title': size=TITLE.get(d.get('hierarchy'),32)
    parts.append(f'font-size:{size}px')
    zone=n.get('semantic_zone')
    if zone in {'story','story-title'}:
        parts.append('text-align:center' if d.get('axis')=='center' else 'text-align:left')
        parts.append({'0':'line-height:1.2','1':'line-height:1.45','2':'line-height:1.75'}.get(d.get('density'),'line-height:1.45'))
    return ';'.join(parts)


def render_canvas(edit=False):
    w,p=_page(); design=p.get('design') or {}; d={**REC,**(design.get('decision') or {})}
    bg=COLORS.get(d['color'],COLORS['paper']);dark=d['color'] in {'watch-night','olive'}
    line={'0':'transparent','1':'rgba(96,73,26,.18)','2':'rgba(96,73,26,.42)'}.get(d['lines'],'rgba(96,73,26,.18)')
    nodes=[]
    for n in p.get('nodes',[]):
        nid=escape(str(n.get('id','')));typ=n.get('type','text');zone=n.get('semantic_zone','')
        cls=f'node {typ} {escape(zone)}'
        style=_node_style(n,d)
        attrs=f'data-id="{nid}" data-field="text"' if edit and typ=='text' else ''
        if typ=='rule':
            body='';style+=';background:#8c6818'
        elif typ=='block':
            # The story background is a semantic surface, not a fake content card.
            body='';style+=f';background:{bg};border-top:1px solid {line};border-bottom:1px solid {line};padding:0'
        else:
            text=escape(str(n.get('text',''))).replace('\n','<br>');body=text
            if zone in {'story','story-title'} and dark: style+=';color:#f0e7c8'
            elif n.get('role')=='hero': style+=';color:#8c6818'
        if nid in {'mw-path-update','mw-path-book'}: style+=f';border-left:1px solid {line};padding-left:24px'
        nodes.append(f'<div class="{cls}" style="{style}" {attrs}>{body}</div>')
    editing='true' if edit else 'false'
    select_js='''<script>document.addEventListener('click',e=>{const n=e.target.closest('[data-id]');if(!n)return;e.preventDefault();parent.postMessage({type:'dore-select',page_id:'multiwrite-home',id:n.dataset.id,field:n.dataset.field,value:n.innerText},'*')});parent.postMessage({type:'dore-ready',page_id:'multiwrite-home',revision:%d},'*');</script>'''%w.get('revision',0) if edit else ''
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>多寫 · DORÉ DESIGN</title><style>
*{{box-sizing:border-box}}html,body{{margin:0;background:#c2c2bf;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",Georgia,serif}}body{{padding:22px}}.frame{{width:min(1200px,100%);margin:auto;overflow:auto}}.canvas{{position:relative;width:1200px;height:2280px;background:#CEBD74;box-shadow:0 12px 42px #0003;transform-origin:top left}}.node{{position:absolute;white-space:normal;line-height:1.35;z-index:2}}.story-bg{{z-index:0}}.hero,.library{{z-index:2}}[data-id]{{cursor:text}}[data-id]:hover{{outline:1px dashed rgba(24,24,24,.45);outline-offset:4px}}@media(max-width:1244px){{.canvas{{transform:scale(calc((100vw - 44px)/1200));margin-bottom:calc(2280px * ((100vw - 44px)/1200) - 2280px)}}}} </style></head><body data-edit="{editing}"><main class="frame"><article class="canvas">{''.join(nodes)}</article></main>{select_js}</body></html>'''


SEMANTIC_CSS='''<style>.mw-semantic{{border:1px solid #c7c1b2;background:#fff;padding:10px;margin:0 0 14px}}.mw-semantic label{{display:block;margin:8px 0 4px;color:#666}}.mw-semantic select{{width:100%;padding:6px;border:1px solid #aaa;background:#fff;font:11px ui-monospace,monospace}}.mw-semantic .row{{display:grid;grid-template-columns:1fr 1fr;gap:6px}}.mw-semantic button{{width:100%;margin-top:7px;padding:7px;border:0;background:#222;color:#fff;cursor:pointer}}.mw-semantic .recommend{{background:#8c6818}}.mw-semantic .why{{font:11px/1.45 Arial,sans-serif;color:#5b5549;margin-top:8px}}</style>'''
SEMANTIC_PANEL='''<div id="mw-semantic" class="mw-semantic" hidden><h3>DORÉ · MULTIWRITE DESIGN</h3><div class="hint">Design by meaning, inside the existing workspace.</div><label>BACKGROUND ROLE</label><select id="mw-color"><option value="paper">Living Paper</option><option value="first-light">First Light</option><option value="watch-night">Watch Night</option><option value="olive">Olive</option></select><div class="row"><div><label>TITLE</label><select id="mw-hierarchy"><option value="quiet">Quiet</option><option value="equal">Equal</option><option value="display">Display</option></select></div><div><label>AXIS</label><select id="mw-axis"><option value="center">Centered · Gate</option><option value="left">Editorial left</option></select></div></div><div class="row"><div><label>DENSITY</label><select id="mw-density"><option value="0">Compact</option><option value="1">Balanced</option><option value="2">Airy</option></select></div><div><label>LINES</label><select id="mw-lines"><option value="0">None</option><option value="1">Quiet</option><option value="2">Strong</option></select></div></div><button class="recommend" id="mw-recommend">DORÉ RECOMMENDS</button><button id="mw-apply">Apply semantic design</button><div id="mw-why" class="why"></div></div>'''
SEMANTIC_JS=r'''<script>(()=>{const ID='multiwrite-home',REC={color:'paper',hierarchy:'quiet',axis:'center',density:'1',lines:'1'},WHY={paper:'紙承載正文；讓首屏的金保有稀缺性。',first-light:'初光適合顯現與入口，不宜讓第二頁維持同等強度。','watch-night':'守望夜對比強，會把第二頁推成新的主角。',olive:'橄欖帶生命、安息與恢復語義。'};const g=id=>document.getElementById(id);function read(){return {color:g('mw-color').value,hierarchy:g('mw-hierarchy').value,axis:g('mw-axis').value,density:g('mw-density').value,lines:g('mw-lines').value}}function sync(){const p=ws?.pages?.find(x=>x.id===active),box=g('mw-semantic');if(!box)return;box.hidden=active!==ID;if(box.hidden)return;const d={...REC,...(p?.design?.decision||{})};g('mw-color').value=d.color;g('mw-hierarchy').value=d.hierarchy;g('mw-axis').value=d.axis;g('mw-density').value=d.density;g('mw-lines').value=d.lines;g('mw-why').textContent=(p?.design?.reasoning?.color||WHY[d.color])+' '+(p?.design?.reasoning?.axis||'')}}async function save(d){const r=await fetch('/api/workspace',{method:'POST',headers:{'Content-Type':'application/json'},body:JSON.stringify({op:'design_decision',page_id:ID,decision:d})});if(!r.ok){g('status').textContent='SEMANTIC DESIGN FAILED';return}ws=await r.json();g('canvas').src=canvasUrl();renderLayers();sync();g('status').textContent='semantic design saved · r'+ws.revision+' · '+active}g('mw-recommend').onclick=()=>save(REC);g('mw-apply').onclick=()=>save(read());const rp=renderPages;renderPages=function(){rp();sync()};const sp=switchPage;switchPage=function(id){sp(id);sync()};const rw=refreshWorkspace;refreshWorkspace=async function(){await rw();sync()};setTimeout(sync,0)})()</script>'''


def augment_editor(html):
    if 'id="inspector"' not in html: raise RuntimeError('multiwrite_editor_inspector_marker_missing')
    html=html.replace('</head>',SEMANTIC_CSS+'</head>',1)
    html=html.replace('<h3>INSPECTOR</h3>',SEMANTIC_PANEL+'<h3>INSPECTOR</h3>',1)
    return html.replace('</body>',SEMANTIC_JS+'</body>',1)
