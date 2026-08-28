#!/usr/bin/env python3
from __future__ import annotations
import hashlib, json, sqlite3
from datetime import datetime, timezone

STATES={'inherited','observed','verified','corrected','rejected'}

def now(): return datetime.now(timezone.utc).isoformat()
def _id(prefix,*parts): return prefix+'_'+hashlib.sha256('|'.join(parts).encode()).hexdigest()[:20]

def ensure_schema(conn: sqlite3.Connection):
    conn.executescript('''
    CREATE TABLE IF NOT EXISTS dore_self_memory(
      key TEXT PRIMARY KEY, content TEXT NOT NULL, source_type TEXT NOT NULL,
      source_ref TEXT, epistemic_state TEXT NOT NULL, updated_at TEXT NOT NULL);
    CREATE TABLE IF NOT EXISTS dore_learning_events(
      id TEXT PRIMARY KEY, domain TEXT NOT NULL, stage TEXT, claim TEXT NOT NULL,
      assessment TEXT, status TEXT NOT NULL, evidence_ref TEXT, source_type TEXT NOT NULL,
      epistemic_state TEXT NOT NULL, created_at TEXT NOT NULL, updated_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_dore_learning_domain ON dore_learning_events(domain,epistemic_state,status);
    ''')
    conn.commit()

def upsert_self(conn,key,content,source_type='runtime',source_ref=None,epistemic_state='observed'):
    if epistemic_state not in STATES: raise ValueError('invalid epistemic_state')
    conn.execute('''INSERT INTO dore_self_memory(key,content,source_type,source_ref,epistemic_state,updated_at)
      VALUES(?,?,?,?,?,?) ON CONFLICT(key) DO UPDATE SET content=excluded.content,source_type=excluded.source_type,
      source_ref=excluded.source_ref,epistemic_state=excluded.epistemic_state,updated_at=excluded.updated_at''',
      (key,content,source_type,source_ref,epistemic_state,now())); conn.commit()

def add_learning(conn,domain,claim,stage=None,assessment=None,status='recorded',evidence_ref=None,source_type='runtime',epistemic_state='observed'):
    if epistemic_state not in STATES: raise ValueError('invalid epistemic_state')
    # A PASS is a capability claim. It cannot be verified without evidence.
    if status.lower()=='pass' and epistemic_state=='verified' and not evidence_ref:
        raise ValueError('verified PASS requires evidence_ref')
    lid=_id('learn',domain,stage or '',claim,evidence_ref or source_type)
    t=now(); conn.execute('''INSERT OR REPLACE INTO dore_learning_events
      (id,domain,stage,claim,assessment,status,evidence_ref,source_type,epistemic_state,created_at,updated_at)
      VALUES(?,?,?,?,?,?,?,?,?,?,?)''',(lid,domain,stage,claim,assessment,status,evidence_ref,source_type,epistemic_state,t,t)); conn.commit(); return lid

def status(conn):
    ensure_schema(conn)
    self_rows=[dict(r) for r in conn.execute('SELECT * FROM dore_self_memory ORDER BY key')]
    learning=[dict(r) for r in conn.execute("SELECT * FROM dore_learning_events WHERE epistemic_state!='rejected' ORDER BY updated_at DESC")]
    verified=[x for x in learning if x['epistemic_state']=='verified']
    inherited=[x for x in learning if x['epistemic_state']=='inherited']
    return {'ok':True,'self_memory':self_rows,'learning':{'total':len(learning),'verified':len(verified),'inherited':len(inherited),'events':learning}}

def context(conn,limit=12):
    s=status(conn); lines=[]
    for x in s['self_memory']:
        if x['epistemic_state']!='rejected': lines.append(f"- [self:{x['epistemic_state']}; source={x['source_type']}] {x['content']}")
    for x in s['learning']['events'][:limit]:
        evidence=f"; evidence={x['evidence_ref']}" if x['evidence_ref'] else ''
        lines.append(f"- [learning:{x['epistemic_state']}; status={x['status']}{evidence}] {x['domain']}: {x['claim']}")
    return '\n'.join(lines)
