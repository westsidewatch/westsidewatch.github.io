#!/usr/bin/env python3
"""Doré Resident Runtime v0.1.

A small, dependency-free resident control loop for macOS.

Design sources adapted, not re-invented:
- macOS launchd owns process supervision and restart.
- Microsoft Agent Framework autonomous handoff inspires NO_USER_INPUT -> CONTINUE.
- A2A task semantics inspire durable state/event separation from any chat connection.
- LangGraph/Temporal ideas inspire checkpoint-before-action and resume-after-failure.

This runtime does not require a chat window. It owns the cadence, persists a heartbeat,
classifies STALL / RESEARCH_REQUIRED / PASS, invokes the autonomous driver, and records
what happened. Unknown technical gaps are not a HUMAN_GATE by default.
"""
from __future__ import annotations

import fcntl
import hashlib
import json
import os
import subprocess
import sys
import time
from datetime import datetime, timezone
from pathlib import Path

HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
RUNTIME = HOME / "runtime"
LEARNING = HOME / "coordination" / "learning"
DRIVER = ROOT / "local" / "dore-local" / "autonomous_driver.py"
STATE = RUNTIME / "state.json"
EVENTS = RUNTIME / "events.jsonl"
HEARTBEAT = RUNTIME / "heartbeat.json"
LOCK = RUNTIME / "runtime.lock"
INTERVAL = max(10, int(os.environ.get("DORE_RUNTIME_INTERVAL_SECONDS", "30")))
STALL_AFTER = max(INTERVAL * 2, int(os.environ.get("DORE_RUNTIME_STALL_SECONDS", "90")))
PARENT_ID = os.environ.get("DORE_RUNTIME_PARENT_ID", "new-westside-storybook-real-loop-2")
PARENT_GOAL = os.environ.get("DORE_RUNTIME_PARENT_GOAL", "New Westside visual construction")


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


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
        "schema": "dore.runtime.v0.1",
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
            "runtime": "dore.resident-runtime.v0.1",
            "at": now(),
            "state": "IDLE_HEALTHY",
            "parent_goal": PARENT_GOAL,
            "next_tick_seconds": INTERVAL,
        })
        return

    # No-information-gain guard: do not hammer the same terminally failed evidence every tick.
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
        "runtime": "dore.resident-runtime.v0.1",
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
        "runtime": "dore.resident-runtime.v0.1",
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


def main() -> int:
    RUNTIME.mkdir(parents=True, exist_ok=True)
    with LOCK.open("w") as lock_file:
        try:
            fcntl.flock(lock_file.fileno(), fcntl.LOCK_EX | fcntl.LOCK_NB)
        except BlockingIOError:
            return 0
        append_event("RUNTIME_STARTED", pid=os.getpid(), interval_seconds=INTERVAL, supervisor="launchd")
        while True:
            try:
                tick()
            except subprocess.TimeoutExpired as exc:
                append_event("ACTION_TIMEOUT", command=str(exc.cmd), timeout=exc.timeout)
            except Exception as exc:
                append_event("RUNTIME_ERROR", error=repr(exc))
            time.sleep(INTERVAL)


if __name__ == "__main__":
    raise SystemExit(main())
