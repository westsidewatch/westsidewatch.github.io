#!/usr/bin/env python3
"""Acceptance: exercise GOOD TV through the formal Video Acquisition Adapter probe path. No media download."""
import json, pathlib, subprocess, sys
ROOT=pathlib.Path(__file__).resolve().parents[2]
ADAPTER=ROOT/"dore-core"/"tools"/"video_acquisition.py"
URL="https://www.goodtv.tv/watch?episode=80467"
p=subprocess.run([sys.executable,str(ADAPTER),"probe",URL],cwd=ROOT,text=True,capture_output=True,timeout=60)
raw=(p.stdout or p.stderr).strip()
print(raw)
if p.returncode: sys.exit(p.returncode)
try: data=json.loads(raw)
except Exception: sys.exit(2)
ok=data.get("engine")=="N_m3u8DL-RE" and bool(data.get("manifest_candidates")) and data.get("runtime",{}).get("engine")=="playwright-runtime"
sys.exit(0 if ok else 3)
