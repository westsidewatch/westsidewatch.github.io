#!/usr/bin/env python3
"""Owner-only GitHub Issue relay into the local DORÉ Unix-socket control plane."""
from __future__ import annotations

import json
import os
import re
import urllib.request
from pathlib import Path

HERE = Path(__file__).resolve().parent
import sys
if str(HERE) not in sys.path:
    sys.path.insert(0, str(HERE))

from unix_rpc_client import call  # noqa: E402

PROTOCOL = "dore.a2a/1"
TITLE_PREFIX = "[DORÉ A2A]"
CAP_RE = re.compile(r"^[A-Za-z0-9_.-]{1,128}$")
MAX_COMMENT_BYTES = 60000


def fail(message: str) -> dict:
    return {"ok": False, "protocol": PROTOCOL, "status": "failed", "error": message}


def post_comment(repo: str, issue_number: str, token: str, payload: dict) -> None:
    marker = "[DORÉ_LOCAL_RESULT " + json.dumps(payload, ensure_ascii=False, separators=(",", ":")) + "]"
    raw = json.dumps({"body": marker}, ensure_ascii=False).encode("utf-8")
    if len(raw) > MAX_COMMENT_BYTES:
        payload = fail("result_too_large")
        marker = "[DORÉ_LOCAL_RESULT " + json.dumps(payload, separators=(",", ":")) + "]"
        raw = json.dumps({"body": marker}).encode("utf-8")
    req = urllib.request.Request(
        f"https://api.github.com/repos/{repo}/issues/{issue_number}/comments",
        data=raw,
        method="POST",
        headers={
            "Authorization": f"Bearer {token}",
            "Accept": "application/vnd.github+json",
            "X-GitHub-Api-Version": "2022-11-28",
            "Content-Type": "application/json",
            "User-Agent": "dore-a2a-github-relay",
        },
    )
    with urllib.request.urlopen(req, timeout=20) as response:
        if response.status not in (200, 201):
            raise RuntimeError(f"comment_http_{response.status}")


def main() -> int:
    repo = os.environ.get("GITHUB_REPOSITORY", "")
    actor = os.environ.get("GITHUB_ACTOR", "")
    title = os.environ.get("DORE_ISSUE_TITLE", "")
    body = os.environ.get("DORE_ISSUE_BODY", "")
    issue_number = os.environ.get("DORE_ISSUE_NUMBER", "")
    token = os.environ.get("GITHUB_TOKEN", "")

    owner = repo.split("/", 1)[0] if "/" in repo else ""
    result: dict
    try:
        if not repo or not issue_number or not token:
            raise ValueError("missing_github_context")
        if actor != owner:
            raise PermissionError("actor_not_repository_owner")
        if not title.startswith(TITLE_PREFIX):
            raise PermissionError("invalid_title_prefix")
        command = json.loads(body)
        if not isinstance(command, dict):
            raise ValueError("body_must_be_json_object")
        if command.get("protocol") != PROTOCOL:
            raise ValueError("invalid_protocol")
        request_id = str(command.get("request_id") or "").strip()
        capability = str(command.get("capability") or "").strip()
        args = command.get("args", {})
        if not request_id or len(request_id) > 128:
            raise ValueError("invalid_request_id")
        if not CAP_RE.fullmatch(capability):
            raise ValueError("invalid_capability")
        if not isinstance(args, dict):
            raise ValueError("args_must_be_object")

        rpc = call("dore.call", {"capability": capability, "args": args})
        result = {
            "ok": "result" in rpc,
            "protocol": PROTOCOL,
            "request_id": request_id,
            "capability": capability,
            "rpc": rpc,
        }
    except Exception as exc:
        result = fail(f"{type(exc).__name__}:{exc}")

    print(json.dumps(result, ensure_ascii=False, indent=2))
    if repo and issue_number and token:
        post_comment(repo, issue_number, token, result)
    return 0 if result.get("ok") else 1


if __name__ == "__main__":
    raise SystemExit(main())
