#!/usr/bin/env python3
"""Install the current resident Doré Design surface and verify the visible result."""
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BASE='http://127.0.0.1:4310'


def read(path):
    return urllib.request.urlopen(BASE+path,timeout=10).read().decode('utf-8')


seed=subprocess.run(
    ['python3','dore-design/workspace_cli.py','get'],
    cwd=ROOT,text=True,capture_output=True,timeout=60
)
if seed.returncode!=0:
    raise SystemExit('workspace_seed_failed:'+seed.stderr[-1200:])
migration=subprocess.run(
    ['python3','dore-design/upgrade_living_fortress_v2.py'],
    cwd=ROOT,text=True,capture_output=True,timeout=60
)
if migration.returncode!=0:
    raise SystemExit('workspace_upgrade_failed:'+migration.stderr[-1200:])

result=subprocess.run(
    ['bash','dore-design/install-macos.sh'],
    cwd=ROOT,text=True,capture_output=True,timeout=120
)
if result.returncode!=0:
    raise SystemExit('install_failed:'+result.stderr[-1200:])

health=json.loads(read('/api/health'))
homepage=read('/')
editor=read('/editor')
workspace=json.loads(read('/api/workspace'))
checks={
    'version_current':health.get('version')=='1.3',
    'living_fortress_default':health.get('default_surface')=='homepage-v2-living-fortress',
    'selected_direction':health.get('design_direction')=='A-living-fortress',
    'homepage_v2_marker':'data-design="living-fortress-v2"' in homepage,
    'living_fortress_marker':'A · LIVING FORTRESS / HOMEPAGE V2' in homepage,
    'journal_is_portal':'Journal 是城中的展覽，不是整座城' in homepage,
    'structured_editor_preserved':'DORÉ DESIGN 1.3 · STRUCTURE EDITOR' in editor,
    'workspace_surface':workspace.get('active_surface')=='homepage-v2-living-fortress',
    'workspace_direction':workspace.get('design_direction')=='A-living-fortress',
    'workspace_homepage_v2':any(
        p.get('id')=='homepage' and any(n.get('id')=='one-territory' for n in p.get('nodes',[]))
        for p in workspace.get('pages',[])
    ),
}
ok=all(checks.values())
print(json.dumps({
    'ok':ok,
    'code':'DORE_DESIGN_LIVING_FORTRESS_PASS' if ok else 'DORE_DESIGN_LIVING_FORTRESS_FAIL',
    'health':health,
    'workspace_revision':workspace.get('revision'),
    'migration':migration.stdout.strip(),
    'checks':checks,
},ensure_ascii=False))
raise SystemExit(0 if ok else 1)
