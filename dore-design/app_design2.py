#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import os
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design_motion_registry

# Stable runtime identity for A2A/Control Plane verification.
# Values are injected by the launcher when available; safe defaults keep the
# runtime self-identifying without scanning local processes or Git state.
current.DORE_RUNTIME_IDENTITY = {
    'service': 'dore-design',
    'version': '2.0',
    'entrypoint': 'dore-design/app_design2.py',
    'branch': os.environ.get('DORE_GIT_BRANCH', 'unknown'),
    'commit': os.environ.get('DORE_GIT_COMMIT', 'unknown'),
    'workspace_id': os.environ.get('DORE_WORKSPACE_ID', 'westside-watch'),
    'workspace_revision': os.environ.get('DORE_WORKSPACE_REVISION', 'unknown'),
    'port': int(os.environ.get('DORE_DESIGN_PORT', '4310')),
}

# The Codrops 8:5 page is a startup migration. Register the renderer every time,
# but persist the page only when it is actually missing. A resident restart must
# not manufacture a new workspace revision.
_pure_workspace=current.visual.base.workspace
_existing_ids={p.get('id') for p in _pure_workspace().get('pages',[])}
_codrops_id=design_motion_registry.codrops_site_8x5.PAGE_ID
design_motion_registry.install(current)
if _codrops_id not in _existing_ids:
    current.visual.base.workspace()
current.visual.base.workspace=_pure_workspace
# ThreadingHTTPServer may process multiple editor mutations at once. Install the
# single-writer guard only after startup migrations are complete so runtime POSTs
# reload the latest workspace under one lock and cannot lose each other's edits.
import runtime_serialization
runtime_serialization.install(current.visual.base)
import candidate01_visual_graph_experiment
candidate01_visual_graph_experiment.install(current)
import design2_phase4_http,design2_phase5_http,design2_phase6_http,design2_phase7_http
design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)
design2_phase6_http.install(current.H,current.visual.base)
design2_phase7_http.install(current.H,current.visual.base)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',current.DORE_RUNTIME_IDENTITY['port']),current.H).serve_forever()