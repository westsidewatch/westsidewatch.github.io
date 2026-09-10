#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import os
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design_motion_registry
design_motion_registry.install(current)
import design2_phase4_http,design2_phase5_http,design2_phase6_http,design2_phase7_http
design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)
design2_phase6_http.install(current.H,current.visual.base)
design2_phase7_http.install(current.H,current.visual.base)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),current.H).serve_forever()
