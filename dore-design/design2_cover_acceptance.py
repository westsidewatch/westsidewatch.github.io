#!/usr/bin/env python3
"""Acceptance probe for the Multiwrite Cover production consumer."""
def check(base):
    w=base.workspace();p=base.page(w,'multiwrite-cover');ids={n.get('id') for n in (p or {}).get('nodes',[])}
    required={'mwc-frame','mwc-kicker','mwc-title','mwc-subtitle','mwc-rule','mwc-note'}
    checks={'page':bool(p),'structured_nodes':required.issubset(ids),'canvas':bool(p and p.get('canvas',{}).get('w')==1200 and p.get('canvas',{}).get('h')==1500),'revisioned':isinstance(w.get('revision'),int)}
    return {'ok':all(checks.values()),'schema':'dore.design.cover-acceptance.v1','page_id':'multiwrite-cover','revision':w.get('revision'),'node_count':len((p or {}).get('nodes',[])),'checks':checks}
