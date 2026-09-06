#!/usr/bin/env python3
"""Install/update the DORÉ wake worker LaunchAgent on macOS.

Stdlib-only and idempotent. It writes a user LaunchAgent that invokes the short-lived
wake worker every 15 minutes and whenever the trigger directory is non-empty.
"""
from __future__ import annotations

import argparse
import os
import plistlib
import subprocess
import sys
from pathlib import Path

LABEL = 'org.westsidewatch.dore.wake'


def build_plist(runtime: Path, db: Path, trigger_dir: Path, log_dir: Path) -> dict:
    return {
        'Label': LABEL,
        'ProgramArguments': [
            sys.executable,
            str(runtime),
            '--db',
            str(db),
            'run-once',
            '--limit',
            '3',
        ],
        'StartInterval': 900,
        'QueueDirectories': [str(trigger_dir)],
        'RunAtLoad': True,
        'ProcessType': 'Background',
        'LowPriorityIO': True,
        'ThrottleInterval': 30,
        'StandardOutPath': str(log_dir / 'wake.out.log'),
        'StandardErrorPath': str(log_dir / 'wake.err.log'),
    }


def main() -> int:
    if sys.platform != 'darwin':
        print('This installer is for macOS launchd.', file=sys.stderr)
        return 2
    parser = argparse.ArgumentParser()
    parser.add_argument('--repo', default=str(Path(__file__).resolve().parents[2]))
    args = parser.parse_args()
    repo = Path(args.repo).expanduser().resolve()
    runtime = repo / 'dore-core/runtime/wake_runtime.py'
    app = Path.home() / 'Library/Application Support/Dore'
    db = app / 'wake-state.sqlite3'
    trigger_dir = app / 'wake-triggers'
    log_dir = app / 'logs'
    agents = Path.home() / 'Library/LaunchAgents'
    for p in (app, trigger_dir, log_dir, agents):
        p.mkdir(parents=True, exist_ok=True)
    plist_path = agents / f'{LABEL}.plist'
    with plist_path.open('wb') as fh:
        plistlib.dump(build_plist(runtime, db, trigger_dir, log_dir), fh, sort_keys=True)
    subprocess.run([sys.executable, str(runtime), '--db', str(db), 'init'], check=True)
    uid = os.getuid()
    domain = f'gui/{uid}'
    subprocess.run(['/bin/launchctl', 'bootout', domain, str(plist_path)], check=False, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    subprocess.run(['/bin/launchctl', 'bootstrap', domain, str(plist_path)], check=True)
    subprocess.run(['/bin/launchctl', 'enable', f'{domain}/{LABEL}'], check=True)
    subprocess.run(['/bin/launchctl', 'kickstart', '-k', f'{domain}/{LABEL}'], check=True)
    print(f'installed {LABEL}: {plist_path}')
    return 0


if __name__ == '__main__':
    raise SystemExit(main())
