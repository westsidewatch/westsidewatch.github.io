#!/usr/bin/env python3
from __future__ import annotations
import hashlib, sqlite3
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
    CREATE TABLE IF NOT EXISTS dore_learning_transitions(
      id TEXT PRIMARY KEY, learning_id TEXT NOT NULL, from_state TEXT, to_state TEXT NOT NULL,
      reason TEXT, evidence_ref TEXT, created_at TEXT NOT NULL);
    CREATE INDEX IF NOT EXISTS idx_dore_learning_transition ON dore_learning_transitions(learning_id,created_at);
    '''); conn.commit()

def upsert_self(conn,key,content,source_type='runtime',source_ref=None,epistemic_state='observed'):
    if epistemic_state not in STATES: raise ValueError('invalid epistemic_state')
    conn.execute('''INSERT INTO dore_self_memory(key,content,source_type,source_ref,epistemic_state,updated_at)
      VALUES(?,?,?,?,?,?) ON CONFLICT(key) DO UPDATE SET content=excluded.content,source_type=excluded.source_type,
      source_ref=excluded.source_ref,epistemic_state=excluded.epistemic_state,updated_at=excluded.updated_at''',
      (key,content,source_type,source_ref,epistemic_state,now())); conn.commit()

def add_learning(conn,domain,claim,stage=None,assessment=None,status='recorded',evidence_ref=None,source_type='runtime',epistemic_state='observed'):
    if epistemic_state not in STATES: raise ValueError('invalid epistemic_state')
    if status.lower()=='pass' and epistemic_state=='verified' and not evidence_ref: raise ValueError('verified PASS requires evidence_ref')
    lid=_id('learn',domain,stage or '',claim,evidence_ref or source_type); t=now()
    conn.execute('''INSERT INTO dore_learning_events(id,domain,stage,claim,assessment,status,evidence_ref,source_type,epistemic_state,created_at,updated_at)
      VALUES(?,?,?,?,?,?,?,?,?,?,?) ON CONFLICT(id) DO UPDATE SET assessment=excluded.assessment,status=excluded.status,
      evidence_ref=excluded.evidence_ref,source_type=excluded.source_type,epistemic_state=excluded.epistemic_state,updated_at=excluded.updated_at''',
      (lid,domain,stage,claim,assessment,status,evidence_ref,source_type,epistemic_state,t,t)); conn.commit(); return lid

def transition_learning(conn,learning_id,to_state,reason=None,evidence_ref=None,status=None):
    if to_state not in STATES: raise ValueError('invalid epistemic_state')
    row=conn.execute('SELECT * FROM dore_learning_events WHERE id=?',(learning_id,)).fetchone()
    if not row: raise KeyError('learning event not found')
    target_status=status or row['status']; ev=evidence_ref or row['evidence_ref']
    if to_state=='verified' and target_status.lower()=='pass' and not ev: raise ValueError('verified PASS requires evidence_ref')
    tid=_id('transition',learning_id,row['epistemic_state'],to_state,now())
    conn.execute('INSERT INTO dore_learning_transitions(id,learning_id,from_state,to_state,reason,evidence_ref,created_at) VALUES(?,?,?,?,?,?,?)',(tid,learning_id,row['epistemic_state'],to_state,reason,evidence_ref,now()))
    conn.execute('UPDATE dore_learning_events SET epistemic_state=?,status=?,evidence_ref=?,updated_at=? WHERE id=?',(to_state,target_status,ev,now(),learning_id)); conn.commit(); return tid

def status(conn):
    ensure_schema(conn)
    self_rows=[dict(r) for r in conn.execute('SELECT * FROM dore_self_memory ORDER BY key')]
    learning=[dict(r) for r in conn.execute("SELECT * FROM dore_learning_events WHERE epistemic_state!='rejected' ORDER BY updated_at DESC")]
    counts={s:sum(1 for x in learning if x['epistemic_state']==s) for s in STATES}
    capabilities=[x for x in learning if x['epistemic_state']=='verified' and x['status'].lower()=='pass' and x['evidence_ref']]
    current={}
    for x in learning:
        k=x['domain']; current.setdefault(k,x)
    return {'ok':True,'self_memory':self_rows,'learning':{'total':len(learning),'states':counts,'verified_capabilities':capabilities,'current_by_domain':current,'events':learning}}

def context(conn,limit=16):
    s=status(conn); lines=[]
    for x in s['self_memory']:
        if x['epistemic_state']!='rejected': lines.append(f"- [self:{x['epistemic_state']}; source={x['source_type']}] {x['content']}")
    for x in s['learning']['events'][:limit]:
        evidence=f"; evidence={x['evidence_ref']}" if x['evidence_ref'] else ''
        lines.append(f"- [learning:{x['epistemic_state']}; status={x['status']}{evidence}] {x['domain']} / {x['stage'] or '-'}: {x['claim']}")
    return '\n'.join(lines)
