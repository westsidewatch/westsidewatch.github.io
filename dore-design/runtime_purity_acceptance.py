#!/usr/bin/env python3
"""Acceptance: Doré Design reads are revision-pure; explicit mutations are exact.

Runs against a resident app_design2.py service. It intentionally exercises the
most common read surfaces repeatedly because historical workspace installers
used to persist migrations during reads, causing revision drift and stale
candidate/publication failures.
"""
import json, os, urllib.request, urllib.parse

BASE=f"http://127.0.0.1:{os.environ.get('DORE_DESIGN_PORT','4310')}"

def raw(path):
    with urllib.request.urlopen(BASE+path,timeout=5) as r:
        return r.status,r.headers.get_content_type(),r.read()

def get(path):
    return json.loads(raw(path)[2])

def post(path,payload):
    req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=5) as r:
        return json.load(r)

w0=get('/api/workspace')
r0=int(w0['revision'])
page='feature-story' if any(p.get('id')=='feature-story' for p in w0.get('pages',[])) else w0['pages'][0]['id']
pg=next(p for p in w0['pages'] if p['id']==page)
node=next((n for n in pg.get('nodes',[]) if n.get('type')=='text'),None)
assert node, 'runtime_purity_requires_text_node'
node_id=node['id']; original=node.get('text','')

# Read-only resident surfaces must never persist anything.
read_json_paths=['/api/workspace','/api/health','/api/templates','/api/multiwrite/status','/api/verify','/api/design2/production-health']
read_html_paths=['/','/editor?page=multiwrite-home','/editor-canvas?page=multiwrite-home','/editor-canvas?page=living-water-candidate-01']
for _ in range(4):
    for path in read_json_paths:
        raw(path)
    for path in read_html_paths:
        raw(path)
    assert int(get('/api/workspace')['revision'])==r0, {'error':'read_revision_drift','expected':r0,'actual':get('/api/workspace')['revision']}

# One explicit mutation must be one revision, no more and no less.
probe=original+' · RUNTIME PURITY PROBE'
w1=post('/api/workspace',{'op':'set_node','page_id':page,'id':node_id,'patch':{'text':probe}})
r1=int(w1['revision'])
assert r1==r0+1, {'error':'mutation_revision_delta','before':r0,'after':r1}

# Reads after a mutation remain pure.
for _ in range(3):
    for path in read_json_paths+read_html_paths:
        raw(path)
assert int(get('/api/workspace')['revision'])==r1, {'error':'post_mutation_read_drift','expected':r1,'actual':get('/api/workspace')['revision']}

# Restore is another exact explicit mutation.
w2=post('/api/workspace',{'op':'set_node','page_id':page,'id':node_id,'patch':{'text':original}})
r2=int(w2['revision'])
assert r2==r1+1, {'error':'restore_revision_delta','before':r1,'after':r2}
for _ in range(2):
    raw('/api/workspace');raw('/api/health');raw('/api/design2/production-health')
assert int(get('/api/workspace')['revision'])==r2

print(json.dumps({'ok':True,'code':'DORE_DESIGN_RUNTIME_PURITY_PASS','revision_start':r0,'revision_after_mutation':r1,'revision_final':r2,'read_cycles':9,'mutation_delta':1,'restore_delta':1},ensure_ascii=False))
