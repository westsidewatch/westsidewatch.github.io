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
rev=int(status['revision'])
page='multiwrite-home'
first=post('/api/design2/candidate',{'page_id':page,'revision':rev})['candidate']
preview=get_text('/api/design2/preview?candidate='+first['id'])
assert '多寫' in preview or 'Write on. Make it a book.' in preview
r1=post('/api/design2/publish',{'candidate_id':first['id'],'revision':rev,'target':page})['release']
published1=get_text('/design2/published')
assert r1['candidate_id']==first['id']
assert published1==preview
# A second immutable candidate/release proves last-known-good + rollback.
second=post('/api/design2/candidate',{'page_id':page,'revision':rev})['candidate']
r2=post('/api/design2/publish',{'candidate_id':second['id'],'revision':rev,'target':page})['release']
assert r2['previous']['candidate_id']==first['id']
restored=post('/api/design2/rollback',{})['release']
assert restored['candidate_id']==first['id']
assert get_text('/design2/published')==published1
registry=get_json('/api/design2/publication')['registry']
assert registry['current_release']['candidate_id']==first['id']
print('DORE_DESIGN2_PHASE4_HTTP_ACCEPTANCE_PASS')
