#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
ui=(R/'design2_typography_ui.py').read_text();render=(R/'design2_cover_render.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ('TYPE','d2-font','d2-size','d2-weight','d2-color','d2-leading','d2-tracking','data-type-align','Apply type'):
    assert token in ui,token
for token in ('font_family','font-size','font-weight','line-height','letter-spacing','text-align','color'):
    assert token in render,token
assert 'design2_typography_ui.install' in app
assert "typography':'family+size+weight+color+leading+tracking+align'" in app
print('PASS Cover typography inspector contract')
