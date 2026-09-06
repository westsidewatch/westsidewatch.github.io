#!/usr/bin/env python3
"""Render a generic structured workspace page as an editable Design canvas."""
from html import escape

def render(base,page_id,edit=False):
    w=base.workspace();p=base.page(w,page_id)
    if not p: raise FileNotFoundError('page_not_found')
    c=p.get('canvas') or {'w':1200,'h':1500};cw=c.get('w',1200);ch=c.get('h',1500);parts=[]
    for n in p.get('nodes',[]):
        typ=n.get('type','text');nid=escape(str(n.get('id','')));x=n.get('x',0);y=n.get('y',0);ww=n.get('w',0);hh=n.get('h');style=f'left:{x}px;top:{y}px;width:{ww}px;'
        if hh is not None:style+=f'height:{hh}px;'
        attrs=f'data-id="{nid}" data-field="text" data-type="{escape(str(typ))}"' if edit else ''
        if typ=='rule':body='';style+='background:#8c6818;'
        elif typ=='block':body='';style+=f'border:1px solid {escape(str(n.get("frame_stroke","#8c6818")))};background:{escape(str(n.get("frame_fill","transparent")))};'
        elif typ=='image':
            a=w.get('assets',{}).get(n.get('asset_id'),{});uri=escape(str(a.get('uri','')),quote=True);fit=n.get('fit','cover');pos=f'{n.get("crop_x",50)}% {n.get("crop_y",50)}%';body=f'<img src="{uri}" style="width:100%;height:100%;object-fit:{fit};object-position:{pos};display:block">';style+='overflow:hidden;'
        else:body=escape(str(n.get('text',''))).replace('\n','<br>');style+=f'font-size:{n.get("size",18)}px;'
        parts.append(f'<div class="node {escape(str(typ))}" style="{style}" {attrs}>{body}</div>')
    return f'''<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>多寫 · Cover · DORÉ DESIGN</title><style>*{{box-sizing:border-box}}html,body{{margin:0;background:#c2c2bf;color:#252525;font-family:"Cormorant Garamond","Noto Serif TC",Georgia,serif}}body{{padding:22px}}.frame{{width:min({cw}px,100%);margin:auto;overflow:auto}}.canvas{{position:relative;width:{cw}px;height:{ch}px;background:#CEBD74;box-shadow:0 12px 42px #0003;transform-origin:top left}}.node{{position:absolute;white-space:normal;line-height:1.25;text-align:center}}[data-id]{{cursor:move}}[data-id]:hover{{outline:1px dashed rgba(24,24,24,.38);outline-offset:3px}}</style></head><body><main class="frame"><article class="canvas">{''.join(parts)}</article></main></body></html>'''
