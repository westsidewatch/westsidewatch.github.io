#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import html as html_lib
import os
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design_motion_registry
design_motion_registry.install(current)

# Production contract: Candidate 01 must visibly contain the same Third Alive 4W
# surface even if an upstream renderer wrapper is bypassed or reordered.
_candidate_render = current.multipage_wysiwyg.render_canvas

def _render_with_candidate_4w(page_id='homepage', edit=False):
    doc = _candidate_render(page_id, edit=edit)
    if page_id != current.living_water_candidate.PAGE_ID:
        return doc
    required = ('WATCH', 'WITNESS', 'WALK', 'WORSHIP')
    if 'data-current="4w"' in doc and all(word in doc for word in required):
        return doc
    four_w_html = current.living_water_third_alive_lab.render(edit=False)
    srcdoc = html_lib.escape(four_w_html, quote=True)
    block = (
        '<section class="candidate-third-alive-screen" data-current="4w" '
        'data-layer="navigation" data-screen="4" '
        'data-4w="WATCH WITNESS WALK WORSHIP" '
        'style="position:relative;min-height:100svh;height:100svh;overflow:hidden;background:#171817">'
        '<iframe title="Living Water Third Alive 4W" loading="eager" '
        'style="display:block;width:100%;height:100%;border:0;background:#171817" srcdoc="'
        + srcdoc + '"></iframe></section>'
    )
    anchor = '<section class="world dark">'
    if anchor not in doc:
        raise RuntimeError('candidate01_4w_anchor_missing')
    return doc.replace(anchor, block + anchor, 1)

current.multipage_wysiwyg.render_canvas = _render_with_candidate_4w

# Fail fast at process start if Candidate 01 still does not expose all four W labels.
_candidate_probe = current.multipage_wysiwyg.render_canvas(current.living_water_candidate.PAGE_ID, edit=False)
if 'data-current="4w"' not in _candidate_probe or not all(
    word in _candidate_probe for word in ('WATCH', 'WITNESS', 'WALK', 'WORSHIP')
):
    raise RuntimeError('candidate01_4w_contract_failed')

import design2_phase4_http,design2_phase5_http,design2_phase6_http,design2_phase7_http
design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)
design2_phase6_http.install(current.H,current.visual.base)
design2_phase7_http.install(current.H,current.visual.base)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),current.H).serve_forever()
