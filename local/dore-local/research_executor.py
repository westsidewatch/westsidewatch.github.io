#!/usr/bin/env python3
"""Doré Research Executor v0.3 — executable resource search with provenance."""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path
ROOT=Path(os.environ.get('DORE_REPO_ROOT') or Path(__file__).resolve().parents[2]).expanduser().resolve();CONTROL_ROOT=Path(os.environ.get('DORE_CONTROL_ROOT',ROOT)).expanduser().resolve();HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();RESEARCH=HOME/'coordination'/'research';KNOWLEDGE=ROOT/'dore-design'/'knowledge-lab';CATALOG=KNOWLEDGE/'resources'/'source-catalog.json';LOCAL=CONTROL_ROOT/'local'/'dore-local';sys.path.insert(0,str(LOCAL))
def now():return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
 try:return json.loads(Path(p).read_text(encoding='utf-8'))
 except Exception:return default
def atomic_json(p,v):
 p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def transition(p,job,state,**extra):
 job.update({'state':state,'updated_at':now(),**extra});job.setdefault('history',[]).append({'at':now(),'state':state});atomic_json(p,job);return job
def run(argv,cwd=ROOT,timeout=90):
 try:
  cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout);return {'available':True,'argv':argv,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-16000:],'stderr':(cp.stderr or '')[-8000:]}
 except FileNotFoundError:return {'available':False,'argv':argv,'returncode':127,'error':'tool_not_found:'+str(argv[0])}
 except Exception as e:return {'available':True,'argv':argv,'returncode':126,'error':type(e).__name__+': '+str(e)}
def terms(text):
 raw=re.findall(r'[A-Za-z0-9@._:/+-]{3,}',text or '');stop={'error','failed','failure','current','parent','determine','missing','capability','knowledge','causing','task','find','verified','repair','path','required'};out=[]
 for x in raw:
  k=x.lower().strip('.,:;()[]{}')
  if k and k not in stop and k not in out:out.append(k)
 return out[:14]
def local_search(qs,limit=20):
 hits=[]
 for base in [KNOWLEDGE,LOCAL,HOME/'coordination'/'learning']:
  if not base.exists():continue
  for p in base.rglob('*'):
   if not p.is_file() or p.suffix.lower() not in {'.md','.json','.jsonl','.py','.js','.jsx','.ts','.tsx'}:continue
   try:text=p.read_text(encoding='utf-8',errors='replace')
   except Exception:continue
   low=text.lower();score=sum(1 for t in qs if t in low)
   if score:
    sample=next((line.strip()[:500] for line in text.splitlines() if any(t in line.lower() for t in qs)),'')
    try:path=str(p.relative_to(ROOT))
    except Exception:path=str(p)
    hits.append({'kind':'local','path':path,'score':score,'sample':sample})
 try:
  from failure_memory import find
  for row in find(' '.join(qs),8):hits.append({'kind':'failure-memory','score':20,'record':row})
 except Exception:pass
 return sorted(hits,key=lambda x:-int(x.get('score') or 0))[:limit]
def catalog_search(qs):
 out=[]
 for s in (read_json(CATALOG,{}) or {}).get('sources') or []:
  hay=' '.join([str(s.get('id','')),str(s.get('upstream','')),str(s.get('url',''))]+list(s.get('topics') or [])).lower();score=sum(1 for t in qs if t in hay)
  if score:out.append({**s,'score':score,'kind':'catalog-'+str(s.get('kind','source'))})
 return sorted(out,key=lambda x:-x['score'])
def external_search(qs):
 q=' '.join(qs[:6]) or 'agent research';probes=[];candidates=[]
 gh=shutil.which('gh')
 if gh:
  r=run([gh,'search','repos',q,'--limit','8','--json','fullName,url,description,updatedAt']);probes.append({'provider':'github-cli','result':r})
  if r.get('returncode')==0:
   try:
    for x in json.loads(r.get('stdout') or '[]'):candidates.append({'kind':'github-repository','source':'gh search repos','name':x.get('fullName'),'url':x.get('url'),'description':x.get('description'),'updated_at':x.get('updatedAt')})
   except Exception:pass
 else:probes.append({'provider':'github-cli','available':False,'reason':'gh_not_installed'})
 npm=shutil.which('npm')
 if npm and any(t in {'storybook','vite','jsx','npm','node','plugin','stories','stories.js'} for t in qs):
  r=run([npm,'search',q,'--json'],timeout=120);probes.append({'provider':'npm-search','result':r})
  if r.get('returncode')==0:
   try:
    for x in json.loads(r.get('stdout') or '[]')[:10]:candidates.append({'kind':'npm-package','source':'npm search','name':x.get('name'),'version':x.get('version'),'description':x.get('description'),'links':x.get('links')})
   except Exception:pass
 return candidates,probes
def peer_escalate(job,artifact):
 try:
  from coordination_mailbox import send_to_chatgpt
  rid=job['research_id'];body=json.dumps({'schema':'dore.peer-research-request.v1','research_id':rid,'parent_message_id':job.get('parent_message_id'),'parent_goal':job.get('parent_goal'),'question':job.get('question'),'failure_fingerprint':job.get('failure_fingerprint'),'self_research':artifact,'required_return_schema':'dore.knowledge-artifact.v1'},ensure_ascii=False);msg=send_to_chatgpt('Doré peer research: '+rid,body,requires_reply=True,priority='high',related_goal=job.get('parent_goal'),evidence_refs=['research-job:'+rid],message_id='peer-'+rid,metadata={'research_id':rid,'kind':'peer_research'});return {'queued':True,'message_id':msg.get('message_id'),'transport':'dore.mail.v2 -> GitHub coordination-outbox'}
 except Exception as e:return {'queued':False,'error':type(e).__name__+': '+str(e)}
def acceptance(job,artifact):
 cfg=job.get('acceptance') or {};minimum=int(cfg.get('minimum_qualified_references') or 0);minimum_families=int(cfg.get('minimum_source_families') or 0);sources=artifact.get('sources') or {};families=[k for k,v in sources.items() if isinstance(v,list) and v];count=int(artifact.get('evidence_count') or 0)
 return {'minimum_qualified_references':minimum,'current_qualified_references':count,'minimum_source_families':minimum_families,'current_source_families':len(families),'source_families':families,'met':count>=minimum and len(families)>=minimum_families}
def execute(job_path):
 p=Path(job_path);job=read_json(p,{}) or {}
 if not job.get('research_id'):return {'ok':False,'error':'invalid_research_job'}
 if job.get('state') in {'KNOWLEDGE_RETURNED','VERIFIED','PROMOTED','RESUME_PARENT'}:return {'ok':True,'state':job.get('state'),'job':job}
 transition(p,job,'RESEARCHING');qs=terms(str(job.get('question') or '')+' '+str(job.get('failure_fingerprint') or ''));local=local_search(qs);catalog=catalog_search(qs);external,probes=external_search(qs);artifact={'schema':'dore.knowledge-artifact.v1','knowledge_id':'knowledge-'+job['research_id'],'research_id':job['research_id'],'created_at':now(),'discovered_by':'dore-research-executor','query_terms':qs,'sources':{'local':local,'catalog':catalog,'external':external},'tool_probes':probes,'provenance_preserved':True,'reuse_before_rebuild':True,'parent_goal':job.get('parent_goal')};artifact['evidence_count']=len(local)+len(catalog)+len(external)
 gate=acceptance(job,artifact);artifact['acceptance']=gate
 if artifact['evidence_count'] and gate['met']:
  artifact.update({'lesson':'Relevant resources found. Derive a falsifiable hypothesis and verify it in the smallest parent-specific experiment before promotion.','hypothesis_status':'CANDIDATES_FOUND','experiment_required':True})
  try:
   from shared_learning import record
   artifact['shared_learning_candidate']=record(artifact,learned_by='dore',status='CANDIDATE',parent_goal=job.get('parent_goal'))
  except Exception as e:artifact['shared_learning_candidate']={'ok':False,'error':repr(e)}
  transition(p,job,'KNOWLEDGE_RETURNED',knowledge_artifact=artifact);return {'ok':True,'state':'KNOWLEDGE_RETURNED','research_id':job['research_id'],'knowledge_artifact':artifact}
 peer=peer_escalate(job,artifact);transition(p,job,'PEER_RESEARCH_QUEUED' if peer.get('queued') else 'RESEARCH_BLOCKED',peer_research=peer,knowledge_artifact=artifact);return {'ok':False,'state':job['state'],'research_id':job['research_id'],'peer_research':peer,'knowledge_artifact':artifact}
if __name__=='__main__':
 if len(sys.argv)!=2:print(json.dumps({'ok':False,'error':'usage: research_executor.py JOB.json'}));raise SystemExit(2)
 out=execute(sys.argv[1]);print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 3)
