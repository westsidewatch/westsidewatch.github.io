#!/usr/bin/env python3
"""Install Doré Resident Runtime as a per-user macOS LaunchAgent.

Uses launchd (built into macOS) as the mature supervisor rather than inventing
another daemon manager. No root privilege and no paid service are required.
"""
from __future__ import annotations

import os
import plistlib
import subprocess
import sys
from pathlib import Path

ROOT = Path(os.environ.get("DORE_REPO_ROOT", Path.home() / "westsidewatch.github.io")).expanduser()
HOME = Path(os.environ.get("DORE_LOCAL_HOME", Path.home() / ".dore")).expanduser()
RUNTIME = ROOT / "local" / "dore-local" / "resident_runtime.py"
LABEL = "org.westsidewatch.dore.runtime"
PLIST = Path.home() / "Library" / "LaunchAgents" / f"{LABEL}.plist"
LOGDIR = HOME / "runtime"


def call(argv, check=False):
    return subprocess.run(argv, text=True, capture_output=True, check=check)


def main() -> int:
    if not RUNTIME.exists():
        print(f"missing runtime: {RUNTIME}", file=sys.stderr)
        return 2
    PLIST.parent.mkdir(parents=True, exist_ok=True)
    LOGDIR.mkdir(parents=True, exist_ok=True)

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
    print(f"plist={PLIST}")
    print(f"python={program}")
    print((status.stdout or status.stderr)[-6000:])
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
