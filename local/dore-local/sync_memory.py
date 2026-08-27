#!/usr/bin/env python3
import argparse,json,sqlite3,urllib.request,urllib.parse,urllib.error,hashlib,uuid,os
from pathlib import Path
from datetime import datetime,timezone
HOME=Path.home()/'.dore'; DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'sync-state.json'
def load_state():
 try:return json.loads(STATE.read_text())
 except:return {'last_pull':None,'imported':0}
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
def fetch_cloud(base,q,headers):
 tested=[]
 for path in ('/api/dore/memory','/v1/memory'):
  url=base.rstrip('/')+path+'?'+urllib.parse.urlencode(q); tested.append(url)
  try:return path,url,json.loads(urllib.request.urlopen(urllib.request.Request(url,headers=headers),timeout=60).read())
  except urllib.error.HTTPError as e:
   if e.code==404:continue
   detail=e.read().decode('utf-8','replace');raise SystemExit(json.dumps({'ok':False,'stage':'cloud_fetch','status':e.code,'url':url,'detail':detail[:1000],'workers_ai_used':False},ensure_ascii=False))
  except urllib.error.URLError as e:raise SystemExit(json.dumps({'ok':False,'stage':'cloud_fetch','url':url,'detail':str(e),'workers_ai_used':False},ensure_ascii=False))
 raise SystemExit(json.dumps({'ok':False,'stage':'cloud_fetch','status':404,'tested':tested,'detail':'No supported memory endpoint found','workers_ai_used':False},ensure_ascii=False))
def pull(base,project,conversation=None,limit=80,token=None):
 q={'project_id':project,'limit':str(limit)}
 if conversation:q['conversation_id']=conversation
 headers={'Accept':'application/json'}
 if token:headers['Authorization']='Bearer '+token
 endpoint,url,data=fetch_cloud(base,q,headers); rows=extract_rows(data); normalized=[x for x in (normalize(r,project) for r in rows) if x]; n=sum(put(x) for x in normalized); s=load_state();s['last_pull']=datetime.now(timezone.utc).isoformat();s['last_endpoint']=url;s['imported']=s.get('imported',0)+n;save_state(s);print(json.dumps({'ok':True,'direction':'cloud-to-local','endpoint':endpoint,'received':len(rows),'normalized':len(normalized),'imported':n,'workers_ai_used':False},ensure_ascii=False))
def import_jsonl(path):
 n=0;total=0
 for line in Path(path).read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  total+=1
  try:
   raw=json.loads(line);row=normalize(raw,raw.get('project_id','dore-global') if isinstance(raw,dict) else 'dore-global');n+=1 if row and put(row) else 0
  except Exception as e:print('skip',total,e)
 print(json.dumps({'ok':True,'source':str(path),'records':total,'imported':n,'workers_ai_used':False},ensure_ascii=False))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cloud');p.add_argument('--project',default='dore-global');p.add_argument('--conversation');p.add_argument('--jsonl');p.add_argument('--token',default=os.environ.get('DORE_CLOUD_SYNC_TOKEN'));a=p.parse_args()
 if a.jsonl:import_jsonl(a.jsonl)
 elif a.cloud:pull(a.cloud,a.project,a.conversation,token=a.token)
 else:p.error('use --cloud or --jsonl')
