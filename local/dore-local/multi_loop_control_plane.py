#!/usr/bin/env python3
"""Doré Multi-Loop Control Plane 1.0: durable event-driven workflow routing."""
from __future__ import annotations
import json,os
from datetime import datetime,timezone
from pathlib import Path
VERSION='dore.multi-loop-control-plane.v1.0';HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();STORE=HOME/'control-plane'/'state.json';ASSETS=HOME/'control-plane'/'knowledge-assets.jsonl'
def now():return datetime.now(timezone.utc).isoformat()
def load(path=STORE):
 try:return json.loads(Path(path).read_text())
 except Exception:return {'schema':'dore.control-plane-state.v1','control_plane':VERSION,'workflows':{},'active':None,'events':[]}
def save(data,path=STORE):
 p=Path(path);p.parent.mkdir(parents=True,exist_ok=True);data['updated_at']=now();t=p.with_suffix('.tmp');t.write_text(json.dumps(data,ensure_ascii=False,indent=2));t.replace(p);return data
def event(data,name,**detail):data.setdefault('events',[]).append({'at':now(),'event':name,**detail});data['events']=data['events'][-100:]
def register(loop_id,goal,*,kind,priority=50,state_path=STORE,metadata=None):
 data=load(state_path);data['workflows'][loop_id]={'loop_id':loop_id,'kind':kind,'goal':goal,'status':'DORMANT','base_priority':priority,'effective_priority':priority,'checkpoint':{},'triggers':[],'consumed_assets':[],'metadata':metadata or {},'updated_at':now()};event(data,'RECORD',loop_id=loop_id);save(data,state_path);return data['workflows'][loop_id]
def wake(loop_id,trigger,*,gravity=0,state_path=STORE):
 data=load(state_path);row=data['workflows'][loop_id];row['status']='READY';row['effective_priority']=int(row['base_priority'])+int(gravity);row['triggers'].append({'at':now(),'trigger':trigger,'gravity':gravity});event(data,'WAKE',loop_id=loop_id,trigger=trigger);save(data,state_path);return row
def route(*,state_path=STORE):
 data=load(state_path);ready=[x for x in data['workflows'].values() if x['status'] in {'READY','ACTIVE'}]
 if not ready:return None
 chosen=max(ready,key=lambda x:(x['effective_priority'],x['updated_at']));prior=data.get('active')
 if prior and prior!=chosen['loop_id'] and data['workflows'][prior]['status']=='ACTIVE':
  data['workflows'][prior]['status']='YIELDED';data['workflows'][prior]['checkpoint']={'at':now(),'reason':'higher-value workflow ready'};event(data,'YIELD',loop_id=prior,to=chosen['loop_id'])
 chosen['status']='ACTIVE';chosen['updated_at']=now();data['active']=chosen['loop_id'];event(data,'ROUTE',loop_id=chosen['loop_id'],priority=chosen['effective_priority']);save(data,state_path);return chosen
def share(loop_id,asset,*,state_path=STORE,asset_path=ASSETS):
 if not asset.get('knowledge_id') or not asset.get('provenance_preserved'):raise ValueError('verified provenance-preserving KnowledgeAsset required')
 p=Path(asset_path);p.parent.mkdir(parents=True,exist_ok=True);existing=[]
 if p.exists():existing=[json.loads(x) for x in p.read_text().splitlines() if x.strip()]
 if not any(x.get('knowledge_id')==asset['knowledge_id'] for x in existing):
  with p.open('a') as f:f.write(json.dumps({'at':now(),'producer_loop':loop_id,'asset':asset},ensure_ascii=False)+'\n')
 data=load(state_path);event(data,'SHARE',loop_id=loop_id,knowledge_id=asset['knowledge_id']);save(data,state_path);return {'ok':True,'knowledge_id':asset['knowledge_id'],'deduplicated':any(x.get('knowledge_id')==asset['knowledge_id'] for x in existing)}
def complete(loop_id,*,state_path=STORE):
 data=load(state_path);data['workflows'][loop_id]['status']='PASS';data['active']=None;event(data,'PASS',loop_id=loop_id)
 yielded=[x for x in data['workflows'].values() if x['status']=='YIELDED']
 if yielded:
  resume=max(yielded,key=lambda x:x['effective_priority']);resume['status']='READY';event(data,'RESUME',loop_id=resume['loop_id'],after=loop_id)
 save(data,state_path);return route(state_path=state_path) if yielded else None
def consume(loop_id,asset,*,state_path=STORE):
 data=load(state_path);row=data['workflows'][loop_id]
 if asset['knowledge_id'] not in row['consumed_assets']:row['consumed_assets'].append(asset['knowledge_id'])
 refs={str(x.get('id') or x.get('url')) for x in (row['metadata'].get('references') or [])};new=[x for x in asset.get('sources',[]) if str(x.get('id') or x.get('url')) not in refs]
 row['metadata']['references']=(row['metadata'].get('references') or [])+new;row['metadata']['current_qualified_references']=len(row['metadata']['references']);event(data,'KNOWLEDGE_REUSE',loop_id=loop_id,knowledge_id=asset['knowledge_id'],new_references=len(new));save(data,state_path);return {'new_references':len(new),'total':len(row['metadata']['references'])}
def agent_cycle(goal):
 """Run the one-shot Dawn enrichment handoff, then leave Storybook active."""
 if 'storybook' not in str(goal.get('project_loop','')).lower() and 'reference' not in str(goal.get('goal','')).lower():return {'ok':True,'managed':False}
 data=load();story='storybook-reference-expansion';dawn='dawn-library-enrichment'
 if story not in data['workflows']:
  from dawn_library_enrichment import enrich
  seed=enrich()['sources'][:int((goal.get('metadata') or {}).get('current_qualified_references') or 21)];register(story,goal.get('goal','Storybook reference expansion'),kind='storybook',priority=60,metadata={'references':seed,'minimum_qualified_references':int((goal.get('metadata') or {}).get('minimum_qualified_references') or 40)});wake(story,'agent-core-parent-goal');route()
  register(dawn,'Enrich reusable publishing knowledge',kind='dawn-library',priority=65);wake(dawn,'repository-source-material',gravity=20);route();asset=enrich();share(dawn,asset);complete(dawn);reuse=consume(story,asset);return {'ok':True,'managed':True,'handoff_completed':True,'active':story,'knowledge_id':asset['knowledge_id'],'reference_working_set':reuse['total']}
 selected=route();return {'ok':True,'managed':True,'handoff_completed':False,'active':selected.get('loop_id') if selected else data.get('active')}
