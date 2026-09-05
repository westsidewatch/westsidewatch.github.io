#!/usr/bin/env python3
"""Live acceptance against the resident Doré Design service without user intervention.

This smoke test verifies the resident workspace/mutation/render path. Individual
product surfaces (Journal, candidates, Multiwrite, etc.) have their own
acceptance checks and must not make this core mutation smoke test fail merely
because an optional fixture has not been imported into a fresh temp workspace.
"""
import json,urllib.request,urllib.parse,sys,time
BASE='http://127.0.0.1:4310'
def req(path,data=None):
 body=None;headers={}
 if data is not None:
  body=json.dumps(data).encode();headers['Content-Type']='application/json'
 r=urllib.request.Request(BASE+path,data=body,headers=headers,method='POST' if data is not None else 'GET')
 with urllib.request.urlopen(r,timeout=5) as x:return x.status,x.headers.get_content_type(),x.read()
def j(path,data=None):return json.loads(req(path,data)[2])
health=j('/api/health');assert health.get('service')=='dore-design' and str(health.get('version',''))>='0.8',health
w=j('/api/workspace');assert len(w.get('pages',[]))>=2
pid='feature-story' if any(p['id']=='feature-story' for p in w['pages']) else w['pages'][0]['id']
probe='local-acceptance-probe'
# clean an interrupted prior probe first
pg=next(p for p in w['pages'] if p['id']==pid)
if any(n['id']==probe for n in pg.get('nodes',[])):
 w=j('/api/workspace',{'op':'delete_node','page_id':pid,'id':probe})
r0=w['revision']
w=j('/api/workspace',{'op':'add_text','page_id':pid,'id':probe,'text':'DORÉ LOCAL ACCEPTANCE'});assert w['revision']==r0+1
pg=next(p for p in w['pages'] if p['id']==pid);assert any(n['id']==probe for n in pg['nodes'])
w=j('/api/workspace',{'op':'set_node','page_id':pid,'id':probe,'patch':{'x':96,'y':760,'w':700,'size':22,'text':'DORÉ LOCAL ACCEPTANCE — EDITED'}})
_,ctype,svg=req('/api/export.svg?page='+urllib.parse.quote(pid));assert ctype=='image/svg+xml' and b'DOR' in svg and b'EDITED' in svg
v=j('/api/verify');assert v['ok'] and v['page_count']>=2,v
w=j('/api/workspace',{'op':'delete_node','page_id':pid,'id':probe});pg=next(p for p in w['pages'] if p['id']==pid);assert not any(n['id']==probe for n in pg['nodes'])
v2=j('/api/verify');assert v2['ok'],v2
print(json.dumps({'ok':True,'code':'DORE_DESIGN_LOCAL_ACCEPTANCE_PASS','version':health.get('version'),'service_ready':True,'aggregate_health':health.get('ok'),'page_count':v2['page_count'],'revision':v2['revision'],'same_artifact_mutation':True,'resident_render':True,'resident_verify':True,'cleanup':True},ensure_ascii=False))
