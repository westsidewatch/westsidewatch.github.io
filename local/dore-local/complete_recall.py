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
    raw = re.findall(r"[A-Za-z0-9_-]{2,}|[\u3400-\u9fff]{2,}", q.lower())
    # Remove only recall-language filler. Task qualifiers such as website/design/rebuild
    # are evidence and must remain; dropping them caused broad false matches in v2.
    stop = {"回想","回憶","回忆","完整","記憶","记忆","一下","一下子","關於","关于"}
    return [x for x in dict.fromkeys(raw) if x not in stop][:20]


def _score_text(text, tokens):
    low = text.lower()
    present = [t for t in tokens if t in low]
    coverage = len(present)
    repetitions = sum(low.count(t) for t in present)
    bonus = 0
    if coverage >= 2: bonus += 8
    if coverage >= 3: bonus += 16
    if coverage >= 4: bonus += 28
    return coverage * 20 + min(repetitions, 20) + bonus, present


def _conversation_rows(c, table, cid):
    cols = _cols(c, table)
    text = next((x for x in ("content","text","body") if x in cols), None)
    role = next((x for x in ("role","author_role","sender") if x in cols), None)
    order = next((x for x in ("created_at","timestamp","message_index","id") if x in cols), None)
    if not text:
        return [], text, role, order
    q = f"select * from {table} where conversation_id=?"
    if order: q += f" order by {order}"
    return list(c.execute(q, (cid,))), text, role, order


def complete_recall(query, max_conversations=8, window=10):
    result = {"schema":"dore.complete-recall.v3","query":query,"conversations":[]}
    if not DB.exists():
        result["error"] = "db_missing"; return result
    tokens = _tokens(query); result["tokens"] = tokens
    if not tokens:
        result["error"] = "no_search_tokens"; return result
    with sqlite3.connect(DB) as c:
        c.row_factory = sqlite3.Row; tables = _tables(c)
        sources = [t for t in ("aug_raw_messages", "dore_messages") if t in tables]
        ranked = []
        for source_priority, table in enumerate(sources):
            cols = _cols(c, table)
            text = next((x for x in ("content","text","body") if x in cols), None)
            cidcol = next((x for x in ("conversation_id","conversation_uuid","chat_id") if x in cols), None)
            if not text or not cidcol: continue
            where = " OR ".join([f"lower({text}) like ?" for _ in tokens]); params = [f"%{t}%" for t in tokens]
            for row in c.execute(f"select distinct {cidcol} cid from {table} where {where} limit 300", params):
                cid = row["cid"]
                rows, textcol, rolecol, ordercol = _conversation_rows(c, table, cid)
                if not rows: continue
                joined = "\n".join(str(r[textcol]) for r in rows)
                score, present = _score_text(joined, tokens)
                score += 5 if table == "aug_raw_messages" else 0
                ranked.append((score, len(present), -source_priority, cid, table, present, rows, textcol, rolecol, ordercol))
        ranked.sort(key=lambda x:(x[0],x[1],x[2]), reverse=True)
        seen = set()
        for score, coverage, _, cid, table, present, rows, textcol, rolecol, ordercol in ranked:
            if cid in seen or len(result["conversations"]) >= max_conversations: continue
            seen.add(cid)
            hit_idx = [i for i,r in enumerate(rows) if any(t in str(r[textcol]).lower() for t in present)]
            if not hit_idx: continue
            lo=max(0,min(hit_idx)-window); hi=min(len(rows),max(hit_idx)+window+1)
            messages=[{"role":str(r[rolecol]) if rolecol else "unknown","content":str(r[textcol]),"time":str(r[ordercol]) if ordercol else None} for r in rows[lo:hi]]
            result["conversations"].append({"conversation_id":cid,"source":table,"score":score,"coverage":coverage,"matched_tokens":present,"window_start":lo,"window_end":hi,"messages":messages})
    result["conversation_count"] = len(result["conversations"])
    result["ranking_rule"] = "task qualifier coverage > repetition; multi-entity co-occurrence bonus; original AUG archive preferred when relevance is comparable"
    return result

if __name__ == "__main__":
    print(json.dumps(complete_recall(" ".join(sys.argv[1:])), ensure_ascii=False, indent=2))
