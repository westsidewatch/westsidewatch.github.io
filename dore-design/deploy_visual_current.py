#!/usr/bin/env python3
"""Install Doré Design 1.7.1 and prove Journal editability plus import fidelity."""
import json,subprocess,urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parent.parent;BASE='http://127.0.0.1:4310'
def read(path):return urllib.request.urlopen(BASE+path,timeout=12).read().decode('utf-8')
def raw(path):return urllib.request.urlopen(BASE+path,timeout=12).read()
def post(payload):
 r=urllib.request.Request(BASE+'/api/workspace',data=json.dumps(payload).encode(),headers={'Content-Type':'application/json'},method='POST')
 return json.loads(urllib.request.urlopen(r,timeout=12).read().decode('utf-8'))
seed=subprocess.run(['python3','dore-design/workspace_cli.py','get'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if seed.returncode!=0:raise SystemExit('workspace_seed_failed:'+seed.stderr[-1200:])
home=subprocess.run(['python3','dore-design/upgrade_living_fortress_v2.py'],cwd=ROOT,text=True,capture_output=True,timeout=60)
if home.returncode!=0:raise SystemExit('workspace_upgrade_failed:'+home.stderr[-1200:])
journal_import=subprocess.run(['python3','dore-design/journal_import.py'],cwd=ROOT,text=True,capture_output=True,timeout=150)
if journal_import.returncode!=0:raise SystemExit('journal_import_failed:'+journal_import.stderr[-3000:]+journal_import.stdout[-1500:])
install=subprocess.run(['bash','dore-design/install-macos.sh'],cwd=ROOT,text=True,capture_output=True,timeout=120)
if install.returncode!=0:raise SystemExit('install_failed:'+install.stderr[-1600:])
health=json.loads(read('/api/health'));status=json.loads(read('/api/preview/status'));jstatus=json.loads(read('/api/journal/status'));preview=read('/');editor=read('/editor?page=journal-vol-00');home_canvas=read('/editor-canvas?page=homepage');journal_canvas=read('/editor-canvas?page=journal-vol-00');journal=read('/journal/');workspace=json.loads(read('/api/workspace'))
home_markers=['class="hero"','class="city-grid"','class="gate-line"','class="watch"','WATCH<br>FOR THE <em>DAWN.</em>']
jpage=next((p for p in workspace.get('pages',[]) if p.get('id')=='journal-vol-00'),None)
probe_ok=False;restored=False
if jpage and jpage.get('nodes'):
 n=next((x for x in jpage['nodes'] if x.get('type')=='text' and x.get('text')),jpage['nodes'][0]);original=n.get('text','');marker=' [DORÉ EDIT PROBE]'
 post({'op':'set_node','page_id':'journal-vol-00','id':n['id'],'patch':{'text':original+marker}})
 probe_ok=marker in read('/journal/')
 post({'op':'set_node','page_id':'journal-vol-00','id':n['id'],'patch':{'text':original}})
 restored=marker not in read('/journal/')
asset_ok=False
try:asset_ok=len(raw('/images/westside-watch-morning-star.svg'))>100
except Exception:asset_ok=False
checks={
 'version_current':health.get('version')=='1.7.1',
 'homepage_locked':health.get('layout_source')=='approved-front-door-262-locked' and all(m in preview for m in home_markers) and all(m in home_canvas for m in home_markers),
 'multi_page_mode':health.get('preview_mode')=='multi-page-shared-workspace' and status.get('mode')=='multi-page-shared-workspace',
 'journal_workspace_page':bool(jpage) and jpage.get('renderer')=='journal-imported-dom-v2' and len(jpage.get('nodes',[]))>=20,
 'journal_editable_status':health.get('journal_mode')=='editable-workspace-page' and health.get('runtime_mirror') is False and jstatus.get('editable') is True and jstatus.get('runtime_mirror') is False,
 'journal_preview_bound':'data-dore-page="journal-vol-00"' in journal and 'dore-journal-bound' in journal,
 'journal_canvas_editable':'data-dore-canvas="true"' in journal_canvas and 'data-dore-page="journal-vol-00"' in journal_canvas and 'contentEditable' in journal_canvas,
 'editor_multi_page':'MULTI-PAGE EDITOR' in editor and 'journal-vol-00' in editor and 'PAGES' in editor and 'INSPECTOR' in editor,
 'homepage_links_journal':'href="/journal/"' in preview,
 'workspace_mutation_drives_journal':probe_ok and restored,
 'journal_slogan_preserved':'Watch for the Dawn' in journal and '<p class="hero__watchword"><span></span><em><dore-text' in journal,
 'journal_asset_fallback':health.get('journal_asset_fallback')=='package+repo-static' and jstatus.get('asset_fallback')=='package+repo-static' and asset_ok,
}
ok=all(checks.values());print(json.dumps({'ok':ok,'code':'DORE_DESIGN_JOURNAL_FIDELITY_PASS' if ok else 'DORE_DESIGN_JOURNAL_FIDELITY_FAIL','health':health,'journal_status':jstatus,'journal_import':journal_import.stdout[-1000:],'workspace_revision':workspace.get('revision'),'journal_node_count':len(jpage.get('nodes',[])) if jpage else 0,'checks':checks},ensure_ascii=False));raise SystemExit(0 if ok else 1)
