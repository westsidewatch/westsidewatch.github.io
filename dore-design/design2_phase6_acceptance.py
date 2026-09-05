#!/usr/bin/env python3
"""End-to-end Phase 6 acceptance for the Multiwrite production specimen."""
import json,urllib.request

BASE='http://127.0.0.1:4310'

def get_json(path):
    with urllib.request.urlopen(BASE+path) as r:return json.load(r)

def get_text(path):
    with urllib.request.urlopen(BASE+path) as r:return r.read().decode('utf-8')

def post(path,payload):
    req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode('utf-8'),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req) as r:return json.load(r)

spec=get_json('/api/design2/specimen')
assert spec['ok'] and spec['phase']==6 and spec['page_id']=='multiwrite-home'
assert all(spec['checks'].values())
assert 'DORÉ · 多寫' in get_text('/editor?page=multiwrite-home')
canvas=get_text('/editor-canvas?page=multiwrite-home')
assert '多寫' in canvas and 'Write on. Make it a book.' in canvas
rev=int(spec['revision'])
proposal=post('/api/design2/recommendation',{
    'page_id':'multiwrite-home',
    'reason':'Phase 6 production specimen proves Doré recommendation mutates the same canonical page.',
    'context':{'phase':6,'specimen':'multiwrite-home'},
    'signals':['production-specimen','multiwrite'],
    'commands':[{'op':'node.text','page_id':'multiwrite-home','id':'mw-story-title','text':'寫作、閱讀與成書，\n在同一個地方真正發生。'}]
})['recommendation']
accepted=post('/api/design2/recommendation/decision',{
    'recommendation_id':proposal['id'],'decision':'accept','revision':rev
})['recommendation']
new_rev=int(accepted['result_revision'])
assert new_rev>rev
spec2=get_json('/api/design2/specimen')
assert spec2['ok'] and int(spec2['revision'])==new_rev
candidate=post('/api/design2/candidate',{'page_id':'multiwrite-home','revision':new_rev})['candidate']
preview=get_text('/api/design2/preview?candidate='+candidate['id'])
assert '真正發生' in preview
release=post('/api/design2/publish',{'candidate_id':candidate['id'],'revision':new_rev,'target':'multiwrite-home'})['release']
published=get_text('/design2/published')
assert published==preview
assert release['page_id']=='multiwrite-home' and int(release['revision'])==new_rev
learning=get_json('/api/design2/recommendations')['log']
row=next(e for e in learning['events'] if e.get('id')==proposal['id'])
assert row['decision']=='accept' and int(row['result_revision'])==new_rev
print('DORE_DESIGN2_PHASE6_MULTIWRITE_PRODUCTION_SPECIMEN_PASS')
