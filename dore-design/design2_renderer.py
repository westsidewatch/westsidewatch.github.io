"""Deterministic canonical HTML renderer for DORÉ DESIGN 2.0 snapshots."""
from html import escape


def _num(value, default=0):
    try:
        return float(value)
    except (TypeError, ValueError):
        return float(default)


def _css_num(value):
    n=_num(value)
    return str(int(n)) if n.is_integer() else ("%.4f" % n).rstrip('0').rstrip('.')


def _node_text(node):
    for key in ('text','title','eyebrow','body'):
        if node.get(key) is not None:
            return str(node.get(key))
    return ''


def render_snapshot(snapshot, edit=False):
    if snapshot.get('schema')!='dore.design.publish-snapshot.v1':
        raise ValueError('invalid_snapshot_schema')
    page=snapshot.get('page') or {}
    canvas=page.get('canvas') or {}
    width=_css_num(canvas.get('width', page.get('width', 1440)))
    height=_css_num(canvas.get('height', page.get('height', 900)))
    nodes=[]
    for node in page.get('nodes') or []:
        nid=escape(str(node.get('id','')), quote=True)
        kind=escape(str(node.get('type','node')), quote=True)
        x=_css_num(node.get('x',0));y=_css_num(node.get('y',0))
        w=node.get('w',node.get('width'));h=node.get('h',node.get('height'))
        style=[f'left:{x}px',f'top:{y}px','position:absolute']
        if w is not None: style.append(f'width:{_css_num(w)}px')
        if h is not None: style.append(f'height:{_css_num(h)}px')
        if node.get('size') is not None: style.append(f'font-size:{_css_num(node["size"])}px')
        if node.get('text_align') in ('left','center','right'): style.append('text-align:'+node['text_align'])
        text=escape(_node_text(node))
        attrs=f'data-d2-node="{nid}" data-id="{nid}" data-kind="{kind}"' if edit else f'data-id="{nid}" data-kind="{kind}"'
        nodes.append(f'<div {attrs} style="{";".join(style)}">{text}</div>')
    marker=escape(str(snapshot.get('sha256','')),quote=True)
    return '<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><style>html,body{margin:0;background:#bbb}.d2-page{position:relative;overflow:hidden;background:#fff;margin:0 auto}</style></head><body><main class="d2-page" data-d2-snapshot="'+marker+'" style="width:'+width+'px;height:'+height+'px">'+''.join(nodes)+'</main></body></html>'
