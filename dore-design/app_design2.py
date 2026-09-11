#!/usr/bin/env python3
"""DORÉ DESIGN 2.0 production resident entrypoint."""
import os
import re
from http.server import ThreadingHTTPServer
import app_visual_v2 as current
import design_motion_registry
design_motion_registry.install(current)

# Candidate 01: the four EXISTING currents across focus screens 2 and 3 are the 4W.
# Do not add a page/current and do not alter the locked motion.
_candidate_render = current.multipage_wysiwyg.render_canvas
_LABEL_STYLE = '''<style id="candidate-01-4w-labels">
.candidate-focus-screen{position:relative}
.candidate-4w-label{position:absolute;z-index:8;left:4vw;color:#CEBD74;font:500 11px/1.2 "Cormorant Garamond",serif;letter-spacing:.16em;text-transform:uppercase;pointer-events:none;text-shadow:0 1px 10px rgba(0,0,0,.18)}
.candidate-4w-label.current-a{top:3.1vh}.candidate-4w-label.current-b{top:51.1vh}
</style>'''

def _strip_wrong_third_alive(doc):
    return re.sub(r'<section class="candidate-third-alive-screen".*?</section>', '', doc, count=1, flags=re.S)

def _label_focus(doc, screen_no, first, second):
    marker = f'<section class="candidate-focus-screen" data-current="focus" data-layer="first" data-screen="{screen_no}">'
    labels = (f'<span class="candidate-4w-label current-a">{first}</span>'
              f'<span class="candidate-4w-label current-b">{second}</span>')
    return doc.replace(marker, marker + labels, 1)

def _render_candidate_4w_labels(page_id='homepage', edit=False):
    doc = _candidate_render(page_id, edit=edit)
    if page_id != current.living_water_candidate.PAGE_ID:
        return doc
    doc = _strip_wrong_third_alive(doc)
    if 'id="candidate-01-4w-labels"' not in doc:
        doc = doc.replace('</head>', _LABEL_STYLE + '</head>', 1)
    doc = _label_focus(doc, 2, '第一樂章 WATCH', '第二樂章 WITNESS')
    doc = _label_focus(doc, 3, '第三樂章 WALK', '第四樂章 WORSHIP')
    return doc

current.multipage_wysiwyg.render_canvas = _render_candidate_4w_labels

# Contract: exactly the existing two focus screens carry all four movement labels;
# the mistakenly embedded Third Alive page must not survive in Candidate 01.
_probe = current.multipage_wysiwyg.render_canvas(current.living_water_candidate.PAGE_ID, edit=False)
if 'candidate-third-alive-screen' in _probe or not all(x in _probe for x in (
    '第一樂章 WATCH','第二樂章 WITNESS','第三樂章 WALK','第四樂章 WORSHIP'
)):
    raise RuntimeError('candidate01_existing_currents_4w_contract_failed')

import design2_phase4_http,design2_phase5_http,design2_phase6_http,design2_phase7_http
design2_phase4_http.install(current.H,current.visual.base,current.ROOT)
design2_phase5_http.install(current.H,current.visual.base,current.ROOT)
design2_phase6_http.install(current.H,current.visual.base)
design2_phase7_http.install(current.H,current.visual.base)
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',int(os.environ.get('DORE_DESIGN_PORT','4310'))),current.H).serve_forever()
