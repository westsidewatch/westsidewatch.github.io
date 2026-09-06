#!/usr/bin/env python3
from pathlib import Path
root=Path(__file__).resolve().parent
layers=(root/'design2_layers_ui.py').read_text(encoding='utf-8')
ops=(root/'design2_layer_ops.py').read_text(encoding='utf-8')
assert 'draggable=true' in layers
assert "op:'reorder_node'" in layers
assert "patch:{hidden:!n.hidden}" in layers
assert "patch:{locked:!n.locked}" in layers
for marker in ('d2-x','d2-y','d2-w','d2-h','d2-geom-apply','d2-duplicate'):
    assert marker in layers, marker
assert "payload.get('op')!='reorder_node'" in ops
print('PASS design2 layers ui')
