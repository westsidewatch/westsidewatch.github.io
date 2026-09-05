"""Pre-promotion validation for immutable DORÉ DESIGN 2.0 candidates."""
from urllib.parse import urlparse
import design2_snapshot

ALLOWED_SCHEMES={'','http','https','mailto','tel'}
URL_KEYS={'href','src','url','link'}


def validate_snapshot(snapshot):
    errors=[]
    if not design2_snapshot.verify(snapshot): errors.append('snapshot_integrity')
    page=snapshot.get('page') or {}
    if page.get('id')!=snapshot.get('page_id'): errors.append('page_id_mismatch')
    nodes=page.get('nodes') or []
    ids=[]
    for node in nodes:
        nid=node.get('id')
        if not isinstance(nid,str) or not nid: errors.append('node_id_missing')
        else: ids.append(nid)
        for key in URL_KEYS:
            value=node.get(key)
            if value is None: continue
            if not isinstance(value,str): errors.append(f'invalid_url_type:{nid}:{key}');continue
            parsed=urlparse(value.strip())
            if parsed.scheme.lower() not in ALLOWED_SCHEMES: errors.append(f'unsafe_url_scheme:{nid}:{key}')
            if value.strip().lower().startswith(('javascript:','data:text/html','vbscript:')): errors.append(f'unsafe_url:{nid}:{key}')
        for key,value in node.items():
            if key.lower().startswith('on') and isinstance(value,str) and value.strip(): errors.append(f'executable_attribute:{nid}:{key}')
    if len(ids)!=len(set(ids)): errors.append('duplicate_node_id')
    return {'ok':not errors,'errors':errors,'checks':{'integrity':True,'structure':True,'urls':True,'executable_content':True}}


def require_valid(snapshot):
    result=validate_snapshot(snapshot)
    if not result['ok']: raise ValueError('candidate_validation_failed:'+','.join(result['errors']))
    return result
