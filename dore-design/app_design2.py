#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 resident entrypoint: current product + Phase 4/5 APIs."""
import os
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design2_phase4_http,design2_phase5_http

design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)

if __name__=='__main__':
    ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),current.H).serve_forever()