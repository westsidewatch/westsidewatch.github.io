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
preview_status=json.loads(read('/api/preview/status'))
editor=read('/editor')
workspace=json.loads(read('/api/workspace'))
home=next((p for p in workspace.get('pages',[]) if p.get('id')=='homepage'),None)
node_ids={n.get('id') for n in (home or {}).get('nodes',[])}
texts='\n'.join(str(n.get('text',''))+' '+str(n.get('title','')) for n in (home or {}).get('nodes',[]))
checks={
    'version_current':health.get('version')=='1.4',
    'single_source':health.get('source_of_truth')=='structured-workspace',
    'same_renderer':health.get('preview_mode')=='same-workspace-same-renderer',
    'selected_direction':health.get('design_direction')=='watch-for-the-dawn',
    'structured_editor_preserved':'DORÉ DESIGN 1.4 · STRUCTURE EDITOR' in editor,
    'workspace_surface':workspace.get('active_surface')=='homepage-watch-for-the-dawn-workspace-v3',
    'workspace_direction':workspace.get('design_direction')=='watch-for-the-dawn',
    'approved_hero':'WATCH\nFOR THE\nDAWN.' in texts,
    'approved_destinations':{'journal-tower','one-territory','church-territory','library-territory','join-territory'}.issubset(node_ids),
    'preview_workspace_match':preview_status.get('workspace_id')==workspace.get('id'),
    'preview_revision_match':preview_status.get('revision')==workspace.get('revision'),
    'preview_page_match':preview_status.get('page_id')=='homepage',
}
ok=all(checks.values())
print(json.dumps({
    'ok':ok,
    'code':'DORE_DESIGN_WATCH_FOR_DAWN_PASS' if ok else 'DORE_DESIGN_WATCH_FOR_DAWN_FAIL',
    'health':health,
    'preview_status':preview_status,
    'workspace_revision':workspace.get('revision'),
    'migration':migration.stdout.strip(),
    'checks':checks,
},ensure_ascii=False))
raise SystemExit(0 if ok else 1)
