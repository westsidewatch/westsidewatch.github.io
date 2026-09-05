"""Phase 6 production specimen contract for DORÉ DESIGN 2.0."""
PAGE_ID='multiwrite-home'
REQUIRED_NODES={'mw-title','mw-slogan','mw-story-title','mw-story-body','mw-library'}


def inspect(workspace):
    page=next((p for p in workspace.get('pages',[]) if p.get('id')==PAGE_ID),None)
    if not page:return {'ok':False,'page_id':PAGE_ID,'errors':['page_missing']}
    ids={n.get('id') for n in page.get('nodes',[])}
    design=page.get('design') or {}
    decision=design.get('decision') or {}
    checks={
        'canonical_page':page.get('id')==PAGE_ID,
        'product_identity':page.get('product')=='multiwrite',
        'required_nodes':REQUIRED_NODES.issubset(ids),
        'semantic_design':design.get('schema')=='dore.design-decision.v1' and bool(decision),
        'canvas':int((page.get('canvas') or {}).get('w',0))>0 and int((page.get('canvas') or {}).get('h',0))>0,
    }
    return {
        'ok':all(checks.values()),
        'schema':'dore.design.production-specimen.v1',
        'phase':6,
        'page_id':PAGE_ID,
        'workspace_id':workspace.get('id'),
        'revision':workspace.get('revision'),
        'checks':checks,
        'node_count':len(page.get('nodes',[])),
        'design':design,
        'surfaces':{
            'editor':'/editor?page=multiwrite-home',
            'canvas':'/editor-canvas?page=multiwrite-home',
            'candidate':'/api/design2/candidate',
            'preview':'/api/design2/preview?candidate=<id>',
            'published':'/design2/published',
            'recommendations':'/api/design2/recommendations',
        },
    }
