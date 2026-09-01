#!/usr/bin/env python3
"""Doré Resident Runtime v0.2.

Resident macOS control loop with two missing control-plane capabilities added:
1. Telemetry publication to an isolated Git branch so ChatGPT can observe the loop.
2. Safe self-update of the runtime/driver from this repository's main branch.

Design sources adapted, not re-invented:
- macOS launchd owns process supervision and restart.
- Microsoft Agent Framework autonomous handoff inspires NO_USER_INPUT -> CONTINUE.
- A2A task semantics inspire durable state/event separation from any chat connection.
- LangGraph/Temporal ideas inspire checkpoint-before-action and resume-after-failure.
- Git's own branch/worktree model isolates telemetry writes from the product worktree.

The chat window is not the scheduler. launchd keeps this process alive; this process owns
cadence, recovery and observation publication. Unknown technical gaps are not a HUMAN_GATE
by default.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import shutil
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

VERSION = "dore.resident-runtime.v0.2"
HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
RUNTIME = HOME / "runtime"
LEARNING = HOME / "coordination" / "learning"
DRIVER = ROOT / "local" / "dore-local" / "autonomous_driver.py"
SELF = ROOT / "local" / "dore-local" / "resident_runtime.py"
STATE = RUNTIME / "state.json"
EVENTS = RUNTIME / "events.jsonl"
HEARTBEAT = RUNTIME / "heartbeat.json"
LOCK = RUNTIME / "runtime.lock"
TELEMETRY_REPO = RUNTIME / "telemetry-repo"
TELEMETRY_BRANCH = os.environ.get("DORE_RUNTIME_TELEMETRY_BRANCH", "dore-runtime-telemetry")
TELEMETRY_INTERVAL = max(60, int(os.environ.get("DORE_RUNTIME_TELEMETRY_SECONDS", "120")))
SELF_UPDATE_INTERVAL = max(120, int(os.environ.get("DORE_RUNTIME_SELF_UPDATE_SECONDS", "300")))
INTERVAL = max(10, int(os.environ.get("DORE_RUNTIME_INTERVAL_SECONDS", "30")))
STALL_AFTER = max(INTERVAL * 2, int(os.environ.get("DORE_RUNTIME_STALL_SECONDS", "90")))
PARENT_ID = os.environ.get("DORE_RUNTIME_PARENT_ID", "new-westside-storybook-real-loop-2")
PARENT_GOAL = os.environ.get("DORE_RUNTIME_PARENT_GOAL", "New Westside visual construction")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def run(argv, cwd=ROOT, timeout=120):
    return subprocess.run(argv, cwd=str(cwd), text=True, capture_output=True, timeout=timeout)


def read_json(path: Path, default=None):
    try:
        return json.loads(path.read_text(encoding="utf-8"))
    except Exception:
        return default


def atomic_json(path: Path, value) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    tmp = path.with_suffix(path.suffix + ".tmp")
    tmp.write_text(json.dumps(value, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)


def append_event(kind: str, **data) -> None:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    row = {"at": now(), "event": kind, **data}
    with EVENTS.open("a", encoding="utf-8") as f:
        f.write(json.dumps(row, ensure_ascii=False) + "\n")


def fingerprint(value) -> str:
    raw = json.dumps(value, ensure_ascii=False, sort_keys=True, default=str).encode("utf-8")
    return hashlib.sha256(raw).hexdigest()


def tail_events(limit=24):
    if not EVENTS.exists():
        return []
    rows = []
    for line in EVENTS.read_text(encoding="utf-8", errors="replace").splitlines()[-limit:]:
        try:
            rows.append(json.loads(line))
        except Exception:
            rows.append({"event": "UNPARSEABLE_EVENT", "raw": line[-1000:]})
    return rows


def latest_learning():
    direct = LEARNING / f"{PARENT_ID}.json"
    if direct.exists():
        data = read_json(direct)
        if isinstance(data, dict):
            return direct, data
    if not LEARNING.exists():
        return None, None
    files = sorted(LEARNING.glob("*.json"), key=lambda p: p.stat().st_mtime, reverse=True)
    for p in files:
        data = read_json(p)
        if isinstance(data, dict) and data.get("state") == "RESEARCH_REQUIRED":
            return p, data
    return None, None


def run_driver(reason: str, learning_path: Path | None, learning: dict | None):
    if not DRIVER.exists():
        return {"ok": False, "error": "driver_missing", "driver": str(DRIVER)}
    message_id = f"resident-{int(time.time())}"
    msg = {
        "schema": "dore.runtime.v0.2",
        "message_id": message_id,
        "kind": "autonomous_driver",
        "sender": "dore-resident-runtime",
        "recipient": "dore",
        "related_goal": PARENT_GOAL,
        "task": {
            "parent_source_message_id": PARENT_ID,
            "parent_goal": PARENT_GOAL,
            "trigger": reason,
            "learning_evidence": str(learning_path) if learning_path else None,
            "failure_fingerprint": (learning or {}).get("failure_fingerprint"),
        },
    }
    cp = subprocess.run(
        [sys.executable, str(DRIVER)],
        cwd=str(ROOT),
        input=json.dumps(msg, ensure_ascii=False),
        text=True,
        capture_output=True,
        timeout=1200,
    )
    parsed = None
    try:
        parsed = json.loads((cp.stdout or "").strip().splitlines()[-1])
    except Exception:
        pass
    return {
        "ok": cp.returncode == 0 and isinstance(parsed, dict) and bool(parsed.get("ok")),
        "returncode": cp.returncode,
        "stdout": (cp.stdout or "")[-12000:],
        "stderr": (cp.stderr or "")[-12000:],
        "result": parsed,
    }


def telemetry_snapshot():
    state = read_json(STATE, {}) or {}
    heartbeat = read_json(HEARTBEAT, {}) or {}
    return {
        "schema": "dore.runtime.telemetry.v0.1",
        "published_at": now(),
        "runtime": VERSION,
        "host_role": "dore-local-mac",
        "parent_goal": PARENT_GOAL,
        "parent_message_id": PARENT_ID,
        "heartbeat": heartbeat,
        "state": state,
        "events": tail_events(24),
    }


def ensure_telemetry_repo():
    remote = run(["git", "remote", "get-url", "origin"], timeout=30)
    if remote.returncode != 0 or not remote.stdout.strip():
        raise RuntimeError("origin_remote_unavailable")
    url = remote.stdout.strip()
    if not (TELEMETRY_REPO / ".git").exists():
        if TELEMETRY_REPO.exists():
            shutil.rmtree(TELEMETRY_REPO)
        cp = run(["git", "clone", "--filter=blob:none", "--no-checkout", url, str(TELEMETRY_REPO)], cwd=RUNTIME, timeout=180)
        if cp.returncode != 0:
            raise RuntimeError("telemetry_clone_failed:" + (cp.stderr or cp.stdout)[-1500:])
        run(["git", "config", "user.name", "DORE-RUNTIME"], cwd=TELEMETRY_REPO, timeout=30)
        run(["git", "config", "user.email", "westsidewatchca@gmail.com"], cwd=TELEMETRY_REPO, timeout=30)
    return TELEMETRY_REPO


def publish_telemetry(force=False):
    state = read_json(STATE, {}) or {}
    last = float(state.get("last_telemetry_epoch") or 0)
    if not force and time.time() - last < TELEMETRY_INTERVAL:
        return False
    repo = ensure_telemetry_repo()
    run(["git", "fetch", "origin", TELEMETRY_BRANCH], cwd=repo, timeout=90)
    exists = run(["git", "show-ref", "--verify", f"refs/remotes/origin/{TELEMETRY_BRANCH}"], cwd=repo, timeout=30).returncode == 0
    if exists:
        cp = run(["git", "checkout", "-B", TELEMETRY_BRANCH, f"origin/{TELEMETRY_BRANCH}"], cwd=repo, timeout=60)
    else:
        cp = run(["git", "checkout", "--orphan", TELEMETRY_BRANCH], cwd=repo, timeout=60)
        if cp.returncode == 0:
            run(["git", "rm", "-rf", "."], cwd=repo, timeout=60)
    if cp.returncode != 0:
        raise RuntimeError("telemetry_checkout_failed:" + (cp.stderr or cp.stdout)[-1500:])
    payload = repo / "runtime-latest.json"
    payload.write_text(json.dumps(telemetry_snapshot(), ensure_ascii=False, indent=2) + "\n", encoding="utf-8")
    run(["git", "add", "runtime-latest.json"], cwd=repo, timeout=30)
    changed = run(["git", "diff", "--cached", "--quiet"], cwd=repo, timeout=30).returncode != 0
    if changed:
        commit = run(["git", "commit", "-m", "chore(dore): publish resident runtime telemetry"], cwd=repo, timeout=60)
        if commit.returncode != 0:
            raise RuntimeError("telemetry_commit_failed:" + (commit.stderr or commit.stdout)[-1500:])
        push = run(["git", "push", "origin", f"HEAD:{TELEMETRY_BRANCH}"], cwd=repo, timeout=120)
        if push.returncode != 0:
            raise RuntimeError("telemetry_push_failed:" + (push.stderr or push.stdout)[-1500:])
    state["last_telemetry_epoch"] = time.time()
    state["last_telemetry_at"] = now()
    state["telemetry_branch"] = TELEMETRY_BRANCH
    atomic_json(STATE, state)
    return changed


def maybe_self_update():
    state = read_json(STATE, {}) or {}
    last = float(state.get("last_self_update_check_epoch") or 0)
    if time.time() - last < SELF_UPDATE_INTERVAL:
        return False
    state["last_self_update_check_epoch"] = time.time()
    state["last_self_update_check_at"] = now()
    atomic_json(STATE, state)
    fetch = run(["git", "fetch", "origin", "main"], timeout=120)
    if fetch.returncode != 0:
        append_event("SELF_UPDATE_FETCH_FAILED", detail=(fetch.stderr or fetch.stdout)[-1200:])
        return False
    changed = []
    for rel, target in [
        ("local/dore-local/resident_runtime.py", SELF),
        ("local/dore-local/autonomous_driver.py", DRIVER),
    ]:
        show = run(["git", "show", f"origin/main:{rel}"], timeout=60)
        if show.returncode != 0:
            continue
        remote_text = show.stdout
        local_text = target.read_text(encoding="utf-8") if target.exists() else ""
        if remote_text != local_text:
            tmp = target.with_suffix(target.suffix + ".remote")
            tmp.write_text(remote_text, encoding="utf-8")
            tmp.replace(target)
            changed.append(rel)
    if changed:
        append_event("SELF_UPDATED", files=changed, source="origin/main")
        publish_telemetry(force=True)
        if "local/dore-local/resident_runtime.py" in changed:
            os.execv(sys.executable, [sys.executable, str(SELF)])
    return bool(changed)


def tick() -> None:
    state = read_json(STATE, {}) or {}
    lp, learning = latest_learning()
    learning_fp = fingerprint(learning) if learning else None
    last_progress = float(state.get("last_progress_epoch") or 0)
    elapsed = time.time() - last_progress if last_progress else None

    if learning and learning.get("state") == "RESEARCH_REQUIRED":
        reason = "RESEARCH_REQUIRED"
    elif not state.get("driver_passed"):
        reason = "NO_USER_INPUT_CONTINUE"
    elif elapsed is not None and elapsed >= STALL_AFTER:
        reason = "STALL_DETECTED"
    else:
        atomic_json(HEARTBEAT, {
            "runtime": VERSION,
            "at": now(),
            "state": "IDLE_HEALTHY",
            "parent_goal": PARENT_GOAL,
            "next_tick_seconds": INTERVAL,
        })
        return

    if (
        reason == "RESEARCH_REQUIRED"
        and learning_fp
        and state.get("last_learning_fingerprint") == learning_fp
        and state.get("last_driver_ok") is False
        and state.get("last_attempt_epoch")
        and time.time() - float(state["last_attempt_epoch"]) < STALL_AFTER
    ):
        append_event("WAIT_FOR_INFORMATION_GAIN", parent_goal=PARENT_GOAL, fingerprint=learning_fp)
        return

    append_event("CONTINUE", reason=reason, parent_goal=PARENT_GOAL, learning=str(lp) if lp else None)
    before = time.time()
    result = run_driver(reason, lp, learning)
    progressed = bool(result.get("ok")) or fingerprint(result) != state.get("last_result_fingerprint")
    new_state = {
        **state,
        "runtime": VERSION,
        "parent_goal": PARENT_GOAL,
        "parent_message_id": PARENT_ID,
        "last_event": reason,
        "last_attempt_at": now(),
        "last_attempt_epoch": before,
        "last_driver_ok": bool(result.get("ok")),
        "last_learning_fingerprint": learning_fp,
        "last_result_fingerprint": fingerprint(result),
        "driver_passed": bool(result.get("ok")),
    }
    if progressed:
        new_state["last_progress_at"] = now()
        new_state["last_progress_epoch"] = time.time()
    atomic_json(STATE, new_state)
    atomic_json(HEARTBEAT, {
        "runtime": VERSION,
        "at": now(),
        "state": "PASS" if result.get("ok") else "RUNNING_WITH_FAILURE_EVIDENCE",
        "parent_goal": PARENT_GOAL,
        "last_event": reason,
        "driver_ok": bool(result.get("ok")),
        "next_tick_seconds": INTERVAL,
    })
    append_event(
        "DRIVER_RESULT",
        reason=reason,
        ok=bool(result.get("ok")),
        returncode=result.get("returncode"),
        information_gain=progressed,
        result=(result.get("result") or {}).get("error") if isinstance(result.get("result"), dict) else None,
    )
    publish_telemetry(force=True)


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        append_event("RUNTIME_STARTED", pid=os.getpid(), interval_seconds=INTERVAL, supervisor="launchd", runtime=VERSION)
        while True:
            try:
                maybe_self_update()
                tick()
                publish_telemetry(force=False)
            except subprocess.TimeoutExpired as exc:
                append_event("ACTION_TIMEOUT", command=str(exc.cmd), timeout=exc.timeout)
            except Exception as exc:
                append_event("RUNTIME_ERROR", error=repr(exc))
            time.sleep(INTERVAL)


if __name__ == "__main__":
    raise SystemExit(main())
