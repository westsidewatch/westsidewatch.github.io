#!/usr/bin/env python3
"""Safe resident updater for Doré Local.

Fast-forwards this checkout from origin/main when possible, rebases clean local-only
commits when branches diverge, then runs the coordination worker so GitHub inbox
requests are consumed without a human relay.
Never resets, force-checkouts, or discards uncommitted local work.
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


def clean_worktree() -> bool:
    cp = run("git", "status", "--porcelain", timeout=20)
    return cp.returncode == 0 and not cp.stdout.strip()


def sync() -> str:
    if not (ROOT/".git").exists():
        return "repo_missing"

    fetch = run("git", "fetch", "origin", "main")
    if fetch.returncode:
        return "fetch_failed:" + (fetch.stderr or "")[-240:].replace("\n", " ")

    # Remote is ahead (or equal): ordinary safe fast-forward.
    ff = run("git", "merge-base", "--is-ancestor", "HEAD", "origin/main", timeout=20)
    if ff.returncode == 0:
        merge = run("git", "merge", "--ff-only", "origin/main")
        if merge.returncode == 0:
            return "fast_forwarded" if "Already up to date" not in merge.stdout else "up_to_date"
        return "ff_blocked:" + (merge.stderr or merge.stdout or "")[-240:].replace("\n", " ")

    # Local contains origin/main already: no incoming work to consume.
    ahead = run("git", "merge-base", "--is-ancestor", "origin/main", "HEAD", timeout=20)
    if ahead.returncode == 0:
        return "local_ahead"

    # Branches diverged. This commonly happens because Doré persists local evidence
    # commits while ChatGPT concurrently lands new inbox work on origin/main.
    # Never touch a dirty tree. On a clean tree, preserve local commits by rebasing
    # them on top of origin/main instead of resetting/discarding anything.
    if not clean_worktree():
        return "diverged_dirty_blocked"

    rebase = run("git", "rebase", "origin/main", timeout=300)
    if rebase.returncode == 0:
        return "diverged_rebased"

    # A conflict should not leave the resident updater stuck in an in-progress rebase.
    abort = run("git", "rebase", "--abort", timeout=30)
    detail = (rebase.stderr or rebase.stdout or "")[-240:].replace("\n", " ")
    if abort.returncode:
        detail += " abort_failed=" + (abort.stderr or abort.stdout or "")[-120:].replace("\n", " ")
    return "diverged_rebase_conflict:" + detail


def main() -> int:
    LOCK.parent.mkdir(parents=True, exist_ok=True)
    with LOCK.open("a+") as lock:
        try:
            fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0

        state = sync()
        log("sync=" + state)

        # If incoming work could not be integrated, do not run a stale worker and
        # falsely imply the command path is healthy.
        if state.startswith(("repo_missing", "fetch_failed", "ff_blocked", "diverged_dirty_blocked", "diverged_rebase_conflict")):
            return 3

        if not WORKER.exists():
            log("worker_missing")
            return 2

        cp = subprocess.run([sys.executable, str(WORKER)], cwd=ROOT, text=True, capture_output=True, timeout=900)
        log(f"worker_rc={cp.returncode} " + ((cp.stderr or cp.stdout or "")[-300:].replace("\n", " ")))
        return cp.returncode


if __name__ == "__main__":
    raise SystemExit(main())
