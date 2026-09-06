#!/usr/bin/env python3
from pathlib import Path
import importlib.util,json,sqlite3,sys,tempfile
ROOT=Path(__file__).resolve().parents[1]

def load(name,path):
 s=importlib.util.spec_from_file_location(name,path);m=importlib.util.module_from_spec(s);sys.modules[name]=m;assert s and s.loader;s.loader.exec_module(m);return m
sub=load("conversation_substrate",ROOT/"conversation_substrate.py")

def main():
 with tempfile.TemporaryDirectory(prefix="dore-conv-converge-") as td:
  db=Path(td)/"dore.sqlite3"
  with sqlite3.connect(db) as c:
   c.execute("CREATE TABLE dore_messages(id TEXT PRIMARY KEY,conversation_id TEXT,project_id TEXT,role TEXT,content TEXT,created_at TEXT,archive_key TEXT)")
   c.execute("INSERT INTO dore_messages VALUES(?,?,?,?,?,?,?)",("m1","c1","dore-search","user","基列雅比沒有去攻打便雅憫","2026-09-05T00:00:00Z","conversations/dore-search/c1/m1.json"))
   c.execute("INSERT INTO dore_messages VALUES(?,?,?,?,?,?,?)",("m2","c1","dore-search","assistant","這是一段查經對話","2026-09-05T00:00:01Z","conversations/dore-search/c1/m2.json"))
  cs=sub.ConversationSubstrate(db);first=cs.backfill();second=cs.backfill();hits=cs.recall("基列雅比")
  with sqlite3.connect(db) as c:
   domain=c.execute("SELECT COUNT(*) FROM dore_messages").fetchone()[0]; projected=c.execute("SELECT COUNT(*) FROM dore_artifacts WHERE kind='conversation-message'").fetchone()[0]
  checks={"domain_rows_preserved":domain==2,"messages_projected_once":projected==2 and first["created"]==2,"backfill_idempotent":second["created"]==0 and second["existing"]==2,"shared_retrieval_finds_conversation":bool(hits) and hits[0]["artifact_id"]=="message:m1","archive_not_required_for_recall":True}
  out={"ok":all(checks.values()),"schema":"dore.conversation-substrate.acceptance.v1","checks":checks,"first":first,"second":second,"search_engine":hits[0]["engine"] if hits else None};print(json.dumps(out,ensure_ascii=False,indent=2));return 0 if out["ok"] else 1
if __name__=="__main__":raise SystemExit(main())
