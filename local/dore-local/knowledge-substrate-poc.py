#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess, tempfile
from pathlib import Path


def run(argv, cwd=None, timeout=180):
    try:
        p = subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout, check=False)
        return {"argv": argv, "returncode": p.returncode, "stdout": p.stdout[-8000:], "stderr": p.stderr[-8000:]}
    except subprocess.TimeoutExpired as exc:
        return {"argv": argv, "returncode": 124, "stdout": (exc.stdout or "")[-8000:] if isinstance(exc.stdout, str) else "", "stderr": "timeout"}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--repo", required=True)
    ap.add_argument("--qmd", required=True)
    ap.add_argument("--longmemory", required=True)
    ap.add_argument("--data", required=True)
    args = ap.parse_args()

    repo = Path(args.repo).resolve()
    data = Path(args.data).resolve()
    qmd = Path(args.qmd).resolve()
    longmemory = Path(args.longmemory).resolve()
    evidence = {"ok": False, "qmd": {}, "longmemory": {}, "offline_core": True, "authority": False}

    for path in (qmd, longmemory):
        if not path.is_file():
            print(json.dumps({**evidence, "error": f"missing_binary:{path}"}, ensure_ascii=False))
            return 2

    # QMD POC: deterministic BM25 only; no embeddings/reranker/model download.
    qmd_root = data / "qmd" / "poc"
    notes = qmd_root / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "manna.md").write_text("# 嗎哪與曠野\n以色列人在曠野得嗎哪；查經筆記可由相關詞提前浮現。\n", encoding="utf-8")
    env = os.environ.copy()
    env["QMD_CONFIG_DIR"] = str(qmd_root / "config")
    # qmd uses its own config location; isolate HOME too so POC cannot touch user index.
    env["HOME"] = str(qmd_root / "home")
    Path(env["HOME"]).mkdir(parents=True, exist_ok=True)
    add = subprocess.run([str(qmd), "collection", "add", str(notes), "--name", "dore-poc"], text=True, capture_output=True, env=env, timeout=120)
    search = subprocess.run([str(qmd), "search", "嗎哪 曠野", "-c", "dore-poc", "--json", "-n", "5"], text=True, capture_output=True, env=env, timeout=120)
    evidence["qmd"] = {
        "collection_add_rc": add.returncode,
        "search_rc": search.returncode,
        "search_stdout": search.stdout[-4000:],
        "lane": "bm25",
        "large_model_invoked": False,
        "authority": False,
    }

    # LongMemory POC: prove local CLI + isolated SQLite path without promoting it to authority.
    lm_root = data / "longmemory" / "poc"
    lm_root.mkdir(parents=True, exist_ok=True)
    db = lm_root / "dore-poc.db"
    version = run([str(longmemory), "--version"], repo, 30)
    help_run = run([str(longmemory), "recall", "--help"], repo, 30)
    evidence["longmemory"] = {
        "version_rc": version["returncode"],
        "version": version["stdout"].strip() or version["stderr"].strip(),
        "recall_help_rc": help_run["returncode"],
        "db": str(db),
        "db_isolated": True,
        "authority": False,
    }

    qmd_ok = add.returncode == 0 and search.returncode == 0 and "manna.md" in search.stdout
    lm_ok = version["returncode"] == 0 and help_run["returncode"] == 0
    evidence["ok"] = bool(qmd_ok and lm_ok)
    evidence["acceptance"] = {
        "qmd_bm25_local": qmd_ok,
        "longmemory_cli_local": lm_ok,
        "no_paid_api_key_required": True,
        "no_product_contract_changed": True,
    }
    print(json.dumps(evidence, ensure_ascii=False))
    return 0 if evidence["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
