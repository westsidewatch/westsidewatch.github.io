#!/usr/bin/env python3
"""Machine-readable contract for the first real Design 2.0 consumer page."""
def status(base):
    w=base.workspace();p=base.page(w,'multiwrite-cover')
    return {'ok':bool(p),'consumer':'multiwrite','surface':'cover','page_id':'multiwrite-cover','editable':True,'structured':True,'node_count':len(p.get('nodes',[])) if p else 0,'revision':w.get('revision'),'editor':'/editor?page=multiwrite-cover'}
