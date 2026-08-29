#!/usr/bin/env python3
"""Safe resident updater for Doré Local.

Fast-forwards this checkout from origin/main when possible, then runs the
coordination worker so GitHub inbox requests are consumed without a human relay.
Never resets, force-checkouts, or discards local work.
"""
from __future__ import annotations
import fcntl
import os
import subprocess
import sys
from datetime import datetime, timezone
from pathlib import Path

ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home()/"westsidewatch.github.io")).expanduser()
HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home()/".dore")).expanduser()
LOCK = HOME/"coordination"/"updater.lock"
LOG = HOME/"coordination"/"updater.log"
WORKER = ROOT/"local"/"dore-local"/"coordination_worker.py"


def log(msg: str) -> None:
    LOG.parent.mkdir(parents=True, exist_ok=True)
    with LOG.open("a", encoding="utf-8") as f:
        f.write(f"{datetime.now(timezone.utc).isoformat()} {msg}\n")


def run(*args: str, timeout: int = 90) -> subprocess.CompletedProcess[str]:
    return subprocess.run(list(args), cwd=ROOT, text=True, capture_output=True, timeout=timeout)


def sync() -> str:
    if not (ROOT/".git").exists():
        return "repo_missing"
    fetch = run("git", "fetch", "origin", "main")
    if fetch.returncode:
        return "fetch_failed:" + (fetch.stderr or "")[-240:].replace("\n", " ")
    # Only fast-forward. Never overwrite Doré's local work.
    ff = run("git", "merge-base", "--is-ancestor", "HEAD", "origin/main", timeout=20)
    if ff.returncode == 0:
        merge = run("git", "merge", "--ff-only", "origin/main")
        if merge.returncode == 0:
            return "fast_forwarded" if "Already up to date" not in merge.stdout else "up_to_date"
        return "ff_blocked:" + (merge.stderr or merge.stdout or "")[-240:].replace("\n", " ")
    ahead = run("git", "merge-base", "--is-ancestor", "origin/main", "HEAD", timeout=20)
    if ahead.returncode == 0:
        return "local_ahead"
    return "diverged"


def main() -> int:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        state = sync()
        log("sync=" + state)
        if not WORKER.exists():
            log("worker_missing")
            return 2
        cp = subprocess.run([sys.executable, str(WORKER)], cwd=ROOT, text=True, capture_output=True, timeout=900)
        log(f"worker_rc={cp.returncode} " + ((cp.stderr or cp.stdout or "")[-300:].replace("\n", " ")))
        return cp.returncode


if __name__ == "__main__":
    raise SystemExit(main())
