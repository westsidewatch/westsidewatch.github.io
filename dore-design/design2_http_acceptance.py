#!/usr/bin/env python3
"""Resident HTTP acceptance for DORÉ DESIGN 2.0 Phase 4."""
import json,urllib.request

BASE='http://127.0.0.1:4310'

def get_json(path):
    with urllib.request.urlopen(BASE+path) as r:
        return json.load(r)

def get_text(path):
    with urllib.request.urlopen(BASE+path) as r:
        return r.read().decode('utf-8')

def post(path,payload):
    req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req) as r:
        return json.load(r)

status=get_json('/api/preview/status')
rev1=int(status['revision'])
page='multiwrite-home'
first=post('/api/design2/candidate',{'page_id':page,'revision':rev1})['candidate']
preview1=get_text('/api/design2/preview?candidate='+first['id'])
assert '多寫' in preview1 or 'Write on. Make it a book.' in preview1
r1=post('/api/design2/publish',{'candidate_id':first['id'],'revision':rev1,'target':page})['release']
published1=get_text('/design2/published')
assert r1['candidate_id']==first['id']
assert published1==preview1

# Mutate the live workspace. The already published immutable snapshot must not move.
w2=post('/api/workspace',{'op':'design_decision','page_id':page,'decision':{'color':'watch-night','hierarchy':'display','axis':'left','density':'2','lines':'2'}})
rev2=int(w2['revision'])
assert rev2>rev1
assert get_text('/design2/published')==published1

# Publish the new revision, then roll back to the previous known-good release.
second=post('/api/design2/candidate',{'page_id':page,'revision':rev2})['candidate']
assert second['id']!=first['id']
preview2=get_text('/api/design2/preview?candidate='+second['id'])
assert preview2!=preview1
r2=post('/api/design2/publish',{'candidate_id':second['id'],'revision':rev2,'target':page})['release']
assert r2['previous']['candidate_id']==first['id']
assert get_text('/design2/published')==preview2
restored=post('/api/design2/rollback',{})['release']
assert restored['candidate_id']==first['id']
assert get_text('/design2/published')==published1
registry=get_json('/api/design2/publication')['registry']
assert registry['current_release']['candidate_id']==first['id']
print('DORE_DESIGN2_PHASE4_HTTP_ACCEPTANCE_PASS')
