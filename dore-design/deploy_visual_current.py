#!/usr/bin/env python3
"""Install Doré Design and verify locked homepage plus complete main-site Journal."""
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
health=json.loads(read('/api/health'));status=json.loads(read('/api/preview/status'));mirror=json.loads(read('/api/mirror/status'));preview=read('/');editor=read('/editor');canvas=read('/editor-canvas');journal=read('/journal/');journal_index=read('/journal-index/');structure=read('/structure-editor');workspace=json.loads(read('/api/workspace'))
home_markers=['class="hero"','class="city-grid"','class="gate-line"','class="watch"','WATCH<br>FOR THE <em>DAWN.</em>']
journal_markers=['id="vol-00-proclamation"','id="contents"','id="movement-watch"','Opening declaration','Continue reading']
checks={
'version_current':health.get('version')=='1.6',
'design_locked':health.get('layout_source')=='approved-front-door-262-locked',
'shared_workspace':health.get('preview_mode')=='locked-template-shared-workspace',
'preview_approved_layout':all(m in preview for m in home_markers),
'canvas_approved_layout':all(m in canvas for m in home_markers),
'preview_has_editor_entry':'class="dore-preview-edit"' in preview and 'href="/editor"' in preview,
'homepage_journal_link':'href="/journal/"' in preview,
'journal_full_issue':all(m in journal for m in journal_markers),
'journal_inside_design':'class="dore-journal-nav"' in journal and 'href="/editor"' in journal and 'href="/"' in journal,
'journal_mode':health.get('journal_mode')=='full-main-site-journal-in-design' and status.get('journal_full_issue') is True and mirror.get('mode')=='full-main-site-journal-in-design',
'journal_index_preserved':'issue-door' in journal_index and 'journal-quicklinks' in journal_index,
'editor_mode_visible':'EDITOR' in editor and 'PAGES' in editor and 'LAYERS' in editor and 'INSPECTOR' in editor,
'editor_uses_canvas':'src="/editor-canvas"' in editor,
'canvas_editable':'data-dore-canvas="true"' in canvas and 'data-node-id="home-title"' in canvas,
'structure_preserved':'STRUCTURE' in structure,
'workspace_revision_match':status.get('revision')==workspace.get('revision'),
'workspace_page_match':status.get('page_id')=='homepage',
}
ok=all(checks.values());print(json.dumps({'ok':ok,'code':'DORE_DESIGN_FULL_JOURNAL_PASS' if ok else 'DORE_DESIGN_FULL_JOURNAL_FAIL','health':health,'preview_status':status,'mirror_status':mirror,'workspace_revision':workspace.get('revision'),'checks':checks},ensure_ascii=False));raise SystemExit(0 if ok else 1)
