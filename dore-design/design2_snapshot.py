"""Immutable revision snapshots for DORÉ DESIGN 2.0 Phase 4."""
import copy,hashlib,json,time

def _canonical_bytes(value):
    return json.dumps(value,ensure_ascii=False,sort_keys=True,separators=(',',':')).encode('utf-8')

def snapshot(workspace,page_id):
    page=next((p for p in workspace.get('pages',[]) if p.get('id')==page_id),None)
    if not page: raise ValueError('page_not_found')
    revision=int(workspace.get('revision',0))
    payload={
        'schema':'dore.design.publish-snapshot.v1',
        'workspace_id':workspace.get('id'),
        'revision':revision,
        'page_id':page_id,
        'page':copy.deepcopy(page),
        'tokens':copy.deepcopy(workspace.get('tokens',{})),
    }
    digest=hashlib.sha256(_canonical_bytes(payload)).hexdigest()
    return {**payload,'sha256':digest,'created_at':int(time.time())}

def verify(s):
    if s.get('schema')!='dore.design.publish-snapshot.v1': return False
    digest=s.get('sha256')
    payload={k:copy.deepcopy(v) for k,v in s.items() if k not in {'sha256','created_at'}}
    return isinstance(digest,str) and hashlib.sha256(_canonical_bytes(payload)).hexdigest()==digest
