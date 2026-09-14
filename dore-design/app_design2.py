#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import os
from http.server import ThreadingHTTPServer
from urllib.parse import urlparse
import app_visual_v2 as current
import design_motion_registry

# Stable runtime identity for A2A/Control Plane verification.
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

_pure_workspace=current.visual.base.workspace
_existing_ids={p.get('id') for p in _pure_workspace().get('pages',[])}
_codrops_id=design_motion_registry.codrops_site_8x5.PAGE_ID
design_motion_registry.install(current)
if _codrops_id not in _existing_ids:
    current.visual.base.workspace()
current.visual.base.workspace=_pure_workspace

import runtime_serialization
runtime_serialization.install(current.visual.base)
import candidate01_visual_graph_experiment
candidate01_visual_graph_experiment.install(current)

# Install the editorial research surface into the actual resident entrypoint.
import italian_editorial_atlas_runtime
italian_editorial_atlas_runtime.install(current)

import design2_phase4_http,design2_phase5_http,design2_phase6_http,design2_phase7_http
design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)
design2_phase6_http.install(current.H,current.visual.base)
design2_phase7_http.install(current.H,current.visual.base)

_BaseHandler = current.H
class _RuntimeIdentityHandler(_BaseHandler):
    def do_GET(self):
        if urlparse(self.path).path == '/api/runtime/identity':
            identity = dict(current.DORE_RUNTIME_IDENTITY)
            workspace = current.visual.base.workspace()
            identity['workspace_id'] = workspace.get('id')
            identity['workspace_revision'] = workspace.get('revision')
            identity['ok'] = (
                identity.get('service') == 'dore-design'
                and identity.get('version') == '2.0'
                and identity.get('entrypoint') == 'dore-design/app_design2.py'
            )
            return self.out(200 if identity['ok'] else 503, identity)
        return super().do_GET()
current.H = _RuntimeIdentityHandler

if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',current.DORE_RUNTIME_IDENTITY['port']),current.H).serve_forever()