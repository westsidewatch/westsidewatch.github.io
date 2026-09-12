#!/usr/bin/env python3
"""Acceptance for real repo-backed Visual Editorial Director candidates."""
from pathlib import Path
import json

import sitewide_editorial_candidates as sitewide
import visual_editorial_director as ved

r=sitewide.load()
ids=[c.id for c in r.candidates]
assert ids and len(ids)==len(set(ids))
assert all(x.startswith('site:') for x in ids)

required=('church','dawn-library','one','dore-folio','visual-graph')
for source in required:
    assert r.diagnostics[source]['count']>0, (source,r.diagnostics[source])

# Journal currently has structural _index only: zero is truthful and must remain
# zero until real articles appear. This test intentionally rejects fake fillers.
assert r.diagnostics['journal']['count']==0, r.diagnostics['journal']
assert not any(c.id.startswith('site:journal:') for c in r.candidates)

root=sitewide.ROOT.resolve()
for cid,p in r.provenance.items():
    rel=p['path']
    # Glob-style diagnostic paths are never candidate provenance paths.
    path=(root/rel).resolve()
    assert path==root or root in path.parents, (cid,path)
    assert path.exists(), (cid,path)

# Visual assets that reach the editorial pool must be rights-cleared for branded
# derivative use. Restricted manuscript imagery must not leak into homepage use.
visual=[c for c in r.candidates if c.id.startswith('site:visual:')]
assert visual
for c in visual:
    p=r.provenance[c.id]
    assert c.image
    assert p['rights']['branded_derivative_allowed'] is True
assert not any('initiale-lev1' in c.id for c in visual)

selected=ved.select(r.candidates,per_w=4)
assert tuple(selected)==ved.WORLDS
assert all(len(v)==4 for v in selected.values()), {k:len(v) for k,v in selected.items()}
chosen=[c for pairs in selected.values() for c,_ in pairs]
assert len({c.id for c in chosen})==16
assert all(c.id.startswith('site:') for c in chosen)

# Build-time ONE operational metadata is read-only provenance and is never wired
# into the ONE reader runtime.
assert r.diagnostics['one']['runtime_isolation'] is True
assert all(r.provenance[c.id].get('runtime_isolation') is True for c in r.candidates if c.id.startswith('site:one:'))

print(json.dumps({
    'ok':True,
    'code':'DORE_SITEWIDE_EDITORIAL_CANDIDATES_PASS',
    'total':len(r.candidates),
    'sources':{k:v.get('count') for k,v in r.diagnostics.items() if isinstance(v,dict) and 'count' in v},
    'selected':{k:[c.id for c,_ in v] for k,v in selected.items()},
},ensure_ascii=False))
