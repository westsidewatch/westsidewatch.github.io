#!/usr/bin/env python3
"""Run the experimental runtime probe against the GOOD TV acceptance sample.
This is intentionally branch-only and does not download media."""
import json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
PROBE=ROOT/"dore-core"/"tools"/"video_runtime_probe.py"
URL="https://www.goodtv.tv/watch?episode=80467"
p=subprocess.run([sys.executable,str(PROBE),URL,"--timeout-ms","20000"],cwd=ROOT,text=True,capture_output=True,timeout=45)
print(p.stdout or p.stderr)
sys.exit(p.returncode)
