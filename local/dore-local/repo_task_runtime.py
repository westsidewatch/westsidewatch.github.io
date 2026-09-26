#!/usr/bin/env python3
"""Doré Local Agent Runtime v0: bounded repo execution substrate.

This module deliberately does not expose an unrestricted shell. Every operation
is rooted inside an explicitly allowlisted repository and commands are selected
from a fixed verb table.
"""
from __future__ import annotations

import json
import os
import subprocess
import sys
from pathlib import Path
from typing import Any

CAPABILITY = "engineering.repo-task"
DEFAULT_REPO_NAME = "westsidewatch.github.io"
MAX_READ_BYTES = 1_000_000
MAX_OUTPUT = 12_000


def _repo() -> Path:
    root = Path(os.environ.get("DORE_WORKTREE") or os.environ.get("DORE_REPO_ROOT") or Path.home() / DEFAULT_REPO_NAME).expanduser().resolve()
    if root.name != DEFAULT_REPO_NAME or not (root / ".git").exists():
        raise RuntimeError("repo_not_allowlisted")
    return root


def _inside(repo: Path, relative: str) -> Path:
    if not relative or relative.startswith("/"):
        raise ValueError("relative_path_required")
    target = (repo / relative).resolve()
    if target != repo and repo not in target.parents:
        raise ValueError("path_outside_repo")
    return target


def _run(repo: Path, argv: list[str], timeout: int = 120) -> dict[str, Any]:
    proc = subprocess.run(argv, cwd=repo, text=True, capture_output=True, timeout=timeout)
    return {
        "argv": argv,
        "returncode": proc.returncode,
        "stdout": proc.stdout[-MAX_OUTPUT:],
        "stderr": proc.stderr[-MAX_OUTPUT:],
    }


def _command(repo: Path, verb: str) -> dict[str, Any]:
    commands = {
        "status": ["git", "status", "--short"],
        "diff": ["git", "diff", "--"],
        "diff-check": ["git", "diff", "--check"],
        "head": ["git", "rev-parse", "HEAD"],
    }
    argv = commands.get(verb)
    if argv is None:
        return {"ok": False, "error": "command_not_allowlisted", "verb": verb}
    result = _run(repo, argv)
    return {"ok": result["returncode"] == 0, "result": result}


def execute(args: dict[str, Any] | None = None) -> dict[str, Any]:
    args = args or {}
    try:
        repo = _repo()
    except Exception as exc:
        return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": str(exc)}

    op = str(args.get("operation") or "inspect")
    try:
        if op == "inspect":
            status = _command(repo, "status")
            head = _command(repo, "head")
            return {"ok": status["ok"] and head["ok"], "status": "completed", "capability": CAPABILITY, "repo": str(repo), "git_status": status, "head": head}

        if op == "read":
            path = _inside(repo, str(args.get("path") or ""))
            if not path.is_file():
                raise FileNotFoundError(str(path))
            if path.stat().st_size > MAX_READ_BYTES:
                raise ValueError("file_too_large")
            return {"ok": True, "status": "completed", "capability": CAPABILITY, "path": str(path.relative_to(repo)), "content": path.read_text(encoding="utf-8")}

        if op == "write":
            path = _inside(repo, str(args.get("path") or ""))
            content = args.get("content")
            if not isinstance(content, str):
                raise ValueError("content_must_be_string")
            if len(content.encode("utf-8")) > MAX_READ_BYTES:
                raise ValueError("content_too_large")
            if not path.exists():
                raise ValueError("v0_refuses_new_file_write")
            before = path.read_text(encoding="utf-8")
            path.write_text(content, encoding="utf-8")
            check = _command(repo, "diff-check")
            diff = _command(repo, "diff")
            if not check["ok"]:
                path.write_text(before, encoding="utf-8")
                return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": "git_diff_check_failed", "rolled_back": True, "check": check}
            return {"ok": True, "status": "completed", "capability": CAPABILITY, "path": str(path.relative_to(repo)), "diff": diff, "check": check}

        if op == "verify":
            verb = str(args.get("verb") or "diff-check")
            result = _command(repo, verb)
            return {"ok": result["ok"], "status": "completed" if result["ok"] else "failed", "capability": CAPABILITY, "verification": result}

        return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": "operation_not_allowlisted", "operation": op}
    except Exception as exc:
        return {"ok": False, "status": "failed", "capability": CAPABILITY, "error": f"{type(exc).__name__}:{exc}"}


def main() -> int:
    try:
        payload = json.loads(sys.stdin.read() or "{}")
    except json.JSONDecodeError as exc:
        print(json.dumps({"ok": False, "error": f"invalid_json:{exc}"}))
        return 2
    result = execute(payload)
    print(json.dumps(result, ensure_ascii=False, separators=(",", ":")))
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
