#!/usr/bin/env python3
import json, subprocess, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent
r=subprocess.run(['bash','dore-design/install-macos.sh'],cwd=ROOT,text=True,capture_output=True,timeout=120)
if r.returncode!=0:
    raise SystemExit('install_failed:'+r.stderr[-1000:])
health=json.loads(urllib.request.urlopen('http://127.0.0.1:4310/api/health',timeout=10).read().decode())
html=urllib.request.urlopen('http://127.0.0.1:4310/',timeout=10).read().decode()
editor=urllib.request.urlopen('http://127.0.0.1:4310/editor',timeout=10).read().decode()
checks={
 'version_11':health.get('version')=='1.1',
 'real_homepage_default':health.get('default_surface')=='real-homepage-v1',
 'homepage_marker':'A WALL' in html and 'CURRENT JOURNAL' in html,
 'editor_link':'EDIT IN DORÉ DESIGN' in html,
 'structured_editor_preserved':'STRUCTURE EDITOR' in editor,
}
print(json.dumps({'ok':all(checks.values()),'code':'NEW_WESTSIDE_VISUAL_SURFACE_PASS' if all(checks.values()) else 'NEW_WESTSIDE_VISUAL_SURFACE_FAIL','health':health,'checks':checks},ensure_ascii=False))
raise SystemExit(0 if all(checks.values()) else 1)
