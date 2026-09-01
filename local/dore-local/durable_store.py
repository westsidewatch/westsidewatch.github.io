#!/usr/bin/env python3
"""Doré local durable state store.

SQLite WAL-backed checkpoints, event journal, idempotency records and execution
leases. Stdlib-only and local-first. This complements human-readable JSON/Git
telemetry; it does not replace A2A or the mailbox transport.
"""
from __future__ import annotations
import hashlib,json,os,sqlite3,time,uuid
from contextlib import contextmanager
from datetime import datetime,timezone
from pathlib import Path
HOME=Path(os.environ.get('DORE_LOCAL_HOME',Path.home()/'.dore')).expanduser();DB=HOME/'runtime'/'dore-loop.sqlite3'

def now():return datetime.now(timezone.utc).isoformat()
def fingerprint(v):return hashlib.sha256(json.dumps(v,ensure_ascii=False,sort_keys=True,default=str).encode()).hexdigest()
def connect():
 DB.parent.mkdir(parents=True,exist_ok=True);c=sqlite3.connect(str(DB),timeout=15,isolation_level=None);c.row_factory=sqlite3.Row
 c.execute('PRAGMA journal_mode=WAL');c.execute('PRAGMA synchronous=FULL');c.execute('PRAGMA foreign_keys=ON');c.execute('PRAGMA busy_timeout=15000');init(c);return c
def init(c):
 c.executescript('''CREATE TABLE IF NOT EXISTS checkpoints(scope TEXT NOT NULL,key TEXT NOT NULL,value_json TEXT NOT NULL,version INTEGER NOT NULL DEFAULT 1,updated_at TEXT NOT NULL,PRIMARY KEY(scope,key));
CREATE TABLE IF NOT EXISTS events(id INTEGER PRIMARY KEY AUTOINCREMENT,event_id TEXT NOT NULL UNIQUE,trace_id TEXT NOT NULL,span_id TEXT NOT NULL,parent_span_id TEXT,category TEXT NOT NULL,state TEXT,goal_id TEXT,fingerprint TEXT,payload_json TEXT NOT NULL,created_at TEXT NOT NULL);
CREATE INDEX IF NOT EXISTS idx_events_goal ON events(goal_id,id);CREATE INDEX IF NOT EXISTS idx_events_trace ON events(trace_id,id);
CREATE TABLE IF NOT EXISTS idempotency(idempotency_key TEXT PRIMARY KEY,status TEXT NOT NULL,result_json TEXT,updated_at TEXT NOT NULL);
CREATE TABLE IF NOT EXISTS leases(resource TEXT PRIMARY KEY,owner TEXT NOT NULL,lease_until REAL NOT NULL,updated_at TEXT NOT NULL);''')
@contextmanager
def tx():
 c=connect();c.execute('BEGIN IMMEDIATE')
 try:yield c;c.execute('COMMIT')
 except Exception:c.execute('ROLLBACK');raise
 finally:c.close()
def checkpoint_put(scope,key,value):
 raw=json.dumps(value,ensure_ascii=False,sort_keys=True,default=str)
 with tx() as c:c.execute('INSERT INTO checkpoints(scope,key,value_json,version,updated_at) VALUES(?,?,?,?,?) ON CONFLICT(scope,key) DO UPDATE SET value_json=excluded.value_json,version=checkpoints.version+1,updated_at=excluded.updated_at',(scope,key,raw,1,now()))
 return {'ok':True,'scope':scope,'key':key}
def checkpoint_get(scope,key,default=None):
 c=connect();r=c.execute('SELECT value_json,version,updated_at FROM checkpoints WHERE scope=? AND key=?',(scope,key)).fetchone();c.close()
 if not r:return default
 try:v=json.loads(r['value_json'])
 except Exception:v=default
 return {'value':v,'version':r['version'],'updated_at':r['updated_at']}
def append_event(category,*,state=None,goal_id=None,payload=None,trace_id=None,span_id=None,parent_span_id=None,event_id=None):
 trace_id=trace_id or uuid.uuid4().hex;span_id=span_id or uuid.uuid4().hex[:16];event_id=event_id or str(uuid.uuid4());payload=payload or {};fp=fingerprint({'category':category,'state':state,'goal_id':goal_id,'payload':payload})
 with tx() as c:c.execute('INSERT OR IGNORE INTO events(event_id,trace_id,span_id,parent_span_id,category,state,goal_id,fingerprint,payload_json,created_at) VALUES(?,?,?,?,?,?,?,?,?,?)',(event_id,trace_id,span_id,parent_span_id,category,state,goal_id,fp,json.dumps(payload,ensure_ascii=False,sort_keys=True,default=str),now()))
 return {'event_id':event_id,'trace_id':trace_id,'span_id':span_id,'fingerprint':fp}
def recent_events(goal_id=None,limit=50):
 c=connect();rows=c.execute('SELECT * FROM events WHERE goal_id=? ORDER BY id DESC LIMIT ?',(goal_id,limit)).fetchall() if goal_id else c.execute('SELECT * FROM events ORDER BY id DESC LIMIT ?',(limit,)).fetchall();c.close();return [dict(r) for r in reversed(rows)]
def idempotency_begin(key):
 with tx() as c:
  r=c.execute('SELECT status,result_json FROM idempotency WHERE idempotency_key=?',(key,)).fetchone()
  if r:return {'acquired':False,'status':r['status'],'result':json.loads(r['result_json']) if r['result_json'] else None}
  c.execute('INSERT INTO idempotency(idempotency_key,status,updated_at) VALUES(?,?,?)',(key,'RUNNING',now()))
 return {'acquired':True,'status':'RUNNING'}
def idempotency_finish(key,status,result=None):
 with tx() as c:c.execute('INSERT INTO idempotency(idempotency_key,status,result_json,updated_at) VALUES(?,?,?,?) ON CONFLICT(idempotency_key) DO UPDATE SET status=excluded.status,result_json=excluded.result_json,updated_at=excluded.updated_at',(key,status,json.dumps(result,ensure_ascii=False,sort_keys=True,default=str) if result is not None else None,now()))
 return {'ok':True,'key':key,'status':status}
def acquire_lease(resource,owner=None,ttl=90):
 owner=owner or f'pid-{os.getpid()}-{uuid.uuid4().hex[:8]}';t=time.time()
 with tx() as c:
  r=c.execute('SELECT owner,lease_until FROM leases WHERE resource=?',(resource,)).fetchone()
  if r and float(r['lease_until'])>t and r['owner']!=owner:return {'acquired':False,'owner':r['owner'],'lease_until':r['lease_until']}
  c.execute('INSERT INTO leases(resource,owner,lease_until,updated_at) VALUES(?,?,?,?) ON CONFLICT(resource) DO UPDATE SET owner=excluded.owner,lease_until=excluded.lease_until,updated_at=excluded.updated_at',(resource,owner,t+ttl,now()))
 return {'acquired':True,'owner':owner,'lease_until':t+ttl}
def release_lease(resource,owner):
 with tx() as c:c.execute('DELETE FROM leases WHERE resource=? AND owner=?',(resource,owner))
 return {'ok':True}
def health():
 c=connect();mode=c.execute('PRAGMA journal_mode').fetchone()[0];counts={t:c.execute(f'SELECT count(*) FROM {t}').fetchone()[0] for t in ['checkpoints','events','idempotency','leases']};c.close();return {'ok':mode.lower()=='wal','schema':'dore.durable-store.v1','db':str(DB),'journal_mode':mode,'counts':counts}
if __name__=='__main__':print(json.dumps(health(),ensure_ascii=False))
