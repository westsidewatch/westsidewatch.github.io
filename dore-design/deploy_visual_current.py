#!/usr/bin/env python3
"""Install the current resident Doré Design surface and verify the visible result."""
import json
import subprocess
import urllib.request
from pathlib import Path

ROOT=Path(__file__).resolve().parent.parent
BASE='http://127.0.0.1:4310'

def read(path): return urllib.request.urlopen(BASE+path,timeout=10).read().decode('utf-8')

seed=subprocess.run(['python3','dore-design/workspace_cli.py','get'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if seed.returncode!=0: raise SystemExit('workspace_seed_failed:'+seed.stderr[-1200:])
migration=subprocess.run(['python3','dore-design/upgrade_living_fortress_v2.py'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if migration.returncode!=0: raise SystemExit('workspace_upgrade_failed:'+migration.stderr[-1200:])
result=subprocess.run(['bash','dore-design/install-macos.sh'],cwd=ROOT,text=True,capture_output=True,timeout=120)
if result.returncode!=0: raise SystemExit('install_failed:'+result.stderr[-1200:])

health=json.loads(read('/api/health'))
preview_status=json.loads(read('/api/preview/status'))
preview=read('/')
editor=read('/editor')
structure=read('/structure-editor')
workspace=json.loads(read('/api/workspace'))
home=next((p for p in workspace.get('pages',[]) if p.get('id')=='homepage'),None)
node_ids={n.get('id') for n in (home or {}).get('nodes',[])}
texts='\n'.join(str(n.get('text',''))+' '+str(n.get('title','')) for n in (home or {}).get('nodes',[]))
checks={
    'version_current':health.get('version')=='1.5',
    'single_source':health.get('source_of_truth')=='structured-workspace',
    'approved_layout_source':health.get('layout_source')=='approved-front-door-262',
    'same_wysiwyg_renderer':health.get('preview_mode')=='same-template-same-workspace-wysiwyg',
    'selected_direction':health.get('design_direction')=='watch-for-the-dawn',
    'preview_exact_layout':'class="city-grid"' in preview and 'class="hero"' in preview and 'class="gate-line"' in preview and 'class="watch"' in preview,
    'editor_exact_layout':'data-dore-editor="true"' in editor and 'DORÉ DESIGN 1.5 · WYSIWYG' in editor and 'class="city-grid"' in editor,
    'editor_has_bindings':'data-node-id="home-title"' in editor and 'data-node-id="journal-tower"' in editor,
    'structure_demoted':'DORÉ DESIGN 1.5 · STRUCTURE' in structure,
    'workspace_surface':workspace.get('active_surface')=='homepage-watch-for-the-dawn-wysiwyg-v4',
    'workspace_layout_source':workspace.get('layout_source')=='approved-front-door-262',
    'approved_hero':'WATCH\nFOR THE\nDAWN.' in texts,
    'approved_destinations':{'journal-tower','one-territory','church-territory','library-territory','join-territory'}.issubset(node_ids),
    'preview_workspace_match':preview_status.get('workspace_id')==workspace.get('id'),
    'preview_revision_match':preview_status.get('revision')==workspace.get('revision'),
    'preview_page_match':preview_status.get('page_id')=='homepage',
}
ok=all(checks.values())
print(json.dumps({'ok':ok,'code':'DORE_DESIGN_WYSIWYG_FRONT_DOOR_PASS' if ok else 'DORE_DESIGN_WYSIWYG_FRONT_DOOR_FAIL','health':health,'preview_status':preview_status,'workspace_revision':workspace.get('revision'),'migration':migration.stdout.strip(),'checks':checks},ensure_ascii=False))
raise SystemExit(0 if ok else 1)
