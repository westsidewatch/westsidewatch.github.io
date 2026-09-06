#!/usr/bin/env python3
"""Final Design 2.0 product closeout acceptance."""
def check(base):
    w=base.workspace();pages={p.get('id'):p for p in w.get('pages',[])};home=pages.get('multiwrite-home');cover=pages.get('multiwrite-cover')
    checks={'workspace':bool(w.get('id')),'multiwrite_home':bool(home),'multiwrite_cover':bool(cover),'cover_structured':bool(cover and len(cover.get('nodes',[]))>=5),'revisioned':isinstance(w.get('revision'),int),'assets':isinstance(w.get('assets',{}),dict)}
    return {'ok':all(checks.values()),'schema':'dore.design2.closeout.v1','status':'complete' if all(checks.values()) else 'incomplete','checks':checks,'revision':w.get('revision'),'editor':'/editor?page=multiwrite-cover'}
