#!/usr/bin/env python3
from __future__ import annotations
import json
import os
import tempfile
from pathlib import Path
import repo_task_runtime as runtime


def main() -> int:
    with tempfile.TemporaryDirectory(prefix="dore-repo-task-") as tmp:
        repo = Path(tmp) / "westsidewatch.github.io"
        repo.mkdir()
        os.system(f"git -C {repo!s} init -q")
        os.system(f"git -C {repo!s} config user.email dore@example.invalid")
        os.system(f"git -C {repo!s} config user.name DoreAcceptance")
        specimen = repo / "specimen.txt"
        specimen.write_text("before\n", encoding="utf-8")
        os.system(f"git -C {repo!s} add specimen.txt && git -C {repo!s} commit -qm init")
        old = os.environ.get("DORE_WORKTREE")
        os.environ["DORE_WORKTREE"] = str(repo)
        try:
            inspect = runtime.execute({"operation": "inspect"})
            read = runtime.execute({"operation": "read", "path": "specimen.txt"})
            escape = runtime.execute({"operation": "read", "path": "../outside.txt"})
            write = runtime.execute({"operation": "write", "path": "specimen.txt", "content": "after\n"})
            verify = runtime.execute({"operation": "verify", "verb": "diff-check"})
            shell = runtime.execute({"operation": "verify", "verb": "shell"})
            ok = bool(inspect.get("ok") and read.get("ok") and not escape.get("ok") and write.get("ok") and verify.get("ok") and not shell.get("ok") and specimen.read_text() == "after\n")
            print(json.dumps({"ok": ok, "capability": runtime.CAPABILITY, "checks": {"inspect": inspect.get("ok"), "read": read.get("ok"), "path_escape_rejected": not escape.get("ok"), "write": write.get("ok"), "diff_check": verify.get("ok"), "unlisted_command_rejected": not shell.get("ok")}}, separators=(",", ":")))
            return 0 if ok else 1
        finally:
            if old is None:
                os.environ.pop("DORE_WORKTREE", None)
            else:
                os.environ["DORE_WORKTREE"] = old


if __name__ == "__main__":
    raise SystemExit(main())
