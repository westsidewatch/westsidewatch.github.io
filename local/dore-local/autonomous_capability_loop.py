#!/usr/bin/env python3
"""Doré Autonomous Capability Loop v0.1.

A small durable learning/recovery layer inspired by mature agent patterns:
- Voyager: skill library + curriculum from real work
- Reflexion: failure evidence becomes reusable memory
- LangGraph: explicit durable states and parent-goal resume semantics
- OpenHands Skills: repository-local, executable skills with triggers

This module is intentionally dependency-light so it can sit underneath the resident
coordination worker. It does not use an LLM. It detects known capability gaps,
selects a verified local skill, runs the smallest safe learning action, records
provenance/evidence, and tells the worker whether to resume the parent goal.
Unknown gaps become structured research requests rather than blind retries.
"""
from __future__ import annotations

import json
import os
import re
import subprocess
from datetime import datetime, timezone
from pathlib import Path

HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
STATE_DIR = HOME / "coordination" / "learning"
REGISTRY = ROOT / "dore-design" / "knowledge-lab" / "skills" / "registry.json"


def now() -> str:
    return datetime.now(timezone.utc).isoformat()


def _text_failure(result: dict) -> str:
    parts = []
    for key in ("error", "cause", "failed_stderr", "failed_stdout", "stderr", "stdout"):
        value = result.get(key)
        if value:
            parts.append(str(value))
    for item in result.get("results") or []:
        if isinstance(item, dict):
            parts.extend(str(item.get(k) or "") for k in ("stderr", "stdout"))
    return "\n".join(parts)


def _load_registry() -> list[dict]:
    try:
        payload = json.loads(REGISTRY.read_text(encoding="utf-8"))
        return payload.get("skills") or []
    except Exception:
        return []


def _match(skill: dict, text: str) -> bool:
    triggers = skill.get("triggers") or []
    if not triggers:
        return False
    low = text.lower()
    return all(str(t).lower() in low for t in triggers)


def _safe_script(path: str) -> Path:
    target = (ROOT / path).resolve()
    allowed = (ROOT / "dore-design" / "knowledge-lab" / "training").resolve()
    if not (target == allowed or allowed in target.parents):
        raise RuntimeError("learning_script_outside_training_root:" + str(target))
    if target.suffix != ".py" or not target.exists():
        raise RuntimeError("learning_script_unavailable:" + str(target))
    return target


def _persist(message_id: str, record: dict) -> Path:
    STATE_DIR.mkdir(parents=True, exist_ok=True)
    path = STATE_DIR / f"{message_id}.json"
    tmp = path.with_suffix(".tmp")
    tmp.write_text(json.dumps(record, ensure_ascii=False, indent=2), encoding="utf-8")
    tmp.replace(path)
    return path


def attempt_learning_recovery(msg: dict, failure_result: dict) -> dict:
    """Try one evidence-backed local learning action.

    Returns a structured result. `retry_parent=True` means the selected skill was
    verified and the caller should immediately retry the original parent task.
    """
    mid = str(msg.get("message_id") or "unknown")
    parent_goal = str(msg.get("related_goal") or mid)
    failure_text = _text_failure(failure_result)
    base = {
        "loop": "dore.autonomous-capability-loop.v0.1",
        "message_id": mid,
        "parent_goal": parent_goal,
        "observed_at": now(),
        "state": "GAP_DETECTED",
        "parent_goal_preserved": True,
        "failure_fingerprint": re.sub(r"\s+", " ", failure_text)[-4000:],
    }

    skill = next((s for s in _load_registry() if _match(s, failure_text)), None)
    if not skill:
        record = {
            **base,
            "state": "RESEARCH_REQUIRED",
            "retry_parent": False,
            "knowledge_request": {
                "question": "Find a mature, evidence-backed way to resolve this capability gap, create a minimal reusable Doré skill, verify it in isolation, then resume the preserved parent goal.",
                "failure": base["failure_fingerprint"],
                "reuse_before_rebuild": True,
            },
        }
        path = _persist(mid, record)
        return {**record, "evidence_path": str(path)}

    record = {**base, "state": "LEARNING", "selected_skill": skill.get("id"), "provenance": skill.get("provenance") or []}
    _persist(mid, record)
    try:
        script = _safe_script(str(skill["script"]))
        cp = subprocess.run(
            ["python3", str(script)],
            cwd=str(ROOT),
            text=True,
            capture_output=True,
            timeout=min(int(skill.get("timeout") or 180), 900),
        )
        verified = cp.returncode == 0
        record.update({
            "state": "VERIFIED" if verified else "LEARNING_FAILED",
            "retry_parent": verified,
            "skill_returncode": cp.returncode,
            "skill_stdout": (cp.stdout or "")[-12000:],
            "skill_stderr": (cp.stderr or "")[-12000:],
            "verified_at": now() if verified else None,
        })
    except Exception as exc:
        record.update({"state": "LEARNING_FAILED", "retry_parent": False, "error": type(exc).__name__ + ": " + str(exc)})

    path = _persist(mid, record)
    return {**record, "evidence_path": str(path)}


if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser()
    parser.add_argument("--message-id", default="acl-self-test")
    parser.add_argument("--failure", required=True)
    args = parser.parse_args()
    out = attempt_learning_recovery(
        {"message_id": args.message_id, "related_goal": "dore-autonomous-loop-self-test"},
        {"ok": False, "error": args.failure},
    )
    print(json.dumps(out, ensure_ascii=False))
    raise SystemExit(0 if out.get("retry_parent") else 2)
