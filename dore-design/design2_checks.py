"""Bounded structural/accessibility/link/smoke checks for Phase 4 staging."""
from urllib.parse import urlparse


def run(snapshot,html):
    errors=[]
    page=snapshot.get('page') or {}
    nodes=page.get('nodes') or []
    for n in nodes:
        nid=n.get('id','?')
        if n.get('type')=='image':
            alt=n.get('alt')
            if not isinstance(alt,str) or not alt.strip(): errors.append(f'image_alt_missing:{nid}')
        for key in ('href','src','url','link'):
            value=n.get(key)
            if not isinstance(value,str) or not value.strip(): continue
            p=urlparse(value.strip())
            if p.scheme in ('http','https') and not p.netloc: errors.append(f'broken_absolute_url:{nid}:{key}')
    if '<script' in html.lower(): errors.append('published_runtime_script_present')
    if 'moveable' in html.lower() or 'selecto' in html.lower(): errors.append('editor_dependency_present')
    if snapshot.get('sha256') not in html: errors.append('snapshot_marker_missing')
    return {'ok':not errors,'errors':errors,'checks':{'accessibility':True,'links':True,'published_runtime':True,'snapshot_marker':True}}


def require(snapshot,html):
    result=run(snapshot,html)
    if not result['ok']: raise ValueError('staging_checks_failed:'+','.join(result['errors']))
    return result
