#!/usr/bin/env python3
"""Acceptance: concurrent Doré Design mutations are serialized without loss."""
from concurrent.futures import ThreadPoolExecutor, as_completed
import json, os, urllib.request

BASE=f"http://127.0.0.1:{os.environ.get('DORE_DESIGN_PORT','4310')}"
COUNT=int(os.environ.get('DORE_CONCURRENCY_PROBES','16'))

def get(path):
    with urllib.request.urlopen(BASE+path,timeout=8) as r:return json.load(r)

def post(payload):
    req=urllib.request.Request(BASE+'/api/workspace',data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req,timeout=8) as r:return json.load(r)

w0=get('/api/workspace');r0=int(w0['revision'])
page='feature-story' if any(p.get('id')=='feature-story' for p in w0.get('pages',[])) else w0['pages'][0]['id']
prefix='concurrency-probe-'
payloads=[{'op':'add_text','page_id':page,'id':f'{prefix}{i:02d}','text':f'CONCURRENT PROBE {i:02d}'} for i in range(COUNT)]

results=[]
with ThreadPoolExecutor(max_workers=min(COUNT,12)) as pool:
    futures=[pool.submit(post,p) for p in payloads]
    for f in as_completed(futures):results.append(f.result())

wf=get('/api/workspace');rf=int(wf['revision'])
assert rf==r0+COUNT, {'error':'concurrent_revision_loss','before':r0,'after':rf,'expected':r0+COUNT}
pg=next(p for p in wf['pages'] if p['id']==page)
ids={n.get('id') for n in pg.get('nodes',[])}
missing=[f'{prefix}{i:02d}' for i in range(COUNT) if f'{prefix}{i:02d}' not in ids]
assert not missing, {'error':'lost_concurrent_nodes','missing':missing}
assert len(results)==COUNT
revs=sorted(int(x['revision']) for x in results)
assert revs==list(range(r0+1,r0+COUNT+1)), {'error':'non_serial_revision_sequence','revisions':revs}

print(json.dumps({'ok':True,'code':'DORE_DESIGN_RUNTIME_CONCURRENCY_PASS','writers':COUNT,'revision_start':r0,'revision_final':rf,'all_nodes_present':True,'serial_revision_sequence':True},ensure_ascii=False))
