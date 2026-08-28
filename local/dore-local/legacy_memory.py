#!/usr/bin/env python3
"""Legacy-memory transplant support for Doré.

Imported legacy memories are inherited immediately, but provenance and epistemic
state remain explicit. They are not silently rewritten as verified facts.
"""
from __future__ import annotations
import json, sqlite3, uuid, hashlib
from datetime import datetime, timezone
from pathlib import Path

LEGACY_STATES={'inherited','verified','corrected','rejected'}

def now(): return datetime.now(timezone.utc).isoformat()

def ensure_schema(conn: sqlite3.Connection):
    conn.execute('''CREATE TABLE IF NOT EXISTS dore_legacy_memory (
      id TEXT PRIMARY KEY,
      subject TEXT NOT NULL,
      content TEXT NOT NULL,
      source_type TEXT NOT NULL DEFAULT 'chatgpt_legacy_memory',
      source_ref TEXT,
      epistemic_state TEXT NOT NULL DEFAULT 'inherited',
      content_sha256 TEXT NOT NULL UNIQUE,
      created_at TEXT NOT NULL,
      updated_at TEXT NOT NULL
    )''')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_legacy_subject ON dore_legacy_memory(subject)')
    conn.execute('CREATE INDEX IF NOT EXISTS idx_legacy_state ON dore_legacy_memory(epistemic_state)')

def import_items(conn, root: Path, items):
    ensure_schema(conn); out=[]
    archive=root/'archive'/'legacy-memory'; archive.mkdir(parents=True,exist_ok=True)
    for item in items:
        content=str(item.get('content') or '').strip()
        if not content: continue
        subject=str(item.get('subject') or 'general').strip()
        state=str(item.get('epistemic_state') or 'inherited')
        if state not in LEGACY_STATES: state='inherited'
        source_type=str(item.get('source_type') or 'chatgpt_legacy_memory')
        source_ref=item.get('source_ref')
        h=hashlib.sha256((subject+'\n'+content).encode()).hexdigest(); ts=now(); mid=str(uuid.uuid4())
        cur=conn.execute('INSERT OR IGNORE INTO dore_legacy_memory(id,subject,content,source_type,source_ref,epistemic_state,content_sha256,created_at,updated_at) VALUES(?,?,?,?,?,?,?,?,?)',(mid,subject,content,source_type,source_ref,state,h,ts,ts))
        if cur.rowcount:
            payload={'schema':'dore.legacy-memory.v1','id':mid,'subject':subject,'content':content,'source_type':source_type,'source_ref':source_ref,'epistemic_state':state,'created_at':ts}
            (archive/f'{mid}.json').write_text(json.dumps(payload,ensure_ascii=False,indent=2),encoding='utf-8')
            out.append(mid)
    return out

def query_terms(q):
    import re
    s=str(q).lower(); terms=set(re.findall(r'[a-z0-9_:-]{2,}',s))
    for run in re.findall(r'[\u3400-\u9fff]+',s):
        if len(run)<=4: terms.add(run)
        for n in (2,3,4):
            for i in range(max(0,len(run)-n+1)): terms.add(run[i:i+n])
    return terms

def recall(conn, q, limit=16):
    ensure_schema(conn); terms=query_terms(q)
    rows=[dict(x) for x in conn.execute("SELECT * FROM dore_legacy_memory WHERE epistemic_state!='rejected' ORDER BY updated_at DESC")]
    scored=[]
    for r in rows:
        hay=(r['subject']+' '+r['content']).lower(); hits=sum(1 for t in terms if t in hay)
        # Identity/world/learning memories remain weakly available even without lexical hits.
        prior=3 if r['subject'] in {'identity','learning','westside','church','one','dawn-library','relationships'} else 0
        score=hits*10+prior
        if score: scored.append((score,r))
    scored.sort(key=lambda x:(x[0],x[1]['updated_at']),reverse=True)
    return [r for _,r in scored[:limit]]

def context(rows):
    if not rows: return '- none'
    return '\n'.join(f"- [{r['epistemic_state']}; source={r['source_type']}] {r['content']}" for r in rows)
