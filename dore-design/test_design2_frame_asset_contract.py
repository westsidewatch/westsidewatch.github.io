#!/usr/bin/env python3
from pathlib import Path
ROOT=Path(__file__).resolve().parent
ops=(ROOT/'design2_layer_ops.py').read_text()
ui=(ROOT/'design2_arrange_ui.py').read_text()
canvas=(ROOT/'design2_canvas_state.py').read_text()
for token in ('add_frame','set_asset','frame_fill','frame_stroke'):
    assert token in ops,token
for token in ('+ Frame','+ Image','Apply fit','Apply position','Replace image','FileReader','place_image'):
    assert token in ui,token
for token in ('d2-frame-node','d2-image-node','backgroundImage','backgroundPosition','backgroundSize'):
    assert token in canvas,token
print('PASS design2 frame asset contract')
