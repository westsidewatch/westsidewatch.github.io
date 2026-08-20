#!/usr/bin/env python3
"""Publish one Doré/ONE image binary directly through the GitHub Git Data API.

This is the canonical no-fragment publisher for generated Doré assets.
It accepts a real local file path, verifies the image, creates one Git blob,
adds/replaces the target path in a tree, creates a commit, and advances a branch.

Required environment:
  GITHUB_TOKEN   token with contents:write

Example:
  python tools/dore_publish_binary.py \
    --repo westsidewatch/westsidewatch.github.io \
    --branch dore/lamentations-03-hq \
    --source /work/lamentations-03.png \
    --target static/one/studio/lamentations-03-dore-master.png \
    --message 'asset(one): publish Lamentations 3 Doré master'
"""

from __future__ import annotations

import argparse
import base64
import hashlib
import json
import os
from pathlib import Path
import struct
import sys
import urllib.error
import urllib.request

API = "https://api.github.com"
ALLOWED_EXTENSIONS = {".png", ".jpg", ".jpeg", ".webp", ".avif"}


def fail(message: str) -> "NoReturn":
    raise SystemExit(message)


def image_dimensions(data: bytes, suffix: str) -> tuple[int | None, int | None]:
    if suffix == ".png":
        if data[:8] != b"\x89PNG\r\n\x1a\n" or len(data) < 24:
            fail("invalid PNG signature")
        return struct.unpack(">II", data[16:24])
    if suffix in {".jpg", ".jpeg"}:
        if not data.startswith(b"\xff\xd8"):
            fail("invalid JPEG signature")
        i = 2
        while i + 9 < len(data):
            if data[i] != 0xFF:
                i += 1
                continue
            marker = data[i + 1]
            i += 2
            if marker in {0xD8, 0xD9}:
                continue
            if i + 2 > len(data):
                break
            length = int.from_bytes(data[i:i+2], "big")
            if marker in {0xC0, 0xC1, 0xC2, 0xC3, 0xC5, 0xC6, 0xC7, 0xC9, 0xCA, 0xCB, 0xCD, 0xCE, 0xCF}:
                if i + 7 > len(data):
                    break
                return int.from_bytes(data[i+5:i+7], "big"), int.from_bytes(data[i+3:i+5], "big")
            i += length
        return None, None
    if suffix == ".webp":
        if not (data[:4] == b"RIFF" and data[8:12] == b"WEBP"):
            fail("invalid WebP signature")
        return None, None
    if suffix == ".avif":
        if not (len(data) > 12 and data[4:12] in {b"ftypavif", b"ftypavis"}):
            fail("invalid AVIF signature")
        return None, None
    return None, None


def request_json(method: str, url: str, token: str, payload: dict | None = None) -> dict:
    body = None if payload is None else json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(
        url,
        data=body,
        method=method,
        headers={
            "Accept": "application/vnd.github+json",
            "Authorization": f"Bearer {token}",
            "X-GitHub-Api-Version": "2022-11-28",
            "User-Agent": "westsidewatch-dore-binary-publisher",
            "Content-Type": "application/json",
        },
    )
    try:
        with urllib.request.urlopen(req) as response:
            return json.loads(response.read())
    except urllib.error.HTTPError as exc:
        detail = exc.read().decode("utf-8", "replace")
        fail(f"GitHub API {exc.code}: {detail}")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--repo", required=True, help="owner/repository")
    parser.add_argument("--branch", default="main")
    parser.add_argument("--source", required=True)
    parser.add_argument("--target", required=True)
    parser.add_argument("--message", required=True)
    parser.add_argument("--min-bytes", type=int, default=100_000)
    parser.add_argument("--min-width", type=int, default=900)
    parser.add_argument("--min-height", type=int, default=1400)
    parser.add_argument("--expected-sha256")
    args = parser.parse_args()

    token = os.environ.get("GITHUB_TOKEN")
    if not token:
        fail("GITHUB_TOKEN is required")

    source = Path(args.source)
    if not source.is_file():
        fail(f"source file not found: {source}")
    suffix = source.suffix.lower()
    if suffix not in ALLOWED_EXTENSIONS:
        fail(f"unsupported image extension: {suffix}")

    data = source.read_bytes()
    if len(data) < args.min_bytes:
        fail(f"asset too small for production: {len(data)} < {args.min_bytes} bytes")
    digest = hashlib.sha256(data).hexdigest()
    if args.expected_sha256 and digest != args.expected_sha256.lower():
        fail(f"sha256 mismatch: {digest} != {args.expected_sha256.lower()}")

    width, height = image_dimensions(data, suffix)
    if width is not None and width < args.min_width:
        fail(f"image width too small: {width} < {args.min_width}")
    if height is not None and height < args.min_height:
        fail(f"image height too small: {height} < {args.min_height}")

    repo_url = f"{API}/repos/{args.repo}"
    ref = request_json("GET", f"{repo_url}/git/ref/heads/{args.branch}", token)
    parent_sha = ref["object"]["sha"]
    parent_commit = request_json("GET", f"{repo_url}/git/commits/{parent_sha}", token)
    base_tree = parent_commit["tree"]["sha"]

    blob = request_json(
        "POST",
        f"{repo_url}/git/blobs",
        token,
        {"content": base64.b64encode(data).decode("ascii"), "encoding": "base64"},
    )
    tree = request_json(
        "POST",
        f"{repo_url}/git/trees",
        token,
        {
            "base_tree": base_tree,
            "tree": [
                {
                    "path": args.target,
                    "mode": "100644",
                    "type": "blob",
                    "sha": blob["sha"],
                }
            ],
        },
    )
    commit = request_json(
        "POST",
        f"{repo_url}/git/commits",
        token,
        {"message": args.message, "tree": tree["sha"], "parents": [parent_sha]},
    )
    request_json(
        "PATCH",
        f"{repo_url}/git/refs/heads/{args.branch}",
        token,
        {"sha": commit["sha"], "force": False},
    )

    print(json.dumps({
        "ok": True,
        "source": str(source),
        "target": args.target,
        "bytes": len(data),
        "sha256": digest,
        "width": width,
        "height": height,
        "blob_sha": blob["sha"],
        "commit_sha": commit["sha"],
        "branch": args.branch,
    }, ensure_ascii=False))


if __name__ == "__main__":
    main()
