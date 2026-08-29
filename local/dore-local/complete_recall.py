#!/usr/bin/env python3
from __future__ import annotations
import json, os, re, sqlite3, sys
from pathlib import Path

HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home()/".dore")).expanduser()
DB = HOME/"data"/"dore.sqlite3"


def _tables(c):
    return {r[0] for r in c.execute("select name from sqlite_master where type='table'")}


def _cols(c, table):
    return {r[1] for r in c.execute(f"pragma table_info({table})")}


def _tokens(q):
    parts = re.findall(r"[A-Za-z0-9_-]{2,}|[\u3400-\u9fff]{2,}", q.lower())
    return list(dict.fromkeys(parts))[:16]


def complete_recall(query, max_conversations=8, window=8):
    result = {"schema":"dore.complete-recall.v1","query":query,"conversations":[]}
    if not DB.exists():
        result["error"] = "db_missing"
        return result
    tokens = _tokens(query)
    result["tokens"] = tokens
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row
        tables = _tables(c)
        sources = [t for t in ("aug_raw_messages", "dore_messages") if t in tables]
        candidates = []
        for table in sources:
            cols = _cols(c, table)
            text = next((x for x in ("content","text","body") if x in cols), None)
            cid = next((x for x in ("conversation_id","conversation_uuid","chat_id") if x in cols), None)
            if not text or not cid or not tokens:
                continue
            where = " OR ".join([f"lower({text}) like ?" for _ in tokens])
            params = [f"%{t}%" for t in tokens]
            sql = f"select {cid} cid, count(*) hits from {table} where {where} group by {cid} order by hits desc limit ?"
            for row in c.execute(sql, params+[max_conversations]):
                candidates.append((row["cid"], row["hits"], table))
            if candidates:
                break
        seen = set()
        for cid, hits, table in candidates:
            if cid in seen:
                continue
            seen.add(cid)
            cols = _cols(c, table)
            text = next((x for x in ("content","text","body") if x in cols), None)
            role = next((x for x in ("role","author_role","sender") if x in cols), None)
            order = next((x for x in ("created_at","timestamp","message_index","id") if x in cols), None)
            q = f"select * from {table} where conversation_id=?"
            if order:
                q += f" order by {order}"
            rows = list(c.execute(q, (cid,)))
            hit_idx = [i for i,r in enumerate(rows) if any(t in str(r[text]).lower() for t in tokens)]
            if not hit_idx:
                continue
            lo = max(0, min(hit_idx)-window)
            hi = min(len(rows), max(hit_idx)+window+1)
            messages = []
            for r in rows[lo:hi]:
                messages.append({
                    "role": str(r[role]) if role else "unknown",
                    "content": str(r[text]),
                    "time": str(r[order]) if order else None,
                })
            result["conversations"].append({
                "conversation_id": cid,
                "source": table,
                "hits": hits,
                "window_start": lo,
                "window_end": hi,
                "messages": messages,
            })
    result["conversation_count"] = len(result["conversations"])
    return result


if __name__ == "__main__":
    print(json.dumps(complete_recall(" ".join(sys.argv[1:])), ensure_ascii=False, indent=2))
