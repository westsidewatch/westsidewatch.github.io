#!/usr/bin/env python3
import argparse,json,sqlite3,urllib.request,urllib.parse,hashlib,uuid
from pathlib import Path
from datetime import datetime,timezone
HOME=Path.home()/'.dore'; DB=HOME/'data'/'dore.sqlite3'; STATE=HOME/'sync-state.json'
def load_state():
 try:return json.loads(STATE.read_text())
 except:return {'last_pull':None,'imported':0}
def save_state(s):STATE.write_text(json.dumps(s,indent=2))
def ensure(c):
 c.execute('CREATE TABLE IF NOT EXISTS dore_sync_log(remote_id TEXT PRIMARY KEY, direction TEXT, synced_at TEXT)')
def put(row):
 with sqlite3.connect(DB) as c:
  ensure(c); rid=str(row.get('id') or row.get('message_id') or uuid.uuid4());
  if c.execute('SELECT 1 FROM dore_sync_log WHERE remote_id=?',(rid,)).fetchone():return False
  cid=str(row.get('conversation_id') or 'cloud-import'); project=str(row.get('project_id') or 'dore-global'); role=str(row.get('role') or 'user'); content=str(row.get('content') or ''); ts=str(row.get('created_at') or datetime.now(timezone.utc).isoformat()); h=str(row.get('content_sha256') or hashlib.sha256(content.encode()).hexdigest()); key=str(row.get('archive_key') or f'cloud/{project}/{cid}/{rid}.json')
  c.execute('INSERT OR IGNORE INTO dore_conversations(id,project_id,actor_id,mode,title,created_at,updated_at) VALUES(?,?,?,?,?,?,?)',(cid,project,'cloud-sync','SYNC',None,ts,ts)); c.execute('INSERT OR IGNORE INTO dore_messages(id,conversation_id,project_id,actor_id,role,content,content_sha256,archive_key,created_at) VALUES(?,?,?,?,?,?,?,?,?)',(rid,cid,project,'cloud-sync',role,content,h,key,ts)); c.execute('INSERT INTO dore_sync_log VALUES(?,?,?)',(rid,'cloud-to-local',datetime.now(timezone.utc).isoformat()))
  p=HOME/'archive'/key;p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(row,ensure_ascii=False),encoding='utf-8');return True
def pull(base,project,conversation=None,limit=80):
 q={'project_id':project,'limit':str(limit)}
 if conversation:q['conversation_id']=conversation
 url=base.rstrip('/')+'/api/dore/memory?'+urllib.parse.urlencode(q); req=urllib.request.Request(url,headers={'Accept':'application/json'}); data=json.loads(urllib.request.urlopen(req,timeout=60).read()); rows=data.get('messages',[]); n=sum(put(x) for x in rows); s=load_state();s['last_pull']=datetime.now(timezone.utc).isoformat();s['imported']=s.get('imported',0)+n;save_state(s);print(json.dumps({'ok':True,'direction':'cloud-to-local','received':len(rows),'imported':n,'workers_ai_used':False}))
def import_jsonl(path):
 n=0; total=0
 for line in Path(path).read_text(encoding='utf-8').splitlines():
  if not line.strip():continue
  total+=1
  try:n+=1 if put(json.loads(line)) else 0
  except Exception as e:print('skip',total,e)
 print(json.dumps({'ok':True,'source':str(path),'records':total,'imported':n,'workers_ai_used':False}))
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--cloud');p.add_argument('--project',default='dore-global');p.add_argument('--conversation');p.add_argument('--jsonl');a=p.parse_args()
 if a.jsonl:import_jsonl(a.jsonl)
 elif a.cloud:pull(a.cloud,a.project,a.conversation)
 else:p.error('use --cloud or --jsonl')
