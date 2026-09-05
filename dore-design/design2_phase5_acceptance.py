#!/usr/bin/env python3
"""HTTP acceptance for DORÉ DESIGN 2.0 Phase 5 recommendation learning."""
import json,urllib.request
BASE='http://127.0.0.1:4310'

def get(path):
    with urllib.request.urlopen(BASE+path) as r:return json.load(r)

def post(path,payload):
    req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
    with urllib.request.urlopen(req) as r:return json.load(r)

rev=int(get('/api/preview/status')['revision'])
cmd={'op':'node.nudge','page_id':'multiwrite-home','ids':['mw-story-title'],'dx':8,'dy':0}
rec1=post('/api/design2/recommendation',{'page_id':'multiwrite-home','commands':[cmd],'reason':'test reject'})['recommendation']
rej=post('/api/design2/recommendation/decision',{'recommendation_id':rec1['id'],'decision':'reject','revision':rev})['recommendation']
assert rej['decision']=='reject' and rej['result_revision']==rev
rec2=post('/api/design2/recommendation',{'page_id':'multiwrite-home','commands':[cmd],'reason':'test accept','signals':['alignment']})['recommendation']
acc=post('/api/design2/recommendation/decision',{'recommendation_id':rec2['id'],'decision':'accept','revision':rev})['recommendation']
assert acc['decision']=='accept' and acc['result_revision']>rev
log=get('/api/design2/recommendations')['log']
rows={e['id']:e for e in log['events']}
assert rows[rec1['id']]['decision']=='reject'
assert rows[rec2['id']]['decision']=='accept'
assert rows[rec2['id']]['result_revision']==acc['result_revision']
print('DORE_DESIGN2_PHASE5_RECOMMENDATION_ACCEPTANCE_PASS')
