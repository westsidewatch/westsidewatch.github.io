#!/usr/bin/env python3
"""HTTP acceptance for DORÉ DESIGN 2.0 Phase 5 recommendation learning."""
import json,os,urllib.request,urllib.error
BASE=f"http://127.0.0.1:{os.environ.get('DORE_DESIGN_PORT','4310')}";stage='bootstrap'

def get(path):
    with urllib.request.urlopen(BASE+path) as r:return json.load(r)

def post(path,payload):
    req=urllib.request.Request(BASE+path,data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
    try:
        with urllib.request.urlopen(req) as r:return json.load(r)
    except urllib.error.HTTPError as e:
        body=e.read().decode('utf-8','replace');raise RuntimeError(f'HTTP {e.code} {path}: {body}') from e

try:
    stage='revision';rev=int(get('/api/workspace')['revision'])
    cmd={'op':'node.text','page_id':'multiwrite-home','id':'mw-story-title','text':'PHASE 5 RECOMMENDATION ACCEPTED'}
    stage='propose-reject';rec1=post('/api/design2/recommendation',{'page_id':'multiwrite-home','commands':[cmd],'reason':'test reject'})['recommendation']
    stage='decide-reject';rej=post('/api/design2/recommendation/decision',{'recommendation_id':rec1['id'],'decision':'reject','revision':rev})['recommendation']
    assert rej['decision']=='reject' and rej['result_revision']==rev
    stage='propose-accept';rec2=post('/api/design2/recommendation',{'page_id':'multiwrite-home','commands':[cmd],'reason':'test accept','signals':['renderer-visible-text']})['recommendation']
    stage='decide-accept';acc=post('/api/design2/recommendation/decision',{'recommendation_id':rec2['id'],'decision':'accept','revision':rev})['recommendation']
    assert acc['decision']=='accept' and acc['result_revision']>rev
    stage='workspace-visible';workspace=get('/api/workspace');page=next(p for p in workspace['pages'] if p['id']=='multiwrite-home');node=next(n for n in page['nodes'] if n['id']=='mw-story-title');assert node['text']=='PHASE 5 RECOMMENDATION ACCEPTED'
    stage='learning-log';log=get('/api/design2/recommendations')['log'];rows={e['id']:e for e in log['events']};assert rows[rec1['id']]['decision']=='reject';assert rows[rec2['id']]['decision']=='accept';assert rows[rec2['id']]['result_revision']==acc['result_revision']
except Exception as e:
    print(f'::error title=Phase 5 regression::{stage}: {type(e).__name__}: {e}')
    raise
print('DORE_DESIGN2_PHASE5_RECOMMENDATION_ACCEPTANCE_PASS')
