"""Deterministic canonical HTML renderer for DORÉ DESIGN 2.0 snapshots."""
from __future__ import annotations
import base64,hashlib
from html import escape
from pathlib import Path

def _num(value,default=0):
    try:return float(value)
    except (TypeError,ValueError):return float(default)
def _css_num(value):
    n=_num(value);return str(int(n)) if n.is_integer() else ("%.4f"%n).rstrip('0').rstrip('.')
def _node_text(node):
    for key in ('text','title','eyebrow','body'):
        if node.get(key) is not None:return str(node.get(key))
    return ''

def _extra_style(node):
    raw=node.get('style') or {};out=[]
    mapping={'background':'background','color':'color','border':'border','border_radius':'border-radius','opacity':'opacity','letter_spacing':'letter-spacing','line_height':'line-height','font_weight':'font-weight','font_family':'font-family'}
    forbidden=('url(', 'expression(', 'javascript:', '@import', 'data:', 'file:')
    for key,css in mapping.items():
        if key not in raw:continue
        value=str(raw[key]).replace(';','').replace('<','').replace('>','')
        if any(token in value.lower() for token in forbidden):raise ValueError('unsafe_style_value')
        out.append(f'{css}:{value}')
    kind=node.get('type')
    if kind=='light':out+=['pointer-events:none','filter:blur(28px)']
    if kind=='portal':out+=['box-sizing:border-box']
    return out

def _trusted_data_uri(asset):
    if not isinstance(asset,dict) or asset.get('trusted') is not True:raise ValueError('trusted_image_asset_required')
    mime=str(asset.get('mime_type') or '')
    if mime not in {'image/png','image/jpeg','image/webp'}:raise ValueError('trusted_image_mime_invalid')
    path=Path(str(asset.get('path') or ''))
    if not path.is_file():raise ValueError('trusted_image_asset_missing')
    raw=path.read_bytes()
    digest=hashlib.sha256(raw).hexdigest()
    if digest!=str(asset.get('sha256') or ''):raise ValueError('trusted_image_sha_mismatch')
    if len(raw)!=int(asset.get('bytes') or -1):raise ValueError('trusted_image_size_mismatch')
    return 'data:'+mime+';base64,'+base64.b64encode(raw).decode('ascii')

def render_snapshot(snapshot,edit=False,trusted_assets=None):
    if snapshot.get('schema')!='dore.design.publish-snapshot.v1':raise ValueError('invalid_snapshot_schema')
    trusted_assets=trusted_assets or {};page=snapshot.get('page') or {};canvas=page.get('canvas') or {};width=_css_num(canvas.get('width',canvas.get('w',page.get('width',1440))));height=_css_num(canvas.get('height',canvas.get('h',page.get('height',900))));nodes=[]
    for node in page.get('nodes') or []:
        nid=escape(str(node.get('id','')),quote=True);kind=escape(str(node.get('type','node')),quote=True);x=_css_num(node.get('x',0));y=_css_num(node.get('y',0));w=node.get('w',node.get('width'));h=node.get('h',node.get('height'));style=[f'left:{x}px',f'top:{y}px','position:absolute']
        if w is not None:style.append(f'width:{_css_num(w)}px')
        if h is not None:style.append(f'height:{_css_num(h)}px')
        if node.get('size') is not None:style.append(f'font-size:{_css_num(node["size"])}px')
        if node.get('text_align') in ('left','center','right'):style.append('text-align:'+node['text_align'])
        style+=_extra_style(node);attrs=f'data-d2-node="{nid}" data-id="{nid}" data-kind="{kind}"' if edit else f'data-id="{nid}" data-kind="{kind}"'
        if node.get('type')=='image':
            ref=str(node.get('asset_ref') or '');asset=trusted_assets.get(ref)
            if asset is None:raise ValueError('trusted_image_asset_ref_missing:'+ref)
            src=escape(_trusted_data_uri(asset),quote=True);fit=str(node.get('fit') or 'cover')
            if fit not in {'cover','contain','fill'}:raise ValueError('trusted_image_fit_invalid')
            cx=max(0,min(100,_num(node.get('crop_x',50),50)));cy=max(0,min(100,_num(node.get('crop_y',50),50)))
            img_style='width:100%;height:100%;display:block;object-fit:'+fit+';object-position:'+_css_num(cx)+'% '+_css_num(cy)+'%'
            nodes.append(f'<div {attrs} style="{";".join(style)};overflow:hidden"><img alt="" aria-hidden="true" src="{src}" style="{img_style}"></div>')
        else:
            text=escape(_node_text(node));nodes.append(f'<div {attrs} style="{";".join(style)}">{text}</div>')
    marker=escape(str(snapshot.get('sha256','')),quote=True)
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;background:#bbb}.d2-page{position:relative;overflow:hidden;background:#fff;margin:0 auto}</style></head><body><main class="d2-page" data-d2-snapshot="'+marker+'" style="width:'+width+'px;height:'+height+'px">'+''.join(nodes)+'</main></body></html>'