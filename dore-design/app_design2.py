#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import os
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design_motion_registry
# The Codrops 8:5 page is a startup migration. design_motion_registry installs a
# workspace wrapper whose legacy installer saves on every read; traverse it once
# to persist the runtime page, then restore the side-effect-free reader.
_pure_workspace=current.visual.base.workspace
design_motion_registry.install(current)
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
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),current.H).serve_forever()