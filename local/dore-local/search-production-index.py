#!/usr/bin/env python3
"""Build/update Doré Search's local production document index.

The indexer owns ingestion only. QMD remains a retrieval substrate and never becomes
Knowledge Authority. Every indexed document gets a sidecar provenance record.
"""
from __future__ import annotations
import argparse, hashlib, json, os, shutil, subprocess
from pathlib import Path

COLLECTION = "dore-production"
ALLOWED = {".md", ".txt"}
EXCLUDE_PARTS = {".git", "node_modules", ".venv", "vendor", "artifacts", "reports"}


def _run(argv, cwd, env, timeout=180):
    p = subprocess.run(argv, cwd=str(cwd), env=env, text=True, capture_output=True, timeout=timeout, check=False)
    return {"returncode": p.returncode, "stdout": p.stdout[-8000:], "stderr": p.stderr[-8000:]}


def _eligible(path: Path, repo: Path) -> bool:
    try: rel = path.relative_to(repo)
    except ValueError: return False
    if path.suffix.lower() not in ALLOWED: return False
    if any(part in EXCLUDE_PARTS for part in rel.parts): return False
    # Production search indexes authored knowledge/content, not generated build output.
    return rel.parts[0] in {"docs", "content", "data", "notes"}


def main():
    ap=argparse.ArgumentParser(); ap.add_argument("--repo",required=True); ap.add_argument("--qmd",required=True); ap.add_argument("--data",required=True)
    args=ap.parse_args(); repo=Path(args.repo).resolve(); qmd=Path(args.qmd).resolve(); data=Path(args.data).resolve()
    root=data/"qmd"/"production"; corpus=root/"corpus"; manifest_path=root/"manifest.json"
    corpus.mkdir(parents=True,exist_ok=True)
    old={}
    if manifest_path.is_file():
        try: old=json.loads(manifest_path.read_text(encoding="utf-8")).get("documents",{})
        except Exception: old={}
    docs={}; copied=0; unchanged=0
    for src in sorted(repo.rglob("*")):
        if not src.is_file() or not _eligible(src,repo): continue
        rel=src.relative_to(repo).as_posix(); raw=src.read_bytes(); digest=hashlib.sha256(raw).hexdigest()
        dest=corpus/rel; dest.parent.mkdir(parents=True,exist_ok=True)
        if old.get(rel,{}).get("sha256")==digest and dest.is_file(): unchanged+=1
        else: shutil.copy2(src,dest); copied+=1
        docs[rel]={"sha256":digest,"source":"repo","source_ref":rel,"authority":False}
    removed=0
    for rel in set(old)-set(docs):
        target=corpus/rel
        if target.is_file(): target.unlink(); removed+=1
    manifest={"schema":"dore.search-index.v1","collection":COLLECTION,"authority":False,"documents":docs}
    manifest_path.write_text(json.dumps(manifest,ensure_ascii=False,indent=2)+"\n",encoding="utf-8")
    env=os.environ.copy(); home=root/"home"; config=root/"config"; cache=root/"cache"
    for p in (home,config,cache): p.mkdir(parents=True,exist_ok=True)
    env.update({"HOME":str(home),"XDG_CONFIG_HOME":str(config),"XDG_CACHE_HOME":str(cache)})
    add=_run([str(qmd),"collection","add",str(corpus),"--name",COLLECTION],repo,env,120)
    update=_run([str(qmd),"update"],repo,env,240)
    # Collection-add is idempotent; existing collection may return nonzero.
    ok=update["returncode"]==0
    print(json.dumps({"ok":ok,"collection":COLLECTION,"authority":False,"documents":len(docs),"copied":copied,"unchanged":unchanged,"removed":removed,"manifest":str(manifest_path),"collection_add_rc":add["returncode"],"update_rc":update["returncode"],"update_stderr":update["stderr"][-2000:]},ensure_ascii=False))
    return 0 if ok else 1

if __name__=="__main__": raise SystemExit(main())
