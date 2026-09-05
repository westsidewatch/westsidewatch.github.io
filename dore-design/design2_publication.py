"""Candidate registry and promotion metadata for DORÉ DESIGN 2.0 Phase 4."""
import json,os,tempfile
from pathlib import Path
import design2_snapshot,design2_validation

def _atomic_json(path,data):
    path=Path(path);path.parent.mkdir(parents=True,exist_ok=True)
    fd,tmp=tempfile.mkstemp(prefix=path.name+'.',dir=str(path.parent))
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as f: json.dump(data,f,ensure_ascii=False,indent=2,sort_keys=True)
        os.replace(tmp,path)
    finally:
        if os.path.exists(tmp): os.unlink(tmp)

def create_candidate(workspace,page_id,registry_path):
    snap=design2_snapshot.snapshot(workspace,page_id)
    validation=design2_validation.validate_snapshot(snap)
    reg=_load(registry_path)
    cid=f"{page_id}-r{snap['revision']}-{snap['sha256'][:12]}"
    row={'id':cid,'status':'validated' if validation['ok'] else 'rejected','snapshot':snap,'validation':validation}
    reg.setdefault('candidates',{})[cid]=row
    _atomic_json(registry_path,reg)
    return row

def promote(candidate_id,registry_path):
    reg=_load(registry_path);row=(reg.get('candidates') or {}).get(candidate_id)
    if not row: raise ValueError('candidate_not_found')
    validation=design2_validation.require_valid(row['snapshot'])
    previous=reg.get('current_release')
    release={'candidate_id':candidate_id,'page_id':row['snapshot']['page_id'],'revision':row['snapshot']['revision'],'sha256':row['snapshot']['sha256'],'previous':previous,'validation':validation}
    reg['last_known_good']=previous or reg.get('last_known_good')
    reg['current_release']=release
    row['status']='published';row['validation']=validation
    _atomic_json(registry_path,reg)
    return release

def rollback(registry_path):
    reg=_load(registry_path);target=reg.get('last_known_good')
    if not target: raise ValueError('rollback_unavailable')
    current=reg.get('current_release');reg['current_release']=target;reg['last_known_good']=current
    _atomic_json(registry_path,reg)
    return target

def _load(path):
    p=Path(path)
    if not p.exists(): return {'schema':'dore.design.publication-registry.v1','candidates':{}}
    return json.loads(p.read_text(encoding='utf-8'))
