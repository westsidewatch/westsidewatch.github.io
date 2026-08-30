#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, os, sqlite3, urllib.parse, urllib.request
from datetime import datetime, timezone
from pathlib import Path

ROOT=Path(os.environ.get('DORE_REPO_ROOT',Path.home()/'westsidewatch.github.io')).expanduser()
DORE=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser()
DB=DORE/'data'/'dore.sqlite3'; STATE=DORE/'data'/'resource-discovery-state.json'; LOG=DORE/'logs'/'resource-discovery.jsonl'
API='https://api.github.com'
QUERIES=[
 ('agent-orchestration','AI agent orchestration MCP stars:>50 archived:false'),
 ('code-intelligence','codebase knowledge graph MCP code intelligence stars:>30 archived:false'),
 ('agent-web-research','AI agent web research browser search CLI stars:>50 archived:false'),
 ('bible-research','Bible scripture open source dataset search theology stars:>20 archived:false'),
 ('design-media','agent design video media automation open source stars:>30 archived:false'),
]
COST_UNKNOWN='COST_UNKNOWN'
FREE_VERIFIED='FREE_VERIFIED'
FREE_PATH_AVAILABLE='FREE_PATH_AVAILABLE'
PAID_DEPENDENCY='PAID_DEPENDENCY'
COST_PASS={FREE_VERIFIED,FREE_PATH_AVAILABLE}

def now(): return datetime.now(timezone.utc).isoformat()
def emit(event,**extra):
 LOG.parent.mkdir(parents=True,exist_ok=True)
 with LOG.open('a',encoding='utf-8') as f:f.write(json.dumps({'ts':now(),'event':event,**extra},ensure_ascii=False)+'\n')
def ensure_schema(c):
 c.executescript('''
 CREATE TABLE IF NOT EXISTS dore_resource_candidates(
  id TEXT PRIMARY KEY, canonical_url TEXT NOT NULL UNIQUE, name TEXT NOT NULL, source TEXT NOT NULL,
  capability_family TEXT NOT NULL, description TEXT, discovered_at TEXT NOT NULL, last_seen_at TEXT NOT NULL,
  source_updated_at TEXT, stars INTEGER, license_spdx TEXT, archived INTEGER NOT NULL DEFAULT 0,
  status TEXT NOT NULL DEFAULT 'candidate', evidence_json TEXT NOT NULL,
  cost_verdict TEXT NOT NULL DEFAULT 'COST_UNKNOWN', free_only_eligible INTEGER NOT NULL DEFAULT 0);
 CREATE INDEX IF NOT EXISTS idx_resource_family ON dore_resource_candidates(capability_family,status,last_seen_at DESC);
 CREATE TABLE IF NOT EXISTS dore_resource_discovery_runs(
  id TEXT PRIMARY KEY, started_at TEXT NOT NULL, finished_at TEXT, query_count INTEGER NOT NULL,
  candidate_count INTEGER NOT NULL DEFAULT 0, new_count INTEGER NOT NULL DEFAULT 0, status TEXT NOT NULL, evidence_json TEXT);
 ''')
 cols={r[1] for r in c.execute('PRAGMA table_info(dore_resource_candidates)')}
 if 'cost_verdict' not in cols:c.execute("ALTER TABLE dore_resource_candidates ADD COLUMN cost_verdict TEXT NOT NULL DEFAULT 'COST_UNKNOWN'")
 if 'free_only_eligible' not in cols:c.execute('ALTER TABLE dore_resource_candidates ADD COLUMN free_only_eligible INTEGER NOT NULL DEFAULT 0')
 c.commit()
def headers():
 h={'Accept':'application/vnd.github+json','User-Agent':'Dore-Resource-Discovery/1.1'}
 token=os.environ.get('GITHUB_TOKEN') or os.environ.get('GH_TOKEN')
 if token:h['Authorization']='Bearer '+token
 return h
def get_json(url):
 req=urllib.request.Request(url,headers=headers())
 with urllib.request.urlopen(req,timeout=30) as r:return json.loads(r.read())
def rid(url):return 'resource_'+hashlib.sha256(url.encode()).hexdigest()[:20]
def run_id():return 'resource-run_'+hashlib.sha256((now()+str(os.getpid())).encode()).hexdigest()[:20]
def upsert(c,family,item):
 url=str(item.get('html_url') or '')
 if not url:return False
 existed=c.execute('SELECT 1 FROM dore_resource_candidates WHERE canonical_url=?',(url,)).fetchone() is not None
 lic=item.get('license') or {}
 evidence={'github_id':item.get('id'),'full_name':item.get('full_name'),'default_branch':item.get('default_branch'),'fork':item.get('fork'),'open_issues_count':item.get('open_issues_count'),'topics':item.get('topics') or [],'language':item.get('language'),'homepage':item.get('homepage'),'cost_policy':'Discovery does not imply free-to-run. Candidate remains blocked until intended execution path is verified free-only.'}
 c.execute('''INSERT INTO dore_resource_candidates(id,canonical_url,name,source,capability_family,description,discovered_at,last_seen_at,source_updated_at,stars,license_spdx,archived,status,evidence_json,cost_verdict,free_only_eligible)
 VALUES(?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(canonical_url) DO UPDATE SET name=excluded.name,capability_family=excluded.capability_family,description=excluded.description,last_seen_at=excluded.last_seen_at,source_updated_at=excluded.source_updated_at,stars=excluded.stars,license_spdx=excluded.license_spdx,archived=excluded.archived,evidence_json=excluded.evidence_json''',
 (rid(url),url,str(item.get('full_name') or item.get('name') or url),'github',family,item.get('description'),now(),now(),item.get('updated_at'),int(item.get('stargazers_count') or 0),lic.get('spdx_id'),1 if item.get('archived') else 0,'candidate',json.dumps(evidence,ensure_ascii=False),COST_UNKNOWN,0))
 return not existed
def main():
 DORE.joinpath('data').mkdir(parents=True,exist_ok=True); run=run_id(); started=now(); total=new=0; errors=[]
 try:
  c=sqlite3.connect(DB); c.row_factory=sqlite3.Row; ensure_schema(c); c.execute('INSERT INTO dore_resource_discovery_runs(id,started_at,query_count,status) VALUES(?,?,?,?)',(run,started,len(QUERIES),'running')); c.commit()
  for family,q in QUERIES:
   try:
    url=API+'/search/repositories?'+urllib.parse.urlencode({'q':q,'sort':'updated','order':'desc','per_page':10})
    payload=get_json(url); items=payload.get('items') or []
    for item in items:
     if item.get('archived') or item.get('fork'):continue
     total+=1; new+=1 if upsert(c,family,item) else 0
    c.commit(); emit('query',family=family,count=len(items))
   except Exception as e:errors.append({'family':family,'error':type(e).__name__+':'+str(e)});emit('query_error',family=family,detail=errors[-1]['error'])
  status='ok' if not errors else ('partial' if total else 'error'); finished=now(); evidence={'queries':[{'family':f,'query':q} for f,q in QUERIES],'errors':errors,'policy':'candidate-only; no auto-install; revalidate-before-use; free-only hard gate','cost_gate':'Every new candidate starts COST_UNKNOWN and free_only_eligible=0. Adoption requires FREE_VERIFIED or a verified FREE_PATH_AVAILABLE integration path.'}
  c.execute('UPDATE dore_resource_discovery_runs SET finished_at=?,candidate_count=?,new_count=?,status=?,evidence_json=? WHERE id=?',(finished,total,new,status,json.dumps(evidence,ensure_ascii=False),run));c.commit()
  blocked=c.execute("SELECT COUNT(*) FROM dore_resource_candidates WHERE cost_verdict NOT IN ('FREE_VERIFIED','FREE_PATH_AVAILABLE') OR free_only_eligible=0").fetchone()[0]
  state={'ok':status!='error','run_id':run,'checked_at':finished,'candidate_count':total,'new_count':new,'cost_blocked_candidates':blocked,'errors':errors,'policy':'Discover continuously. Revalidate before use. Reuse when better. Build only when necessary. Zero incremental paid dependencies.'};STATE.write_text(json.dumps(state,ensure_ascii=False,indent=2),encoding='utf-8');emit('complete',**state);return 0 if status!='error' else 1
 except Exception as e:
  STATE.write_text(json.dumps({'ok':False,'run_id':run,'checked_at':now(),'error':type(e).__name__+':'+str(e)},ensure_ascii=False,indent=2),encoding='utf-8');emit('error',detail=type(e).__name__+':'+str(e));return 1
if __name__=='__main__':raise SystemExit(main())
