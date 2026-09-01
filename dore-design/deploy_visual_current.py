#!/usr/bin/env python3
"""Install Doré Design and verify locked #262 design, full editor mode, and preview return entry."""
import json,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;BASE='http://127.0.0.1:4310'
def read(path):return urllib.request.urlopen(BASE+path,timeout=10).read().decode('utf-8')
seed=subprocess.run(['python3','dore-design/workspace_cli.py','get'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if seed.returncode!=0:raise SystemExit('workspace_seed_failed:'+seed.stderr[-1200:])
migration=subprocess.run(['python3','dore-design/upgrade_living_fortress_v2.py'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if migration.returncode!=0:raise SystemExit('workspace_upgrade_failed:'+migration.stderr[-1200:])
result=subprocess.run(['bash','dore-design/install-macos.sh'],cwd=ROOT,text=True,capture_output=True,timeout=120)
if result.returncode!=0:raise SystemExit('install_failed:'+result.stderr[-1200:])
health=json.loads(read('/api/health'));status=json.loads(read('/api/preview/status'));preview=read('/');editor=read('/editor');canvas=read('/editor-canvas');structure=read('/structure-editor');workspace=json.loads(read('/api/workspace'))
markers=['class="hero"','class="city-grid"','class="gate-line"','class="watch"','WATCH<br>FOR THE <em>DAWN.</em>']
checks={
'version_current':health.get('version')=='1.5.2',
'design_locked':health.get('layout_source')=='approved-front-door-262-locked',
'shared_workspace':health.get('preview_mode')=='locked-template-shared-workspace',
'preview_approved_layout':all(m in preview for m in markers),
'canvas_approved_layout':all(m in canvas for m in markers),
'preview_has_editor_entry':'class="dore-preview-edit"' in preview and 'href="/editor"' in preview and 'Edit in Doré Design' in preview,
'preview_entry_status':health.get('preview_edit_entry') is True and status.get('preview_edit_entry') is True,
'editor_mode_visible':'DORÉ DESIGN 1.5.1 · EDITOR' in editor and 'PAGES' in editor and 'LAYERS' in editor and 'INSPECTOR' in editor,
'editor_uses_canvas':'src="/editor-canvas"' in editor,
'canvas_editable':'data-dore-canvas="true"' in canvas and 'data-node-id="home-title"' in canvas,
'structure_preserved':'STRUCTURE' in structure,
'workspace_revision_match':status.get('revision')==workspace.get('revision'),
'workspace_page_match':status.get('page_id')=='homepage',
}
ok=all(checks.values());print(json.dumps({'ok':ok,'code':'DORE_DESIGN_PREVIEW_EDITOR_ENTRY_PASS' if ok else 'DORE_DESIGN_PREVIEW_EDITOR_ENTRY_FAIL','health':health,'preview_status':status,'workspace_revision':workspace.get('revision'),'checks':checks},ensure_ascii=False));raise SystemExit(0 if ok else 1)
