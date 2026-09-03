#!/usr/bin/env python3
"""Install/repair Doré Resident Runtime as a per-user macOS LaunchAgent.

This installer is also the bootstrap repair path for a stale resident runtime.
Before launch it explicitly advances refs/remotes/origin/main, synchronizes the
runtime-control manifest and every declared control file from that ref, then
restarts launchd. This avoids the historical bootstrap trap where
`git fetch origin main` refreshed FETCH_HEAD but left origin/main stale.
"""
from __future__ import annotations

import json
import os
import plistlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
PRODUCT_ROOT = Path(os.environ.get("DORE_PRODUCT_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
RUNTIME = ROOT / "local" / "dore-local" / "resident_runtime.py"
MANIFEST_REL = "dore-design/knowledge-lab/a2a/runtime-control-manifest.json"
LABEL = "org.westsidewatch.dore.runtime"
PLIST = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOGDIR = HOME / "runtime"


def call(argv, check=False):
    return subprocess.run(argv, cwd=str(ROOT), text=True, capture_output=True, check=check)


def git_show(rel: str) -> str | None:
    cp = call(["git", "show", f"origin/main:{rel}"])
    return cp.stdout if cp.returncode == 0 else None


def sync_from_origin_main() -> list[str]:
    fetch = call(["git", "fetch", "origin", "+refs/heads/main:refs/remotes/origin/main"])
    if fetch.returncode != 0:
        raise RuntimeError("bootstrap_fetch_failed: " + (fetch.stderr or fetch.stdout)[-2000:])

    manifest_text = git_show(MANIFEST_REL)
    if not manifest_text:
        raise RuntimeError("bootstrap_manifest_unavailable")
    manifest = json.loads(manifest_text)
    rels = [MANIFEST_REL, *[str(x) for x in manifest.get("files", []) if isinstance(x, str)]]
    changed: list[str] = []
    for rel in dict.fromkeys(rels):
        remote = git_show(rel)
        if remote is None:
            continue
        target = ROOT / rel
        local = target.read_text(encoding="utf-8") if target.exists() else ""
        if local == remote:
            continue
        target.parent.mkdir(parents=True, exist_ok=True)
        tmp = target.with_suffix(target.suffix + ".bootstrap")
        tmp.write_text(remote, encoding="utf-8")
        tmp.replace(target)
        changed.append(rel)
    return changed


def main() -> int:
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)

    try:
        changed = sync_from_origin_main()
    except Exception as exc:
        print(f"DORE_BOOTSTRAP_SYNC_FAILED: {exc}", file=sys.stderr)
        return 3

    if not RUNTIME.exists():
        print(f"missing runtime after bootstrap sync: {RUNTIME}", file=sys.stderr)
        return 2

    program = sys.executable
    payload = {
        "Label": LABEL,
        "ProgramArguments": [program, str(RUNTIME)],
        "WorkingDirectory": str(ROOT),
        "RunAtLoad": True,
        "KeepAlive": True,
        "ProcessType": "Background",
        "ThrottleInterval": 10,
        "StandardOutPath": str(LOGDIR / "launchd.stdout.log"),
        "StandardErrorPath": str(LOGDIR / "launchd.stderr.log"),
        "EnvironmentVariables": {
            "DORE_REPO_ROOT": str(ROOT),
            "DORE_PRODUCT_ROOT": str(PRODUCT_ROOT),
            "DORE_LOCAL_HOME": str(HOME),
            "DORE_RUNTIME_INTERVAL_SECONDS": os.environ.get("DORE_RUNTIME_INTERVAL_SECONDS", "30"),
            "DORE_RUNTIME_STALL_SECONDS": os.environ.get("DORE_RUNTIME_STALL_SECONDS", "90"),
        },
    }
    with PLIST.open("wb") as f:
        plistlib.dump(payload, f, sort_keys=False)

    uid = os.getuid()
    domain = f"gui/{uid}"
    service = f"{domain}/{LABEL}"
    call(["launchctl", "bootout", domain, str(PLIST)])
    boot = call(["launchctl", "bootstrap", domain, str(PLIST)])
    if boot.returncode != 0:
        print(boot.stderr or boot.stdout, file=sys.stderr)
        return boot.returncode
    kick = call(["launchctl", "kickstart", "-k", service])
    if kick.returncode != 0:
        print(kick.stderr or kick.stdout, file=sys.stderr)
        return kick.returncode
    status = call(["launchctl", "print", service])
    print("DORE_RESIDENT_RUNTIME_INSTALLED")
    print("bootstrap_sync=PASS")
    print("synced_files=" + json.dumps(changed, ensure_ascii=False))
    print(f"plist={PLIST}")
    print(f"python={program}")
    print((status.stdout or status.stderr)[-6000:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
