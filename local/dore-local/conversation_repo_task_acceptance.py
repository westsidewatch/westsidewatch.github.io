#!/usr/bin/env python3
"""End-to-end acceptance for conversation -> A2A -> repo-task execution."""
from __future__ import annotations
import json
import os
import subprocess
import tempfile
from pathlib import Path

import conversation_gateway as gateway

CAPABILITY = "engineering.repo-task"


def git(repo: Path, *args: str) -> None:
    subprocess.run(["git", "-C", str(repo), *args], check=True, stdout=subprocess.DEVNULL)


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="dore-conversation-repo-") as tmp:
        repo = Path(tmp) / "westsidewatch.github.io"
        repo.mkdir()
        git(repo, "init", "-q")
        git(repo, "config", "user.email", "dore@example.invalid")
        git(repo, "config", "user.name", "DoreConversationAcceptance")
        specimen = repo / "specimen.txt"
        specimen.write_text("before\n", encoding="utf-8")
        git(repo, "add", "specimen.txt")
        git(repo, "commit", "-qm", "init")

        old = os.environ.get("DORE_WORKTREE")
        os.environ["DORE_WORKTREE"] = str(repo)
        try:
            discovered = gateway.discover("repo-task")
            caps = discovered.get("capabilities") or []
            found = any(x.get("id") == CAPABILITY and x.get("callable") is True for x in caps)

            described = gateway.describe(CAPABILITY)
            descriptor = described.get("descriptor") or {}
            callable_descriptor = described.get("ok") is True and descriptor.get("callable") is True

            inspected = gateway.call(CAPABILITY, {"operation": "inspect"}, request_id="repo-task-e2e-inspect")
            read = gateway.call(CAPABILITY, {"operation": "read", "path": "specimen.txt"}, request_id="repo-task-e2e-read")
            escape = gateway.call(CAPABILITY, {"operation": "read", "path": "../outside.txt"}, request_id="repo-task-e2e-escape")
            write = gateway.call(CAPABILITY, {"operation": "write", "path": "specimen.txt", "content": "after\n"}, request_id="repo-task-e2e-write")
            verify = gateway.call(CAPABILITY, {"operation": "verify", "verb": "diff-check"}, request_id="repo-task-e2e-verify")

            checks = {
                "discover_callable": found,
                "describe_callable": callable_descriptor,
                "inspect": inspected.get("ok") is True,
                "read": read.get("ok") is True,
                "path_escape_rejected": escape.get("ok") is False,
                "write": write.get("ok") is True,
                "diff_check": verify.get("ok") is True,
                "filesystem_changed": specimen.read_text(encoding="utf-8") == "after\n",
            }
            ok = all(checks.values())
            print(json.dumps({"ok": ok, "capability": CAPABILITY, "path": "conversation-gateway->native-host->a2a->capability-bus->repo-task-runtime", "checks": checks}, separators=(",", ":")))
            return 0 if ok else 1
        finally:
            if old is None:
                os.environ.pop("DORE_WORKTREE", None)
            else:
                os.environ["DORE_WORKTREE"] = old


if __name__ == "__main__":
    raise SystemExit(main())
