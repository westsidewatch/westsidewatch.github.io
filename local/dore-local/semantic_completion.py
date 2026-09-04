#!/usr/bin/env python3
from __future__ import annotations
import hashlib,json,urllib.request

def _get(url,timeout=10):
    with urllib.request.urlopen(url,timeout=timeout) as r:
        data=r.read()
        return r.status,data,r.headers.get('content-type','')

def verify(msg,result,root=None,home=None):
    meta=msg.get('metadata') or {}
    contract=meta.get('semantic_contract')
    if not isinstance(contract,dict):
        return {'ok':True,'code':'NO_SEMANTIC_CONTRACT','checked':False}
    ctype=contract.get('type')
    if ctype!='dore_design_editor_pages':
        return {'ok':False,'code':'UNKNOWN_SEMANTIC_CONTRACT','checked':True,'type':ctype}
    base=str(contract.get('editor_base') or 'http://127.0.0.1:4310').rstrip('/')
    required=list(contract.get('required_page_ids') or [])
    rationale_keys=list(contract.get('rationale_keys') or ['hypothesis','why_test','prior_learning_consumed','deliberately_rejected','largest_risk'])
    minimum_nodes=int(contract.get('minimum_nodes_per_page') or 1)
    status,data,_=_get(base+'/api/workspace')
    if status!=200:
        return {'ok':False,'code':'WORKSPACE_HTTP_FAIL','checked':True,'status':status}
    try:w=json.loads(data.decode('utf-8'))
    except Exception as e:return {'ok':False,'code':'WORKSPACE_JSON_FAIL','checked':True,'error':repr(e)}
    pages={p.get('id'):p for p in w.get('pages',[]) if isinstance(p,dict)}
    missing=[pid for pid in required if pid not in pages]
    details=[]
    failures=[]
    if missing:failures.append({'gate':'required_pages','missing':missing})
    for pid in required:
        p=pages.get(pid)
        if not p:continue
        rationale=p.get('rationale') if isinstance(p.get('rationale'),dict) else {}
        missing_rationale=[k for k in rationale_keys if not str(rationale.get(k) or '').strip()]
        nodes=p.get('nodes') if isinstance(p.get('nodes'),list) else []
        editable_ok=len(nodes)>=minimum_nodes and all(isinstance(n,dict) and n.get('id') and n.get('type') for n in nodes)
        acceptance_ok=p.get('experimental_only') is True and p.get('product_acceptance') is False and p.get('style_acceptance') is False
        preview_status,preview,_=_get(base+'/preview/'+pid)
        export_status,exported,_=_get(base+'/api/export.html?page='+pid)
        preview_sha=hashlib.sha256(preview).hexdigest(); export_sha=hashlib.sha256(exported).hexdigest()
        same_source=preview_status==200 and export_status==200 and preview_sha==export_sha
        row={'page_id':pid,'node_count':len(nodes),'editable_ok':editable_ok,'missing_rationale':missing_rationale,'acceptance_ok':acceptance_ok,'preview_status':preview_status,'export_status':export_status,'preview_sha256':preview_sha,'export_sha256':export_sha,'preview_export_same':same_source}
        details.append(row)
        if not editable_ok:failures.append({'gate':'editable_page','page_id':pid,'node_count':len(nodes)})
        if missing_rationale:failures.append({'gate':'rationale','page_id':pid,'missing':missing_rationale})
        if not acceptance_ok:failures.append({'gate':'acceptance_semantics','page_id':pid})
        if not same_source:failures.append({'gate':'preview_export_same_source','page_id':pid})
    min_count=int(contract.get('minimum_family_count') or len(required))
    matched=sum(1 for pid in required if pid in pages)
    if matched<min_count:failures.append({'gate':'minimum_family_count','required':min_count,'actual':matched})
    ok=not failures
    return {'ok':ok,'code':'SEMANTIC_COMPLETION_PASS' if ok else 'SEMANTIC_COMPLETION_FAIL','checked':True,'contract_type':ctype,'workspace_revision':w.get('revision'),'workspace_page_count':len(pages),'required_count':len(required),'matched_count':matched,'details':details,'failures':failures}
