#!/usr/bin/env python3
from __future__ import annotations
import argparse, json, os, subprocess
from pathlib import Path


def run(argv, cwd=None, timeout=180, env=None):
    try:
        p = subprocess.run(argv, cwd=str(cwd) if cwd else None, text=True, capture_output=True, timeout=timeout, check=False, env=env)
        return {"argv": argv, "returncode": p.returncode, "stdout": p.stdout[-8000:], "stderr": p.stderr[-8000:]}
    except subprocess.TimeoutExpired:
        return {"argv": argv, "returncode": 124, "stdout": "", "stderr": "timeout"}


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

    # QMD POC: deterministic BM25 only; no embeddings, reranker, or large model.
    qmd_root = data / "qmd" / "poc"
    notes = qmd_root / "notes"
    notes.mkdir(parents=True, exist_ok=True)
    (notes / "manna.md").write_text("# 嗎哪與曠野\n以色列人在曠野得嗎哪；查經筆記可由相關詞提前浮現。\n", encoding="utf-8")
    env = os.environ.copy()
    env["HOME"] = str(qmd_root / "home")
    env["XDG_CONFIG_HOME"] = str(qmd_root / "config")
    env["XDG_CACHE_HOME"] = str(qmd_root / "cache")
    for key in ("HOME", "XDG_CONFIG_HOME", "XDG_CACHE_HOME"):
        Path(env[key]).mkdir(parents=True, exist_ok=True)

    add = run([str(qmd), "collection", "add", str(notes), "--name", "dore-poc"], repo, 120, env)
    update = run([str(qmd), "update"], repo, 120, env)
    search = run([str(qmd), "search", "嗎哪 曠野", "-c", "dore-poc", "--json", "-n", "5"], repo, 120, env)
    qmd_search_hit = search["returncode"] == 0 and "manna.md" in search["stdout"] and "嗎哪與曠野" in search["stdout"]
    evidence["qmd"] = {
        "collection_add_rc": add["returncode"],
        "collection_add_stdout": add["stdout"][-2000:],
        "collection_add_stderr": add["stderr"][-2000:],
        "update_rc": update["returncode"],
        "search_rc": search["returncode"],
        "search_stdout": search["stdout"][-4000:],
        "search_hit": qmd_search_hit,
        "lane": "bm25",
        "large_model_invoked": False,
        "authority": False,
    }

    # LongMemory POC: prove the local CLI surface is callable and reserve an
    # isolated SQLite path. The current `lom` CLI reports help/version through
    # a non-zero status, so acceptance is based on the stable command surface,
    # not on conventional help exit-code assumptions.
    lm_root = data / "longmemory" / "poc"
    lm_root.mkdir(parents=True, exist_ok=True)
    db = lm_root / "dore-poc.db"
    version = run([str(longmemory), "--version"], repo, 30)
    help_run = run([str(longmemory), "--help"], repo, 30)
    lm_text = "\n".join([version["stdout"], version["stderr"], help_run["stdout"], help_run["stderr"]]).lower()
    lm_cli_surface = "longmemory cli" in lm_text and "add <text>" in lm_text and "query <text>" in lm_text
    evidence["longmemory"] = {
        "version_rc": version["returncode"],
        "version": version["stdout"].strip() or version["stderr"].strip(),
        "help_rc": help_run["returncode"],
        "cli_surface_detected": lm_cli_surface,
        "db": str(db),
        "db_isolated": True,
        "canonical_ingest": False,
        "authority": False,
    }

    # Collection creation is intentionally idempotent: a repeated POC may see
    # "already exists" while search/update continue to work. Actual retrieval
    # behavior is therefore the acceptance signal.
    qmd_ok = update["returncode"] == 0 and qmd_search_hit
    lm_ok = lm_cli_surface
    evidence["ok"] = bool(qmd_ok and lm_ok)
    evidence["acceptance"] = {
        "qmd_bm25_local": qmd_ok,
        "longmemory_cli_local": lm_ok,
        "no_large_model_for_passive_probe": True,
        "no_paid_api_key_required": True,
        "no_product_contract_changed": True,
        "canonical_knowledge_untouched": True,
    }
    print(json.dumps(evidence, ensure_ascii=False))
    return 0 if evidence["ok"] else 1


if __name__ == "__main__":
    raise SystemExit(main())
