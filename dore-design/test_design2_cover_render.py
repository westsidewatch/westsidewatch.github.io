#!/usr/bin/env python3
from pathlib import Path
R=Path(__file__).resolve().parent
s=(R/'design2_cover_render.py').read_text();app=(R/'app_visual_v2.py').read_text()
for token in ('object-fit:{fit}','object-position:{pos}','data-id=','frame_stroke','class="canvas"'):assert token in s,token
assert "page_id=='multiwrite-cover'" in app
assert 'design2_cover_render.render' in app
print('PASS native cover renderer contract')
