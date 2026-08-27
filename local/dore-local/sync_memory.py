#!/usr/bin/env python3
import argparse,json,sqlite3,urllib.request,urllib.parse,urllib.error,hashlib,uuid,os,subprocess,shutil
from pathlib import Path
from datetime import datetime,timezone
HOME=Path.home()/'.dore'; DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'sync-state.json'; BROWSER_UA='Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/605.1.15 Version/18.0 Safari/605.1.15'
def load_state():
 try:return json.loads(STATE.read_text())
 except:return {'last_pull':None,'last_push':None,'imported':0,'pushed':0}
def save_state(s):STATE.write_text(json.dumps(s,indent=2))
def ensure(c):c.execute('CREATE TABLE IF NOT EXISTS dore_sync_log(remote_id TEXT PRIMARY KEY, direction TEXT, synced_at TEXT)')
def normalize(row,project):
 if not isinstance(row,dict):return None
 content=row.get('content') or row.get('text') or row.get('message')
 if isinstance(content,dict):content=content.get('text') or content.get('content') or json.dumps(content,ensure_ascii=False)
 if not content:return None
 return {'id':str(row.get('id') or row.get('message_id') or row.get('memory_id') or uuid.uuid4()),'conversation_id':str(row.get('conversation_id') or row.get('thread_id') or row.get('session_id') or 'cloud-import'),'project_id':str(row.get('project_id') or project or 'dore-global'),'role':str(row.get('role') or row.get('author') or 'user'),'content':str(content),'created_at':str(row.get('created_at') or row.get('timestamp') or row.get('source_created_at') or datetime.now(timezone.utc).isoformat()),'content_sha256':row.get('content_sha256'),'archive_key':row.get('archive_key'),'remote':row}
def put(row):
 with sqlite3.connect(DB) as c:
  ensure(c); rid=row['id']
  if c.execute('SELECT 1 FROM dore_sync_log WHERE remote_id=?',(rid,)).fetchone():return False
  cid=row['conversation_id']; project=row['project_id']; role=row['role']; content=row['content']; ts=row['created_at']; h=str(row.get('content_sha256') or hashlib.sha256(content.encode()).hexdigest()); key=str(row.get('archive_key') or f'cloud/{project}/{cid}/{rid}.json')
  c.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,project,'cloud-sync','SYNC',None,ts,ts)); c.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(rid,cid,project,'cloud-sync',role,content,h,key,ts)); c.execute('INSERT INTO dore_sync_log VALUES(?,?,?)',(rid,'cloud-to-local',datetime.now(timezone.utc).isoformat()))
  p=HOME/'archive'/key;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(row.get('remote') or row,ensure_ascii=False),encoding='utf-8');return True
def extract_rows(data):
 if isinstance(data,list):return data
 if not isinstance(data,dict):return []
 for k in ('messages','memories','items','results','data'):
  v=data.get(k)
  if isinstance(v,list):return v
  if isinstance(v,dict):
   for kk in ('messages','memories','items','results'):
    if isinstance(v.get(kk),list):return v[kk]
 return []
def req_json(url,headers,method='GET',payload=None):
 data=None if payload is None else json.dumps(payload,ensure_ascii=False).encode()
 req=urllib.request.Request(url,data=data,headers=headers,method=method)
 try:return json.loads(urllib.request.urlopen(req,timeout=60).read())
 except urllib.error.HTTPError as e:
  detail=e.read().decode('utf-8','replace'); raise RuntimeError(f'HTTP {e.code}: {detail[:500]}')
def fetch_cloud(base,q,headers):
 last=None
 for path in ('/api/dore/memory','/v1/memory'):
  url=base.rstrip('/')+path+'?'+urllib.parse.urlencode(q)
  try:return path,url,req_json(url,headers)
  except Exception as e:last=str(e)
 raise RuntimeError(last or 'no_supported_endpoint')
def pull(base,project,conversation=None,limit=80,token=None):
 q={'project_id':project,'limit':str(limit)}
 if conversation:q['conversation_id']=conversation
 headers={'Accept':'application/json','User-Agent':BROWSER_UA}
 if token:headers['Authorization']='Bearer '+token
 endpoint,url,data=fetch_cloud(base,q,headers); rows=extract_rows(data); normalized=[x for x in (normalize(r,project) for r in rows) if x]; n=sum(put(x) for x in normalized); s=load_state();s['last_pull']=datetime.now(timezone.utc).isoformat();s['last_endpoint']=url;s['imported']=s.get('imported',0)+n;save_state(s);return {'ok':True,'direction':'cloud-to-local','endpoint':endpoint,'received':len(rows),'normalized':len(normalized),'imported':n,'workers_ai_used':False}
def local_unsynced(project,limit=100):
 with sqlite3.connect(DB) as c:
  ensure(c);c.row_factory=sqlite3.Row
  rows=c.execute("SELECT m.* FROM dore_messages m LEFT JOIN dore_sync_log s ON s.remote_id=m.id AND s.direction='local-to-cloud' WHERE m.project_id=? AND (s.remote_id IS NULL) AND m.actor_id<>'cloud-sync' ORDER BY m.created_at ASC LIMIT ?",(project,limit)).fetchall();return [dict(r) for r in rows]
def push(base,project,token,limit=100):
 if not token:raise RuntimeError('DORE_CLOUD_SYNC_TOKEN required')
 rows=local_unsynced(project,limit)
 if not rows:return {'ok':True,'direction':'local-to-cloud','selected':0,'inserted':0,'deduplicated':0,'conflicts':0,'workers_ai_used':False}
 url=base.rstrip('/')+'/api/dore/sync-memory'; headers={'Accept':'application/json','Content-Type':'application/json','Authorization':'Bearer '+token,'User-Agent':BROWSER_UA}; out=req_json(url,headers,'POST',{'messages':rows})
 with sqlite3.connect(DB) as c:
  ensure(c)
  for d in out.get('details',[]):
   if d.get('status') in ('inserted','deduplicated','conflict'):c.execute('INSERT OR REPLACE INTO dore_sync_log VALUES(?,?,?)',(d.get('id'),'local-to-cloud',datetime.now(timezone.utc).isoformat()))
 s=load_state();s['last_push']=datetime.now(timezone.utc).isoformat();s['pushed']=s.get('pushed',0)+int(out.get('inserted',0));save_state(s);return {'ok':bool(out.get('ok')),'direction':'local-to-cloud','selected':len(rows),'inserted':out.get('inserted',0),'deduplicated':out.get('deduplicated',0),'conflicts':out.get('conflicts',0),'failed':out.get('failed',0),'conflict_policy':out.get('conflict_policy'),'workers_ai_used':False}
def import_jsonl(path):
 n=0;total=0
 for line in Path(path).read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  total+=1
  try:
   raw=json.loads(line);row=normalize(raw,raw.get('project_id','dore-global') if isinstance(raw,dict) else 'dore-global');n+=1 if row and put(row) else 0
  except Exception as e:print('skip',total,e)
 return {'ok':True,'source':str(path),'records':total,'imported':n,'workers_ai_used':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cloud');p.add_argument('--project',default='dore-global');p.add_argument('--conversation');p.add_argument('--jsonl');p.add_argument('--token',default=os.environ.get('DORE_CLOUD_SYNC_TOKEN'));p.add_argument('--push',action='store_true');p.add_argument('--both',action='store_true');a=p.parse_args()
 try:
  if a.jsonl:out=import_jsonl(a.jsonl)
  elif a.both:out={'pull':pull(a.cloud,a.project,a.conversation,token=a.token),'push':push(a.cloud,a.project,a.token),'workers_ai_used':False}
  elif a.push:out=push(a.cloud,a.project,a.token)
  elif a.cloud:out=pull(a.cloud,a.project,a.conversation,token=a.token)
  else:p.error('use --cloud, --push, --both or --jsonl')
  print(json.dumps(out,ensure_ascii=False))
 except Exception as e:print(json.dumps({'ok':False,'error':str(e),'workers_ai_used':False},ensure_ascii=False));raise SystemExit(1)
