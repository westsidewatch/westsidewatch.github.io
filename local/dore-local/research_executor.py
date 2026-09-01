#!/usr/bin/env python3
"""Doré Research Executor v0.1.

Turns a durable RESEARCH_QUEUED job into actual resource discovery. It never
pretends research happened: every source/candidate is recorded with provenance,
and insufficient evidence escalates through the durable Doré->ChatGPT mailbox
rather than retrying the parent task.
"""
from __future__ import annotations
import json, os, re, shutil, subprocess, sys
from datetime import datetime, timezone
from pathlib import Path

HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
RESEARCH=HOME/'coordination'/'research'
KNOWLEDGE=ROOT/'dore-design'/'knowledge-lab'
CATALOG=KNOWLEDGE/'resources'/'source-catalog.json'


def now(): return datetime.now(timezone.utc).isoformat()
def read_json(p,default=None):
    try:return json.loads(Path(p).read_text(encoding='utf-8'))
    except Exception:return default

def atomic_json(p,v):
    p=Path(p);p.parent.mkdir(parents=True,exist_ok=True);t=p.with_suffix(p.suffix+'.tmp');t.write_text(json.dumps(v,ensure_ascii=False,indent=2),encoding='utf-8');t.replace(p)
def run(argv,cwd=ROOT,timeout=60):
    try:
        cp=subprocess.run(argv,cwd=str(cwd),text=True,capture_output=True,timeout=timeout)
        return {'available':True,'argv':argv,'returncode':cp.returncode,'stdout':(cp.stdout or '')[-16000:],'stderr':(cp.stderr or '')[-8000:]}
    except FileNotFoundError:return {'available':False,'argv':argv,'returncode':127,'error':'tool_not_found:'+argv[0]}
    except Exception as e:return {'available':True,'argv':argv,'returncode':126,'error':type(e).__name__+': '+str(e)}
def terms(text):
    raw=re.findall(r'[A-Za-z0-9@._:/+-]{3,}',text or '')
    stop={'error','failed','failure','current','parent','determine','missing','capability','knowledge','causing','task','find','verified','repair','path','required'}
    out=[]
    for x in raw:
        k=x.lower().strip('.,:;()[]{}')
        if k and k not in stop and k not in out:out.append(k)
    return out[:12]
def local_search(query_terms,limit=16):
    hits=[]
    roots=[KNOWLEDGE,ROOT/'local'/'dore-local']
    for base in roots:
        if not base.exists():continue
        for p in base.rglob('*'):
            if not p.is_file() or p.suffix.lower() not in {'.md','.json','.py','.js','.jsx','.ts','.tsx'}:continue
            try:text=p.read_text(encoding='utf-8',errors='replace')
            except Exception:continue
            low=text.lower();score=sum(1 for t in query_terms if t in low)
            if score:
                lines=text.splitlines();sample=''
                for line in lines:
                    if any(t in line.lower() for t in query_terms):sample=line.strip()[:500];break
                hits.append({'kind':'local','path':str(p.relative_to(ROOT)),'score':score,'sample':sample})
    return sorted(hits,key=lambda x:(-x['score'],x['path']))[:limit]
def catalog_search(query_terms):
    data=read_json(CATALOG,{}) or {};out=[]
    for s in data.get('sources') or []:
        hay=' '.join([str(s.get('id','')),str(s.get('upstream',''))]+list(s.get('topics') or [])).lower()
        score=sum(1 for t in query_terms if t in hay)
        if score:out.append({**s,'score':score,'kind':'catalog-'+str(s.get('kind','source'))})
    return sorted(out,key=lambda x:-x['score'])
def external_search(query_terms):
    """Use real locally available public-resource clients; record absence/failure."""
    q=' '.join(query_terms[:6]) or 'agent research'
    probes=[];candidates=[]
    gh=shutil.which('gh')
    if gh:
        r=run([gh,'search','repos',q,'--limit','8','--json','fullName,url,description,updatedAt'],timeout=90);probes.append({'provider':'github-cli','result':r})
        if r.get('returncode')==0:
            try:
                for x in json.loads(r.get('stdout') or '[]'):candidates.append({'kind':'github-repository','source':'gh search repos','name':x.get('fullName'),'url':x.get('url'),'description':x.get('description'),'updated_at':x.get('updatedAt')})
            except Exception:pass
    else:probes.append({'provider':'github-cli','available':False,'reason':'gh_not_installed'})
    npm=shutil.which('npm')
    if npm and any(t in {'storybook','vite','jsx','npm','node','plugin','stories'} for t in query_terms):
        r=run([npm,'search',q,'--json'],timeout=120);probes.append({'provider':'npm-search','result':r})
        if r.get('returncode')==0:
            try:
                for x in json.loads(r.get('stdout') or '[]')[:10]:candidates.append({'kind':'npm-package','source':'npm search','name':x.get('name'),'version':x.get('version'),'description':x.get('description'),'links':x.get('links')})
            except Exception:pass
    return candidates,probes
def peer_escalate(job,artifact):
    """Publish a real durable peer-research request through the existing mailbox."""
    try:
        sys.path.insert(0,str(ROOT/'local'/'dore-local'))
        from coordination_mailbox import send_to_chatgpt
        rid=job['research_id'];body=json.dumps({'schema':'dore.peer-research-request.v1','research_id':rid,'parent_message_id':job.get('parent_message_id'),'parent_goal':job.get('parent_goal'),'question':job.get('question'),'failure_fingerprint':job.get('failure_fingerprint'),'self_research':artifact,'required_return_schema':'dore.knowledge-artifact.v1'},ensure_ascii=False)
        msg=send_to_chatgpt('Doré peer research: '+rid,body,requires_reply=True,priority='high',related_goal=job.get('parent_goal'),evidence_refs=['research-job:'+rid],message_id='peer-'+rid,metadata={'research_id':rid,'kind':'peer_research'})
        return {'queued':True,'message_id':msg.get('message_id'),'transport':'dore.mail.v2 -> GitHub coordination-outbox'}
    except Exception as e:return {'queued':False,'error':type(e).__name__+': '+str(e)}
def execute(job_path):
    p=Path(job_path);job=read_json(p,{}) or {}
    if not job.get('research_id'):return {'ok':False,'error':'invalid_research_job'}
    if job.get('state') in {'KNOWLEDGE_RETURNED','VERIFIED','PROMOTED','RESUME_PARENT'}:return {'ok':True,'state':job.get('state'),'job':job}
    job['state']='RESEARCHING';job['updated_at']=now();atomic_json(p,job)
    text=' '.join([str(job.get('question') or ''),str(job.get('failure_fingerprint') or '')]);qs=terms(text)
    local=local_search(qs);catalog=catalog_search(qs);external,probes=external_search(qs)
    artifact={'schema':'dore.knowledge-artifact.v1','knowledge_id':'knowledge-'+job['research_id'],'research_id':job['research_id'],'created_at':now(),'query_terms':qs,'sources':{'local':local,'catalog':catalog,'external':external},'tool_probes':probes,'provenance_preserved':True,'reuse_before_rebuild':True}
    evidence_count=len(local)+len(catalog)+len(external)
    artifact['evidence_count']=evidence_count
    # Research discovery alone is not verification. It becomes KNOWLEDGE_RETURNED only
    # when there is at least one task-relevant source; the Driver must still experiment.
    if evidence_count:
        artifact['lesson']='Relevant prior knowledge/resources were found. Form a falsifiable hypothesis from these sources and run the parent-specific minimal experiment before promotion.'
        artifact['hypothesis_status']='CANDIDATES_FOUND'
        artifact['experiment_required']=True
        job['state']='KNOWLEDGE_RETURNED';job['knowledge_artifact']=artifact;job['updated_at']=now();atomic_json(p,job)
        return {'ok':True,'state':'KNOWLEDGE_RETURNED','research_id':job['research_id'],'knowledge_artifact':artifact}
    peer=peer_escalate(job,artifact);job['peer_research']=peer;job['knowledge_artifact']=artifact;job['state']='PEER_RESEARCH_QUEUED' if peer.get('queued') else 'RESEARCH_BLOCKED';job['updated_at']=now();atomic_json(p,job)
    return {'ok':False,'state':job['state'],'research_id':job['research_id'],'peer_research':peer,'knowledge_artifact':artifact}

if __name__=='__main__':
    if len(sys.argv)!=2:print(json.dumps({'ok':False,'error':'usage: research_executor.py JOB.json'}));raise SystemExit(2)
    out=execute(sys.argv[1]);print(json.dumps(out,ensure_ascii=False));raise SystemExit(0 if out.get('ok') else 3)
